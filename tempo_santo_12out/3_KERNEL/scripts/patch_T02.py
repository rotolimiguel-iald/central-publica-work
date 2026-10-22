"""Patch T01 -> T02: corrige os 4 erros da compilacao T01 (logs/T01_saida.txt), limpa os 7 avisos de linter e
acrescenta os CONTRAEXEMPLOS de cada «se e so se» (pedido da tarefa). Cada substituicao exige padrao UNICO."""
import sys

p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
s = open(p, encoding="utf-8").read()


def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)


# E1 (l.288) sonda L2: timeout de whnf ao reenunciar a conclusao nas instancias default. Agora: so se
# instancia o teorema (hipoteses habitadas) em M2(C) com a norma L2, com folga de heartbeats; e uma segunda
# sonda robusta em A = C.
R("""theorem probe_bounded_spectral_translation :
    ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)⁻¹ : Matrix (Fin 2) (Fin 2) ℂ) * 0
        * ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ)
      ≠ 0 + algebraMap ℂ (Matrix (Fin 2) (Fin 2) ℂ) 1 := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  exact no_bounded_spectral_translation 1 0 one_ne_zero""",
  """set_option maxHeartbeats 4000000 in
theorem probe_bounded_spectral_translation : True := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  have _h := no_bounded_spectral_translation (A := Matrix (Fin 2) (Fin 2) ℂ) 1 0 (one_ne_zero (α := ℂ))
  trivial""")
R("""end L2Probe
""", """end L2Probe

/-- Sonda V-T2-b (segunda instância, comutativa): `A = ℂ`, `V = 1`, `H = 0`, `s = 1`. -/
theorem probe_bounded_spectral_translation_complex :
    ((1 : ℂˣ)⁻¹ : ℂ) * 0 * ((1 : ℂˣ) : ℂ) ≠ 0 + algebraMap ℂ ℂ 1 :=
  no_bounded_spectral_translation 1 0 one_ne_zero
""")
# E2 (l.591) injetividade de (2/3, 1/3)
R("""    (fun a b h => by fin_cases a <;> fin_cases b <;> norm_num at h ⊢) psiPlus]""",
  """    (fun a b h => by fin_cases a <;> fin_cases b <;> first | rfl | (norm_num at h)) psiPlus]""")
# E3 (l.753) Liouville linear: o limite das potencias do determinante
R("""  rw [Matrix.det_zero ⟨⟨0, hm⟩⟩] at hdet
  simp_rw [Matrix.det_pow] at hdet
  by_contra hge
  push_neg at hge
  have hone : ∀ k : ℕ, 1 ≤ |L.det ^ k| := fun k => by
    rw [abs_pow]; exact one_le_pow₀ hge
  have habs : Filter.Tendsto (fun k : ℕ => |L.det ^ k|) Filter.atTop (nhds 0) := by
    have := (continuous_abs.tendsto (0 : ℝ)).comp hdet
    simpa using this
  have hle : (1 : ℝ) ≤ 0 := ge_of_tendsto habs (Filter.Eventually.of_forall hone)
  linarith""", """  rw [Matrix.det_zero ⟨⟨0, hm⟩⟩] at hdet
  simp_rw [Matrix.det_pow] at hdet
  exact tendsto_pow_atTop_nhds_zero_iff.mp hdet""")
# E4 (l.915) seta: normalizar o expoente antes do linarith
R("""  show purityR (dephase (gRate 1) (-1) psiPlus) > purityR psiPlus
  rw [probe_psiPlus_purity, purityR_dephase]
  simp only [Fin.sum_univ_two, gRate_00, gRate_01, gRate_10, gRate_11, psiPlus_apply,
    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero]
  have he : 1 < Real.exp (-(2 * -1 * 1)) := by
    rw [show -(2 * -1 * 1 : ℝ) = 2 by norm_num]
    have := Real.add_one_le_exp (2 : ℝ)
    linarith
  linarith""", """  show purityR (dephase (gRate 1) (-1) psiPlus) > purityR psiPlus
  rw [probe_psiPlus_purity, purityR_dephase]
  simp only [Fin.sum_univ_two, gRate_00, gRate_01, gRate_10, gRate_11, psiPlus_apply,
    Complex.normSq_ofReal, mul_zero, neg_zero, Real.exp_zero, mul_one, mul_neg, neg_neg]
  have he : 3 ≤ Real.exp 2 := by
    have := Real.add_one_le_exp (2 : ℝ)
    linarith
  linarith""")
# avisos de linter
R("""  have h00 := congrFun (congrFun h 0) 0
  simp [Matrix.mul_apply, Fin.sum_univ_two] at h00""", """  have h00 := congrFun (congrFun h 0) 0
  simp at h00""")
R("""      (fun s t w => by
        beta_reduce
        rw [← mul_assoc, ← Complex.exp_add]""", """      (fun s t w => by
        rw [← mul_assoc, ← Complex.exp_add]""")
R("""    · simp [Pi.single_apply, hik]""", """    · simp [hik]""")
R("""  simp [Matrix.diagonal_apply_eq, Pi.single_apply, hij] at h00""",
  """  simp [Matrix.diagonal_apply_eq, hij] at h00""")
