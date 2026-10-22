import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.O16.IdempotentDephasing_v2
open TGLExt.TheAxiomAndTheFalseWitness

#check @ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent

/-- teste da aferição (NÃO é pedra): a FIAÇÃO de `axiomFlow` ao termo canônico já auditado
    `ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent` (escalares reais). -/
theorem afericao_axiomFlow_eq_exp_via_O16 {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A]
    {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    NormedSpace.exp ((-t) • (1 - P)) = axiomFlow P t := by
  rw [ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent P hP.eq t]
  unfold axiomFlow
  rw [Complex.coe_smul]

#print axioms afericao_axiomFlow_eq_exp_via_O16
