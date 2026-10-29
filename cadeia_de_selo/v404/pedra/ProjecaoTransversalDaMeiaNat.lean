import TGLExt.Posto
import TGLExt.ObserverInside
import TGLExt.AngularSelectorIntertwining
import TGLExt.ConjugateAct

set_option autoImplicit false

/-!
# A PROJEÇÃO TRANSVERSAL DA MEIA-NAT — o ângulo agudo do neutrino deixa de ser postulado
[pedra candidata; nome PROVISÓRIO da gerência c1, 28/10/2026 — o nome é do operador]

## A cunhagem do operador (28/10/2026; verbatim em
`work\projecao_transversal_28out\OPERADOR_28out_materia_projecao_transversal_derivada_verbatim.txt`, sha256 no recibo)

> «Matéria não é proporcional ao raio de betatgl, foi isso que erramos, a matéria é a projeção do eixo
> transversal, e por isso meu ângulo agudo para o neutrino faz sentido, então a matéria não é proporcional,
> ela seria a derivada.»

## A ordem (28/10/2026; verbatim em `OPERADOR_28out_ordem_prova_do_neutrino_verbatim.txt`)

> «veja se consegue fazer a prova do neutrino para derivarmos e não ser mais postulado»

## O que esta pedra prova (só álgebra sobre termos que o kernel já tem; nada do dado)

A fórmula do neutrino no programa é `m₂ = β · sen 45° · E₀` (um.py, `neutrino_mass`: «sin(45deg) é POSTULADO
[POSTULATE, ordem do operador 20/08/2026], NÃO derivado»). Aqui o fator `sen 45°` é DERIVADO:

* **a Meia-Nat é o ângulo de 45°**: a fronteira autoconjugada dá `x = 1 − x ⟹ x = ½`
  (`observer_inverse_projection_halfnat`; `halfnat_from_J_symmetry`: cada face pesa ½), e a amplitude
  transversal de um peso ½ é `√½ = sen(π/4)` (`half_amplitude_sq`, `half_amplitude_eq_halfRoot`,
  `forty_five_unique`: em `[0, π/2]` só o ângulo `π/4` tem `sen² = ½`);
* **a forma do neutrino é (peso da reflexão da fronteira) × (projeção transversal da Meia-Nat) × (o corpo)**:
  `β = sen²θ_M` é o Teorema S-∂ (`Posto.sin_sq_thetaMiguel`), logo
  `β · sen 45° · E₀ = sen²θ_M · sen(π/4) · E₀` (`neutrino_mass_form_eq`);
* **o ângulo agudo do neutrino NÃO é θ_M**: `θ_M ≠ π/4` sempre que `β ≠ ½` (`theta_miguel_ne_pi_div_four`);
* **«não proporcional, derivada»**: a derivada do peso transversal `sen²θ` é `sen 2θ` e vale exatamente `1`
  em `π/4` (`transverse_weight_hasDerivAt_half`): o ponto autoconjugado é onde a sombra muda mais depressa.

## O que esta pedra NÃO prova (dito antes)

Não deriva `E₀` (a escala «1 eV» do programa continua DECLARADA); não deriva β (β = α√e é a regra, do axioma);
não afirma que a massa do neutrino É a projeção transversal do estado inscrito — essa identificação é
[ONTO], leitura do operador ratificada em 28/10/2026 e nomeada como hipótese; não abre dado; não move o gate.
Estatuto do que se prova: [KERNEL]; da leitura: [ONTO]; da escala: [INPUT].
-/

namespace TGLExt.ProjecaoTransversalDaMeiaNat

/-- Dois reais não negativos com o mesmo quadrado são iguais (lema auxiliar). -/
theorem eq_of_sq_eq_of_nonneg {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (h : a ^ 2 = b ^ 2) : a = b := by
  nlinarith [sq_nonneg (a - b), sq_nonneg (a + b), mul_nonneg ha hb]

/-- A amplitude transversal da Meia-Nat: `sen(π/4)`. -/
noncomputable def halfAmplitude : ℝ := Real.sin (Real.pi / 4)

/-- [★] `x = 1 − x ⟹ x = ½`: a fronteira autoconjugada pesa meio a meio (a mesma conta de
`observer_inverse_projection_halfnat`, aqui na forma do ponto fixo). -/
theorem half_from_self_conjugate (x : ℝ) (h : x = 1 - x) : x = 1 / 2 := by
  linarith

/-- A Meia-Nat pela J-simetria dá o mesmo ½ (ponte à pedra `ConjugateAct`). -/
theorem half_from_J_symmetry {n : ℕ}
    (w : (((Fin n → ℝ) × (Fin n → ℝ)) → ((Fin n → ℝ) × (Fin n → ℝ))) → ℝ)
    (hJ : w (fun p => conjJ (faceIn (conjJ p))) = w faceIn)
    (hsum : w faceIn + w faceOut = 1) :
    w faceIn = 1 / 2 :=
  halfnat_from_J_symmetry w hJ hsum

theorem half_amplitude_nonneg : 0 ≤ halfAmplitude := by
  unfold halfAmplitude
  apply Real.sin_nonneg_of_nonneg_of_le_pi
  · positivity
  · linarith [Real.pi_pos]

/-- [★] `sen²(π/4) = ½`: a Meia-Nat É o ângulo de 45°. -/
theorem half_amplitude_sq : halfAmplitude ^ 2 = 1 / 2 := by
  unfold halfAmplitude
  rw [Real.sin_pi_div_four, div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  norm_num

/-- A amplitude transversal é a raiz da metade (o `halfRoot` da bancada angular). -/
theorem half_amplitude_eq_halfRoot : halfAmplitude = ChatgptAudit.AngularSelector.halfRoot := by
  apply eq_of_sq_eq_of_nonneg half_amplitude_nonneg (Real.sqrt_nonneg _)
  rw [half_amplitude_sq]
  -- o `apply` já expôs `halfRoot` como `√(1/2)`: o alvo é `1/2 = √(1/2) ^ 2`
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 1 / 2)]