R("""  simp only [dotProduct, Matrix.mulVec, Fin.sum_univ_two, Pi.star_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons, star_one, star_neg]""",
  """  simp only [dotProduct, Matrix.mulVec, Fin.sum_univ_two, Pi.star_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, star_one, star_neg]""")

# CONTRAEXEMPLOS de cada «se e so se» (secao nova antes das clausulas compostas)
R("""/-! ## As duas cláusulas compostas (só conjunções, sem dedução nova) -/""",
  """/-! ## Contraexemplos dos «se e só se» (cada lado pode falhar; cada hipótese pesa)

* T9.a (`flow_isIdempotentElem_iff`): o lado esquerdo FALHA em `t = 1` e VALE em `t = 0` (P = diag(1,0));
  sem `1 − P ≠ 0` o «se e só se» cai (`flow_of_one_is_idempotent`, controle C-T9-a).
* T4.b (ii) / T3.b (i) (`modular_orbit_converges_iff_diagonal`, `fixed_sector_is_the_centralizer`): os dois
  lados FALHAM para ψ₊ (`probe_modular_orbit_of_psiPlus_has_no_limit`) e VALEM para `postDiag`; sem a
  INJETIVIDADE dos pesos o «se e só se» cai (pesos iguais: tudo converge, ψ₊ não é diagonal).
* T4.d / T5.a (`fixed_set_of_dephasing_is_the_diagonal`): sem taxas POSITIVAS fora da diagonal o «se e só se»
  cai (taxa nula: ψ₊ é fixo e não é diagonal).
* T10.a (`clock_faithful_iff_one_turn`): sem `κ ≠ 0` cai (`frozen_clock_not_faithful`, controle C-T10-a).
* T4.b (iii) (`light_modular_orbit_converges_iff_post`): o contraexemplo exigiria um `FockCertificate`
  concreto; NÃO construído aqui (fica dito). -/

/-- CE-T9a: em `t = 1` o fluxo do posto `diag(1,0)` NÃO é idempotente … -/
theorem flow_at_one_is_not_idempotent :
    ¬ IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1) := fun h =>
  one_ne_zero ((flow_isIdempotentElem_iff postDiag_idem postDiag_compl_ne_zero 1).mp h)

/-- … e em `t = 0` é (borda C-T9-b). -/
example : IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag 0) :=
  flow_at_zero_is_idempotent postDiag

/-- `rhoD (1, 1) = 1` (pesos iguais: o estado é escalar). -/
theorem rhoD_equal_weights : rhoD ![(1 : ℝ), 1] = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rhoD]

/-- CE-T4b(ii)/T3b(i): com pesos IGUAIS (não injetivos) o fluxo modular é a identidade — a órbita de ψ₊
    converge e ψ₊ NÃO é diagonal: a hipótese de injetividade é necessária. -/
theorem modular_iff_needs_injective_weights :
    (∃ z, Filter.Tendsto (fun t => sigma (rhoD ![(1 : ℝ), 1]) t psiPlus) Filter.atTop (nhds z)) ∧
      psiPlus ≠ diagExpect psiPlus := by
  refine ⟨⟨psiPlus, ?_⟩, psiPlus_not_diagonal⟩
  have hfix : ∀ t, sigma (rhoD ![(1 : ℝ), 1]) t psiPlus = psiPlus := fun t =>
    sigma_fixed_of_commute _ _ (by rw [rhoD_equal_weights]; exact Commute.one_left _) t
  simp_rw [hfix]
  exact tendsto_const_nhds

/-- Os dois lados de T4.b (ii) VALEM para o posto diagonal (a órbita é constante). -/
example : ∃ z, Filter.Tendsto (fun t => sigma (rhoD ![(2 / 3 : ℝ), 1 / 3]) t postDiag)
    Filter.atTop (nhds z) := by
  rw [modular_orbit_converges_iff_diagonal ![(2 / 3 : ℝ), 1 / 3]
    (fun i => by fin_cases i <;> norm_num)
    (fun a b h => by fin_cases a <;> fin_cases b <;> first | rfl | (norm_num at h)) postDiag]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [postDiag, diagExpect]

/-- CE-T4d/T5a: com taxa NULA, ψ₊ é fixo por todo `T_t` e NÃO é diagonal: a positividade das taxas fora da
    diagonal é necessária. -/
theorem dephasing_iff_needs_positive_rates :
    (∀ t : ℝ, dephase (fun _ _ : Fin 2 => (0 : ℝ)) t psiPlus = psiPlus) ∧
      psiPlus ≠ diagExpect psiPlus := by
  refine ⟨fun t => ?_, psiPlus_not_diagonal⟩
  ext i j
  rw [dephase_apply, mul_zero, neg_zero, Real.exp_zero, Complex.ofReal_one, one_mul]

/-! ## As duas cláusulas compostas (só conjunções, sem dedução nova) -/""")
R("""#print axioms TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
""", """#print axioms TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#print axioms TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation_complex
#print axioms TGLExt.TheTimeHasNoRank.flow_at_one_is_not_idempotent
#print axioms TGLExt.TheTimeHasNoRank.rhoD_equal_weights
#print axioms TGLExt.TheTimeHasNoRank.modular_iff_needs_injective_weights
#print axioms TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
""")

with open(p, "w", encoding="utf-8", newline="\n") as fo:
    fo.write(s)
print("ok", len(s.encode("utf-8")))
