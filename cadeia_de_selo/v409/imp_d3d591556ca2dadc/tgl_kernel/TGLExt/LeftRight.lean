import TGLExt.Commutant

set_option autoImplicit false

/-!
# Esquerda/Direita: o bicomutante concreto e a conjugação J   [TGLExt — Degraus 1→0]

O palco do Tomita–Takesaki finito: `H = Mₙ(ℂ)` com a forma de Frobenius
`⟨x,y⟩ = Tr(xᴴ y)`. A álgebra `M = Mₙ(ℂ)` age em H por multiplicação à
esquerda (`Lmul`); provamos que o comutante é EXATAMENTE a multiplicação
à direita (`Rmul`) — a forma concreta do teorema do bicomutante para a
representação padrão — e que a conjugação `J z = zᴴ` é antiunitária e
realiza `J M J = M′` (a metade algébrica do teorema de Tomita).
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- Multiplicação à esquerda: a representação padrão de `Mₙ(ℂ)` em `H = Mₙ(ℂ)`. -/
def Lmul (a : Matrix n n ℂ) : Module.End ℂ (Matrix n n ℂ) := LinearMap.mulLeft ℂ a

/-- Multiplicação à direita: a representação oposta (o candidato a comutante). -/
def Rmul (a : Matrix n n ℂ) : Module.End ℂ (Matrix n n ℂ) := LinearMap.mulRight ℂ a

@[simp] theorem Lmul_apply (a x : Matrix n n ℂ) : Lmul a x = a * x := rfl
@[simp] theorem Rmul_apply (a x : Matrix n n ℂ) : Rmul a x = x * a := rfl

/-- [KERNEL] `Lmul` e `Rmul` comutam (associatividade — a raiz de tudo). -/
theorem lmul_mul_rmul_comm (a b : Matrix n n ℂ) :
    Lmul a * Rmul b = Rmul b * Lmul a :=
  LinearMap.ext fun x => by simp [Module.End.mul_apply, mul_assoc]

/-- [KERNEL] O COMUTANTE CONCRETO: `L(Mₙ)′ = R(Mₙ)`.
    (Se `T` comuta com toda `Lmul a`, então `T = Rmul (T 1)`.) -/
theorem commutant_range_Lmul :
    commutantSet (Set.range (Lmul (n := n))) = Set.range (Rmul (n := n)) := by
  apply Set.Subset.antisymm
  · intro T hT
    refine ⟨T 1, LinearMap.ext fun x => ?_⟩
    have h := LinearMap.congr_fun (hT (Lmul x) ⟨x, rfl⟩) 1
    simpa [Module.End.mul_apply] using h
  · rintro _ ⟨b, rfl⟩ _ ⟨a, rfl⟩
    exact lmul_mul_rmul_comm a b

/-- [KERNEL] O simétrico: `R(Mₙ)′ = L(Mₙ)`. -/
theorem commutant_range_Rmul :
    commutantSet (Set.range (Rmul (n := n))) = Set.range (Lmul (n := n)) := by
  apply Set.Subset.antisymm
  · intro T hT
    refine ⟨T 1, LinearMap.ext fun x => ?_⟩
    have h := LinearMap.congr_fun (hT (Rmul x) ⟨x, rfl⟩) 1
    simpa [Module.End.mul_apply] using h
  · rintro _ ⟨b, rfl⟩ _ ⟨a, rfl⟩
    exact (lmul_mul_rmul_comm b a).symm

/-- [KERNEL] O TEOREMA DO BICOMUTANTE (forma concreta): `L(Mₙ)′′ = L(Mₙ)`.
    A representação padrão da álgebra plena é seu próprio bicomutante —
    o caso concreto do teorema de von Neumann; o caso geral (subálgebras-*
    próprias de `Mₙ`) é a próxima pedra do Degrau 1. -/
theorem bicommutant_range_Lmul :
    commutantSet (commutantSet (Set.range (Lmul (n := n)))) =
      Set.range (Lmul (n := n)) := by
  rw [commutant_range_Lmul, commutant_range_Rmul]

/-! ## A conjugação modular J do traço -/

/-- A conjugação modular do estado tracial: `J z = zᴴ` (antilinear, involutiva). -/
def Jconj (z : Matrix n n ℂ) : Matrix n n ℂ := zᴴ

omit [Fintype n] [DecidableEq n] in
@[simp] theorem Jconj_Jconj (z : Matrix n n ℂ) : Jconj (Jconj z) = z :=
  conjTranspose_conjTranspose z

omit [Fintype n] [DecidableEq n] in
theorem Jconj_add (x y : Matrix n n ℂ) : Jconj (x + y) = Jconj x + Jconj y :=
  conjTranspose_add x y

omit [Fintype n] [DecidableEq n] in
/-- `J` é ANTIlinear: `J(c • z) = c̄ • J z`. -/
theorem Jconj_smul (c : ℂ) (z : Matrix n n ℂ) :
    Jconj (c • z) = star c • Jconj z := by
  simp [Jconj]

/-- A forma de Frobenius `⟨x,y⟩ = Tr(xᴴ y)` — o produto interno GNS do traço. -/
def frob (x y : Matrix n n ℂ) : ℂ := (xᴴ * y).trace

omit [DecidableEq n] in
theorem frob_conj_symm (x y : Matrix n n ℂ) : frob y x = star (frob x y) := by
  show (yᴴ * x).trace = star ((xᴴ * y).trace)
  rw [← trace_conjTranspose, conjTranspose_mul, conjTranspose_conjTranspose]

omit [DecidableEq n] in
/-- [KERNEL] `J` é ANTIUNITÁRIO para a forma de Frobenius: `⟨Jx, Jy⟩ = ⟨y, x⟩`. -/
theorem frob_Jconj_Jconj (x y : Matrix n n ℂ) :
    frob (Jconj x) (Jconj y) = frob y x := by
  simp only [frob, Jconj, conjTranspose_conjTranspose]
  exact trace_mul_comm x yᴴ

/-- [KERNEL] `J L_a J = R_{aᴴ}`: a conjugação leva a álgebra ao comutante.
    A metade algébrica do TEOREMA DE TOMITA, em dimensão finita. -/
theorem Jconj_Lmul_Jconj (a z : Matrix n n ℂ) :
    Jconj (Lmul a (Jconj z)) = Rmul aᴴ z := by
  simp [Jconj, conjTranspose_mul]

/-- [KERNEL] `J M J = M′` na forma existencial: todo elemento de `M′ = R(Mₙ)`
    é conjugação `J (·) J` de um elemento de `M = L(Mₙ)`. -/
theorem exists_Jconj_conj_Lmul (b : Matrix n n ℂ) :
    ∃ a, ∀ z, Jconj (Lmul a (Jconj z)) = Rmul b z :=
  ⟨bᴴ, fun z => by simp [Jconj, conjTranspose_mul]⟩

end

end TGLExt
