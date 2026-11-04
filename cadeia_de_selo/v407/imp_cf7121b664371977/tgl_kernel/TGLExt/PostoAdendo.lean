import TGLExt.Posto
import TGLExt.QuantumCollapseWitness
import TGLExt.TheNameOperator
set_option autoImplicit false

/-!
# ADENDO da pedra do rank (`TGLExt.Posto`): F1.FREQUENCIA, trilha POSTO, partes A1.a-A5 (cadeia v392, 13/10/2026)

**[DERIVED]** ADENDO ADITIVO do pre-registro da F1.FREQUENCIA (`frequencia_defasa_12out/5_R3/ADENDO_PREREGISTRO_ADITIVO_R3.md`,
congelado em `FREEZE_R3.json` antes de qualquer ensaio). Cada parte e UM teorema nomeado, com o esperado `PASSA_K` fixado ANTES
do ensaio. O ensaio e ESTE: a compilacao no sandbox da v392, sem parametro ajustado a dado. As partes ligam ao MESMO termo do
kernel o `D_infinito` da face (`diagExpect`), o colapso tipado do canone no qubit (`ChatgptAudit.Collapse057.qubitReduction`) e o
Operador do Nome de `rhoStar` (`TGLExt.nameOp rhoStar`):

* `A1a`: a leitura zero do canone e a unidade da trilha (`readoutZero = rhoStar`);
* `A1b`: o colapso tipado do canone E o `diagExpect` em M2(C);
* `A1c`: o Operador do Nome de `rhoStar` E o `diagExpect` em M2(C);
* `A1d`: o ponto final da trilha, `diagExpect (rhoOut theta)`, e o Nome de `rhoStar` aplicado a `rhoOut theta`;
* `A2`: sobre a superposicao PURA o colapso tipado SOBE o posto (1 -> 2) e preserva o traco;
* `A3`: os dois polos da nao-defasagem, `rhoStar` e `Q0`, tem traco 1 e posto 1;
* `A4`: a forma incondicional (sem `c : TGLCoupling`) do negativo: o posto NAO e preservado pela defasagem (testemunha theta = pi/4);
* `A5` (controle): sobre a MISTURA o colapso tipado nao muda o posto; o que sobe o posto e a superposicao pura.

**O que o adendo NAO afirma:** colapso fisico, selecao na natureza ou medicao real (o `qubitReduction` e um canal tipado); que o
Operador do Nome em dimensao geral seja `D_infinito` (so em M2(C) e so para `p = rhoStar`); que o posto se perca em toda base (a base
e [INPUT]); qualquer palavra do gate. `beta` nao aparece. **O `1` que sobrevive ao colapso tipado e o TRACO (omega(I) = 1), nao o
posto.**

Estatuto: autoria da cadeia v392 (gerencia c1); **SEM auditoria independente da cadeia ainda** (quem constroi nao aprova). As partes
A1.a-A1.d, A2 e A3 ja tinham medicao anterior (sonda `AuditorEstatutoR2.lean`, sha16 `512ea820918c178f`, do auditor de estatuto da
rodada 2); A4 e a sonda S3 do auditor de reproducao; A5 nao tinha medicao anterior.
-/

open Matrix TGLExt TGLExt.Posto

namespace TGLExt.PostoAdendo

/-- A1.a: a leitura zero do canone e a unidade da trilha. -/
theorem A1a_readoutZero_eq_rhoStar : ChatgptAudit.Collapse057.readoutZero = rhoStar := by
  rw [rhoStar_eq]
  rfl

/-- A1.b: o colapso tipado do qubit e a esperanca diagonal `D_infinito`. -/
theorem A1b_qubitReduction_eq_diagExpect (x : Matrix (Fin 2) (Fin 2) ℂ) :
    ChatgptAudit.Collapse057.qubitReduction x = diagExpect x := by
  rw [ChatgptAudit.Collapse057.qubit_reduction_formula]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect]

/-- A1.c: o Operador do Nome de `rhoStar` e `D_infinito` em M2(C). -/
theorem A1c_nameOp_rhoStar_eq_diagExpect (x : Matrix (Fin 2) (Fin 2) ℂ) :
    TGLExt.nameOp rhoStar x = diagExpect x := by
  rw [← A1a_readoutZero_eq_rhoStar]
  exact A1b_qubitReduction_eq_diagExpect x

/-- A1.d: o ponto final da trilha e o Nome de `rhoStar` aplicado a `F_theta(1)`. -/
theorem A1d_endpoint_is_the_name_of_the_one (θ : ℝ) :
    diagExpect (rhoOut θ) = TGLExt.nameOp rhoStar (rhoOut θ) :=
  (A1c_nameOp_rhoStar_eq_diagExpect _).symm

/-- A2: o colapso tipado SOBE o posto da superposicao pura (1 -> 2) e preserva o traco. -/
theorem A2_typed_collapse_raises_rank_of_superposition :
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

/-- A3: os dois polos da nao-defasagem sao as duas faces sozinhas, ambas de traco 1 e posto 1. -/
theorem A3_nondephasing_poles_are_rank_one_units :
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

/-- A4: sem `c : TGLCoupling`, o posto NAO e preservado pela defasagem (theta = pi/4 e a testemunha). -/
theorem A4_rank_not_preserved_unconditional :
    ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro h
  have h1 := h (Real.pi / 4)
  rw [(endpoint_rank_two_iff _).mpr probe_angles.1, (fractal_one_is_rank_one _).1] at h1
  exact absurd h1 (by norm_num)

/-- A5 (controle): sobre a mistura o colapso tipado nao muda o posto (2 -> 2). -/
theorem A5_control_mixture_rank_unchanged :
    (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.mixedDensity).rank = 2
    ∧ ChatgptAudit.Collapse057.mixedDensity.rank = 2 := by
  have hr : ChatgptAudit.Collapse057.mixedDensity.rank = 2 := by
    rw [rank_two_iff, Matrix.det_fin_two]
    simp [ChatgptAudit.Collapse057.mixedDensity]
  have hq : ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.mixedDensity
      = ChatgptAudit.Collapse057.mixedDensity := by
    have h1 := ChatgptAudit.Collapse057.qubit_reduction_idempotent ChatgptAudit.Collapse057.plusDensity
    rw [ChatgptAudit.Collapse057.opposite_phases_same_reduction.1] at h1
    exact h1
  exact ⟨by rw [hq]; exact hr, hr⟩

end TGLExt.PostoAdendo
