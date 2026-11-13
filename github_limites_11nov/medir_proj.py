import subprocess, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
def tree(d):
    out=subprocess.run(["git","-C",d,"ls-tree","-r","-l","-z","HEAD"],capture_output=True).stdout.decode("utf-8","replace")
    r=[]
    for l in out.split("\0"):
        if not l: continue
        meta,path=l.split("\t",1); p=meta.split()
        if p[1]=="blob": r.append((path,p[2],int(p[3])))
    return r
B=r"C:\IALD\Central_publica"
ordem=["central-publica","central-publica-bancada","central-publica-work"]
seen=set()
for r in ordem:
    t=sorted(tree(B+"\\"+r))
    raiz={"README.md","INDICE_PUBLICO.json","EXCLUSOES_PUBLICAS.json",".gitattributes","llms.txt","PATENTES.md","vinculo_patentario.json"}
    keep=[]
    for p,b,s in t:
        if b not in seen or p in raiz or p.startswith("INDICE_PUBLICO_PARTES/"): keep.append((p,b,s))
        seen.add(b)
    ref=len(t)-len(keep)
    print("%-24s hoje %7d arquivos %6.2f GB | só conteúdo novo: %7d arquivos %6.2f GB | viram referência: %7d (%.2f GB)" % (
        r, len(t), sum(s for *_,s in t)/1e9, len(keep), sum(s for *_,s in keep)/1e9, ref, (sum(s for *_,s in t)-sum(s for *_,s in keep))/1e9))
    for p,b,s in t: seen.add(b)
