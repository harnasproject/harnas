import errno
import shutil

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
