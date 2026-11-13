import subprocess, sys, collections, os
sys.stdout.reconfigure(encoding="utf-8")
def tree(d, ref):
    out=subprocess.run(["git","-C",d,"ls-tree","-r","-l","-z",ref],capture_output=True).stdout.decode("utf-8","replace")
    r={}
    for l in out.split("\0"):
        if not l: continue
        meta,path=l.split("\t",1); p=meta.split()
        if p[1]=="blob": r[path]=(p[2],int(p[3]))
    return r
W=r"C:\IALD\Central_publica\central-publica-work"
P=r"C:\IALD\Central_publica\central-publica"
h=tree(W,"HEAD"); h1=tree(W,"HEAD~1")
old=set(b for b,_ in h1.values())
new={}
for path,(b,s) in h.items():
    if b not in old: new[b]=s
print("push v410 do work: %d blobs novos, %.2f GB brutos (o pack vai comprimido)" % (len(new), sum(new.values())/1e9))
# objetos do pack enviado: tamanho comprimido aproximado dos blobs novos
# entradas por pasta
dirs=collections.Counter(os.path.dirname(p) for p in h)
print("maiores pastas por entradas diretas:", [(d,n) for d,n in dirs.most_common(4)])
print("profundidade máxima:", max(p.count("/") for p in h)+1)
# cópias idênticas: cadeia_de_selo vs o resto do work e vs central-publica
pub=tree(P,"HEAD")
bl_pub=set(b for b,_ in pub.values())
fora_cad=set(b for p,(b,_) in h.items() if not p.startswith("cadeia_de_selo/"))
cad=[(p,b,s) for p,(b,s) in h.items() if p.startswith("cadeia_de_selo/")]
seen=set(); c_pub=c_fora=c_rep=0; s_pub=s_fora=s_rep=0; uniq_n=0; uniq_s=0
ext=collections.Counter(); exts=collections.Counter()
for p,b,s in sorted(cad):
    if b in bl_pub: c_pub+=1; s_pub+=s
    elif b in fora_cad: c_fora+=1; s_fora+=s
    elif b in seen: c_rep+=1; s_rep+=s
    else:
        uniq_n+=1; uniq_s+=s; e=os.path.splitext(p)[1].lower() or "(sem)"; ext[e]+=1; exts[e]+=s
    seen.add(b)
print("cadeia_de_selo: %d arquivos" % len(cad))
print("  idênticos a arquivo do central-publica (cofre/kernel): %d, %.2f GB" % (c_pub, s_pub/1e9))
print("  idênticos a arquivo do work fora da cadeia: %d, %.2f GB" % (c_fora, s_fora/1e9))
print("  repetição dentro da própria cadeia: %d, %.2f GB" % (c_rep, s_rep/1e9))
print("  conteúdo único (primeira ocorrência): %d, %.2f GB" % (uniq_n, uniq_s/1e9))
print("  únicos por extensão (GB/arquivos):", ", ".join("%s %.2f/%d"%(e,exts[e]/1e9,ext[e]) for e,_ in exts.most_common(10)))
