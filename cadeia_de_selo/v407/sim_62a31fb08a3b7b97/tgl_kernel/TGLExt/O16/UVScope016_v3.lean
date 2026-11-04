import Lean
import Init

set_option autoImplicit false

/-!
A7.d — scope contracts only. The predicates below are NAMED INPUTS.
This file neither defines a type-III factor analytically nor constructs a
metric operator or a renormalized quantum theory. The final counterexample
is propositional bookkeeping, not a physical model.
-/
namespace ChatgptAudit.UVScope016

universe u v w

structure Problem where
  Algebra : Type u
  Operator : Type v
  Metric : Type w
  zeroOperator : Operator
  isTypeIII1 : Algebra → Prop
  metricSymmetric : Metric → Prop
  commonDenseDomain : Metric → Prop
  covariance : Metric → Prop
  classicalLimit : Metric → Prop
  finiteBreuerCorner : Prop
  renormalizedAllOrders : Prop
  interactingQME : Prop
  matchesPhysicalPair : Prop

/-- Route A: zero effective Hamiltonian is supplied, not inferred from type III. -/
structure ZeroEffectiveHamiltonianRoute (P : Problem) where
  algebra : P.Algebra
  typeIII1 : P.isTypeIII1 algebra
  effectiveHamiltonian : P.Operator
  effectiveHamiltonian_zero : effectiveHamiltonian = P.zeroOperator

/-- Route B: an actual candidate and its domain/covariance data must be supplied. -/
structure MetricOperatorRoute (P : Problem) where
  metric : P.Metric
  symmetric : P.metricSymmetric metric
  domain : P.commonDenseDomain metric
  covariant : P.covariance metric
  classical : P.classicalLimit metric

/-- These obligations are separate from BOTH route packages and corner finiteness. -/
structure Completion (P : Problem) : Prop where
  uv : P.renormalizedAllOrders
  qme : P.interactingQME
  physicalPair : P.matchesPhysicalPair

theorem completion_requires_uv (P : Problem) (h : Completion P) :
    P.renormalizedAllOrders := h.uv

theorem completion_requires_qme (P : Problem) (h : Completion P) :
    P.interactingQME := h.qme

theorem completion_requires_physical_pair (P : Problem) (h : Completion P) :
    P.matchesPhysicalPair := h.physicalPair

theorem unresolved_uv_blocks_completion (P : Problem) (h : ¬ P.renormalizedAllOrders) :
    ¬ Completion P := fun hC => h hC.uv

theorem unresolved_qme_blocks_completion (P : Problem) (h : ¬ P.interactingQME) :
    ¬ Completion P := fun hC => h hC.qme

theorem unresolved_pair_blocks_completion (P : Problem) (h : ¬ P.matchesPhysicalPair) :
    ¬ Completion P := fun hC => h hC.physicalPair

theorem completion_of_explicit_payments (P : Problem)
    (huv : P.renormalizedAllOrders) (hqme : P.interactingQME)
    (hp : P.matchesPhysicalPair) : Completion P := ⟨huv, hqme, hp⟩

/-! A logical countermodel to an INVALID generic implication. No physics is supplied. -/
def missingUV : Problem.{u, v, w} where
  Algebra := PUnit.{u+1}
  Operator := PUnit.{v+1}
  Metric := PUnit.{w+1}
  zeroOperator := PUnit.unit
  isTypeIII1 := fun _ => True
  metricSymmetric := fun _ => True
  commonDenseDomain := fun _ => True
  covariance := fun _ => True
  classicalLimit := fun _ => True
  finiteBreuerCorner := True
  renormalizedAllOrders := False
  interactingQME := False
  matchesPhysicalPair := False

def formalZeroRoute : ZeroEffectiveHamiltonianRoute missingUV.{u, v, w} where
  algebra := PUnit.unit
  typeIII1 := True.intro
  effectiveHamiltonian := PUnit.unit
  effectiveHamiltonian_zero := rfl

def formalMetricRoute : MetricOperatorRoute missingUV.{u, v, w} where
  metric := PUnit.unit
  symmetric := True.intro
  domain := True.intro
  covariant := True.intro
  classical := True.intro

theorem formal_routes_do_not_supply_completion :
    Nonempty (ZeroEffectiveHamiltonianRoute missingUV) ∧
    Nonempty (MetricOperatorRoute missingUV) ∧
    missingUV.finiteBreuerCorner ∧ ¬ Completion missingUV := by
  refine ⟨⟨formalZeroRoute⟩, ⟨formalMetricRoute⟩, True.intro, ?_⟩
  intro h
  exact h.uv

theorem finite_corner_is_not_a_generic_uv_proof :
    ¬ (∀ P : Problem, P.finiteBreuerCorner → P.renormalizedAllOrders) := by
  intro h
  exact h missingUV True.intro

theorem zero_route_is_not_a_generic_uv_proof :
    ¬ (∀ P : Problem, ZeroEffectiveHamiltonianRoute P → P.renormalizedAllOrders) := by
  intro h
  exact h missingUV formalZeroRoute

theorem metric_route_is_not_a_generic_uv_proof :
    ¬ (∀ P : Problem, MetricOperatorRoute P → P.renormalizedAllOrders) := by
  intro h
  exact h missingUV formalMetricRoute

#print axioms completion_requires_uv
#print axioms completion_requires_qme
#print axioms completion_requires_physical_pair
#print axioms unresolved_uv_blocks_completion
#print axioms unresolved_qme_blocks_completion
#print axioms unresolved_pair_blocks_completion
#print axioms completion_of_explicit_payments
#print axioms formal_routes_do_not_supply_completion
#print axioms finite_corner_is_not_a_generic_uv_proof
#print axioms zero_route_is_not_a_generic_uv_proof
#print axioms metric_route_is_not_a_generic_uv_proof

end ChatgptAudit.UVScope016


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
