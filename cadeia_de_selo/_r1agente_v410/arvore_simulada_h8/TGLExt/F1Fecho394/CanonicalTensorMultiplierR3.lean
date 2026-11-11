import TGLExt.F1Fecho394.CanonicalTensorBoostR3
import TGLExt.F1Fecho394.GammaGraphParametersR3
/-! Concrete scalar multiplication for bounded second quantization on the
unchanged canonical symmetric sectors. Tensor products, not scalar addition,
are transported. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
open MeasureTheory Filter UniformSpace
namespace F1Fecho.TensorCoordinates
open F1Rede.BosonicSectors TGLExt.ImportedSQ F1Rede.CanonicalWedge
open ChatgptAudit.Continuous049

def productWeight (w:ℝ→ℂ) : (n:ℕ)→(data n).Index→ℂ
  | 0 => w
  | n+1 => fun p=>w p.2*productWeight w n p.1

theorem productWeight_measurable (w:ℝ→ℂ) (hw:Measurable w) (n:ℕ) :
    Measurable (productWeight w n) := by
  induction n with
  | zero => exact hw
  | succ n ih => exact (hw.comp measurable_snd).mul (ih.comp measurable_fst)

theorem productWeight_bound (w:ℝ→ℂ) (hb:∀x,‖w x‖≤1) (n:ℕ) (p:(data n).Index) :
    ‖productWeight w n p‖≤1 := by
  induction n with
  | zero => exact hb p
  | succ n ih =>
    change ‖w p.2*productWeight w n p.1‖≤1
    rw [norm_mul]
    exact mul_le_one₀ (hb p.2) (norm_nonneg _) (ih p.1)

def productData (w:ℝ→ℂ) (hw:Measurable w) (hb:∀x,‖w x‖≤1) (n:ℕ) :
    ScalarL2.Data (data n).measure where
  value:=productWeight w n
  measurable:=(productWeight_measurable w hw n).aestronglyMeasurable
  bound:=1
  nonneg:=zero_le_one
  bounded:=productWeight_bound w hb n

def productMultiplier (w:ℝ→ℂ) (hw:Measurable w) (hb:∀x,‖w x‖≤1) (n:ℕ) :
    Space n→L[ℂ]Space n := ScalarL2.op _ (productData w hw hb n)

theorem productMultiplier_ae (w:ℝ→ℂ) (hw:Measurable w) (hb:∀x,‖w x‖≤1)
    (n:ℕ) (u:Space n) : productMultiplier w hw hb n u=ᵐ[(data n).measure]
      fun p=>productWeight w n p•u p := ScalarL2.op_ae _ _ _

variable (A:H1→L[ℂ]H1) (w:ℝ→ℂ) (hw:Measurable w) (hb:∀x,‖w x‖≤1)
  (hAw:∀f:H1,Phi (A f)=ᵐ[volume] fun x=>w x•Phi f x)

include hAw in
theorem profile_multiplier (n:ℕ) (f:H1) :
    profile n (A f)=productMultiplier w hw hb n (profile n f) := by
  induction n with
  | zero =>
    rw [profile_zero,profile_zero]
    apply Lp.ext
    filter_upwards [hAw f,productMultiplier_ae w hw hb 0 (Phi f)] with x hx hy
    exact hx.trans hy.symm
  | succ n ih =>
    have hi : profile n (A f)=ᵐ[(data n).measure]
        fun p=>productWeight w n p•profile n f p := by
      rw [ih]
      exact productMultiplier_ae w hw hb n (profile n f)
    apply Lp.ext
    filter_upwards [profile_succ_ae n (A f),profile_succ_ae n f,
      productMultiplier_ae w hw hb (n+1) (profile (n+1) f),
      Measure.quasiMeasurePreserving_fst.ae hi,Measure.quasiMeasurePreserving_snd.ae (hAw f)]
      with p hl hr hmul hi hf
    rw [hl,hmul,hr,hi,hf,pure_smul_pair]
    rfl

include hAw in
theorem sector_multiplier (n:ℕ) (x:Sector (n+1)) :
    coordinates n (BoundedGamma.sector A (n+1) x : TensorHilbert (n+1))=
      productMultiplier w hw hb n (coordinates n (x:TensorHilbert (n+1))) := by
  let L:TensorHilbert (n+1)→L[ℂ]Space n:=(coordinates n).toLinearIsometry.toContinuousLinearMap.comp
    (BoundedGamma.tensor A (n+1))
  let M:TensorHilbert (n+1)→L[ℂ]Space n:=(productMultiplier w hw hb n).comp
    (coordinates n).toLinearIsometry.toContinuousLinearMap
  have hbase : algebraicSymmetricSpan (n+1)≤(L-M).ker := by
    apply Submodule.span_le.mpr
    rintro _ ⟨f,rfl⟩
    change L (pureCompleted (n+1) f)-M (pureCompleted (n+1) f)=0
    apply sub_eq_zero.mpr
    change coordinates n (BoundedGamma.tensor A (n+1) (pureCompleted (n+1) f))=_
    rw [BoundedGamma.tensor_pure]
    exact profile_multiplier A w hw hb hAw n f
  have hx: (x:TensorHilbert (n+1))∈(L-M).ker:=
    (algebraicSymmetricSpan (n+1)).topologicalClosure_minimal hbase (L-M).isClosed_ker x.property
  exact sub_eq_zero.mp hx

def weightA (c x:ℝ) : ℂ := spectralWeightA c x
def weightB (c x:ℝ) : ℂ := spectralWeightB c x
lemma weightA_measurable (c:ℝ) : Measurable (weightA c) :=
  Complex.continuous_ofReal.measurable.comp (spectral_weightA_continuous c).measurable
lemma weightB_measurable (c:ℝ) : Measurable (weightB c) :=
  Complex.continuous_ofReal.measurable.comp (spectral_weightB_continuous c).measurable
lemma weightA_bound (c x:ℝ) : ‖weightA c x‖≤1 := by
  simpa only [weightA,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (spectral_weightA_pos c x)]
    using spectral_weightA_le_one c x
lemma weightB_bound (c x:ℝ) : ‖weightB c x‖≤1 := by
  simpa only [weightB,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (spectral_weightB_pos c x)]
    using spectral_weightB_le_one c x

theorem sector_WA (c:ℝ) (n:ℕ) (x:Sector (n+1)) :
    coordinates n (BoundedGamma.sector (WA c) (n+1) x : TensorHilbert (n+1))=
      productMultiplier (weightA c) (weightA_measurable c) (weightA_bound c) n
        (coordinates n (x:TensorHilbert (n+1))) := by
  apply sector_multiplier
  intro f
  change Phi (pull (F1Rede.Wedge.A c) f)=ᵐ[volume] _
  rw [Phi_pull]
  exact F1Rede.Wedge.A_ae c (Phi f)

theorem sector_WB (c:ℝ) (n:ℕ) (x:Sector (n+1)) :
    coordinates n (BoundedGamma.sector (WB c) (n+1) x : TensorHilbert (n+1))=
      productMultiplier (weightB c) (weightB_measurable c) (weightB_bound c) n
        (coordinates n (x:TensorHilbert (n+1))) := by
  apply sector_multiplier
  intro f
  change Phi (pull (F1Rede.Wedge.B c) f)=ᵐ[volume] _
  rw [Phi_pull]
  exact F1Rede.Wedge.B_ae c (Phi f)

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.sector_multiplier
#print axioms F1Fecho.TensorCoordinates.sector_WA
#print axioms F1Fecho.TensorCoordinates.sector_WB
