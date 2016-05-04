import errno
import os
import shutil

from django.conf import settings
from django.db import transaction


def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            raise e


def save_task(task):
    try:
        with transaction.atomic():
            task.save()
        return True
    except Exception as e:
        print('Error while saving task: %s' % e)
        return False


def get_task_dir(task_id):
    return os.path.join(settings.TASK_STORAGE_PREFIX, str(task_id))


def save_testcase_file(file, dest_dir):
    dest_path = os.path.join(dest_dir, file.name)
    with open(dest_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
