import Mathlib
import TGL.TransportData

set_option autoImplicit false

/-!
# O Índice do Nome   [KERNEL]   (v27 -- rodada 3 do especialista, auditada)

Tipagem final da intuicao do operador ("o indice do Nome = espelho; o contorno e'
o indice e a paridade inversa o referencial"), corrigida pelo especialista:
**o espelho nao e' numericamente o indice; o indice do Nome e' LIDO no espelho.**
  e_Nome = projecao de Jones = espelho ; N_3L ⊂ C_W = contorno ;
  Ind(E_3L) = resistencia do contorno ; J_ref = referencial ;
  U_Π = J·J_ref = paridade inversa LINEARIZADA (produto de duas antiunitarias).

DUAS CORRECOES FISCAIS ENCODADAS:
(1) [REFUTED] a rota Haar/pontos-fixos NAO da' csc²θ universalmente (acao de grupo
    finito ⟹ indice = ordem do grupo). A rota valida e' Pimsner-Popa: a constante
    otima λ(E) e' o INVERSO do indice [KNOWN, Pimsner-Popa 1986; Kosaki 1986];
    `λ(E_3L) = sin²θ` e' o ALVO MODELO-ESPECIFICO, nao um fato de Haar.
(2) `index · sin²θ = 1` NAO pode ser campo (hipotetizaria a conclusao): aqui
    `ppIndex := 1/ppBest` e' DEFINIDO e a equacao e' CONCLUSAO do teorema.

Kernel-checked aqui:
  - camada da PARIDADE INVERSA: dado γ (StarAlgEquiv linear, γ²=id -- a
    linearizacao U_Π=J·J_ref vive a montante), a media E_Π=(x+γx)/2 e'
    idempotente, unital, γ-invariante, fixa os fixos e e' bimodular sobre eles;
  - camada PIMSNER-POPA: `IsPPLowerBound`, `ppBest = sSup`, `ppIndex = 1/ppBest`;
    otimalidade ⟹ `ppBest = sin²θ` ⟹ **TEOREMA DO INDICE DO NOME**:
    `ppIndex = csc²θ` e `ppIndex · sin²θ = 1` (CONCLUSOES);
  - forma TEMPERLEY-LIEB escalar [UNCONDITIONAL]: δ=1/sinθ; δ⁻²=sin²θ;
    amplitude → (quadrado) → peso → (inversao) → indice.

[MODEL-SPECIFIC TARGET, nao provado aqui]: P_F = e_Nome; E₁(e_Nome)=sin²θ·1;
sin²θ = constante PP otima de E_3L. Falhas nomeadas: mirror_not_jones,
markov_weight_not_sin_squared, pimsner_popa_constant_not_optimal,
reference_parity_not_involutive, no_expectation_exists, index_not_beta.
Nenhuma instancia e' construida. β jamais literal (θ e' variavel).
-/

namespace TGL.NameIndex

open TGL.TransportData

/-- Dados da PARIDADE INVERSA linearizada: `γ = Ad(U_Π)` com `U_Π = J·J_ref`
    (produto de duas antiunitarias = linear). O dado exigido e' a involutividade:
    a paridade inversa e' o referencial que compara `J` com `J_ref`. -/
structure ParityData (A : Type) [Ring A] [StarRing A] [Algebra ℂ A] where
  γ : A ≃⋆ₐ[ℂ] A
  γ_involutive : ∀ x : A, γ (γ x) = x

namespace ParityData

variable {A : Type} [Ring A] [StarRing A] [Algebra ℂ A] (P : ParityData A)

/-- A media de paridade: `E_Π(x) = (x + γ(x))/2` -- a esperanca do referencial. -/
noncomputable def average (x : A) : A := (2⁻¹ : ℂ) • (x + P.γ x)

theorem γ_average (x : A) : P.γ (P.average x) = P.average x := by
  simp only [average, map_smul, map_add, P.γ_involutive]
  rw [add_comm]

theorem average_idem (x : A) : P.average (P.average x) = P.average x := by
  have h := P.γ_average x
  simp only [average] at h ⊢
  rw [h]
  module

theorem average_of_fixed (x : A) (h : P.γ x = x) : P.average x = x := by
  simp only [average, h]
  module

theorem average_unital : P.average 1 = 1 := by
  simpa [average] using P.average_of_fixed 1 (map_one P.γ)

/-- Bimodularidade sobre os pontos fixos: a media e' uma esperanca sobre o
    subanel do referencial. -/
theorem average_bimodular (a b x : A) (ha : P.γ a = a) (hb : P.γ b = b) :
    P.average (a * x * b) = a * P.average x * b := by
  simp only [average, map_mul, ha, hb]
  rw [mul_smul_comm, smul_mul_assoc, mul_add, add_mul]