/-- [★] A amplitude transversal de um peso ½ é `sen(π/4)`: de `x = 1 − x` ao ângulo agudo. -/
theorem transverse_amplitude_of_self_conjugate (x : ℝ) (h : x = 1 - x) :
    Real.sqrt x = halfAmplitude := by
  rw [half_from_self_conjugate x h, half_amplitude_eq_halfRoot]
  rfl

/-- [★] Unicidade: em `[0, π/2]`, só `π/4` tem `sen² = ½`. -/
theorem forty_five_unique (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi / 2)
    (h : Real.sin θ ^ 2 = 1 / 2) : θ = Real.pi / 4 := by
  have hs : Real.sin θ = Real.sin (Real.pi / 4) := by
    apply eq_of_sq_eq_of_nonneg
    · exact Real.sin_nonneg_of_nonneg_of_le_pi h0 (by linarith [Real.pi_pos])
    · exact half_amplitude_nonneg
    · rw [h]
      exact half_amplitude_sq.symm
  exact Real.injOn_sin ⟨by linarith [Real.pi_pos], h1⟩
    ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩ hs

/-- A forma da massa do neutrino no programa: `β · sen 45° · E₀` (E₀ é o corpo, [INPUT]). -/
noncomputable def neutrinoMassForm (c : TGLCoupling) (E0 : ℝ) : ℝ :=
  c.beta * halfAmplitude * E0

/-- [★★] A forma do neutrino É (peso da reflexão da fronteira, `sen²θ_M = β`, Teorema S-∂)
× (projeção transversal da Meia-Nat, `sen(π/4)`) × (o corpo `E₀`). -/
theorem neutrino_mass_form_eq (c : TGLCoupling) (E0 : ℝ) :
    neutrinoMassForm c E0 = Real.sin (thetaMiguel c.beta) ^ 2 * Real.sin (Real.pi / 4) * E0 := by
  unfold neutrinoMassForm halfAmplitude
  rw [Posto.sin_sq_thetaMiguel]

/-- O ângulo agudo do neutrino NÃO é o ângulo de Miguel: `θ_M ≠ π/4` sempre que `β ≠ ½`. -/
theorem theta_miguel_ne_pi_div_four (c : TGLCoupling) (h : c.beta ≠ 1 / 2) :
    thetaMiguel c.beta ≠ Real.pi / 4 := by
  intro heq
  have h1 := Posto.sin_sq_thetaMiguel c
  have h2 := half_amplitude_sq
  unfold halfAmplitude at h2
  rw [heq] at h1
  exact h (by linarith)

/-- [DERIVED, álgebra] «não proporcional, derivada»: a derivada do peso transversal `sen²θ` em `π/4`
vale exatamente `1` (`sen 2θ` em `θ = π/4`): o ponto autoconjugado é onde a sombra muda mais depressa. -/
theorem transverse_weight_hasDerivAt_half :
    HasDerivAt (fun θ : ℝ => Real.sin θ ^ 2) 1 (Real.pi / 4) := by
  have h := (Real.hasDerivAt_sin (Real.pi / 4)).pow 2
  have hs : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  have hq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  refine h.congr_deriv ?_
  rw [Real.sin_pi_div_four, Real.cos_pi_div_four]
  norm_num
  nlinarith [hs, hq]

end TGLExt.ProjecaoTransversalDaMeiaNat

#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.half_from_self_conjugate
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.half_from_J_symmetry
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.half_amplitude_sq
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.half_amplitude_eq_halfRoot
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.transverse_amplitude_of_self_conjugate
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.forty_five_unique
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.neutrino_mass_form_eq
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.theta_miguel_ne_pi_div_four
#print axioms TGLExt.ProjecaoTransversalDaMeiaNat.transverse_weight_hasDerivAt_half
