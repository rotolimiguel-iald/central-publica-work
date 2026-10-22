from pathlib import Path
from PIL import Image
import random,hashlib,json
w=Path(__file__).resolve().parent
r=random.Random(73)
size=768
pixels=bytearray(size*size*3)
for y in range(size):
    for x in range(size):
        i=(y*size+x)*3
        rgb=(r.randrange(160,256),r.randrange(0,80),r.randrange(0,80)) if x<size//2 else (r.randrange(0,80),r.randrange(0,80),r.randrange(160,256))
        pixels[i:i+3]=bytes(rgb)
p=w/'large_two_colors.png'
assert not p.exists()
Image.frombytes('RGB',(size,size),bytes(pixels)).save(p)
raw=p.read_bytes()
receipt=dict(fixture=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),expected='red left, blue right',synthetic=True,personal_data=False)
(w/'LARGE_FIXTURE.json').write_bytes(json.dumps(receipt,indent=2).encode())
print(json.dumps(receipt))
