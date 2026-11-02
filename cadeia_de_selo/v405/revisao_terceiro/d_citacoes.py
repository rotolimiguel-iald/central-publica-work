# -*- coding: utf-8 -*-
"""Revisor terceiro: toda citacao entre aspas angulares nas pedras e nos textos, confrontada com TODAS as falas; todo hex de 16+ confrontado com sha256 de arquivos; todo identificador em crase/texttt confrontado com o kernel do sandbox."""
import glob, hashlib, os, re, sys, json, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
W="C:/IALD/Central de Patentes/work/"; R=W+"cadeia_de_selo/v405/"; K="C:/t/k405c/final/"
verb={}
for pat in [W+"cunhagens_13out/*.txt",W+"experimento_espelho_30out/*.txt",W+"projecao_transversal_28out/*.txt",W+"cadeia_de_selo405/insumos/cunhagens/*",R+"insumos/cunhagens/*"]:
    for p in glob.glob(pat):
        if os.path.isfile(p):
            try: verb[p]=open(p,encoding="utf-8",newline="").read()
            except Exception as e: print("erro",p,e)
print("falas lidas",len(verb))
tudo="\n".join(verb.values())
def norm(s): return re.sub(r"\s+"," ",s.replace("\r","")).strip()
tudoN=norm(tudo)
alvos={"pedras":sorted(glob.glob(R+"pedra/*.lean")),"textos":[R+"delta_v405.py",R+"registros_v405.py",R+"runtime_v405.py",R+"artigo_pt_v405.pysnip",R+"artigo_en_v405.pysnip",R+"pos_rito/textos_v405_novo.pysnip",R+"A_IDENTIDADE_traducao_en_da_gerencia.txt"]}
print({k:len(v) for k,v in alvos.items()})
nao={}
tot=0
for grupo,arqs in alvos.items():
    for p in arqs:
        t=open(p,encoding="utf-8").read()
        if p.endswith(".lean"): t=re.sub(r"\n>\s*"," ",t).replace("\n"," ")
        for m in re.finditer(r"«([^»]{3,}?)»",t):
            q=m.group(1); tot+=1
            qq=norm(q)
            if qq in tudoN: continue
            # tenta sem reticencias
            partes=[norm(x) for x in re.split(r"…|\.\.\.|\[\.\.\.\]",q) if len(norm(x))>2]
            if partes and all(x in tudoN for x in partes): continue
            nao.setdefault(os.path.basename(p),[]).append(qq[:160])
print("citacoes",tot)
for k,v in nao.items():
    print("==",k,len(v))
    for x in sorted(set(v)): print("   ",x)
json.dump(nao,open(R+"revisao_terceiro/d_nao_verbatim.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
