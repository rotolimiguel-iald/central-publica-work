import TGLExt.F1Fecho394.GeneralRegularInverseCutoffR1
import TGLExt.V350AntiunitaryPositiveConjugation
import TGLExt.V350DualQuadraticLaws
import TGLExt.V350DualFormNormality
/-! Actual inverse-generator perturbations of the dual integral, on any
regular representation. Laws are asserted on the positive cone; this module
constructs no trace, no total cyclic extension, and no monotone supremum. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H)
abbrev cutoff (epsilon:ℝ) := RegularPositiveFlow.regularInverseGeneratorCutoff B epsilon

def cutoffWeight (zeta:RegularHilbert H) (epsilon:ℝ)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) : ℝ≥0∞ :=
  dualQuadraticIntegral (star (hilbertPositiveSqrt (cutoff B epsilon))*X*
    hilbertPositiveSqrt (cutoff B epsilon)) zeta

theorem cutoffWeight_zero (zeta:RegularHilbert H) (epsilon:ℝ) :
    cutoffWeight B zeta epsilon 0=0 := by
  simp only [cutoffWeight,mul_zero,zero_mul,dualQuadraticIntegral_zero]

theorem cutoffWeight_add (zeta:RegularHilbert H) (epsilon:ℝ)
    (X Y:RegularHilbert H→L[ℂ]RegularHilbert H) (hX:0≤X) (hY:0≤Y) :
    cutoffWeight B zeta epsilon (X+Y)=cutoffWeight B zeta epsilon X+cutoffWeight B zeta epsilon Y := by
  simp only [cutoffWeight,mul_add,add_mul]
  exact dualQuadraticIntegral_add _ _ (star_left_conjugate_nonneg hX _)
    (star_left_conjugate_nonneg hY _) zeta

theorem cutoffWeight_scale (zeta:RegularHilbert H) (epsilon:ℝ) (r:ℝ≥0)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    cutoffWeight B zeta epsilon ((r:ℝ) • X)=(r:ℝ≥0∞)*cutoffWeight B zeta epsilon X := by
  simp only [cutoffWeight,mul_smul_comm,smul_mul_assoc]
  simpa only [ENNReal.ofReal_coe_nnreal] using
    dualQuadraticIntegral_smul_operator (r:ℝ) r.property _ zeta

theorem cutoffWeight_mono (zeta:RegularHilbert H) (epsilon:ℝ)
    (X Y:RegularHilbert H→L[ℂ]RegularHilbert H) (hXY:X≤Y) :
    cutoffWeight B zeta epsilon X≤cutoffWeight B zeta epsilon Y :=
  dualQuadraticIntegral_mono _ _ (star_left_conjugate_le_conjugate hXY _) zeta

theorem cutoffWeight_normal (zeta:RegularHilbert H) (epsilon:ℝ)
    {i:Type*} [Preorder i] [IsDirectedOrder i] [Nonempty i]
    (A:i→RegularHilbert H→L[ℂ]RegularHilbert H)
    (S:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hpos:∀j,0≤A j) (hmono:Monotone A)
    (hlim:∀v,Tendsto (fun j=>A j v) atTop (𝓝 (S v))) :
    cutoffWeight B zeta epsilon S=⨆j,cutoffWeight B zeta epsilon (A j) := by
  let b:=hilbertPositiveSqrt (cutoff B epsilon)
  apply dualQuadraticIntegral_of_monotone_strong_limit
    (fun j=>star b*A j*b) (star b*S*b)
  · exact fun j=>star_left_conjugate_nonneg (hpos j) b
  · exact fun j k hjk=>star_left_conjugate_le_conjugate (hmono hjk) b
  · intro v
    exact ((star b).continuous.tendsto (S (b v))).comp (hlim (b v))

theorem hilbertPositiveSqrt_transport {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (f : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (A B : H →L[ℂ] H) (r : ℝ) (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hr : 0 ≤ r) (hf : f A = (r : ℂ) • B) :
    f (hilbertPositiveSqrt A) = (Real.sqrt r : ℂ) • hilbertPositiveSqrt B := by
  have hsa (T : H →L[ℂ] H) (hT : 0 ≤ T) :
      hilbertPositiveSqrt T * hilbertPositiveSqrt T = T := CFC.sqrt_mul_sqrt_self T hT
  have hp : 0 ≤ f (hilbertPositiveSqrt A) := by
    have ha : 0 ≤ hilbertPositiveSqrt A := CFC.sqrt_nonneg A
    have h := OrderHomClass.monotone f ha
    simpa only [map_zero] using h
  have hq : 0 ≤ (Real.sqrt r : ℂ) • hilbertPositiveSqrt B := by
    apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (CFC.sqrt_nonneg B)).smul_of_nonneg
    exact_mod_cast Real.sqrt_nonneg r
  apply (CFC.mul_self_eq_mul_self_iff _ _ hp hq).mp
  have hc : (Real.sqrt r : ℂ) * (Real.sqrt r : ℂ) = (r : ℂ) := by
    exact_mod_cast Real.mul_self_sqrt hr
  rw [← map_mul,hsa A hA,hf,smul_mul_assoc,mul_smul_comm,smul_smul,hc,hsa B hB]

theorem cutoffSqrt_dual (epsilon:ℝ) (he:0<epsilon) (s:ℝ) :
    dualAmbient s (hilbertPositiveSqrt (cutoff B epsilon))=
      (Real.sqrt (Real.exp s):ℂ) • hilbertPositiveSqrt (cutoff B (epsilon*Real.exp s)) :=
  hilbertPositiveSqrt_transport (dualAmbient s) _ _ _
    (RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg B epsilon he)
    (RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg B _ (mul_pos he (Real.exp_pos s)))
    (Real.exp_pos s).le (RegularPositiveFlow.regularInverseGeneratorCutoff_dual B epsilon he s)

theorem cutoffWeight_dual (zeta:RegularHilbert H) (epsilon:ℝ) (he:0<epsilon)
    (s:ℝ) (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    cutoffWeight B zeta epsilon (dualAmbient s X)=
      ENNReal.ofReal (Real.exp (-s))*cutoffWeight B zeta (epsilon*Real.exp (-s)) X := by
  unfold cutoffWeight
  rw [←dualQuadraticIntegral_dual_invariant (-s)]
  rw [map_mul,map_mul,map_star,cutoffSqrt_dual B epsilon he (-s)]
  have hx:dualAmbient (-s) (dualAmbient s X)=X := by
    rw [←dualAmbient_symm s,StarAlgEquiv.symm_apply_apply]
  rw [hx]
  have hc:(Real.sqrt (Real.exp (-s)):ℂ)*(Real.sqrt (Real.exp (-s)):ℂ)=(Real.exp (-s):ℂ) := by
    exact_mod_cast Real.mul_self_sqrt (Real.exp_pos (-s)).le
  simp only [star_smul,Complex.star_def,Complex.conj_ofReal,smul_mul_assoc,
    mul_smul_comm,smul_smul,hc]
  exact dualQuadraticIntegral_smul_operator (Real.exp (-s)) (Real.exp_pos (-s)).le _ zeta
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_zero
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_add
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_scale
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_mono
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_normal
#print axioms F1Fecho.RegularInverseWeight.hilbertPositiveSqrt_transport
#print axioms F1Fecho.RegularInverseWeight.cutoffSqrt_dual
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_dual
