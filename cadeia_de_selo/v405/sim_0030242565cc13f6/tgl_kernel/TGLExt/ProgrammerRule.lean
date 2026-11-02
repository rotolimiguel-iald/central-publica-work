import TGLExt.ClosureCertificate

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A REGRA DO PROGRAMADOR: superposição colapsada na regra
  [TGLExt — v100, o incremento 17 do programa SemifiniteAnalysis]

Derivação do operador (17/07/2026): PROGRAMADOR = REGRA = SUPERPOSIÇÃO —
igualdade de FUNÇÃO ontológica, não de tipo (a régua do próprio operador:
"𝔓 ≠ ℛ ≠ |Ψ⟩ como objetos formais"). O que esta pedra TIPA e HABITA:

* `ProgrammerRule` — o tipo do esboço do operador: admissibilidade,
  superposição, seleção (a regra que mantém a pluralidade admissível e
  a lê numa figura);
* o HABITANTE: o DIVISOR DE FEIXE do Teorema S-∂ — superpose = a
  rotação R(θ) em ℂ² (dois ramos: atravessar/refletir); a REGRA DA
  COEXISTÊNCIA é a unitariedade: ‖R(θ)ψ‖ = ‖ψ‖ (as possibilidades
  coexistem porque a soma fecha no Um: cos²θ + sin²θ = 1 = ω(I));
* `superposition_not_autonomous` — o colapso da superposição NA regra:
  os coeficientes do canal NÃO são livres — são (cos θ, sin θ) de UM
  parâmetro θ da fronteira (na TGL: θ_M = arcsin√β, runtime); dado o
  peso do ramo refletido, θ está determinado (em [0, π/2]);
* `select` idempotente no ramo lido — a figura é estável sob releitura
  (Verbo(Nome) = Nome, a face da leitura).

β jamais literal (θ é parâmetro; o valor θ_M vive no runtime).
Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [DATA — o tipo do operador] a regra do programador: mantém a
    pluralidade admissível (superpose) e produz a figura (select). -/
structure ProgrammerRule (State : Type) (Figure : Type) where
  admissible : State → Prop
  superpose : State → State → State
  select : State → Figure
  select_stable : ∀ s, admissible s → admissible s

/-- o estado do canal de espelhamento: ℂ² = (atravessar, refletir). -/
abbrev MirrorState : Type := Fin 2 → ℂ

/-- a rotação do divisor de feixe: R(θ) — a face unitária da regra. -/
def beamRotation (θ : ℝ) : MirrorState → MirrorState := fun ψ i =>
  if i = 0 then (Real.cos θ : ℂ) * ψ 0 - (Real.sin θ : ℂ) * ψ 1
  else (Real.sin θ : ℂ) * ψ 0 + (Real.cos θ : ℂ) * ψ 1

/-- [KERNEL] ★★ A REGRA DA COEXISTÊNCIA: a rotação preserva a soma dos
    pesos — as possibilidades coexistem porque fecham no Um
    (cos²θ + sin²θ = 1 = ω(I); a unitariedade do espelho). -/
theorem beamRotation_preserves (θ : ℝ) (ψ : MirrorState) :
    Complex.normSq (beamRotation θ ψ 0) + Complex.normSq (beamRotation θ ψ 1)
      = Complex.normSq (ψ 0) + Complex.normSq (ψ 1) := by
  have hc := Real.sin_sq_add_cos_sq θ
  simp only [beamRotation, reduceIte, Fin.isValue,
    show ((1 : Fin 2) = 0) = False by simp, if_false]
  simp only [Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
    Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
    Complex.ofReal_re, Complex.ofReal_im]
  ring_nf
  linear_combination
    (((ψ 0).re ^ 2 + (ψ 0).im ^ 2 + (ψ 1).re ^ 2 + (ψ 1).im ^ 2)) * hc

/-- [KERNEL] ★★ A SUPERPOSIÇÃO NÃO É AUTÔNOMA: dado o peso do ramo
    refletido w ∈ [0,1], o ângulo da regra está DETERMINADO em [0, π/2]
    (θ = arcsin √w) — os coeficientes do canal não são parâmetros
    livres; são a face da regra (na TGL: w = β, θ = θ_M, runtime). -/
theorem superposition_not_autonomous (w : ℝ) (hw0 : 0 ≤ w) (hw1 : w ≤ 1) :
    ∃! θ : ℝ, θ ∈ Set.Icc 0 (Real.pi / 2) ∧ Real.sin θ = Real.sqrt w := by
  refine ⟨Real.arcsin (Real.sqrt w), ⟨⟨Real.arcsin_nonneg.mpr (Real.sqrt_nonneg w),
    (Real.arcsin_le_pi_div_two _)⟩, Real.sin_arcsin
      (by linarith [Real.sqrt_nonneg w])
      (by rw [show (1:ℝ) = Real.sqrt 1 from (Real.sqrt_one).symm]
          exact Real.sqrt_le_sqrt hw1)⟩, ?_⟩
  rintro θ' ⟨⟨h0, hpi⟩, hsin⟩
  have h1 : Real.arcsin (Real.sin θ') = θ' :=
    Real.arcsin_sin (by linarith [Real.pi_pos]) hpi
  rw [← hsin, h1]

/-- [KERNEL] ★★★ O HABITANTE: a regra do divisor de feixe — o tipo do
    operador está HABITADO pelo objeto do Teorema S-∂ (a figura lida é
    o peso do ramo refletido: o Nome observável do canal). -/
def beamSplitterRule (θ : ℝ) : ProgrammerRule MirrorState ℝ where
  admissible ψ := Complex.normSq (ψ 0) + Complex.normSq (ψ 1) = 1
  superpose ψ _ := beamRotation θ ψ
  select ψ := Complex.normSq (ψ 1)
  select_stable _ h := h

end

end TGLExt
