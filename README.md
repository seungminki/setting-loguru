# setting-loguru

## example

* quick-start
```sh
from utils import Pusher, send_log_file

if __name__ == "__main__":
    pusher = Pusher.get_logger()

    # logging

    project_name = "test"
    send_log_file(project_name)
```

* 동적으로 사용하기
```sh
pusher.info("Server started successfully")
# {"@timestamp": "2024-11-27T16:54:56+0900", "message": "Server started successfully", "levelname": "INFO"}

pusher.info(
    "Debugging user session",
    extra={
        "type": "debug",
        "user_id": 101,
        "session_id": "abc123",
    },
)
# {"@timestamp": "2024-11-27T16:54:56+0900", "message": "Debugging user session", "levelname": "INFO", "extra": {"type": "debug", "user_id": 101, "session_id": "abc123"}}

pusher.debug(
    "User login successful",
    extra={
        "type": "authentication",
        "user_id": 101,
        "ip_address": "192.168.1.1"
    },
)
# {"@timestamp": "2024-11-27T16:54:56+0900", "message": "User login successful", "levelname": "DEBUG", "extra": {"type": "authentication", "user_id": 101, "ip_address": "192.168.1.1"}}
```
* monitor_resources in func
```sh
from utils import Pusher

def test():
    Pusher.monitor_resources(func_or_str="test")

# 2024-11-27 13:18:58.381 | INFO | utils.tools:monitor_resources:177 - Function test CPU Count: 20, Total Memory usage : 15852MB, Available Memory usage : 13303MB, Used Percent Memory usage : 16.1%
```



* Decorator로 사용하기
```sh
from utils import Pusher

@Pusher.time_execution()
@Pusher.monitor_resources_de() # = monitor_resources
def test():
    return 0

# 2024-11-27 13:22:02.262 | INFO | utils.tools:monitor_resources:185 - Function test CPU Count: 20, Total Memory usage : 15852MB, Available Memory usage : 13274MB, Used Percent Memory usage : 16.3%
# 2024-11-27 13:22:02.263 | INFO | utils.tools:time_wrapper:144 - Time spent on test: 0.0022 seconds
```