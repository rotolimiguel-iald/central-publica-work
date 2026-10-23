import TGLExt.LeftRight

set_option autoImplicit false

/-!
# Tomiyama finito: esperanças condicionais + relação de Jones + MASA
  [TGLExt — Degrau 1 (fecho parcial) → entrada do Degrau 2]

As duas esperanças condicionais canônicas de `Mₙ(ℂ)` como teoremas de kernel:

* `E_ℂ = trExpect` (sobre os escalares): unital, idempotente, preserva o
  traço, autoadjunta na forma de Frobenius — e a RELAÇÃO DE JONES ESCALAR
  `e·L_x·e = (Tr x / n)·e`;
* `E_D = diagExpect` (sobre a subálgebra diagonal): unital, idempotente,
  D-bimodular, preserva traço, autoadjunta em Frobenius, POSITIVA — e a
  RELAÇÃO DE JONES `e_D·L_x·e_D = L_{E_D(x)}·e_D`: a compressão pelo
  espelho É a esperança condicional (a lei do transporte do seletor, v26
  da casa, agora como teorema externo em dimensão finita);
* MASA: `D′ = D` — a diagonal é maximal abeliana (o comutante DENTRO da
  álgebra, primeiro uso do `commutantSet` em `Mₙ` em vez de `End`).

β NÃO entra: infraestrutura pura. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## C1: a esperança condicional tracial E_ℂ -/

/-- `E_ℂ(x) = (Tr x / n)·1` — a esperança condicional sobre os escalares. -/
def trExpect (x : Matrix n n ℂ) : Matrix n n ℂ :=
  (x.trace / (Fintype.card n : ℂ)) • (1 : Matrix n n ℂ)

theorem trExpect_one [Nonempty n] : trExpect (1 : Matrix n n ℂ) = 1 := by
  simp [trExpect]

/-- [KERNEL] `E_ℂ` preserva o traço (traço de Markov). -/
theorem trace_trExpect [Nonempty n] (x : Matrix n n ℂ) :
    (trExpect x).trace = x.trace := by
  have hc : ((Fintype.card n : ℂ)) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  simp [trExpect, div_mul_cancel₀ _ hc]

theorem trExpect_idem [Nonempty n] (x : Matrix n n ℂ) :
    trExpect (trExpect x) = trExpect x := by
  rw [show trExpect (trExpect x)
      = ((trExpect x).trace / (Fintype.card n : ℂ)) • (1 : Matrix n n ℂ) from rfl,
    trace_trExpect]
  rfl

/-- [KERNEL] `E_ℂ` é autoadjunta na forma de Frobenius: projeção ORTOGONAL. -/
theorem frob_trExpect_symm (x y : Matrix n n ℂ) :
    frob (trExpect x) y = frob x (trExpect y) := by
  simp only [frob, trExpect, conjTranspose_smul, conjTranspose_one, Matrix.smul_mul,
    Matrix.one_mul, Matrix.mul_smul, Matrix.mul_one, trace_smul, smul_eq_mul,
    trace_conjTranspose, star_div₀, star_natCast]
  ring

/-! ## C2: eTr como endomorfismo e a relação de Jones escalar -/

/-- `E_ℂ` empacotada como endomorfismo de `H = Mₙ(ℂ)`. -/
def eTr : Module.End ℂ (Matrix n n ℂ) where
  toFun := trExpect
  map_add' x y := by simp [trExpect, add_div, add_smul]
  map_smul' c x := by simp [trExpect, smul_smul, mul_div_assoc]

@[simp] theorem eTr_apply (x : Matrix n n ℂ) : eTr x = trExpect x := rfl

/-- [KERNEL] RELAÇÃO DE JONES ESCALAR: `e·L_x·e = (Tr x/n)·e` — comprimir
    pelo projetor tracial devolve o peso do estado. -/
theorem eTr_Lmul_eTr (x : Matrix n n ℂ) :
    eTr * Lmul x * eTr = (x.trace / (Fintype.card n : ℂ)) • eTr := by
  refine LinearMap.ext fun y => ?_
  simp only [Module.End.mul_apply, LinearMap.smul_apply, eTr_apply, Lmul_apply,
    trExpect, Matrix.mul_smul, Matrix.mul_one, trace_smul, smul_eq_mul, smul_smul]
  congr 1
  ring

/-! ## C3: a esperança condicional diagonal E_D -/

/-- `E_D(x) = diag(x)` — a esperança condicional sobre a subálgebra diagonal. -/
def diagExpect (x : Matrix n n ℂ) : Matrix n n ℂ := diagonal x.diag

