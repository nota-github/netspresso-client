################# NETSPRESSO CLIENT ############################################################
# client 프로그램은 client 프로그램으로서의 역할과 동시에 API에 대한 설명을 하고 있습니다.
# 따라서 API동작에 대한 이해를 하기 쉽게, 과도한 추상화나 wrapping은 지양했습니다.
# 
# client 프로그램은 다음과 같이 세 부분으로 구성되어 있습니다.
# 1. compression을 하는 부분(파일 업로드 포함)
# 2. monitoring APIs 사용 부분
# 3. 결과 출력 및 파일 다운로드 부분
################################################################################################

import time
import sys
import yaml
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from netspresso_cli import settings
from netspresso_cli.clouds.aws import connection
from netspresso_cli.clouds.types import ReturnDataType, DataSetFormat, InputModelType
from netspresso_cli.clouds.compression_sessions import CompSession
from netspresso_cli.clouds .monitoring_apis import get_compression_status_list
from netspresso_cli.clouds.monitoring_apis import get_compression_status
from netspresso_cli.clouds.monitoring_apis import get_worker_status_list
from netspresso_cli.clouds.monitoring_apis import get_task_queue_size
from netspresso_cli.clouds.monitoring_apis import get_result
from netspresso_cli.clouds.monitoring_apis import download_log_file
from netspresso_cli.clouds.monitoring_apis import download_original_type_compressed_model_file
from netspresso_cli.clouds.monitoring_apis import download_converted_type_compressed_model_file
from netspresso_cli.clouds.monitoring_apis import delete_compression_id_in_task_queue

from netspresso_cli.clouds.common import get_argparse
from netspresso_cli.clouds.common import calculate_duration

from netspresso_cli.clouds.common import get_aws_info
from netspresso_cli.clouds.common import check_login

def main():
    ################### DO COMPRESSION ##############################################################
    args = get_argparse()
    if args.login:
        get_aws_info()
        exit(0)
    if not check_login():
        print("please login first")
        print("main.py --login")
        exit(0)
    with open(args.config) as f:
        configs = yaml.safe_load(f.read())
    comp_sess = CompSession()
    # upload config, data, model
    comp_sess.upload_config(config_path=args.config, storage_config=configs["STORAGE"])
    comp_sess.upload_data(data_path=configs["DATASET"]["path"], dataset_type=configs["DATASET"]["type"], storage_config=configs["STORAGE"])
    comp_sess.upload_model(model_path=configs["INPUT"]["path"], model_type=configs["INPUT"]["type"], storage_config=configs["STORAGE"])
    # Do compression session
    compression_id = comp_sess.compress()
    print(f"compression id: {compression_id}")
    #################################################################################################



    ##################### MONITORING APIS EXAMPLE ###################################################
    # if status == 3, break
    while True:
        current_status = get_compression_status(compression_id, return_type=ReturnDataType.JSON)
        current_compression_id = current_status["compression_id"]
        print("==========current status==========")
        print(current_status)
        print("==================================")
        if current_compression_id == None: # 요청한 compression_id가 없는 경우, 프로그램 종료
            print(f"compression_id({current_compression_id}) does not exists")
            exit(0)
        elif current_status["status"] != 0: # 도중에 error가 발생한 경우(status!=0), 프로그램 종료
            print("error in progressing")
            exit(0)
        elif current_status["progress"] == 1: # compression task가 queue에서 대기하고 있음.
            print("[*] compression task in queue!")
            print("[*] currently stacked compression queue size : ", get_task_queue_size())
        elif current_status["progress"] == 2:
            print("[*] compression is in progress.")
        elif current_status["progress"] == 3: # 정상적으로 프로세스가 완료된 경우
            print("compression completed!")
            break
        print(f"[*] running time in current step: ", calculate_duration(time_from=current_status["updated_time"]))
        print(f"[*] total time: ", calculate_duration(time_from=current_status["created_time"]))
        print("\n\n")
        time.sleep(20)

    #################################################################################################

    ##################### DOWNLOAD RESULT FILES######################################################
    aws_auth_info = connection.get_auth()
    result = get_result(compression_id, return_type=ReturnDataType.JSON)
    print(result)
    log_file = connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_log"])
    print(f"[*] log file(filename: {log_file}) saved")
    input_type_compressed_model = connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_input_type_compressed_model"])
    print(f"[*] input type compressed model(filename: {input_type_compressed_model}) saved")
    converted_type_compressed_model = connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_converted_type_compressed_model"])
    print(f"[*] converted type compressed model(filename: {converted_type_compressed_model}) saved")
    ################################################################################################


    ######################### FORMATTING OPTION EXAMPLES ###########################################
    print("[*] worker status as YAML format")
    print(get_worker_status_list(return_type=ReturnDataType.YAML))
    print("[*] compression status list as DATA_FRAME format")
    print(get_compression_status_list(return_type=ReturnDataType.DATA_FRAME))
    ################################################################################################

if __name__ == '__main__':
    main()
