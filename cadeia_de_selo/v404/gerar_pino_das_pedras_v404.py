# -*- coding: utf-8 -*-
"""gerar_pino_das_pedras_v404.py -- escreve pedras_sha16_da_ordem.json (o pino de cada pedra da v404) LENDO o sha16 do arquivo da pedra (work\\projecao_transversal_28out\\*.lean) e CONFERINDO contra o que os RECIBOS de 28/10/2026 deram
(RECIBO_PEDRA_PROJECAO_TRANSVERSAL_28out.json e RECIBO_PEDRA_JO8V32_28out.json: o campo lean.sha256, escrito pela gerencia no momento da compilacao no trio). O arquivo manda; se o recibo e o arquivo divergem, ABORTA (nada e' digitado de memoria).
Confere tambem nos recibos: sorry 0 e todos os teoremas no trio {propext, Classical.choice, Quot.sound}. Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta.
uso: python -I -B -X utf8 gerar_pino_das_pedras_v404.py   (molde: gerar_pino_das_pedras_v403.py)"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PED = os.path.join(os.path.dirname(os.path.dirname(HERE)), "projecao_transversal_28out")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
CHAVES = {"projecao": ("ProjecaoTransversalDaMeiaNat", "RECIBO_PEDRA_PROJECAO_TRANSVERSAL_28out.json", 9),
          "jo8v32": ("Jo8v32", "RECIBO_PEDRA_JO8V32_28out.json", 1)}
pino = {}
detalhe = {}
for k, (nome, recibo, n_teoremas) in CHAVES.items():
    b = open(os.path.join(PED, nome + ".lean"), "rb").read()
    h = hashlib.sha256(b).hexdigest()
    r = json.load(open(os.path.join(PED, recibo), encoding="utf-8"))
    assert r["lean"]["sha256"] == h and r["lean"]["bytes"] == len(b), ("o arquivo da pedra DIVERGE do recibo", nome, h[:16], r["lean"]["sha256"][:16], len(b), r["lean"]["bytes"])
    assert r.get("sorry") == 0, ("o recibo nao diz sorry 0", nome)
    th = r["teoremas_no_trio"]
    assert len(th) == n_teoremas and all(set(v) == TRIO for v in th.values()), ("os teoremas do recibo nao estao todos no trio", nome, list(th))
    pino[k] = h[:16]
    detalhe[k] = {"arquivo": os.path.join(PED, nome + ".lean"), "sha256": h, "bytes": len(b), "recibo": recibo, "recibo_sha256": hashlib.sha256(open(os.path.join(PED, recibo), "rb").read()).hexdigest(), "n_teoremas_no_trio": len(th), "sorry": r["sorry"]}
out = os.path.join(HERE, "pedras_sha16_da_ordem.json")
novo = json.dumps(pino, ensure_ascii=False)
if os.path.exists(out):
    assert open(out, encoding="utf-8").read().strip() == novo, "pedras_sha16_da_ordem.json ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "w", encoding="utf-8", newline="\n").write(novo + "\n"); assert os.path.getsize(out + ".tmp") > 0; os.replace(out + ".tmp", out)
json.dump(detalhe, open(os.path.join(HERE, "PINO_DAS_PEDRAS_DETALHE_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(novo)
