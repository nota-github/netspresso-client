import os
from netspresso_cli.common import types

class API_SERVER:
    # HOST = "localhost"
    # PORT = 22080
    HOST = "143.248.251.119"
    PORT = 12080
    TARGET_URL = "http://" + HOST + ":" + str(PORT)

RESULT_DIR = "result"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVICE_TYPE = types.API_SERVICE_TYPE.ONPREM