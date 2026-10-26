import TGLExt.ContratoQG_v31

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3.1 — OS TEOREMAS (leem os campos do tipo `ContratoQG_v31`)
  [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\contrato_v3\v31\ContratoQG_v31_Teoremas.lean` (sha16 f4983661f5c3b763): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: screenBlock → screenBlockV31, response_covariant → response_covariant_v31.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]

  §A  unitariedade das translações.
  §B  o que a v2 pedia como campo e a v3/v3.1 DERIVA (Δit fixa Ω; BW geométrico; Poincaré; não-trivial).
  §C  ★★★ COERÊNCIA ESPECTRAL: todo habitante tem Δ^{it} SEM autovetor fora de ℂΩ (oposto da v2).
  §C' ★ as paredes do cético 1 transpostas (T1–T4): U transversal, boost trivial, torre, momento nulo discreto.
  §C''★ os certificados de sinal do cético 2 transpostos: inclusão semilateral, forma de Borchers, orientação.
  §D  ★★ κ: Unruh como relação KMS (β_Killing·κ = 2π); κ = 1/ρ(N); κ FIXO dado N; (W,R) NÃO fixa κ.
  §E  o implementador é ÚNICO.
  §F  as energias: K = 2πB; ★ a energia BILATERAL não tem termo de 1ª ordem (cético 2, transposto).
  §G  o frame.
  §H  ★★★ H3 v3.1: a lei local ao longo do gerador; BH/Clausius/8πG como teoremas de JANELA (integração
      exata); a energia nula não se anula; a expansão não é constante; G NÃO é predito (Jacobson).
  §I  as paredes no par legado e contra translações que comutam com Δit.
  §J  o import indexado.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv31

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

/-! ## §A — as translações de qualquer testemunha são unitárias -/

section Unitarity

variable (W : TGLSpecificAQFTWitness)

theorem U_neg_mul (a : Fin 4 → ℝ) : W.U (-a) * W.U a = 1 := by
  rw [← W.U_add, neg_add_cancel, W.U_zero]

theorem U_neg_apply (a : Fin 4 → ℝ) (x : W.H) : W.U (-a) (W.U a x) = x := by
  have h := congrArg (fun T : W.H →L[ℂ] W.H => T x) (U_neg_mul W a)
  exact h

theorem U_pos_neg_apply (a : Fin 4 → ℝ) (x : W.H) : W.U a (W.U (-a) x) = x := by
  have := U_neg_apply W (-a) x
  rwa [neg_neg] at this

theorem U_inner_adj (a : Fin 4 → ℝ) (x y : W.H) : ⟪W.U a x, y⟫_ℂ = ⟪x, W.U (-a) y⟫_ℂ := by
  rw [← W.U_star a, ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right]

theorem U_norm (a : Fin 4 → ℝ) (x : W.H) : ‖W.U a x‖ = ‖x‖ := by
  have h : ⟪W.U a x, W.U a x⟫_ℂ = ⟪x, x⟫_ℂ := by
    rw [U_inner_adj, U_neg_apply]
  rw [inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K] at h
  have h2 : ‖W.U a x‖ ^ 2 = ‖x‖ ^ 2 := by exact_mod_cast h
  have := norm_nonneg (W.U a x)
  have := norm_nonneg x
  nlinarith [sq_nonneg (‖W.U a x‖ - ‖x‖), sq_nonneg (‖W.U a x‖ + ‖x‖)]

end Unitarity

/-! ## §B — o que a v2 pedia como CAMPO e a v3.1 DERIVA -/

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- [DERIVED] Δ^{it} fixa o vácuo (de `bw` + `V_vac`). -/
theorem Δit_vac (C : ContratoH2 W R N) (t : ℝ) : C.Δit t W.vac = W.vac := by
  rw [C.bw]; exact C.boost.V_vac _

/-- [DERIVED] Ad(Δ^{it}) é GEOMÉTRICO na rede: net(O) ↦ net(Λ(−2πt)O). -/
theorem bw_covariance (C : ContratoH2 W R N) (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H)
    (hT : T ∈ W.net O) :
    (C.Δit t).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O) := by
  rw [C.bw]; exact C.boost.V_net _ O T hT

/-- [DERIVED] Δ^{it} U(a) Δ^{−it} = U(Λ(−2πt)a). -/
theorem poincare_relation (C : ContratoH2 W R N) (t : ℝ) (a : Fin 4 → ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap (-(2 * Real.pi * t)) a) := by
  rw [C.bw]; exact C.boost.V_translations _ a

/-- [DERIVED] as translações não são triviais (fidelidade). -/
theorem translates (C : ContratoH2 W R N) : ∃ a : Fin 4 → ℝ, W.U a ≠ 1 := by
  refine ⟨nullDir, fun h => ?_⟩
  have h0 := congrFun (C.translations_faithful _ h) 0
  simp [nullDir] at h0

/-! ## §C — ★★★ COERÊNCIA ESPECTRAL -/

theorem eigen_null_correlation_dilation (C : ContratoH2 W R N) {ψ : W.H} {r : ℝ}
    (hψ : ∀ t : ℝ, C.Δit t ψ = ChatgptAudit.modularPhase t r • ψ) (t l : ℝ) :
    ⟪ψ, W.U ((l * Real.exp (-(2 * Real.pi * t))) • nullDir) ψ⟫_ℂ
      = ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ := by
  set p : ℂ := ChatgptAudit.modularPhase t r with hpdef
  have hp : ‖p‖ = 1 := by
    rw [hpdef]
    unfold ChatgptAudit.modularPhase
    exact Complex.norm_exp_ofReal_mul_I _
  have hp0 : p ≠ 0 := by
    intro h; rw [h, norm_zero] at hp; exact zero_ne_one hp
  have hsymm : (C.Δit t).symm ψ = p⁻¹ • ψ := by
    apply (C.Δit t).injective
    rw [LinearIsometryEquiv.apply_symm_apply, LinearIsometryEquiv.map_smul, hψ t, smul_smul,
      inv_mul_cancel₀ hp0, one_smul]
  have hrel := congrArg (fun T : W.H →L[ℂ] W.H => T ψ) (C.poincare_relation t (l • nullDir))
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at hrel
  rw [wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul] at hrel
  rw [← hrel]
  have hin : ⟪ψ, C.Δit t (W.U (l • nullDir) ((C.Δit t).symm ψ))⟫_ℂ
      = ⟪(C.Δit t).symm ψ, W.U (l • nullDir) ((C.Δit t).symm ψ)⟫_ℂ := by
    have h := (C.Δit t).inner_map_map ((C.Δit t).symm ψ)
      (W.U (l • nullDir) ((C.Δit t).symm ψ))
    rw [LinearIsometryEquiv.apply_symm_apply] at h
    exact h
  rw [hin, hsymm, map_smul, inner_smul_left, inner_smul_right, ← mul_assoc]
  have hq : (starRingEnd ℂ) p⁻¹ * p⁻¹ = 1 := by
    rw [Complex.conj_mul', norm_inv, hp, inv_one]
    simp
  rw [hq, one_mul]

/-- [DERIVED] ★★★ O TEOREMA DE COERÊNCIA: em QUALQUER habitante da v3.1, Δ^{it} não tem autovetor fora
    de ℂ·Ω (o OPOSTO de `contratoH2_forces_point_spectrum`, v2). Não usa energia positiva nem KMS. -/
theorem no_point_spectrum (C : ContratoH2 W R N) : NoEigenOutsideVacuum W C.Δit := by
  intro ψ r hψ
  apply C.null_ergodic
  set g : ℝ → ℂ := fun l => ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ with hg
  have hcont : Continuous g := by
    have h1 : Continuous (fun l : ℝ => W.U (l • nullDir) ψ) :=
      (C.translations_continuous ψ).comp (continuous_id.smul continuous_const)
    exact continuous_const.inner h1
  have hdil : ∀ l μ : ℝ, 0 < μ → g (l * μ) = g l := by
    intro l μ hμ
    have h := eigen_null_correlation_dilation C hψ (-(Real.log μ) / (2 * Real.pi)) l
    have hpi : (2 * Real.pi) ≠ 0 := by positivity
    have he : Real.exp (-(2 * Real.pi * (-(Real.log μ) / (2 * Real.pi)))) = μ := by
      have : -(2 * Real.pi * (-(Real.log μ) / (2 * Real.pi))) = Real.log μ := by
        field_simp
      rw [this, Real.exp_log hμ]
    rw [he] at h
    exact h
  have hconst : ∀ l : ℝ, g l = g 0 := by
    intro l
    have hlim : Tendsto (fun μ : ℝ => g (l * μ)) (𝓝[>] 0) (𝓝 (g 0)) := by
      have h0 : Tendsto (fun μ : ℝ => l * μ) (𝓝[>] (0:ℝ)) (𝓝 0) := by
        have h : Tendsto (fun μ : ℝ => l * μ) (𝓝 (0:ℝ)) (𝓝 (l * 0)) :=
          (continuous_const_mul l).tendsto 0
        rw [mul_zero] at h
        exact h.mono_left nhdsWithin_le_nhds
      exact (hcont.tendsto 0).comp h0
    have hlim' : Tendsto (fun μ : ℝ => g (l * μ)) (𝓝[>] 0) (𝓝 (g l)) := by
      apply tendsto_const_nhds.congr'
      filter_upwards [self_mem_nhdsWithin] with μ hμ
      exact (hdil l μ hμ).symm
    exact tendsto_nhds_unique hlim' hlim
  have hg0 : g 0 = ⟪ψ, ψ⟫_ℂ := by
    simp only [hg, zero_smul, W.U_zero]
    rfl
  intro l
  have hgl : ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ = ⟪ψ, ψ⟫_ℂ := by
    have := hconst l
    rw [hg0] at this
    exact this
  have hre : RCLike.re ⟪W.U (l • nullDir) ψ, ψ⟫_ℂ = ‖ψ‖ ^ 2 := by
    rw [inner_re_symm, hgl, inner_self_eq_norm_sq_to_K]
    norm_cast
  have hn := @norm_sub_sq ℂ W.H _ _ _ (W.U (l • nullDir) ψ) ψ
  rw [hre, U_norm] at hn
  have hz : ‖W.U (l • nullDir) ψ - ψ‖ ^ 2 = 0 := by rw [hn]; ring
  have hz' : ‖W.U (l • nullDir) ψ - ψ‖ = 0 := by
    exact (pow_eq_zero_iff two_ne_zero).mp hz
  exact sub_eq_zero.mp (norm_eq_zero.mp hz')

/-! ## §C' — as paredes do CÉTICO 1 (BrinqH2Paredes.lean, 957f5ac79142a327), transpostas à v3.1 -/

/-- (T2, cético 1) grupo de boosts trivial não habita. -/
theorem trivial_boost_excluded (C : ContratoH2 W R N)
    (hV : ∀ s : ℝ, C.boost.V s = LinearIsometryEquiv.refl ℂ W.H) : False := by
  have hm0 : (Real.exp (-(2 * Real.pi)) - 1) • nullDir ≠ 0 := by
    intro h0
    have h := congrFun h0 0
    have hlt : Real.exp (-(2 * Real.pi)) < 1 := by
      have := Real.exp_lt_exp.mpr (show -(2 * Real.pi) < 0 by
        have := Real.pi_pos; linarith)
      simpa using this
    simp [nullDir] at h
    linarith
  apply hm0
  apply C.translations_faithful
  have hB := C.poincare_relation 1 nullDir
  rw [C.bw, hV] at hB
  have hid : (LinearIsometryEquiv.refl ℂ W.H).conjStarAlgEquiv (W.U nullDir) = W.U nullDir := by
    ext x; simp
  rw [hid, wedgeBoostMap_nullDir, mul_one] at hB
  have hsplit : Real.exp (-(2 * Real.pi)) • nullDir
      = nullDir + (Real.exp (-(2 * Real.pi)) - 1) • nullDir := by
    rw [sub_smul, one_smul]; abel
  rw [hsplit, W.U_add] at hB
  have hinv : W.U (-nullDir) * W.U nullDir = 1 := by
    rw [← W.U_add, neg_add_cancel, W.U_zero]
  calc W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir)
      = (W.U (-nullDir) * W.U nullDir) * W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir) := by
        rw [hinv, one_mul]
    _ = W.U (-nullDir) * (W.U nullDir * W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir)) := by
        rw [mul_assoc]
    _ = W.U (-nullDir) * W.U nullDir := by rw [← hB]
    _ = 1 := hinv

theorem boost_moves_null_eigen (C : ContratoH2 W R N) (ψ : W.H) (ω : ℝ)
    (h : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) (s l : ℝ) :
    W.U (l • nullDir) (C.boost.V s ψ)
      = Complex.exp (((l * (Real.exp (-s) * ω) : ℝ) : ℂ) * I) • C.boost.V s ψ := by
  have hrel := congrArg (fun T : W.H →L[ℂ] W.H => T (C.boost.V s ψ))
    (C.boost.V_translations s ((l * Real.exp (-s)) • nullDir))
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply] at hrel
  rw [wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul] at hrel
  have he : l * Real.exp (-s) * Real.exp s = l := by
    rw [mul_assoc, ← Real.exp_add]; simp
  rw [he] at hrel
  rw [← hrel, h, LinearIsometryEquiv.map_smul]
  congr 2
  push_cast
  ring

theorem null_eigen_orth (ψ φ : W.H) (ω ω' : ℝ) (hne : ω' - ω ≠ 0)
    (hψ : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ)
    (hφ : ∀ l : ℝ, W.U (l • nullDir) φ = Complex.exp (((l * ω' : ℝ) : ℂ) * I) • φ) :
    ⟪ψ, φ⟫_ℂ = 0 := by
  set l : ℝ := Real.pi / (ω' - ω) with hl
  have hinv : ⟪ψ, φ⟫_ℂ = ⟪W.U (l • nullDir) ψ, W.U (l • nullDir) φ⟫_ℂ := by
    rw [U_inner_adj W, U_neg_apply W]
  rw [hψ l, hφ l, inner_smul_left, inner_smul_right, ← mul_assoc] at hinv
  have hlω : l * ω' - l * ω = Real.pi := by
    rw [hl]; field_simp
  have hphase : (starRingEnd ℂ) (Complex.exp (((l * ω : ℝ) : ℂ) * I))
      * Complex.exp (((l * ω' : ℝ) : ℂ) * I) = -1 := by
    rw [← Complex.exp_conj, map_mul, Complex.conj_ofReal, Complex.conj_I, ← Complex.exp_add]
    have hc : ((l * ω' - l * ω : ℝ) : ℂ) = (Real.pi : ℂ) := by exact_mod_cast hlω
    have : ((l * ω : ℝ) : ℂ) * -I + ((l * ω' : ℝ) : ℂ) * I = (Real.pi : ℂ) * I := by
      push_cast at hc ⊢
      linear_combination hc * I
    rw [this, Complex.exp_pi_mul_I]
  rw [hphase] at hinv
  linear_combination (1 / 2 : ℂ) * hinv

/-- (T4, cético 1) ★★ num habitante, todo autovetor das translações nulas está em ℂΩ (exclui U de momento
    discreto — «de dimensão finita» ou de torre). Primeiro consumidor de `V_continuous`. -/
theorem null_point_spectrum_excluded (C : ContratoH2 W R N) (ψ : W.H) (ω : ℝ)
    (h : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) :
    ψ ∈ (ℂ ∙ W.vac) := by
  by_cases hω : ω = 0
  · apply C.null_ergodic
    intro l
    rw [h l, hω]
    simp
  · suffices hψ : ψ = 0 by rw [hψ]; exact Submodule.zero_mem _
    have horth : ∀ s : ℝ, s ≠ 0 → ⟪ψ, C.boost.V s ψ⟫_ℂ = 0 := by
      intro s hs
      have hne : Real.exp (-s) * ω - ω ≠ 0 := by
        intro h0
        have h1 : (Real.exp (-s) - 1) * ω = 0 := by linarith [h0]
        rcases mul_eq_zero.mp h1 with h2 | h2
        · have h3 : Real.exp (-s) = 1 := by linarith
          have h4 : -s = 0 := Real.exp_eq_one_iff (-s) |>.mp h3
          exact hs (by linarith)
        · exact hω h2
      exact null_eigen_orth ψ (C.boost.V s ψ) ω (Real.exp (-s) * ω) hne h
        (boost_moves_null_eigen C ψ ω h s)
    have hcont : Continuous (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) :=
      continuous_const.inner (C.boost.V_continuous ψ)
    have hlim : Tendsto (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (𝓝[≠] 0) (𝓝 0) := by
      apply tendsto_const_nhds.congr'
      filter_upwards [self_mem_nhdsWithin] with s hs
      exact (horth s hs).symm
    have hlim2 : Tendsto (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (𝓝[≠] 0)
        (𝓝 ⟪ψ, C.boost.V 0 ψ⟫_ℂ) :=
      (hcont.tendsto 0).mono_left nhdsWithin_le_nhds
    have h0 : ⟪ψ, C.boost.V 0 ψ⟫_ℂ = 0 := tendsto_nhds_unique hlim2 hlim
    rw [C.boost.V_zero] at h0
    change ⟪ψ, ψ⟫_ℂ = 0 at h0
    exact inner_self_eq_zero.mp h0

end ContratoH2

/-- (T1, cético 1) U que só lê as coordenadas transversais não habita. -/
theorem transverse_U_excluded {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (hU : ∀ a : Fin 4 → ℝ, W.U a = W.U ![0, 0, a 2, a 3]) : IsEmpty (ContratoH2 W R N) := by
  refine ⟨fun C => ?_⟩
  have h0 := C.translations_faithful nullDir (by
    rw [hU]
    have : (![0, 0, nullDir 2, nullDir 3] : Fin 4 → ℝ) = 0 := by
      funext i; fin_cases i <;> simp [nullDir]
    rw [this, W.U_zero])
  have := congrFun h0 0
  simp [nullDir] at this

/-- (T4', cético 1) U de momento nulo discreto ⟹ vazio. -/
theorem discrete_null_momentum_excluded {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (hpt : ∃ (ψ : W.H) (ω : ℝ), ψ ∉ (ℂ ∙ W.vac) ∧
      ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) :
    IsEmpty (ContratoH2 W R N) := by
  refine ⟨fun C => ?_⟩
  obtain ⟨ψ, ω, hψ, h⟩ := hpt
  exact hψ (C.null_point_spectrum_excluded ψ ω h)

/-! ## §C'' — os certificados de sinal do CÉTICO 2 (CeticoKappaGauge.lean §2, 333a662a8fde1b51), transpostos -/

theorem translate_null_subset (l : ℝ) (hl : 0 ≤ l) :
    TGL.SpecificAQFT.translate (l • nullDir) rightWedge ⊆ rightWedge := by
  rintro _ ⟨x, hx, rfl⟩
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  show |(x + l • nullDir) 0| < (x + l • nullDir) 1
  simp only [Pi.add_apply, Pi.smul_apply, nullDir, smul_eq_mul, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one]
  rw [abs_lt]
  constructor <;> linarith

/-- [DERIVED] ★ (a) A INCLUSÃO SEMILATERAL, da covariância e da isotonia do kernel. -/
theorem halfsided_inclusion (W : TGLSpecificAQFTWitness) (l : ℝ) (hl : 0 ≤ l)
    (T : W.H →L[ℂ] W.H) (hT : T ∈ W.net rightWedge) :
    W.U (l • nullDir) * T * W.U (-(l • nullDir)) ∈ W.net rightWedge := by
  have h := (W.covariance (l • nullDir) rightWedge T).mp hT
  exact W.isotony _ _ (translate_null_subset l hl) h

/-- [DERIVED] ★ (b) A FORMA DE BORCHERS no contrato: Δ^{it} U(λn) Δ^{−it} = U(e^{−2πt}·λ·n). -/
theorem ContratoH2.contract_borchers_form {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} (C : ContratoH2 W R N) (t l : ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U (l • nullDir))
      = W.U ((Real.exp (-(2 * Real.pi * t)) * l) • nullDir) := by
  rw [C.poincare_relation, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul, mul_comm l]

/-- [DERIVED] (c) a orientação de `PositiveEnergy`: z ↦ e^{izλ} (λ ≥ 0) é limitada no semiplano superior. -/
theorem positiveEnergy_orientation (lam : ℝ) (hlam : 0 ≤ lam) (z : ℂ) (hz : 0 ≤ z.im) :
    ‖Complex.exp (I * z * lam)‖ ≤ 1 := by
  rw [Complex.norm_exp]
  have : (I * z * (lam : ℂ)).re = -(z.im * lam) := by
    simp [Complex.mul_re, Complex.mul_im]
  rw [this, Real.exp_le_one_iff]
  have := mul_nonneg hz hlam
  linarith

/-! ## §D — ★★ κ: Unruh como RELAÇÃO KMS; κ fixo DADO N; (W,R) não fixa κ -/

/-- [DERIVED] REESCALA DO KMS: α KMS a β ⟹ τ ↦ α(cτ) KMS a β/c. -/
theorem KMSAt.rescale {W : TGLSpecificAQFTWitness} {α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {β : ℝ}
    (h : KMSAt W α β) {c : ℝ} (hc : 0 < c) :
    KMSAt W (fun τ => α (c * τ)) (β / c) := by
  intro A hA B hB
  obtain ⟨F, hF, ⟨M, hM⟩, h1, h2⟩ := h A hA B hB
  have him : ∀ w : ℂ, ((c : ℂ) * w).im = c * w.im := by
    intro w; simp [Complex.mul_im]
  refine ⟨fun w => F ((c : ℂ) * w), ?_, ⟨M, ?_⟩, ?_, ?_⟩
  · have hg : DiffContOnCl ℂ (fun w : ℂ => (c : ℂ) * w) (kmsStrip (β / c)) :=
      (differentiable_id.const_mul _).diffContOnCl
    refine hF.comp hg ?_
    intro w hw
    simp only [kmsStrip, Set.mem_setOf_eq] at hw ⊢
    rw [him]
    refine ⟨mul_pos hc hw.1, ?_⟩
    calc c * w.im < c * (β / c) := mul_lt_mul_of_pos_left hw.2 hc
      _ = β := by field_simp
  · intro z hz0 hzβ
    apply hM
    · rw [him]; exact mul_nonneg hc.le hz0
    · rw [him]
      calc c * z.im ≤ c * (β / c) := mul_le_mul_of_nonneg_left hzβ hc.le
        _ = β := by field_simp
  · intro t
    have := h1 (c * t)
    simp only
    rw [← this]
    push_cast
    rfl
  · intro t
    have := h2 (c * t)
    have hc0 : (c : ℂ) ≠ 0 := by exact_mod_cast hc.ne'
    have harg : (c : ℂ) * ((t : ℂ) + ((β / c : ℝ) : ℂ) * I) = ((c * t : ℝ) : ℂ) + (β : ℂ) * I := by
      push_cast
      rw [mul_add, div_mul_eq_mul_div, mul_div_assoc', mul_div_cancel_left₀ _ hc0]
    simp only
    rw [harg, this]
    congr 3
    ring

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem modular_is_boost_at_two_pi (C : ContratoH2 W R N) :
    (fun t => C.Δit (-t)) = (fun t => C.boost.V (2 * Real.pi * t)) := by
  funext t
  rw [C.bw]
  ring_nf

/-- [DERIVED] ★ UNRUH COMO RELAÇÃO KMS: o fluxo de Killing τ ↦ V(κτ) é KMS a β = 2π/κ. ⚠ (rodada 2) isto fixa
    o PRODUTO β_Killing·κ = 2π — NÃO o valor de κ (cético 1, `kms_product_is_two_pi`). -/
theorem unruh_is_kms (C : ContratoH2 W R N) :
    KMSAt W C.killingFlow (2 * Real.pi / C.kappa) := by
  have h1 : KMSAt W (fun t => C.boost.V (2 * Real.pi * t)) 1 := by
    have := C.kms
    rwa [modular_is_boost_at_two_pi] at this
  have hc : 0 < C.kappa / (2 * Real.pi) := div_pos C.kappa_pos (by positivity)
  have h2 := KMSAt.rescale h1 hc
  have hfun : (fun τ => (fun t => C.boost.V (2 * Real.pi * t)) (C.kappa / (2 * Real.pi) * τ))
      = C.killingFlow := by
    funext τ
    unfold ContratoH2.killingFlow
    field_simp
  have hβ : (1 : ℝ) / (C.kappa / (2 * Real.pi)) = 2 * Real.pi / C.kappa := by
    field_simp
  rw [hfun, hβ] at h2
  exact h2

theorem unruh_is_kms_temperature (C : ContratoH2 W R N) :
    KMSAt W C.killingFlow (1 / C.unruhTemperature) := by
  have h := unruh_is_kms C
  have : (1 : ℝ) / C.unruhTemperature = 2 * Real.pi / C.kappa := by
    unfold ContratoH2.unruhTemperature
    have := C.kappa_pos.ne'
    field_simp
  rw [this]; exact h

/-- [DERIVED] a relação que o tipo fixa: β_Killing·κ = 2π (a do cético 1). -/
theorem kms_product_is_two_pi (C : ContratoH2 W R N) :
    (2 * Real.pi / C.kappa) * C.kappa = 2 * Real.pi := by
  have := C.kappa_pos.ne'
  field_simp

/-- o raio de Rindler do relógio de N. -/
def refRadius (N : KillingNormalization) : ℝ := Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2)

theorem refRadius_pos (N : KillingNormalization) : 0 < refRadius N := by
  have hx : |N.point 0| < N.point 1 := N.point_in_wedge
  obtain ⟨h1, h2⟩ := abs_lt.mp hx
  unfold refRadius
  apply Real.sqrt_pos.mpr
  nlinarith

/-- [DERIVED] κ·ρ(N) = 1. -/
theorem kappa_mul_radius (C : ContratoH2 W R N) : C.kappa * refRadius N = 1 := by
  have h := C.observer_unit
  simp [minkowskiSq, killingField] at h
  have hk : C.kappa ^ 2 * (N.point 1 ^ 2 - N.point 0 ^ 2) = 1 := by
    linear_combination h
  unfold refRadius
  rw [← Real.sqrt_sq C.kappa_pos.le, ← Real.sqrt_mul (sq_nonneg _), hk, Real.sqrt_one]

/-- [DERIVED] ★ κ = 1/ρ(N): o VALOR de κ é o do relógio externo. -/
theorem kappa_eq_inv_radius (C : ContratoH2 W R N) : C.kappa = 1 / refRadius N := by
  have h := kappa_mul_radius C
  have hne := (refRadius_pos N).ne'
  field_simp
  linarith [h]

/-- [DERIVED] ★★ κ FIXO DADO N: dois habitantes de `ContratoH2 W R N` têm o MESMO κ (o `rekappa` do cético 1 e
    o `regauge` do cético 2 NÃO habitam o mesmo tipo indexado). -/
theorem kappa_fixed (C C' : ContratoH2 W R N) : C.kappa = C'.kappa := by
  rw [kappa_eq_inv_radius C, kappa_eq_inv_radius C']

theorem no_rekappa (C : ContratoH2 W R N) {κ' : ℝ} (h : κ' ≠ C.kappa) :
    ¬ ∃ C' : ContratoH2 W R N, C'.kappa = κ' :=
  fun ⟨C', hC'⟩ => h (hC' ▸ kappa_fixed C' C)

/-- a unidade do Killing no relógio de N' com κ' = 1/ρ(N'). -/
theorem observer_unit_of_index (N' : KillingNormalization) :
    minkowskiSq (killingField (1 / refRadius N') N'.point) = 1 := by
  have hr := refRadius_pos N'
  have hsq : refRadius N' ^ 2 = N'.point 1 ^ 2 - N'.point 0 ^ 2 := by
    unfold refRadius
    have hx : |N'.point 0| < N'.point 1 := N'.point_in_wedge
    obtain ⟨h1, h2⟩ := abs_lt.mp hx
    rw [Real.sq_sqrt (by nlinarith)]
  simp [minkowskiSq, killingField]
  field_simp
  linarith [hsq]

/-- ★ RE-INDEXAR: de um habitante sobre N, outro sobre QUALQUER N' (mesmo Δit, boost, frame, bloco (P)). -/
def reindex (C : ContratoH2 W R N) (N' : KillingNormalization) : ContratoH2 W R N' where
  kappa := 1 / refRadius N'
  kappa_pos := by have := refRadius_pos N'; positivity
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := observer_unit_of_index N'
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    intro x hx
    obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
    have hk := C.kappa_pos
    have hr := refRadius_pos N'
    refine ⟨c * C.kappa * refRadius N', by positivity, ?_⟩
    rw [h]
    funext i
    simp only [killingField, Pi.smul_apply, smul_eq_mul]
    field_simp

/-- [DERIVED] ★★ HONESTO: o par (W, R) NÃO fixa κ — se há habitante sobre algum N, há sobre TODO N'. O valor
    de κ é o [INPUT] N; a v3.1 NÃO «fixa o parâmetro espectral» a partir do par. -/
theorem kappa_is_input (h : Nonempty (ContratoH2 W R N)) (N' : KillingNormalization) :
    Nonempty (ContratoH2 W R N') :=
  ⟨reindex h.some N'⟩

theorem killingFlow_add (C : ContratoH2 W R N) (τ σ : ℝ) :
    C.killingFlow (τ + σ) = (C.killingFlow σ).trans (C.killingFlow τ) := by
  unfold ContratoH2.killingFlow
  rw [mul_add, C.boost.V_add]

theorem killingFlow_zero (C : ContratoH2 W R N) :
    C.killingFlow 0 = LinearIsometryEquiv.refl ℂ W.H := by
  unfold ContratoH2.killingFlow
  rw [mul_zero, C.boost.V_zero]

/-! ## §F — as energias -/

theorem modularEnergy_of_boostEnergy (C : ContratoH2 W R N) {ψ : W.H} {b : ℝ}
    (h : HasBoostEnergy C.boost.V ψ b) : HasModularEnergy C.Δit ψ (2 * Real.pi * b) := by
  unfold HasBoostEnergy at h
  unfold HasModularEnergy
  have hg : HasDerivAt (fun t : ℝ => -(2 * Real.pi * t)) (-(2 * Real.pi)) 0 := by
    have h0 := (hasDerivAt_id (0:ℝ)).const_mul (-(2 * Real.pi))
    have e : (fun t : ℝ => -(2 * Real.pi * t)) = (fun y : ℝ => -(2 * Real.pi) * id y) := by
      funext t; simp [id]
    rw [e]
    exact h0.congr_deriv (by ring)
  have h' : HasDerivAt (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (I * (b : ℂ)) (-(2 * Real.pi * 0)) := by
    simpa using h
  have hc := h'.scomp (0:ℝ) hg
  have hfun : (fun t : ℝ => ⟪ψ, C.Δit t ψ⟫_ℂ)
      = (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) ∘ (fun t : ℝ => -(2 * Real.pi * t)) := by
    funext t
    simp only [Function.comp, C.bw]
  rw [hfun]
  refine hc.congr_deriv ?_
  rw [Complex.real_smul]
  push_cast
  ring

theorem modularEnergy_unique {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : ℝ → (H ≃ₗᵢ[ℂ] H)} {ψ : H} {k k' : ℝ}
    (h : HasModularEnergy D ψ k) (h' : HasModularEnergy D ψ k') : k = k' := by
  have hu := h.unique h'
  have hI : I * (k : ℂ) = I * (k' : ℂ) := neg_inj.mp hu
  have : (k : ℂ) = k' := mul_left_cancel₀ Complex.I_ne_zero hI
  exact_mod_cast this

theorem vac_modularEnergy (C : ContratoH2 W R N) : HasModularEnergy C.Δit W.vac 0 := by
  unfold HasModularEnergy
  have : (fun t : ℝ => ⟪W.vac, C.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext t; rw [Δit_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

theorem vac_boostEnergy (C : ContratoH2 W R N) : HasBoostEnergy C.boost.V W.vac 0 := by
  unfold HasBoostEnergy
  have : (fun s : ℝ => ⟪W.vac, C.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext s; rw [C.boost.V_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

theorem inner_vac_Δit (C : ContratoH2 W R N) (t : ℝ) (φ : W.H) :
    ⟪W.vac, C.Δit t φ⟫_ℂ = ⟪W.vac, φ⟫_ℂ := by
  have h := (C.Δit t).inner_map_map W.vac φ
  rw [Δit_vac] at h
  exact h

/-- [DERIVED] ★★ (cético 2, CeticoFirstLaw.lean 39e2508fdde98aef, transposto) a energia modular BILATERAL da
    perturbação Ω + εφ é ε²·k_φ: SEM termo de 1ª ordem. É por isso que o δS de H3 v3.1 NÃO é esta energia,
    e sim a carga UNILATERAL do corte nulo (`windowEntropy`). -/
theorem bilateral_no_first_order (C : ContratoH2 W R N) {φ : W.H} {k : ℝ}
    (hk : HasModularEnergy C.Δit φ k) (ε : ℝ) :
    HasModularEnergy C.Δit (W.vac + (ε : ℂ) • φ) (ε ^ 2 * k) := by
  unfold HasModularEnergy at hk ⊢
  have hfun : (fun t : ℝ => ⟪W.vac + (ε : ℂ) • φ, C.Δit t (W.vac + (ε : ℂ) • φ)⟫_ℂ)
      = fun t : ℝ => (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
          + ((ε : ℂ) ^ 2) * ⟪φ, C.Δit t φ⟫_ℂ := by
    funext t
    rw [map_add, map_smul, Δit_vac, inner_add_left, inner_add_right, inner_add_right,
      inner_smul_left, inner_smul_left, inner_smul_right, inner_smul_right, inner_vac_Δit]
    simp only [Complex.conj_ofReal]
    ring
  rw [hfun]
  have h2 := (hk.const_mul ((ε : ℂ) ^ 2)).const_add
    (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
  refine h2.congr_deriv ?_
  push_cast
  ring

end ContratoH2

/-! ## §E — o implementador é ÚNICO -/

theorem implementer_unique {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (D₁ D₂ : ℝ → (W.H ≃ₗᵢ[ℂ] W.H))
    (h₁v : ∀ t, D₁ t W.vac = W.vac) (h₂v : ∀ t, D₂ t W.vac = W.vac)
    (h₁ : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D₁ t).conjStarAlgEquiv a.val)
    (h₂ : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D₂ t).conjStarAlgEquiv a.val)
    (t : ℝ) : D₁ t = D₂ t := by
  have hpt : ∀ T ∈ W.net rightWedge, D₁ t (T W.vac) = D₂ t (T W.vac) := by
    intro T hT
    have hmem : T ∈ R.modular.wedgeAlgebra.toStarSubalgebra := by
      show T ∈ R.modular.wedgeAlgebra
      rw [R.modular.wedgeAlgebra_eq]; exact hT
    have e1 := congrArg (fun X : W.H →L[ℂ] W.H => X W.vac) (h₁ t ⟨T, hmem⟩)
    have e2 := congrArg (fun X : W.H →L[ℂ] W.H => X W.vac) (h₂ t ⟨T, hmem⟩)
    simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at e1 e2
    have s1 : (D₁ t).symm W.vac = W.vac := by
      apply (D₁ t).injective
      rw [LinearIsometryEquiv.apply_symm_apply, h₁v]
    have s2 : (D₂ t).symm W.vac = W.vac := by
      apply (D₂ t).injective
      rw [LinearIsometryEquiv.apply_symm_apply, h₂v]
    rw [s1] at e1
    rw [s2] at e2
    rw [← e1, ← e2]
  have hspan : ∀ x ∈ Submodule.span ℂ
      ((fun T : W.H →L[ℂ] W.H => T W.vac) '' (W.net rightWedge : Set (W.H →L[ℂ] W.H))),
      D₁ t x = D₂ t x := by
    intro x hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨T, hT, rfl⟩ := hx
      exact hpt T hT
    | zero => simp
    | add x y _ _ hx hy => rw [map_add, map_add, hx, hy]
    | smul c x _ hx => rw [map_smul, map_smul, hx]
  have hfun : (fun x => D₁ t x) = (fun x => D₂ t x) :=
    Continuous.ext_on W.vac_cyclic_wedge (D₁ t).continuous (D₂ t).continuous hspan
  ext x
  exact congrFun hfun x

/-- (T3, cético 1) ★ A TORRE: se um implementador do fluxo de R (fixando Ω) tem autovetor fora de ℂΩ, NENHUM
    contrato v3.1 existe sobre (W, R, N). -/
theorem tower_excluded {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (hDv : ∀ t, D t W.vac = W.vac)
    (hD : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D t).conjStarAlgEquiv a.val)
    (hpt : ∃ (v : W.H) (r : ℝ), v ∉ (ℂ ∙ W.vac) ∧
      ∀ t : ℝ, D t v = ChatgptAudit.modularPhase t r • v) :
    IsEmpty (ContratoH2 W R N) := by
  refine ⟨fun C => ?_⟩
  obtain ⟨v, r, hv, hvD⟩ := hpt
  apply hv
  apply C.no_point_spectrum v r
  intro t
  rw [implementer_unique C.Δit D C.Δit_vac hDv C.flow_implemented hD t]
  exact hvD t

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem Δit_determined (C C' : ContratoH2 W R N) (t : ℝ) : C.Δit t = C'.Δit t :=
  implementer_unique C.Δit C'.Δit C.Δit_vac C'.Δit_vac C.flow_implemented C'.flow_implemented t

/-- [DERIVED] o Δit NÃO depende do índice N (dois habitantes sobre N e N' têm o mesmo Δit). -/
theorem Δit_index_free {N' : KillingNormalization} (C : ContratoH2 W R N) (C' : ContratoH2 W R N')
    (t : ℝ) : C.Δit t = C'.Δit t :=
  implementer_unique C.Δit C'.Δit C.Δit_vac C'.Δit_vac C.flow_implemented C'.flow_implemented t

/-! ## §G — o frame -/

theorem boostMat_det_isUnit (s : ℝ) : IsUnit (boostMat s).det := by
  have h := congrArg Matrix.det (boostMat_isLorentz s)
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at h
  have hη : eta4.det ≠ 0 := by
    unfold eta4
    rw [Matrix.det_diagonal, Fin.prod_univ_four]
    norm_num [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail]
  have hsq : (boostMat s).det * (boostMat s).det = 1 := by
    have h' : ((boostMat s).det * (boostMat s).det - 1) * eta4.det = 0 := by
      linear_combination h
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · exact absurd h1 hη
  refine isUnit_iff_ne_zero.mpr ?_
  intro h0
  rw [h0, mul_zero] at hsq
  exact zero_ne_one hsq

theorem feeds_finite_face (C : ContratoH2 W R N) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (C.E x)⁻¹ * C.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.E x)⁻¹) :=
  four_frame_gives_lorentz_metric (C.E x) (C.det_unit_on x hx)

theorem det_unit_along_orbit (C : ContratoH2 W R N) (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    IsUnit (C.E (wedgeBoostMap s x)).det := by
  rw [C.dragged s x hx, Matrix.det_mul]
  exact (boostMat_det_isUnit s).mul (C.det_unit_on x hx)

end ContratoH2

theorem curvedFrame_not_dragged :
    ¬ ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
        theCurvedFrame.E (wedgeBoostMap s x) = boostMat s * theCurvedFrame.E x := by
  intro h
  have hx : (![0, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp
  have h10 := congrFun (congrFun (h 1 _ hx) 1) 0
  rw [curvedFrame_E_apply, curvedFrame_E_apply] at h10
  simp [Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn] at h10
  exact (Real.sinh_pos_iff.mpr one_pos).ne' h10.symm

theorem curvedFrame_fiducial_not_modular (κ : ℝ) :
    ¬ ∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
        (fun i => theCurvedFrame.E x i 0) = c • killingField κ x := by
  intro h
  have hx : (![1/2, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp; norm_num
  obtain ⟨c, hc, hE⟩ := h _ hx
  have h0 := congrFun hE 0
  have h1 := congrFun hE 1
  simp [curvedFrame_E_apply, killingField, profileFn] at h0 h1
  rcases h1 with h1 | h1
  · exact hc.ne' h1
  · rw [h1, mul_zero] at h0
    norm_num at h0

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem frame_ne_curvedFrame_by_drag (C : ContratoH2 W R N) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_not_dragged
  intro s x hx
  have h := C.dragged s x hx
  rw [hE] at h
  exact h

theorem frame_ne_curvedFrame_by_fiducial (C : ContratoH2 W R N) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_fiducial_not_modular C.kappa
  intro x hx
  have h := C.fiducial_is_modular x hx
  rw [hE] at h
  exact h

end ContratoH2

/-! ## §H — ★★★ H3 v3.1 -/

/-- aritmética de pontos no gerador. -/
theorem shift_point (x : Fin 4 → ℝ) (l μ : ℝ) :
    (x + l • nullDir) + (μ - l) • nullDir = x + μ • nullDir := by
  rw [add_assoc, ← add_smul]
  congr 2
  ring

/-- [DERIVED] a carga nula de uma energia nula identicamente nula é 0. -/
theorem nullPlaneCharge_of_zero {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H)
    (h : ∀ x, nullEnergy T ψ x = 0) : nullPlaneCharge T ψ = 0 := by
  unfold nullPlaneCharge
  have : (fun p : ℝ × (Fin 2 → ℝ) => p.1 * nullEnergy T ψ (p.1 • nullDir + screenEmbed p.2))
      = fun _ => (0:ℝ) := by
    funext p; rw [h, mul_zero]
  rw [this, integral_zero]

/-- [DERIVED] o vácuo não tem energia nula (T_vac). -/
theorem nullEnergy_vac {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (x : Fin 4 → ℝ) :
    nullEnergy T W.vac x = 0 := by
  simp [nullEnergy, pairing, T.T_vac]

/-- [DERIVED] a energia nula é covariante (T_covariant). -/
theorem nullEnergy_covariant {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (a : Fin 4 → ℝ)
    (ψ : W.H) (x : Fin 4 → ℝ) : nullEnergy T (W.U a ψ) x = nullEnergy T ψ (x - a) := by
  simp [nullEnergy, T.T_covariant]

theorem areaDensity_smul (c : ℝ) (h : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (x : Fin 4 → ℝ) :
    areaDensity (fun y => c • h y) x = c * areaDensity h x := by
  simp [areaDensity]
  ring

namespace ContratoH3

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
  {T : StressTensorData W}

/-- [DERIVED] a resposta do vácuo é nula (T_vac + propagator_zero). -/
theorem response_vac (C : ContratoH3 W R N T) : C.response W.vac = 0 := by
  unfold ContratoH3.response
  have h : T.T W.vac = 0 := by funext x; exact T.T_vac x
  rw [h, C.propagator_zero]

/-- [DERIVED] ★ a COVARIÂNCIA DA RESPOSTA é teorema (T_covariant + propagator_covariant). -/
theorem response_covariant_v31 (C : ContratoH3 W R N T) (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ) :
    C.response (W.U a ψ) x = C.response ψ (x - a) := by
  unfold ContratoH3.response
  have h : T.T (W.U a ψ) = fun y => T.T ψ (y - a) := by funext y; exact T.T_covariant a ψ y
  rw [h, C.propagator_covariant]

/-- [DERIVED] ★★ MESMA FONTE, MESMA GEOMETRIA: dois estados com o mesmo ⟨T⟩ têm a mesma resposta (não há escolha
    por estado — a objeção central dos dois céticos). -/
theorem same_source_same_geometry (C : ContratoH3 W R N T) {ψ φ : W.H} (h : T.T ψ = T.T φ) :
    C.response ψ = C.response φ := by
  unfold ContratoH3.response
  rw [h]

/-- [DERIVED] θ é a derivada da densidade de área em TODO parâmetro do gerador (não só em 0). -/
theorem theta_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (l : ℝ) :
    HasDerivAt (fun μ => areaDensity (C.response ψ) (x + μ • nullDir))
      (C.theta ψ (x + l • nullDir)) l := by
  have h := C.theta_is_expansion ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => areaDensity (C.response ψ) ((x + l • nullDir) + ν • nullDir))
      (C.theta ψ (x + l • nullDir)) (l - l) := by rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => areaDensity (C.response ψ) (x + μ • nullDir))
      = fun μ => areaDensity (C.response ψ) ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

/-- [DERIVED] a lei local em TODO parâmetro do gerador. -/
theorem theta_deriv_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (l : ℝ) :
    HasDerivAt (fun μ => C.theta ψ (x + μ • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) l := by
  have h := C.raychaudhuri_einstein ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => C.theta ψ ((x + l • nullDir) + ν • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) (l - l) := by
    rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => C.theta ψ (x + μ • nullDir))
      = fun μ => C.theta ψ ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

/-- [DERIVED] ★★★ A PRIMEIRA LEI DA JANELA (integração EXATA, sem janela pequena): em todo gerador nulo por x,
    para todo corte c e toda janela [c, d] cuja expansão se anula no fim (equilíbrio, θ(d) = 0),
        a(d) − a(c) = 8πG ∫_c^d (λ − c) T_nn(x + λn) dλ.
    Prova: F(μ) = (μ − c)θ(μ) − a(μ) tem F′ = (μ − c)·θ′ = −8πG(μ − c)T_nn (FTC). -/
theorem first_law_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowArea (C.response ψ) x c d = 8 * Real.pi * C.G * windowCharge T ψ x c d := by
  have hcont : Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)) :=
    C.energy_continuous ψ hψ x
  have hF : ∀ μ ∈ Set.uIcc c d,
      HasDerivAt (fun μ => (μ - c) * C.theta ψ (x + μ • nullDir)
          - areaDensity (C.response ψ) (x + μ • nullDir))
        (-(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) μ := by
    intro μ _
    have h1 := ((hasDerivAt_id μ).sub_const c).mul (theta_deriv_along C hψ x μ)
    have h2 := theta_along C hψ x μ
    refine (h1.sub h2).congr_deriv ?_
    simp only [id]
    ring
  have hint : IntervalIntegrable
      (fun μ => -(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) volume c d := by
    apply Continuous.intervalIntegrable
    exact continuous_const.mul ((continuous_id.sub continuous_const).mul hcont)
  have hI := intervalIntegral.integral_eq_sub_of_hasDerivAt hF hint
  rw [intervalIntegral.integral_const_mul] at hI
  unfold windowArea windowCharge
  rw [hθ] at hI
  simp only [sub_self, zero_mul, mul_zero, zero_sub] at hI
  linarith [hI]

/-- [DERIVED] ★★ BEKENSTEIN–HAWKING DA JANELA: δS = δA/(4G), com δS = 2π × a carga unilateral do corte. -/
theorem bekenstein_hawking_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowEntropy T ψ x c d = windowArea (C.response ψ) x c d / (4 * C.G) := by
  rw [first_law_window C hψ x c d hθ]
  unfold windowEntropy
  have hG := C.G_pos.ne'
  field_simp
  ring

/-- [DERIVED] CLAUSIUS da janela: δQ = T_U·δS — IDENTIDADE (δS := δQ/T_U, a leitura do cético 2). -/
theorem clausius_window (C : ContratoH3 W R N T) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowHeat C.H2.kappa T ψ x c d = C.H2.unruhTemperature * windowEntropy T ψ x c d := by
  unfold windowHeat windowEntropy ContratoH2.unruhTemperature
  field_simp

/-- [DERIVED] ★ o 8πG da janela: δQ = κ·δA/(8πG). -/
theorem einstein_coefficient_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowHeat C.H2.kappa T ψ x c d
      = C.H2.kappa * windowArea (C.response ψ) x c d / (8 * Real.pi * C.G) := by
  rw [clausius_window, bekenstein_hawking_window C hψ x c d hθ]
  unfold ContratoH2.unruhTemperature
  exact einstein_coefficient_from_clausius _ _ _ C.G_pos.ne'

/-- [DERIVED] κ cancela: δQ/T_U = δS. -/
theorem kappa_cancels_window (C : ContratoH3 W R N T) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowHeat C.H2.kappa T ψ x c d / C.H2.unruhTemperature = windowEntropy T ψ x c d := by
  rw [clausius_window]
  have hT : C.H2.unruhTemperature ≠ 0 := by
    unfold ContratoH2.unruhTemperature
    exact div_ne_zero C.H2.kappa_pos.ne' (by positivity)
  field_simp

/-- [DERIVED] ★ a energia nula NÃO se anula: há estado admissível e ponto com T_nn ≠ 0
    (de `admissible_nontrivial` + `modular_charge`). -/
theorem nontrivial_null_energy (C : ContratoH3 W R N T) :
    ∃ ψ ∈ C.admissible, ∃ x : Fin 4 → ℝ, nullEnergy T ψ x ≠ 0 := by
  obtain ⟨ψ, hψ, k, hk, hk0⟩ := C.admissible_nontrivial
  refine ⟨ψ, hψ, ?_⟩
  by_contra hcon
  push_neg at hcon
  have h := C.modular_charge ψ hψ k hk
  rw [nullPlaneCharge_of_zero T ψ hcon, mul_zero] at h
  exact hk0 h

/-- [DERIVED] ★★ A EXPANSÃO NÃO É CONSTANTE: em todo habitante há estado admissível e gerador em que θ varia.
    (Refuta todo «ajustador» cuja densidade de área é afim ao longo dos geradores.) -/
theorem expansion_not_constant (C : ContratoH3 W R N T) :
    ∃ ψ ∈ C.admissible, ∃ x : Fin 4 → ℝ, ∃ l : ℝ,
      C.theta ψ (x + l • nullDir) ≠ C.theta ψ (x + 0 • nullDir) := by
  obtain ⟨ψ, hψ, x, hx⟩ := nontrivial_null_energy C
  refine ⟨ψ, hψ, x, ?_⟩
  by_contra hcon
  push_neg at hcon
  have hfun : (fun l : ℝ => C.theta ψ (x + l • nullDir)) = fun _ => C.theta ψ (x + 0 • nullDir) := by
    funext l; exact hcon l
  have h := C.raychaudhuri_einstein ψ hψ x
  rw [hfun] at h
  have h0 := h.unique (hasDerivAt_const (0:ℝ) (C.theta ψ (x + 0 • nullDir)))
  have hG : 8 * Real.pi * C.G ≠ 0 := by have := C.G_pos; positivity
  rcases mul_eq_zero.mp h0 with h1 | h1
  · exact hG (neg_eq_zero.mp h1)
  · exact hx h1

/-- [DERIVED] a resposta nula é recusada: se `response ψ = 0` para todo estado admissível, contradição. -/
theorem response_not_identically_zero (C : ContratoH3 W R N T) :
    ¬ ∀ ψ ∈ C.admissible, C.response ψ = 0 := by
  intro h0
  obtain ⟨ψ, hψ, x, l, hne⟩ := expansion_not_constant C
  apply hne
  have hz : ∀ y, C.theta ψ y = 0 := by
    intro y
    have h : HasDerivAt (fun l : ℝ => areaDensity (C.response ψ) (y + l • nullDir)) (C.theta ψ y) 0 :=
      C.theta_is_expansion ψ hψ y
    have hfun : (fun l : ℝ => areaDensity (C.response ψ) (y + l • nullDir)) = fun _ => (0:ℝ) := by
      funext l; rw [h0 ψ hψ]; simp [areaDensity]
    rw [hfun] at h
    exact h.unique (hasDerivAt_const (0:ℝ) (0:ℝ))
  rw [hz, hz]

/-- [DERIVED] ★★ (refuta o ajustador «inclinação por estado» dos céticos, porte linear de `toyResp`/`expFrame`)
    NENHUM habitante tem resposta da forma h_ψ(x) = (c(ψ)·x⁰)·M: a covariância força c ≡ 0, e então a
    resposta é nula — recusada acima. -/
theorem slope_response_excluded (C : ContratoH3 W R N T) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ) (hresp : ∀ ψ x, C.response ψ x = (c ψ * x 0) • M) : False := by
  apply response_not_identically_zero C
  intro ψ hψ
  by_cases hM : M = 0
  · funext x; rw [hresp, hM, smul_zero]; rfl
  · have hc : c ψ = 0 := by
      have h := C.response_covariant_v31 ![1, 0, 0, 0] ψ 0
      rw [hresp, hresp] at h
      simp only [Pi.zero_apply, mul_zero, zero_smul, zero_sub, Pi.neg_apply] at h
      have h' : (c ψ * -(1:ℝ)) • M = 0 := by
        simpa using h.symm
      rcases smul_eq_zero.mp h' with h1 | h1
      · linarith
      · exact absurd h1 hM
    funext x; rw [hresp, hc, zero_mul, zero_smul]; rfl

/-- [DERIVED] ★★ (refuta o porte exponencial do ajustador) NENHUM habitante tem resposta
    h_ψ(x) = (e^{c(ψ)·x⁰} − 1)·M: a covariância força e^{−c(ψ)} = 1, logo c ≡ 0 e a resposta é nula. -/
theorem exp_response_excluded (C : ContratoH3 W R N T) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hresp : ∀ ψ x, C.response ψ x = (Real.exp (c ψ * x 0) - 1) • M) : False := by
  apply response_not_identically_zero C
  intro ψ hψ
  by_cases hM : M = 0
  · funext x; rw [hresp, hM, smul_zero]; rfl
  · have hc : c ψ = 0 := by
      have h := C.response_covariant_v31 ![1, 0, 0, 0] ψ 0
      rw [hresp, hresp] at h
      simp only [Pi.zero_apply, mul_zero, Real.exp_zero, sub_self, zero_smul, zero_sub,
        Pi.neg_apply] at h
      have h' : (Real.exp (c ψ * -(1:ℝ)) - 1) • M = 0 := by
        simpa using h.symm
      rcases smul_eq_zero.mp h' with h1 | h1
      · have h2 : Real.exp (c ψ * -(1:ℝ)) = 1 := by linarith
        have h3 := Real.exp_eq_one_iff _ |>.mp h2
        linarith
      · exact absurd h1 hM
    funext x; rw [hresp, hc, zero_mul, Real.exp_zero, sub_self, zero_smul]; rfl

/-- [DERIVED] ★★ o ajustador POR FONTE (o porte mais forte dos céticos na v3.1) é excluído: nenhum habitante
    tem propagador da forma 𝔉(f)(x) = (c(f)·x⁰)·M. -/
theorem slope_propagator_excluded (C : ContratoH3 W R N T)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hP : ∀ f x, C.propagator f x = (c f * x 0) • M) : False :=
  slope_response_excluded C (fun ψ => c (T.T ψ)) M (fun ψ x => hP (T.T ψ) x)

/-- [DERIVED] ★★ idem para o porte exponencial por fonte. -/
theorem exp_propagator_excluded (C : ContratoH3 W R N T)
    (c : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → ℝ) (M : Matrix (Fin 4) (Fin 4) ℝ)
    (hP : ∀ f x, C.propagator f x = (Real.exp (c f * x 0) - 1) • M) : False :=
  exp_response_excluded C (fun ψ => c (T.T ψ)) M (fun ψ x => hP (T.T ψ) x)

/-- ★ G NÃO É PREDITO (rota de Jacobson, G = 1/(4ħη) é entrada): de todo habitante sai outro, com o MESMO H2, a
    MESMA classe e o MESMO T, e G' arbitrário — a resposta escala por G'/G. [KNOWN: Jacobson 1995.] -/
def rescaleG (C : ContratoH3 W R N T) (G' : ℝ) (hG' : 0 < G') : ContratoH3 W R N T where
  H2 := C.H2
  G := G'
  G_pos := hG'
  admissible := C.admissible
  admissible_unit := C.admissible_unit
  vac_admissible := C.vac_admissible
  admissible_translate := C.admissible_translate
  modular_charge := C.modular_charge
  admissible_nontrivial := C.admissible_nontrivial
  energy_continuous := C.energy_continuous
  background_screen_flat := C.background_screen_flat
  propagator := fun f x => (G' / C.G) • C.propagator f x
  propagator_zero := by
    funext x
    rw [C.propagator_zero]
    simp
  propagator_covariant := by
    intro a f
    funext x
    rw [C.propagator_covariant]
  response_symm := by
    intro ψ hψ x
    rw [Matrix.transpose_smul, C.response_symm ψ hψ x]
  lightcone_gauge := by
    intro ψ hψ x
    rw [Matrix.smul_mulVec, C.lightcone_gauge ψ hψ x, smul_zero]
  theta := fun ψ x => (G' / C.G) * C.theta ψ x
  theta_is_expansion := by
    intro ψ hψ x
    have h := (C.theta_is_expansion ψ hψ x).const_mul (G' / C.G)
    have e : (fun l : ℝ => areaDensity (fun y => (G' / C.G) • C.propagator (T.T ψ) y) (x + l • nullDir))
        = fun l => (G' / C.G) * areaDensity (C.propagator (T.T ψ)) (x + l • nullDir) := by
      funext l; exact areaDensity_smul _ _ _
    rw [e]; exact h
  raychaudhuri_einstein := by
    intro ψ hψ x
    have h := (C.raychaudhuri_einstein ψ hψ x).const_mul (G' / C.G)
    refine h.congr_deriv ?_
    have hG := C.G_pos.ne'
    field_simp

theorem G_not_predicted (C : ContratoH3 W R N T) (G' : ℝ) (hG' : 0 < G') :
    ∃ C' : ContratoH3 W R N T, C'.H2 = C.H2 ∧ C'.G = G' ∧ C'.admissible = C.admissible :=
  ⟨rescaleG C G' hG', rfl, rfl, rfl⟩

/-! ### consumidores dos campos de significado (resposta ao cético 2: campo sem consumidor é campo sem dente) -/

/-- [DERIVED] (lê `vac_admissible`) o VÁCUO ESTÁ EM EQUILÍBRIO: θ_Ω ≡ 0. -/
theorem theta_vac (C : ContratoH3 W R N T) (x : Fin 4 → ℝ) : C.theta W.vac x = 0 := by
  have h : HasDerivAt (fun l : ℝ => areaDensity (C.response W.vac) (x + l • nullDir)) (C.theta W.vac x) 0 :=
    C.theta_is_expansion W.vac C.vac_admissible x
  have hfun : (fun l : ℝ => areaDensity (C.response W.vac) (x + l • nullDir)) = fun _ => (0:ℝ) := by
    funext l; rw [response_vac]; simp [areaDensity]
  rw [hfun] at h
  exact h.unique (hasDerivAt_const (0:ℝ) (0:ℝ))

theorem windowCharge_covariant (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowCharge T (W.U a ψ) x c d = windowCharge T ψ (x - a) c d := by
  unfold windowCharge
  congr 1
  funext l
  rw [nullEnergy_covariant]
  congr 2
  abel

theorem windowArea_covariant (C : ContratoH3 W R N T) (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ)
    (c d : ℝ) : windowArea (C.response (W.U a ψ)) x c d = windowArea (C.response ψ) (x - a) c d := by
  unfold windowArea areaDensity
  rw [response_covariant_v31, response_covariant_v31]
  have e1 : x + d • nullDir - a = x - a + d • nullDir := by abel
  have e2 : x + c • nullDir - a = x - a + c • nullDir := by abel
  rw [e1, e2]

/-- [DERIVED] ★ (lê `admissible_translate`) A LEI VALE EM TODA A FAMÍLIA TRANSLADADA DE HORIZONTES: a primeira
    lei da janela do estado U(a)ψ no gerador por x é a do estado ψ no gerador por x − a — o mesmo G, o mesmo T. -/
theorem first_law_translated (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (a : Fin 4 → ℝ) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : C.theta (W.U a ψ) (x + d • nullDir) = 0) :
    windowArea (C.response ψ) (x - a) c d = 8 * Real.pi * C.G * windowCharge T ψ (x - a) c d := by
  have h := first_law_window C (C.admissible_translate a ψ hψ) x c d hθ
  rw [windowArea_covariant, windowCharge_covariant] at h
  exact h

/-- [DERIVED] (lê `lightcone_gauge`) o gerador continua NULO na métrica perturbada: δg_nn = nᵀ h n = 0. -/
theorem response_null_null_zero (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) : pairing (C.response ψ x) nullDir nullDir = 0 := by
  unfold pairing ContratoH3.response
  rw [C.lightcone_gauge ψ hψ x, dotProduct_zero]

/-- [DERIVED] (lê `response_symm` + `lightcone_gauge`) o gauge vale nos DOIS índices: nᵀ h = 0. -/
theorem response_row_null (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) : Matrix.vecMul nullDir (C.response ψ x) = 0 := by
  unfold ContratoH3.response
  rw [← Matrix.mulVec_transpose, C.response_symm ψ hψ x, C.lightcone_gauge ψ hψ x]

/-- [DERIVED] ★ (lê `background_screen_flat`) a DENSIDADE DE ÁREA LINEARIZADA É a variação de primeira ordem da
    área da tela do FUNDO DE H2: d/dε √|det(tela(g_H2 + ε h))| em ε = 0 é −(h₂₂ + h₃₃)/2. -/
theorem areaDensity_is_linearized_area (C : ContratoH3 W R N T) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge)
    (h : Matrix (Fin 4) (Fin 4) ℝ) :
    HasDerivAt (fun ε : ℝ => Real.sqrt |(screenBlockV31 (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det|)
      (-(h 2 2 + h 3 3) / 2) 0 := by
  have hflat := C.background_screen_flat x hx
  have hb : ∀ ε : ℝ, screenBlockV31 (solderMetric4 (C.H2.E x)⁻¹ + ε • h)
      = screenBlockV31 (solderMetric4 (C.H2.E x)⁻¹) + ε • screenBlockV31 h := by
    intro ε; ext i j; fin_cases i <;> fin_cases j <;> simp [screenBlockV31]
  set p : ℝ → ℝ := fun ε => (-1 + ε * h 2 2) * (-1 + ε * h 3 3) - (ε * h 2 3) * (ε * h 3 2) with hp
  have hdet : ∀ ε : ℝ, (screenBlockV31 (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det = p ε := by
    intro ε
    rw [hb, hflat, Matrix.det_fin_two]
    simp [screenBlockV31, hp]
  have hp0 : p 0 = 1 := by simp [hp]
  have hpd : HasDerivAt p (-(h 2 2 + h 3 3)) 0 := by
    have h1 : HasDerivAt (fun ε : ℝ => -1 + ε * h 2 2) (h 2 2) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).mul_const (h 2 2)).const_add (-1)
    have h2 : HasDerivAt (fun ε : ℝ => -1 + ε * h 3 3) (h 3 3) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).mul_const (h 3 3)).const_add (-1)
    have h3a : HasDerivAt (fun ε : ℝ => ε * h 2 3) (h 2 3) 0 := by
      simpa using (hasDerivAt_id (0:ℝ)).mul_const (h 2 3)
    have h3b : HasDerivAt (fun ε : ℝ => ε * h 3 2) (h 3 2) 0 := by
      simpa using (hasDerivAt_id (0:ℝ)).mul_const (h 3 2)
    have h3 : HasDerivAt (fun ε : ℝ => (ε * h 2 3) * (ε * h 3 2)) 0 0 := by
      refine (h3a.mul h3b).congr_deriv ?_
      simp
    have := (h1.mul h2).sub h3
    refine this.congr_deriv ?_
    simp only [zero_mul, mul_zero, add_zero, zero_add, sub_zero]
    ring
  have hcont : ContinuousAt p 0 := hpd.continuousAt
  have hpos : ∀ᶠ ε in 𝓝 (0:ℝ), 0 < p ε := by
    have : (0:ℝ) < p 0 := by rw [hp0]; norm_num
    exact hcont.eventually (lt_mem_nhds this)
  have hev : (fun ε : ℝ => Real.sqrt |(screenBlockV31 (solderMetric4 (C.H2.E x)⁻¹ + ε • h)).det|)
      =ᶠ[𝓝 (0:ℝ)] fun ε => Real.sqrt (p ε) := by
    filter_upwards [hpos] with ε hε
    rw [hdet, abs_of_pos hε]
  have hsq : HasDerivAt (fun ε => Real.sqrt (p ε)) (-(h 2 2 + h 3 3) / (2 * Real.sqrt (p 0))) 0 :=
    hpd.sqrt (by rw [hp0]; norm_num)
  rw [hp0, Real.sqrt_one, mul_one] at hsq
  exact hsq.congr_of_eventuallyEq hev

/-- a PROJEÇÃO no consumidor legado `HorizonEquilibriumData`, numa janela de equilíbrio DADA (os números são
    CALCULADOS: δA = a(d) − a(c), δS = 2π·carga, δQ = κ·carga). -/
def toHorizonData (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) : HorizonEquilibriumData where
  kappa := C.H2.kappa
  G := C.G
  G_pos := C.G_pos
  dA := windowArea (C.response ψ) x c d
  dS := windowEntropy T ψ x c d
  dQ := windowHeat C.H2.kappa T ψ x c d
  area_entropy := bekenstein_hawking_window C hψ x c d hθ
  clausius := by
    have := clausius_window C ψ x c d
    unfold ContratoH2.unruhTemperature at this
    exact this

/-- [DERIVED] ★★ o contrato ALIMENTA o teorema mestre (v74), numa janela de equilíbrio dada. -/
theorem feeds_the_master (C : ContratoH3 W R N T)
    {L : Type} [Lattice L] [BoundedOrder L] {Tr : SubadditiveTraceData L}
    (S : SusyRelativeData L Tr) {x₀ : Fin 4 → ℝ} (hx₀ : x₀ ∈ rightWedge)
    {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    (0 < Tr.tau S.ker ∧ Tr.tau S.ker < ⊤) ∧
      Tr.tau S.ker / Tr.tau S.ker = 1 ∧
      ((C.H2.E x₀)⁻¹ * C.H2.E x₀ = 1 ∧ LorentzByCongruence (solderMetric4 (C.H2.E x₀)⁻¹)) ∧
      (C.toHorizonData hψ x c d hθ).dQ = (C.toHorizonData hψ x c d hθ).kappa
        * (C.toHorizonData hψ x c d hθ).dA / (8 * Real.pi * (C.toHorizonData hψ x c d hθ).G) :=
  emergence_master_full_triad S (C.H2.E x₀) (C.H2.det_unit_on x₀ hx₀) (C.toHorizonData hψ x c d hθ)

end ContratoH3

/-! ## §I — as paredes -/

theorem contratoH2_empty_of_unfaithful (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization)
    (h : ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ W.U a = 1) : IsEmpty (ContratoH2 W R N) :=
  ⟨fun C => by
    obtain ⟨a, ha, hU⟩ := h
    exact ha (C.translations_faithful a hU)⟩

theorem contratoH2_empty_on_legacy (N : KillingNormalization) :
    IsEmpty (ContratoH2 theSpecificAQFTWitness regularModularRealization N) :=
  contratoH2_empty_of_unfaithful _ _ N ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩

theorem contratoH3_empty_on_legacy (N : KillingNormalization)
    (T : StressTensorData theSpecificAQFTWitness) :
    IsEmpty (ContratoH3 theSpecificAQFTWitness regularModularRealization N T) :=
  ⟨fun C => (contratoH2_empty_on_legacy N).false C.H2⟩

theorem ContratoH2.commuting_translations_excluded {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} {N : KillingNormalization} (C : ContratoH2 W R N) :
    ¬ ∀ (t : ℝ) (a : Fin 4 → ℝ), (C.Δit t).conjStarAlgEquiv (W.U a) = W.U a := by
  intro hcomm
  set m : Fin 4 → ℝ := (Real.exp (-(2 * Real.pi)) - 1) • nullDir with hm
  have hm0 : m ≠ 0 := by
    intro h0
    have h := congrFun h0 0
    have hlt : Real.exp (-(2 * Real.pi)) < 1 := by
      have := Real.exp_lt_exp.mpr (show -(2 * Real.pi) < 0 by
        have := Real.pi_pos; linarith)
      simpa using this
    simp [hm, nullDir] at h
    linarith
  apply hm0
  apply C.translations_faithful
  have hB := C.poincare_relation 1 nullDir
  rw [hcomm, wedgeBoostMap_nullDir, mul_one] at hB
  have hsplit : Real.exp (-(2 * Real.pi)) • nullDir = nullDir + m := by
    rw [hm, sub_smul, one_smul]; abel
  rw [hsplit, W.U_add] at hB
  have hinv : W.U (-nullDir) * W.U nullDir = 1 := by
    rw [← W.U_add, neg_add_cancel, W.U_zero]
  calc W.U m = (W.U (-nullDir) * W.U nullDir) * W.U m := by rw [hinv, one_mul]
    _ = W.U (-nullDir) * (W.U nullDir * W.U m) := by rw [mul_assoc]
    _ = W.U (-nullDir) * W.U nullDir := by rw [← hB]
    _ = 1 := hinv

/-- [DERIVED] ★ o sinal de BW é load-bearing: nenhum habitante satisfaz também Δ^{it} = V(+2πt). -/
theorem ContratoH2.bw_sign_matters {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} (C : ContratoH2 W R N) :
    ¬ ∀ t : ℝ, C.Δit t = C.boost.V (2 * Real.pi * t) := by
  intro hflip
  apply C.trivial_boost_excluded
  intro s
  have hpi : (4 * Real.pi) ≠ 0 := by positivity
  have h1 := hflip (s / (4 * Real.pi))
  rw [C.bw] at h1
  -- V(−s/2) = V(s/2) ⟹ V(s) = V(s/2 + s/2) = V(s/2)∘V(s/2) = V(s/2)∘V(−s/2) = 1
  have e1 : -(2 * Real.pi * (s / (4 * Real.pi))) = -(s / 2) := by field_simp; ring
  have e2 : 2 * Real.pi * (s / (4 * Real.pi)) = s / 2 := by field_simp; ring
  rw [e1, e2] at h1
  have hsum : C.boost.V s = (C.boost.V (s / 2)).trans (C.boost.V (s / 2)) := by
    rw [← C.boost.V_add]; congr 1; ring
  have hzero : (C.boost.V (-(s / 2))).trans (C.boost.V (s / 2)) = LinearIsometryEquiv.refl ℂ W.H := by
    rw [← C.boost.V_add, add_neg_cancel, C.boost.V_zero]
  rw [hsum]
  rw [← h1] at hzero ⊢
  exact hzero

/-! ## §J — o import indexado -/

theorem ContratoImportH3.nonvacuous {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} {T : StressTensorData W}
    {h2 : ContratoH2 W R N} (I : ContratoImportH3 W R N T h2) : Nonempty (ContratoH3 W R N T) :=
  ⟨I.produce h2⟩

theorem ContratoImportH3.same_horizon_data {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} {T : StressTensorData W}
    {h2 : ContratoH2 W R N} (I : ContratoImportH3 W R N T h2) :
    (I.produce h2).H2.kappa = h2.kappa ∧ (I.produce h2).H2.Δit = h2.Δit ∧
      (I.produce h2).H2.boost = h2.boost := by
  rw [I.same_horizon h2]
  exact ⟨rfl, rfl, rfl⟩

theorem no_import_on_legacy (N : KillingNormalization) (T : StressTensorData theSpecificAQFTWitness) :
    ¬ ∃ h2 : ContratoH2 theSpecificAQFTWitness regularModularRealization N,
        Nonempty (ContratoImportH3 theSpecificAQFTWitness regularModularRealization N T h2) :=
  fun ⟨h2, _⟩ => (contratoH2_empty_on_legacy N).false h2

/-! ## Os `#print axioms` -/

#print axioms U_norm
#print axioms ContratoH2.Δit_vac
#print axioms ContratoH2.bw_covariance
#print axioms ContratoH2.poincare_relation
#print axioms ContratoH2.translates
#print axioms ContratoH2.eigen_null_correlation_dilation
#print axioms ContratoH2.no_point_spectrum
#print axioms ContratoH2.trivial_boost_excluded
#print axioms ContratoH2.boost_moves_null_eigen
#print axioms ContratoH2.null_eigen_orth
#print axioms ContratoH2.null_point_spectrum_excluded
#print axioms transverse_U_excluded
#print axioms discrete_null_momentum_excluded
#print axioms translate_null_subset
#print axioms halfsided_inclusion
#print axioms ContratoH2.contract_borchers_form
#print axioms positiveEnergy_orientation
#print axioms KMSAt.rescale
#print axioms ContratoH2.modular_is_boost_at_two_pi
#print axioms ContratoH2.unruh_is_kms
#print axioms ContratoH2.unruh_is_kms_temperature
#print axioms ContratoH2.kms_product_is_two_pi
#print axioms ContratoH2.refRadius_pos
#print axioms ContratoH2.kappa_mul_radius
#print axioms ContratoH2.kappa_eq_inv_radius
#print axioms ContratoH2.kappa_fixed
#print axioms ContratoH2.no_rekappa
#print axioms ContratoH2.observer_unit_of_index
#print axioms ContratoH2.reindex
#print axioms ContratoH2.kappa_is_input
#print axioms ContratoH2.killingFlow_add
#print axioms ContratoH2.killingFlow_zero
#print axioms ContratoH2.modularEnergy_of_boostEnergy
#print axioms ContratoH2.modularEnergy_unique
#print axioms ContratoH2.vac_modularEnergy
#print axioms ContratoH2.vac_boostEnergy
#print axioms ContratoH2.inner_vac_Δit
#print axioms ContratoH2.bilateral_no_first_order
#print axioms implementer_unique
#print axioms tower_excluded
#print axioms ContratoH2.Δit_determined
#print axioms ContratoH2.Δit_index_free
#print axioms ContratoH2.boostMat_det_isUnit
#print axioms ContratoH2.feeds_finite_face
#print axioms ContratoH2.det_unit_along_orbit
#print axioms curvedFrame_not_dragged
#print axioms curvedFrame_fiducial_not_modular
#print axioms ContratoH2.frame_ne_curvedFrame_by_drag
#print axioms ContratoH2.frame_ne_curvedFrame_by_fiducial
#print axioms shift_point
#print axioms nullPlaneCharge_of_zero
#print axioms nullEnergy_vac
#print axioms nullEnergy_covariant
#print axioms areaDensity_smul
#print axioms ContratoH3.response_vac
#print axioms ContratoH3.response_covariant_v31
#print axioms ContratoH3.same_source_same_geometry
#print axioms ContratoH3.theta_along
#print axioms ContratoH3.theta_deriv_along
#print axioms ContratoH3.first_law_window
#print axioms ContratoH3.bekenstein_hawking_window
#print axioms ContratoH3.clausius_window
#print axioms ContratoH3.einstein_coefficient_window
#print axioms ContratoH3.kappa_cancels_window
#print axioms ContratoH3.nontrivial_null_energy
#print axioms ContratoH3.expansion_not_constant
#print axioms ContratoH3.response_not_identically_zero
#print axioms ContratoH3.slope_response_excluded
#print axioms ContratoH3.exp_response_excluded
#print axioms ContratoH3.slope_propagator_excluded
#print axioms ContratoH3.exp_propagator_excluded
#print axioms ContratoH3.rescaleG
#print axioms ContratoH3.G_not_predicted
#print axioms ContratoH3.theta_vac
#print axioms ContratoH3.windowCharge_covariant
#print axioms ContratoH3.windowArea_covariant
#print axioms ContratoH3.first_law_translated
#print axioms ContratoH3.response_null_null_zero
#print axioms ContratoH3.response_row_null
#print axioms ContratoH3.areaDensity_is_linearized_area
#print axioms ContratoH3.toHorizonData
#print axioms ContratoH3.feeds_the_master
#print axioms contratoH2_empty_of_unfaithful
#print axioms contratoH2_empty_on_legacy
#print axioms contratoH3_empty_on_legacy
#print axioms ContratoH2.commuting_translations_excluded
#print axioms ContratoH2.bw_sign_matters
#print axioms ContratoImportH3.nonvacuous
#print axioms ContratoImportH3.same_horizon_data
#print axioms no_import_on_legacy

end

end TGLExt.ContratoQGv31
