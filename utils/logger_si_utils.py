# singleton pattern

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


class LoggerSi:
    _logger = None
    project_name = None

    @classmethod
    def _initialize_logger(cls):
        def _serialize(record):
            subset = {
                "@timestamp": record["timestamp"],
                "message": record["message"],
                "levelname": record["level"].name,
            }
            subset.update(record["extra"])
            return json.dumps(subset)

        def _patching(record):
            _dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
            record["timestamp"] = _dt
            record["extra"]["serialized"] = _serialize(record)

        logger.configure(patcher=_patching)
        logger.add(  # Console log
            sys.stderr,
            format="{extra[serialized]}",
            level="DEBUG",
        )
        logger.add(  # File log
            LOG_FILE_PATH,
            format="{extra[serialized]}",
            level="DEBUG",
        )
        return logger

    # @classmethod
    # def reset(cls):
    #     if cls._logger:
    #         for handler in cls._logger.handlers[:]:
    #             cls._logger.removeHandler(handler)
    #             handler.close()
    #     cls._logger = None

    @classmethod
    def log(cls, level, message, **kwargs):
        if cls._logger is None:
            cls._logger = cls._initialize_logger()
        log_func = getattr(cls._logger, level, None)
        if log_func:
            log_func(message, **kwargs)
        else:
            raise ValueError(f"Invalid log level: {level}")

    @classmethod
    def debug(cls, message, **kwargs):
        cls.log("debug", message, **kwargs)

    @classmethod
    def info(cls, message, **kwargs):
        cls.log("info", message, **kwargs)

    @classmethod
    def warning(cls, message, **kwargs):
        cls.log("warning", message, **kwargs)

    @classmethod
    def error(cls, message, **kwargs):
        cls.log("error", message, **kwargs)

    @classmethod
    def critical(cls, message, **kwargs):
        cls.log("critical", message, **kwargs)

    @classmethod
    def time_execution(cls):
        def time_decorator(func):
            @wraps(func)
            def time_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                total_time = end_time - start_time
                cls.info(f"Time spent on {func.__name__}: {total_time:.4f} seconds")
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
            cls.info(
                f"Function {func_name} monitor resources",
                extra={
                    "CPU Count": c_count,
                    "Total Memory usage": f"{total_mem}MB",
                    "Available Memory usage": f"{available_mem}MB",
                    "Used Percent Memory usage": f"{mem_percent}%",
                },
            )

        else:
            func = func_or_str
            cls.info(
                f"Function {func.__name__} monitor resources",
                extra={
                    "CPU Count": c_count,
                    "Total Memory usage": f"{total_mem}MB",
                    "Available Memory usage": f"{available_mem}MB",
                    "Used Percent Memory usage": f"{mem_percent}%",
                },
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
