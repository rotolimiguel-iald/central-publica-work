# -*- coding: utf-8 -*-
"""registros_v400.py -- os DADOS dos registros que a v400 herda da v399, sem acrescentar nenhum: a v400 e' uma versao de CORRECAO (nenhum registro por spec novo, nenhuma inscricao nova, nenhuma fonte nova).
Reexporta o registros_v399 (fontes pinadas, as quatro inscricoes de 24/10 e a declaracao, DECL_SHA256, S_DECL, SHA16, TEXTOS...), importado POR CAMINHO da pasta da v399 (que fica intocada); o sys.path e' restaurado depois do import.
Os scripts da cadeia v400 que conferem a declaracao, as citacoes e as cunhagens leem daqui o que a v399 selou; nada e' digitado de memoria."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V399 = os.path.join(os.path.dirname(HERE), "v399")
_save = list(sys.path)
sys.path.insert(0, V399)            # o registros_v399 importa o delta_v399 por nome
try:
    _spec = importlib.util.spec_from_file_location("registros_v399", os.path.join(V399, "registros_v399.py"))
    R9 = importlib.util.module_from_spec(_spec)
    sys.modules["registros_v399"] = R9
    _spec.loader.exec_module(R9)
finally:
    sys.path[:] = _save
globals().update({k: v for k, v in vars(R9).items() if not k.startswith("__")})
