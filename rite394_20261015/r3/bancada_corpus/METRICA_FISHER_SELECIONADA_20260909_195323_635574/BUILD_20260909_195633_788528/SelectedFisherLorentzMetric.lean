import TGLExt.FisherInformationTensor
import TGLExt.GeneralAngularTensorCodec
import TGLExt.GeneralMetricEinstein
import Mathlib.Analysis.Matrix.Order

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.SelectedFisher
open Matrix TGLExt ChatgptAudit ChatgptAudit.FisherField
open ChatgptAudit.Coherent023 ChatgptAudit.AngularTensorCodec
open ChatgptAudit.GeneralMetric
open scoped MatrixOrder ContDiff
noncomputable section

/-- A signed reading of a positive information tensor, with a selected covector. -/
def reflectedMetric (F : Tensor4) (c : Coordinate4) : Tensor4 :=
  (2 / tensorQuad F⁻¹ c) • vecMulVec c c - F

def reflectedInverse (F : Tensor4) (c : Coordinate4) : Tensor4 :=
  (2 / tensorQuad F⁻¹ c) • vecMulVec (F⁻¹ *ᵥ c) (F⁻¹ *ᵥ c) - F⁻¹

theorem positive_gram_factor (F : Tensor4) (hF : F.PosDef) :
    ∃ B : Tensor4, IsUnit B.det ∧ Bᵀ * B = F := by
  obtain ⟨B, hB⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hF.posSemidef.nonneg
  have hb : Bᵀ * B = F := by simpa using hB.symm
  refine ⟨B, ?_, hb⟩
  apply isUnit_iff_ne_zero.mpr
  intro hz
  have hh := congrArg Matrix.det hb
  rw [Matrix.det_mul, Matrix.det_transpose, hz, zero_mul] at hh
  exact (ne_of_gt hF.det_pos) hh.symm

/-- An explicit orthogonal reflection whose first row is a prescribed unit vector. -/
theorem unit_vector_frame (z : Coordinate4) (hz : z ⬝ᵥ z = 1) :
    ∃ Q : Tensor4, Qᵀ * Q = 1 ∧ Q 0 = z := by
  let e : Coordinate4 := Pi.single 0 1
  let w : Coordinate4 := e-z
  have hez : e ⬝ᵥ z = z 0 := by simp [e, dotProduct]
  have hze : z ⬝ᵥ e = z 0 := by simp [e, dotProduct]
  have hee : e ⬝ᵥ e = 1 := by simp [e, dotProduct]
  have hw : w ⬝ᵥ w = 2*(1-z 0) := by
    dsimp [w]
    rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hee, hez, hze, hz]
    ring
  by_cases hzero : 1-z 0=0
  · have hww : w ⬝ᵥ w=0 := by rw [hw,hzero,mul_zero]
    have hw0 : w=0 := dotProduct_self_eq_zero.mp hww
    have he : e=z := sub_eq_zero.mp hw0
    refine ⟨1, by simp, ?_⟩
    rw [←he]
    ext j
    simp [e, Matrix.one_apply, Pi.single_apply, eq_comm]
  · let k : ℝ := 1/(1-z 0)
    let W : Tensor4 := vecMulVec w w
    let Q : Tensor4 := 1-k • W
    have hWW : W*W=(w ⬝ᵥ w) • W := by
      simp [W, Matrix.vecMulVec_mul_vecMulVec, Matrix.smul_vecMulVec]
    have hWT : Wᵀ=W := Matrix.transpose_vecMulVec _ _
    have hQT : Qᵀ=Q := by simp [Q,hWT]
    have hQ : Qᵀ*Q=1 := by
      rw [hQT]
      dsimp [Q]
      rw [sub_mul, mul_sub, mul_sub, one_mul, mul_one, one_mul,
        Matrix.smul_mul, Matrix.mul_smul, hWW, smul_smul, smul_smul]
      have hk : k*(k*(w ⬝ᵥ w))=k+k := by rw [hw]; dsimp [k]; field_simp; ring
      rw [hk, add_smul]
      abel
    refine ⟨Q,hQ,?_⟩
    ext j
    have hw0 : w 0=1-z 0 := by simp [w,e]
    change (1:Tensor4) 0 j-k*(w 0*w j)=z j
    rw [hw0]
    dsimp [k,w,e]
    simp only [Pi.sub_apply, Matrix.one_apply, Pi.single_apply]
    field_simp
    split_ifs <;> simp_all <;> ring

