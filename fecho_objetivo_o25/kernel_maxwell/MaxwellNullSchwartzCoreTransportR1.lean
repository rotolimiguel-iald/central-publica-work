import MaxwellNullSchwartzConsumerR2
import SmoothScreenDualTensorR5
import Mathlib.Analysis.Calculus.ContDiff.WithLp

/-! Candidate S1-S3: smooth compact null-coordinate amplitudes.

Inputs are the actual smooth compact momentum representative g and its
existing transverse-axis cutoff. Smoothness of the screen amplitude, a
strict positive null-frequency gap on tsupport g, and smooth compactness
of the zero extension are conclusions. No such conclusion is a field or
an extra hypothesis. The resulting Schwartz map is given by the explicit
same polarization and inverse null-frequency map used by the wave.

OPEN after this component: pull back orbital a.e. representatives through
the null-coordinate map (S4), assemble NullSchwartzData for the same H1 h
(S5), then reuse the existing density (S6). No charge_link, strong H1
boost derivative, nonzero modular energy, or MaxwellCertificate is claimed.
The author did not compile this candidate.
-/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory Matrix SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency
open scoped ContDiff Topology

/-- The same null polarization applied to a smooth representative of H1. -/
def screenAmplitudeOf (g : MomentumCoordinates → Fib) (a : Fin 2)
    (y : MomentumCoordinates) : ℂ :=
  ∑ j : Fin 2, (nullPolarization y a j : ℂ) * g y j

 theorem screenAmplitudeOf_eq_zero (g : MomentumCoordinates → Fib) (a : Fin 2)
    (y : MomentumCoordinates) (hy : g y = 0) : screenAmplitudeOf g a y = 0 := by
  simp [screenAmplitudeOf, hy]

/-- S1: the existing division-by-transverse-mass lemma removes the gauge
singularity because the representative already vanishes near that axis. -/
 theorem screenAmplitudeOf_smooth (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2) :
    ContDiff ℝ ∞ (screenAmplitudeOf g a) := by
  let v : MomentumCoordinates → Fin 2 → ℂ := fun y => WithLp.ofLp (g y)
  have hv : ContDiff ℝ ∞ v := PiLp.contDiff_ofLp.comp hg
  have hvcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → v y = 0 := by
    intro y hy
    change WithLp.ofLp (g y) = 0
    rw [hcut y hy]
    rfl
  have h0 := screenRatio_smooth v hv ε hε hvcut 0
  have h1 := screenRatio_smooth v hv ε hε hvcut 1
  have hq0 : ContDiff ℝ ∞ (fun y : MomentumCoordinates => (y.1 0 : ℂ)) := by fun_prop
  have hq1 : ContDiff ℝ ∞ (fun y : MomentumCoordinates => (y.1 1 : ℂ)) := by fun_prop
  fin_cases a
  · convert (hq0.mul h0).neg.add (hq1.mul h1) using 1
    funext y
    simp [screenAmplitudeOf, nullPolarization, transverseRatio, Fin.sum_univ_two, v]
    <;> ring
  · convert (hq1.mul h0).neg.sub (hq0.mul h1) using 1
    funext y
    simp [screenAmplitudeOf, nullPolarization, transverseRatio, Fin.sum_univ_two, v]
    <;> ring

 theorem screenAmplitudeOf_compact (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) (a : Fin 2) : HasCompactSupport (screenAmplitudeOf g a) := by
  apply hc.mono
  intro y hy
  change g y ≠ 0
  intro hz
  exact hy (screenAmplitudeOf_eq_zero g a y hz)

 theorem axisCutoff_tsupport_lower (g : MomentumCoordinates → Fib) (ε : ℝ)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) :
    tsupport g ⊆ {y : MomentumCoordinates | ε ≤ ‖y.1‖} := by
  change closure (Function.support g) ⊆ _
  apply closure_minimal ?_ (isClosed_le continuous_const continuous_fst.norm)
  intro y hy
  by_contra hn
  exact hy (hcut y (le_of_lt (lt_of_not_ge hn)))

 theorem nullCoreFrequency_continuous : Continuous shellNullFrequency :=
  shellEnergy_continuous.sub continuous_snd

