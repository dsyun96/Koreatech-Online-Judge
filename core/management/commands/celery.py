import shlex
import subprocess
import os
import logging

from django.core.management.base import BaseCommand
from django.utils import autoreload

logger = logging.getLogger()


def restart_celery():
    cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(cmd))

    env = os.environ.copy()  # 현재의 환경변수 Copy
    env.update({"C_FORCE_ROOT": "1"})  # 사용할 환경 변수 Update

    cmd = 'celery -A config worker'
    subprocess.call(shlex.split(cmd), env=env)  # 환경 변수를 적용하여 Celery 실행


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info('Start Celery Worker with Auto Restart...')
        autoreload.run_with_reloader(restart_celery)
