import TGLExt.F1Fecho394.CanonicalFockActualRootCutFormsR2
import TGLExt.F1Fecho394.CanonicalFockFiniteStarCoreR1

/-! DECLARADO / UNCOMPILED CANDIDATE, R49, 2026-10-16.
Tracial square equality on the existing finite star-core of the SAME Fock
regular algebra and original scalar-weight GNS. The closed original Tomita
extends adjunction on this core; its proved polar factorization supplies the
root vector used in ActualRootCutFormsR2. Both inverse suprema are the existing
all-positive-regulator weights, not new definitions of a trace.
The proof pattern of V351QuadraticTrace is reused at the concrete Fock objects;
no SiteProfile, new trace/balance/regularity premise, or replacement GNS occurs.
The public final interface accepts exactly the finiteDualStarCore membership
needed by GeneralInverseFiniteApproximationR1.inverseSupremum_tracial_iff_core.
The bounded-core extension is a separate consumer. Total trace/PF remain open.
Native dictionaries and heartbeat limits are retained from R48.
Require EXIT0 and all four public axiom reports before calling this compiled. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockActualStarCoreTracialR1
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace weightContext)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (regularFockVacuum)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal finiteDualLeftIdeal_le_scalarWeight)
open F1Fecho.CanonicalFockWeightCompletion (scalarWeightGNSEmbedding scalarWeightGNSEmbedding_uniform)
open F1Fecho.CanonicalFockWeightClosedTomita (closedTomitaDomain closedTomita extends_star)
open F1Fecho.CanonicalFockWeightPolar (scalarTomitaPositiveRoot
  scalarClosedTomitaDomain_le_root scalarTomitaPolarFactor_root)
open F1Fecho.CanonicalFockActualModularBalanceR6 (J)
open F1Fecho.CanonicalFockActualDoubleCutR2 (C)
open F1Fecho.CanonicalFockActualRootCutFormsR2
  (actual_root_cut_supremum inverseSupremum_square_form)
open F1Fecho.RegularScalarTomitaGraph (finiteStarCore scalarGNSStarEmbedding)
open F1Fecho.RegularScalarClosedTomita (scalarStarCore_mem_closedTomitaDomain)
open F1Fecho.RegularInverseWeight (inverseSupremum)
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open scoped ENNReal

private abbrev nativeNormedAddCommGroup : NormedAddCommGroup GNSHilbert := inferInstance
private abbrev nativeInnerProductSpace : InnerProductSpace ℂ GNSHilbert := inferInstance
private abbrev nativeNormedSpace : NormedSpace ℂ GNSHilbert := inferInstance
private abbrev nativeModule : Module ℂ GNSHilbert := inferInstance
private abbrev nativeTopologicalSpace : TopologicalSpace GNSHilbert := inferInstance
private abbrev nativeUniformSpace : UniformSpace GNSHilbert := inferInstance
private abbrev nativeCompleteSpace : CompleteSpace GNSHilbert :=
  F1Fecho.CanonicalFockGNS.gnsCompleteSpace
private abbrev nativeStar : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
attribute [local instance] nativeNormedAddCommGroup nativeInnerProductSpace
  nativeNormedSpace nativeModule nativeTopologicalSpace nativeUniformSpace
  nativeCompleteSpace nativeStar

abbrev UniformStarCore := finiteStarCore weightContext

/-- Inclusion of the already finite uniform star-core into the scalar-weight ideal. -/
def starCoreWeightInput (a : UniformStarCore) : scalarWeightLeftIdeal :=
  Submodule.inclusion finiteDualLeftIdeal_le_scalarWeight ⟨a.val,a.property.1⟩

theorem uniform_embedding (a : UniformStarCore) :
    scalarWeightGNSEmbedding (starCoreWeightInput a) = scalarGNSStarEmbedding weightContext a :=
  scalarWeightGNSEmbedding_uniform ⟨a.val,a.property.1⟩
#print axioms uniform_embedding

/-- Original closed Tomita domain, followed by the proved domain inclusion. -/
def starCoreRootInput (a : UniformStarCore) : scalarTomitaPositiveRoot.domain :=
  Submodule.inclusion scalarClosedTomitaDomain_le_root
    ⟨scalarGNSStarEmbedding weightContext a,scalarStarCore_mem_closedTomitaDomain a⟩

/-- The adjoint core vector is obtained from the original Tomita graph. -/
theorem starCore_root_eq_inverse_polar (a : UniformStarCore) :
    J.symm (scalarGNSStarEmbedding weightContext (star a)) =
      scalarTomitaPositiveRoot (starCoreRootInput a) := by
  have hroot : J (scalarTomitaPositiveRoot (starCoreRootInput a)) =
      scalarGNSStarEmbedding weightContext (star a) :=
    (scalarTomitaPolarFactor_root (starCoreRootInput a)).trans (extends_star a)
  exact J.injective ((J.apply_symm_apply _).trans hroot.symm)
