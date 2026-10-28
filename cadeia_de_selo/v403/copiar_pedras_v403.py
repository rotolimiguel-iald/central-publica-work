# -*- coding: utf-8 -*-
"""copiar_pedras_v403.py -- copia de BYTES das TRES pedras para v403\\pedra\\, depois de conferir o sha16 de cada uma contra o que o PLANO_v403.md deu (pedras_sha16_da_ordem.json, gerado por gerar_pino_das_pedras_v403.py; o arquivo manda e a divergencia ABORTA)
e contra a copia compilada no sandbox de desenvolvimento onde ela foi provada (C:\\t\\k403c\\final; so' leitura). As pedras vem de v403_kernel\\pedras (a construcao de 27/10/2026, so' leitura): so' o arquivo .lean e' copiado.
Reexecutavel: o que existe e e' igual fica; o que difere aborta.   uso: python -I -B -X utf8 copiar_pedras_v403.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v403 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
os.makedirs(os.path.join(HERE, "pedra"), exist_ok=True)
rep = {}
for s, pf in zip(DL.STONES, DL.pedras_fontes()):
    b = open(s["origem"], "rb").read()
    k = os.path.join(s["compilado_em"], *s["rel"].split("/"))
    assert open(k, "rb").read() == b, ("a pedra compilada no sandbox de desenvolvimento difere da fonte aprovada", s["name"], k)
    d = s["src"]
    if os.path.exists(d):
        assert open(d, "rb").read() == b, ("a copia em v403\\pedra ja existe e DIFERE: nao sobrescrevo", s["name"])
    else:
        open(d + ".tmp", "wb").write(b); assert os.path.getsize(d + ".tmp") == len(b); os.replace(d + ".tmp", d)
    assert open(d, "rb").read() == b
    rep[s["rel"]] = {"sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "origem": s["origem"], "compilado_em": k, "compilado_em_igual": True, "sha16_da_ordem": s["sha16_da_ordem"], "autoria": s["autoria"]}
json.dump(rep, open(os.path.join(HERE, "PEDRAS_COPIA_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha16"] for k, v in rep.items()}, ensure_ascii=False))
