import sys, os

app_name = 'harnas'
env_name = 'harnas'

cwd = os.getcwd()
sys.path.append(cwd + '/../')
sys.path.append(cwd)

INTERP = '/home/harnas' + '/.venvs/' + env_name + '/bin/python'
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, cwd + '/.venvs/' + env_name + '/bin')
sys.path.insert(0, cwd + '/.venvs/' + env_name + '/lib/python3.4/site-packages/django')
sys.path.insert(0, cwd + '/.venvs/' + env_name + '/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()