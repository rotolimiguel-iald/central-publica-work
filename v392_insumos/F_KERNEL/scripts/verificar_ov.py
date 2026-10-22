# confere byte a byte a sobreposicao ov contra a pasta compilada do kernel do Nos (so leitura)
import os,hashlib,json,sys
SRC=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\build\lib\lean"
DST=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"ov")
def h(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
n=0;dif=[];falta=[]
agg=hashlib.sha256()
for r,ds,fs in os.walk(SRC):
  ds.sort()
  for f in sorted(fs):
    s=os.path.join(r,f);rel=os.path.relpath(s,SRC);d=os.path.join(DST,rel)
    if not os.path.exists(d): falta.append(rel);continue
    hs=h(s)
    if hs!=h(d): dif.append(rel)
    agg.update((rel+"|"+hs+"\n").encode());n+=1
extra=[]
for r,ds,fs in os.walk(DST):
  for f in fs:
    rel=os.path.relpath(os.path.join(r,f),DST)
    if not os.path.exists(os.path.join(SRC,rel)): extra.append(rel)
res=dict(arquivos=n,diferentes=dif,faltando=falta,extras_no_ov=sorted(extra),agregado_sha256=agg.hexdigest())
print(json.dumps(res,ensure_ascii=False)[:2000])
json.dump(res,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
