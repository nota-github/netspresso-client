import requests
import json

from netspresso_cli import settings
from urllib.parse import urljoin

def create_compression(user_key,
        config_json_path,
        custom_model_dataset=False,
        model_url=None,
        dataset_url=None,
        compression_title=None,
        destination_path_s3=None
        ):
    target_url_path = "/api/v1/compressions/create"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    with open(config_json_path) as f:
        data = json.load(f)
    
    if custom_model_dataset:
        if model_url:
            data["configs"]["INPUT"]["path"] = model_url
        if dataset_url:
            data["configs"]["DATASET"]["path"]["zip_dir"] = dataset_url
    if compression_title:
        data["configs"]["COMPRESSION_ALIAS"] = compression_title
    if destination_path_s3:
        data["configs"]["STORAGE"]["destination_path"] = "/" + destination_path_s3
    res = requests.post(target_url, headers=headers, json=data)
    return res.json()

def delete_compression(user_key, compression_id):
    target_url_path = f"/api/v1/compressions/{compression_id}/delete"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    res = requests.post(target_url, headers=headers)
    return res.json()

def delete_task_queue(user_key, compression_id):
    target_url_path = "/api/v1/task_queue/delete"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    data = {"compression_id": compression_id}

    res = requests.post(target_url, headers=headers, json=data)
    ret_val = f"{res.text.strip()} items affected"
    return ret_val

def kill_core_process(user_key, compression_id):
    target_url_path = f"/api/v1/compressions/{compression_id}/kill"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    res = requests.get(target_url, headers=headers)
    return res.text

def restart_process(user_key, compression_id):
    target_url_path = f"/api/v1/compressions/{compression_id}/restart"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    res = requests.get(target_url, headers=headers)
    return res.text

def upload_model_to_s3(user_key, local_filename):
    target_url_path = "/api/v1/files/s3/model/upload"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    files = {'data': open(local_filename,'rb')}
    headers["User-Key"] = user_key

    res = requests.post(target_url, headers=headers, files=files)
    s3_url = res.text
    return s3_url

def upload_dataset_to_s3(user_key, local_filename):
    target_url_path = "/api/v1/files/s3/dataset/upload"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    files = {'data': open(local_filename,'rb')}
    headers["User-Key"] = user_key

    res = requests.post(target_url, headers=headers, files=files)
    s3_url = res.text
    return s3_url