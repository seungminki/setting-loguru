import os

ES_HOST = os.getenv("ES_HOST", "dev-es.co.kr")
ES_PORT = os.getenv("ES_PORT", 9200)

ES_INDEX_FORMAT_LOG = "{project_name}"
# ES_INDEX_FORMAT_LOG = "{project_name}-{today}"
# ES_INDEX_FORMAT_LOG = "{mode}_{deepfm_{detail_index}_{course}_{grade}_{author}-{today}"
LOG_FILE_PATH = "./log/out.log"
