import json,hashlib,re,math,sys,os
sys.stdout.reconfigure(encoding='utf-8')
NOS=r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
out={}
for fn in ['um.py','um_absoluto.json','um_absoluto_selo.json']:
    p=os.path.join(NOS,fn); b=open(p,'rb').read(); h=hashlib.sha256(b).hexdigest()
    out[fn]={'path':p,'bytes':len(b),'sha256':h,'sha16':h[:16]}
    print(fn,len(b),h[:16])
src=open(os.path.join(NOS,'um.py'),'rb').read().decode('utf-8','replace')
m=re.search(r'ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',src); a=float(m.group(1))
print('ALPHA_FINE_CODATA_2018 =',m.group(1),'line',src[:m.start()].count('\n')+1)
beta=a*math.sqrt(math.e); print('beta runtime =',repr(beta))
out['alpha']=m.group(1); out['beta_runtime']=repr(beta)
m3=re.search(r'UM_VERSION\s*=\s*["\']([^"\']+)',src); print('UM_VERSION',m3.group(1) if m3 else None)
out['UM_VERSION']=m3.group(1) if m3 else None
sel=json.load(open(os.path.join(NOS,'um_absoluto_selo.json'),encoding='utf-8'))
print('selo keys:',list(sel.keys()))
for k in sel:
    v=sel[k]
    if isinstance(v,(str,int,float,bool)) and any(t in k.lower() for t in ['version','sha','hash','verdict','time','date','gate']):
        print(' ',k,'=',str(v)[:260])
json.dump({'files':out,'selo_keys':list(sel.keys())},open('base_v386_lida.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
