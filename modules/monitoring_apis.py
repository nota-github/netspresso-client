import requests
import os
from urllib.request import urlretrieve

import settings
from modules.types import ReturnDataType, DataSetFormat
from modules.codec import encoder


def get_compression_status_list(
    return_type: ReturnDataType = ReturnDataType.JSON,
) -> ReturnDataType:
    r = requests.get(
        f"http://{settings.API_SERVER.HOST}:{settings.API_SERVER.PORT}/api/v1/compressions"
    )
    return encoder(json_data=r.json(), output_format=return_type)


def get_worker_status_list(
    return_type: ReturnDataType = ReturnDataType.JSON,
) -> ReturnDataType:
    r = requests.get(
        f"http://{settings.API_SERVER.HOST}:{settings.API_SERVER.PORT}/api/v1/worker_status_list"
    )
    return encoder(json_data=r.json(), output_format=return_type)


def get_compression_status(compression_id: str, return_type: ReturnDataType = ReturnDataType.JSON):
    r = requests.get(
        f"http://{settings.API_SERVER.HOST}:{settings.API_SERVER.PORT}/api/v1/compressions/{compression_id}"
    )
    return encoder(json_data=r.json(), output_format=return_type)

def get_result(
    compression_id: str,
    return_type: ReturnDataType = ReturnDataType.JSON,
) -> ReturnDataType:
    r = requests.get(
        f"http://{settings.API_SERVER.HOST}:{settings.API_SERVER.PORT}/api/v1/compressions/{compression_id}/result"
    )
    return encoder(json_data=r.json(), output_format=return_type)


def download_log_file(compression_id: str, dst_folder_path:str, download_url: str)->None:
    return download_file(compression_id, dst_folder_path, download_url)

def download_original_type_compressed_model_file(compression_id: str, dst_folder_path:str, download_url: str)->None:
    return download_file(compression_id, dst_folder_path, download_url)

def download_converted_type_compressed_model_file(compression_id: str, dst_folder_path:str, download_url: str)->None:
    return download_file(compression_id, dst_folder_path, download_url)


def download_file(compression_id: str, dst_folder_path:str, target_url: str)->None:
    # get file name
    target_filename = None
    pre_response = requests.head(target_url)
    if pre_response.status_code >= 400: # there is an error
        print("download_log_file failed!")
    else:
        try:
            target_filename = pre_response.headers["Content-Disposition"].split("=")[1].strip("\"")
            target_path = os.path.join(dst_folder_path, target_filename)
            urlretrieve(target_url, target_path)
        except Exception as e:
            print(f"error occured! {e}")
            exit(0)
    return target_filename