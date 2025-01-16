"""
run:
    python manage.py runscript celery_scripts.restart_workers
or:
    from celery_scripts.restart_workers import RestartWorkers
    # workers names = main, general, log_processing, parser
    RestartWorkers.restart_workers(restart_all=False, worker_name="general")
"""

import logging
import os
from time import sleep

from django.utils.timezone import now

from celery_scripts.constants import CeleryConstants, time_it

from config.settings import DEBUG

logger = logging.getLogger(__name__)


def run() -> None:
    RestartWorkers.restart_workers()
    return None


class RestartWorkers:
    @classmethod
    @time_it
    def restart_workers(cls, restart_all: bool = True, worker_name: str = "") -> None:
        if DEBUG:
            log_lvl = "info"
        else:
            log_lvl = "warning"

        date_str = now().strftime(CeleryConstants.Y_M_D_FORMAT)

        """
        1. Main queue ->
        !!! ALWAYS 'celery' !!!
        """
        if restart_all or worker_name == CeleryConstants.DEFAULT_WORKER_NAME:
            cls.kill_celery_worker(
                worker_name=CeleryConstants.DEFAULT_WORKER_NAME,
            )
            cls.start_celery_worker(
                worker_name=CeleryConstants.DEFAULT_WORKER_NAME,
                queue_name=CeleryConstants.DEFAULT_QUEUE,
                concurrency_number=CeleryConstants.DEFAULT_CONCURRENCY,
                log_lvl=log_lvl,
                log_date=date_str,
                with_beat=True,
                with_autoscale=False,
                autoscale_value="",
            )
        """ <- Main queue """

        """ 2. Custom 'general' queue -> """
        if restart_all or worker_name == CeleryConstants.GENERAL_WORKER_NAME:
            cls.kill_celery_worker(
                worker_name=CeleryConstants.GENERAL_WORKER_NAME,
            )
            cls.start_celery_worker(
                worker_name=CeleryConstants.GENERAL_WORKER_NAME,
                queue_name=CeleryConstants.GENERAL_QUEUE,
                concurrency_number=CeleryConstants.GENERAL_CONCURRENCY,
                log_lvl=log_lvl,
                log_date=date_str,
                with_beat=False,
                with_autoscale=True,
                autoscale_value=f"{CeleryConstants.GENERAL_CONCURRENCY + 2},1",
            )
        """ <- Custom 'general' queue """

        """ 3. Custom 'data_processing' queue -> """
        if restart_all or worker_name == CeleryConstants.DATA_PROCESSING_WORKER_NAME:
            cls.kill_celery_worker(
                worker_name=CeleryConstants.DATA_PROCESSING_WORKER_NAME,
            )
            cls.start_celery_worker(
                worker_name=CeleryConstants.DATA_PROCESSING_WORKER_NAME,
                queue_name=CeleryConstants.DATA_PROCESSING_QUEUE,
                concurrency_number=CeleryConstants.DATA_PROCESSING_CONCURRENCY,
                log_lvl=log_lvl,
                log_date=date_str,
                with_beat=True,
                with_autoscale=True,
                autoscale_value=f"{CeleryConstants.DATA_PROCESSING_CONCURRENCY + 2},1",
            )
        """ <- Custom 'data_processing' queue """

        return None

    @staticmethod
    def kill_celery_worker(worker_name: str) -> None:
        try:
            """find worker pid file"""
            stream = os.popen(f"ls ./logs/{worker_name}_worker.pid")
            if worker_pid_file := [i for i in str(stream.read()).split("\n") if i]:
                with open(worker_pid_file[0], "r") as pid_file:
                    pid_id = str(pid_file.read()).replace("\n", "")
                    """ kill worker process """
                    os.system(f"kill -HUP {pid_id}")
                    pid_file.close()
        except Exception as ex:
           pass
        else:
            logger.info(f"celery worker stopped; {worker_name = }")
            """ wait server to stop precess """
            sleep(2)

            if worker_pid_file:
                try:
                    """remove worker pid file if not self-deleted"""
                    os.system(f"rm {worker_pid_file[0]}")
                except Exception as ex:
                   pass

        return None

    @staticmethod
    def start_celery_worker(
        worker_name: str,
        queue_name: str,
        concurrency_number: int,
        log_lvl: str,
        log_date: str,
        with_beat: bool,
        with_autoscale: bool,
        autoscale_value: str,
    ) -> None:
        if with_autoscale:
            autoscale = f"--autoscale={autoscale_value}"
        else:
            autoscale = ""
        try:
            os.system(
                f"celery multi start worker"
                f" --app=config"
                f" --loglevel={log_lvl}"
                f" --concurrency={concurrency_number}"
                f" {'--beat' if with_beat else ''}"
                f" --queues={queue_name}"
                f" {autoscale}"
                f" --hostname=mm_back_{queue_name}@%n"
                f" --pidfile=./logs/{worker_name}_%n.pid"
                f" --logfile=./logs/{worker_name}_%n_{log_date}.log"
            )
        except Exception as ex:
            pass
        else:
            logger.info(f"celery worker started")

        return None
