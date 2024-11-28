from utils import LoggerFa, LoggerSi
from utils import send_log_file

PROJECT_NAME = "test"


@LoggerFa.time_execution()
@LoggerFa.monitor_resources_de()
def factory_test(message: str):

    pusher = LoggerFa.get_logger()

    pusher.error(message)

    # send_log_file(PROJECT_NAME)


@LoggerSi.time_execution()
@LoggerSi.monitor_resources_de()
def singleton_test(message: str):

    # LoggerSi.reset()

    LoggerSi.debug("This is an error message.", extra={"user": "John Doe"})

    # send_log_file(PROJECT_NAME)


if __name__ == "__main__":
    singleton_test("hello world!")
