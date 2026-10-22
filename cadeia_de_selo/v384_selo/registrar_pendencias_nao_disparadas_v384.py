# -*- coding: utf-8 -*-
"""Os achados da verificacao da cadeia (workflow_verificacao_cadeia_resultado.json) que NAO foram corrigidos porque so disparam fora do ramo 9 do pilar;
a rodada real concluiu no ramo 9 (lido do core aqui), entao os textos gravados nao os contem. Ficam ditos para a proxima cadeia (v385+). So leitura do core."""
import json, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
core = json.load(open(os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "um_absoluto.json"), encoding="utf-8"))["core"]
v = core["quantum_pillar_v384"]["verdict"]
W = json.load(open(os.path.join(HERE, "workflow_verificacao_cadeia_resultado.json"), encoding="utf-8"))["result"]
pend = []
for g in W["grupos"]:
    r = g["resultado"] or {}
    pend += [{"grupo": g["grupo"], "tipo": "item_parcial", **x} for x in r.get("itens", []) if x["estado"] != "RESOLVIDO"]
    pend += [{"grupo": g["grupo"], "tipo": "novo", **x} for x in r.get("novos", [])]
rec = {"o_que_e": __doc__.strip(), "veredito_do_pilar_desta_rodada": v, "ramo_9": v.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE"),
       "fonte": {"arquivo": "workflow_verificacao_cadeia_resultado.json", "sha256": hashlib.sha256(open(os.path.join(HERE, "workflow_verificacao_cadeia_resultado.json"), "rb").read()).hexdigest()},
       "pendencias": pend}
out = os.path.join(HERE, "PENDENCIAS_NAO_DISPARADAS_v384.json")
b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
print("pendencias:", len(pend), "| ramo 9:", rec["ramo_9"], "|", hashlib.sha256(b).hexdigest()[:16])
