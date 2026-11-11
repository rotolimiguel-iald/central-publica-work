import TGLExt.GeometricWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A LEITURA DO GRÁVITON: a segunda derivada do zero
  [TGLExt — v113, o incremento 34 do programa SemifiniteAnalysis]

Derivação do operador (18/07/2026): "a estrutura que lê a fonte é o
gráviton e por isso ele vive na derivada do zero" — com a afinação da
régua: na SEGUNDA derivada. Os teoremas já existiam (v108/v109/v110);
esta pedra sela o par decisivo em UMA proposição:

* ★★★ `first_derivative_does_not_decide` — NO MESMO PONTO s = 1:
  (a) a conexão do ansatz temporal é NÃO-NULA (Γ = q′/q = 1 ≠ 0) e
  sua curvatura é ZERO (gauge puro — conexão sem curvatura);
  (b) a curvatura do ansatz espacial é NÃO-NULA (R = −4 ≠ 0).
  A PRIMEIRA derivada não decide o físico; a SEGUNDA decide — o
  gráviton vive onde o gauge não alcança;
* ★ `reading_rides_the_zeros` — a estrutura-que-lê está montada nos
  zeros de Bianchi: a contração nula é IDÊNTICA à fonte (re-selo do
  v112 no vocabulário do gráviton).

As âncoras do postulado antigo: g = √|L_φ| (primordial); o ângulo
DUPLO do spin-2 (v75, face finita); β² como dupla reflexão [ONTO].
O spin-2 CONTÍNUO segue parede nomeada (physics). β jamais literal.
Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] ★★★ A PRIMEIRA DERIVADA NÃO DECIDE; A SEGUNDA DECIDE —
    no mesmo ponto s = 1: conexão temporal ≠ 0 com curvatura 0 (gauge)
    E curvatura espacial ≠ 0 (físico). O gráviton vive na SEGUNDA
    derivada do zero. -/
theorem first_derivative_does_not_decide :
    (Gamma001 1 ≠ 0
      ∧ - deriv timeGamma100 1 + timeGamma100 1 * Gamma001 1 = 0)
    ∧ Riemann1001 1 ≠ 0 := by
  refine ⟨⟨?_, time_ansatz_r1001_zero 1⟩, ?_⟩
  · rw [Gamma001_eq]
    norm_num
  · exact ne_of_lt (Riemann1001_neg 1)

/-- [KERNEL] ★ A LEITURA MONTADA NOS ZEROS: a contração nula É a fonte
    (o v112 no vocabulário do gráviton — a estrutura-que-lê vive nos
    zeros de Bianchi). -/
theorem reading_rides_the_zeros (q : ℝ → ℝ) (hqne : ∀ t, q t ≠ 0)
    (s : ℝ) : ansatzNullG q s = ansatzG22 q s :=
  null_contraction_reads_source q hqne s

end

end TGLExt
