import requests
import shutil
import re
from pathlib import Path
import os

def download_file(url, target_name=None, target_dir=None)->str:
    r = requests.get(url, stream=True)

    # extract file name
    if target_name:
        fname = target_name
    elif r.headers.get('content-disposition'):
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
    else:
        fname = url.split("/")[-1]
    if target_dir:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        fname = str(Path(target_dir) / fname)
    if r.status_code == 200:
        with open(fname, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return fname