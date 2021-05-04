import yaml
import json
import requests
import os
from typing import Dict
from pathlib import Path

from netspresso_cli.clouds.types import DataSetFormat, ReturnDataType, InputModelType
from netspresso_cli.clouds.types import ModelTypeError
from netspresso_cli.clouds.aws import connection as aws_connection
from netspresso_cli.clouds import monitoring_apis
from netspresso_cli import settings


class CompSession:
    def __init__(self, compression_id=None):
        self.compression_id = compression_id
        self.config = None
        self.config_yaml = None
        self.model_type = None
        self.model_path = None
        self.data_path = None
        self.aws_auth_info = None
        self.s3_data_url = None
        self.s3_config_url = None
        self.s3_model_url = None
        self.dataset_type = None
        self.config_json = None

    def upload_config(self, config_path, storage_config: Dict):
        # check parameters
        assert os.path.exists(config_path), "[ERROR] config file does'not exist"
        assert os.path.isdir(config_path)==False, "[ERROR] config path is dir, but expected file"
        assert storage_config.get("type") != None, "[ERROR] storage type must be filled"
        assert storage_config["type"] in ["s3"]
        assert storage_config["destination_path"] != None, "[ERROR] storage destination_path is null"

        with open(config_path, "rt") as f:
            self.config_yaml = f.read()
            self.config = yaml.safe_load(self.config_yaml)
        aws_auth_info = aws_connection.get_auth()
        config_filename = os.path.split(config_path)[1]
        
        dst_path = (Path(storage_config["destination_path"].lstrip("/")) / "config" / config_filename).as_posix()
        self.s3_config_url = aws_connection.upload_file_to_s3(
            aws_auth_info, config_path, dst_path
        )

    def upload_data(self, data_path, storage_config: Dict, dataset_type="imagefolder"):
        if isinstance(data_path, dict):
            return
        if dataset_type == "imagefolder" and not isinstance(data_path, dict):
            assert os.path.exists(data_path), "[ERROR] dataset file does'not exist"
        elif dataset_type == "npy":
            pass
        else:
            assert dataset_type in ["imagefolder", "npy"], "[ERROR] dataset_type error"
        if dataset_type == "imagefolder"and not isinstance(data_path, dict):
            assert os.path.isdir(data_path)==True, "[ERROR] config path is file, but expected directory"
        elif dataset_type == "npy":
            pass
        else:
            assert dataset_type in ["imagefolder", "npy"], "[ERROR] dataset type error"
        assert storage_config.get("type") != None, "[ERROR] storage type must be filled"
        assert storage_config["type"] in ["s3"]
        assert storage_config["destination_path"] != None, "[ERROR] storage destination_path is null"

        if dataset_type == "imagefolder" and not isinstance(data_path, dict):
            if data_path.startswith("http"):
                return
        elif dataset_type == "npy":
            if data_path["train_x"].startswith("http"):
                return

        data_path = Path(data_path).__str__()
        self.data_path = data_path
        self.dataset_type = dataset_type
        dataset_filename = os.path.split(data_path)[1]
        dst_path = (Path(storage_config["destination_path"].lstrip("/")) / "dataset" / dataset_filename).as_posix() + ".zip"
        aws_auth_info = aws_connection.get_auth()
        self.s3_data_url = aws_connection.upload_folder_to_s3_using_zip(
            aws_auth_info, data_path, dst_path
        )

    def upload_model(self, model_path, storage_config: Dict, model_type="pb"):
        if model_path.startswith("http"):
           return
        else: 
            assert os.path.exists(model_path), "[ERROR] model file does'not exist"
        assert model_type in ["pb", "h5"], "[ERROR] model type is invalid"
        if model_type=="pb":
            assert os.path.isdir(model_path)==True, "[ERROR] model path is file, but expected directory"
        elif model_type=="h5":
            assert os.path.isdir(model_path)==False, "[ERROR] model path is directory, but expected file"
        assert storage_config.get("type") != None, "[ERROR] storage type must be filled"
        assert storage_config["type"] in ["s3"]
        assert storage_config["destination_path"] != None, "[ERROR] storage destination_path is null"

        self.model_path = model_path
        self.model_type = model_type
        
        aws_auth_info = aws_connection.get_auth()
        model_filename = os.path.split(model_path)[1]
        if model_type == "pb":
            dst_path = (Path(storage_config["destination_path"].lstrip("/")) / "model" / model_filename).as_posix() + ".zip"
            self.s3_model_url = aws_connection.upload_folder_to_s3_using_zip(aws_auth_info, model_path, dst_path)
        elif model_type == "h5":
            dst_path = (Path(storage_config["destination_path"].lstrip("/")) / "model" / model_filename).as_posix()
            self.s3_model_url = aws_connection.upload_file_to_s3(aws_auth_info, model_path, dst_path)
        else:
            raise ModelTypeError("Model Type Error", "invalid model type")
        

    def compress(self):
        config_yaml = self.config_yaml
        assert is_fulfilled_configs(config_yaml)==True, "[ERROR] config is invalid"

        configs_dict = yaml.safe_load(config_yaml)
        if self.s3_model_url:
            configs_dict["INPUT"]["path"] = self.s3_model_url
        if self.dataset_type == "imagefolder" and self.s3_data_url != None:
            configs_dict["DATASET"]["path"] = {"zip_dir":self.s3_data_url}

        self.config_yaml = yaml.dump(configs_dict)
        data = {
            "configs": configs_dict,  # yaml config
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        r = requests.post(
            f"http://{settings.API_SERVER.HOST}:{settings.API_SERVER.PORT}/api/v1/compressions/create",
            data=json.dumps(data), headers=headers
        )
        return r.json() # return compression_id

    def get_result(
        self, return_type: ReturnDataType = ReturnDataType.JSON
    ) -> ReturnDataType:
        return monitoring_apis.get_result(self.compression_id, return_type)


def is_fulfilled_configs(config_yaml: str) -> bool:
    """
    ==================
    example config
    ==================

TASK: classification
COMPRESSION_ALIAS: test-compression
COMPRESSION_CONSTRAINTS:
  objective: accuracy
  acceptable_drop_percent_point: 20.0
INPUT:
  type: pb # pb, h5
  path: "C:\\Users\\NOTA2001\\Desktop\\vgg_model" # url or local path. # model_path = "C:\\Users\\NOTA2001\\Desktop\\0402"
  test_accuracy_percent: 50.0
  image_height_width: [32, 32]
OUTPUT:
  model_type: tflite # h5
  dtype: float16
  test_device: pc # raspberrypi
DATASET:
  type: imagefolder # imagefolder
  path: "C:\\Users\\NOTA2001\\Desktop\\CIFAR10" # url or local path # data_path = "C:\\Users\\NOTA2001\\Desktop\\CIFAR10-jh"
  dataloader_config:
    preprocessing:
      rescale_value: 255
      mean: [0.0, 0.0, 0.0]
      std: [1.0, 1.0, 1.0]
    default_batch_size: 16
STORAGE:
  type: s3
  destination_path: "/vgg-test" # specify folder name in the destination storage
"""
    retn = True

    configs_dict = yaml.safe_load(config_yaml)
    if not configs_dict.get("TASK") in ["classification"]:
        retn = False
    if configs_dict.get("COMPRESSION_ALIAS") == None:
        retn = False
    if configs_dict.get("COMPRESSION_CONSTRAINTS") == None:
        retn = False
    if not configs_dict["COMPRESSION_CONSTRAINTS"].get("objective") in ["accuracy"]:
        retn = False
    if configs_dict["COMPRESSION_CONSTRAINTS"].get("acceptable_drop_percent_point") == None:
        retn = False
    if configs_dict.get("INPUT") == None:
        retn = False
    if not configs_dict["INPUT"].get("type") in ["pb", "h5"]:
        retn = False
    #TODO: further checks have to be placed here.
    
    return retn
