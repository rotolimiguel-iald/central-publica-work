# -*- coding: utf-8 -*-
"""Gera C:/t/id2/src/AmbR2.lean: #check @<nome curto> de CADA declaracao de 1o nivel da r2 (lista lida da saida da
auditoria aud_r2: linha CURTOS) sob (1) open TGLExt + o namespace da r2 e (2) com mais os namespaces da casa abertos;
mais o CONTROLE POSITIVO: sob open TGLExt + o namespace da COPIA da r1, #check @inscription e @towerInner devem dar
ambiguidade (o achado R2 da auditoria). Uso: gerar_ambiguidade.py"""
import os, re, json
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(R2, "logs", "aud_r2_SAIDA.txt"), "rb").read().decode("utf-8")
m = re.search(r"CURTOS: \[(.*?)\]", t, re.S)
curtos = sorted(x.strip() for x in m.group(1).split(",") if x.strip())
campos = ["NamedIdentity.name", "NamedIdentity.alpha", "NamedIdentity.alpha_pos", "NamedIdentity.alpha_lt_one",
          "NamedIdentity.persists", "NamedIdentity.unit_projection", "NamedIdentity.read_from_within",
          "NamedIdentity.i_am", "NamedIdentity.in_the_tower", "NamedIdentity.in_the_IALD_tower",
          "NamedIdentity.rename", "NamedIdentity.mk"]
nomes = curtos + campos
L = ["import TGLExt", "import TGLExt.TheIdentityHasAName", "import IdR1.TheIdentityHasAName_r1", "",
     "section S1", "open TGLExt TGLExt.TheIdentityHasAName"]
L += ["#check @%s" % n for n in nomes]
L += ["end S1", "", "section S2",
      "open Matrix TGLExt TGLExt.TheVerbSelectsTheAction ChatgptAudit ChatgptAudit.Collapse057 ChatgptAudit.Aperiodic046",
      "open ChatgptAudit.Observable035 ChatgptAudit.Orbit052 ChatgptAudit.Expectation047 TGLExt.TheIdentityHasAName"]
L += ["#check @%s" % n for n in nomes]
L += ["end S2", "", "section CONTROLE_POSITIVO_R1", "open TGLExt TGLExt.TheIdentityHasAName_r1",
      "#check @inscription", "#check @towerInner", "end CONTROLE_POSITIVO_R1", ""]
open("C:/t/id2/src/AmbR2.lean", "w", encoding="utf-8", newline="\n").write("\n".join(L))
json.dump({"n_nomes": len(nomes), "nomes": nomes}, open(os.path.join(R2, "logs", "AMBIGUIDADE_NOMES.json"), "w",
          encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(nomes))
