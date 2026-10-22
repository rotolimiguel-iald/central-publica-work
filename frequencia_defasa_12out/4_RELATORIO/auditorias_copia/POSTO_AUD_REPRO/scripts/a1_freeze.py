# -*- coding: utf-8 -*-
# Auditor REPRO, item (1): o FREEZE e anterior a TODOS os arquivos de 2_OPTICO e 3_KERNEL (horarios e hashes).
# So leitura fora da pasta do auditor; grava saidas/A1_FREEZE.json.
import os, sys, json, hashlib, datetime, re

BASE = "C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out"
PRE = os.path.join(BASE, "1_PREREGISTRO")
OPT = os.path.join(BASE, "2_OPTICO")
KER = os.path.join(BASE, "3_KERNEL")
LEV = os.path.join(BASE, "0_LEVANTAMENTO")
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "A1_FREEZE.json")

# valores do FREEZE tal como vieram na ordem do auditor (para comparar com o arquivo)
ORDEM = {
    "congelado_utc": "2026-10-12T16:22:52.525493+00:00",
    "PREREGISTRO.json": (46753, "0c20d7c196a4c7efa75b6eae86fe233c5b12735f1e958f396b3b33a8634df813"),
    "PREREGISTRO.md": (27071, "3c80ea21057c337153f5cf135b3f99677f6b85916677924b47d811bef71ae066"),
}


def sha(p):
    b = open(p, "rb").read()
    return len(b), hashlib.sha256(b).hexdigest()


def tempos(p):
    st = os.stat(p)
    bt = getattr(st, "st_birthtime", None)
    return st.st_mtime, bt


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).isoformat()


fz_path = os.path.join(PRE, "FREEZE.json")
fz_bytes = open(fz_path, "rb").read()
FZ = json.loads(fz_bytes.decode("utf-8"))
t_freeze = datetime.datetime.fromisoformat(FZ["congelado_utc"]).timestamp()
out = {"FREEZE.json": {"bytes": len(fz_bytes), "sha256": hashlib.sha256(fz_bytes).hexdigest()}}
falhas = []

# (a) o FREEZE do arquivo = o FREEZE da ordem
if FZ["congelado_utc"] != ORDEM["congelado_utc"]:
    falhas.append("congelado_utc do arquivo difere da ordem")
for k in ("PREREGISTRO.json", "PREREGISTRO.md"):
    n, s = sha(os.path.join(PRE, k))
    ok = (n, s) == ORDEM[k] and FZ[k]["bytes"] == n and FZ[k]["sha256"] == s
    out[k] = {"bytes": n, "sha256": s, "confere_freeze_e_ordem": ok}
    if not ok:
        falhas.append(k + " nao confere")

# (b) os 27 demais arquivos da pasta: hash e tamanho; nenhum arquivo novo
demais = FZ["demais_arquivos_da_pasta"]
vistos = {}
for dp, dns, fns in os.walk(PRE):
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, PRE).replace("\\", "/")
        mt, bt = tempos(p)
        n, s = sha(p)
        vistos[rel] = {"bytes": n, "sha256": s, "mtime_utc": iso(mt), "birth_utc": iso(bt) if bt else None,
                       "mtime_menos_freeze_s": round(mt - t_freeze, 3), "birth_menos_freeze_s": round(bt - t_freeze, 3) if bt else None}
conf_demais = {}
for rel, (n, s) in demais.items():
    v = vistos.get(rel)
    ok = v is not None and v["bytes"] == n and v["sha256"] == s
    conf_demais[rel] = ok
    if not ok:
        falhas.append("demais: " + rel + " nao confere")
novos = sorted(set(vistos) - set(demais) - {"FREEZE.json", "PREREGISTRO.json", "PREREGISTRO.md"})
if novos:
    falhas.append("arquivos novos em 1_PREREGISTRO: " + ", ".join(novos))
# todo arquivo de 1_PREREGISTRO (exceto o proprio FREEZE) com mtime <= freeze
pre_depois = [r for r, v in vistos.items() if r != "FREEZE.json" and v["mtime_menos_freeze_s"] > 0]
if pre_depois:
    falhas.append("1_PREREGISTRO com mtime depois do freeze: " + ", ".join(pre_depois))
