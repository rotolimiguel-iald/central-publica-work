# -*- coding: utf-8 -*-
# Confere a cobertura do mapeamento (b) do pre-registro: toda frase da trilha tem linha? marcas por classe.
import json, sys, hashlib, re, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segmentar_copia as S
PRE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\1_PREREGISTRO\PREREGISTRO.json"
pre = json.load(open(PRE, encoding="utf-8"))
linhas = pre["b_mapeamento"]["linhas"]
ids_map = {l[0]: l for l in linhas}
faltam, extra = [], []
segs_all = {}
for c in ("V1", "V2", "V3", "V4"):
    segs, h, n, fr = S.segmentos(c)
    for s in segs:
        segs_all[s["id"]] = s
        if s["escopo"] != "TRILHA_POSTO":
            continue
        if s["id"] not in ids_map:
            faltam.append(s["id"])
for k in ids_map:
    if k not in segs_all:
        extra.append(k)
# sha16 da frase integra confere?
sha_ok, sha_bad = 0, []
for k, l in ids_map.items():
    s = segs_all.get(k)
    if not s: continue
    h16 = hashlib.sha256(s["texto"].encode("utf-8")).hexdigest()[:16]
    if h16 == l[2]: sha_ok += 1
    else: sha_bad.append((k, h16, l[2]))
# marcas [ONTO] cuja leitura diz DECLARADO/OPEN/KNOWN
onto_dec = [(l[0], l[4]) for l in linhas if l[3] == "[ONTO]" and re.search(r"DECLARADO|OPEN|KNOWN", l[4])]
onto_sem = [(l[0], l[4]) for l in linhas if l[3] == "[ONTO]" and not re.search(r"DECLARADO|OPEN|KNOWN", l[4]) and not l[4].startswith("idem")]
inp_onto = [(l[0], l[4]) for l in linhas if l[3].startswith("[INPUT") and "ONTO" in l[4]]
out = {"n_linhas_mapa": len(linhas), "frases_da_trilha_sem_linha": faltam, "linhas_sem_frase": extra,
       "sha16_conferem": sha_ok, "sha16_divergem": sha_bad,
       "ONTO_cuja_leitura_e_DECLARADO_OPEN_KNOWN": onto_dec, "ONTO_puro": onto_sem,
       "INPUT_com_parte_ONTO": inp_onto}
json.dump(out, open("COBERTURA_MAPEAMENTO.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in out.items()}, ensure_ascii=False, indent=1))
print("ONTO->DECLARADO/OPEN/KNOWN:", [x[0] for x in onto_dec])
print("ONTO puro:", [x[0] for x in onto_sem])
print("INPUT com parte ONTO:", [x[0] for x in inp_onto])
print("sha divergem:", sha_bad)
