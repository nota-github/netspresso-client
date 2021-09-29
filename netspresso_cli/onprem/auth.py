import requests
from urllib.parse import urljoin
import hashlib

from netspresso_cli import settings

def login(user_id, user_pw):
    
    target_url_path = "/api/v1/users/login"
    target_url = urljoin(settings.API_SERVER.TARGET_URL, target_url_path)
    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    user_pw = hashlib.sha256(user_pw.encode()).hexdigest()
    data = {"user_id": user_id, "user_pw": user_pw}
    res = requests.post(target_url, data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("user_id or user_pw not incorrect!!")
    