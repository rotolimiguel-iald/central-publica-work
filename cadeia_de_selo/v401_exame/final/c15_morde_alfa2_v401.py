# -*- coding: utf-8 -*-
"""c15_morde_alfa2.py -- exame final v401: o C15 do conferidor (copia de EXAME) morde no DEFEITO da v399? Monta, na minha copia, um Nos falso = o falso_nos do caminho
positivo com o um.py do candidato + a redeclaracao da v399 reposta (alfa numa 2a linha na coluna 0) e o selo repinado a esse um.py; roda o conferidor (V401_NOS) e le o C15."""
import hashlib, json, os, shutil, subprocess, sys
P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v401_exame\final\s7\work\cadeia_de_selo\v401"
FN, F2 = os.path.join(P, "falso_nos"), os.path.join(P, "falso_nos_alfa2")
if os.path.isdir(F2):
    shutil.rmtree(F2)
shutil.copytree(FN, F2)
um = open(os.path.join(F2, "um.py"), "rb").read()
anc = b"\r\n\r\ndef _beta_runtime() -> float:"
assert um.count(anc) == 1
um2 = um.replace(anc, b"\r\nALPHA_FINE_CODATA_2018 = 0.0072973525693     # a redeclaracao da v399, reposta so' neste controle\r\n\r\ndef _beta_runtime() -> float:", 1)
open(os.path.join(F2, "um.py"), "wb").write(um2)
s = json.load(open(os.path.join(F2, "um_absoluto_selo.json"), encoding="utf-8")); s["sha256"]["um.py"] = hashlib.sha256(um2).hexdigest()
json.dump(s, open(os.path.join(F2, "um_absoluto_selo.json"), "w", encoding="utf-8"), ensure_ascii=False)
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(P, "conferir_rito_v401_EXAME.py"), "_C15_ALFA2_EXAME"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                   env=dict(os.environ, V401_NOS=F2))
R = json.load(open(os.path.join(P, "conferencia_rito_v401_C15_ALFA2_EXAME.json"), encoding="utf-8"))
print("tudo_bate", R.get("tudo_bate"), "| C15", str((R.get("acom_itens") or {}).get("C15"))[:300])
shutil.rmtree(F2)