omit [Fintype n] in
theorem diagExpect_one : diagExpect (1 : Matrix n n ℂ) = 1 := by
  simp [diagExpect]

omit [Fintype n] in
theorem diagExpect_idem (x : Matrix n n ℂ) :
    diagExpect (diagExpect x) = diagExpect x := by
  simp [diagExpect]

omit [Fintype n] in
theorem diagExpect_diagonal (d : n → ℂ) : diagExpect (diagonal d) = diagonal d := by
  simp [diagExpect]

/-- [KERNEL] `E_D` é D-BIMODULAR: a lei da esperança condicional
    (Tomiyama finito — o dado central de `ConditionalExpectationData` da
    casa, agora teorema externo). -/
theorem diagExpect_bimod (d d' : n → ℂ) (x : Matrix n n ℂ) :
    diagExpect (diagonal d * x * diagonal d')
      = diagonal d * diagExpect x * diagonal d' := by
  ext i j
  by_cases h : i = j
  · subst h; simp [diagExpect]
  · simp [diagExpect, h]

/-- [KERNEL] `E_D` preserva o traço. -/
theorem trace_diagExpect (x : Matrix n n ℂ) : (diagExpect x).trace = x.trace := by
  simp [diagExpect, Matrix.trace]

/-- [KERNEL] `E_D` é autoadjunta na forma de Frobenius: projeção ORTOGONAL. -/
theorem frob_diagExpect_symm (x y : Matrix n n ℂ) :
    frob (diagExpect x) y = frob x (diagExpect y) := by
  simp [frob, diagExpect, Matrix.trace, Matrix.mul_apply, diagonal_apply,
    conjTranspose_apply, Finset.sum_ite_eq, apply_ite]

omit [Fintype n] in
/-- [KERNEL] `E_D` é POSITIVA: leva psd em psd (esperança condicional genuína). -/
theorem diagExpect_posSemidef {x : Matrix n n ℂ} (hx : x.PosSemidef) :
    (diagExpect x).PosSemidef :=
  posSemidef_diagonal_iff.mpr fun _ => hx.diag_nonneg

/-! ## C4: eD como endomorfismo e a relação de Jones -/

/-- `E_D` empacotada como endomorfismo de `H = Mₙ(ℂ)` (o projetor de Jones
    da inclusão `D ⊆ Mₙ` agindo no GNS do traço). -/
def eD : Module.End ℂ (Matrix n n ℂ) where
  toFun := diagExpect
  map_add' x y := by simp [diagExpect]
  map_smul' c x := by simp [diagExpect]

omit [Fintype n] in
@[simp] theorem eD_apply (x : Matrix n n ℂ) : eD x = diagExpect x := rfl

/-- [KERNEL] A RELAÇÃO DE JONES: `e_D·L_x·e_D = L_{E_D(x)}·e_D` — a
    compressão pelo espelho É a esperança condicional. A lei do transporte
    do seletor (v26 da casa), como teorema de kernel em dimensão finita. -/
theorem eD_Lmul_eD (x : Matrix n n ℂ) :
    eD * Lmul x * eD = Lmul (diagExpect x) * eD := by
  refine LinearMap.ext fun y => ?_
  simp only [Module.End.mul_apply, eD_apply, Lmul_apply]
  ext i j
  by_cases h : i = j
  · subst h; simp [diagExpect]
  · simp [diagExpect, h]

/-! ## C5: a MASA diagonal -/

/-- [KERNEL] MASA: `D′ = D` — o comutante da subálgebra diagonal DENTRO de
    `Mₙ(ℂ)` é ela mesma (maximal abeliana). A prova mata `x i j` (i≠j)
    testando contra o indicador `diagonal (Pi.single i 1)`. -/
theorem commutant_range_diagonal :
    commutantSet (Set.range (diagonal : (n → ℂ) → Matrix n n ℂ))
      = Set.range (diagonal : (n → ℂ) → Matrix n n ℂ) := by
  apply Set.Subset.antisymm
  · intro x hx
    refine ⟨x.diag, Matrix.ext fun i j => ?_⟩
    by_cases h : i = j
    · subst h; simp
    · have h1 := Matrix.ext_iff.mpr
        (hx (diagonal (Pi.single i 1)) ⟨Pi.single i 1, rfl⟩) i j
      simp only [diagonal_mul, mul_diagonal, Pi.single_eq_same, one_mul,
        Pi.single_eq_of_ne (Ne.symm h), mul_zero] at h1
      simp [diagonal_apply_ne _ h, h1]
  · rintro _ ⟨d, rfl⟩ _ ⟨d', rfl⟩
    exact (commute_diagonal d' d).eq

end

end TGLExt