out["1_PREREGISTRO"] = {"n_arquivos": len(vistos), "demais_conferem": all(conf_demais.values()), "n_demais": len(demais),
                        "novos": novos, "mtime_depois_do_freeze": pre_depois,
                        "FREEZE.json_mtime_menos_freeze_s": vistos["FREEZE.json"]["mtime_menos_freeze_s"],
                        "max_mtime_menos_freeze_s_dos_demais": max(v["mtime_menos_freeze_s"] for r, v in vistos.items() if r != "FREEZE.json")}

# (c) todos os arquivos de 2_OPTICO e 3_KERNEL depois do freeze (mtime e criacao)
for nome, raiz in (("2_OPTICO", OPT), ("3_KERNEL", KER)):
    lst = []
    for dp, dns, fns in os.walk(raiz):
        dns.sort()
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, raiz).replace("\\", "/")
            mt, bt = tempos(p)
            n, s = sha(p)
            lst.append({"arq": rel, "bytes": n, "sha256": s, "mtime_utc": iso(mt), "birth_utc": iso(bt) if bt else None,
                        "mtime_menos_freeze_s": round(mt - t_freeze, 3), "birth_menos_freeze_s": round(bt - t_freeze, 3) if bt else None})
    antes = [x["arq"] for x in lst if x["mtime_menos_freeze_s"] <= 0 or (x["birth_menos_freeze_s"] is not None and x["birth_menos_freeze_s"] <= 0)]
    if antes:
        falhas.append(nome + ": arquivos com hora anterior ao freeze: " + ", ".join(antes))
    out[nome] = {"n_arquivos": len(lst), "anteriores_ao_freeze": antes,
                 "menor_mtime_menos_freeze_s": min(x["mtime_menos_freeze_s"] for x in lst),
                 "menor_birth_menos_freeze_s": min(x["birth_menos_freeze_s"] for x in lst if x["birth_menos_freeze_s"] is not None),
                 "primeiro_arquivo": min(lst, key=lambda x: x["mtime_menos_freeze_s"])["arq"],
                 "arquivos": lst}

# (d) os resultados citam os hashes do FREEZE (amarracao por hash)
amarra = {}
for nome, p in (("RESULTADO_OPTICO.json", os.path.join(OPT, "RESULTADO_OPTICO.json")),
                ("RESULTADO_KERNEL.json", os.path.join(KER, "RESULTADO_KERNEL.json")),
                ("2_OPTICO/CONFERENCIA_FREEZE.json", os.path.join(OPT, "CONFERENCIA_FREEZE.json")),
                ("3_KERNEL/CONFERENCIA_FREEZE.json", os.path.join(KER, "CONFERENCIA_FREEZE.json"))):
    t = open(p, "rb").read().decode("utf-8")
    amarra[nome] = {"cita_sha_PREREGISTRO.json": ORDEM["PREREGISTRO.json"][1] in t,
                    "cita_sha_PREREGISTRO.md": ORDEM["PREREGISTRO.md"][1] in t,
                    "cita_sha_FREEZE.json": out["FREEZE.json"]["sha256"] in t}
out["amarracao_por_hash"] = amarra
# horarios internos declarados nos resultados (gerado_utc etc.)
internos = {}
for nome, p in (("RESULTADO_OPTICO.json", os.path.join(OPT, "RESULTADO_OPTICO.json")), ("RESULTADO_KERNEL.json", os.path.join(KER, "RESULTADO_KERNEL.json"))):
    t = open(p, "rb").read().decode("utf-8")
    internos[nome] = sorted(set(re.findall(r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d[.\d]*\+00:00", t)))
out["horarios_internos_declarados"] = internos
internos_antes = {k: [x for x in v if datetime.datetime.fromisoformat(x).timestamp() < t_freeze] for k, v in internos.items()}
out["horarios_internos_anteriores_ao_freeze"] = internos_antes
out["falhas"] = falhas
out["veredito"] = "CONFERE" if not falhas else "NAO_CONFERE"
os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
txt = json.dumps(out, ensure_ascii=False, indent=1)
open(SAIDA, "w", encoding="utf-8").write(txt)
resumo = {k: v for k, v in out.items() if k not in ("2_OPTICO", "3_KERNEL")}
resumo["2_OPTICO"] = {k: v for k, v in out["2_OPTICO"].items() if k != "arquivos"}
resumo["3_KERNEL"] = {k: v for k, v in out["3_KERNEL"].items() if k != "arquivos"}
print(json.dumps(resumo, ensure_ascii=False, indent=1))
