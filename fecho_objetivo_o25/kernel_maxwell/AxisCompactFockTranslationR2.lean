import CompactFockBoostDerivativeR2
import RegularFockStressTranslationR3
import ConcreteWeylContinuityR2
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

/-! Translation invariance of the existing axis-compact class and its actual
finite coherent Fock domain. The massless phase is smooth away from the axis;
on the axis, the existing gap makes the product locally zero. No smoothness
of the massless energy at the vertex is assumed. Density uses the already
proved H1 density and continuity/totality of the same exponential vectors.

R2 only separates the typed translation witnesses before assembling the
existential profile, and supplies classical decidable equality for finite
support union. R1 timed out in its combined constructor; smoothness was not
the failing stage. The heartbeat budget and all theorem statements are kept.

This is an uncompiled candidate. It supplies a named vacuum-containing,
translation-invariant dense domain, not a MaxwellCertificate or charge link.
The global regular stress can be retained; boost invariance is not an input.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory
open TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions F1Fecho.Exponential
open scoped Topology ContDiff

theorem orbitalPhase_contDiffAt_off_axis (a : Fin 4 → ℝ)
    (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    ContDiffAt ℝ ∞ (orbitalPhase 0 a) y := by
  have hmpos := transverseMass_pos_of_ne_zero 0 y.1 hy
  have hm : ContDiffAt ℝ ∞ (fun z : MomentumCoordinates => transverseMass 0 z.1) y := by
    unfold transverseMass
    apply ContDiffAt.sqrt
    · fun_prop
    · exact ne_of_gt (Real.sqrt_pos.mp hmpos)
  have he : ContDiffAt ℝ ∞
      (fun z : MomentumCoordinates => energy (transverseMass 0 z.1) z.2) y := by
    unfold energy
    apply ContDiffAt.sqrt
    · exact (hm.pow 2).add (contDiff_snd.contDiffAt.pow 2)
    · nlinarith [sq_pos_of_pos hmpos, sq_nonneg y.2]
  have hs : ContDiffAt ℝ ∞ (shellMomentum 0) y := by
    apply contDiffAt_pi.mpr
    intro i
    fin_cases i
    · exact he
    · exact contDiff_snd.contDiffAt
    · change ContDiffAt ℝ ∞ (fun z : MomentumCoordinates => z.1 0) y
      fun_prop
    · change ContDiffAt ℝ ∞ (fun z : MomentumCoordinates => z.1 1) y
      fun_prop
  have hp : ContDiffAt ℝ ∞
      (fun z => ChatgptAudit.WignerOrbit016.orbitPairing a (shellMomentum 0 z)) y := by
    unfold ChatgptAudit.WignerOrbit016.orbitPairing
    fun_prop
  unfold orbitalPhase ChatgptAudit.WignerOrbit016.phase
  exact ((Complex.ofRealCLM.contDiff.contDiffAt.comp y hp).mul contDiffAt_const).cexp

theorem orbitalPhase_smul_axisGap_contDiff (a : Fin 4 → ℝ)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g)
    (ε : ℝ) (hε : 0 < ε)
    (hgap : ∀ y : MomentumCoordinates, ‖transverseProjection y‖ ≤ ε → g y = 0) :
    ContDiff ℝ ∞ (fun y => orbitalPhase 0 a y • g y) := by
  apply contDiff_iff_contDiffAt.mpr
  intro y
  by_cases hy : y.1 = 0
  · have hlt : ‖transverseProjection y‖ < ε := by
      change ‖y.1‖ < ε
      simpa only [hy, norm_zero] using hε
    have hsmall : {z : MomentumCoordinates | ‖transverseProjection z‖ < ε} ∈ 𝓝 y :=
      (isOpen_lt transverseProjection.continuous.norm continuous_const).mem_nhds hlt
    have heq : (fun z => orbitalPhase 0 a z • g z) =ᶠ[𝓝 y] (fun _ => (0 : Fib)) := by
      filter_upwards [hsmall] with z hz
      rw [hgap z (le_of_lt hz), smul_zero]
    exact contDiffAt_const.congr_of_eventuallyEq heq
  · exact (orbitalPhase_contDiffAt_off_axis a y hy).smul hg.contDiffAt