end ParityData

/-- Elemento positivo em forma concreta: `x = y*·y`. -/
def IsPositiveElem {A : Type} [Ring A] [StarRing A] (x : A) : Prop :=
  ∃ y : A, x = star y * y

/-- Cota inferior de Pimsner-Popa para uma esperanca (em DADOS): para todo
    positivo `x`, `ι(E x) − λ·x` e' positivo (i.e. `E(x) ≥ λx`). -/
def IsPPLowerBound {M Ext : Type}
    [Ring M] [StarRing M] [Algebra ℂ M]
    [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]
    (D : ConditionalExpectationData M Ext) (lam : ℝ) : Prop :=
  ∀ x : Ext, IsPositiveElem x → IsPositiveElem (D.incl (D.E x) - (lam : ℂ) • x)

variable {M Ext : Type}
  [Ring M] [StarRing M] [Algebra ℂ M]
  [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]

/-- A MELHOR constante de Pimsner-Popa (supremo das cotas validas). -/
noncomputable def ppBest (D : ConditionalExpectationData M Ext) : ℝ :=
  sSup {lam : ℝ | IsPPLowerBound D lam}

/-- O INDICE lido pela constante otima: `Ind = 1/ppBest`
    [KNOWN, Pimsner-Popa 1986: o melhor λ e' o inverso do indice]. DEFINIDO,
    jamais hipotetizado. -/
noncomputable def ppIndex (D : ConditionalExpectationData M Ext) : ℝ :=
  1 / ppBest D

/-- Otimalidade fixa o supremo: se `b` e' cota valida e domina toda cota,
    `ppBest = b`. -/
theorem ppBest_eq_of_optimal (D : ConditionalExpectationData M Ext) {b : ℝ}
    (hb : IsPPLowerBound D b)
    (hopt : ∀ lam : ℝ, IsPPLowerBound D lam → lam ≤ b) :
    ppBest D = b :=
  IsGreatest.csSup_eq ⟨hb, hopt⟩

/-- **O TEOREMA DO INDICE DO NOME** [KERNEL/CONDITIONAL ON DATA]: se `sin²θ` e'
    cota PP valida E OTIMA da esperanca do contorno, o indice e' `csc²θ`.
    A OTIMALIDADE e' indispensavel (sem ela so' se prova `Ind ≤ csc²θ`). -/
theorem name_index_eq_csc_sq (D : ConditionalExpectationData M Ext) (θ : ℝ)
    (hpp : IsPPLowerBound D (Real.sin θ ^ 2))
    (hopt : ∀ lam : ℝ, IsPPLowerBound D lam → lam ≤ Real.sin θ ^ 2) :
    ppIndex D = 1 / Real.sin θ ^ 2 := by
  unfold ppIndex
  rw [ppBest_eq_of_optimal D hpp hopt]

/-- A CONCLUSAO (jamais hipotese): `Ind · sin²θ = 1`. No angulo de Miguel
    (`sin²θ_M = β`, com β = α√e em runtime -- variavel aqui):
    `Ind(E_3L) = 1/β`. -/
theorem name_index_mul_sin_sq (D : ConditionalExpectationData M Ext) (θ : ℝ)
    (hs : Real.sin θ ≠ 0)
    (hpp : IsPPLowerBound D (Real.sin θ ^ 2))
    (hopt : ∀ lam : ℝ, IsPPLowerBound D lam → lam ≤ Real.sin θ ^ 2) :
    ppIndex D * Real.sin θ ^ 2 = 1 := by
  rw [name_index_eq_csc_sq D θ hpp hopt]
  field_simp

/-- Forma Temperley-Lieb escalar [KERNEL/UNCONDITIONAL]: o parametro de loop
    `δ = 1/sinθ` tem `δ⁻² = sin²θ` -- o peso Markov da primeira reflexao. -/
theorem tl_loop_parameter_sq_inv (θ : ℝ) (hs : Real.sin θ ≠ 0) :
    ((1 / Real.sin θ) ^ 2)⁻¹ = Real.sin θ ^ 2 := by
  field_simp

/-- A cadeia amplitude → peso → indice [KERNEL/UNCONDITIONAL]:
    `amplitude² · indice = indice · peso = 1` com amplitude `= sinθ = √β`,
    peso `= sin²θ = β`, indice `= δ² = csc²θ = 1/β`. -/
theorem amplitude_weight_index_chain (θ : ℝ) (hs : Real.sin θ ≠ 0) :
    (1 / Real.sin θ) ^ 2 * Real.sin θ ^ 2 = 1 := by
  field_simp

end TGL.NameIndex
