import TGLExt.V350ScalarGNSCutNorm
import TGLExt.V350DualOrbitStrongLimits

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

/-- A finite-interval vector in the existing ambient L² space. It is not normalized
to a state and no separating property is included in its definition. -/
def scalarCutVacuum (P : SiteProfile) (R : ℝ) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    indicatorConstLp 2 (measurableSet_Ioc (a := -R) (b := R)) (by simp) (regularVacuum P)

theorem scalarCutVacuum_ae (P : SiteProfile) (R : ℝ) :
    (scalarCutVacuum P R : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      (Set.Ioc (-R) R).indicator (fun _ => (Real.sqrt dualHaarFactor : ℝ) • regularVacuum P) := by
  let f : RegularHilbert (RegularHilbert (TowerHilbert P)) :=
    indicatorConstLp 2 (measurableSet_Ioc (a := -R) (b := R)) (by simp) (regularVacuum P)
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ) f,
    indicatorConstLp_coeFn (p := (2 : ENNReal))
      (hs := measurableSet_Ioc (a := -R) (b := R)) (hμs := by simp) (c := regularVacuum P)]
    with x h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • f) x = _
  simp only [Pi.smul_apply] at h1
  rw [h1,show f x = _ from h2]
  by_cases hx : x ∈ Set.Ioc (-R) R <;> simp [hx]

/-- The cut of every finite-ideal GNS vector is generated from the same cut vacuum. -/
theorem scalarGNSCutMap_embedding_eq_action (P : SiteProfile) (R : ℝ)
    (A : finiteDualLeftIdeal P) :
    scalarGNSCutMap P R (scalarGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P R) := by
  apply Lp.ext
  filter_upwards [measurableCut_ae (Set.Ioc (-R) R) measurableSet_Ioc (scalarGNSOrbit P A),
    scalarGNSOrbit_ae P A,operatorFieldLift_ae (dualIntegralFamily A.val.val) (scalarCutVacuum P R),
    scalarCutVacuum_ae P R] with s h1 h2 h3 h4
  change measurableCut (Set.Ioc (-R) R) measurableSet_Ioc (scalarGNSOrbit P A) s =
    operatorFieldLift (dualIntegralFamily A.val.val) (scalarCutVacuum P R) s
  rw [h1,h3,h4]
  by_cases hs : s ∈ Set.Ioc (-R) R
  · simp only [Set.indicator_of_mem hs,h2]
    change (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s A.val.val (regularVacuum P) =
      dualAmbient s A.val.val ((↑(Real.sqrt dualHaarFactor) : ℂ) • regularVacuum P)
    exact (map_smul (dualAmbient s A.val.val) _ _).symm
  · simp only [Set.indicator_of_notMem hs,map_zero]

theorem scalarCutVacuum_mem_closure_cut_range (P : SiteProfile) (R : ℝ) :
    scalarCutVacuum P R ∈ closure (Set.range (scalarGNSCutMap P R)) := by
  have ht := dualOrbit_tendsto_of_uniformly_bounded
    (fun h : ℝ => regularAverage P h) 1 1 (regularAverage_norm_le_one P)
    (fun v => by simpa only [one_apply_eq_self] using regularAverage_tendsto_identity P v)
    (scalarCutVacuum P R)
  have ht' : Tendsto (fun h : ℝ => dualOrbitRepresentation (regularAverage P h)
      (scalarCutVacuum P R)) (𝓝[>] 0) (𝓝 (scalarCutVacuum P R)) := by
    simpa only [map_one,one_apply_eq_self] using ht.mono_left (nhdsGT_le_nhdsNE 0)
  apply mem_closure_of_tendsto ht'
  filter_upwards [self_mem_nhdsWithin] with h hh
  let A : finiteDualLeftIdeal P :=
    ⟨⟨regularAverage P h,regularAverage_mem P h⟩,regularAverage_hasFiniteDualSquare P h hh⟩
  exact ⟨scalarGNSEmbedding P A,scalarGNSCutMap_embedding_eq_action P R A⟩

#print axioms scalarCutVacuum
#print axioms scalarCutVacuum_ae
#print axioms scalarGNSCutMap_embedding_eq_action
#print axioms scalarCutVacuum_mem_closure_cut_range
end
end TGLV350.Regular
