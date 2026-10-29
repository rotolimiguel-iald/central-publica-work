# -*- coding: utf-8 -*-
"""copiar_pedras_v404.py -- copia de BYTES das DUAS pedras para v404\\pedra\\, depois de conferir o sha16 de cada uma contra o que a ordem deu (pedras_sha16_da_ordem.json, gerado por gerar_pino_das_pedras_v404.py a partir dos recibos de 28/10/2026; o arquivo manda e a divergencia ABORTA).
A fonte e' work\\projecao_transversal_28out (a construcao de 28/10/2026, so' leitura). Nesta preparacao as pedras ainda NAO estao no sandbox C:\\t\\k404c\\final (elas entram em preparar_kernel_v404.py gerar), logo a conferencia contra o sandbox so' e' feita
se o arquivo ja existir la (o compilado de 28/10 foi provado em C:\\t\\k403c\\final por `lake env lean`, ver os recibos). Reexecutavel: o que existe e e' igual fica; o que difere aborta.   uso: python -I -B -X utf8 copiar_pedras_v404.py
Molde: copiar_pedras_v403.py."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
os.makedirs(os.path.join(HERE, "pedra"), exist_ok=True)
rep = {}
for s, pf in zip(DL.STONES, DL.pedras_fontes()):
    b = open(s["origem"], "rb").read()
    k = os.path.join(s["compilado_em"], *s["rel"].split("/"))
    k_igual = None
    if os.path.exists(k):
        assert open(k, "rb").read() == b, ("a pedra no sandbox difere da fonte aprovada", s["name"], k)
        k_igual = True
    d = s["src"]
    if os.path.exists(d):
        assert open(d, "rb").read() == b, ("a copia em v404\\pedra ja existe e DIFERE: nao sobrescrevo", s["name"])
    else:
        open(d + ".tmp", "wb").write(b); assert os.path.getsize(d + ".tmp") == len(b); os.replace(d + ".tmp", d)
    assert open(d, "rb").read() == b
    rep[s["rel"]] = {"sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "origem": s["origem"], "no_sandbox": k, "no_sandbox_igual": k_igual, "sha16_da_ordem": s["sha16_da_ordem"], "autoria": s["autoria"]}
json.dump(rep, open(os.path.join(HERE, "PEDRAS_COPIA_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha16"] for k, v in rep.items()}, ensure_ascii=False))
