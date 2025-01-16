"""
run:
    python manage.py runscript celery_scripts.kill_workers
"""

from celery_scripts.restart_workers import RestartWorkers
from celery_scripts.constants import CeleryConstants

def run() -> None:
    RestartWorkers.kill_celery_worker(
        worker_name=CeleryConstants.DATA_PROCESSING_WORKER_NAME,
    )
    RestartWorkers.kill_celery_worker(
        worker_name=CeleryConstants.GENERAL_WORKER_NAME,
    )
    RestartWorkers.kill_celery_worker(
        worker_name=CeleryConstants.DEFAULT_WORKER_NAME,
    )

    return None
