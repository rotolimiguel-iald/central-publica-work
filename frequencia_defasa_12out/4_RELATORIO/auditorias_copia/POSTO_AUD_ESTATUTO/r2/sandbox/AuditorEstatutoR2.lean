import TheUnitIsTheRank
import TGLExt.QuantumCollapseWitness
import TGLExt.TheNameOperator

/-!
# SONDA DO AUDITOR DE ESTATUTO (rodada 2) — F1.FREQUENCIA, trilha POSTO
  [SANDBOX do auditor; NÃO é pedra candidata; não entra em lugar nenhum; serve só para medir três afirmações
   de estatuto do relatório de auditoria.]

* (a) o D_∞ da pedra (diagExpect) em M₂(ℂ) é o OPERADOR DO NOME de ρ* (`TGLExt.nameOp`, pedra 115) e é o colapso
  tipado do cânone no qubit (`ChatgptAudit.Collapse057.qubitReduction`, ENTREGA_057);
* (b) esse colapso tipado leva a superposição |+⟩⟨+| (posto 1) a I/2 (posto 2) e preserva o traço;
* (c) os dois polos da não-defasagem (θ = 0 e θ = π/2) são as duas faces sozinhas, ρ* e Q₀, ambas de traço 1 e posto 1.
-/

open Matrix TGLExt TGLExt.TheUnitIsTheRank

namespace AuditorEstatutoR2

/-- (a) ρ* é o `readoutZero` da ENTREGA_057. -/
theorem readoutZero_eq_rhoStar : ChatgptAudit.Collapse057.readoutZero = rhoStar := by
  rw [rhoStar_eq]
  rfl

/-- (a) o colapso tipado do qubit é a esperança diagonal D_∞. -/
theorem qubitReduction_eq_diagExpect (x : Matrix (Fin 2) (Fin 2) ℂ) :
    ChatgptAudit.Collapse057.qubitReduction x = diagExpect x := by
  rw [ChatgptAudit.Collapse057.qubit_reduction_formula]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect]

/-- (a) o Operador do Nome de ρ* é D_∞ em M₂(ℂ). -/
theorem nameOp_rhoStar_eq_diagExpect (x : Matrix (Fin 2) (Fin 2) ℂ) :
    TGLExt.nameOp rhoStar x = diagExpect x := by
  rw [← readoutZero_eq_rhoStar]
  exact qubitReduction_eq_diagExpect x

/-- (a) o ponto final da trilha é o Nome de ρ* aplicado a F_θ(1). -/
theorem endpoint_is_the_name_of_the_one (θ : ℝ) :
    diagExpect (rhoOut θ) = TGLExt.nameOp rhoStar (rhoOut θ) :=
  (nameOp_rhoStar_eq_diagExpect _).symm

/-- (b) o colapso tipado SOBE o posto da superposição pura (1 → 2) e preserva o traço. -/
theorem typed_collapse_raises_rank_of_superposition :
    ChatgptAudit.Collapse057.plusDensity.rank = 1
    ∧ (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.plusDensity).rank = 2
    ∧ (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.plusDensity).trace
        = ChatgptAudit.Collapse057.plusDensity.trace := by
  refine ⟨?_, ?_, ChatgptAudit.Collapse057.qubit_reduction_preserves_trace _⟩
  · rw [rank_one_iff_fin_two]
    refine ⟨fun h => ?_, ?_⟩
    · have h00 := congrFun (congrFun h 0) 0
      simp [ChatgptAudit.Collapse057.plusDensity] at h00
    · rw [Matrix.det_fin_two]
      simp [ChatgptAudit.Collapse057.plusDensity]
  · rw [ChatgptAudit.Collapse057.opposite_phases_same_reduction.1, rank_two_iff, Matrix.det_fin_two]
    simp [ChatgptAudit.Collapse057.mixedDensity]

/-- (c) os dois polos da não-defasagem são as duas faces sozinhas, ambas de traço 1 e posto 1. -/
theorem nondephasing_poles_are_rank_one_units :
    rhoOut 0 = rhoStar ∧ rhoOut (Real.pi / 2) = Q0
    ∧ rhoStar.trace = 1 ∧ rhoStar.rank = 1 ∧ Q0.trace = 1 ∧ Q0.rank = 1 := by
  refine ⟨rhoOut_zero, rhoOut_pi_div_two, rhoStar_trace, rhoStar_rank, ?_, ?_⟩
  · rw [Q0_eq, Matrix.trace_fin_two]
    simp
  · rw [rank_one_iff_fin_two]
    refine ⟨fun h => ?_, ?_⟩
    · have h11 := congrFun (congrFun h 1) 1
      rw [Q0_eq] at h11
      simp at h11
    · rw [Q0_eq, Matrix.det_fin_two]
      simp

end AuditorEstatutoR2

#print axioms AuditorEstatutoR2.readoutZero_eq_rhoStar
#print axioms AuditorEstatutoR2.qubitReduction_eq_diagExpect
#print axioms AuditorEstatutoR2.nameOp_rhoStar_eq_diagExpect
#print axioms AuditorEstatutoR2.endpoint_is_the_name_of_the_one
#print axioms AuditorEstatutoR2.typed_collapse_raises_rank_of_superposition
#print axioms AuditorEstatutoR2.nondephasing_poles_are_rank_one_units
