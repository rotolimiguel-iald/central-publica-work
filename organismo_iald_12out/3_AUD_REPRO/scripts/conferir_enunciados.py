# -*- coding: utf-8 -*-
"""Auditor: compara os ENUNCIADOS (do nome ate o ':=' de topo) da pedra do desenho (congelada) com a da construcao."""
import re, json, hashlib, sys
D = r"C:\IALD\Central de Patentes\work\organismo_iald_12out\1_DESENHO_PEDRA\sandbox\IALD.lean"
C = r"C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_REPRO\sandbox\TGLExt\IALD.lean"
def decls(p):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"/-.*?-/", "", t, flags=re.S)
    t = re.sub(r"--[^\n]*", "", t)
    out = {}
    for m in re.finditer(r"^(theorem|def|lemma|abbrev|instance|axiom|opaque)\s+([^\s(:{\[]+)", t, re.M):
        start = m.start()
        i = t.find(":=", m.end())
        stmt = " ".join(t[start:i].split())
        out[m.group(2)] = {"kind": m.group(1), "stmt": stmt}
    return out, t
d, td = decls(D); c, tc = decls(C)
res = {"desenho_sha256": hashlib.sha256(open(D,'rb').read()).hexdigest(),
       "construcao_sha256": hashlib.sha256(open(C,'rb').read()).hexdigest(),
       "n_desenho": len(d), "n_construcao": len(c),
       "so_no_desenho": sorted(set(d)-set(c)), "novas_na_construcao": sorted(set(c)-set(d)),
       "enunciado_diferente": {k: {"desenho": d[k]["stmt"], "construcao": c[k]["stmt"]} for k in d if k in c and d[k]["stmt"] != c[k]["stmt"]},
       "kinds_construcao": {k: v["kind"] for k, v in c.items()},
       "tokens_proibidos_construcao": {w: len(re.findall(r"\b"+w+r"\b", tc)) for w in ["sorry","admit","axiom","native_decide","implemented_by","unsafe","opaque","decide"]},
       "tokens_proibidos_desenho": {w: len(re.findall(r"\b"+w+r"\b", td)) for w in ["sorry","admit","axiom","native_decide","implemented_by","unsafe","opaque"]}}
json.dump(res, open(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_REPRO\medidas\CONFERENCIA_ENUNCIADOS_AUDITOR.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in res if k!="kinds_construcao"}, ensure_ascii=False, indent=1))
