import requests
import markdown as md_lib
token = [line.strip().split('=', 1)[1] for line in open('.env') if line.startswith('ETAPI_TOKEN=')][0]
headers = {"Authorization": token}

raw = """
# Heading 1
## Heading 2

a | b
---|---
c | d
"""

html_notoc = md_lib.markdown(raw, extensions=["tables"])
html_toc = md_lib.markdown(raw, extensions=["tables", "toc"])

# without toc
r = requests.post("http://localhost:8023/etapi/create-note", json={"parentNoteId": "root", "title": "Test no toc", "type": "text", "content": html_notoc}, headers=headers)
print("No toc status:", r.status_code)

# with toc
r2 = requests.post("http://localhost:8023/etapi/create-note", json={"parentNoteId": "root", "title": "Test with toc", "type": "text", "content": html_toc}, headers=headers)
print("With toc status:", r2.status_code)

