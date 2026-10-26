import CoherentMaxwellStressBoostR4
import RegularCoherentTransportR1
import RegularFockPointStressR4

/-! Canonical boost covariance of the point stress form on its actual
regular Fock domain. The transformed coefficients are unique. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt TGLExt.ImportedSQ F1Fecho.CoherentKernel F1Fecho.CovariantTensor
open F1Fecho.SpacetimeLorentz ChatgptAudit.WignerRapidityMeasure016

theorem finiteKernel_tensor_clm {ι : Type*} (L : TensorValue→L[ℂ]TensorValue)
    (M : ι→ι→TensorValue) (c d : ι→₀ℂ) :
    (fun μ ν=>finiteKernel (fun i j=>L (M i j) μ ν) c d)=
      L (fun μ ν=>finiteKernel (fun i j=>M i j μ ν) c d) := by
  have ht (N : ι→ι→TensorValue) :
      (fun μ ν=>finiteKernel (fun i j=>N i j μ ν) c d)=
        c.sum (fun i a=>d.sum (fun j b=>((starRingEnd ℂ) a*b) • N i j)) := by
    ext μ ν
    simp [finiteKernel,Finsupp.sum,Finset.sum_apply,smul_eq_mul]
  rw [ht,ht]
  simp only [Finsupp.sum,map_sum,map_smul]

theorem strongRegularProfile_B0_symm (s : ℝ) (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile ((B0 s).symm h) := by
  rw [orbitalBoostUnitary_symm_apply 0 s h]
  exact strongRegularProfile_B0 (-s) h hh

theorem pointStressForm_boost (s : ℝ) (ψ χ : regularFockDomain) (x : Spacetime) :
    (fun μ ν=>pointStressForm (regularGamma (B0 s) (strongRegularProfile_B0 s) ψ)
      (regularGamma (B0 s) (strongRegularProfile_B0 s) χ) μ ν x)=
      pull (complexBoost (-s))
        (fun μ ν=>pointStressForm ψ χ μ ν ((action (theBoost s)).symm x)) := by
  unfold pointStressForm
  simp only [regularCoefficients_gamma (B0 s) (strongRegularProfile_B0 s)
    (strongRegularProfile_B0_symm s),finiteKernel_reindex]
  have he (h k : RegularLabel) :
      (fun μ ν=>coherentProfileStress
        (regularLabelEquiv (B0 s) (strongRegularProfile_B0 s)
          (strongRegularProfile_B0_symm s) h).val
        (regularLabelEquiv (B0 s) (strongRegularProfile_B0 s)
          (strongRegularProfile_B0_symm s) k).val μ ν x)=
      pull (complexBoost (-s))
        (fun μ ν=>coherentProfileStress h.val k.val μ ν ((action (theBoost s)).symm x)) :=
    coherentProfileStress_boost s h.val k.val h.property.1 k.property.1 x
  have he' (h k : RegularLabel) (μ ν : Fin 4) := congrFun (congrFun (he h k) μ) ν
  simp_rw [he']
  exact finiteKernel_tensor_clm _ _ _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.finiteKernel_tensor_clm
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_boost
