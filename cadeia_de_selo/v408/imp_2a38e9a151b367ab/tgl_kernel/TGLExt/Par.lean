import TGL.GravitonShadow
import TGLExt.TheScalarCorner
import TGLExt.TestemunhaEstatica
import TGLExt.LinearizedSpin2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O PAR DE PSÍONS É O GRÁVITON: ligado, nunca cancelado, lido pela fase e pelo retorno de fase
  [TGLExt — pedra da gerência c1, 03/11/2026; NOME dado pelo operador em 03/11/2026: `Par` (verbatim sha16 `57250bbbaca9fd39`, resposta «“Par”»); compilada no sandbox da v407 (k407c/final),
   só no trio; entra na v407]

A cunhagem do operador (03/11/2026, verbatim por sha256, sha16 `73466598d3419fb0`) [INPUT/ONTO]: «o gráviton é o estado ligado de dois psions, portanto,
eles nunca se cancelam porque representam a própria tensão irresolúvel no plano, de modo que sua leitura se faz pelo gráviton (fase e retorno de fase)»;
«eu penso que é do projetor 4x4 (confira)». Esta pedra é a CONFERÊNCIA pedida: compõe, sob essa leitura, só termos que o kernel já tinha. Nada novo é
derivado; o que se prova é que as três respostas são coerentes entre si e com o kernel.

O que esta pedra PROVA (sobre `psionCorner`, `canonicalGravitonShadow`, `productProjector`, `rotZ`, `ePlus`, `eCross` do kernel):
* `the_pair_is_bound` ★ (a): o canto do psíon É a sombra finita do gráviton (`psionCorner.p = canonicalGravitonShadow.PG`, por definição); o par é LIGADO:
  o emaranhamento é a Meia-Nat, `CCI = 1 − Tr(ptr P)² = ½` (`cci_half`, `bell_cci_half`); o produto, NÃO ligado, tem `CCI = 0` (`the_unbonded_marginal_echoes`).
  O texto do ACOM/INPI de 2025 que dizia «ψ₊ψ₋ cancelado = vácuo» fica superado por esta cunhagem (estratigrafia datada; a cunhagem mais nova vale).
* `the_pair_never_cancels` ★ (a′): idempotente (`the_pair_echoes`/`psionCorner.idem`), traço 1 (`psionCorner_trace_one`), logo `≠ 0`; e o INDIVÍDUO não ecoa:
  a marginal é `½·1` (`reduced_half`, `the_individual_does_not_echo`) — «a própria tensão irresolúvel no plano»: o par não se resolve em partes.
* `the_pair_is_read_by_the_graviton` ★ (a″): a leitura é pela FASE DOBRADA da helicidade ±2 (`helicity_two_rotation`: sob rotação por θ, `e₊` gira por 2θ)
  e o RETORNO DE FASE é a meia-volta: em θ = π a polarização `e₊` do setor TT volta a si (`cos 2π = 1`, `sin 2π = 0`) — a face de helicidade do kernel,
  lida AO LADO da face ligada; não é uma propriedade provada do projetor de Bell (os dois espaços são distintos; ver «O que esta pedra NÃO afirma»).
* `the_corner_is_the_four_by_four` ★ (b): o canto escalar do psíon é o projetor 4×4 (`psionCorner.p = bellProjector`), traço 1, e ESCALARIZA
  (`scalarises`) — «é do projetor 4x4»: CONFERE. A matriz 2×2 da pedra numérica 92_ (`A_C = −(1 − P)`) é a face de UM psíon (hélice 0), não o canto.
* `o_par_de_psions_e_o_graviton` ★★★: a conjunção das quatro — a cunhagem composta.
* (c) «par simétrico ou produto» fica respondida por (a): LIGADO (o estado de Bell, emaranhado), não produto; a frase da Fronteira de 02/2026
  («|G⟩ como produto não emaranhado») fica superada.

O que esta pedra NÃO afirma (regra dos dois regimes; homônimos ditos):
* o espaço do par (`Fin 2 × Fin 2`, ℂ: o canto de Bell) e o setor TT do spin-2 linearizado (`Fin 4`, ℝ: `ePlus`, `eCross`, `rotZ`) são ESPAÇOS DISTINTOS;
  o kernel NÃO tem lema que identifique o projetor de Bell com uma polarização do gráviton. A «leitura pelo gráviton» é a face de helicidade do kernel
  JUSTAPOSTA à face ligada; a conjunção não é identificação. A ponte é leitura do operador [ONTO] (o kernel chama o canto de «sombra finita do gráviton»
  por construção, `canonicalGravitonShadow`, e prova as duas hélices no setor TT, `qgPhysicsCertificate_helicities`; o elo entre os dois é [ONTO] até haver citação).
