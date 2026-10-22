# -*- coding: utf-8 -*-
"""Testes da regra do acervo do Escritório na guarda pública (22/10/2026). Os nomes e números são fictícios."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarda_publica as GP  # noqa: E402

casos = {r"raiz C:\Escritorio\ é PJ separada": False,
         r"memória do escritório: C:\Escritorio\CLAUDE.md e C:\Escritorio\INSTRUCOES.md": False,
         r"a casa Escritório tem raiz C:/Escritorio/": False,
         r"C:\Escritorio\Processos\2026\peticao.pdf": True,
         r'"C:\\Escritorio\\Audiencias\\gravacao.mp4"': True,
         r"Audiências Realizadas\Audiência Realizada Fulano de Tal - 01.02.2026": True,
         r"processo 0001234-56.2026.8.09.0051": True,
         r"PCT/BR2026/050577 e BR102026003428-2": False}
falhas = 0
for t, esp in casos.items():
    r = GP.toca_escritorio(t)
    falhas += r != esp
    print("ok   " if r == esp else "FALHA", esp, repr(t))
print("FALHAS:", falhas)
