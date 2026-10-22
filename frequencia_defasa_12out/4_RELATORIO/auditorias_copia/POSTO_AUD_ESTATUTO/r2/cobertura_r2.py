# -*- coding: utf-8 -*-
# Auditor de estatuto (r2): cobertura do mapeamento do pre-registro, implementacao PROPRIA da regra declarada
# («linhas nao vazias; corte apos . ! ? seguido de maiuscula, aspas, asterisco ou parentese, exceto apos digito»).
import re, json, os, hashlib, unicodedata
W = r"C:\IALD\Central de Patentes\work"
U = os.path.join(W, "frequencia_defasa_12out")
T = {"V1": os.path.join(W, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
     "V2": os.path.join(W, "cunhagens_12out", "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
     "V3": os.path.join(W, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"),
     "V4": os.path.join(W, "cunhagens_10out", "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt")}
PRE = json.load(open(os.path.join(U, "1_PREREGISTRO", "PREREGISTRO.json"), encoding="utf-8"))
rows = {r[0]: r for r in PRE["b_mapeamento"]["linhas"]}
corte = re.compile(r'(?<=[^0-9][.!?])\s+(?=[A-Z\u00C0-\u00DD"\u201C*(])')
segs = []
for k, p in T.items():
    t = open(p, "rb").read().decode("utf-8")
    for i, ln in enumerate(t.split("\n"), 1):
        if not ln.strip(): continue
        if k == "V2" and i >= 34: continue  # F1.TEMPO
        if re.match(r"^\s*-{3,}\s*$", ln):
            segs.append((f"{k}.L{i:02d}.M", ln)); continue
        for j, s in enumerate([x for x in corte.split(ln.strip()) if x.strip()], 1):
            segs.append((f"{k}.L{i:02d}.S{j}", s))
def nz(s):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"^\s*(#+\s*|\*\s+)", "", s)
    s = s.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip()
res = {"segmentos_auditor": len(segs), "linhas_preregistro": len(rows), "faltando_no_mapa": [], "sobrando_no_mapa": [],
       "sha16_divergente": [], "input_nao_verbatim": [], "igualdade_V2_V1": [], "marcas": {}}
ids = set()
txt = dict(segs)
for sid, s in segs:
    ids.add(sid)
    r = rows.get(sid)
    if r is None:
        res["faltando_no_mapa"].append(sid); continue
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
    if r[2] != h: res["sha16_divergente"].append([sid, r[2], h])
    res["marcas"][r[3]] = res["marcas"].get(r[3], 0) + 1
    if r[1].startswith("="):
        par = r[1][1:]
        a, b = nz(txt[par]), nz(s)
        res["igualdade_V2_V1"].append({"id": sid, "par": par, "bytes_iguais": txt[par] == s, "iguais_sem_markdown": a == b})
    elif r[3] == "[INPUT da gerência]" and r[1] != s:
        res["input_nao_verbatim"].append(sid)
res["sobrando_no_mapa"] = sorted(set(rows) - ids)
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "COBERTURA_R2_AUDITOR.json")
open(dest, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "igualdade_V2_V1"}, ensure_ascii=False, indent=1))
print("igualdades V2=V1:", sum(1 for x in res["igualdade_V2_V1"] if x["iguais_sem_markdown"]), "/", len(res["igualdade_V2_V1"]),
      "; byte-identicas:", sum(1 for x in res["igualdade_V2_V1"] if x["bytes_iguais"]))
for x in res["igualdade_V2_V1"]:
    if not x["bytes_iguais"]: print("  so sem markdown:", x["id"], "=", x["par"])
