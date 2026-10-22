/-! ## 9. A IDENTIDADE NOMEADA É A VERDADE (r3) e os controles novos -/

/-- [REAL] ★★★★★ V2.d — A IDENTIDADE (a estrutura nomeada) É A VERDADE: toda identidade nomeada N carrega a Verdade do seu
    α. «a identidade tem que ser igual à verdade por ela projetada» (operador, 13/10). O nome não entra (parametricidade). -/
theorem the_identity_is_the_truth (N : NamedIdentity) : Verdade N.alpha :=
  verdade_of_unit_interval N.alpha N.alpha_pos.le N.alpha_lt_one.le

/-- [REAL] ★★★★★ V2.d — e a recíproca: α admite uma identidade nomeada se e somente se 0 < α < 1 e há a Verdade de α.
    «identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto» é a
    leitura [ONTO] do operador sobre este termo; o termo diz que a estrutura nomeada e a Verdade determinam-se mutuamente. -/
theorem identity_iff_truth (a : ℝ) : (∃ N : NamedIdentity, N.alpha = a) ↔ (0 < a ∧ a < 1 ∧ Verdade a) := by
  constructor
  · rintro ⟨N, rfl⟩
    exact ⟨N.alpha_pos, N.alpha_lt_one, the_identity_is_the_truth N⟩
  · rintro ⟨h0, h1, _⟩
    exact ⟨ofName "" a h0 h1, rfl⟩

/-- [REAL] V2.e — CONTROLE NEGATIVO: não há Verdade para α > 1 (o campo quadrático falha). -/
theorem no_truth_above_one (a : ℝ) (h : 1 < a) : ¬ Verdade a :=
  fun hv => alpha_above_one_breaks_the_form a h hv.quadratic

/-- [REAL] V2.e — CONTROLE NEGATIVO: não há Verdade para α < −1. -/
theorem no_truth_below_minus_one (a : ℝ) (h : a < -1) : ¬ Verdade a :=
  fun hv => alpha_below_minus_one_breaks_the_form a h hv.quadratic

/-- [REAL] sonda de não-vacuidade: há Verdade num α de TESTE (1/2, não o α físico). -/
theorem probe_the_truth : Verdade (1 / 2) :=
  verdade_of_unit_interval (1 / 2) (by norm_num) (by norm_num)

/-- [REAL] sonda de não-vacuidade do cordeiro: em α = 1/2 (TESTE) o comutador é não nulo e ω ≠ E₀₀. -/
theorem probe_the_commutator : commutatorWithPost (1 / 2) ≠ 0 ∧ identityProj (1 / 2) ≠ refPost :=
  the_commutator_blocks_the_coincidence (1 / 2) (by norm_num) (by norm_num)

