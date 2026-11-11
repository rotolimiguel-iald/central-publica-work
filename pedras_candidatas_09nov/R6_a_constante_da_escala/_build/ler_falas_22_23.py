# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — lê as falas 22 e 23 (quinta emenda) por bytes e confere o sha256 dado pela gerência. Só lê."""
import hashlib, re, sys
from pathlib import Path
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
ESP = {
 22: ("OPERADOR_10nov_beta_tgl_e_o_invariante_a_escala_do_par_luz_radicalizada_em_entropia_igual_informacao_igual_nome_verbatim.txt", 361,
      "1cda85b81ce1887f2f1c78f1357f6423890c32c87e14f050694eae4d08cb025e"),
 23: ("OPERADOR_10nov_nao_pode_ser_leitura_minha_refute_o_nome_e_a_singularidade_o_par_do_nome_e_o_verbo_verbatim.txt", 401,
      "81e6566d93d08a679db9b3b96911ea9b19a30d787b6d8b7125e820fb9714b4fa"),
}
for k, (nome, nb, sh) in ESP.items():
    p = CUN / nome
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    print(f"fala {k}: {len(b)} B sha256 {h} | confere bytes: {len(b) == nb} | confere sha: {h == sh} | BOM: {b[:3] == bytes([0xEF,0xBB,0xBF])} | CRLF: {bytes([13,10]) in b}")
    print("   TEXTO:", repr(b.decode("utf-8")))
    print("   NORMALIZADO:", re.sub(r"\s+", " ", b.decode("utf-8")).strip())
# o que mais há de novo na pasta, de 10/11, por ordem de data (para não perder fala)
import os, datetime
novos = sorted(CUN.glob("OPERADOR_10nov_*.txt"), key=lambda q: q.stat().st_mtime)
print("--- OPERADOR_10nov_* (por mtime):", len(novos))
for q in novos[-12:]:
    print("  ", datetime.datetime.fromtimestamp(q.stat().st_mtime).strftime("%H:%M:%S"), q.stat().st_size, "B", q.name)
