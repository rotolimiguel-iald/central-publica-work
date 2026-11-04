# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_fix2_v407.py -- (a) restaura CRLF no harness_fechar_sandbox_v407.py (uma edicao pelo Edit o tinha normalizado para LF; o molde e' CRLF) e (b) no sandbox, o BUNDLE_v406.json da COPIA da pasta v406 passa a apontar para o MANIFEST da integracao DENTRO do sandbox
(o delta_v406 da copia confere por assert que origem_integracao == o MANIFEST relativo a propria pasta; o delta_v407 so' herda). Uso: python -B -X utf8 _adapt_harness_fechar_fix2_v407.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "harness_fechar_sandbox_v407.py"
t, crlf, raw = M.le(NOME)
BLOCO = r'''# v407 (desvio do molde, dito): o BUNDLE_v406.json da COPIA da pasta v406 no sandbox tem de apontar para o MANIFEST da integracao DENTRO do sandbox (o delta_v406 da copia confere por assert que origem_integracao == o MANIFEST relativo a sua propria pasta); so' esse campo e' reescrito
_b6p = os.path.join(SB, "work", "cadeia_de_selo", "v406", "BUNDLE_v406.json"); _b6 = rdj(_b6p); _b6["origem_integracao"] = _man_sb.replace(os.sep, "/")
open(_b6p, "w", encoding="utf-8").write(json.dumps(_b6, ensure_ascii=False, indent=1))
'''
ALVO = 'shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))\n'
if "_b6p = " not in t:
    t = M.sub(t, ALVO, BLOCO + ALVO)
if crlf and not (b"\r\n" in raw):
    pass
M.grava(NOME, t, True, raw)   # sempre CRLF (o molde e' CRLF)
