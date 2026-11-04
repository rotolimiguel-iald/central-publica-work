import sys
sys.path.insert(0, '.')
from secoes import segmentar, gancho
b = open(sys.argv[1], 'rb').read()
pre, segs = segmentar(b)
a = int(sys.argv[2]); z = int(sys.argv[3])
for k, s in enumerate(segs[a:z], start=a):
    print(k, s["bytes"], s["titulo"][:70], '||', gancho(b[s["ini"]:s["fim"]], 130))
