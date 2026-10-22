# Auditoria de estatuto F1.TEMPO: cobertura do mapeamento das 23 frases (somente leitura).
import json, hashlib, re, sys, unicodedata
OP = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
PJ = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
raw = open(OP, "rb").read()
assert hashlib.sha256(raw).hexdigest().startswith("2c8b7b712aa9ad7f")
seg2 = raw[2853:]
assert hashlib.sha256(seg2).hexdigest().startswith("6dcefdbe5c6a7752")
s2 = seg2.decode("utf-8")
d = json.load(open(PJ, encoding="utf-8"))
out = {"frases": [], "resumo": {}}
marks = {}
tot_lac = 0
pos = 0
covered_sent = []
for f in d["mapeamento_frases"]:
    t = f["texto"]
    i = s2.find(t)
    ok_sub = i >= 0
    h = hashlib.sha256(t.encode("utf-8")).hexdigest()
    cov = [False] * len(t)
    cls = []
    for c in f["clausulas"]:
        tr = c["trecho"]
        j = t.find(tr)
        exact = j >= 0
        if exact:
            for k in range(j, j + len(tr)):
                cov[k] = True
        else:
            # tenta achar sem enfase/aspas normalizadas
            pass
        m = c["marca"]
        for tag in re.findall(r"\[([^\]]+)\]", m):
            marks[tag] = marks.get(tag, 0) + 1
        cls.append({"trecho": tr, "marca": m, "substring_exata_da_frase": exact, "testes": c.get("testes", [])})
    # lacunas: trechos nao cobertos com letras
    lac = []
    k = 0
    while k < len(t):
        if not cov[k]:
            j = k
            while j < len(t) and not cov[j]:
                j += 1
            piece = t[k:j]
            letters = re.findall(r"[A-Za-zÀ-ÿ]+", piece)
            if letters:
                lac.append(piece)
            k = j
        else:
            k += 1
    tot_lac += len(lac)
    out["frases"].append({"frase": f["frase"], "sha16": h[:16], "sha_confere_json": h == f["sha256"],
                          "texto_e_substring_do_verbatim": ok_sub, "clausulas": cls, "lacunas_com_letras": lac})
out["resumo"]["n_frases"] = len(d["mapeamento_frases"])
out["resumo"]["n_clausulas"] = sum(len(f["clausulas"]) for f in d["mapeamento_frases"])
out["resumo"]["etiquetas"] = marks
out["resumo"]["clausulas_nao_exatas"] = [(f["frase"], c["trecho"]) for f in out["frases"] for c in f["clausulas"] if not c["substring_exata_da_frase"]]
out["resumo"]["frases_com_lacuna"] = {f["frase"]: f["lacunas_com_letras"] for f in out["frases"] if f["lacunas_com_letras"]}
# frases do verbatim que nao aparecem no mapeamento (tiling)
cover2 = [False]*len(s2)
for f in d["mapeamento_frases"]:
    i = s2.find(f["texto"])
    if i >= 0:
        for k in range(i, i+len(f["texto"])): cover2[k] = True
rest = []
k = 0
while k < len(s2):
    if not cover2[k]:
        j = k
        while j < len(s2) and not cover2[j]: j += 1
        if re.search(r"[A-Za-zÀ-ÿ]", s2[k:j]): rest.append(s2[k:j])
        k = j
    else: k += 1
out["resumo"]["texto_do_verbatim_fora_das_23_frases_com_letras"] = rest
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out["resumo"], ensure_ascii=False, indent=1))
