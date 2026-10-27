import OppositeNullSimultaneous
namespace F1Fecho.MaxwellGlobal
def momentumParitySignR (μ ν : Fin 4) : ℝ :=
  if (μ = 0 ∧ ν = 1) ∨ (μ = 1 ∧ ν = 0) ∨ (μ = 2 ∧ ν = 3) ∨ (μ = 3 ∧ ν = 2) ∨
    (μ = 1 ∧ ν = 2) ∨ (μ = 2 ∧ ν = 1) ∨ (μ = 1 ∧ ν = 3) ∨ (μ = 3 ∧ ν = 1)
  then 1 else -1
#eval momentumParitySignR 0 1
#eval momentumParitySignR 0 2
#eval momentumParitySignR 0 3
#eval momentumParitySignR 1 2
#eval momentumParitySignR 1 3
#eval momentumParitySignR 2 0
#eval momentumParitySignR 2 1
#eval momentumParitySignR 2 3
#eval momentumParitySignR 3 0
#eval momentumParitySignR 3 1
#eval momentumParitySignR 3 2
example : momentumParitySignR 0 2 = -1 := by norm_num [momentumParitySignR]
example : momentumParitySignR 1 2 = 1 := by norm_num [momentumParitySignR]
example : momentumParitySignR 2 3 = 1 := by norm_num [momentumParitySignR]