#print axioms starCore_root_eq_inverse_polar

/-- Restriction of the previously identified all-regulator supremum. -/
theorem inverseSupremum_uniform_square_form (a : UniformStarCore) :
    inverseSupremum fockFlow regularFockVacuum (star a.val.val*a.val.val) =
      ⨆ n : ℕ, ENNReal.ofReal
        (inner ℂ (J.symm (scalarGNSStarEmbedding weightContext a))
          (C (1/((n : ℝ)+1)) (J.symm (scalarGNSStarEmbedding weightContext a)))).re :=
  (inverseSupremum_square_form (starCoreWeightInput a)).trans
    (congrArg (fun v : GNSHilbert =>
      ⨆ n : ℕ, ENNReal.ofReal
        (inner ℂ (J.symm v) (C (1/((n : ℝ)+1)) (J.symm v))).re)
      (uniform_embedding a))
#print axioms inverseSupremum_uniform_square_form

-- The antiunitary inner-product conversion is proved before specialization,
-- so Lean need not rediscover the native GNS dictionaries in a concrete simp.
private theorem conjugated_form_re
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (V : H →L[ℂ] H) (x : H) :
    (inner ℂ x (antiunitaryConjugate j V x)).re =
      (inner ℂ (j.symm x) (V (j.symm x))).re := by
  have he := ChatgptAudit.Continuous050.antiunitary_inner_conj j
    (j.symm x) (V (j.symm x))
  simp only [LinearIsometryEquiv.apply_symm_apply] at he
  have hr := congrArg Complex.re he
  simpa only [antiunitaryConjugate_apply,Complex.star_def,Complex.conj_re] using hr

/-- The exact finite-star-core interface required by the bounded-core extension.
No traciality or polar balance is an input to this theorem. -/
theorem inverseSupremum_star_core (a : core.toStarSubalgebra)
    (ha : a ∈ F1Fecho.RegularFiniteStarCore.finiteDualStarCore fockFlow M) :
    inverseSupremum fockFlow regularFockVacuum (star a.val*a.val) =
      inverseSupremum fockFlow regularFockVacuum (a.val*star a.val) := by
  let b : UniformStarCore := ⟨a,ha⟩
  let x : scalarTomitaPositiveRoot.domain := starCoreRootInput b
  let y : GNSHilbert := scalarTomitaPositiveRoot x
  have hy : J.symm (scalarGNSStarEmbedding weightContext (star b)) = y :=
    starCore_root_eq_inverse_polar b
  have he :
      inverseSupremum fockFlow regularFockVacuum
        (star (star b).val.val*(star b).val.val) =
      inverseSupremum fockFlow regularFockVacuum (star b.val.val*b.val.val) := by
    calc
      _ = ⨆ n : ℕ, ENNReal.ofReal
          (inner ℂ (J.symm (scalarGNSStarEmbedding weightContext (star b)))
            (C (1/((n : ℝ)+1))
              (J.symm (scalarGNSStarEmbedding weightContext (star b))))).re :=
        inverseSupremum_uniform_square_form (star b)
      _ = ⨆ n : ℕ, ENNReal.ofReal (inner ℂ y (C (1/((n : ℝ)+1)) y)).re :=
        congrArg (fun v : GNSHilbert =>
          ⨆ n : ℕ, ENNReal.ofReal (inner ℂ v (C (1/((n : ℝ)+1)) v)).re) hy
      _ = ⨆ n : ℕ, ENNReal.ofReal
          (inner ℂ (x : GNSHilbert)
            (antiunitaryConjugate (H := GNSHilbert) J
              (C (1/((n : ℝ)+1))) x)).re := actual_root_cut_supremum x
      _ = ⨆ n : ℕ, ENNReal.ofReal
          (inner ℂ (J.symm (scalarGNSStarEmbedding weightContext b))
            (C (1/((n : ℝ)+1))
              (J.symm (scalarGNSStarEmbedding weightContext b)))).re := by
        apply congrArg (fun f : ℕ → ℝ≥0∞ => ⨆ n, f n)
        exact funext (fun n => congrArg ENNReal.ofReal
          (@conjugated_form_re GNSHilbert nativeNormedAddCommGroup
            nativeInnerProductSpace nativeCompleteSpace J (C (1/((n : ℝ)+1)))
            (scalarGNSStarEmbedding weightContext b)))
      _ = inverseSupremum fockFlow regularFockVacuum (star b.val.val*b.val.val) :=
        (inverseSupremum_uniform_square_form b).symm
  change inverseSupremum fockFlow regularFockVacuum (star (star a.val)*star a.val) =
    inverseSupremum fockFlow regularFockVacuum (star a.val*a.val) at he
  symm
  simpa only [star_star] using he
#print axioms inverseSupremum_star_core

end F1Fecho.CanonicalFockActualStarCoreTracialR1
