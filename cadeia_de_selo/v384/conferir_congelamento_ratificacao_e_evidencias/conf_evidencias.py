# -*- coding: utf-8 -*-
# Conferencia independente das EVIDENCIAS do V1 (lente ratificacao_e_evidencias). Somente leitura fora desta pasta.
import json, hashlib, os, stat, ctypes
PERM = r"C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out"
V1P = os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
V1M = os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.md")
EVD = os.path.join(PERM, "evidencias_PREREGISTRO_V1")
HERE = os.path.dirname(os.path.abspath(__file__))
FILE_ATTRIBUTE_READONLY = 0x1


def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def attrs(p):
    a = ctypes.windll.kernel32.GetFileAttributesW(p)
    return a


def ro(p):
    a = attrs(p)
    return {"win_attr": a, "readonly_attr": bool(a != -1 and a != 0xFFFFFFFF and (a & FILE_ATTRIBUTE_READONLY)),
            "st_mode_write_bit": bool(os.stat(p).st_mode & stat.S_IWRITE)}


V1 = json.load(open(V1P, encoding="utf-8"))
EV = V1["evidencias"]
res = {"n_entradas": len(EV), "entradas": [], "mudaram_na_origem": [], "copia_difere": [], "copia_ausente": [], "origem_ausente": [],
       "fora_da_pasta": [], "papeis_duplicados": [], "nomes_duplicados": []}
papeis = [e["papel"] for e in EV]
res["papeis_duplicados"] = sorted({p for p in papeis if papeis.count(p) > 1})
nomes = []
for e in EV:
    cp = e.get("copia_permanente")
    r = {"papel": e["papel"], "origem": e["origem"], "sha256_gravado": e["sha256"], "copia_permanente": cp}
    if not cp:
        r["sem_copia_permanente"] = True
    else:
        if os.path.normcase(os.path.dirname(cp)) != os.path.normcase(EVD):
            res["fora_da_pasta"].append(e["papel"])
        nomes.append(os.path.basename(cp))
        if os.path.exists(cp):
            r["sha256_copia"] = fsha(cp)
            r["copia_eq_gravado"] = r["sha256_copia"] == e["sha256"]
            r["copia_ro"] = ro(cp)
            r["copia_bytes"] = os.path.getsize(cp)
            if not r["copia_eq_gravado"]:
                res["copia_difere"].append(e["papel"])
        else:
            r["copia_existe"] = False
            res["copia_ausente"].append(e["papel"])
    if os.path.exists(e["origem"]):
        r["sha256_origem_agora"] = fsha(e["origem"])
        r["origem_eq_gravado"] = r["sha256_origem_agora"] == e["sha256"]
        r["origem_bytes"] = os.path.getsize(e["origem"])
        r["origem_mtime"] = os.path.getmtime(e["origem"])
        if not r["origem_eq_gravado"]:
            res["mudaram_na_origem"].append(e["papel"])
    else:
        r["origem_existe"] = False
        res["origem_ausente"].append(e["papel"])
    res["entradas"].append(r)
res["nomes_duplicados"] = sorted({n for n in nomes if nomes.count(n) > 1})
na_pasta = sorted(os.listdir(EVD))
res["arquivos_na_pasta"] = na_pasta
res["n_arquivos_na_pasta"] = len(na_pasta)
res["a_mais_na_pasta"] = sorted(set(na_pasta) - set(nomes))
res["a_menos_na_pasta"] = sorted(set(nomes) - set(na_pasta))
res["subpastas"] = [x for x in na_pasta if os.path.isdir(os.path.join(EVD, x))]
res["todos_ro_na_pasta"] = all(ro(os.path.join(EVD, x))["readonly_attr"] for x in na_pasta)
res["nao_ro_na_pasta"] = [x for x in na_pasta if not ro(os.path.join(EVD, x))["readonly_attr"]]
res["v1_json_ro"] = ro(V1P)
res["v1_md_ro"] = ro(V1M)
res["pasta_evidencias_attr"] = attrs(EVD)
res["v1_json_sha256"] = fsha(V1P)
res["v1_md_sha256"] = fsha(V1M)
# o MD traz o mesmo verbatim e o mesmo spec?
md = open(V1M, encoding="utf-8").read()
res["md_contem_verbatim"] = V1["ratificacao_do_operador"]["verbatim"] in md
res["md_contem_spec_sha"] = V1["spec_sha256"] in md
res["md_contem_sha_da_linha"] = V1["ratificacao_do_operador"]["transcrito"]["sha256_das_linhas_da_mensagem"][0] in md
# o gerador nas evidencias = o gerador da pasta permanente?
ger = os.path.join(PERM, "gerar_preregistro_pilar_quantico_03out.py")
res["gerador_permanente_sha256"] = fsha(ger)
g = [e for e in EV if e["papel"] == "gerador"]
res["gerador_evidencia_origem"] = g[0]["origem"] if g else None
res["gerador_evidencia_sha_eq_permanente"] = bool(g) and g[0]["sha256"] == res["gerador_permanente_sha256"]
rascger = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\rascunho_prereg_v13\gerar_preregistro_pilar_quantico_03out.py"
res["gerador_do_rascunho_sha256"] = fsha(rascger)
res["gerador_do_rascunho_eq_permanente"] = res["gerador_do_rascunho_sha256"] == res["gerador_permanente_sha256"]
with open(os.path.join(HERE, "resultado_evidencias.json"), "w", encoding="utf-8") as fo:
    json.dump(res, fo, ensure_ascii=False, indent=1)
for r in res["entradas"]:
    print("%-28s copia=%s origem=%s ro=%s" % (r["papel"], r.get("copia_eq_gravado"), r.get("origem_eq_gravado"), (r.get("copia_ro") or {}).get("readonly_attr")))
print(json.dumps({k: v for k, v in res.items() if k != "entradas"}, ensure_ascii=False, indent=1))
