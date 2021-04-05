import requests
import yaml
import json
import glob
import time
from pathlib import Path

from netspresso_real_client.modules import monitoring_apis
from netspresso_real_client.modules.types import ReturnDataType
from netspresso_real_client.modules import aws_connection

def run_netspresso(yaml_fname: str, uri: str)-> str:
    print("[*] netspresso started to compress.")
    yaml_fname = Path(yaml_fname).__str__()
    with open(yaml_fname, "rt") as f:
        dict_content = yaml.safe_load(f)
    print(dict_content)
    data = {
        "configs": dict_content,  # yaml config
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(
        f"http://{uri}/api/v1/compressions/create",
        data=json.dumps(data), headers=headers
    )
    return r.json()




# 1. compress
yaml_fname = "yaml_files/example1.yaml"
uri = "acfe62d997b9043858797f5154a0fc86-1177422271.us-east-2.elb.amazonaws.com:8000"
compression_id = run_netspresso(yaml_fname, uri)

# 2. monitor compression's status
start_time = time.time()
while True:
    compression_status = monitoring_apis.get_compression_status(compression_id, ReturnDataType.JSON)
    print("[*] compression_status: ", compression_status)
    if compression_status["status"] == 1:
        print("[*] error occured during compression.")
        break
    if compression_status["progress"] == 3:
        print(f"[*] compression completed: compression id({compression_id}) ")
        break
    current_time = time.time()
    time_delta = (current_time - start_time) / 60
    time_delta_formatted = f"{time_delta:.2f}"
    print("[*] compression is running. ")
    print(f"[*] time duration: {time_delta_formatted} minutes")
    time.sleep(10)

# 3. get result
if compression_status["status"] != 1 and compression_status["progress"] == 3:
    compression_result = monitoring_apis.get_result(compression_id, ReturnDataType.JSON)
    print(compression_result)
elif compression_status["status"] == 1 and compression_status["progress"] == 3: # error
    compression_result = monitoring_apis.get_result(compression_id, ReturnDataType.JSON)
    print(compression_result)

# 4. download files
if compression_status["status"] != 1 and compression_status["progress"] == 3:
    aws_auth_info = aws_connection.get_auth()
    log_file = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=compression_result["url_log"])
    print(f"[*] log file(filename: {log_file}) saved")
    input_type_compressed_model = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=compression_result["url_input_type_compressed_model"])
    print(f"[*] input type compressed model(filename: {input_type_compressed_model}) saved")
    converted_type_compressed_model = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=compression_result["url_converted_type_compressed_model"])
    print(f"[*] converted type compressed model(filename: {converted_type_compressed_model}) saved")