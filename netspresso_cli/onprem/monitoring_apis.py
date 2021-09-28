import requests

from netspresso_cli import settings
from urllib.parse import urljoin

def is_alive():
    target_url_path = "/"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url)
    if res.status_code == 200:
        return True
    else:
        return False

def get_compression_list(user_key):
    if not user_key:
        raise Exception("enter user_key!!")
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = "/api/v1/compressions"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_compression_status(user_key: str, compression_id: str):
    if not user_key:
        raise Exception("enter user_key!!")
    if not compression_id:
        raise Exception("enter compression_id!!")
    
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = f"/api/v1/compressions/{compression_id}"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_compression_status_index():
    target_url_path = f"/api/v1/compressions/status/index"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url)
    return res.json()

def get_compression_progress_index():
    target_url_path = f"/api/v1/compressions/progress/index"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url)
    return res.json()

def get_compression_result_list(user_key):
    if not user_key:
        raise Exception("enter user_key!!")
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = "/api/v1/compressions/results"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_compression_result(user_key: str, compression_id: str):
    if not user_key:
        raise Exception("enter user_key!!")
    if not compression_id:
        raise Exception("enter compression_id!!")
    
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = f"/api/v1/compressions/{compression_id}/result"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_worker_status_list():
    target_url_path = "/api/v1/worker_status_list"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url)
    return res.json()

def get_task_queue_status():
    target_url_path = "/api/v1/task_queue_status"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url)
    return res.json()

def get_task_queue_list(user_key):
    if not user_key:
        raise Exception("enter user_key!!")
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = "/api/v1/task_queue_list"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_compression_progress_details(user_key, compression_id):
    if not user_key:
        raise Exception("enter user_key!!")
    if not compression_id:
        raise Exception("enter compression_id!!")
    
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = f"/api/v1/compressions/{compression_id}/progress"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")

def get_one_compression_in_progress(user_key):
    if not user_key:
        raise Exception("enter user_key!!")
    headers = {}
    headers["User-Key"] = user_key
    target_url_path = "/api/v1/compressions/get_one_compression_in_progress"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    res = requests.get(target_url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("invalid user_key!!")