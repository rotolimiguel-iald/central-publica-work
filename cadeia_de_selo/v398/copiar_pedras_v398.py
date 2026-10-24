# -*- coding: utf-8 -*-
"""copiar_pedras_v398.py -- copia de BYTES das DUAS pedras (work\\sonico_v398\\Sonico.lean e work\\afinacao_das_cordas_v398\\AfinacaoDasCordas.lean, aprovadas em revisao independente e ratificadas pelo operador) para
v398\\pedra\\, depois de conferir o sha16 de cada uma contra o que a ORDEM da gerencia deu (a317094e337fd8b7 e 66e28e61086cc6ba; o arquivo manda e a divergencia ABORTA) e contra a copia compilada no sandbox de origem
(C:\\t\\k398b, so' leitura). Reexecutavel: o que existe e e' igual fica; o que difere aborta. uso: python -I -B -X utf8 copiar_pedras_v398.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
os.makedirs(os.path.join(HERE, "pedra"), exist_ok=True)
rep = {}
for s, pf in zip(DL.STONES, DL.pedras_fontes()):
    b = open(s["origem"], "rb").read()
    k = os.path.join(DL.SANDBOX_ORIGEM, *s["rel"].split("/"))
    assert open(k, "rb").read() == b, ("a pedra compilada no sandbox de origem (k398b) difere da fonte aprovada", s["name"])
    d = s["src"]
    if os.path.exists(d):
        assert open(d, "rb").read() == b, ("a copia em v398\\pedra ja existe e DIFERE: nao sobrescrevo", s["name"])
    else:
        open(d + ".tmp", "wb").write(b); assert os.path.getsize(d + ".tmp") == len(b); os.replace(d + ".tmp", d)
    assert open(d, "rb").read() == b
    rep[s["rel"]] = {"sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "origem": s["origem"], "sandbox_origem_igual": True}
json.dump(rep, open(os.path.join(HERE, "PEDRAS_COPIA_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha16"] for k, v in rep.items()}, ensure_ascii=False))
