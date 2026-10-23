# -*- coding: utf-8 -*-
"""Qualifica o fornecedor REAL do fundo BG1 (E1/E2). NAO le nenhum centro local de H0: so Planck comprimido + DESI DR2 (o mesmo R2 do V1).
Grava testes/QUALIFICACAO_FORNECEDOR_REAL.json."""
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "runner"))
import f9v2_background as B  # noqa: E402

t0 = time.time()
P = B.BancadaBackgroundProvider()
t1 = time.time()
bg = P.compute()
t2 = time.time()
chk = B.check_reproduction(bg, 68.531, 0.301)
out = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "init_s": t1 - t0, "fit_s": t2 - t1, "reproducao_E2": chk, "fundo": bg,
       "bancada_pins": B.bancada_pins(),
       "nota": "nenhum centro local de H0 entrou; so Planck comprimido + DESI DR2 (fundo). Mesmo R2 do runner V1."}
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
open(os.path.join(HERE, "QUALIFICACAO_FORNECEDOR_REAL.json"), "wb").write(b)
print(json.dumps({k: out[k] for k in ("init_s", "fit_s", "reproducao_E2")}, indent=1))
print("BG1:", bg["bg1"]["H0"], bg["bg1"]["sigma_H0"], bg["bg1"]["theta_H0_ombh2_omch2"])
print("free:", bg["fundo_livre"])
print("sha", hashlib.sha256(b).hexdigest()[:16])
