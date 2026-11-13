import subprocess, os, re, sys, collections, glob
sys.stdout.reconfigure(encoding="utf-8")
# 1) crescimento do um.py pelas cópias do cofre
V = r"C:\IALD\Central de Patentes\vault\originals_copy"
pts=[]
for d in glob.glob(os.path.join(V,"um_unificado_v*")):
    m=re.fullmatch(r"um_unificado_v(\d+)", os.path.basename(d))
    f=os.path.join(d,"um.py")
    if m and os.path.isfile(f): pts.append((int(m.group(1)), os.path.getsize(f)))
pts.sort()
print("um.py por versão (MB):", " ".join("v%d:%.1f"%(v,s/1e6) for v,s in pts[-14:]))
if len(pts)>=2:
    (v0,s0),(v1,s1)=pts[max(0,len(pts)-11)],pts[-1]
    taxa=(s1-s0)/(v1-v0); print("taxa média últimas %d versões: %.2f MB/versão; até 100 MB: ~%d versões; até 50 MB: ~%d" % (v1-v0, taxa/1e6, (100e6-s1)/taxa if taxa>0 else -1, (50e6-s1)/taxa if taxa>0 else -1))
# 2) duplicação no work
d=r"C:\IALD\Central_publica\central-publica-work"
out=subprocess.run(["git","-C",d,"ls-tree","-r","-l","-z","HEAD"],capture_output=True).stdout.decode("utf-8","replace")
tot=0; uniq={}; cad_tot=0; cad_uniq={}; cnt=collections.Counter(); sub=collections.Counter(); subn=collections.Counter()
for l in out.split("\0"):
    if not l: continue
    meta,path=l.split("\t",1); p=meta.split()
    if p[1]!="blob": continue
    s=int(p[3]); tot+=s; uniq[p[2]]=s
    if path.startswith("cadeia_de_selo/"):
        cad_tot+=s; cad_uniq[p[2]]=s; cnt["cadeia"]+=1
        parts=path.split("/")
        k="/".join(parts[1:3]) if len(parts)>3 else parts[1]
        key=parts[2] if len(parts)>3 else "(raiz)"
        sub[key]+=s; subn[key]+=1
print("work: %.2f GB em árvore; %.2f GB em blobs únicos" % (tot/1e9, sum(uniq.values())/1e9))
print("cadeia_de_selo: %d arquivos, %.2f GB em árvore, %.2f GB únicos" % (cnt["cadeia"], cad_tot/1e9, sum(cad_uniq.values())/1e9))
print("subpastas de cadeia_de_selo/vNNN/* (GB, arquivos):", ", ".join("%s %.2f/%d"%(k,v/1e9,subn[k]) for k,v in sub.most_common(10)))
