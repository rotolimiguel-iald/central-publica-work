import RegularMaxwellWaveR2
import SchwartzMaxwellNonzeroR6

/-! A nonzero actual spacetime Maxwell wave from a nonnegative smooth
momentum bump. The witness is a Schwartz test, not a compact spacetime test. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Matrix SchwartzMap Set
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem waveDensity_tensor01 (f : SchwartzTensor) (b : Spacetime→ℂ)
    (hf : ∀p,f p=b p•tensorUnit01) (y : MomentumCoordinates) :
    waveDensity f 0 1 y=b (shellEmbedding y)*(transverseMass 0 y.1:ℂ)^2 := by
  unfold waveDensity
  rw [Fin.sum_univ_two]
  have h0 : cartesianStrength y 0 0 1=transverseMass 0 y.1 := rfl
  have h1 : cartesianStrength y 1 0 1=0 := rfl
  rw [h0,h1,tensor01_coefficient f b hf y]
  push_cast
  ring

theorem regularWave_zero_integral (f : SchwartzTensor) (μ ν : Fin 4) :
    regularWave f μ ν 0=∫ y,waveDensity f μ ν y ∂orbitalMeasure 0 := by
  simp only [regularWave,waveIntegrand,wavePhase,inner_zero_right,neg_zero,
    Complex.ofReal_zero,mul_zero,Complex.exp_zero,one_mul]

theorem exists_nonzero_regularWave : ∃f : SchwartzTensor,0<(regularWave f 0 1 0).re := by
  let y : MomentumCoordinates := (![1,0],0)
  obtain ⟨b,_,hbc,hbs,hb01,hb1⟩ := exists_contDiff_tsupport_subset
    (x:=shellEmbedding y) (n:=⊤) (s:=Set.univ) (Filter.univ_mem)
  let v : Spacetime→TensorValue := fun p=>(b p:ℂ)•tensorUnit01
  have hvC : HasCompactSupport v := hbc.of_isClosed_subset (isClosed_tsupport _) (by
    apply closure_mono
    intro p hp
    contrapose! hp
    simp only [Function.mem_support] at hp ⊢
    simp [v,hp])
  have hvD : ContDiff ℝ (⊤ : ℕ∞) v := by
    convert hbs.smul (contDiff_const (c:=tensorUnit01)) using 1
    funext p
    simp [v]
  let f : SchwartzTensor := hvC.toSchwartzMap hvD
  have hf : ∀p,f p=(b p:ℂ)•tensorUnit01 := fun _=>rfl
  have he : (fun z=>(waveDensity f 0 1 z).re)=
      fun z=>b (shellEmbedding z)*transverseMass 0 z.1^2 := by
    funext z
    rw [waveDensity_tensor01 f (fun p=>(b p:ℂ)) hf]
    norm_cast
  have hi : Integrable (fun z=>b (shellEmbedding z)*transverseMass 0 z.1^2)
      (orbitalMeasure 0) := by
    rw [← he]
    exact (waveDensity_integrable f 0 1).re
  have hc : Continuous (fun z : MomentumCoordinates=>b (shellEmbedding z)*transverseMass 0 z.1^2) :=
    (hbs.continuous.comp shellEmbedding_continuous).mul (by unfold transverseMass; fun_prop)
  have hn : 0≤fun z : MomentumCoordinates=>b (shellEmbedding z)*transverseMass 0 z.1^2 := by
    intro z
    exact mul_nonneg (hb01 (mem_range_self (shellEmbedding z))).1 (sq_nonneg _)
  have hneq : b (shellEmbedding y)*transverseMass 0 y.1^2≠0 := by
    simp [hb1,y,transverseMass]
  letI:=orbitalMeasure_openPos 0
  have hpos:=integral_pos_of_integrable_nonneg_nonzero hc hi hn hneq
  refine ⟨f,?_⟩
  have hr : (∫ y,(waveDensity f 0 1 y).re ∂orbitalMeasure 0)=
      (∫ y,waveDensity f 0 1 y ∂orbitalMeasure 0).re := by
    simpa only [RCLike.re_eq_complex_re] using integral_re (waveDensity_integrable f 0 1)
  rw [regularWave_zero_integral,← hr]
  simpa only [he] using hpos

theorem exists_nonzero_physicalWave : ∃f : SchwartzTensor,0<(physicalWave f 0 1 0).re := by
  obtain ⟨g,hg⟩:=exists_nonzero_regularWave
  obtain ⟨f,hf⟩:=physicalFourier_surjective g
  exact ⟨f,by simpa only [physicalWave,hf] using hg⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.waveDensity_tensor01
#print axioms F1Fecho.MaxwellGlobal.regularWave_zero_integral
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_regularWave
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_physicalWave
