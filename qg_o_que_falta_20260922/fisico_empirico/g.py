import json,sys
P=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
c=json.load(open(P,encoding='utf-8'))['core']
o=c
for k in sys.argv[1].split('.'):
    o=o[int(k)] if isinstance(o,list) else o[k]
s=json.dumps(o,ensure_ascii=False,indent=1)
n=int(sys.argv[2]) if len(sys.argv)>2 else 8000
print(s[:n])
