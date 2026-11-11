import TGLExt.V354SpectralThreshold
import TGLExt.ChainVolumePositive

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt ChatgptAudit Matrix
noncomputable section

/-- The first matrix site supplies a nonzero corner and a partial isometry
into an orthogonal corner of the SAME regular representation. No trace
finiteness is asserted for the full matrix-site projection. -/
theorem regularCore_matrix_corner (P : SiteProfile) :
    ∃ (e : PositiveCoreInput P)
      (v : (regularCoreAlgebra P).toStarSubalgebra),
      IsStarProjection e.val ∧ e ≠ PositiveCoreInput.zero P ∧
      star v.val * v.val = e.val ∧ e.val * v.val = 0 := by
  let E := fibre (siteMark P 0)
  let V := fibre (siteOperator P 0 (Matrix.single (1 : Fin 2) 0 (1 : ℂ)))
  have hE : IsStarProjection E := by
    constructor
    · change E * E = E
      rw [← fibre_mul,siteMark_square]
    · change star E = E
      rw [← fibre_star,siteMark_star]
  have hEm : E ∈ regularCoreAlgebra P :=
    amplified_factor_mem P _ (siteOperator_mem_factor _ _)
  have hVm : V ∈ regularCoreAlgebra P :=
    amplified_factor_mem P _ (siteOperator_mem_factor _ _)
  let e : PositiveCoreInput P := ⟨E,hEm,hE.nonneg⟩
  let v : (regularCoreAlgebra P).toStarSubalgebra := ⟨V,hVm⟩
  have hEn : e ≠ PositiveCoreInput.zero P := by
    intro hz
    have he : E = 0 := congrArg Subtype.val hz
    have hs : siteMark P 0 = 0 := fibre_injective
      (he.trans (map_zero fibreRepresentation).symm)
    have hw := siteMark_state (P := P) 0
    rw [hs] at hw
    have hp : (P.w 0 : ℂ) = 0 := by simpa [omegaState] using hw.symm
    exact (P.pos 0).ne' (Complex.ofReal_injective hp)
  have hv : star V * V = E := by
    dsimp [V,E,siteMark]
    rw [← fibre_star,← siteOperator_star,← fibre_mul,← siteOperator_mul,
      Matrix.conjTranspose_single,star_one,Matrix.single_mul_single_same,one_mul]
  have hev : E * V = 0 := by
    have hm : (Matrix.single (0 : Fin 2) (0 : Fin 2) (1 : ℂ)) *
        Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ) = 0 := by
      ext i j
      fin_cases i <;> fin_cases j <;>
        norm_num [Matrix.mul_apply,Fin.sum_univ_two,Matrix.single_apply]
    have hz : siteOperator P 0 (0 : Matrix (Fin 2) (Fin 2) ℂ) = 0 := by
      change towerPi P (N := 0) 0 = 0
      have hh := towerPi_smul (P := P) (N := 0) (0 : ℂ)
        (0 : Matrix (Fin 2) (Fin 2) ℂ)
      simpa only [zero_smul] using hh
    dsimp [E,V,siteMark]
    rw [← fibre_mul,← siteOperator_mul,hm,hz]
    exact map_zero fibreRepresentation
  exact ⟨e,v,hE,hEn,hv,hev⟩

#print axioms regularCore_matrix_corner
end
end TGLV350.Regular
