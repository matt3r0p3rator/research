import requests
token = [line.strip().split('=', 1)[1] for line in open('.env') if line.startswith('ETAPI_TOKEN=')][0]
headers = {"Authorization": token}

raw = """
# Header
a | b
---|---
c | d
"""

files = {"file": ("test.md", raw, "application/octet-stream")}
r = requests.post("http://localhost:8023/etapi/notes/root/import", files=files, headers=headers)
print("Import status:", r.status_code, r.text[:100])
