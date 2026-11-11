import TGLExt.F1Fecho394.GeneralSineResolventApproxR2
import TGLExt.F1Fecho394.GenericModularCutToolsR1
/-! CFC and bounded-strong transport for the actual regular generator in any
representation of its core. Strong continuity and commutation are explicit
premises, to be discharged by the concrete Fock GNS representation. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
namespace F1Fecho.RepresentedRegularResolvent
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.RegularPositiveFlow F1Fecho.RegularCovariantCore
open scoped Topology
variable {H K : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
local instance : NormedSpace ℂ (K →L[ℂ] K) := inferInstance
local instance : Module ℂ (K →L[ℂ] K) := ContinuousLinearMap.module
local instance : ContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : IsometricContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instIsometricContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : SMulCommClass ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  change c • a (b x) = a (c • b x)
  exact (a.map_smul c (b x)).symm⟩
local instance : IsScalarTower ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  rfl⟩
variable (Q : UnitaryFlow H) (M : VonNeumannAlgebra H)
variable (π : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra →⋆ₐ[ℂ] (K →L[ℂ] K))

def groupElement (t : ℝ) : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra :=
  ⟨F1Fecho.RegularCovariantCore.regularUnitary Q t,regular_mem Q M t⟩

def resolventElement : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra :=
  ⟨F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q,
    F1Fecho.RegularPositiveFlow.regularSpectralResolvent_mem Q M⟩

def windowElement (m : ℝ) : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (groupElement Q M (-1/m)-groupElement Q M (1/m))

theorem windowElement_val (m : ℝ) : (windowElement Q M m).val =
    F1Fecho.RegularPositiveFlow.regularSineWindow Q m := rfl

private theorem core_closed : IsClosed ((F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra : Set (RegularHilbert H →L[ℂ] RegularHilbert H)) := by
  change IsClosed (F1Fecho.RegularCovariantCore.core Q M : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
  rw [← VonNeumannAlgebra.centralizer_centralizer (F1Fecho.RegularCovariantCore.core Q M)]
  exact Set.isClosed_centralizer _

theorem represented_damped_phase (t : ℝ) :
    π (groupElement Q M t) * resolventDampingOperator (H := K) (π (resolventElement Q M)) =
      resolventPhaseOperator (H := K) (π (resolventElement Q M)) t := by
  letI := core_closed Q M
  let r := resolventElement Q M
  let f : ℂ → ℂ := fun z => resolventPhaseFunction t z.re
  have hf : Continuous f := (resolventPhaseFunction_continuous t).comp Complex.continuous_re
  have hr : IsSelfAdjoint r.val :=
    IsSelfAdjoint.of_nonneg (F1Fecho.RegularPositiveFlow.regularSpectralResolvent_nonneg Q)
  obtain ⟨hm,hmap,_⟩ := F1Fecho.ModularCutBalance.closed_representation_cfc (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra π r hr f hf
  have he : groupElement Q M t * (r*(1-r)) = (⟨cfc f r.val,hm⟩ : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra) := by
    apply Subtype.ext
    ext1 x
    change F1Fecho.RegularCovariantCore.regularUnitary Q t
      (resolventDampingOperator (F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q) x) =
      resolventPhaseOperator (F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q) t x
    rw [← F1Fecho.RegularPositiveFlow.regularPositiveGenerator_imaginaryPower Q t]
    exact resolventImaginaryPower_damping _ _ _ _ _ t x
  have hp := congrArg (fun a : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra => π a) he
  simp only [map_mul,map_sub,map_one] at hp
  exact hp.trans hmap

theorem represented_resolvent_commutes
    (hπstrong : ∀ (b : ℕ → (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra) (r : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra) (C : ℝ),
      (∀ n, ‖(b n).val‖ ≤ C) →
      (∀ x, Tendsto (fun n => (b n).val x) atTop (𝓝 (r.val x))) →
      ∀ x, Tendsto (fun n => π (b n) x) atTop (𝓝 (π r x)))
    (T : K →L[ℂ] K) (hgroup : ∀ t : ℝ, Commute T (π (groupElement Q M t))) :
    Commute T (π (resolventElement Q M)) := by
  letI := core_closed Q M
  have hwin (m : ℝ) : Commute T (π (windowElement Q M m)) := by
    change Commute T (π ((1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
      (groupElement Q M (-1/m)-groupElement Q M (1/m))))
    simp only [map_add,map_smul,map_sub,map_one]
    exact ((Commute.one_right T).smul_right (1/2 : ℂ)).add_right
      (((hgroup (-1/m)).sub_right (hgroup (1/m))).smul_right (1/(4*Complex.I) : ℂ))
  have hsmem (m : ℝ) : F1Fecho.RegularPositiveFlow.regularSineResolvent Q m ∈ (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra := by
    rw [F1Fecho.RegularPositiveFlow.regularSineResolvent_cfc]
    exact cfc_mem (𝕜' := ℂ) _ (windowElement Q M m).property
  let b (n : ℕ) : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra :=
    ⟨F1Fecho.RegularPositiveFlow.regularSineResolvent Q ((n : ℝ)+1),hsmem ((n : ℝ)+1)⟩
  have hb (n : ℕ) : Commute T (π (b n)) := by
    let m : ℝ := (n : ℝ)+1
    let w : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra := windowElement Q M m
    let f : ℂ → ℂ := fun z => (Real.sigmoid (m*(2*z.re-1)) : ℂ)
    have hf : Continuous f := by fun_prop
    have hw : IsSelfAdjoint w.val := by
      change IsSelfAdjoint (F1Fecho.RegularPositiveFlow.regularSineWindow Q m)
      rw [F1Fecho.RegularPositiveFlow.regularSineWindow_spectral]
      exact (IsSelfAdjoint.of_nonneg (realScalarMultiplier_nonneg (H := H) _ _ _ _)).map _
    obtain ⟨hm,_,hc⟩ := F1Fecho.ModularCutBalance.closed_representation_cfc (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra π w hw f hf
    have hbn : (⟨cfc f w.val,hm⟩ : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra)=b n :=
      Subtype.ext (F1Fecho.RegularPositiveFlow.regularSineResolvent_cfc Q m).symm
    specialize hc T (hwin m)
    rw [hbn] at hc
    exact hc
  have hlim (x : K) : Tendsto (fun n => π (b n) x) atTop
      (𝓝 (π (resolventElement Q M) x)) :=
    hπstrong b (resolventElement Q M) 1
      (fun n => F1Fecho.RegularPositiveFlow.regularSineResolvent_norm_le Q ((n : ℝ)+1))
      (F1Fecho.RegularPositiveFlow.regularSineResolvent_tendsto Q) x
  apply ContinuousLinearMap.ext
  intro x
  have h1 := T.continuous.continuousAt.tendsto.comp (hlim x)
  have h2 := hlim (T x)
  have heq : (fun n => T (π (b n) x))=(fun n => π (b n) (T x)) := by
    funext n
    exact congrArg (fun W : K →L[ℂ] K => W x) (hb n).eq
  change Tendsto (fun n => T (π (b n) x)) atTop (𝓝 (T (π (resolventElement Q M) x))) at h1
  rw [heq] at h1
  exact tendsto_nhds_unique h1 h2
end F1Fecho.RepresentedRegularResolvent
#print axioms F1Fecho.RepresentedRegularResolvent.groupElement
#print axioms F1Fecho.RepresentedRegularResolvent.resolventElement
#print axioms F1Fecho.RepresentedRegularResolvent.windowElement
#print axioms F1Fecho.RepresentedRegularResolvent.windowElement_val
#print axioms F1Fecho.RepresentedRegularResolvent.represented_damped_phase
#print axioms F1Fecho.RepresentedRegularResolvent.represented_resolvent_commutes
