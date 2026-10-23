import TGLExt.V351InverseCutoffCFC

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section

/-- Evaluate the existing dual weight on a right perturbation of a square in its
existing GNS domain, using the same polar antiunitary. -/
theorem scalarWeight_right_perturbed_norm (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val * A.val.val) * b.val)
      (regularVacuum P) =
    ENNReal.ofReal (‖scalarGNSRepresentation P (star b)
      ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2) := by
  obtain ⟨hAb, he⟩ := hb.1 A
  calc
    _ = ENNReal.ofReal (‖scalarWeightGNSEmbedding P ⟨A.val*b,hAb⟩‖^2) := by
      have hn := scalarWeightGNSEmbedding_norm_sq P ⟨A.val*b,hAb⟩
      change ENNReal.ofReal (‖scalarWeightGNSEmbedding P ⟨A.val*b,hAb⟩‖^2) =
        dualQuadraticIntegral (star (A.val.val*b.val)*(A.val.val*b.val))
          (regularVacuum P) at hn
      simpa only [star_mul, mul_assoc] using hn.symm
    _ = ENNReal.ofReal (‖antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star b)) (scalarWeightGNSEmbedding P A)‖^2) :=
      congrArg (fun v : ScalarGNSHilbert P => ENNReal.ofReal (‖v‖^2)) he
    _ = _ := congrArg (fun r : ℝ => ENNReal.ofReal (r^2))
      ((scalarTomitaPolarFactor P).norm_map
        (scalarGNSRepresentation P (star b)
          ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))))

/-- The original inverse-generator cut and its original positive square root
instantiate the norm identity without a residual right-action hypothesis. -/
theorem scalarWeight_inverseCutoff_perturbed_norm (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (A : scalarWeightLeftIdeal P) :
    ∃ hb : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      dualQuadraticIntegral
        (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) *
          (star A.val.val * A.val.val) *
          hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P) =
      ENNReal.ofReal (‖scalarGNSRepresentation P
        (star (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hb⟩ :
          (regularCoreAlgebra P).toStarSubalgebra))
        ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2) := by
  obtain ⟨hb,hr⟩ := regularInverseGeneratorCutoff_sqrt_right P ε hε
  exact ⟨hb,scalarWeight_right_perturbed_norm P _ hr A⟩

end
end TGLV350.Regular
