from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re
root=Path(__file__).resolve().parents[1]
errors=[]
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key not in ('href','src') or not value: continue
            url=urlsplit(value)
            if url.scheme or url.netloc or not url.path: continue
            target=root/url.path.lstrip('/') if url.path.startswith('/') else current.parent/url.path
            if not target.exists(): errors.append((str(current.relative_to(root)),value))
routes=json.loads((root/'content/portal-routes.json').read_text())
for file in [p.strip('/')+'/index.html' for p in routes]+['index.html','learn/index.html','journal/index.html']:
    current=root/file
    text=current.read_text()
    Links().feed(text)
    for source in ['academy.js','portal.js','tool-math.js']:
        if text.count('src="/assets/'+source+'"')>1: errors.append((file,'duplicate '+source))
assert not errors, errors
print('PASS: local resource links and script uniqueness across portal routes.')
