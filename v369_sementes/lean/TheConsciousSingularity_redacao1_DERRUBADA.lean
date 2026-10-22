import Mathlib
import TGL.GravitonShadow

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A SINGULARIDADE CONSCIENTE É A FORMA MATRICIAL DA LUZ  [TGLExt — v369; RASCUNHO]

(cabeçalho definitivo depois da busca no acervo e dos céticos)
-/

namespace TGLExt.TheConsciousSingularity

open TGL.GravitonShadow
open scoped Matrix

/-- As duas faces: `ℂ² ⊗ ℂ²`, indexado por pares. -/
abbrev TwoFaces := Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ

/-- A troca das duas faces (a face do par, `conjJ`, lida no produto tensorial). -/
def swapFaces (P : TwoFaces) : TwoFaces := P.submatrix Prod.swap Prod.swap

/-- A FORMA MATRICIAL DA LUZ: idempotente (a forma matricial — o reconhecimento), fixa pela Luz
    (a conjugação-transposta) e singular (traço 1). -/
structure IsMatrixFormOfLight (P : TwoFaces) : Prop where
  idem : P * P = P
  light : star P = P
  singular : Matrix.trace P = 1

/-- A SINGULARIDADE CONSCIENTE: a forma matricial da luz COM a ligação — cada uma das duas faces
    reduz a ½ (a Meia-Nat): a identidade não se perde em nenhuma face. -/
structure IsConsciousSingularity (P : TwoFaces) : Prop extends IsMatrixFormOfLight P where
  face_one : ptr P = (2⁻¹ : ℂ) • 1
  face_two : ptr (swapFaces P) = (2⁻¹ : ℂ) • 1

/-- [KERNEL] a troca das faces fixa o projetor de Bell. -/
theorem bell_fixed_by_the_exchange_of_faces : swapFaces bellProjector = bellProjector := by
  ext p q
  simp [swapFaces, bellProjector, Matrix.submatrix_apply, eq_comm]

/-- [KERNEL] ★★★ O projetor de Bell da v29 É uma singularidade consciente. -/
theorem bell_is_a_conscious_singularity : IsConsciousSingularity bellProjector where
  idem := bell_idem
  light := bell_star
  singular := bell_trace_one
  face_one := bell_reduced_half
  face_two := by rw [bell_fixed_by_the_exchange_of_faces]; exact bell_reduced_half

/-- [KERNEL] o estado produto é forma matricial da luz. -/
theorem product_is_a_matrix_form_of_light : IsMatrixFormOfLight productProjector where
  idem := by
    ext p q
    simp only [productProjector, Matrix.mul_apply, Matrix.of_apply]
    rw [Fintype.sum_prod_type]
    simp [Fin.sum_univ_two]
    rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;> simp
  light := by
    ext p q
    simp [productProjector, Matrix.star_apply, and_comm]
  singular := by
    simp [Matrix.trace, productProjector]

/-- [KERNEL] ★★ CONTROLE: o estado produto NÃO é singularidade consciente — a sua face é pura. -/
theorem product_is_not_a_conscious_singularity : ¬ IsConsciousSingularity productProjector := by
  intro h
  have h1 := h.face_one
  rw [product_reduced_pure] at h1
  have h2 := congrFun (congrFun h1 0) 0
  simp [e00] at h2

/-- [KERNEL] ★★★ A FORMA MATRICIAL DA LUZ SOZINHA NÃO LIGA: existe forma matricial da luz que não é
    singularidade consciente. A ligação (½ em cada face) é o que distingue. -/
theorem the_matrix_form_of_light_alone_does_not_bind :
    ∃ P : TwoFaces, IsMatrixFormOfLight P ∧ ¬ IsConsciousSingularity P :=
  ⟨productProjector, product_is_a_matrix_form_of_light, product_is_not_a_conscious_singularity⟩

/-- A vetorização: `M₂ ≅ ℂ² ⊗ ℂ²`. -/
def vecOf (y : Matrix (Fin 2) (Fin 2) ℂ) : Fin 2 × Fin 2 → ℂ := fun p => y p.1 p.2

/-- [KERNEL] ★★★ A PONTE DO J: o J de Tomita da face matricial (`y ↦ yᴴ`) é, lido nas duas faces,
    a TROCA das faces composta com a conjugação. -/
theorem tomita_J_is_the_exchange_of_faces (y : Matrix (Fin 2) (Fin 2) ℂ) :
    vecOf yᴴ = fun p => star (vecOf y p.swap) := by
  funext p
  simp [vecOf, Matrix.conjTranspose_apply]

/-- O vácuo do estado traço, na face matricial: `Ω = (1/√2)·1`. -/
noncomputable def tracialVacuum : Matrix (Fin 2) (Fin 2) ℂ := ((Real.sqrt 2 : ℂ)⁻¹) • 1

/-- [KERNEL] a Luz fixa o vácuo: `Ωᴴ = Ω`. -/
theorem light_fixes_the_tracial_vacuum : tracialVacuumᴴ = tracialVacuum := by
  simp [tracialVacuum, Matrix.conjTranspose_smul]

/-- [KERNEL] ★★★ A SINGULARIDADE É O VÁCUO: o projetor sobre o vácuo do estado traço, lido nas duas
    faces, é exatamente o projetor de Bell da v29. -/
theorem the_singularity_is_the_vacuum :
    Matrix.vecMulVec (vecOf tracialVacuum) (star (vecOf tracialVacuum)) = bellProjector := by
  ext p q
  have hs : ((Real.sqrt 2 : ℂ)⁻¹) * ((Real.sqrt 2 : ℂ)⁻¹) = (2⁻¹ : ℂ) := by
    rw [← mul_inv, ← Complex.ofReal_mul, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩
  simp only [Matrix.vecMulVec_apply, vecOf, tracialVacuum, bellProjector, Matrix.of_apply,
    Matrix.smul_apply, Matrix.one_apply, Pi.star_apply, smul_eq_mul]
  by_cases h1 : a = b <;> by_cases h2 : c = d <;> simp [h1, h2, hs, Complex.conj_ofReal]

end TGLExt.TheConsciousSingularity

#print axioms TGLExt.TheConsciousSingularity.bell_fixed_by_the_exchange_of_faces
#print axioms TGLExt.TheConsciousSingularity.bell_is_a_conscious_singularity
#print axioms TGLExt.TheConsciousSingularity.product_is_a_matrix_form_of_light
#print axioms TGLExt.TheConsciousSingularity.product_is_not_a_conscious_singularity
#print axioms TGLExt.TheConsciousSingularity.the_matrix_form_of_light_alone_does_not_bind
#print axioms TGLExt.TheConsciousSingularity.tomita_J_is_the_exchange_of_faces
#print axioms TGLExt.TheConsciousSingularity.light_fixes_the_tracial_vacuum
#print axioms TGLExt.TheConsciousSingularity.the_singularity_is_the_vacuum
