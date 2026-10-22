import TGLExt.F1Fecho394.CanonicalTensorCoordinatesR4
import TGLExt.F1Fecho394.ScalarL2MultiplierR3
/-! The already constructed boost on the same symmetric sectors becomes
multiplication by a phase of the sum of all rapidity Fourier coordinates.
This proves the unitary-group transport, not yet the unbounded graph identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
open MeasureTheory Filter UniformSpace
open scoped TensorProduct
namespace F1Fecho.TensorCoordinates
open F1Rede.BosonicSectors F1Rede.BosonicTwoParticle TGLExt.ImportedSQ
open F1Rede.CanonicalWedge F1Rede.Canonical TGLV350.Regular

def rapiditySum : (n:ℕ)→(data n).Index→ℝ
  | 0 => id
  | n+1 => fun p=>p.2+rapiditySum n p.1

theorem rapiditySum_measurable (n:ℕ) : Measurable (rapiditySum n) := by
  induction n with
  | zero => exact measurable_id
  | succ n ih => exact measurable_snd.add (ih.comp measurable_fst)

def boostData (n:ℕ) (s:ℝ) : ScalarL2.Data (data n).measure where
  value x:=characterPhase (2*Real.pi*s) (rapiditySum n x)
  measurable := ((by unfold characterPhase; fun_prop : Continuous (characterPhase (2*Real.pi*s))).measurable.comp
    (rapiditySum_measurable n)).aestronglyMeasurable
  bound:=1
  nonneg:=zero_le_one
  bounded x:=le_of_eq (characterPhase_norm _ _)

def spectralBoost (n:ℕ) (s:ℝ) : Space n→L[ℂ]Space n := ScalarL2.op _ (boostData n s)

theorem spectralBoost_ae (n:ℕ) (s:ℝ) (u:Space n) :
    spectralBoost n s u=ᵐ[(data n).measure]
      fun p=>characterPhase (2*Real.pi*s) (rapiditySum n p)•u p := ScalarL2.op_ae _ _ _

def profile (n:ℕ) (f:H1) : Space n := coordinates n (pureCompleted (n+1) f)

theorem profile_zero (f:H1) : profile 0 f=Phi f := first_pure f

theorem profile_succ_ae (n:ℕ) (f:H1) : profile (n+1) f=ᵐ[(data (n+1)).measure]
    fun p=>CompletedTensor.pure (Phi f p.2,profile n f p.1) :=
  coordinates_succ_ae n f (pureAlgebraic f (n+1))

lemma phase_x_add (s x y:ℝ) : characterPhase s (x+y)=characterPhase s x*characterPhase s y := by
  unfold characterPhase
  rw [←Complex.exp_add]
  congr 1
  push_cast
  ring

lemma pure_smul_pair {E F:Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [NormedAddCommGroup F] [InnerProductSpace ℂ F] (a b:ℂ) (x:E) (y:F) :
    CompletedTensor.pure (a•x,b•y)=(a*b)•CompletedTensor.pure (x,y) := by
  change (Completion.toComplL : (E⊗[ℂ]F)→L[ℂ]CompletedTensor.CT E F)
    (CompletedTensor.bilinear (a•x) (b•y))=_
  simp only [map_smul,ContinuousLinearMap.smul_apply,smul_smul]
  rw [mul_comm b a]
  rfl

theorem profile_boost (n:ℕ) (s:ℝ) (f:H1) :
    profile n (B0 s f)=spectralBoost n s (profile n f) := by
  induction n with
  | zero =>
    rw [profile_zero,profile_zero,canonicalPartialFourier_boost]
    apply Lp.ext
    filter_upwards [characterMultiplier_ae (2*Real.pi*s) (Phi f),spectralBoost_ae 0 s (Phi f)] with x hx hy
    exact hx.trans hy.symm
  | succ n ih =>
    have hi : profile n (B0 s f)=ᵐ[(data n).measure]
        fun p=>characterPhase (2*Real.pi*s) (rapiditySum n p)•profile n f p := by
      rw [ih]
      exact spectralBoost_ae n s (profile n f)
    have hf : Phi (B0 s f)=ᵐ[volume] fun x=>characterPhase (2*Real.pi*s) x•Phi f x := by
      rw [canonicalPartialFourier_boost]
      exact characterMultiplier_ae _ _
    apply Lp.ext
    filter_upwards [profile_succ_ae n (B0 s f),profile_succ_ae n f,
      spectralBoost_ae (n+1) s (profile (n+1) f),
      Measure.quasiMeasurePreserving_fst.ae hi,Measure.quasiMeasurePreserving_snd.ae hf]
      with p hl hr hb hi hf
    rw [hl,hb,hr,hi,hf,pure_smul_pair]
    congr 1
    exact (phase_x_add _ _ _).symm

theorem sector_boost (n:ℕ) (s:ℝ) (x:Sector (n+1)) :
    coordinates n (gammaSector (B0 s) (n+1) x : TensorHilbert (n+1))=
      spectralBoost n s (coordinates n (x:TensorHilbert (n+1))) := by
  let L:TensorHilbert (n+1)→L[ℂ]Space n:=(coordinates n).toLinearIsometry.toContinuousLinearMap.comp
    (tensorGamma (B0 s) (n+1)).toLinearIsometry.toContinuousLinearMap
  let M:TensorHilbert (n+1)→L[ℂ]Space n:=(spectralBoost n s).comp (coordinates n).toLinearIsometry.toContinuousLinearMap
  have hb : algebraicSymmetricSpan (n+1)≤(L-M).ker := by
    apply Submodule.span_le.mpr
    rintro _ ⟨f,rfl⟩
    change L (pureCompleted (n+1) f)-M (pureCompleted (n+1) f)=0
    apply sub_eq_zero.mpr
    change coordinates n (tensorGamma (B0 s) (n+1) (pureCompleted (n+1) f))=_
    rw [tensorGamma_pure]
    exact profile_boost n s f
  have hx: (x:TensorHilbert (n+1))∈(L-M).ker:=
    (algebraicSymmetricSpan (n+1)).topologicalClosure_minimal hb (L-M).isClosed_ker x.property
  exact sub_eq_zero.mp hx

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.profile_boost
#print axioms F1Fecho.TensorCoordinates.sector_boost
