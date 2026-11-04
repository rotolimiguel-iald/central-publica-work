import sys, re, hashlib
p = sys.argv[1]
b = open(p,'rb').read()
print(p, len(b), 'CRLF', b.count(b'\r\n'), 'LF', b.count(b'\n'), 'sha256', hashlib.sha256(b).hexdigest())
lines = b.split(b'\n')
# seções ## (nível 2), fora de blocos de código
secs=[]
off=0
incode=False
for i,l in enumerate(lines):
    ls=l.rstrip(b'\r')
    if ls.startswith(b'```'): incode = not incode
    if not incode and ls.startswith(b'## '):
        secs.append((i,off,ls.decode('utf8','replace')))
    off+=len(l)+1
print('secoes', len(secs))
pre = secs[0][1] if secs else len(b)
print('preambulo bytes', pre)
for k,(i,o,t) in enumerate(secs):
    e = secs[k+1][1] if k+1<len(secs) else len(b)
    print(f"{k:3d} L{i+1:6d} {e-o:8d} {t[:110]}")
