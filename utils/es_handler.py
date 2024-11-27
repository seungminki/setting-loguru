from elasticsearch import Elasticsearch
from elasticsearch import helpers

import json

from pytz import timezone
from datetime import datetime

from settings import ES_HOST, ES_PORT, ES_INDEX_FORMAT_LOG, LOG_FILE_PATH

today = datetime.now(timezone("Asia/Seoul"))


def _alter(line: str, project_name: str, **kwargs):
    j_line = json.loads(line.strip())
    j_line.update(kwargs)

    if "extra" in j_line:
        _ = j_line.pop("extra")
        j_line.update(_)

    es_index_name = ES_INDEX_FORMAT_LOG.format(
        project_name=project_name,
    )

    return {"_index": es_index_name, "_source": j_line}


def _bulk(client, data: list, chunk_size: int = 100):
    try:
        client = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")

        for chunked in [
            data[i : i + chunk_size] for i in range(0, len(data), chunk_size)
        ]:
            helpers.bulk(client, chunked)
        return True
    except ConnectionError as ce:
        print("Error occurred during bulk data", str(ce))
        return False
    except Exception as e:
        print("Error occurred during bulk data", str(e))
        return False


def send_log_file(project_name: str):
    log_files = [LOG_FILE_PATH]
    # for filename in os.listdir("./log"):
    #     if filename.endswith(".log"):
    #         log_files.append(filename)

    log_entries = []
    for file_name in log_files:
        try:
            with open(LOG_FILE_PATH, "r") as file:
                for line in file:
                    _mes = _alter(line, project_name)
                    log_entries.append(_mes)
            return 0

        except FileNotFoundError as fnfe:
            print(f"Log directory not found: {fnfe}")

        except Exception as e:
            print(f"Error indexing log: {e}")
