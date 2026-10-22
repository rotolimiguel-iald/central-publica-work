import TGLExt.PostoAdendo
set_option autoImplicit false
set_option pp.fullNames true

-- Auditor cetico c1: os enunciados do ADENDO congelado (FREEZE_R3), reescritos com nomes TOTALMENTE qualificados
-- (TheUnitIsTheRank -> Posto, o nome dado pelo operador), fechados SO pelos teoremas da pedra. Se a pedra provasse
-- outra coisa (outro rhoStar, outro diagExpect), estes `theorem` nao fechariam.

theorem chk_A1a : ChatgptAudit.Collapse057.readoutZero = TGLExt.Posto.rhoStar :=
  TGLExt.PostoAdendo.A1a_readoutZero_eq_rhoStar

theorem chk_A1b : ∀ x : Matrix (Fin 2) (Fin 2) ℂ, ChatgptAudit.Collapse057.qubitReduction x = TGLExt.diagExpect x :=
  TGLExt.PostoAdendo.A1b_qubitReduction_eq_diagExpect

theorem chk_A1c : ∀ x : Matrix (Fin 2) (Fin 2) ℂ, TGLExt.nameOp TGLExt.Posto.rhoStar x = TGLExt.diagExpect x :=
  TGLExt.PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect

theorem chk_A1d : ∀ θ : ℝ, TGLExt.diagExpect (TGLExt.rhoOut θ) = TGLExt.nameOp TGLExt.Posto.rhoStar (TGLExt.rhoOut θ) :=
  TGLExt.PostoAdendo.A1d_endpoint_is_the_name_of_the_one

theorem chk_A2 : ChatgptAudit.Collapse057.plusDensity.rank = 1
    ∧ (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.plusDensity).rank = 2
    ∧ (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.plusDensity).trace
        = ChatgptAudit.Collapse057.plusDensity.trace :=
  TGLExt.PostoAdendo.A2_typed_collapse_raises_rank_of_superposition

theorem chk_A3 : TGLExt.rhoOut 0 = TGLExt.Posto.rhoStar ∧ TGLExt.rhoOut (Real.pi / 2) = TGLExt.Posto.Q0
    ∧ TGLExt.Posto.rhoStar.trace = 1 ∧ TGLExt.Posto.rhoStar.rank = 1
    ∧ TGLExt.Posto.Q0.trace = 1 ∧ TGLExt.Posto.Q0.rank = 1 :=
  TGLExt.PostoAdendo.A3_nondephasing_poles_are_rank_one_units

theorem chk_A4 : ¬ ∀ θ : ℝ, (TGLExt.diagExpect (TGLExt.rhoOut θ)).rank = (TGLExt.rhoOut θ).rank :=
  TGLExt.PostoAdendo.A4_rank_not_preserved_unconditional

theorem chk_A5 : (ChatgptAudit.Collapse057.qubitReduction ChatgptAudit.Collapse057.mixedDensity).rank = 2
    ∧ ChatgptAudit.Collapse057.mixedDensity.rank = 2 :=
  TGLExt.PostoAdendo.A5_control_mixture_rank_unchanged

-- os objetos, como o ADENDO os fixa (§0)
theorem chk_rhoStar_def : TGLExt.Posto.rhoStar = Matrix.single 0 0 1 := rfl
theorem chk_Q0_def : TGLExt.Posto.Q0 = 1 - TGLExt.Posto.rhoStar := rfl
example : ChatgptAudit.Collapse057.plusDensity = !![1/2, 1/2; 1/2, 1/2] := rfl
example : ChatgptAudit.Collapse057.mixedDensity = !![1/2, 0; 0, 1/2] := rfl
example : ChatgptAudit.Collapse057.readoutZero = !![1, 0; 0, 0] := rfl

#check @TGLExt.PostoAdendo.A1a_readoutZero_eq_rhoStar
#check @TGLExt.PostoAdendo.A4_rank_not_preserved_unconditional
#print axioms chk_A1a
#print axioms chk_A5
