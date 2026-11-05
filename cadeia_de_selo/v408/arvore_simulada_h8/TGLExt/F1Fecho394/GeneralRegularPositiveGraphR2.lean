import TGLExt.V351RegularPositiveGraph
import TGLExt.F1Fecho394.CoefficientBoostR1

/-! Generalization of the existing v351 regular positive generator to the
actual strongly continuous UnitaryFlow on H. The scalar multiplier, resolvent
graph and all their positivity results are reused. The positive generator is
not yet identified with the crossed-product implementer by this module. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- From the spectral L² coordinate to the original regular representation. -/
def regularSpectralCoordinates (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    RegularHilbert H ≃ₗᵢ[ℂ] RegularHilbert H :=
  (Lp.fourierTransformₗᵢ ℝ H).symm.trans
    (F1Fecho.CoefficientBoost.unitary B 1)

/-- The candidate (1+h)^{-1}, with the spectral function already in mathlib. -/
def regularSpectralResolvent (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    RegularHilbert H →L[ℂ] RegularHilbert H :=
  (regularSpectralCoordinates B).conjStarAlgEquiv
    (realScalarMultiplier (fun x => Real.sigmoid (2*Real.pi*x)) (by fun_prop)
      (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _))

theorem regularSpectralResolvent_nonneg (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    0 ≤ regularSpectralResolvent B := by
  exact map_nonneg (regularSpectralCoordinates B).conjStarAlgEquiv
    (realScalarMultiplier_nonneg _ _ _ _)

theorem regularSpectralResolvent_le_one (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    regularSpectralResolvent B ≤ 1 := by
  apply sub_nonneg.mp
  have h := map_nonneg (regularSpectralCoordinates B).conjStarAlgEquiv
    (sub_nonneg.mpr (realScalarMultiplier_le_one
      (H := H) (fun x => Real.sigmoid (2*Real.pi*x)) (by fun_prop)
      (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _)))
  simpa only [map_sub, map_one, regularSpectralResolvent] using h

theorem regularSpectralResolvent_injective (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    Function.Injective (regularSpectralResolvent B) :=
  (regularSpectralCoordinates B).injective.comp
    ((realScalarMultiplier_injective _ _ _ _ (fun _ => Real.sigmoid_pos _)).comp
      (regularSpectralCoordinates B).symm.injective)

theorem regularSpectralResolvent_complement_injective (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    Function.Injective (1-regularSpectralResolvent B :
      RegularHilbert H →L[ℂ] RegularHilbert H) := by
  let g : ℝ → ℝ := fun x => Real.sigmoid (2*Real.pi*x)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ x, 0 ≤ g x := fun x => Real.sigmoid_nonneg _
  have h1 : ∀ x, g x ≤ 1 := fun x => Real.sigmoid_le_one _
  change Function.Injective (1 - (regularSpectralCoordinates B).conjStarAlgEquiv
    (realScalarMultiplier g hg h0 h1) : _ →L[ℂ] _)
  rw [← map_one (regularSpectralCoordinates B).conjStarAlgEquiv,
    ← map_sub, realScalarMultiplier_complement]
  exact (regularSpectralCoordinates B).injective.comp
    ((realScalarMultiplier_injective _ _ _ _
      (fun x => sub_pos.mpr (Real.sigmoid_lt_one _))).comp
      (regularSpectralCoordinates B).symm.injective)

/-- A positive graph on the same regular Hilbert space. Its imaginary powers,
affiliation and dual scaling are subsequent obligations, not fields assumed here. -/
def regularPositiveGenerator (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    RegularHilbert H →ₗ.[ℂ] RegularHilbert H :=
  resolventGraphOperator (regularSpectralResolvent B) (regularSpectralResolvent_injective B)

theorem regularPositiveGenerator_closed (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    (regularPositiveGenerator B).IsClosed :=
  resolvent_graph_closed _ _

theorem regularPositiveGenerator_domain_dense (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    Dense ((regularPositiveGenerator B).domain : Set (RegularHilbert H)) :=
  resolvent_graph_domain_dense _ _ (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg B))

theorem regularPositiveGenerator_selfadjoint (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    IsSelfAdjoint (regularPositiveGenerator B) :=
  resolvent_graph_selfadjoint _ _ (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg B))

theorem regularPositiveGenerator_positive (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (x : (regularPositiveGenerator B).domain) :
    0 ≤ (inner ℂ (x : RegularHilbert H) (regularPositiveGenerator B x)).re :=
  resolvent_graph_positive _ _ (regularSpectralResolvent_nonneg B)
    (regularSpectralResolvent_le_one B) x

theorem regularPositiveGenerator_zero_kernel (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (x : (regularPositiveGenerator B).domain) (hx : regularPositiveGenerator B x = 0) :
    (x : RegularHilbert H) = 0 := by
  let R := regularSpectralResolvent B
  let hi := regularSpectralResolvent_injective B
  have h : (1-R) (Continuous049.boundedGraphParameter R hi x) = (1-R) 0 := by
    change regularPositiveGenerator B x = (1-R) 0
    rw [hx, map_zero]
  have hz := regularSpectralResolvent_complement_injective B h
  have he := Continuous049.bounded_graph_parameter_apply R hi x
  rw [hz, map_zero] at he
  exact he.symm


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralCoordinates
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_nonneg
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_le_one
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_injective
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_complement_injective
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_closed
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_domain_dense
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_selfadjoint
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_positive
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_zero_kernel
