# -*- coding: utf-8 -*-
"""Gera sandbox/AuditTiposR2.lean: para cada declaracao MANTIDA ou RENOMEADA (TABELA_DECLARACOES_R2.json), dois
`example : type_of% @R1.X := @R2.Y` (os dois sentidos: tipo identico ao da R1, como a V-GERAL-2 da R1); para os quatro
REFORCOS (E5.09, E5.11, E5.12) o tipo R1 e habitado pelo termo R2 (a R2 implica a R1); e `#check` de cada par para a
comparacao textual. Importa o .olean da R1 (3_KERNEL/sandbox, SO DE LEITURA, via TEMPO_LEAN_PATH_EXTRA) e o da R2
(sandbox). Nada e alterado fora de 5_R2/1_PEDRA.
Uso: python -I -X utf8 gerar_audit_tipos_r2.py <TABELA_DECLARACOES_R2.json> <saida.lean>
"""
import json
import os
import sys

R1 = "TGLExt.TheTimeHasNoRank."
R2 = "TGLExt.TheTimeIsNotAPost."
REFORCO_PROVAS = {
    "purityR_modular":
        "example : type_of% @{R1}purityR_modular :=\n"
        "  fun {{n}} _ _ d _hd t x => @{R2}purityR_modular n _ _ d t x\n",
    "clock_reads_modulo_period":
        "example : type_of% @{R1}clock_reads_modulo_period :=\n"
        "  fun {{κ}} _hκ t => {R2}clock_reads_modulo_period κ t\n",
    "the_two_regimes_of_time":
        "example : type_of% @{R1}the_two_regimes_of_time := by\n"
        "  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := {R2}the_two_regimes_of_time\n"
        "  exact ⟨h1, h2, h3, h4, h5, h6, h7, fun {{κ}} _hκ t => h8 κ t, h9⟩\n",
    "probe_bounded_spectral_translation":
        "example : type_of% @{R1}probe_bounded_spectral_translation := trivial\n"
        "example : type_of% @{R2}probe_bounded_spectral_translation := {R2}probe_bounded_spectral_translation\n",
}


def main(tabela_json, saida):
    tab = json.load(open(tabela_json, encoding="utf-8"))["tabela"]
    linhas = ["import TheTimeHasNoRank", "import TheTimeIsNotAPost", "",
              "/-! Auditoria de TIPOS da pedra R2 contra a pedra R1 (F1.TEMPO, construtor da pedra corrigida).",
              "    `example : type_of% @R1.X := @R2.Y` nos dois sentidos = tipo idêntico (defeq). Para os reforços,",
              "    o tipo da R1 é habitado pelo termo da R2 (a R2 implica a R1). `#check` de cada par para a comparação",
              "    textual por script. Nenhum `sorry`. -/", "", "set_option autoImplicit false", "",
              "noncomputable section", "section Frobenius", "open scoped Matrix.Norms.Frobenius Matrix.Norms.L2Operator", ""]
    pares = []
    for e in tab:
        if e["classe"] in ("mantida", "renomeada"):
            pares.append((e["R1"], e["R2"], e["classe"]))
    n_ex = 0
    for a, b, cl in sorted(pares):
        linhas.append("-- %s: %s -> %s" % (cl, a, b))
        linhas.append("example : type_of%% @%s%s := @%s%s" % (R1, a, R2, b))
        linhas.append("example : type_of%% @%s%s := @%s%s" % (R2, b, R1, a))
        linhas.append("#check @%s%s" % (R1, a))
        linhas.append("#check @%s%s" % (R2, b))
        linhas.append("")
        n_ex += 2
    linhas.append("-- reforços (E5.09, E5.11, E5.12): a R2 implica a R1")
    for nome, prova in REFORCO_PROVAS.items():
        linhas.append(prova.format(R1=R1, R2=R2))
        linhas.append("#check @%s%s" % (R1, nome))
        linhas.append("#check @%s%s" % (R2, nome))
        linhas.append("")
    linhas.append("end Frobenius")
    linhas.append("end")
    txt = "\n".join(linhas) + "\n"
    with open(saida + ".tmp", "wb") as f:
        f.write(txt.encode("utf-8"))
    os.replace(saida + ".tmp", saida)
    print("pares mantida/renomeada:", len(pares), "| examples type_of%:", n_ex, "| reforcos:", len(REFORCO_PROVAS))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
