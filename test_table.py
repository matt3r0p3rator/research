import re
import markdown as md_lib
raw = """
title 1 | title 2
---|---
a | b
"""
html = md_lib.markdown(raw, extensions=["tables", "fenced_code", "toc"])
print("Original:")
print(html)
html = re.sub(r"<table>", '<figure class="table"><table>', html)
html = re.sub(r"</table>", "</table></figure>", html)
print("Replaced:")
print(html)
