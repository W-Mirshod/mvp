import multiprocessing
from datetime import timedelta
from functools import wraps
from time import perf_counter


def time_it(func):
    @wraps(func)
    def run_time(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
       # logger.debug(f"'{func.__name__}' = {timedelta(seconds=perf_counter() - t0)}")
        return result

    return run_time


class CeleryConstants:
    """CeleryConstants"""

    Y_M_D_FORMAT = "%Y-%m-%d"
    Y_M_D_H_M_FORMAT = "%Y-%m-%d %H:%M"
    Y_M_D_H_M_S_FORMAT = "%Y-%m-%d %H:%M:%S"
    Y_M_D_H_M_S_F_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    Y_M_D_H_M_S_Z_FORMAT = "%Y-%m-%d %H:%M:%S %z"


    """Celery ->"""
    cpu_count = multiprocessing.cpu_count()

    DEFAULT_QUEUE = "celery"
    DEFAULT_WORKER_NAME = "main"
    DEFAULT_CONCURRENCY = 1

    GENERAL_QUEUE = "general"
    GENERAL_WORKER_NAME = "general"
    GENERAL_CONCURRENCY = 2
    GENERAL_TASK_PREFIX = "general"

    DATA_PROCESSING_QUEUE = "data_processing"
    DATA_PROCESSING_WORKER_NAME = "data_processing"
    DATA_PROCESSING_CONCURRENCY = min([cpu_count, 4])
    DATA_PROCESSING_TASK_PREFIX = "data_processing"
    """<- Celery"""