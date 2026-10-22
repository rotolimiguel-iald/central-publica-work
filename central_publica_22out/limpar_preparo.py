# -*- coding: utf-8 -*-
"""Esvazia SÓ uma das três pastas de preparo dos repositórios públicos (criadas nesta sessão pelos construtores), com trava no caminho.
Uso: limpar_preparo.py <central-publica|central-publica-work|central-publica-bancada>"""
import shutil, sys
from pathlib import Path

NOMES = {"central-publica", "central-publica-work", "central-publica-bancada"}
nome = sys.argv[1] if len(sys.argv) > 1 else "central-publica"
assert nome in NOMES, nome
ALVO = Path(r"C:\IALD\Central_publica") / nome
assert str(ALVO.resolve()).lower() == (r"c:\iald\central_publica" + "\\" + nome).lower(), ALVO
if ALVO.exists():
    shutil.rmtree("\\\\?\\" + str(ALVO.resolve()))
print("preparo esvaziado:", nome, not ALVO.exists())
