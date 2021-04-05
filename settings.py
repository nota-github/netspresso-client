import os

RESULT_DIR = "result"

os.environ["AWS_KEY_ID"] = "AKIAW5VDV2WPWKGZD6VL"
os.environ["AWS_SECRET_KEY"] = "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"
os.environ["AWS_BUCKET_NAME"] = "nota-netspresso-bucket"
os.environ["AWS_REGION_NAME"] = "us-east-2"

class API_SERVER:
    HOST = "acfe62d997b9043858797f5154a0fc86-1177422271.us-east-2.elb.amazonaws.com"
    PORT = 8000