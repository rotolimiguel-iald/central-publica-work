import subprocess, json, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
REPOS = {
 "Central de Patentes": r"C:\IALD\Central de Patentes",
 "central-publica": r"C:\IALD\Central_publica\central-publica",
 "central-publica-work": r"C:\IALD\Central_publica\central-publica-work",
 "central-publica-bancada": r"C:\IALD\Central_publica\central-publica-bancada",
 "the_boundary": r"C:\IALD\Artigo\the_boundary",
}
def g(d,*a):
    return subprocess.run(["git","-C",d]+list(a),capture_output=True,text=True,encoding="utf-8",errors="replace").stdout
for nome,d in REPOS.items():
    if not os.path.isdir(d): print(nome,"AUSENTE"); continue
    rem = g(d,"remote","get-url","origin").strip()
    cnt = g(d,"count-objects","-vH")
    pack = [l for l in cnt.splitlines() if l.startswith(("size-pack","size:","count"))]
    rows=[]
    for l in g(d,"ls-tree","-r","-l","-z","HEAD").split("\0"):
        if not l: continue
        meta,path=l.split("\t",1); p=meta.split()
        if p[1]!="blob": continue
        rows.append((int(p[3]),path))
    tot=sum(s for s,_ in rows)
    top=collections.Counter()
    for s,pth in rows: top[pth.split("/")[0]]+=s
    over50=[(s,p) for s,p in rows if s>50*2**20]
    print("=== %s  (%s)" % (nome, rem))
    print("  HEAD: %d arquivos, %.2f GB; >50MB: %d; >90MiB: %d; maior: %.1f MB %s" % (len(rows), tot/1e9, len(over50), sum(1 for s,_ in rows if s>90*2**20), max(rows)[0]/1e6, max(rows)[1]))
    print("  git:", "; ".join(pack))
    print("  pastas de topo (GB):", ", ".join("%s %.2f"%(k,v/1e9) for k,v in top.most_common(8)))
    for s,p in sorted(over50,reverse=True)[:6]: print("    %.1f MB  %s"%(s/1e6,p))
