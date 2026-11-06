import TGLExt.F1Fecho394.MaxwellSmearingLinearR2

/-! The divergence equation survives the actual compact tensor-to-H1 map.
The lower momentum contracts the upper on-shell bivector. This is the
Fourier-side free Maxwell equation on the regular compact momentum domain;
it does not assert spacetime-local support or a stress tensor. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellSmearing
open MeasureTheory Matrix Filter
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open TGLExt.ImportedSQ F1Fecho.MaxwellOnShell
open scoped CompactlySupported

theorem momentum_continuous : Continuous momentum := by
  unfold momentum
  exact continuous_pi (fun i => Complex.continuous_ofReal.comp
    ((continuous_apply i).comp ((shellMomentum_continuous 0).comp (rapidityChart_continuous 0))))

def lowerMomentum (y : MomentumCoordinates) (μ : Fin 4) : ℂ :=
  if μ=0 then momentum y μ else -momentum y μ

theorem lowerMomentum_continuous (μ : Fin 4) : Continuous (fun y => lowerMomentum y μ) := by
  unfold lowerMomentum
  split_ifs
  · exact (continuous_apply μ).comp momentum_continuous
  · exact ((continuous_apply μ).comp momentum_continuous).neg

theorem real_screen_source_free (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (ν : Fin 4) :
    ∑ μ,lowerMomentum y μ*strength (momentum y) (realLift (screen y j)) μ ν=0 := by
  have ht : pairing (momentum y) (realLift (screen y j))=0 := by
    have hr := screen_transverse y hy j
    rw [orbitPairing_symm] at hr
    simpa [pairing,momentum,realLift,orbitPairing] using congrArg Complex.ofReal hr
  have he := strength_source_free _ _ (momentum_null y hy) ht ν
  have h20 : (2:Fin 4)≠0 := by decide
  have h30 : (3:Fin 4)≠0 := by decide
  simpa [pairing,lowerMomentum,Fin.sum_univ_four,h20,h30,sub_eq_add_neg] using he

def divergenceTest (b : C_c(MomentumCoordinates,ℂ)) (ν : Fin 4) : TestTensor where
  toFun := fun y μ ρ => (if ρ=ν then 1 else 0)*lowerMomentum y μ*b y
  continuous_toFun := continuous_pi (fun μ => continuous_pi (fun ρ =>
    (continuous_const.mul (lowerMomentum_continuous μ)).mul b.continuous))
  hasCompactSupport' := b.hasCompactSupport.of_isClosed_subset (isClosed_tsupport _) (by
    apply closure_mono
    intro y hy
    change (fun μ ρ => (if ρ=ν then 1 else 0)*lowerMomentum y μ*b y)≠0 at hy
    change b y≠0
    intro hz
    apply hy
    ext μ ρ
    simp [hz])

theorem divergenceTest_tsupport (b : C_c(MomentumCoordinates,ℂ)) (ν : Fin 4) :
    tsupport (divergenceTest b ν)⊆tsupport b := by
  apply closure_mono
  intro y hy
  change divergenceTest b ν y≠0 at hy
  change b y≠0
  intro hz
  apply hy
  ext μ ρ
  simp [divergenceTest,hz]

theorem coefficient_divergenceTest_at (b : C_c(MomentumCoordinates,ℂ)) (ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) : coefficient (divergenceTest b ν) y=0 := by
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑ μ,∑ ρ,strength (momentum y) (realLift (screen y j)) μ ρ*
    ((if ρ=ν then 1 else 0)*lowerMomentum y μ*b y))=0
  simp only [ite_mul,mul_ite,mul_zero,zero_mul,one_mul,Finset.sum_ite_eq',Finset.mem_univ,ite_true]
  have he : (∑ μ,strength (momentum y) (realLift (screen y j)) μ ν*(lowerMomentum y μ*b y))=
      (∑ μ,lowerMomentum y μ*strength (momentum y) (realLift (screen y j)) μ ν)*b y := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro μ _
    ring
  rw [he,real_screen_source_free y hy j ν]
  simp

theorem smear_zero_of_coefficient (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0)
    (hz : coefficient f=0) : smear f hreg=0 := by
  apply (orbitalL2Pullback 0).injective
  simp only [map_zero,smear,orbitalL2Pullback_inverse]
  apply Lp.ext
  filter_upwards [(coefficient_memLp f hreg).coeFn_toLp,Lp.coeFn_zero Fib 2 momentumMeasure]
    with y h1 h2
  rw [h1,h2,hz]

theorem smear_divergence_zero (b : C_c(MomentumCoordinates,ℂ)) (ν : Fin 4)
    (hb : ∀ y∈tsupport b,y.1≠0) :
    smear (divergenceTest b ν) (fun y hy => hb y (divergenceTest_tsupport b ν hy))=0 := by
  apply smear_zero_of_coefficient
  funext y
  by_cases hy : y.1≠0
  · exact coefficient_divergenceTest_at b ν y hy
  · apply coefficient_zero_at
    have hz : b y=0 := by
      by_contra hn
      exact hy (hb y (subset_closure hn))
    ext μ ρ
    simp [divergenceTest,hz]

end F1Fecho.MaxwellSmearing
#print axioms F1Fecho.MaxwellSmearing.real_screen_source_free
#print axioms F1Fecho.MaxwellSmearing.coefficient_divergenceTest_at
#print axioms F1Fecho.MaxwellSmearing.smear_divergence_zero
