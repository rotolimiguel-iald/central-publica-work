import TGLExt.EmergentEinstein

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O GRUPO DE POINCARÉ À MÃO: as dez direções em kernel
  [TGLExt — v116, o incremento 37 do programa SemifiniteAnalysis]

A parede da testemunha (v104/v112/v114) pede um grupo de POINCARÉ
genuíno agindo fibro-sensivelmente. A mathlib NÃO tem o grupo de
Lorentz — esta pedra o constrói À MÃO, pela relação definidora:

* `LorentzGrp` = {Λ : M₄(ℝ) // Λᵀ η Λ = η} com instância de GRUPO
  provada à mão (★ a inversa é η Λᵀ η — `mul_eq_one_comm` fecha o
  lado direito; associatividade herdada das matrizes);
* ★ `lorentz_det_sq` — det Λ = ±1 (o quadrado é 1);
* ★★ `theBoost` — o boost hiperbólico B(χ) no plano (0,1), com
  ★★★ `boost_add` — B(χ₁)·B(χ₂) = B(χ₁+χ₂): a ENGRENAGEM HIPERBÓLICA
  do v113 elevada a LEI DE GRUPO em kernel (cosh_add/sinh_add), e
  ★ `boost_ne_one` — χ ≠ 0 ⟹ B(χ) ≠ 1 (o subgrupo a um parâmetro é
  genuíno);
* ★ `theParity` — a paridade P = diag(1,−1,1,1) com det = −1 (o
  representante do setor desconexo — a direção que o flip do v114
  antecipou);
* `PoincareGroup` = ℝ⁴ ⋊ O(1,3) com instância de GRUPO à mão
  (translações + Lorentz: as DEZ direções);
* ★★ `poincare_faithful` — a ação afim em ℝ⁴ é FIEL: quem fixa todos
  os pontos é a identidade — nenhuma das dez direções é cega.

A pedra seguinte (PoincareWitness) põe este grupo para agir na REDE.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — o grupo de Lorentz pela relação definidora -/

/-- a relação definidora: Λ preserva η. -/
def IsLorentz (A : Matrix (Fin 4) (Fin 4) ℝ) : Prop :=
  Aᵀ * eta4 * A = eta4

/-- O GRUPO DE LORENTZ O(1,3), à mão. -/
def LorentzGrp : Type :=
  {A : Matrix (Fin 4) (Fin 4) ℝ // IsLorentz A}

theorem eta4_mul_self : eta4 * eta4 = 1 := by
  unfold eta4
  rw [Matrix.diagonal_mul_diagonal]
  have h : (Matrix.diagonal
        (fun i => (![1, -1, -1, -1] : Fin 4 → ℝ) i * ![1, -1, -1, -1] i))
      = Matrix.diagonal (1 : Fin 4 → ℝ) := by
    congr 1
    funext i
    fin_cases i <;> norm_num
  rw [h]
  exact Matrix.diagonal_one

theorem eta4_swallow (M : Matrix (Fin 4) (Fin 4) ℝ) :
    eta4 * (eta4 * M) = M := by
  rw [← Matrix.mul_assoc, eta4_mul_self, Matrix.one_mul]

theorem isLorentz_one : IsLorentz 1 := by
  unfold IsLorentz
  rw [Matrix.transpose_one, Matrix.one_mul, Matrix.mul_one]

theorem isLorentz_mul {A B : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : IsLorentz A) (hB : IsLorentz B) : IsLorentz (A * B) := by
  unfold IsLorentz at *
  rw [Matrix.transpose_mul]
  calc Bᵀ * Aᵀ * eta4 * (A * B)
      = Bᵀ * (Aᵀ * eta4 * A) * B := by
        simp only [Matrix.mul_assoc]
    _ = Bᵀ * eta4 * B := by rw [hA]
    _ = eta4 := hB

/-- a inversa de Lorentz: η Λᵀ η. -/
def lorentzInv (A : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  eta4 * Aᵀ * eta4

theorem lorentzInv_mul {A : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : IsLorentz A) : lorentzInv A * A = 1 := by
  unfold lorentzInv
  calc eta4 * Aᵀ * eta4 * A
      = eta4 * (Aᵀ * eta4 * A) := by simp only [Matrix.mul_assoc]
    _ = eta4 * eta4 := by rw [hA]
    _ = 1 := eta4_mul_self

theorem mul_lorentzInv {A : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : IsLorentz A) : A * lorentzInv A = 1 :=
  mul_eq_one_comm.mp (lorentzInv_mul hA)

/-- [KERNEL] ★ o outro lado da relação: Λ η Λᵀ = η (via a inversa). -/
theorem isLorentz_other_side {A : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : IsLorentz A) : A * eta4 * Aᵀ = eta4 := by
  have h1 : A * lorentzInv A = 1 := mul_lorentzInv hA
  unfold lorentzInv at h1
  have h2 : A * (eta4 * Aᵀ * eta4) * eta4 = eta4 := by
    rw [h1, Matrix.one_mul]
  calc A * eta4 * Aᵀ
      = A * (eta4 * Aᵀ * eta4) * eta4 := by
        simp only [Matrix.mul_assoc, eta4_mul_self, Matrix.mul_one]
    _ = eta4 := h2

theorem isLorentz_inv {A : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : IsLorentz A) : IsLorentz (lorentzInv A) := by
  unfold IsLorentz lorentzInv
  have htr : (eta4 * Aᵀ * eta4)ᵀ = eta4 * A * eta4 := by
    rw [Matrix.transpose_mul, Matrix.transpose_mul,
      Matrix.transpose_transpose, eta4_symm]
    simp only [Matrix.mul_assoc]
  rw [htr]
  have hmid : A * eta4 * Aᵀ = eta4 := isLorentz_other_side hA
  calc eta4 * A * eta4 * eta4 * (eta4 * Aᵀ * eta4)
      = eta4 * (A * eta4 * Aᵀ) * eta4 := by
        simp only [Matrix.mul_assoc]
        rw [eta4_swallow]
    _ = eta4 * eta4 * eta4 := by rw [hmid]
    _ = eta4 := by rw [eta4_mul_self, Matrix.one_mul]

instance : One LorentzGrp := ⟨⟨1, isLorentz_one⟩⟩
instance : Mul LorentzGrp :=
  ⟨fun A B => ⟨A.1 * B.1, isLorentz_mul A.2 B.2⟩⟩
instance : Inv LorentzGrp :=
  ⟨fun A => ⟨lorentzInv A.1, isLorentz_inv A.2⟩⟩

/-- [KERNEL] ★★ O(1,3) é um GRUPO — provado à mão. -/
instance : Group LorentzGrp where
  mul_assoc a b c := Subtype.ext (Matrix.mul_assoc _ _ _)
  one_mul a := Subtype.ext (Matrix.one_mul _)
  mul_one a := Subtype.ext (Matrix.mul_one _)
  inv_mul_cancel a := Subtype.ext (lorentzInv_mul a.2)

theorem lorentzGrp_mul_val (A B : LorentzGrp) :
    (A * B).1 = A.1 * B.1 := rfl

theorem lorentzGrp_one_val : (1 : LorentzGrp).1 = 1 := rfl

/-- [KERNEL] ★ det Λ = ±1: o quadrado do determinante é 1. -/
theorem lorentz_det_sq (A : LorentzGrp) : A.1.det ^ 2 = 1 := by
  have h := congrArg Matrix.det A.2
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose, eta4_det] at h
  nlinarith [h]

/-! ## B — o boost: a engrenagem hiperbólica como lei de grupo -/

/-- a matriz do boost no plano (0,1). -/
def boostMat (χ : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of ![![Real.cosh χ, Real.sinh χ, 0, 0],
              ![Real.sinh χ, Real.cosh χ, 0, 0],
              ![0, 0, 1, 0],
              ![0, 0, 0, 1]]

theorem boostMat_isLorentz (χ : ℝ) : IsLorentz (boostMat χ) := by
  unfold IsLorentz boostMat eta4
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal_apply,
      Matrix.transpose_apply] <;>
    nlinarith [Real.cosh_sq_sub_sinh_sq χ]

/-- O BOOST como elemento do grupo. -/
def theBoost (χ : ℝ) : LorentzGrp := ⟨boostMat χ, boostMat_isLorentz χ⟩

/-- [KERNEL] ★★★ A ENGRENAGEM HIPERBÓLICA É LEI DE GRUPO:
    B(χ₁)·B(χ₂) = B(χ₁+χ₂) — a rapidez ADICIONA (cosh_add/sinh_add);
    o postulado de leitura do v113 virou teorema de composição. -/
theorem theBoost_add (χ₁ χ₂ : ℝ) :
    theBoost χ₁ * theBoost χ₂ = theBoost (χ₁ + χ₂) := by
  apply Subtype.ext
  show boostMat χ₁ * boostMat χ₂ = boostMat (χ₁ + χ₂)
  unfold boostMat
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four, Real.cosh_add,
      Real.sinh_add] <;>
    ring

/-- [KERNEL] ★ o subgrupo a um parâmetro é GENUÍNO: χ ≠ 0 ⟹ B(χ) ≠ 1
    (a entrada (0,1) é sinh χ ≠ 0). -/
theorem boost_ne_one (χ : ℝ) (hχ : χ ≠ 0) : theBoost χ ≠ 1 := by
  intro h
  have h01 := congrArg (fun A : LorentzGrp => A.1 0 1) h
  have hb : (theBoost χ).1 0 1 = Real.sinh χ := by
    unfold theBoost boostMat
    simp
  have ho : (1 : LorentzGrp).1 0 1 = 0 := by
    rw [lorentzGrp_one_val]
    simp
  rw [hb, ho] at h01
  exact (Real.sinh_ne_zero.mpr hχ) h01

/-! ## C — a paridade: o setor desconexo -/

/-- o vetor da paridade espacial-1: (1,−1,1,1). -/
def parityVec : Fin 4 → ℝ := fun i => if i = 1 then -1 else 1

/-- a matriz da paridade espacial-1: P = diag(1,−1,1,1). -/
def parityMat : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal parityVec

theorem parityMat_isLorentz : IsLorentz parityMat := by
  unfold IsLorentz parityMat eta4
  rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal,
    Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i <;> simp [parityVec]

/-- A PARIDADE como elemento do grupo. -/
def theParity : LorentzGrp := ⟨parityMat, parityMat_isLorentz⟩

/-- [KERNEL] ★ det P = −1: a paridade mora no setor DESCONEXO. -/
theorem parity_det : theParity.1.det = -1 := by
  show parityMat.det = -1
  unfold parityMat
  rw [Matrix.det_diagonal, Fin.prod_univ_four]
  simp [parityVec]

/-- [KERNEL] ★ a paridade não é a identidade (entrada (1,1)). -/
theorem parity_ne_one : theParity ≠ 1 := by
  intro h
  have h11 := congrArg (fun A : LorentzGrp => A.1 1 1) h
  have hp : (theParity).1 1 1 = -1 := by
    show parityMat 1 1 = -1
    unfold parityMat
    simp [parityVec]
  have ho : (1 : LorentzGrp).1 1 1 = 1 := by
    rw [lorentzGrp_one_val]
    simp
  rw [hp, ho] at h11
  norm_num at h11

/-! ## D — o grupo de Poincaré: ℝ⁴ ⋊ O(1,3) -/

/-- O GRUPO DE POINCARÉ: translação + Lorentz (as dez direções). -/
structure PoincareGroup where
  tr : Fin 4 → ℝ
  lor : LorentzGrp

instance : One PoincareGroup := ⟨⟨0, 1⟩⟩
instance : Mul PoincareGroup :=
  ⟨fun g h => ⟨g.tr + g.lor.1.mulVec h.tr, g.lor * h.lor⟩⟩
instance : Inv PoincareGroup :=
  ⟨fun g => ⟨-(g.lor⁻¹.1.mulVec g.tr), g.lor⁻¹⟩⟩

theorem poincare_mul_tr (g h : PoincareGroup) :
    (g * h).tr = g.tr + g.lor.1.mulVec h.tr := rfl

theorem poincare_mul_lor (g h : PoincareGroup) :
    (g * h).lor = g.lor * h.lor := rfl

theorem poincare_one_tr : (1 : PoincareGroup).tr = 0 := rfl

theorem poincare_one_lor : (1 : PoincareGroup).lor = 1 := rfl

theorem poincare_ext {g h : PoincareGroup}
    (htr : g.tr = h.tr) (hlor : g.lor = h.lor) : g = h := by
  cases g
  cases h
  simp only at htr hlor
  rw [htr, hlor]

/-- [KERNEL] ★★ POINCARÉ É UM GRUPO — o produto semidireto à mão. -/
instance : Group PoincareGroup where
  mul_assoc g h k := by
    apply poincare_ext
    · show (g.tr + g.lor.1.mulVec h.tr)
          + (g.lor * h.lor).1.mulVec k.tr
        = g.tr + g.lor.1.mulVec (h.tr + h.lor.1.mulVec k.tr)
      rw [lorentzGrp_mul_val, Matrix.mulVec_add, ← Matrix.mulVec_mulVec]
      rw [add_assoc]
    · show (g.lor * h.lor) * k.lor = g.lor * (h.lor * k.lor)
      exact mul_assoc _ _ _
  one_mul g := by
    apply poincare_ext
    · show (0 : Fin 4 → ℝ) + (1 : LorentzGrp).1.mulVec g.tr = g.tr
      rw [lorentzGrp_one_val, Matrix.one_mulVec, zero_add]
    · show (1 : LorentzGrp) * g.lor = g.lor
      exact one_mul _
  mul_one g := by
    apply poincare_ext
    · show g.tr + g.lor.1.mulVec (0 : Fin 4 → ℝ) = g.tr
      rw [Matrix.mulVec_zero, add_zero]
    · show g.lor * 1 = g.lor
      exact mul_one _
  inv_mul_cancel g := by
    apply poincare_ext
    · show -(g.lor⁻¹.1.mulVec g.tr) + g.lor⁻¹.1.mulVec g.tr = 0
      exact neg_add_cancel _
    · show g.lor⁻¹ * g.lor = 1
      exact inv_mul_cancel _

/-! ## E — a ação afim e a fidelidade das dez direções -/

/-- a ação afim de Poincaré no espaço-tempo: x ↦ Λx + a. -/
def pAct (g : PoincareGroup) (x : Fin 4 → ℝ) : Fin 4 → ℝ :=
  g.lor.1.mulVec x + g.tr

theorem pAct_one (x : Fin 4 → ℝ) : pAct 1 x = x := by
  unfold pAct
  rw [poincare_one_tr, poincare_one_lor, lorentzGrp_one_val,
    Matrix.one_mulVec, add_zero]

theorem pAct_mul (g h : PoincareGroup) (x : Fin 4 → ℝ) :
    pAct (g * h) x = pAct g (pAct h x) := by
  unfold pAct
  rw [poincare_mul_tr, poincare_mul_lor, lorentzGrp_mul_val,
    ← Matrix.mulVec_mulVec, Matrix.mulVec_add]
  abel

/-- [KERNEL] ★★ A AÇÃO É FIEL: quem fixa TODOS os pontos do
    espaço-tempo é a identidade — nenhuma das dez direções é cega. -/
theorem poincare_faithful (g : PoincareGroup)
    (h : ∀ x, pAct g x = x) : g = 1 := by
  have h0 := h 0
  unfold pAct at h0
  rw [Matrix.mulVec_zero, zero_add] at h0
  have hL : ∀ x, g.lor.1.mulVec x = x := by
    intro x
    have hx := h x
    unfold pAct at hx
    rw [h0, add_zero] at hx
    exact hx
  have hM : g.lor.1 = 1 := by
    apply Matrix.ext_of_mulVec_single
    intro j
    rw [hL (Pi.single j 1), Matrix.one_mulVec]
  apply poincare_ext
  · rw [h0, poincare_one_tr]
  · rw [poincare_one_lor]
    exact Subtype.ext hM

/-- [KERNEL] ★ a translação pura move TODO ponto (a ≠ 0). -/
theorem translation_moves (a : Fin 4 → ℝ) (ha : a ≠ 0) (x : Fin 4 → ℝ) :
    pAct ⟨a, 1⟩ x ≠ x := by
  unfold pAct
  intro h
  apply ha
  have h1 : (1 : LorentzGrp).1.mulVec x + a = x := h
  rw [lorentzGrp_one_val, Matrix.one_mulVec] at h1
  have h2 := congrArg (fun v => v - x) h1
  simpa using h2

end

end TGLExt
