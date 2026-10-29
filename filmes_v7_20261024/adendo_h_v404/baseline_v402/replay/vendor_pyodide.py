"""Verify/download the pinned official subset. No global installation."""
import argparse, hashlib, json, pathlib, urllib.request
R=pathlib.Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--download',action='store_true');a=p.parse_args()
receipt=json.loads((R/'replay/PYODIDE_VENDOR.json').read_bytes())
base=receipt['source'];assert base=='https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'
files={}
for f in receipt['files']:
 data=urllib.request.urlopen(base+f['name'],timeout=60).read() if a.download else (R/'web/vendor/pyodide'/f['name']).read_bytes()
 assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],f['name']
 files[f['name']]=data
assert sum(map(len,files.values()))<=25000000
if a.download:
 for name,data in files.items():
  dst=R/'web/vendor/pyodide'/name;tmp=dst.with_name(dst.name+'.tmp');tmp.write_bytes(data);tmp.replace(dst)
print(json.dumps({'status':'VERIFIED','bytes':sum(map(len,files.values())),'files':len(files)}))