/-- S2: a positive minimum is derived on the actual compact support.
This includes the empty-support case, without a nonempty-support premise. -/
 theorem axisCompact_uniform_null_gap (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) :
    ∃ δ : ℝ, 0 < δ ∧ ∀ y ∈ tsupport g, δ ≤ shellNullFrequency y := by
  apply hc.isCompact.exists_forall_le' nullCoreFrequency_continuous.continuousOn
  intro y hy
  apply shellNullFrequency_pos
  intro hzero
  have hle := axisCutoff_tsupport_lower g ε hcut hy
  have hn : ε ≤ 0 := by simpa [hzero] using hle
  exact (not_le_of_gt hε) hn

/-- This explicit rational formula is proved equal to the existing inverse
coordinate; squaring the transverse mass removes sqrt from this chart. -/
def nullCoreMomentum (p : NullFourierSpace) : MomentumCoordinates :=
  (fun j : Fin 2 => p j.succ, (p 1 ^ 2 + p 2 ^ 2 - p 0 ^ 2) / (2 * p 0))

 theorem nullCoreMomentum_eq (p : NullFourierSpace) :
    nullCoreMomentum p = nullMomentumCoordinates (fun j : Fin 2 => p j.succ) (p 0) := by
  apply Prod.ext
  · rfl
  · simp [nullCoreMomentum, nullMomentumCoordinates, inverseLongitudinal, transverseMass_sq]

 theorem nullCoreMomentum_smoothAt (p : NullFourierSpace) (hp : 0 < p 0) :
    ContDiffAt ℝ ∞ nullCoreMomentum p := by
  have hq : ContDiff ℝ ∞ (fun z : NullFourierSpace => fun j : Fin 2 => z j.succ) := by
    apply contDiff_pi.mpr
    intro j
    fun_prop
  have hn : ContDiff ℝ ∞ (fun z : NullFourierSpace => z 1 ^ 2 + z 2 ^ 2 - z 0 ^ 2) := by
    fun_prop
  have hd : ContDiff ℝ ∞ (fun z : NullFourierSpace => 2 * z 0) := by fun_prop
  exact hq.contDiffAt.prodMk (hn.contDiffAt.div hd.contDiffAt (mul_ne_zero two_ne_zero hp.ne'))

 theorem nullCoreMomentum_frequency (p : NullFourierSpace) (hp : 0 < p 0) :
    shellNullFrequency (nullCoreMomentum p) = p 0 := by
  rw [nullCoreMomentum_eq]
  exact null_inverseLongitudinal (transverseMass 0 (fun j : Fin 2 => p j.succ)) (p 0) hp

 theorem nullCoreMomentum_point_inverse (p : NullFourierSpace) (hp : 0 < p 0) :
    nullFourierProfilePoint (nullCoreMomentum p) = p := by
  unfold nullFourierProfilePoint
  rw [nullCoreMomentum_frequency p hp]
  apply PiLp.ext
  intro i
  fin_cases i <;> rfl

 theorem nullCoreMomentum_profilePoint (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    nullCoreMomentum (nullFourierProfilePoint y) = y := by
  rw [nullCoreMomentum_eq]
  change (y.1, inverseLongitudinal (transverseMass 0 y.1) (shellNullFrequency y)) = y
  have hi : inverseLongitudinal (transverseMass 0 y.1) (shellNullFrequency y) = y.2 :=
    inverseLongitudinal_null (transverseMass 0 y.1) y.2
      (transverseMass_pos_of_ne_zero 0 y.1 hy)
  rw [hi]

 theorem nullCoreProfilePoint_continuous : Continuous nullFourierProfilePoint := by
  apply PiLp.continuous_toLp.comp
  apply continuous_pi
  intro i
  fin_cases i
  · exact nullCoreFrequency_continuous
  · exact (continuous_apply (0 : Fin 2)).comp continuous_fst
  · exact (continuous_apply (1 : Fin 2)).comp continuous_fst

/-- The zero extension is a definition on all Euclidean frequency space. -/
def nullCoreAmplitude (g : MomentumCoordinates → Fib) (a : Fin 2)
    (p : NullFourierSpace) : ℂ :=
  if 0 < p 0 then screenAmplitudeOf g a (nullCoreMomentum p) else 0

 theorem nullCoreAmplitude_nonpositive (g : MomentumCoordinates → Fib) (a : Fin 2)
    (p : NullFourierSpace) (hp : p 0 ≤ 0) : nullCoreAmplitude g a p = 0 := by
  simp [nullCoreAmplitude, not_lt_of_ge hp]

 theorem nullCoreAmplitude_zero_below_gap (g : MomentumCoordinates → Fib)
    (a : Fin 2) (δ : ℝ)
    (hgap : ∀ y ∈ tsupport g, δ ≤ shellNullFrequency y)
    (p : NullFourierSpace) (hp : p 0 < δ) : nullCoreAmplitude g a p = 0 := by
  by_cases hu : 0 < p 0
  · have hz : g (nullCoreMomentum p) = 0 := by
      by_contra hn
      have hm : nullCoreMomentum p ∈ tsupport g := (subset_tsupport g) hn
      have hd := hgap (nullCoreMomentum p) hm
      rw [nullCoreMomentum_frequency p hu] at hd
      exact (not_lt_of_ge hd) hp
    simp [nullCoreAmplitude, hu, screenAmplitudeOf_eq_zero g a (nullCoreMomentum p) hz]
  · simp [nullCoreAmplitude, hu]

/-- S3a: smoothness on u>0 and the derived gap prove smoothness through u=0. -/
 theorem nullCoreAmplitude_smooth (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2) :
    ContDiff ℝ ∞ (nullCoreAmplitude g a) := by
  obtain ⟨δ, hδ, hgap⟩ := axisCompact_uniform_null_gap g hc ε hε hcut
  have hcoord : Continuous (fun p : NullFourierSpace => p 0) := PiLp.continuous_apply 0
  rw [contDiff_iff_contDiffAt]
  intro p
  by_cases hp : 0 < p 0
  · have hs : ContDiffAt ℝ ∞
        (fun z => screenAmplitudeOf g a (nullCoreMomentum z)) p :=
      (screenAmplitudeOf_smooth g hg ε hε hcut a).contDiffAt.comp p
        (nullCoreMomentum_smoothAt p hp)
    apply hs.congr_of_eventuallyEq
    have hn : ∀ᶠ z in 𝓝 p, 0 < z 0 :=
      (isOpen_lt continuous_const hcoord).mem_nhds hp
    filter_upwards [hn] with z hz
    simp [nullCoreAmplitude, hz]
  · apply (contDiffAt_const (c := (0 : ℂ))).congr_of_eventuallyEq
    have hpδ : p 0 < δ := lt_of_le_of_lt (le_of_not_gt hp) hδ
    have hn : ∀ᶠ z in 𝓝 p, z 0 < δ :=
      (isOpen_lt hcoord continuous_const).mem_nhds hpδ
    filter_upwards [hn] with z hz
    exact nullCoreAmplitude_zero_below_gap g a δ hgap z hz

/-- S3b: support lies in the compact forward image of the original support.
Compactness is proved, not assumed for the new null-coordinate function. -/
 theorem nullCoreAmplitude_compact (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) (a : Fin 2) : HasCompactSupport (nullCoreAmplitude g a) := by
  apply HasCompactSupport.of_support_subset_isCompact
    (hc.isCompact.image nullCoreProfilePoint_continuous)
  intro p hp
  have hu : 0 < p 0 := by
    by_contra hn
    exact hp (by simp [nullCoreAmplitude, hn])
  have hg : g (nullCoreMomentum p) ≠ 0 := by
    intro hz
    exact hp (by simp [nullCoreAmplitude, hu,
      screenAmplitudeOf_eq_zero g a (nullCoreMomentum p) hz])
  exact ⟨nullCoreMomentum p, (subset_tsupport g) hg, nullCoreMomentum_point_inverse p hu⟩

/-- Constructed Schwartz profile; smoothness and decay are discharged above. -/
def nullCoreSchwartzProfile (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2) :
    𝓢(NullFourierSpace, ℂ) :=
  (nullCoreAmplitude_compact g hc a).toSchwartzMap
    (nullCoreAmplitude_smooth g hg hc ε hε hcut a)

@[simp] theorem nullCoreSchwartzProfile_apply (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2)
    (p : NullFourierSpace) :
    nullCoreSchwartzProfile g hg hc ε hε hcut a p = nullCoreAmplitude g a p := rfl

 theorem nullCoreSchwartzProfile_nonpositive (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2)
    (p : NullFourierSpace) (hp : p 0 ≤ 0) :
    nullCoreSchwartzProfile g hg hc ε hε hcut a p = 0 :=
  nullCoreAmplitude_nonpositive g a p hp

/-- Pointwise identification on the smooth original representative g.
Passing from h=ae g to the null-coordinate representative remains S4. -/
 theorem nullCoreSchwartzProfile_orbital (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2)
    (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    nullCoreSchwartzProfile g hg hc ε hε hcut a (nullFourierProfilePoint y) =
      screenAmplitudeOf g a y := by
  change nullCoreAmplitude g a (nullFourierProfilePoint y) = _
  have hp : 0 < (nullFourierProfilePoint y) 0 := shellNullFrequency_pos y hy
  rw [nullCoreAmplitude, if_pos hp, nullCoreMomentum_profilePoint y hy]

 theorem nullCoreSchwartzProfile_null (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (ε : ℝ) (hε : 0 < ε)
    (hcut : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0) (a : Fin 2)
    (q : Transverse) (u : ℝ) (hu : 0 < u) :
    nullCoreSchwartzProfile g hg hc ε hε hcut a (nullFourierCoordinates q u) =
      screenAmplitudeOf g a (nullMomentumCoordinates q u) := by
  change nullCoreAmplitude g a (nullFourierCoordinates q u) = _
  have hp : 0 < (nullFourierCoordinates q u) 0 := hu
  rw [nullCoreAmplitude, if_pos hp, nullCoreMomentum_eq]
  rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.screenAmplitudeOf_smooth
#print axioms F1Fecho.MaxwellGlobal.screenAmplitudeOf_compact
#print axioms F1Fecho.MaxwellGlobal.axisCutoff_tsupport_lower
#print axioms F1Fecho.MaxwellGlobal.axisCompact_uniform_null_gap
#print axioms F1Fecho.MaxwellGlobal.nullCoreMomentum_eq
#print axioms F1Fecho.MaxwellGlobal.nullCoreMomentum_smoothAt
#print axioms F1Fecho.MaxwellGlobal.nullCoreMomentum_point_inverse
#print axioms F1Fecho.MaxwellGlobal.nullCoreAmplitude_zero_below_gap
#print axioms F1Fecho.MaxwellGlobal.nullCoreAmplitude_smooth
#print axioms F1Fecho.MaxwellGlobal.nullCoreAmplitude_compact
#print axioms F1Fecho.MaxwellGlobal.nullCoreSchwartzProfile
#print axioms F1Fecho.MaxwellGlobal.nullCoreSchwartzProfile_nonpositive
#print axioms F1Fecho.MaxwellGlobal.nullCoreSchwartzProfile_orbital
#print axioms F1Fecho.MaxwellGlobal.nullCoreSchwartzProfile_null
