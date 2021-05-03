import argparse
import os
import json
import datetime
import settings

def get_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="yaml config path")
    parser.add_argument("-l", "--login", required=False, help="login aws", action="store_true")
    args = parser.parse_args()

    return args

def calculate_duration(time_from: str):
    dt_time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')
    time_delta = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None) - dt_time_from
    return str(time_delta)

def get_aws_info()->bool:
    rslt = True
    AWS_KEY_ID = input("AWS Access key ID: ")
    AWS_SECRET_KEY = input("Secret access key: ")
    d = {}
    d["AWS_KEY_ID"] = AWS_KEY_ID
    d["AWS_SECRET_KEY"] = AWS_SECRET_KEY
    fpath = os.path.join(os.path.join(settings.BASE_DIR, "_credentials.json"))
    with open(fpath, "wt") as fp_csvfile:
        json.dump(d, fp_csvfile)
    return rslt

def check_login()->bool:
    # check if exists csv file and valid format
    rslt = True
    fpath = os.path.join(os.path.join(settings.BASE_DIR, "_credentials.json"))
    if not os.path.exists(fpath):
        rslt = False
        return rslt
    
    with open(fpath, newline='') as csvfile:
        credential_dict = json.load(csvfile)
        if credential_dict.get("AWS_KEY_ID") is None:
            print("credential file format error!")
            rslt = False
            return rslt
        if credential_dict.get("AWS_SECRET_KEY") is None:
            print("credential file format error!")
            rslt = False
            return rslt
    os.environ["AWS_KEY_ID"] = credential_dict.get("AWS_KEY_ID")
    os.environ["AWS_SECRET_KEY"] = credential_dict.get("AWS_SECRET_KEY")
    return rslt
