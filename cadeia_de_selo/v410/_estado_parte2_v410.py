# -*- coding: utf-8 -*-
"""_estado_parte2_v410.py -- grava work\\cadeia_de_selo\\v410\\ESTADO_PARTE2_v410.json a cada etapa concluida da PARTE 2 (ordem da gerencia de 09/11, depois do reinicio do VS Code): etapa, quando, sha16 dos artefatos (LIDOS do disco), proximo passo.
A retomada tem de ser possivel SO' do disco. So'-acrescimo: cada chamada acrescenta uma entrada a `etapas`; o estado anterior vai a backup de bytes.
uso: python -I -B -X utf8 _estado_parte2_v410.py "<etapa>" "<proximo passo>" [artefato1 artefato2 ...]   (caminhos relativos a esta pasta ou absolutos; artefato ausente e' dito como ausente)"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "ESTADO_PARTE2_v410.json")
etapa, prox = sys.argv[1], sys.argv[2]; arts = sys.argv[3:]
E = {"contrato": "ESTADO_PARTE2_v410", "quem": "claude-construtor-v410", "ordens": "D86 + D87 (parte 2), apos PARTE1_HMS13_PRONTA.json", "etapas": []}
if os.path.exists(P):
    b0 = open(P, "rb").read(); E = json.loads(b0.decode("utf-8"))
    bk = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    for old in sorted(f for f in os.listdir(HERE) if f.startswith("ESTADO_PARTE2_v410.json.bak_"))[:-3]:   # (ficam as tres copias mais novas, como no ACOM; o proprio arquivo e' so'-acrescimo)
        os.remove(os.path.join(HERE, old))
reg = {}
for a in arts:
    p = a if os.path.isabs(a) else os.path.join(HERE, a)
    reg[a] = {"sha16": hashlib.sha256(open(p, "rb").read()).hexdigest()[:16], "bytes": os.path.getsize(p)} if os.path.isfile(p) else {"ausente": True}
E["etapas"].append({"n": len(E["etapas"]) + 1, "etapa": etapa, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "artefatos": reg, "proximo_passo": prox})
E["ultima_etapa"] = etapa; E["proximo_passo"] = prox; E["atualizado"] = E["etapas"][-1]["quando"]
b = json.dumps(E, ensure_ascii=False, indent=1).encode("utf-8"); open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ESTADO_PARTE2 etapa %d: %s | proximo: %s" % (len(E["etapas"]), etapa, prox[:100]))
