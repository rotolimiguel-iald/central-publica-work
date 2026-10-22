# Le (sem executar) o dicionario _EMBEDDED_KERNEL_FILES do um.py por ast e compara com o kernel do Nos.
import ast,hashlib,json,os,sys
UM=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
K=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
raw=open(UM,'rb').read()
print("um.py sha256",hashlib.sha256(raw).hexdigest(),len(raw),"CRLF",raw.count(b"\r\n"),"LF",raw.count(b"\n"))
lines=raw.decode('utf-8').split('\n')
start=[i for i,l in enumerate(lines) if l.startswith('_EMBEDDED_KERNEL_FILES = {')]
assert len(start)==1; start=start[0]
end=start+1
while lines[end].rstrip('\r')!='}': end+=1
seg='\n'.join(lines[start:end+1])
d=ast.literal_eval(ast.parse(seg).body[0].value)
out={}
for rel,content in d.items():
    p=os.path.join(K,rel.replace('/',os.sep)); b=content.encode('utf-8')
    e=dict(emb_sha256=hashlib.sha256(b).hexdigest(),emb_bytes=len(b))
    if os.path.exists(p):
        fb=open(p,'rb').read(); e['disk_sha256']=hashlib.sha256(fb).hexdigest(); e['igual']=(fb==b)
    else:
        e['disk_sha256']=None; e['igual']=False
    out[rel]=e
keys=list(d.keys())
print("linhas",start+1,end+1,"entradas",len(d),"iguais ao disco",sum(1 for v in out.values() if v['igual']),"ultima chave",keys[-1])
for k in ['TGLExt.lean','TGL/Audit.lean','TGLExt/Fundacao.lean','TGL.lean','lakefile.toml','lean-toolchain']:
    print(k,out[k]['emb_sha256'][:16],out[k]['emb_bytes'],out[k]['igual'])
json.dump(dict(um_sha256=hashlib.sha256(raw).hexdigest(),start_line=start+1,end_line=end+1,n=len(d),entries=out,keys_order=keys),open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
