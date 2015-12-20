# -*- coding=utf-8 -*-
# Copyright (c) 2014 Michał Zieliński <michal@zielinscy.org.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import requests
import json
import io
import os
import socket

try:
    import httplib
except ImportError:
    import http.client as httplib

URL = os.environ.get('HERA_URL', 'http://api.hera.dev/')

default_auth = None

_auth = os.environ.get('HERA_AUTH')
if _auth:
    default_auth = _auth.split(':')

def get_auth(auth):
    if not auth:
        if not default_auth:
            raise ValueError('Not authenticated (pass auth keyword argument ' \
                             'or set heraclient.default_auth)')
        auth = default_auth
    if not isinstance(auth, (tuple, list)) or len(auth) != 2 \
       or not all(map(lambda x: isinstance(x, (str, bytes)), auth)):
        raise ValueError('Bad auth data format (%r). Expected tuple of (login, api_key)' % auth)
    return tuple(auth)

class Sandbox(object):
    def __init__(self, id, auth=None):
        self.id = id
        self.auth = get_auth(auth)

    @classmethod
    def create(self, timeout, disk, owner='me', memory=128, whole_node=False, auth=None,
               async=False, webhook_url=None, webhook_secret=None, priority=None, priority_growth=None):
        if isinstance(disk, Template):
            disk = disk.id
        assert isinstance(memory, int)
        assert isinstance(timeout, (int, float))
        assert isinstance(disk, str)

        data = {
            'owner': owner,
            'timeout': timeout,
            'disk': disk,
            'memory': memory,
            'whole_node': 'true' if whole_node else 'false'
        }

        if async:
            data['webhook_url'] = webhook_url
            data['async'] = 'true'
            if webhook_secret: data['webhook_secret'] = webhook_secret
            if priority is not None: data['priority'] = priority
            if priority_growth is not None:  data['priority_growth'] = priority_growth
        else:
            assert not priority_growth
            assert not priority
            assert not webhook_url
            assert not webhook_secret

        resp = requests.post(URL + 'sandbox/', data=data, auth=get_auth(auth))
        response_raise(resp)

        if not async:
            resp = resp.json()
            return Sandbox(resp['id'], auth=auth)

    def save_as_template(self, name=None):
        assert isinstance(name, (type(None), str))
        resp = self.action('create_template', name=name)
        return Template(resp['id'])

    def execute(self, args, sync=False, chroot=True, shell=False,
                stderr_to_stdout=False, pty_size=None):
        '''
        Execute process in sandbox.
        '''
        kwargs = dict(sync='true' if sync else 'false',
                      chroot='true' if chroot else 'false')
        if shell:
            assert isinstance(args, str)
            kwargs['command'] = args
        else:
            assert all( isinstance(param, str) for param in args )
            kwargs['args'] = json.dumps(args)

        if pty_size:
            kwargs['pty_size'] = json.dumps(pty_size)

        if stderr_to_stdout:
            kwargs['stderr'] = 'stdout'

        resp = self.action('exec', **kwargs)
        return Process(resp, sync=sync)

    def unpack(self, archive_type, archive, archive_size=None, compress_type='', target='/'):
        resp = self.action('unpack', target=target, archive_type=archive_type,
                           compress_type=compress_type)
        input = Stream(resp['input'])
        error = None
        try:
            input.upload_file(archive, archive_size)
        except socket.error as err:
            # For "Connection reset by peer" error message from 'output' will be
            # more useful.
            if err.errno != 104:
                raise
            error = err
        result = Stream(resp['output']).download()
        response_raise(result)
        if error: raise

    def wait(self):
        self.action('wait')

    def kill(self):
        self.action('kill')

    def action(self, type, **args):
        resp = requests.post(URL + 'sandbox/%s/%s' % (self.id, type), data=args,
                             auth=self.auth)
        response_raise(resp)
        return resp.json()

class Process(object):
    def __init__(self, resp, sync):
        self.resp = resp
        self.sync = sync
        if not self.sync:
            self.stdin = Stream(resp['stdin'])
            if resp['stdin'] == resp['stdout']:
                self.stdout = self.stdin
            else:
                self.stdout = Stream(resp['stdout'])
            if 'stderr' in resp:
                self.stderr = Stream(resp['stderr'])

    def read_stdout(self):
        return self._read_stream('stdout')

    def read_stderr(self):
        return self._read_stream('stderr')

    def _read_stream(self, name):
        if self.sync:
            return self.resp[name]
        else:
            return getattr(self, name).download().content

