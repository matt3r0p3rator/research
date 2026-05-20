import requests
import os
# Read token from .env
for line in open('.env').readlines():
    if line.startswith('ETAPI_TOKEN='):
        token = line.strip().split('=', 1)[1]
headers = {"Authorization": token.strip()}
r = requests.get("http://localhost:8023/etapi/notes?search=test", headers=headers)
print(r.status_code, r.text[:200])
