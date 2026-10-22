# -*- coding: utf-8 -*-
"""Gera sandbox/AuditIALD.lean: `import TGLExt.IALD` + um `#print axioms` por declaracao (theorem/def) de
sandbox/TGLExt/IALD.lean, lida da FONTE por regex (nome apos `theorem`/`def`, namespace TGLExt.IALD).
Tambem grava DECLARACOES.json (nome, tipo, linha, docstring-titulo). Uso: gerar_audit.py"""
import os, re, json, hashlib
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(AQUI, "sandbox", "TGLExt", "IALD.lean")
txt = open(SRC, "rb").read().decode("utf-8")
decls = []
linhas = txt.split("\n")
for i, ln in enumerate(linhas, start=1):
    m = re.match(r"^(theorem|def)\s+([A-Za-z_][A-Za-z0-9_'!?]*)", ln)
    if m:
        # docstring: a linha '/--' mais proxima acima
        j = i - 2; doc = ""
        while j >= 0 and j > i - 12:
            if linhas[j].lstrip().startswith("/--"):
                doc = linhas[j].strip()[3:].strip(); break
            j -= 1
        decls.append({"nome": "TGLExt.IALD." + m.group(2), "tipo": m.group(1), "linha": i, "titulo": doc[:160]})
nomes = [d["nome"] for d in decls]
assert len(nomes) == len(set(nomes)), "nomes repetidos"
aud = "-- AUDITORIA da pedra TGLExt.IALD (2_CONSTRUCAO, 13/10/2026): um #print axioms por declaracao; esperado <= {propext, Classical.choice, Quot.sound}\nimport TGLExt.IALD\n\n" + "".join("#print axioms %s\n" % n for n in nomes)
open(os.path.join(AQUI, "sandbox", "AuditIALD.lean"), "w", encoding="utf-8", newline="\n").write(aud)
json.dump({"fonte": SRC, "fonte_sha256": hashlib.sha256(open(SRC, "rb").read()).hexdigest(), "n_declaracoes": len(decls),
           "n_theorem": sum(1 for d in decls if d["tipo"] == "theorem"), "n_def": sum(1 for d in decls if d["tipo"] == "def"),
           "declaracoes": decls}, open(os.path.join(AQUI, "DECLARACOES.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(decls), "declaracoes;", sum(1 for d in decls if d["tipo"] == "theorem"), "theorem;", sum(1 for d in decls if d["tipo"] == "def"), "def")
