import requests

from netspresso_cli import settings
from urllib.parse import urljoin

def create_compression(user_key):
    target_url_path = "/api/v1/compressions/create"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["User-Key"] = user_key

    data = {
        "configs": {
            "TASK":"classification",
            "INPUT":{
                "path":"https://netspresso-test-bucket2.s3.us-east-2.amazonaws.com/models/resnet50_cifar100.h5",
                "type":"h5",
                "storage":"s3",
                "model_config":{
                    "l2_reg":True,
                    "l2_lambda":0.0005,
                    "l2_weights_only":False,
                    "custom_object_path":None
                },
                "image_height_width":[
                    32,
                    32
                ],
                "test_accuracy_percent":77.37
            },
            "OUTPUT":{
                "dtype":"float16",
                "flask_port":"19306",
                "ip_address":"61.82.106.164",
                "model_type":"tflite",
                "test_device":"pc"
            },
            "DATASET":{
                "path":{
                    "test_x":"https://netspresso-test-bucket2.s3.us-east-2.amazonaws.com/datasets/cifar100_npy/test_x.npy",
                    "test_y":"https://netspresso-test-bucket2.s3.us-east-2.amazonaws.com/datasets/cifar100_npy/test_y.npy",
                    "train_x":"https://netspresso-test-bucket2.s3.us-east-2.amazonaws.com/datasets/cifar100_npy/train_x.npy",
                    "train_y":"https://netspresso-test-bucket2.s3.us-east-2.amazonaws.com/datasets/cifar100_npy/train_y.npy"
                },
                "type":"npy",
                "storage":"s3",
                "dataloader_config":{
                    "preprocessing":{
                        "std":[
                        0.2023,
                        0.1994,
                        0.201
                        ],
                        "mean":[
                        0.4914,
                        0.4822,
                        0.4465
                        ],
                        "rescale_value":255
                    },
                    "default_batch_size":128
                }
            },
            "STORAGE":{
                "type":"s3",
                "region_name":"us-east-2",
                "s3_bucket_name":"netspresso-test-bucket1",
                "destination_path":"/ResNet50_CIFAR100"
            },
            "MODEL_PRESET":"res50_cifar100",
            "COMPRESSION_ALIAS":"222_ResNet50_CIFAR100_res50_cifar100",
            "COMPRESSION_STRATEGY":{
                "initial_lr":0.1,
                "prune_margin":0.5
            },
            "COMPRESSION_CONSTRAINTS":{
                "objective":"accuracy",
                "acceptable_drop_percent_point":2
            }
        }
    }


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