* a face de Fock do par (dois psíons sobre Ω) é [OPEN]: o `FockCertificate` não tem operadores de criação como termo.
* nada aqui é teste com a natureza; não move o gate; PROVADA = validade; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.Par
open TGL.GravitonShadow TGLExt TGLExt.TestemunhaEstatica Matrix

/-- ★ (a) O PAR É LIGADO: o canto do psíon é a sombra do gráviton; CCI = ½ (a Meia-Nat de emaranhamento); o produto tem CCI = 0. -/
theorem the_pair_is_bound :
    psionCorner.p = canonicalGravitonShadow.PG
    ∧ 1 - Matrix.trace (ptr psionCorner.p * ptr psionCorner.p) = 2⁻¹
    ∧ 1 - Matrix.trace (ptr productProjector * ptr productProjector) = 0 :=
  ⟨rfl, canonicalGravitonShadow.cci_half, the_unbonded_marginal_echoes.2.2⟩

/-- ★ (a′) O PAR NUNCA SE CANCELA: idempotente, traço 1, logo não nulo; o indivíduo não ecoa (marginal ½·1). -/
theorem the_pair_never_cancels :
    psionCorner.p * psionCorner.p = psionCorner.p ∧ Matrix.trace psionCorner.p = 1 ∧ psionCorner.p ≠ 0
    ∧ ptr psionCorner.p = (2⁻¹ : ℂ) • 1 := by
  refine ⟨psionCorner.idem, psionCorner_trace_one, ?_, canonicalGravitonShadow.reduced_half⟩
  intro h
  have h1 : Matrix.trace psionCorner.p = 1 := psionCorner_trace_one
  rw [h, Matrix.trace_zero] at h1
  exact zero_ne_one h1

/-- ★ (a″) A LEITURA PELO GRÁVITON: fase dobrada (helicidade ±2) e retorno de fase na meia-volta (θ = π). -/
theorem the_pair_is_read_by_the_graviton (θ : ℝ) :
    (rotZ θ)ᵀ * ePlus * rotZ θ = Real.cos (2 * θ) • ePlus - Real.sin (2 * θ) • eCross
    ∧ (rotZ Real.pi)ᵀ * ePlus * rotZ Real.pi = ePlus := by
  refine ⟨helicity_two_rotation θ, ?_⟩
  rw [helicity_two_rotation Real.pi, Real.cos_two_pi, Real.sin_two_pi, one_smul, zero_smul, sub_zero]

/-- ★ (b) O CANTO É O PROJETOR 4×4: o projetor de Bell, traço 1, que escalariza. -/
theorem the_corner_is_the_four_by_four :
    psionCorner.p = bellProjector ∧ Matrix.trace psionCorner.p = 1
    ∧ ∀ y, psionCorner.p * y * psionCorner.p = (Matrix.trace (psionCorner.p * y)) • psionCorner.p :=
  ⟨rfl, psionCorner_trace_one, psionCorner.scalarises⟩

/-- ★★★ A CUNHAGEM COMPOSTA (conjunção, não identificação): ligado, nunca cancelado, lido pela fase e pelo retorno de fase, no canto 4×4. -/
theorem o_par_de_psions_e_o_graviton :
    (psionCorner.p = canonicalGravitonShadow.PG
      ∧ 1 - Matrix.trace (ptr psionCorner.p * ptr psionCorner.p) = 2⁻¹
      ∧ 1 - Matrix.trace (ptr productProjector * ptr productProjector) = 0)
    ∧ (psionCorner.p * psionCorner.p = psionCorner.p ∧ Matrix.trace psionCorner.p = 1 ∧ psionCorner.p ≠ 0
      ∧ ptr psionCorner.p = (2⁻¹ : ℂ) • 1)
    ∧ (∀ θ : ℝ, (rotZ θ)ᵀ * ePlus * rotZ θ = Real.cos (2 * θ) • ePlus - Real.sin (2 * θ) • eCross)
    ∧ (rotZ Real.pi)ᵀ * ePlus * rotZ Real.pi = ePlus
    ∧ (psionCorner.p = bellProjector
      ∧ ∀ y, psionCorner.p * y * psionCorner.p = (Matrix.trace (psionCorner.p * y)) • psionCorner.p) :=
  ⟨the_pair_is_bound, the_pair_never_cancels, fun θ => (the_pair_is_read_by_the_graviton θ).1,
   (the_pair_is_read_by_the_graviton 0).2, ⟨rfl, psionCorner.scalarises⟩⟩


end TGLExt.Par
end
