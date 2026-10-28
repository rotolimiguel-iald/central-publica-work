# -*- coding: utf-8 -*-
"""copiar_logs_do_kernel_v403.py -- copia de BYTES dos logs da CONSTRUCAO de 27/10/2026 (feita no sandbox C:\\t\\k403c\\final pela gerencia c1: `lake build` incremental + `lake env lean TGL/Audit.lean`, 08:43 a 08:53, rc 0) de
..\\v403_kernel\\ (lake_build.log, audit.log, construir_marcas.txt) para v403\\kernel\\, onde pos_build_kernel_v403.py os le (o molde: construir_kernel_v403.sh escreve ali). Confere antes que construir_marcas.txt diz rc=0, rc_build=0 e rc_audit=0 e que a linha
TGL_AXIOM_COVERAGE_TOTAL do build e a do audit sao a mesma; grava kernel\\LOGS_COPIADOS_v403.json (sha256 de cada log e das marcas). Reexecutavel: o que existe e e' igual fica; o que difere aborta (nao sobrescreve).
uso: python -I -B -X utf8 copiar_logs_do_kernel_v403.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ORI = os.path.join(os.path.dirname(HERE), "v403_kernel"); DST = os.path.join(HERE, "kernel")
sha = lambda b: hashlib.sha256(b).hexdigest()
os.makedirs(DST, exist_ok=True)
marcas = open(os.path.join(ORI, "construir_marcas.txt"), encoding="utf-8").read()
assert re.search(r"^rc=0$", marcas, re.M) and re.search(r"rc_build=0\b", marcas) and re.search(r"rc_audit=0\b", marcas), ("a construcao de 27/10 nao deu rc 0", marcas)
cov = {}
rep = {}
for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
    b = open(os.path.join(ORI, nome), "rb").read(); d = os.path.join(DST, nome)
    if os.path.exists(d):
        assert open(d, "rb").read() == b, ("o log ja existe em kernel\\ e DIFERE da origem: nao sobrescrevo", nome)
    else:
        open(d + ".tmp", "wb").write(b); assert os.path.getsize(d + ".tmp") == len(b); os.replace(d + ".tmp", d)
    assert open(d, "rb").read() == b
    rep[nome] = {"bytes": len(b), "sha256": sha(b), "origem": os.path.join(ORI, nome)}
    if nome.endswith(".log"):
        m = re.findall(rb"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\r\n]*", b)
        cov[nome] = [x.decode() for x in m]
assert cov["lake_build.log"] and cov["lake_build.log"] == cov["audit.log"], ("a linha de cobertura do build e a do audit diferem", cov)
rep["cobertura_linha"] = cov["audit.log"]
json.dump(rep, open(os.path.join(DST, "LOGS_COPIADOS_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v["sha256"][:16] if isinstance(v, dict) else v) for k, v in rep.items()}, ensure_ascii=False))
