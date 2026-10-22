import os,hashlib,sys,json,time
roots=[
 r"C:\IALD\Central de Patentes\work\leitura_cria_o_objeto_07out",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F2.3",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.2",
 r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR",
 r"C:\IALD\PROGRAMA_IALD\auditorias\F1.3\art_ad949e97\sandbox",
]
for d in os.listdir(r"C:\IALD\PROGRAMA_IALD\auditorias"):
  if d.startswith("F2.3") or d.startswith("F1.2"):
    roots.append(os.path.join(r"C:\IALD\PROGRAMA_IALD\auditorias",d))
out=[]
for R in roots:
  if not os.path.exists(R):
    print("AUSENTE",R);continue
  for r,ds,fs in os.walk(R):
    ds.sort()
    for f in sorted(fs):
      if f.endswith(('.lean','.olean')):
        p=os.path.join(r,f)
        b=open(p,'rb').read()
        st=os.stat(p)
        out.append(dict(path=p,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),mtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(st.st_mtime))))
for o in out:
  print(o['sha256'][:16],o['bytes'],o['mtime'],o['path'])
json.dump(out,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
