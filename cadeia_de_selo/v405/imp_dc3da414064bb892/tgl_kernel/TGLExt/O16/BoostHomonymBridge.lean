import Lean
import TGLExt.ModularSignatureObstruction
import TGLExt.PoincareGroup

set_option autoImplicit false

/-!
# BoostHomonymBridge — a ponte do homônimo boost4 / boostMat, SEM depender do ANEXO A
  (cético final W5_final, 23/09/2026; scratchpad; separado de W5JetBridge para poder entrar no kernel
  independentemente da v3 do contrato). Conteúdo idêntico às duas primeiras declarações de
  W5JetBridge.lean (d906682a50bb262a). [DERIVED]. β não aparece. Sem sorry, sem axiom.
  ⚠ Homônimos NÃO ligados aqui: `TGLExt.boostMatrix` (ApproximateBoostFlow.lean:49 — plano x⁰–x³,
  parte ímpar = −sinh) e `boost` 2×2 (BisognanoWichmann.lean:55).
-/

namespace W5Final

/-- [DERIVED] as duas matrizes de boost do kernel coincidem entrada a entrada. -/
theorem boost4_eq_boostMat (s : ℝ) : ChatgptAudit.boost4 s = TGLExt.boostMat s := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [ChatgptAudit.boost4, TGLExt.boostMat]

/-- [DERIVED] a parede 2 reescrita com `boostMat`. -/
theorem no_injective_isometric_boostMat_intertwiner {H : Type*}
    [NormedAddCommGroup H] [NormedSpace ℝ H] (U : H →ₗᵢ[ℝ] H)
    (F : (Fin 4 → ℝ) →ₗ[ℝ] H) (hF : Function.Injective F) {s : ℝ}
    (hintertwine : ∀ v, U (F v) = F ((TGLExt.boostMat s).mulVec v)) : s = 0 :=
  ChatgptAudit.no_injective_isometric_boost_intertwiner U F hF
    (fun v => by rw [boost4_eq_boostMat]; exact hintertwine v)

#print axioms boost4_eq_boostMat
#print axioms no_injective_isometric_boostMat_intertwiner

end W5Final


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
