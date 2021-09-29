from __future__ import print_function, unicode_literals
import sys
import os
import json
from PyInquirer import style_from_dict, Token, prompt, Separator
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from netspresso_cli.onprem import auth
from netspresso_cli.onprem import monitoring_apis
from netspresso_cli.onprem import compression
from netspresso_cli.common import time_calc
from netspresso_cli.common import network

# please look at __main__ code first!

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def get_user_id():
    question_user_id = [
        {
            'type': 'input',
            'message': 'user_id: ',
            'name': 'user_id',
        }
    ]
    answers = prompt(question_user_id, style=style)
    return answers["user_id"]


def get_user_pw():
    question_user_pw = [
        {
            'type': 'input',
            'message': 'user_pw: ',
            'name': 'user_pw',
        }
    ]
    answers = prompt(question_user_pw, style=style)
    return answers["user_pw"]

def select_main_task():
    question_task = [
        {
            'type': 'list',
            'message': 'Select a tasks',
            'name': 'task',
            'choices': [
                Separator('= what do you want to do? (please login first) ='),
                {
                    'name': 'Login'
                },
                {
                    'name': "Logout"
                },
                {
                    'name': 'Create a compression'
                },
                {
                    'name': 'Resume monitoring(last compression)'
                },
                {
                    'name': 'Download result'
                },
                {
                    'name': 'Exit'
                }
            ],
            'validate': lambda answer: 'You must choose at least one task.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(question_task, style=style)
    return answers

def select_custom_model_data():
    question_custom_model_data = [
        {
            'type': 'list',
            'message': 'do you want to compress with your custom model & data?',
            'name': 'custom_model_data',
            'choices': [
                Separator('= do you want to compress with your custom model & data? ='),
                {
                    'name': 'Yes'
                },
                {
                    'name': "No"
                },
            ],
            'validate': lambda answer: 'You must choose at least one task.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(question_custom_model_data, style=style)
    return answers

def get_model_path():
    question_model_path = [
        {
            'type': 'input',
            'message': 'model_path: ',
            'name': 'model_path',
        }
    ]
    answers = prompt(question_model_path, style=style)
    return answers["model_path"]

def get_dataset_path():
    question_dataset_path = [
        {
            'type': 'input',
            'message': 'dataset_path: ',
            'name': 'dataset_path',
        }
    ]
    answers = prompt(question_dataset_path, style=style)
    return answers["dataset_path"]

def get_config_path():
    question_config_path = [
        {
            'type': 'input',
            'message': 'compression_config_path: ',
            'name': 'compression_config_path',
        }
    ]
    answers = prompt(question_config_path, style=style)
    return answers["compression_config_path"]

def select_config_file():
    question_config_file = [
        {
            'type': 'list',
            'message': 'choose config',
            'name': 'config',
            'choices': [
                {
                    'name': 'mobilenet_v1_with_cifar100',
                },
                {
                    'name': 'mobilenet_v2_with_imagewoof'
                },
                {
                    'name': 'resnet18_with_cifar100'
                },
                {
                    'name': 'resnet18_with_imagewoof'
                },
                {
                    'name': 'resnet50_with_cifar100'
                },
                {
                    'name': 'resnet50_with_imagewoof'
                },
                {
                    'name': 'vgg19_with_cifar100'
                },
            ],
            'validate': lambda answer: 'You must choose at least one task.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(question_config_file, style=style)
    return answers["config"]

def get_task_name():
    question_task_name = [
        {
            'type': 'input',
            'message': 'specify compression task name: ',
            'name': 'task_name',
        }
    ]
    answers = prompt(question_task_name, style=style)
    return answers["task_name"]

def save_userinfo(user_info):
    with open("user_info.json", "wt") as f:
        json.dump(user_info, f)

def load_userinfo():
    try:
        with open("user_info.json", "rt") as f:
            d = json.load(f)
        return d
    except:
        raise Exception("loading userinfo failed!!")

def delete_userinfo():
    try:
        os.remove("user_info.json")
    except:
        pass

def save_compression_info(compression_info):
    with open("compression_info.json", "wt") as f:
        json.dump(compression_info, f)

def load_compression_info():
    try:
        with open("compression_info.json", "rt") as f:
            d = json.load(f)
        return d
    except:
        raise Exception("loading compression_info failed!!")

def delete_compression_info():
    try:
        os.remove("compression_info.json")
    except:
        pass

def monitor_compression(user_key, compression_info):
    compression_id = compression_info["compression_id"]
    while True:
        current_compression_info = monitoring_apis.get_compression_status(user_key, compression_id)
        current_compression_id = current_compression_info["compression_id"]
        print("==========current status==========")
        print(current_compression_info)
        print("==================================")
        if current_compression_id == None: # 요청한 compression_id가 없는 경우, 프로그램 종료
            print(f"compression_id({current_compression_id}) does not exists")
            exit(0)
        elif current_compression_info["status"] != 0: # 도중에 error가 발생한 경우(status!=0), 프로그램 종료
            print("error in progressing")
            exit(0)
        elif current_compression_info["progress"] == 1: # compression task가 queue에서 대기하고 있음.
            print("[*] compression task in queue!")
            print("[*] currently stacked compression queue size : ", monitoring_apis.get_task_queue_status())
        elif current_compression_info["progress"] == 2:
            print("[*] compression is in progress.")
        elif current_compression_info["progress"] == 3: # 정상적으로 프로세스가 완료된 경우
            print("compression completed!")
            break
        print(f"[*] running time in current step: ", time_calc.calculate_duration(time_from=current_compression_info["updated_time"]))
        print(f"[*] total time: ", time_calc.calculate_duration(time_from=current_compression_info["created_time"]))
        print("\n\n")
        time.sleep(20)

def download_result(user_key, compression_id):
    result = monitoring_apis.get_compression_result(user_key, compression_id)
    try:
        print(result)
        DOWNLOAD_DIR = "/".join(["result", compression_id])
        log_file = network.download_file(result["url_log"], target_dir=DOWNLOAD_DIR)
        print(f"[*] log file(filename: {log_file}) saved")
        input_type_compressed_model = network.download_file(result["url_input_type_compressed_model"], target_dir=DOWNLOAD_DIR)
        print(f"[*] input type compressed model(filename: {input_type_compressed_model}) saved")
        converted_type_compressed_model = network.download_file(result["url_converted_type_compressed_model"], target_dir=DOWNLOAD_DIR)
        print(f"[*] converted type compressed model(filename: {converted_type_compressed_model}) saved")
    except Exception as e:
        print("downloading result failed!!", e)

if __name__ == "__main__":
    answers = select_main_task()
    print(answers)
    if answers["task"] == "Login":
        user_id = get_user_id()
        user_pw = get_user_pw()
        user_info = auth.login(user_id, user_pw)
        save_userinfo(user_info)
    elif answers["task"] == "Logout":
        delete_userinfo()
    elif answers["task"] == "Create a compression":
        print("compression")
        user_info = load_userinfo()
        user_key = user_info["user_key"]
        answer_custom_model_data = select_custom_model_data()
        if answer_custom_model_data["custom_model_data"] == "Yes":
            
            while True:
                model_path = get_model_path()
                s3_model_url = compression.upload_model_to_s3(user_key, model_path)                
                if s3_model_url:
                    print("model url: ", s3_model_url)
                    break
                else:
                    print("invalid model file!!")

            while True:
                dataset_path = get_dataset_path()
                s3_data_url = compression.upload_dataset_to_s3(user_key, dataset_path)
                if s3_data_url:
                    print("dataset url: ", s3_data_url)
                    break
                else:
                    print("invalid dataset file!!")

            config_path = get_config_path()
            if not config_path:
                config_path = "config_files/custom_default.json"
            task_name = get_task_name()
            compression_title = task_name
            destination_path_s3 = "/" + task_name
            compression_info = compression.create_compression(
                user_key, config_json_path=config_path,
                custom_model_dataset=True, model_url=s3_model_url,
                dataset_url=s3_data_url, compression_title=compression_title, destination_path_s3=destination_path_s3
            )
        else: # using model zoo
            compression_config = select_config_file()
            if compression_config == 'mobilenet_v1_with_cifar100':
                compression_config_path = "config_files/mb1_cifar100.json"
            elif compression_config == 'mobilenet_v2_with_imagewoof':
                compression_config_path = "config_files/mb2_imagewoof.json"
            elif compression_config == 'resnet18_with_cifar100':
                compression_config_path = "config_files/res18_cifar100.json"
            elif compression_config == 'resnet18_with_imagewoof':
                compression_config_path = "config_files/res18_imagewoof.json"
            elif compression_config == 'resnet50_with_cifar100':
                compression_config_path = "config_files/res50_cifar100.json"
            elif compression_config == 'resnet50_with_imagewoof':
                compression_config_path = "config_files/res50_imagewoof.json"
            elif compression_config == 'vgg19_with_cifar100':
                compression_config_path = "vgg19_cifar100.json"
            else:
                print("invalid compression config!!")
                exit(0)
            task_name = get_task_name()
            compression_title = "_".join([task_name, compression_config])
            destination_path_s3 = "/" + task_name
            compression_info = compression.create_compression(
                user_key, config_json_path=compression_config_path,
                compression_title=compression_title,destination_path_s3=destination_path_s3
            )
        compression_id = compression_info["compression_id"]
        save_compression_info(compression_info)
        monitor_compression(user_key, compression_info)
        download_result(user_key, compression_id)
        
    elif answers["task"] == "Resume monitoring(last compression)":
        user_info = load_userinfo()
        user_key = user_info["user_key"]
        compression_info = load_compression_info()
        compression_id = compression_info["compression_id"]
        monitor_compression(user_key, compression_info)
        download_result(user_key, compression_id)
    elif answers["task"] == "Download result":
        user_info = load_userinfo()
        user_key = user_info["user_key"]
        compression_info = load_compression_info()
        compression_id = compression_info["compression_id"]
        download_result(user_key, compression_id)
    elif answers["task"] == "Exit":
        print("exit")
    else:
        print("invalid selection")