import TGLExt.F1Fecho394.CanonicalFockFiniteWeightR4
import TGLExt.V350FiniteDualStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockWeightDomain
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockFiniteWeight
open scoped ENNReal NNReal
noncomputable section

/-- Finiteness of the scalar weight, without a uniform bound on every vector. -/
def HasFiniteScalarSquare 
    (A : RegularHilbert F →L[ℂ] RegularHilbert F) : Prop :=
  dualQuadraticIntegral (star A * A) regularFockVacuum < ⊤

theorem HasFiniteScalarSquare.zero  :
    HasFiniteScalarSquare 0 := by
  simp [HasFiniteScalarSquare,dualQuadraticIntegral_zero]

theorem HasFiniteScalarSquare.left_mul 
    (B A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteScalarSquare A) : HasFiniteScalarSquare (B*A) :=
  (dualQuadraticIntegral_left_square_le B A regularFockVacuum).trans_lt
    (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hA)

theorem HasFiniteScalarSquare.add 
    (A B : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteScalarSquare A) (hB : HasFiniteScalarSquare B) :
    HasFiniteScalarSquare (A+B) := by
  have hb := dualQuadraticIntegral_mono _ _ (dualSquare_add_le A B) regularFockVacuum
  rw [dualQuadraticIntegral_smul_operator 2 (by norm_num),
    dualQuadraticIntegral_add _ _ (star_mul_self_nonneg A) (star_mul_self_nonneg B)] at hb
  exact hb.trans_lt (ENNReal.mul_lt_top ENNReal.ofReal_lt_top (ENNReal.add_lt_top.mpr ⟨hA,hB⟩))

theorem HasFiniteScalarSquare.smul  (c : ℂ)
    (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteScalarSquare A) : HasFiniteScalarSquare (c • A) := by
  simpa using HasFiniteScalarSquare.left_mul (c • 1) A hA

/-- The actual n_ν domain inside the same regular core. -/
def scalarWeightLeftIdeal  :
    Submodule ℂ (core).toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare A.val}
  zero_mem' := HasFiniteScalarSquare.zero 
  add_mem' := fun hA hB => HasFiniteScalarSquare.add _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteScalarSquare.smul c _ hA

theorem finiteDualLeftIdeal_le_scalarWeight  :
    finiteLeftIdeal ≤ scalarWeightLeftIdeal :=
  fun A hA => finiteSquare_scalar_finite A.val hA

theorem scalarWeightLeftIdeal_left_mul 
    (B A : (core).toStarSubalgebra) (hA : A ∈ scalarWeightLeftIdeal ) :
    B*A ∈ scalarWeightLeftIdeal := HasFiniteScalarSquare.left_mul B.val A.val hA

end
end F1Fecho.CanonicalFockWeightDomain
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeightDomain).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
