import TGLExt.F1Fecho394.GenericClosedEquationsCFCR5
import TGLExt.F1Fecho394.CanonicalFockPolarRightCutsR3
import TGLExt.F1Fecho394.RegularScalarGNSContinuityR2
import TGLExt.F1Fecho394.CanonicalFockPolarRightAlgebraR6
import TGLExt.F1Fecho394.CanonicalFockGNSClosednessR5
import TGLExt.F1Fecho394.CanonicalFockGNSOrderR4
import TGLExt.F1Fecho394.CanonicalFockRegularRightGNSR11
import TGLExt.F1Fecho394.GeneralSineResolventApproxR2
import TGLExt.F1Fecho394.GeneralRegularCutoffCFCR1
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import TGLExt.F1Fecho394.CanonicalFockWeightSandwichR5
import TGLExt.F1Fecho394.GenericHilbertStarNormOrderR1

-- BEGIN SOURCE CanonicalFockPolarRightClosureR4
/-! Closure, strong-star transport and cutoff consequences on the SAME Fock
GNS. The regular-unitary polar identity remains explicit until its separate
actual polar consumer. Reuses V351 modules as incorporated in v393. -/
/-! Norm closure and ambient functional calculus for the actual polar-right
identity algebra. The antiunitary remains explicit until its concrete polar
consumer; the full-weight embedding is identified by proven cut maps. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (RegularHilbert dualOrbitRepresentation operatorFieldLift dualIntegralFamily operatorFieldLift_norm_le antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSCuts F1Fecho.CanonicalFockGNSClosedness
open scoped Topology
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- Closedness uses bounded cut identities, not a false finite-minorant
characterization of the nontracial weight. -/
theorem scalarPolarRight_isClosed  :
    IsClosed {b : core.toStarSubalgebra | ScalarPolarRight J b} := by
  have hπ : Continuous scalarGNSRepresentation :=
    RegularScalarGNSContinuity.representation_continuous weightContext
  have hdual : Continuous (dualOrbitRepresentation (H := F)) :=
    RegularScalarGNSContinuity.dual_representation_continuous (H := F)
  apply GenericClosedEquationsCFC.isClosed_of_equations
    (fun b : core.toStarSubalgebra => ScalarPolarRight J b)
    (fun (A : scalarWeightLeftIdeal) (n : ℕ) b => scalarGNSCutMap (n : ℝ)
      (antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)))
    (fun (A : scalarWeightLeftIdeal) (n : ℕ) b =>
      dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum (n : ℝ)))
    (scalarPolarRight_iff_cuts J)
  · intro A n
    simp only [antiunitaryConjugate_apply]
    exact (scalarGNSCutMap (n : ℝ)).continuous.comp
      (J.continuous.comp ((hπ.comp continuous_star).clm_apply continuous_const))
  · intro A n
    exact (hdual.comp ((GenericClosedEquationsCFC.continuous_left_mul A.val.val).comp continuous_subtype_val)).clm_apply continuous_const

theorem scalarPolarRightAlgebra_isClosed  :
    IsClosed (scalarPolarRightAlgebra J : Set core.toStarSubalgebra) :=
  (scalarPolarRight_isClosed J).inter ((scalarPolarRight_isClosed J).preimage continuous_star)


/-- Consume the ambient CFC, using a norm-closed image of the actual
right-identity algebra. No CFC or completeness of the core subtype is assumed. -/
theorem scalarRightAction_cfc 
    (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ core.toStarSubalgebra,
      (⟨cfc f b.val,hf⟩ : core.toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  exact GenericClosedEquationsCFC.closed_subalgebra_cfc core.toStarSubalgebra
    (RegularScalarGNSContinuity.algebra_norm_closed core)
    (scalarPolarRightAlgebra J) (scalarPolarRightAlgebra_isClosed J) b hb f


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_iff_cuts
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_isClosed
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra_isClosed
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_cfc

/-! Preserve the explicit polar-right identity under bounded strong-star limits on the same GNS; the approximants remain explicit inputs. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
open F1Fecho.CanonicalFockGNSClosedness F1Fecho.CanonicalFockGNSOrder
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- Pass a proved right identity to an actual bounded strong-star limit.
The approximating family is an input, not asserted to exist by this theorem. -/
theorem scalarRightAction_closed_of_bounded_strongStar 
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → core.toStarSubalgebra)
    (B : core.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal,
      scalarWeightGNSEmbedding ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star (b i))) (scalarWeightGNSEmbedding A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal,
      scalarWeightGNSEmbedding ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star B)) (scalarWeightGNSEmbedding A) := by
  let T (i : ι) : scalarWeightLeftIdeal := ⟨A.val*b i,(hact i).choose⟩
  have hnorm (i : ι) : ‖(star (b i)).val‖ ≤ C := by
    change ‖star (b i).val‖ ≤ C
    simpa only [norm_star] using hbound i
  have hp : Tendsto (fun i => scalarGNSRepresentation (star (b i))
      (J.symm (scalarWeightGNSEmbedding A))) l
      (𝓝 (scalarGNSRepresentation (star B) (J.symm (scalarWeightGNSEmbedding A)))) :=
    scalarGNSRepresentation_tendsto_of_uniformly_bounded
      (fun i => star (b i)) (star B) C hnorm hadjoint
        (J.symm (scalarWeightGNSEmbedding A))
  have hj : Tendsto (fun i => J (scalarGNSRepresentation (star (b i))
      (J.symm (scalarWeightGNSEmbedding A)))) l
      (𝓝 (J (scalarGNSRepresentation (star B) (J.symm (scalarWeightGNSEmbedding A))))) :=
    J.continuous.continuousAt.tendsto.comp hp
  have hgns : Tendsto (fun i => scalarWeightGNSEmbedding (T i)) l
      (𝓝 (antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star B)) (scalarWeightGNSEmbedding A))) := by
    have hi (i : ι) : scalarWeightGNSEmbedding (T i) =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star (b i))) (scalarWeightGNSEmbedding A) :=
      (hact i).choose_spec
    change Tendsto (fun i => scalarWeightGNSEmbedding (T i)) l
      (𝓝 (J (scalarGNSRepresentation (star B) (J.symm (scalarWeightGNSEmbedding A)))))
    exact hj.congr' (Eventually.of_forall (fun i => (hi i).symm))
  apply scalarWeightGNSEmbedding_closed_of_bounded_strong T (A.val*B) _
    (‖A.val.val‖*C) _ _ hgns
  · intro i
    exact (norm_mul_le A.val.val (b i).val).trans
      (mul_le_mul_of_nonneg_left (hbound i) (norm_nonneg A.val.val))
  · intro x
    exact A.val.val.continuous.continuousAt.tendsto.comp (hstrong x)

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_closed_of_bounded_strongStar
