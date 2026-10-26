import AppliedPhysicalBridgeR3
set_option autoImplicit false
set_option Elab.async false
noncomputable section
namespace AppliedBridgeReview
open F1Citations.AppliedBridge TGLExt.PonteDaEscalaDual
open F1Fecho.CanonicalFockModularCoreInputR1

theorem cut_is_inhabited : Nonempty FiniteTraceProjection := ⟨cut⟩
theorem cut_nonzero : cut.val ≠ 0 := by
  intro h
  have ht := cut_trace_one
  rw [h, physicalFockCertificate.trace_zero] at ht
  exact zero_ne_one ht

theorem same_cut_two_positive_masses :
    massSquared (lift physicalDualScaling 1 cut) = 1 ∧
    massSquared (lift physicalDualScaling 4 cut) = 4 ∧
    lift physicalDualScaling 1 cut ≠ lift physicalDualScaling 4 cut :=
  ⟨actual_core_mass_shell 1 cut, actual_core_mass_shell 4 cut,
   actual_core_does_not_select_mass⟩

theorem nonzero_dual_time_moves_the_cut : translatedCut 1 cut ≠ cut :=
  actual_cut_moves 1 (by norm_num)

theorem inner_implementation_refused (u v : physicalFockCertificate.Core)
    (h : v*u=1) :
    ¬ (∀ x, physicalFockCertificate.dualAction 1 x = u*x*v) :=
  actual_dual_not_inner 1 (by norm_num) u v h

#check appliedFullWitness
#check applied_qg_solution_end_to_end
#print axioms cut_is_inhabited
#print axioms cut_nonzero
#print axioms same_cut_two_positive_masses
#print axioms nonzero_dual_time_moves_the_cut
#print axioms inner_implementation_refused
end AppliedBridgeReview
