import Mathlib
import TGL.TransportData

set_option autoImplicit false

/-!
# A torre de Jones da Meia-Nat   [KERNEL]   (v28 -- bloco solo do codificador)

O PRIMEIRO HABITANTE construido de uma camada do programa: a torre finita
`ℂ ⊆ (Fin 2 → ℂ) ⊆ M₂(ℂ)` com espelho `e = (1/2)·[[1,1],[1,1]]`, peso de
Markov `1/2` e indice `2` -- um TERMO de `JonesTowerData`, campo a campo,
sem sorry. Com o termo, os teoremas condicionais do v26 DISPARAM sobre ele:
o espelho Meia-Nat NAO desce (selector_lives_upstairs INSTANCIADO).

A EXPULSAO DO NOME [KERNEL]: no espelho finito do qubit de fronteira, o peso
transportado e' `(b, 1−b)`; ele e' MARKOV (multiplo escalar da identidade)
SE E SOMENTE SE `b = 1/2`. A Meia-Nat e' o UNICO peso de Markov finitamente
realizavel neste espelho; o peso fisico `β ≠ 1/2` expulsa o espelho do Nome
para o continuo -- coerente com o fato [KNOWN, ledger] de que indices de
inclusoes multi-matriciais sao algebricos e `1/β` e' empirico (medido).

Honestidade: este habitante valida as CAMADAS por exibicao (nao-vacuidade
com conteudo real); ele NAO e' a inclusao-β dos Three Locks (peso 1/2 ≠ β;
indice 2 ≠ 1/β). Os alvos modelo-especificos do v27 permanecem ABERTOS.
-/

namespace TGL.HalfNatJonesTower

open TGL.TransportData

abbrev Nc := ℂ
abbrev Md := Fin 2 → ℂ
abbrev Ex := Matrix (Fin 2) (Fin 2) ℂ

/-- Inclusao constante `ℂ → ℂ²`. -/
noncomputable def constIncl : Nc →⋆ₐ[ℂ] Md where
  toFun c := Function.const _ c
  map_one' := rfl
  map_mul' _ _ := rfl
  map_zero' := rfl
  map_add' _ _ := rfl
  commutes' _ := rfl
  map_star' _ := rfl

/-- Esperanca inferior `E₀(f) = (f 0 + f 1)/2` (a media das duas faces). -/
noncomputable def E0 : Md →ₗ[ℂ] Nc where
  toFun f := (2⁻¹ : ℂ) * (f 0 + f 1)
  map_add' f g := by simp; ring
  map_smul' c f := by simp; ring

