import os
import glob
import boto3
import requests
import tqdm
import zipfile
from urllib.parse import urljoin
from pathlib import Path

from netspresso_real_client import settings


def get_auth():
    assert os.environ.get("AWS_KEY_ID") != None
    assert os.environ.get("AWS_SECRET_KEY") != None
    aws_access_key_id = os.environ["AWS_KEY_ID"].strip()
    aws_secret_access_key = os.environ["AWS_SECRET_KEY"].strip()
    aws_bucket_name = os.environ["AWS_BUCKET_NAME"].strip()
    aws_region_name = os.environ["AWS_REGION_NAME"].strip()

    aws_auth_info = {}
    aws_auth_info["aws_access_key_id"] = aws_access_key_id
    aws_auth_info["aws_secret_access_key"] = aws_secret_access_key
    aws_auth_info["bucket_name"] = aws_bucket_name
    aws_auth_info["region_name"] = aws_region_name
    return aws_auth_info


def upload_folder_to_s3(aws_auth_info, src_path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_auth_info["aws_access_key_id"],
        aws_secret_access_key=aws_auth_info["aws_secret_access_key"],
        region_name=aws_auth_info["region_name"],
    )
    path_list = []
    for path in Path(src_path).rglob("*.*"):
        path_list.append(path)
    for path in tqdm.tqdm(path_list):
        s3.upload_file(
            path.absolute().as_posix(),
            aws_auth_info["bucket_name"],
            path.as_posix(),
        )
    return _make_s3_url(
        aws_auth_info["bucket_name"], aws_auth_info["region_name"], src_path
    )


def upload_folder_to_s3_using_zip(aws_auth_info, src_path, dst_path, reuse_file=True):
    dst_zip_path = src_path.rstrip("[/\\]") + ".zip"
    zfile = zipfile.ZipFile(dst_zip_path, "w")
    path_list = []
    for path in Path(src_path).rglob("*.*"):
        arc_path = path.relative_to(src_path)
        path_list.append(path)
        zfile.write(path.as_posix(), arc_path)
    zfile.close()
    s3_zip_url = upload_file_to_s3(aws_auth_info, dst_zip_path, dst_path)
    os.remove(dst_zip_path)
    return s3_zip_url


def upload_file_to_s3(aws_auth_info, src_path, dst_path, reuse_file=True):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_auth_info["aws_access_key_id"],
        aws_secret_access_key=aws_auth_info["aws_secret_access_key"],
        region_name=aws_auth_info["region_name"],
    )
    dst_path = Path(dst_path).as_posix().__str__()
    if not _does_key_exists(s3, aws_auth_info["bucket_name"], dst_path):
        s3.upload_file(src_path, aws_auth_info["bucket_name"], dst_path)
    return _make_s3_url(
        aws_auth_info["bucket_name"], aws_auth_info["region_name"], dst_path
    )


def download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url):
    s3 = boto3.resource(
        "s3",
    )
    bucket_url, key = s3_url.split("/", 2)[-1].split("/", 1)
    bucket_id = bucket_url.split(".")[0]
    save_path = os.path.join(settings.RESULT_DIR, compression_id)
    file_name = key.split("/")[-1]
    file_path = os.path.join(save_path, file_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    s3.Bucket(bucket_id).download_file(key, file_path)
    return file_path

def _make_s3_url(bucket_name: str, region_name: str, key: str) -> str:
    retn = f"https://{bucket_name}.s3.{region_name}.amazonaws.com"
    retn = urljoin(retn, Path(key).as_posix())
    return retn

def _does_key_exists(client, bucket, key):
    """return the key's size if it exist, else None"""
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return obj['Size']

