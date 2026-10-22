from pathlib import Path
import urllib.request,hashlib,json,zipfile
w=Path(__file__).parent
base="https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
expected=urllib.request.urlopen(base+".sha256",timeout=30).read().decode().split()[0].lower()
assert len(expected)==64
p=w/"ffmpeg-essentials.zip"
if not p.exists():
 with urllib.request.urlopen(base,timeout=60) as response,p.open("xb") as out:
  while True:
   chunk=response.read(1024*1024)
   if not chunk:break
   out.write(chunk)
actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==expected
files=[]
with zipfile.ZipFile(p) as archive:
 for name in archive.namelist():
  if name.endswith(("/bin/ffprobe.exe","/bin/ffmpeg.exe","/LICENSE","/README.txt")):
   raw=archive.read(name);dest=w/Path(name).name
   if not dest.exists():dest.write_bytes(raw)
   assert dest.read_bytes()==raw
   files.append(dict(name=dest.name,path=str(dest),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
receipt=dict(status="HASH_VERIFIED_NOT_INSTALLED",source=base,checksum_source=base+".sha256",archive_sha256=actual,files=files)
(w/"RECEIPT.json").write_bytes(json.dumps(receipt,indent=2).encode());print(json.dumps(receipt))
