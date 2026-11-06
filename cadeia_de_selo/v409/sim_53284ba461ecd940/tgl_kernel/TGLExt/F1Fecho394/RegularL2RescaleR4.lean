import TGLExt.V350FourierL1L2
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 900000
noncomputable section
namespace F1Fecho.RegularL2Rescale
open MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
abbrev LH := Lp (α := ℝ) H 2 volume

theorem div_qmp (c : ℝ) (hc : 0 < c) :
    Measure.QuasiMeasurePreserving (fun x : ℝ => x / c) volume volume := by
  simpa only [smul_eq_mul,div_eq_mul_inv,mul_comm] using
    (Measure.quasiMeasurePreserving_smul (volume : Measure ℝ) (inv_ne_zero hc.ne'))

theorem rescale_memLp (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) :
    MemLp (fun x : ℝ => ((Real.sqrt c)⁻¹ : ℝ) • f (x/c)) 2 volume := by
  have hm := (Lp.memLp f).1.comp_quasiMeasurePreserving (div_qmp c hc)
  have hi := ((memLp_two_iff_integrable_sq_norm (Lp.memLp f).1).mp (Lp.memLp f)).comp_div hc.ne'
  exact ((memLp_two_iff_integrable_sq_norm hm).mpr hi).const_smul ((Real.sqrt c)⁻¹ : ℝ)

def rescale (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) : LH (H:=H) :=
  (rescale_memLp c hc f).toLp (fun x : ℝ => ((Real.sqrt c)⁻¹ : ℝ) • f (x/c))

theorem rescale_ae (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) :
    rescale c hc f =ᵐ[volume] fun x : ℝ => ((Real.sqrt c)⁻¹ : ℝ) • f (x/c) :=
  (rescale_memLp c hc f).coeFn_toLp

theorem rescale_norm_sq (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) :
    ‖rescale c hc f‖^2 = ‖f‖^2 := by
  rw [← TGLV350.Fourier.L2_integral_norm_sq,← TGLV350.Fourier.L2_integral_norm_sq]
  calc
    (∫ x : ℝ, ‖rescale c hc f x‖^2) =
        (Real.sqrt c)⁻¹^2 * (∫ x : ℝ, ‖f (x/c)‖^2) := by
      rw [← integral_const_mul]
      apply integral_congr_ae
      filter_upwards [rescale_ae c hc f] with x hx
      rw [hx,norm_smul,mul_pow,Real.norm_eq_abs,sq_abs]
    _ = _ := by
      have hd := Measure.integral_comp_div (fun x : ℝ => ‖f x‖^2) c
      rw [hd,abs_of_pos hc,smul_eq_mul]
      have hs : (Real.sqrt c)^2 = c := Real.sq_sqrt hc.le
      have hn : Real.sqrt c ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hc)
      field_simp
      rw [hs]

theorem rescale_norm (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) :
    ‖rescale c hc f‖ = ‖f‖ := by
  nlinarith [rescale_norm_sq c hc f,norm_nonneg (rescale c hc f),norm_nonneg f]

def rescaleIsometry (c : ℝ) (hc : 0 < c) : LH (H:=H) →ₗᵢ[ℂ] LH (H:=H) where
  toFun := rescale c hc
  map_add' f g := by
    apply Lp.ext
    filter_upwards [rescale_ae c hc (f+g),rescale_ae c hc f,rescale_ae c hc g,
      Lp.coeFn_add (rescale c hc f) (rescale c hc g),
      (div_qmp c hc).ae (Lp.coeFn_add f g)] with x h1 h2 h3 h4 h5
    simp only [Pi.add_apply] at h4 h5
    rw [h1,h4,h2,h3,h5,smul_add]
  map_smul' z f := by
    apply Lp.ext
    filter_upwards [rescale_ae c hc (z • f),rescale_ae c hc f,
      Lp.coeFn_smul z (rescale c hc f),(div_qmp c hc).ae (Lp.coeFn_smul z f)] with x h1 h2 h3 h4
    simp only [Pi.smul_apply] at h3 h4
    simp only [RingHom.id_apply]
    rw [h1,h3,h2,h4,smul_comm]
  norm_map' := rescale_norm c hc

theorem rescale_inverse (c : ℝ) (hc : 0 < c) (f : LH (H:=H)) :
    rescale c hc (rescale c⁻¹ (inv_pos.2 hc) f) = f := by
  apply Lp.ext
  filter_upwards [rescale_ae c hc (rescale c⁻¹ (inv_pos.2 hc) f),
    (div_qmp c hc).ae (rescale_ae c⁻¹ (inv_pos.2 hc) f)] with x h1 h2
  rw [h1,h2,smul_smul]
  have hm : (Real.sqrt c)⁻¹ * (Real.sqrt c⁻¹)⁻¹ = 1 := by
    rw [Real.sqrt_inv,inv_inv,inv_mul_cancel₀ (ne_of_gt (Real.sqrt_pos.2 hc))]
  rw [hm,one_smul]
  congr 1
  field_simp

def rescaleEquiv (c : ℝ) (hc : 0 < c) : LH (H:=H) ≃ₗᵢ[ℂ] LH (H:=H) where
  toFun := rescale c hc
  map_add' := (rescaleIsometry c hc).map_add
  map_smul' := (rescaleIsometry c hc).map_smul
  norm_map' := rescale_norm c hc
  invFun := rescale c⁻¹ (inv_pos.2 hc)
  left_inv f := by
    simpa only [inv_inv] using rescale_inverse c⁻¹ (inv_pos.2 hc) f
  right_inv := rescale_inverse c hc

end F1Fecho.RegularL2Rescale
#print axioms F1Fecho.RegularL2Rescale.div_qmp
#print axioms F1Fecho.RegularL2Rescale.rescale_memLp
#print axioms F1Fecho.RegularL2Rescale.rescale_ae
#print axioms F1Fecho.RegularL2Rescale.rescale_norm_sq
#print axioms F1Fecho.RegularL2Rescale.rescale_norm
#print axioms F1Fecho.RegularL2Rescale.rescaleIsometry

#print axioms F1Fecho.RegularL2Rescale.rescale_inverse
#print axioms F1Fecho.RegularL2Rescale.rescaleEquiv
