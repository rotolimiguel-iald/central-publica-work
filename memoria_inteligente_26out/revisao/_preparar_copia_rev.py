# -*- coding: utf-8 -*-
"""_preparar_copia_rev.py -- revisão independente de memoria.py (gerência c1, 26/10/2026): monta a MINHA cópia em C:\\t\\mem_rev:
  real_copia\\  = os .md do diretório real da memória (sem .bak_) + fila\\ (sem __pycache__)  -> faz o papel de «REAL» para os testes (só leitura para mim)
  testes_memoria_rev.py (nesta pasta) = cópia do testes_memoria.py com REAL/AQUI/TESTE apontando para C:\\t\\mem_rev (contagem exata das trocas).
O diretório real é SÓ LIDO."""
import os, shutil, hashlib, sys
REAL = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
REV = r"C:\t\mem_rev"
RC = os.path.join(REV, "real_copia")
H = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(REV):
    shutil.rmtree(REV)
os.makedirs(os.path.join(RC, "fila"))
n = 0
for f in os.listdir(REAL):
    p = os.path.join(REAL, f)
    if os.path.isfile(p) and f.endswith(".md") and ".bak_" not in f:
        shutil.copy2(p, os.path.join(RC, f)); n += 1
for raiz, dirs, arqs in os.walk(os.path.join(REAL, "fila")):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    rel = os.path.relpath(raiz, os.path.join(REAL, "fila"))
    dst = os.path.join(RC, "fila", rel) if rel != "." else os.path.join(RC, "fila")
    os.makedirs(dst, exist_ok=True)
    for a in arqs:
        shutil.copy2(os.path.join(raiz, a), os.path.join(dst, a))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
print("md copiados:", n, "| memoria.py", sha(os.path.join(RC, "fila", "memoria.py")), "| testes", sha(os.path.join(RC, "fila", "testes_memoria.py")))
t = open(os.path.join(REAL, "fila", "testes_memoria.py"), encoding="utf-8").read()
def sub(a, b):
    global t
    assert t.count(a) == 1, (a, t.count(a)); t = t.replace(a, b)
sub('AQUI = os.path.dirname(os.path.abspath(__file__))        # …\\memory\\fila  (o REAL)', 'AQUI = r"C:\\t\\mem_rev\\real_copia\\fila"        # REVISAO: a copia faz o papel do real')
sub('REAL = os.path.dirname(AQUI)                             # …\\memory       (o REAL)', 'REAL = r"C:\\t\\mem_rev\\real_copia"                             # REVISAO: nunca o diretorio real')
sub('TESTE = "C:\\\\t\\\\mem_teste"', 'TESTE = "C:\\\\t\\\\mem_rev\\\\mem_teste"')
open(os.path.join(H, "testes_memoria_rev.py"), "w", encoding="utf-8", newline="\n").write(t)
import ast; ast.parse(t)
print("testes_memoria_rev.py escrito; trocas: 3")
