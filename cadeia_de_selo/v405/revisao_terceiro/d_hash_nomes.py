# -*- coding: utf-8 -*-
import glob, hashlib, os, re, sys, json, subprocess
sys.stdout.reconfigure(encoding="utf-8")
W="C:/IALD/Central de Patentes/work/"; R=W+"cadeia_de_selo/v405/"; K="C:/t/k405c/final/"
# 1. mapa de hashes: arquivos de falas, recibos, insumos, pedras, base
mapa={}
dirs=[W+"cunhagens_13out",W+"experimento_espelho_30out",W+"projecao_transversal_28out",W+"cadeia_de_selo405",W+"e0_cadeia_31out",W+"observador_terminal_31out",W+"grande_atrator_reclassificacao_01nov",R+"insumos",R+"pedra",R+"base_v404",W+"leitura_cria_o_objeto_07out"]
n=0
for d in dirs:
    for r,ds,fs in os.walk(d):
        for f in fs:
            p=os.path.join(r,f)
            try:
                if os.path.getsize(p)>60_000_000: continue
                h=hashlib.sha256(open(p,"rb").read()).hexdigest(); mapa.setdefault(h,p); n+=1
            except Exception as e: pass
print("arquivos com hash",n)
pref={}
for h,p in mapa.items():
    for L in (16,):
        pref.setdefault(h[:L],p)
arqs=sorted(glob.glob(R+"pedra/*.lean"))+[R+"delta_v405.py",R+"registros_v405.py",R+"runtime_v405.py",R+"artigo_pt_v405.pysnip",R+"artigo_en_v405.pysnip"]
visto={}
for p in arqs:
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r"(?<![0-9a-fA-F])([0-9a-f]{16,64})(?![0-9a-fA-F])",t):
        x=m.group(1)
        if not re.search(r"[a-f]",x) or not re.search(r"[0-9]",x): continue
        visto.setdefault(x,set()).add(os.path.basename(p))
ok=0; ruins={}
for x,fs in visto.items():
    if x[:16] in pref and (len(x)==16 or hashlib.sha256(open(pref[x[:16]],"rb").read()).hexdigest().startswith(x)): ok+=1
    else: ruins[x]=sorted(fs)
print("hex citados",len(visto),"conferem",ok); print("sem arquivo:",json.dumps(ruins,indent=0)[:1500])
# 2. identificadores
src={}
for p in glob.glob(K+"TGLExt/**/*.lean",recursive=True)+glob.glob(K+"TGL/**/*.lean",recursive=True):
    try: src[p]=open(p,encoding="utf-8").read()
    except: pass
blob="\n".join(src.values())
print("fontes",len(src),len(blob))
decl=set(re.findall(r"(?:theorem|lemma|def|abbrev|structure|inductive|class|instance)\s+([^\s:({\[]+)",blob))
last={d.split(".")[-1] for d in decl}|decl
fields=set(re.findall(r"^\s+([A-Za-z_][\w']*)\s*:",blob,re.M))
ids={}
for p in sorted(glob.glob(R+"pedra/*.lean")):
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r"`([^`\n]{3,70})`",t):
        ids.setdefault(m.group(1),set()).add(os.path.basename(p))
for p in [R+"artigo_pt_v405.pysnip",R+"artigo_en_v405.pysnip"]:
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r"\texttt\{([^{}]{3,70})\}",t):
        ids.setdefault(m.group(1).replace("\_","_"),set()).add(os.path.basename(p))
falt={}
for i,fs in ids.items():
    x=i.strip()
    if not re.fullmatch(r"[A-Za-z_][\w'.]*",x): continue
    base=x.split(".")[-1]
    if x in last or base in last or base in fields or x.endswith(".lean"): continue
    falt[x]=sorted(fs)
print("ids testados",len(ids)); print(json.dumps(falt,ensure_ascii=False,indent=0))
