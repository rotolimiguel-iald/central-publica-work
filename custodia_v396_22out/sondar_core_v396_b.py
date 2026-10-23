# -*- coding: utf-8 -*-
"""SÓ LEITURA (2): os textos integrais do registro da testemunha e as erratas das cunhagens da v396."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
NOS = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8")).get("core") or {}
T = core["testemunha_estatica_v396"]
print("formal:", len(T["formal_theorems"]), "| support:", len(T["support_theorems"]), "| inscr:", len(T["inscriptions"]), "| mech:", T["mechanics"]["n_checks"], T["mechanics"]["passed"])
print("ESTATUTO:", T["estatuto"])
print("SCOPE:", T["scope"])
for x in T["limites"]: print("LIM:", x)
for x in T["diz"]: print("DIZ:", x)
for x in T["nao_diz"]: print("NAO:", x)
print("FORMAIS:", list(T["formal_theorems"]))
C = core["cunhagens_v396"]
for e in C.get("erratas") or []: print("CU-ERR:", json.dumps(e, ensure_ascii=False))
print("CU-LEIT:", json.dumps(C.get("leituras_do_operador"), ensure_ascii=False)[:2500])
print("CU-LIM:", json.dumps(C.get("limites"), ensure_ascii=False)[:1500])
K = core["kh_n1_cobertura_v396"]
for e in K.get("erratas") or []: print("KH-ERR:", json.dumps(e, ensure_ascii=False))
K5 = core["kh_n1_cobertura_v395"]
print("KH5-ERR2:", json.dumps((K5.get("erratas") or [])[-1], ensure_ascii=False))