class Template(object):
    def __init__(self, id, auth=None, data=None):
        self.id = id
        self.auth = get_auth(auth)
        if not data:
            resp = requests.get(URL + 'template/%s' % self.id, auth=self.auth)
            response_raise(resp)
            data = resp.json()
        self.name = data['name']
        self.public = data['public']

    def change(self, public=None, name=None):
        req = filter_out_if_none(dict(public=public, name=name))
        resp = requests.post(URL + 'template/%s' % self.id, auth=self.auth, data=req)
        response_raise(resp)
        if public is not None:
            self.public = public
        if name is not None:
            self.name = name

    @classmethod
    def list(self, auth=None):
        auth = get_auth(auth)
        resp = requests.get(URL + 'template/', auth=auth)
        response_raise(resp)
        return [ Template(item['id'], auth=auth, data=item)
                 for item in resp.json()['templates'] ]

def response_raise(resp):
    resp.raise_for_status()
    resp = resp.json()
    if resp.get('status') != 'ok':
        msg = 'Service returned error %r.' % resp.get('status')
        stacktrace = resp.get('stacktrace')
        if stacktrace:
            msg += '\n' + stacktrace
        raise ApiError(msg)

def filter_out_if_none(dict):
    return { k:v for k,v in dict.items() if v is not None }

def new_disk(size):
    return 'new,%s' % size

def get_cluster(auth=None):
    resp = requests.get(URL + 'cluster/', auth=get_auth(auth))
    response_raise(resp)
    return resp.json()['nodes']

class ApiError(Exception):
    pass

# Websocket streams

class _StreamBase(object):
    def __init__(self, urls):
        self.urls = urls
        self._websocket_conn = None
        self._closed = False

    def download(self):
        return requests.get(self.urls['http'], stream=True)

    def upload(self, data):
        return self._upload(io.BytesIO(data), len(data))

    def upload_file(self, file_obj_or_name, size=None):
        if isinstance(file_obj_or_name, str):
            if not size:
                size = os.path.getsize(file_obj_or_name)
            fileobj = open(file_obj_or_name, 'r')
        else:
            fileobj = file_obj_or_name
            assert size is not None

        return self._upload(fileobj, size)

    def _upload(self, stream, size):
        if self._websocket_conn:
            raise IOError('Websocket connection alread opened - cannot upload via HTTP')
        self._closed = True
        conn, path = self._make_connection(self.urls['http'])
        if size is None:
            conn.putrequest('GET', path)
        else:
            conn.putrequest('POST', path)
            conn.putheader('Content-Length', size)
        conn.endheaders()
        if size is not None:
            while size > 0:
                data = stream.read(min(size, 4096))
                if not data:
                    raise IOError('incomplete read from upload source')
                conn.send(data)
                size -= len(data)
        resp = conn.getresponse()
        if resp.status != 200:
            raise ApiError('call to proxy returned code %d' % resp.status)
        return resp

    def _make_connection(self, url):
        proto, rest = url.split('://', 1)
        if proto == 'http':
            clazz = httplib.HTTPConnection
        elif proto == 'https':
            clazz = httplib.HTTPSConnection
        else:
            raise ValueError('unknown protocol %r' %  proto)
        host, _, path = rest.partition('/')
        return clazz(host), '/' + path

class _BufferedInputFileMixin(object):
    def __init__(self):
        self.__buff = ''

    def read_some(self):
        if not self.__buff:
            data = self._unbuffered_read()
            return data
        else:
            buff = self.__buff
            self.__buff = ''
            return buff

    def read(self, n=2**64):
        buff = []
        length_left = n
        while length_left > 0:
            data = self.read_some()
            if not data:
                break
            buff.append(data)
            length_left -= len(data)
        data = ''.join(buff)
        leftover = data[n:]
        if leftover:
            self.unread(leftover)
        return data[:n]

    def unread(self, data):
        if self.__buff:
            raise IOError('unread buffer used')
        self.__buff = data

    def readline(self):
        data = []
        while True:
            frag = self.read_some()
            if not frag:
                break
            index = frag.find(b'\n')
            if index != -1:
                data.append(frag[:index + 1])
                self.unread(frag[index + 1:])
                break
        return b''.join(data)

try:
    import websocket
except (ImportError, SyntaxError) as err:
    import_error = err
    class Stream(_StreamBase):
        def read(self, n=None):
            raise import_error

        def write(self, data):
            raise import_error

        def close(self, data):
            raise import_error

        def read_some(self):
            raise import_error
else:
    class Stream(_StreamBase, _BufferedInputFileMixin):
        def __init__(self, urls):
            _StreamBase.__init__(self, urls)
            _BufferedInputFileMixin.__init__(self)

        @property
        def websocket_conn(self):
            if self._closed:
                raise IOError('Connection closed')
            if not self._websocket_conn:
                url = self.urls['websocket']
                self._websocket_conn = websocket.create_connection(url)
            return self._websocket_conn

        def _unbuffered_read(self):
            return self.websocket_conn.recv()

        def write(self, data):
            self.websocket_conn.send(data)

        def close(self):
            if not self._closed:
                self.websocket_conn.close()
                self._closed = True
