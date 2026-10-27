# -*- coding: utf-8 -*-
"""copiar_pedras_v402.py -- copia de BYTES das TRES pedras para v402\\pedra\\, depois de conferir o sha16 de cada uma contra o que a ORDEM da gerencia deu (pedras_sha16_da_ordem.json; o arquivo manda e a divergencia ABORTA) e contra a copia compilada no sandbox de
desenvolvimento onde ela foi provada (C:\\t\\k402x\\final para a ponte do Codex, C:\\t\\k402\\final para as outras duas; so' leitura). A ponte do Codex vem de Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_025 (pasta SO' LEITURA): so' o arquivo .lean e' copiado (condicao C1 do exame independente;
nenhum outro arquivo da entrega, porque seis deles carregam o hash da fala retirada e a purga exige zero ocorrencia). Reexecutavel: o que existe e e' igual fica; o que difere aborta.
uso: python -I -B -X utf8 copiar_pedras_v402.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v402 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
os.makedirs(os.path.join(HERE, "pedra"), exist_ok=True)
rep = {}
for s, pf in zip(DL.STONES, DL.pedras_fontes()):
    b = open(s["origem"], "rb").read()
    k = os.path.join(s["compilado_em"], *s["rel"].split("/"))
    assert open(k, "rb").read() == b, ("a pedra compilada no sandbox de desenvolvimento difere da fonte aprovada", s["name"], k)
    d = s["src"]
    if os.path.exists(d):
        assert open(d, "rb").read() == b, ("a copia em v402\\pedra ja existe e DIFERE: nao sobrescrevo", s["name"])
    else:
        open(d + ".tmp", "wb").write(b); assert os.path.getsize(d + ".tmp") == len(b); os.replace(d + ".tmp", d)
    assert open(d, "rb").read() == b
    rep[s["rel"]] = {"sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "origem": s["origem"], "compilado_em": k, "compilado_em_igual": True, "sha16_da_ordem": s["sha16_da_ordem"], "autoria": s["autoria"]}
json.dump(rep, open(os.path.join(HERE, "PEDRAS_COPIA_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha16"] for k, v in rep.items()}, ensure_ascii=False))
