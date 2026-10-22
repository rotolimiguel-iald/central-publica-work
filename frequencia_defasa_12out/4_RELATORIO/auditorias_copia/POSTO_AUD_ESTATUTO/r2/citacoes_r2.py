# -*- coding: utf-8 -*-
# Auditor de estatuto (r2): toda citacao entre «» na pedra r2 e conferida contra os BYTES das fontes.
# Regra: espacos/quebras normalizados (comentario Lean quebra linhas); «…» = recorte (cada pedaco tem de estar na fonte, em ordem).
import re, json, os, sys, hashlib
W = r"C:\IALD\Central de Patentes\work"
U = os.path.join(W, "frequencia_defasa_12out")
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xf3) + "s"
PEDRA = os.path.join(U, "3_KERNEL", "rodada2", "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
fontes = {
 "V1": os.path.join(W, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
 "V2": os.path.join(W, "cunhagens_12out", "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
 "V3": os.path.join(W, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"),
 "V4": os.path.join(W, "cunhagens_10out", "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"),
 "um.py": os.path.join(NOS, "um.py"),
}
txt = {}
for k, p in fontes.items():
    b = open(p, "rb").read()
    txt[k] = b.decode("utf-8")
# kernel .lean (docstrings citadas)
KR = os.path.join(NOS, "tgl_kernel")
klean = []
for dp, dn, fn in os.walk(KR):
    if ".lake" in dp: continue
    for f in fn:
        if f.endswith(".lean"):
            klean.append(open(os.path.join(dp, f), "rb").read().decode("utf-8", "replace"))
txt["kernel"] = "\n".join(klean)
def norm(s):
    s = s.replace("\r\n", "\n")
    s = re.sub(r"\s+", " ", s)
    return s.strip()
ntxt = {k: norm(v) for k, v in txt.items()}
def which(q):
    parts = [norm(p) for p in re.split(r"\s*…\s*", q) if norm(p)]
    res = []
    for k, t in ntxt.items():
        pos = 0; ok = True
        for p in parts:
            i = t.find(p, pos)
            if i < 0: ok = False; break
            pos = i + len(p)
        if ok: res.append(k)
    return res
src = open(PEDRA, "rb").read().decode("utf-8")
quotes = re.findall(r"«(.*?)»", src, flags=re.S)
out = []
for q in quotes:
    w = which(q)
    out.append({"citacao": norm(q)[:220], "fontes_onde_esta": w})
nao = [o for o in out if not o["fontes_onde_esta"]]
rel = {"pedra": PEDRA, "pedra_sha256": hashlib.sha256(open(PEDRA,"rb").read()).hexdigest(),
       "n_citacoes": len(out), "n_sem_fonte": len(nao), "sem_fonte": nao, "todas": out}
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CITACOES_PEDRA_R2_AUDITOR.json")
open(dest, "w", encoding="utf-8").write(json.dumps(rel, ensure_ascii=False, indent=1))
print("citacoes:", len(out), "sem fonte nos bytes:", len(nao))
for o in out:
    print(("OK  " if o["fontes_onde_esta"] else "XX  ") + ",".join(o["fontes_onde_esta"]) + " | " + o["citacao"][:150])
