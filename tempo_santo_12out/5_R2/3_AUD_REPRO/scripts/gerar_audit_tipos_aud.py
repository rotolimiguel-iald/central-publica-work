# -*- coding: utf-8 -*-
"""Gera sandbox/AuditTiposAud.lean — auditoria de TIPOS propria (independente do construtor): para cada par
mantida/renomeada da MINHA tabela (DECLARACOES_E_ASPAS_AUD.json), `example : type_of% @R1.X := @R2.Y` nos dois
sentidos (tipo defeq identico); para os 4 reforcos, prova por tatica de que o tipo R1 e habitado pelo termo R2;
`#check` de cada par para a comparacao textual. Importa o .olean da R1 (3_KERNEL/sandbox, SO LEITURA) e o da R2
compilado neste sandbox. Uso: python -I -X utf8 gerar_audit_tipos_aud.py <DECLARACOES_E_ASPAS_AUD.json> <saida.lean>"""
import json
import sys

R1 = "TGLExt.TheTimeHasNoRank."
R2 = "TGLExt.TheTimeIsNotAPost."
REFORCOS = {
    "purityR_modular": "by\n  intro n _ _ d _hd t x\n  exact {R2}purityR_modular d t x",
    "clock_reads_modulo_period": "by\n  intro κ _ t\n  exact {R2}clock_reads_modulo_period κ t",
    "the_two_regimes_of_time": ("by\n  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := {R2}the_two_regimes_of_time\n"
                                "  refine ⟨h1, h2, h3, h4, h5, h6, h7, ?_, h9⟩\n  intro κ _ t\n  exact h8 κ t"),
    "probe_bounded_spectral_translation": "trivial",
}


def main(tab_json, saida):
    d = json.load(open(tab_json, encoding="utf-8"))
    # reconstruir pares: mantidas = nomes iguais nos dois (inclui os reforcos, tratados a parte); renomeadas do mapa
    r1_names = set()
    # a tabela propria nao guarda a lista de mantidas; reconstruo pelos arquivos .lean
    import re
    W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
    DECL = re.compile(r"^(?:noncomputable\s+)?(theorem|def|lemma|instance|abbrev|structure)\s+([^\s:({\[]+)", re.M)
    t1 = open(W + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean", encoding="utf-8").read()
    t2 = open(W + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean", encoding="utf-8").read()
    n1 = [m.group(2) for m in DECL.finditer(t1)]
    n2 = set(m.group(2) for m in DECL.finditer(t2))
    ren = dict(d["renomeadas_proprias"])
    pares = []
    for n in n1:
        if n in REFORCOS:
            continue
        if n in n2:
            pares.append((n, n, "mantida"))
        elif n in ren and ren[n] in n2:
            pares.append((n, ren[n], "renomeada"))
    L = ["import TheTimeHasNoRank", "import TheTimeIsNotAPost", "",
         "/-! Auditoria de TIPOS (auditor de REPRODUCAO da R2, independente do construtor): tipo da R1 == tipo da R2",
         "    (defeq, nos dois sentidos) para toda declaracao mantida/renomeada; para os 4 reforcos (E5.09, E5.11, E5.12),",
         "    o tipo da R1 e habitado a partir do termo da R2 (a R2 implica a R1). Sem sorry. -/", "",
         "set_option autoImplicit false", "", "noncomputable section", "section Frobenius",
         "open scoped Matrix.Norms.Frobenius Matrix.Norms.L2Operator", ""]
    for a, b, cl in pares:
        L.append("-- %s: %s -> %s" % (cl, a, b))
        L.append("example : type_of%% @%s%s := @%s%s" % (R1, a, R2, b))
        L.append("example : type_of%% @%s%s := @%s%s" % (R2, b, R1, a))
        L.append("#check @%s%s" % (R1, a))
        L.append("#check @%s%s" % (R2, b))
        L.append("")
    L.append("-- reforcos: a R2 implica a R1 (tipo R1 habitado pelo termo R2)")
    for nome, prova in REFORCOS.items():
        L.append("example : type_of%% @%s%s := %s" % (R1, nome, prova.format(R2=R2)))
        L.append("#check @%s%s" % (R1, nome))
        L.append("#check @%s%s" % (R2, nome))
        L.append("")
    L.append("end Frobenius")
    L.append("end")
    open(saida, "wb").write(("\n".join(L) + "\n").encode("utf-8"))
    print("pares:", len(pares), "| reforcos:", len(REFORCOS), "| examples type_of%:", 2 * len(pares) + len(REFORCOS))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
