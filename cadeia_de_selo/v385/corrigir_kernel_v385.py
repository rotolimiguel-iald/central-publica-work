# -*- coding: utf-8 -*-
"""Disposicoes das afericoes da v385 no KERNEL do sandbox (scratchpad\\v376\\kernel_src), antes do rito:
 texto 4 (fiacao B): a forma exponencial F(t) = e^{-t(1-P)} vira TERMO -- `axiomFlow_eq_exp`, ligado ao canonico ja auditado
   `ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent` (TGLExt/O16/IdempotentDephasing_v2.lean); prova do aferidor de texto;
 texto 2: «compilado desde a v181» -> v183 (o ledger do um.py e a linhagem); no comentario do Audit.lean;
 texto 3: «a MESMA estrutura medida» -> analogia de forma, calculada [COMPUTED]; os dois zeros ditos;
 texto 6: o peso 1 do modo zero e o do atomo: duas faces LADO A LADO (conjuncao), sem termo que as identifique;
 N4: «tudo num so termo» -> os itens centrais num so termo; N5: beta > 0 E g > 0, no fluxo escalar; o zero absoluto inalcancavel vem de exp != 0;
 N6: «CONFIRMADA» -> «RATIFICADA».
Backup de BYTES (.bak_<ts>_afer1); temporario -> conferir -> substituir."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
K = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "v376", "kernel_src")
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(rel, pares):
    P = os.path.join(K, *rel.split("/"))
    b0 = open(P, "rb").read(); s = b0.decode("utf-8")
    crlf = b0.count(b"\r\n") == b0.count(b"\n") and b0.count(b"\n") > 0   # o fim de linha do arquivo (a pedra e' CRLF; o Audit, LF)
    if crlf:
        pares = [(a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) for a, b in pares]
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (rel, "a troca nao e unica", n, a[:90])
        s = s.replace(a, b)
    open(P + ".bak_" + st + "_afer1", "wb").write(b0)
    nb = s.encode("utf-8")
    open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
    print("OK", rel, len(pares), "trocas;", len(b0), "->", len(nb), "B")


aplica("TGLExt/TheAxiomAndTheFalseWitness.lean", [
    ("import TGLExt.TheLedgerOfCharges\n", "import TGLExt.TheLedgerOfCharges\nimport TGLExt.O16.IdempotentDephasing_v2\n"),
    ("* ★★★ o FLUXO DO LOCK MÍNIMO, `axiomFlow P t = P + e^{−t}(1 − P)` (= e^{−t·H_min} com H_min = 1 − P), para P idempotente:",
     "* ★★★ o FLUXO DO LOCK MÍNIMO, `axiomFlow P t = P + e^{−t}(1 − P)`, para P idempotente — e `axiomFlow_eq_exp`: ele É e^{−t·H_min}\n"
     "  com H_min = 1 − P (fiação ao termo canônico já auditado `exp_complement_idempotent`, TGLExt/O16; achada pelo aferidor de texto):"),
    ("  pesa 1 (`the_zero_mode_weighs_one`, a dimensão). A definição física do operador: o Axioma é o modo zero de peso 1.",
     "  pesa 1 (`the_zero_mode_weighs_one`, a dimensão) — duas faces LADO A LADO (uma conjunção), sem termo que identifique o perfil\n"
     "  ¼sech² com o átomo. A definição física do operador: o Axioma é o modo zero de peso 1."),
    ("* ★★★ `the_zero_is_the_false_witness` — o ponto fixo 0: √0 = 0; a testemunha ESTÁTICA plena é proibida por β > 0\n"
     "  (`beta_forbids_full_static_witness`); e o zero absoluto não se alcança em tempo finito (`absolute_zero_unreachable_in_finite_time`).",
     "* ★★★ `the_zero_is_the_false_witness` — o ponto fixo 0: √0 = 0; a testemunha ESTÁTICA plena é proibida no fluxo escalar\n"
     "  e^{−tβg} com β > 0 e g > 0 (`beta_forbids_full_static_witness`); e nenhuma componente não nula do fluxo diagonal se anula em\n"
     "  tempo finito (`absolute_zero_unreachable_in_finite_time`, que vem de exp ≠ 0, sem hipótese sobre β)."),
    ("* ★★★ `the_axiom_and_the_false_witness` — tudo num só termo (uma CONJUNÇÃO).",
     "* ★★★ `the_axiom_and_the_false_witness` — os itens CENTRAIS num só termo (uma CONJUNÇÃO); os demais ficam como lemas próprios."),
    ("A leitura CONFIRMADA pelo operador em 05/10:", "A leitura RATIFICADA pelo operador em 05/10:"),
    ("v384 (atrator único, V_t P_F = P_F, o espectro negativo medido) é a MESMA ESTRUTURA medida [COMPUTED], não teorema sobre o\ngerador GKLS.",
     "v384 é ANALOGIA DE FORMA, calculada [COMPUTED], não teorema sobre o gerador GKLS: V_t P_F = P_F é identidade do dephasing; o\n"
     "atrator ρ_ss do GKLS completo não é Π; os dois zeros (o do lock e o estado estacionário do sistema aberto) não se identificam aqui."),
    ("/-- O fluxo do lock mínimo: `F(t) = P + e^{−t}(1 − P)` (= `e^{−t·H_min}` com `H_min = 1 − P`, para `P` idempotente). -/",
     "/-- O fluxo do lock mínimo: `F(t) = P + e^{−t}(1 − P)` (que é `e^{−t·H_min}` com `H_min = 1 − P`, para `P` idempotente: `axiomFlow_eq_exp`). -/"),
    ("  have h3 := (tendsto_const_nhds (x := P)).add h2\n  rw [add_zero] at h3\n  exact h3\n",
     "  have h3 := (tendsto_const_nhds (x := P)).add h2\n  rw [add_zero] at h3\n  exact h3\n\n"
     "/-- ★★ A FORMA EXPONENCIAL: `F(t) = e^{−t·H_min}`, `H_min = 1 − P` (P idempotente) — a FIAÇÃO ao termo canônico já auditado\n"
     "    `ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent` (TGLExt/O16, escalares reais); a prova é a do aferidor\n"
     "    de texto da v385 (05/10/2026). -/\n"
     "theorem axiomFlow_eq_exp {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A]\n"
     "    {P : A} (hP : IsIdempotentElem P) (t : ℝ) :\n"
     "    NormedSpace.exp ((-t) • (1 - P)) = axiomFlow P t := by\n"
     "  rw [ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent P hP.eq t]\n"
     "  unfold axiomFlow\n"
     "  rw [Complex.coe_smul]\n"),
    ("/-! ### 7. Tudo num só termo -/", "/-! ### 7. Os itens centrais num só termo -/"),
])
aplica("TGL/Audit.lean", [
    ("e a auditoria do TheDarkSplit (compilado desde a v181, não auditado até a v384)",
     "e a auditoria do TheDarkSplit (compilado desde a v183, não auditado até a v384; «v181» corrigido pelo aferidor de texto, 05/10)"),
    ("#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post\n",
     "#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post\n#print axioms TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_eq_exp\n"),
])