/-- Camada inferior: `ℂ ⊆ ℂ²` com a esperanca da media. -/
noncomputable def lowerCE : ConditionalExpectationData Nc Md where
  incl := constIncl
  incl_injective := fun a b h => congrFun h 0
  E := E0
  E_unital := by
    show (2⁻¹ : ℂ) * ((1 : Md) 0 + (1 : Md) 1) = 1
    norm_num
  E_star := by
    intro f
    show (2⁻¹ : ℂ) * ((star f) 0 + (star f) 1) = star ((2⁻¹ : ℂ) * (f 0 + f 1))
    simp [Pi.star_apply, star_mul', star_add, star_inv₀]
  E_bimodular := by
    intro a b f
    show (2⁻¹ : ℂ) * ((constIncl a * f * constIncl b) 0 + (constIncl a * f * constIncl b) 1)
        = a * ((2⁻¹ : ℂ) * (f 0 + f 1)) * b
    simp [constIncl, Function.const]
    ring
  E_faithful := by
    intro f hf
    have hval : (2⁻¹ : ℂ) * ((star f * f) 0 + (star f * f) 1) = 0 := hf
    have h2 : (2⁻¹ : ℂ) ≠ 0 := by norm_num
    have hsum : star (f 0) * f 0 + star (f 1) * f 1 = 0 := by
      have := (mul_eq_zero.mp hval).resolve_left h2
      simpa [Pi.mul_apply, Pi.star_apply] using this
    have e0 : star (f 0) * f 0 = (Complex.normSq (f 0) : ℂ) := by
      rw [Complex.star_def]; exact Complex.normSq_eq_conj_mul_self.symm
    have e1 : star (f 1) * f 1 = (Complex.normSq (f 1) : ℂ) := by
      rw [Complex.star_def]; exact Complex.normSq_eq_conj_mul_self.symm
    rw [e0, e1] at hsum
    have hr : Complex.normSq (f 0) + Complex.normSq (f 1) = 0 := by exact_mod_cast hsum
    have h00 : Complex.normSq (f 0) = 0 := by
      nlinarith [Complex.normSq_nonneg (f 0), Complex.normSq_nonneg (f 1)]
    have h11 : Complex.normSq (f 1) = 0 := by
      nlinarith [Complex.normSq_nonneg (f 0), Complex.normSq_nonneg (f 1)]
    funext i
    fin_cases i
    · exact Complex.normSq_eq_zero.mp h00
    · exact Complex.normSq_eq_zero.mp h11

/-- Inclusao diagonal `ℂ² → M₂`. -/
noncomputable def diagIncl : Md →⋆ₐ[ℂ] Ex where
  toFun := Matrix.diagonal
  map_one' := Matrix.diagonal_one
  map_mul' f g := (Matrix.diagonal_mul_diagonal f g).symm
  map_zero' := Matrix.diagonal_zero
  map_add' f g := (Matrix.diagonal_add f g).symm
  commutes' c := by rw [Matrix.algebraMap_eq_diagonal]
  map_star' f := (Matrix.diagonal_conjTranspose f).symm

/-- Esperanca superior `E₁(x) = diagonal de x` (compressao ao referencial). -/
noncomputable def E1 : Ex →ₗ[ℂ] Md where
  toFun x i := x i i
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- Camada superior: `ℂ² ⊆ M₂` com a compressao diagonal. -/
noncomputable def upperCE : ConditionalExpectationData Md Ex where
  incl := diagIncl
  incl_injective := fun f g h => funext fun i => by
    have := congrArg (fun m => m i i) h
    simpa [diagIncl, Matrix.diagonal] using this
  E := E1
  E_unital := funext fun i => Matrix.one_apply_eq i
  E_star := fun x => funext fun i => by
    show (star x) i i = star (x i i)
    simp [Matrix.star_apply]
  E_bimodular := by
    intro a b x
    funext i
    show (diagIncl a * x * diagIncl b) i i = (a * (fun j => x j j) * b) i
    simp [diagIncl, Matrix.diagonal_mul, Matrix.mul_diagonal]
  E_faithful := by
    intro x hx
    have hii : ∀ i : Fin 2, (star x * x) i i = 0 := fun i => congrFun hx i
    have hterm : ∀ i k : Fin 2, x k i = 0 := by
      intro i k
      have h := hii i
      rw [Matrix.mul_apply, Fin.sum_univ_two] at h
      have e0 : (star x) i 0 * x 0 i = (Complex.normSq (x 0 i) : ℂ) := by
        rw [Matrix.star_apply, Complex.star_def]
        exact Complex.normSq_eq_conj_mul_self.symm
      have e1 : (star x) i 1 * x 1 i = (Complex.normSq (x 1 i) : ℂ) := by
        rw [Matrix.star_apply, Complex.star_def]
        exact Complex.normSq_eq_conj_mul_self.symm
      rw [e0, e1] at h
      have hr : Complex.normSq (x 0 i) + Complex.normSq (x 1 i) = 0 := by exact_mod_cast h
      have h00 : Complex.normSq (x 0 i) = 0 := by
        nlinarith [Complex.normSq_nonneg (x 0 i), Complex.normSq_nonneg (x 1 i)]
      have h11 : Complex.normSq (x 1 i) = 0 := by
        nlinarith [Complex.normSq_nonneg (x 0 i), Complex.normSq_nonneg (x 1 i)]
      fin_cases k
      · exact Complex.normSq_eq_zero.mp h00
      · exact Complex.normSq_eq_zero.mp h11
    ext k i
    exact hterm i k

/-- O ESPELHO da Meia-Nat: `e = (1/2)·[[1,1],[1,1]]` (o vetor uniforme). -/
noncomputable def eHalf : Ex := Matrix.of fun _ _ => (2⁻¹ : ℂ)

theorem eHalf_idem : eHalf * eHalf = eHalf := by
  ext i j
  rw [Matrix.mul_apply, Fin.sum_univ_two]
  show (2⁻¹ : ℂ) * 2⁻¹ + 2⁻¹ * 2⁻¹ = 2⁻¹
  norm_num

theorem eHalf_star : star eHalf = eHalf := by
  ext i j
  show star ((2⁻¹ : ℂ)) = (2⁻¹ : ℂ)
  simp [star_inv₀]

/-- A relacao de Jones: `e · diag(f) · e = ι(ι₀(E₀ f)) · e`. -/
theorem eHalf_jones (f : Md) :
    eHalf * diagIncl f * eHalf = diagIncl (constIncl (E0 f)) * eHalf := by
  ext i j
  simp [eHalf, diagIncl, constIncl, E0, Matrix.mul_apply, Fin.sum_univ_two,
        Matrix.diagonal, Function.const]
  fin_cases i <;> fin_cases j <;> ring

/-- O peso de Markov do espelho: `E₁(e) = (1/2)·1` — a MEIA-NAT. -/
theorem eHalf_weight : upperCE.E eHalf = ((1 / 2 : ℝ) : ℂ) • (1 : Md) := by
  funext i
  show eHalf i i = ((1 / 2 : ℝ) : ℂ) • (1 : Md) i
  simp [eHalf]

/-- **O PRIMEIRO HABITANTE**: a torre de Jones da Meia-Nat, termo construido
    campo a campo. Peso `1/2`, indice `2`. -/
noncomputable def halfNatJonesTower : JonesTowerData Nc Md Ex where
  lower := lowerCE
  upper := upperCE
  eJones := eHalf
  eJones_idem := eHalf_idem
  eJones_star := eHalf_star
  jones_relation := eHalf_jones
  markovWeight := 1 / 2
  markovWeight_pos := by norm_num
  markovWeight_lt_one := by norm_num
  dual_expectation_jones := eHalf_weight
  indexVal := 2
  index_eq_inverse_weight := by norm_num

/-- O corolario existencial — SOMENTE via `⟨termo⟩`. -/
theorem halfNatJonesTower_exists :
    Nonempty (JonesTowerData Nc Md Ex) :=
  ⟨halfNatJonesTower⟩

/-- [KERNEL — v26 DISPARA no termo] O espelho da Meia-Nat NAO desce:
    `selector_lives_upstairs` INSTANCIADO num habitante real. -/
theorem halfNat_mirror_not_descended :
    halfNatJonesTower.eJones ≠
      halfNatJonesTower.upper.incl (halfNatJonesTower.upper.E halfNatJonesTower.eJones) :=
  jones_selector_not_descended halfNatJonesTower

/-- [KERNEL — estatuto REFINADO na rodada 4 do especialista: o finito NAO expulsa
    o Nome; ele separa o peso GEOMETRICO do peso TRACIAL de Markov]
    O peso transportado do espelho-b do qubit e' `(b, 1−b)`; e' MARKOV (multiplo
    escalar da identidade) ⟺ `b = 1/2`. O que se expulsa e' a IDENTIFICACAO do
    β generico com o traco normalizado rank-one — nao o β em si, que vive
    finitamente como RELACAO (`p·q_β·p = β·p`, ver NameRelation.lean, v30):
    `FINITE_MARKOV_TRACE_EXPELS_ONLY_THE_GENERIC_TRACE_IDENTIFICATION`. -/
theorem finite_markov_forces_half (b : ℝ) :
    (∃ c : ℂ, (fun i : Fin 2 => if i = 0 then ((b : ℝ) : ℂ) else ((1 - b : ℝ) : ℂ)) =
      fun _ => c) ↔ b = 1 / 2 := by
  constructor
  · rintro ⟨c, hc⟩
    have h0 := congrFun hc 0
    have h1 := congrFun hc 1
    simp at h0 h1
    have hb : ((b : ℝ) : ℂ) = 1 - ((b : ℝ) : ℂ) := h0.trans h1.symm
    have hbr : b = 1 - b := by exact_mod_cast hb
    linarith
  · intro hb
    refine ⟨((1 / 2 : ℝ) : ℂ), funext fun i => ?_⟩
    fin_cases i <;> norm_num [hb]

end TGL.HalfNatJonesTower
