from functools import wraps

from loguru import logger
import psutil

import json
import sys
import time

from pytz import timezone
from datetime import datetime

from settings import LOG_FILE_PATH

today = datetime.now(timezone("Asia/Seoul"))


class Pusher:
    _logger = False

    @classmethod
    def get_logger(cls):
        if not cls._logger:

            def _serialize(record):
                subset = {
                    "@timestamp": record["timestamp"],
                    "message": record["message"],
                    "levelname": record["level"].name,
                }

                subset.update(record["extra"])

                return json.dumps(subset)

            def _patching(record):
                _dt = today.strftime("%Y-%m-%dT%H:%M:%S%z")
                record["timestamp"] = _dt

                record["extra"]["serialized"] = _serialize(record)

            logger.configure(patcher=_patching)
            logger.add(  # console
                LOG_FILE_PATH,
                format="{extra[serialized]}",
                level="DEBUG",
            )

            logger.add(  # file_log
                sys.stderr,
                format="{extra[serialized]}",
                level="DEBUG",
            )

            cls._logger = logger

        return cls._logger

    @classmethod
    def time_execution(cls):
        def time_decorator(func):
            @wraps(func)
            def time_wrapper(*args, **kwargs):
                # global_logger.info(f"Function '{func.__name__}' started")
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                total_time = end_time - start_time
                cls.get_logger().info(
                    f"Time spent on {func.__name__}: {total_time:.4f} seconds"
                )
                return result

            return time_wrapper

        return time_decorator

    @classmethod
    def monitor_resources(cls, func_or_str=None, memory=True, cpu=True):
        def _memory_usage():
            mem = psutil.virtual_memory()
            total_mem = mem.total >> 20
            available_mem = mem.available >> 20
            mem_percent = mem.percent

            return total_mem, available_mem, mem_percent

        def _cpu_usage():
            c_count = psutil.cpu_count(logical=True)
            return c_count

        total_mem = available_mem = mem_percent = c_count = "None"
        if memory:
            total_mem, available_mem, mem_percent = _memory_usage()
        if cpu:
            c_count = _cpu_usage()

        if isinstance(func_or_str, str):
            func_name = str(func_or_str)
            cls.get_logger().info(
                f"Function {func_name} CPU Count: {c_count}, Total Memory usage : {total_mem}MB, Available Memory usage : {available_mem}MB, Used Percent Memory usage : {mem_percent}%",
            )

        else:
            func = func_or_str
            cls.get_logger().info(
                f"Function {func.__name__} CPU Count: {c_count}, Total Memory usage : {total_mem}MB, Available Memory usage : {available_mem}MB, Used Percent Memory usage : {mem_percent}%",
                type="usage",
                detail_index="model",
            )

    @classmethod
    def monitor_resources_de(cls, cpu=True, memory=True):
        def resources(func):
            @wraps(func)
            def resources_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                cls.monitor_resources(func_or_str=func, cpu=cpu, memory=memory)
                return result

            return resources_wrapper

        return resources
