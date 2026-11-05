# -*- coding: utf-8 -*-
"""Parte 2 dos ajustes da v407, depois do 1o teste do escopo medido (TESTE_ESCOPO_v407_r1_falhou.json): no sistema vivo o arquivo
.iald_runtime\\monthly_wallet\\web-runtime.lock (trava de processo, presa pelo web vivo) deu PermissionError e deixava accounts_modified = None.
Trava de processo nao e' dado de usuario: os arquivos *.lock saem da medicao (declarado no metodo). Cada troca exige exatamente uma ocorrencia."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent
p = W / "transaction.py"
t = p.read_bytes().decode("utf-8")
eol = "\r\n" if "\r\n" in t else "\n"
pares = [
    ("SCOPE_SKIP_DIRS = frozenset(('Pods', 'build', 'DerivedData', 'xcuserdata', '.gradle', '__pycache__', 'node_modules', '.git'))\n",
     "SCOPE_SKIP_DIRS = frozenset(('Pods', 'build', 'DerivedData', 'xcuserdata', '.gradle', '__pycache__', 'node_modules', '.git'))\n"
     "SCOPE_SKIP_SUFFIXES = ('.lock',)   # travas de processo (ex.: web-runtime.lock, presa pelo web vivo): nao sao dado de usuario\n"),
    ("        for name in sorted(files):\n            yield Path(top) / name\n",
     "        for name in sorted(files):\n            if name.lower().endswith(SCOPE_SKIP_SUFFIXES):\n                continue\n            yield Path(top) / name\n"),
    ("'method': 'sha256 de cada arquivo (estado e cliente) e pid+create_time de quem escuta as portas, antes e depois da escrita, dentro da janela com o web parado; somente leitura',",
     "'method': 'sha256 de cada arquivo (estado e cliente; travas *.lock excluidas) e pid+create_time de quem escuta as portas, antes e depois da escrita, dentro da janela com o web parado; somente leitura',"),
]
for velho, novo in pares:
    velho, novo = velho.replace("\n", eol), novo.replace("\n", eol)
    assert t.count(velho) == 1, (t.count(velho), velho[:80])
    t = t.replace(velho, novo)
p.write_bytes(t.encode("utf-8"))
print(json.dumps({"ajustados": ["transaction.py"], "trocas": len(pares)}))