theorem eta_congruence_by_first_row (E : Tensor4) :
    Eᵀ * eta4 * E = (2:ℝ) • vecMulVec (E 0) (E 0) - Eᵀ*E := by
  ext i j
  norm_num [Matrix.mul_apply, Matrix.transpose_apply, eta4, Fin.sum_univ_four,
    Matrix.vecMulVec, Matrix.sub_apply, Matrix.smul_apply]
  ring

theorem reflected_metric_symmetric (F : Tensor4) (c : Coordinate4) (hF : Fᵀ=F) :
    (reflectedMetric F c)ᵀ=reflectedMetric F c := by
  simp [reflectedMetric, Matrix.transpose_vecMulVec, hF]

theorem clock_norm_positive (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : 0<tensorQuad F⁻¹ c := by
  simpa only [tensorQuad, star_trivial] using hF.inv.dotProduct_mulVec_pos hc

theorem reflected_metric_lorentz (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : LorentzByCongruence (reflectedMetric F c) := by
  obtain ⟨B,hB,hBF⟩ := positive_gram_factor F hF
  let D := B⁻¹
  have hDB : D*B=1 := Matrix.nonsing_inv_mul B hB
  have hBD : B*D=1 := Matrix.mul_nonsing_inv B hB
  have hi : F⁻¹=D*Dᵀ := by rw [←hBF, Matrix.mul_inv_rev, Matrix.transpose_nonsing_inv]; rfl
  let w : Coordinate4 := Dᵀ*ᵥc
  have hcB : Bᵀ*ᵥw=c := by
    dsimp [w]
    rw [Matrix.mulVec_mulVec, ←Matrix.transpose_mul, hDB, Matrix.transpose_one, Matrix.one_mulVec]
  let a : ℝ := tensorQuad F⁻¹ c
  have ha : 0<a := clock_norm_positive F hF c hc
  have hw : w ⬝ᵥ w=a := by
    dsimp [a,tensorQuad,w]
    rw [hi, ←Matrix.mulVec_mulVec, dotProduct_mulVec, ←Matrix.mulVec_transpose]
  let z : Coordinate4 := (Real.sqrt a)⁻¹ • w
  have hs : Real.sqrt a≠0 := ne_of_gt (Real.sqrt_pos.2 ha)
  have hz : z ⬝ᵥ z=1 := by
    dsimp [z]
    rw [smul_dotProduct, dotProduct_smul, hw]
    simp only [smul_eq_mul]
    field_simp
    exact (Real.sq_sqrt ha.le).symm
  obtain ⟨Q,hQ,hQ0⟩ := unit_vector_frame z hz
  let E := Q*B
  have hEE : Eᵀ*E=F := by
    dsimp [E]
    rw [Matrix.transpose_mul]
    calc Bᵀ*Qᵀ*(Q*B)=Bᵀ*(Qᵀ*Q)*B := by noncomm_ring
         _ = F := by rw [hQ,mul_one,hBF]
  have hE0 : E 0=(Real.sqrt a)⁻¹ • c := by
    ext j
    have hh := congrFun hcB j
    change (∑ k, Q 0 k*B k j)=(Real.sqrt a)⁻¹*c j
    rw [hQ0]
    dsimp [z]
    simp only [Pi.smul_apply, smul_eq_mul, ←Finset.mul_sum]
    congr 1
    simpa [Matrix.mulVec, dotProduct, Matrix.transpose_apply, mul_comm] using hh
  have hEd : IsUnit E.det := by
    apply isUnit_iff_ne_zero.mpr
    intro hzE
    have hh := congrArg Matrix.det hEE
    rw [Matrix.det_mul, Matrix.det_transpose, hzE, zero_mul] at hh
    exact (ne_of_gt hF.det_pos) hh.symm
  refine ⟨E,hEd,?_⟩
  rw [eta_congruence_by_first_row,hEE,hE0]
  ext i j
  simp only [reflectedMetric, Matrix.sub_apply, Matrix.smul_apply,
    Matrix.vecMulVec, Matrix.of_apply, Pi.smul_apply, smul_eq_mul]
  change 2/(a)*(c i*c j)-F i j=2*((Real.sqrt a)⁻¹*c i*((Real.sqrt a)⁻¹*c j))-F i j
  congr 1
  field_simp
  nlinarith [Real.sq_sqrt ha.le]

#print axioms reflectedMetric
#print axioms reflectedInverse
#print axioms positive_gram_factor
#print axioms unit_vector_frame
#print axioms eta_congruence_by_first_row
#print axioms reflected_metric_symmetric
#print axioms clock_norm_positive
#print axioms reflected_metric_lorentz
end
end ChatgptAudit.SelectedFisher
