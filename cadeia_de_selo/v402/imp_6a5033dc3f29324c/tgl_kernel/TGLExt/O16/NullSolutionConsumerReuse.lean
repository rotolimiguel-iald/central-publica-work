import Lean
import TGLExt.O16.TeleologicalNullSolution_v2
set_option autoImplicit false
noncomputable section
namespace TGLExt.ContratoQGv31.ProbeResidual
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 MeasureTheory Matrix
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

def responseOf (a : Source → (Fin 4 → ℝ) → ℝ) : Source → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  fun f x => Matrix.diagonal ![0, 0, -(a f x), -(a f x)]

theorem areaDensity_responseOf (a : Source → (Fin 4 → ℝ) → ℝ) (f : Source) :
    areaDensity (responseOf a f) = a f := by
  funext x
  simp [areaDensity, responseOf]

/-- ★ (⟸) UMA SOLUÇÃO nn COVARIANTE HABITA H3 v3.1 (com o H2, o T, a classe e o elo dados). -/
def H3_of_null_solution (C2 : ContratoH2 W R N) (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (b : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U b ψ ∈ A)
    (hmc : ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy C2.Δit ψ k → k = 2 * Real.pi * nullPlaneCharge T ψ)
    (hAn : ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy C2.Δit ψ k ∧ k ≠ 0)
    (hcont : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)))
    (hflat : ∀ x ∈ rightWedge, screenBlockV31 (solderMetric4 (C2.E x)⁻¹) = -1)
    (S : NullSolution W T G A) : ContratoH3 W R N T where
  H2 := C2
  G := G
  G_pos := hG
  admissible := A
  admissible_unit := hAu
  vac_admissible := hAv
  admissible_translate := hAt
  modular_charge := hmc
  admissible_nontrivial := hAn
  energy_continuous := hcont
  background_screen_flat := hflat
  propagator := responseOf S.a
  propagator_zero := by
    funext x
    ext i j
    fin_cases i <;> fin_cases j <;> simp [responseOf, S.a_zero]
  propagator_covariant := by
    intro b f
    funext x
    simp only [responseOf, S.a_cov]
  response_symm := by
    intro ψ hψ x
    exact Matrix.diagonal_transpose _
  lightcone_gauge := by
    intro ψ hψ x
    funext i
    fin_cases i <;> simp [responseOf, nullDir, Matrix.mulVec_diagonal]
  theta := S.θ
  theta_is_expansion := by
    intro ψ hψ x
    rw [areaDensity_responseOf]
    exact S.a_deriv ψ hψ x
  raychaudhuri_einstein := S.θ_deriv

#print axioms responseOf
#print axioms areaDensity_responseOf
#print axioms H3_of_null_solution
end TGLExt.ContratoQGv31.ProbeResidual


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
