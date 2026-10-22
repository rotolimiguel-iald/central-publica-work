# -*- coding: utf-8 -*-
"""Congela o pre-registro: confere as citacoes do operador contra os bytes do verbatim e grava FREEZE.json
com sha256 de cada anexo e o horario. Recusa sobrescrever um FREEZE existente."""
import os, json, hashlib, datetime, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(AQUI)
V = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_identidade_cordeiro_verbatim.txt"
alvo = os.path.join(AQUI, "FREEZE.json")
if os.path.exists(alvo):
    print("RECUSA: FREEZE.json ja existe; o congelado nao se altera (so ADENDO)"); sys.exit(2)
vb = open(V, "rb").read()
vt = vb.decode("utf-8")
assert hashlib.sha256(vb).hexdigest() == "2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e"
pj = json.load(open(os.path.join(AQUI, "PREREGISTRO.json"), encoding="utf-8"))
cit = []
for a in pj["afirmacoes"]:
    for q in re.findall(r"«([^»]+)»", a["frase"]):
        frags = [f.strip() for f in q.split("…")]
        ok = all(f.replace('\\"', '"') in vt for f in frags if f)
        cit.append({"id": a["id"], "citacao": q, "nos_bytes": ok})
ruins = [c for c in cit if not c["nos_bytes"]]
anexos = ["2_PREREGISTRO/PREREGISTRO.json", "2_PREREGISTRO/PREREGISTRO.md", "2_PREREGISTRO/congelar.py",
          "1_LEVANTAMENTO/LEVANTAMENTO.md", "1_LEVANTAMENTO/LEVANTAMENTO_DADOS.json", "1_LEVANTAMENTO/levantar.py",
          "0_FONTES/Conscious_Singularity.txt"]
h = {a: hashlib.sha256(open(os.path.join(W, a), "rb").read()).hexdigest() for a in anexos}
h["VERBATIM:" + V] = hashlib.sha256(vb).hexdigest()
fz = {"unidade": "F1.IDENTIDADE", "congelado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "congelado_em_local": datetime.datetime.now().astimezone().isoformat(),
      "pedra_existe_no_congelamento": os.path.exists("C:/t/id1/src/TGLExt/TheIdentityHasAName.lean"),
      "sha256": h, "citacoes_do_operador": cit, "citacoes_fora_dos_bytes": ruins}
if ruins:
    print("RECUSA: citacao fora dos bytes", ruins); sys.exit(3)
json.dump(fz, open(alvo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(fz, ensure_ascii=False, indent=1))
