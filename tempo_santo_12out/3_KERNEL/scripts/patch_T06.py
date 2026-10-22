"""Patch T05 -> T06: sondas de HABITACAO (V-GERAL-1) em Lean para os teoremas da pedra que ainda nao tinham
instancia concreta (inclusive as re-exportacoes). Cada sonda instancia o teorema com argumentos concretos, isto e,
exibe provas de todas as hipoteses. Padrao UNICO exigido."""
import sys

p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
s = open(p, encoding="utf-8").read()


def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)


R("""/-! ## As duas cláusulas compostas (só conjunções, sem dedução nova) -/""",
  """/-! ## Sondas de habitação (V-GERAL-1): as hipóteses de cada teorema da pedra são habitadas

Cada `example` instancia teoremas com argumentos CONCRETOS (exibe provas de todas as hipóteses). Não habitadas
aqui, e ditas: `nontracial_state_rejects_the_identity_flow` (exige uma testemunha AQFT `W` do kernel) e
`light_modular_orbit_converges_iff_post` / `light_flow_group` (exigem um `FockCertificate`). -/

/-- V-GERAL-1 (T4): boost com `s = 1`; Liouville linear com `L = 0` em `Fin 1`; T4.a com `U = 1`; (c3) com
    `t = 1`; ligação de Schur com `d = (2/3, 1/3)`. -/
example : True := by
  have _h1 := volume_kept_yet_lands (s := 1) one_pos
  have _h2 := global_attractor_needs_volume_loss (m := 1) (0 : Matrix (Fin 1) (Fin 1) ℝ)
    (fun v => by
      refine tendsto_const_nhds.congr' (Filter.eventually_atTop.mpr ⟨1, fun k hk => ?_⟩)
      show (0 : Fin 1 → ℝ) = ((0 : Matrix (Fin 1) (Fin 1) ℝ) ^ k).mulVec v
      rw [zero_pow (by omega), Matrix.zero_mulVec]) one_pos
  have _h3 := unitary_keeps_spectrum_and_purity (1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)
    (by rw [Units.val_one]; exact one_mem _) psiPlus
  have _h4 := dephase_factor_norm_le_one (gRate 1) (t := 1) zero_le_one 0 1 (gRate_nonneg zero_le_one 0 1)
  have _h5 := schurDiag_is_the_modular_flow ![(2 / 3 : ℝ), 1 / 3]
    (fun i => by fin_cases i <;> norm_num) 1 psiPlus
  have _h6 := the_face_lands (gRate 1) (gRate_diag 1) (gRate_off one_pos) psiPlus
  have _h7 := fixed_set_of_dephasing_is_the_diagonal (gRate 1) (gRate_diag 1) (gRate_off one_pos) psiPlus
  trivial

section FrobeniusProbe
open scoped Matrix.Norms.Frobenius

/-- V-GERAL-1 (T4.b, instância i): `U = 1`. -/
example : True := by
  have _h := unitary_conj_isometry (1 : Matrix (Fin 2) (Fin 2) ℂ) (one_mem _)
  trivial

end FrobeniusProbe

/-- V-GERAL-1 (T3, T5, T6, T7, T8): instâncias concretas em `Fin 2`. -/
example : True := by
  have _h1 := fixed_sector_is_the_centralizer ![(2 / 3 : ℝ), 1 / 3] (fun i => by fin_cases i <;> norm_num)
    (fun a b h => by fin_cases a <;> fin_cases b <;> first | rfl | (norm_num at h)) psiPlus
  have _h2 := tracial_state_freezes_the_flow (Region := Unit) (n := Fin 2) () 1 psiPlus
  have _h3 := the_record_is_invariant (gRate 1) (gRate_diag 1) 1 psiPlus
  have _h4 := purity_never_grows_under_dephasing (gRate 1) 1 zero_le_one (gRate_nonneg zero_le_one) psiPlus
  have _h5 := unitary_keeps_purity 1 psiPlus (one_mem _)
  have _h6 := purity_of_hermitian psiPlus psiPlus_posSemidef.isHermitian
  have _h7 := purityR_modular ![(2 / 3 : ℝ), 1 / 3] (fun i => by fin_cases i <;> norm_num) 1 psiPlus
  have _h8 := no_coherence_no_loss (gRate 1) (gRate_diag 1) 1 psiPlus
  have _h9 := control_inverse_on_diagonal (gRate 1) (gRate_diag 1) 1 ![(1 : ℂ), 0]
  have _h10 := the_record_does_not_scale (gRate 1) (gRate_diag 1) 0 psiPlus
    (by rw [psiPlus_apply]; norm_num) (s := 1) one_ne_zero
  have _h11 := weyl_pair_lives_in_L2 (H := ℂ) 1 1
  trivial

/-- V-GERAL-1 (T9, T10, T11): posto `diag(1,0)`, `κ = 1`, `P = 2π`, `V = ℂ` com `P = 0`. -/
example : True := by
  have _h1 := no_finite_instant_is_the_post postDiag_idem postDiag_ne_one 1
  have _h2 := flow_of_one_is_idempotent (A := Matrix (Fin 2) (Fin 2) ℂ) 1
  have _h3 := the_post_is_not_moved postDiag_idem 1
  have _h4 := face_clock_has_no_period (r := 1) one_pos (P := 1) one_pos
  have _h5 := frozen_clock_not_faithful (P := 1) one_ne_zero
  have _h6 := clock_faithful_iff_one_turn (kappa := 1) (period := 2 * Real.pi) one_ne_zero
  have _h7 := clock_reciprocal_temperature (kappa := 1) (period := 2 * Real.pi) one_pos (by positivity)
    (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period one_ne_zero (Or.inl (by ring)))
  have _h8 := angle_has_no_limit (V := ℂ) 0 1 1 (by simp)
  have _h9 := angle_is_periodic (V := ℂ) 0 (ω := 1) one_ne_zero 0 1
  have _h10 := face_has_a_limit (V := ℂ) 0 (r := 1) one_pos 1 1
  have _h11 := face_distinguishes_instants (m := 1) (r := 1) one_pos ![1] (i := 0) (by norm_num) ![1]
    (by norm_num) (t₁ := 0) (t₂ := 1) (by norm_num)
  have _h12 := the_absolute_one_has_no_clock (Region := Unit) (n := Fin 2) () 1 psiPlus
  trivial

/-! ## As duas cláusulas compostas (só conjunções, sem dedução nova) -/""")

with open(p, "w", encoding="utf-8", newline="\n") as fo:
    fo.write(s)
print("ok", len(s.encode("utf-8")))