theorem axisCompactProfile_U1 (a : Fin 4 → ℝ) (h : H1)
    (hh : AxisCompactProfile h) : AxisCompactProfile (U1 a h) := by
  obtain ⟨g, he, hc, hg, ε, hε, hgap⟩ := hh
  let g' : MomentumCoordinates → Fib := fun y => orbitalPhase 0 a y • g y
  have hunit : (U1 a h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0]
      (fun y : MomentumCoordinates => orbitalPhase 0 a y • h y) :=
    orbitalTranslation_ae (E := Fib) 0 a h
  have htransport : (U1 a h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g' := by
    filter_upwards [hunit, he] with y ht hy
    exact ht.trans (congrArg (fun v : Fib => orbitalPhase 0 a y • v) hy)
  have hcompact : HasCompactSupport g' := by
    change HasCompactSupport ((orbitalPhase 0 a) • g)
    exact HasCompactSupport.smul_left (f := orbitalPhase 0 a) hc
  have hsmooth : ContDiff ℝ ∞ g' :=
    orbitalPhase_smul_axisGap_contDiff a g hg ε hε hgap
  have hgap' : ∀ y : MomentumCoordinates, ‖transverseProjection y‖ ≤ ε → g' y = 0 := by
    intro y hy
    change orbitalPhase 0 a y • g y = 0
    rw [hgap y hy, smul_zero]
  refine ⟨g', ?_, ?_, ?_, ?_⟩
  · exact htransport
  · exact hcompact
  · exact hsmooth
  · exact ⟨ε, hε, hgap'⟩

theorem axisCompactProfile_U1_iff (a : Fin 4 → ℝ) (h : H1) :
    AxisCompactProfile (U1 a h) ↔ AxisCompactProfile h := by
  constructor
  · intro hh
    have ht := axisCompactProfile_U1 (-a) (U1 a h) hh
    simpa only [U1_neg, LinearIsometryEquiv.symm_apply_apply] using ht
  · exact axisCompactProfile_U1 a h

theorem axisCompactProfile_zero : AxisCompactProfile (0 : H1) := by
  refine ⟨(0 : MomentumCoordinates → Fib), Lp.coeFn_zero Fib 2 (orbitalMeasure 0),
    HasCompactSupport.zero, contDiff_const, 1, by norm_num, ?_⟩
  intro y _
  rfl

theorem axisCompactFock_zero : AxisCompactFock (0 : regularFockDomain) := by
  have hc : regularCoefficients (0 : regularFockDomain) = 0 := by
    apply regularSynthesis_injective
    rw [regularCoefficients_spec, map_zero]
    rfl
  intro h hh
  rw [hc] at hh
  exact False.elim (by simpa using hh)

theorem axisCompactFock_add (ψ χ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hχ : AxisCompactFock χ) : AxisCompactFock (ψ + χ) := by
  classical
  intro h hh
  rw [regularCoefficients_add] at hh
  rcases Finset.mem_union.mp (Finsupp.support_add hh) with hp | hq
  · exact hψ h hp
  · exact hχ h hq

theorem axisCompactFock_smul (z : ℂ) (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) : AxisCompactFock (z • ψ) := by
  intro h hh
  rw [regularCoefficients_smul] at hh
  exact hψ h (Finsupp.support_smul hh)

theorem axisCompactFock_vacuum : AxisCompactFock regularVacuum := by
  rw [regularVacuum_eq_exponential]
  exact axisCompactFock_exponential _ axisCompactProfile_zero

theorem axisCompactFock_translate (a : Fin 4 → ℝ) (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    AxisCompactFock (regularGamma (U1 a) (strongRegularProfile_U1 a) ψ) := by
  let e : RegularLabel ≃ RegularLabel := regularLabelEquiv (U1 a)
    (strongRegularProfile_U1 a) (strongRegularProfile_U1_symm a)
  intro k hk
  rw [regularCoefficients_gamma (U1 a) (strongRegularProfile_U1 a)
    (strongRegularProfile_U1_symm a)] at hk
  have hk' : e.symm k ∈ (regularCoefficients ψ).support := by
    simpa only [Finsupp.mem_support_iff, Finsupp.equivMapDomain_apply] using hk
  have ht := axisCompactProfile_U1 a (e.symm k).val (hψ (e.symm k) hk')
  have he : U1 a (e.symm k).val = k.val :=
    congrArg Subtype.val (e.apply_symm_apply k)
  exact he ▸ ht

/-- The exact AxisCompactFock condition, embedded in the unchanged Fock space. -/
def axisCompactFockDomain : Submodule ℂ F where
  carrier := {ψ | ∃ hψ : ψ ∈ regularFockDomain, AxisCompactFock ⟨ψ, hψ⟩}
  zero_mem' := ⟨regularFockDomain.zero_mem, axisCompactFock_zero⟩
  add_mem' := by
    rintro ψ χ ⟨hp, hψ⟩ ⟨hq, hχ⟩
    exact ⟨regularFockDomain.add_mem hp hq,
      axisCompactFock_add ⟨ψ, hp⟩ ⟨χ, hq⟩ hψ hχ⟩
  smul_mem' := by
    rintro z ψ ⟨hp, hψ⟩
    exact ⟨regularFockDomain.smul_mem z hp, axisCompactFock_smul z ⟨ψ, hp⟩ hψ⟩

theorem axisCompactFockDomain_le_regular : axisCompactFockDomain ≤ regularFockDomain :=
  fun _ h => h.choose

theorem mem_axisCompactFockDomain_iff (ψ : regularFockDomain) :
    ψ.val ∈ axisCompactFockDomain ↔ AxisCompactFock ψ := by
  constructor
  · rintro ⟨_, h⟩
    exact h
  · exact fun h => ⟨ψ.property, h⟩

theorem vacuum_mem_axisCompactFockDomain : vacuum ∈ axisCompactFockDomain :=
  ⟨vacuum_mem_regularFockDomain, axisCompactFock_vacuum⟩

theorem gamma_U1_mem_axisCompactFockDomain (a : Fin 4 → ℝ) (ψ : F)
    (hψ : ψ ∈ axisCompactFockDomain) : gamma (U1 a) ψ ∈ axisCompactFockDomain := by
  obtain ⟨hp, hc⟩ := hψ
  exact ⟨(regularFockDomain_translate a ψ).mpr hp,
    axisCompactFock_translate a ⟨ψ, hp⟩ hc⟩

theorem axisCompactFockDomain_translate (a : Fin 4 → ℝ) (ψ : F) :
    gamma (U1 a) ψ ∈ axisCompactFockDomain ↔ ψ ∈ axisCompactFockDomain := by
  constructor
  · intro hψ
    have ht := gamma_U1_mem_axisCompactFockDomain (-a) (gamma (U1 a) ψ) hψ
    simpa only [U1_neg, gamma_symm, LinearIsometryEquiv.symm_apply_apply] using ht
  · exact gamma_U1_mem_axisCompactFockDomain a ψ

theorem exponential_mem_axisCompactFockDomain (h : H1) (hh : AxisCompactProfile h) :
    exponential h ∈ axisCompactFockDomain :=
  ⟨exponential_mem_regularFockDomain h (axisCompactProfile_strongRegular h hh),
    axisCompactFock_exponential ⟨h, axisCompactProfile_strongRegular h hh⟩ hh⟩

theorem axisCompactFockDomain_dense : Dense (axisCompactFockDomain : Set F) := by
  apply Submodule.dense_iff_topologicalClosure_eq_top.mpr
  have he : ∀ h : H1, exponential h ∈ axisCompactFockDomain.topologicalClosure := by
    have hc : IsClosed {h : H1 | exponential h ∈ axisCompactFockDomain.topologicalClosure} :=
      axisCompactFockDomain.isClosed_topologicalClosure.preimage
        F1Fecho.ConcreteWeyl.exponential_continuous
    have hs : {h : H1 | AxisCompactProfile h} ⊆
        {h : H1 | exponential h ∈ axisCompactFockDomain.topologicalClosure} := by
      intro h hh
      exact axisCompactFockDomain.le_topologicalClosure (exponential_mem_axisCompactFockDomain h hh)
    exact fun h => closure_minimal hs hc (axisCompactProfile_dense h)
  have hs : Submodule.span ℂ (Set.range exponential) ≤ axisCompactFockDomain.topologicalClosure := by
    apply Submodule.span_le.mpr
    rintro _ ⟨h, rfl⟩
    exact he h
  have ht := (Submodule.span ℂ (Set.range exponential)).topologicalClosure_minimal
    hs axisCompactFockDomain.isClosed_topologicalClosure
  rw [exponential_total] at ht
  exact top_le_iff.mp ht

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.orbitalPhase_contDiffAt_off_axis
#print axioms F1Fecho.MaxwellGlobal.orbitalPhase_smul_axisGap_contDiff
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_U1
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_U1_iff
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_add
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_smul
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_vacuum
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_translate
#print axioms F1Fecho.MaxwellGlobal.axisCompactFockDomain_le_regular
#print axioms F1Fecho.MaxwellGlobal.mem_axisCompactFockDomain_iff
#print axioms F1Fecho.MaxwellGlobal.vacuum_mem_axisCompactFockDomain
#print axioms F1Fecho.MaxwellGlobal.gamma_U1_mem_axisCompactFockDomain
#print axioms F1Fecho.MaxwellGlobal.axisCompactFockDomain_translate
#print axioms F1Fecho.MaxwellGlobal.exponential_mem_axisCompactFockDomain
#print axioms F1Fecho.MaxwellGlobal.axisCompactFockDomain_dense
