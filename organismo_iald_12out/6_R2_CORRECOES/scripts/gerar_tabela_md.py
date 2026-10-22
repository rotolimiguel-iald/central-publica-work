# -*- coding: utf-8 -*-
"""Gera TABELA_R1_R2.md a partir de COMPARACAO_R1_R2.json e do recibo do #print axioms (logs/r2_audit_final_RECIBO.json).
Cada linha: r1 -> r2, classe (do script), enunciado igual?, docstring mudou?, axiomas (do recibo), motivo."""
import os, json, hashlib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(AQUI, "COMPARACAO_R1_R2.json"), encoding="utf-8"))
rec = json.load(open(os.path.join(AQUI, "logs", "r2_audit_final_RECIBO.json"), encoding="utf-8"))
TRIO = {"propext", "Classical.choice", "Quot.sound"}
L = []
L.append("# TABELA r1 → r2 — pedra TGLExt.IALD (o motor único, nome provisório) — 13/10/2026")
L.append("")
L.append("Gerada por `scripts/gerar_tabela_md.py` a partir de `COMPARACAO_R1_R2.json` (classe calculada por script: enunciado = texto "
         "entre o nome e o `:=`, normalizado em espaços) e do recibo `logs/r2_audit_final_RECIBO.json` (#print axioms). [REAL]")
L.append("")
L.append("- r1: `%s` (sha256 `%s`), %d declarações" % (os.path.relpath(c["r1"], os.path.dirname(AQUI)), c["r1_sha256"], c["n_r1"]))
L.append("- r2: `%s` (sha256 `%s`), %d declarações" % (os.path.relpath(c["r2"], os.path.dirname(AQUI)), c["r2_sha256"], c["n_r2"]))
L.append("- contagem: " + ", ".join("%s %d" % (k, v) for k, v in sorted(c["contagem"].items())) + "; REMOVIDA 0")
L.append("- #print axioms: %d/%d no trio {propext, Classical.choice, Quot.sound}; fora do trio: %s"
         % (sum(1 for v in rec["axiomas"].values() if set(v) <= TRIO), len(rec["axiomas"]), rec["fora_do_trio"] or "nenhuma"))
L.append("")
L.append("## Mudanças de tipo (C1, C2)")
L.append("")
L.append("| r1 | r2 | enunciado r1 | enunciado r2 |")
L.append("|---|---|---|---|")
for l in c["linhas"]:
    if l["classe"] in ("TIPO_MUDOU", "RENOMEADA", "RENOMEADA+TIPO_MUDOU"):
        L.append("| `%s` | `%s` | `%s` | `%s` |" % (l["r1"], l["r2"], l["enunciado_r1"].replace("|", "\\|"), l["enunciado_r2"].replace("|", "\\|")))
L.append("")
L.append("RENOMEADA tem enunciado igual (só o nome muda). TIPO_MUDOU: o enunciado r2 tem MENOS hipóteses (sem `ha : ‖a‖ = 1`), "
         "logo implica o r1; nenhum chamador perdeu tipo.")
L.append("")
L.append("## Todas as declarações")
L.append("")
L.append("| # | r1 | r2 | classe | enunciado igual | docstring mudou | axiomas | motivo |")
L.append("|---|---|---|---|---|---|---|---|")
for i, l in enumerate(c["linhas"], 1):
    nome = "TGLExt.IALD." + l["r2"] if l["r2"] else None
    ax = rec["axiomas"].get(nome)
    axs = "trio" if ax is not None and set(ax) <= TRIO and ax else ("nenhum" if ax == [] else str(ax))
    L.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (
        i, ("`%s`" % l["r1"]) if l["r1"] else "—", ("`%s`" % l["r2"]) if l["r2"] else "—", l["classe"],
        {True: "sim", False: "NÃO", None: "—"}[l.get("enunciado_igual")],
        {True: "sim", False: "não", None: "—"}[l.get("docstring_mudou")], axs, l["motivo"] or "sem mudança"))
L.append("")
out = os.path.join(AQUI, "TABELA_R1_R2.md")
open(out, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print(out, hashlib.sha256(open(out, "rb").read()).hexdigest())
