import RegularMaxwellFockDomainR5
import OrbitalLocalFinitenessR2
import ConcreteWeylContinuityR2
import Mathlib.Analysis.Normed.Lp.SmoothApprox

/-! Density of actual smooth compact momentum profiles in the unchanged H1,
and hence of the regular coherent Fock domain. This does not yet remove a
neighborhood of zero or prove a null-plane charge identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Set Filter TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016 F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.OrbitalSpatial
open scoped ContDiff

def SmoothCompactProfile (h : H1) : Prop :=
  ∃g : MomentumCoordinates→Fib,h=ᵐ[orbitalMeasure 0]g ∧
    HasCompactSupport g ∧ ContDiff ℝ ∞ g

theorem smoothCompactProfile_strongRegular (h : H1) (hh : SmoothCompactProfile h) :
    StrongRegularProfile h := by
  obtain ⟨g,he,hc,hd⟩:=hh
  constructor
  · intro m
    have hi : Integrable (fun y=>shellEnergy y^m*‖g y‖) (orbitalMeasure 0) :=
      ((shellEnergy_continuous.pow m).mul hd.continuous.norm).integrable_of_hasCompactSupport
        hc.norm.mul_left
    apply hi.congr
    filter_upwards [he] with y hy
    rw [hy]
  · intro m
    have hsq : HasCompactSupport (fun y=>‖g y‖^2) :=
      hc.norm.comp_left (g:=fun r : ℝ=>r^2) (by norm_num)
    have hi : Integrable (fun y=>shellEnergy y^m*‖g y‖^2) (orbitalMeasure 0) :=
      ((shellEnergy_continuous.pow m).mul (hd.continuous.norm.pow 2)).integrable_of_hasCompactSupport
        hsq.mul_left
    apply hi.congr
    filter_upwards [he] with y hy
    rw [hy]

theorem smoothCompactProfile_dense : Dense {h : H1 | SmoothCompactProfile h} :=
  Lp.dense_hasCompactSupport_contDiff (by norm_num : (2 : ℝ≥0∞)≠⊤)

theorem strongRegularProfile_dense : Dense {h : H1 | StrongRegularProfile h} :=
  smoothCompactProfile_dense.mono (fun h hh=>smoothCompactProfile_strongRegular h hh)

theorem regularFockDomain_dense : Dense (regularFockDomain : Set F) := by
  apply Submodule.dense_iff_topologicalClosure_eq_top.mpr
  have he : ∀h : H1,exponential h∈regularFockDomain.topologicalClosure := by
    have hc : IsClosed {h : H1 | exponential h∈regularFockDomain.topologicalClosure} :=
      regularFockDomain.isClosed_topologicalClosure.preimage
        F1Fecho.ConcreteWeyl.exponential_continuous
    have hs : {h : H1 | StrongRegularProfile h} ⊆
        {h : H1 | exponential h∈regularFockDomain.topologicalClosure} := by
      intro h hh
      exact regularFockDomain.le_topologicalClosure (exponential_mem_regularFockDomain h hh)
    exact fun h=>closure_minimal hs hc (strongRegularProfile_dense h)
  have hs : Submodule.span ℂ (Set.range exponential)≤regularFockDomain.topologicalClosure := by
    apply Submodule.span_le.mpr
    rintro _ ⟨h,rfl⟩
    exact he h
  have ht := (Submodule.span ℂ (Set.range exponential)).topologicalClosure_minimal
    hs regularFockDomain.isClosed_topologicalClosure
  rw [exponential_total] at ht
  exact top_le_iff.mp ht

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.smoothCompactProfile_strongRegular
#print axioms F1Fecho.MaxwellGlobal.smoothCompactProfile_dense
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_dense
#print axioms F1Fecho.MaxwellGlobal.regularFockDomain_dense
