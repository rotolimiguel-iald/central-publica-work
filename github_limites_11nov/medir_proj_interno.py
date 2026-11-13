# Projeção com a referência só DENTRO do mesmo repositório (cada repositório autocontido), fora a raiz gerada e a esteira do work.
import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
B=r"C:\IALD\Central_publica"
RAIZ={"README.md","PATENTES.md","vinculo_patentario.json","INDICE_PUBLICO.json","EXCLUSOES_PUBLICAS.json",".gitattributes","llms.txt"}
for r in ("central-publica","central-publica-bancada","central-publica-work"):
    out=subprocess.run(["git","-C",B+"\\"+r,"ls-tree","-r","-l","-z","HEAD"],capture_output=True).stdout.decode("utf-8","replace")
    t=[]
    for l in out.split("\0"):
        if not l: continue
        meta,path=l.split("\t",1); p=meta.split()
        if p[1]=="blob": t.append((path,p[2],int(p[3])))
    t.sort(); seen=set(); keep=0; ks=0; peq=0
    for p,b,s in t:
        fixo = p in RAIZ or p.startswith(("INDICE_PUBLICO_PARTES/","central_publica_22out/"))
        if fixo or b not in seen: keep+=1; ks+=s
        elif s<1024: peq+=1
        seen.add(b)
    print("%-24s hoje %7d | autocontido: %7d arquivos %.2f GB | viram referência %7d (dos quais %d com menos de 1 KB)" % (r,len(t),keep,ks/1e9,len(t)-keep,peq))
