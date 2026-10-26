import PhysicalMaxwellJointRealizationR2
import TGLExt.QGSolutionComplete
import TGLExt.PonteDaEscalaDual

/-!
Applied consumer, sandbox only. The concrete compact Maxwell net, canonical
Fock realization and regular-domain Wick stress replace abstract certificate
arguments. Existing theorems are reused, not re-proved. The historical QG
conclusion retains its separate v354 tower; the finite trace cut below belongs
to the actual Fock core. No equality of these two cuts is asserted.
H3 here is the fixed-null linearized response with local equilibrium input.
No universal nonlinear H3, physical mass selection, identification of the dual
action with BW, empirical energy calibration or type III1 classification follows.
The cyclic ENNReal extension is used only through its proved positive trace cut.
-/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Citations.AppliedBridge
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open F1Fecho.MaxwellLocalization F1Fecho.MaxwellGlobal
open F1Fecho.CanonicalFockModularCoreInputR1
open TGLExt.PonteDaEscalaDual

abbrev FiniteTraceProjection := {x : physicalFockCertificate.Core //
  star x = x ∧ x*x=x ∧ 0 < physicalFockCertificate.trace x ∧
    physicalFockCertificate.trace x < ⊤}

def cut : FiniteTraceProjection :=
  ⟨physicalFockCertificate.PF, physicalFockCertificate.PF_sa,
   physicalFockCertificate.PF_idem, physicalFockCertificate.PF_pos,
   physicalFockCertificate.PF_fin⟩

def translatedCut (s : ℝ) (a : FiniteTraceProjection) : FiniteTraceProjection := by
  refine ⟨physicalFockCertificate.dualAction s a.val, ?_, ?_, ?_, ?_⟩
  · rw [← map_star, a.property.1]
  · rw [← map_mul, a.property.2.1]
  · rw [physicalFockCertificate.trace_dual_scaling]
    exact mul_pos (ENNReal.ofReal_pos.mpr (Real.exp_pos _)) a.property.2.2.1
  · rw [physicalFockCertificate.trace_dual_scaling]
    exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top a.property.2.2.2

def physicalDualScaling : DualScalingData FiniteTraceProjection where
  tau a := (physicalFockCertificate.trace a.val).toReal
  theta := translatedCut
  scaling s a := by
    change (physicalFockCertificate.trace (physicalFockCertificate.dualAction s a.val)).toReal = _
    rw [physicalFockCertificate.trace_dual_scaling, ENNReal.toReal_mul,
      ENNReal.toReal_ofReal (Real.exp_pos _).le]

theorem physicalDualScaling_positive (a : FiniteTraceProjection) :
    0 < physicalDualScaling.tau a :=
  ENNReal.toReal_pos_iff.mpr ⟨a.property.2.2.1, a.property.2.2.2⟩

theorem cut_trace_one : physicalFockCertificate.trace cut.val = 1 :=
  modularCoreInput_PF_trace physicalCanonicalNet

theorem cut_tau_one : physicalDualScaling.tau cut = 1 := by
  change (physicalFockCertificate.trace cut.val).toReal = 1
  rw [cut_trace_one]; simp

theorem actual_core_mass_shell (mu2 : ℝ) (a : FiniteTraceProjection) :
    massSquared (lift physicalDualScaling mu2 a) = mu2 :=
  lift_mass physicalDualScaling mu2 a (ne_of_gt (physicalDualScaling_positive a))

theorem actual_core_equivariance (mu2 : ℝ) (a : FiniteTraceProjection) (s : ℝ) :
    lift physicalDualScaling mu2 (translatedCut s a) =
      theta s (lift physicalDualScaling mu2 a) :=
  lift_equivariant physicalDualScaling mu2 a s

theorem actual_core_does_not_select_mass :
    lift physicalDualScaling 0 cut ≠ lift physicalDualScaling 1 cut :=
  lift_mass_not_selected physicalDualScaling cut
    (ne_of_gt (physicalDualScaling_positive cut)) 0 1 zero_ne_one

theorem applied_qg_solution_end_to_end
    (N : KillingNormalization) (G : ℝ) (hG : 0 < G) {x₀ : Fin 4 → ℝ} (hx₀ : x₀ ∈ rightWedge)
    {ψ : physicalFockCertificate.F} (hψ : ψ ∈ (lightH3 (physicalMaxwellCertificate N) N G hG).admissible) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : (lightH3 (physicalMaxwellCertificate N) N G hG).theta ψ (x + d • nullDir) = 0) :
    (0 < (TGLV354.coreProjectionTraceSubadditive TGLExt.mixProfile).tau (TGLV354.regularSusyData TGLExt.mixProfile).ker
      ∧ (TGLV354.coreProjectionTraceSubadditive TGLExt.mixProfile).tau (TGLV354.regularSusyData TGLExt.mixProfile).ker < ⊤) ∧
    (TGLV354.coreProjectionTraceSubadditive TGLExt.mixProfile).tau (TGLV354.regularSusyData TGLExt.mixProfile).ker
      / (TGLV354.coreProjectionTraceSubadditive TGLExt.mixProfile).tau (TGLV354.regularSusyData TGLExt.mixProfile).ker = 1 ∧
    (((lightH3 (physicalMaxwellCertificate N) N G hG).H2.E x₀)⁻¹ * (lightH3 (physicalMaxwellCertificate N) N G hG).H2.E x₀ = 1
      ∧ LorentzByCongruence (solderMetric4 ((lightH3 (physicalMaxwellCertificate N) N G hG).H2.E x₀)⁻¹)) ∧
    ((lightH3 (physicalMaxwellCertificate N) N G hG).toHorizonData hψ x c d hθ).dQ = ((lightH3 (physicalMaxwellCertificate N) N G hG).toHorizonData hψ x c d hθ).kappa
      * ((lightH3 (physicalMaxwellCertificate N) N G hG).toHorizonData hψ x c d hθ).dA / (8 * Real.pi * ((lightH3 (physicalMaxwellCertificate N) N G hG).toHorizonData hψ x c d hθ).G) :=
  TGLExt.QGSolution.qg_solution_end_to_end physicalCanonicalNet.toLightNetData
    physicalFockCertificate (physicalMaxwellCertificate N) N G hG hx₀ hψ x c d hθ

end F1Citations.AppliedBridge
#print axioms F1Citations.AppliedBridge.FiniteTraceProjection
#print axioms F1Citations.AppliedBridge.cut
#print axioms F1Citations.AppliedBridge.translatedCut
#print axioms F1Citations.AppliedBridge.physicalDualScaling
#print axioms F1Citations.AppliedBridge.physicalDualScaling_positive
#print axioms F1Citations.AppliedBridge.cut_trace_one
#print axioms F1Citations.AppliedBridge.cut_tau_one
#print axioms F1Citations.AppliedBridge.actual_core_mass_shell
#print axioms F1Citations.AppliedBridge.actual_core_equivariance
#print axioms F1Citations.AppliedBridge.actual_core_does_not_select_mass
#print axioms F1Citations.AppliedBridge.applied_qg_solution_end_to_end
