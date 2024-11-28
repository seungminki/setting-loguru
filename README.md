# setting-loguru

## Overview
글을 못 써서 이런거 적는 게 정말 힘드네요...

## 🛠️ What Has Changed
**[Version 0.0.1]**: Factory Pattern으로 이루어진 logger utils
1. 서로 다른 설정의 logger 객체를 여러 개 생성해서(범용적으로) 사용하려고 했던 듯...
2. 근데 설정이 한개라 factory method pattern으로 애매하게 끝남.
3. v0.0.0 에서는 정해진 파라미터만 로그를 남길 수 있었지만, 동적으로 수행할 수 있도록 변경함.
4. 파일로 만들어진 로그를 Elastic Search로 보내는 모듈을 분리함. (es_handler.py)


**[Version 0.0.2]**: 다음과 같은 이유로 singleton pattern을 적용한 logger utils을 추가함.
1. 각 단계가 각각의 컨테이너로 이루어져 있는 환경이므로 컨테이너 당 로그파일을 하나만 사용하고, 주기적으로 ES로 보내지고 초기화되는 작업이 반복됨.
2. A 모듈은 DEBUG 로그를 파일에 저장하려 하고, B 모듈은 ERROR만 출력하려고 하는 경우가 없기 때문에, 다르게 적용할 필요가 없음. (다양한 요구사항 충족)
3. 기존의 pusher = Pusher.get_logger() 호출을 누락할 가능성. (로거 재사용?)
4. "lazy initialization" 방식으로, 필요할 때만 초기화, 반복적인 초기화 X -> 불필요한 객체 생성을 방지하여 메모리와 초기화 비용 줄임.
5. 다중 스레드 환경?에서의 단점은 아직 공부중... KFP에서 발생할 수 있는 환경인지는 모르겠음.

## example

* quick-start
```sh
main.py 참고
```

* 동적으로 사용하기
```sh
Logger.info("Server started successfully")
# {"@timestamp": "2024-11-27T16:54:56+0900", "message": "Server started successfully", "levelname": "INFO"}

Logger.info(
    "Debugging user session",
    extra={
        "type": "debug",
        "user_id": 101,
        "session_id": "abc123",
    },
)
# {"@timestamp": "2024-11-27T16:54:56+0900", "message": "Debugging user session", "levelname": "INFO", "extra": {"type": "debug", "user_id": 101, "session_id": "abc123"}}

Logger.debug(
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
from utils import Logger

def test():
    Logger.monitor_resources(func_or_str="test")

# 2024-11-27 13:18:58.381 | INFO | utils.tools:monitor_resources:177 - Function test CPU Count: 20, Total Memory usage : 15852MB, Available Memory usage : 13303MB, Used Percent Memory usage : 16.1%
```

* Decorator로 사용하기
```sh
from utils import Logger

@Logger.time_execution()
@Logger.monitor_resources_de() # = monitor_resources
def test():
    return 0

# 2024-11-27 13:22:02.262 | INFO | utils.tools:monitor_resources:185 - Function test CPU Count: 20, Total Memory usage : 15852MB, Available Memory usage : 13274MB, Used Percent Memory usage : 16.3%
# 2024-11-27 13:22:02.263 | INFO | utils.tools:time_wrapper:144 - Time spent on test: 0.0022 seconds
```