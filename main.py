from utils import Pusher, send_log_file

PROJECT_NAME = "test"


@Pusher.time_execution()
@Pusher.monitor_resources_de()
def test(message: str):

    pusher = Pusher.get_logger()

    pusher.error(message)

    send_log_file(PROJECT_NAME)


if __name__ == "__main__":
    test("hello world!")
