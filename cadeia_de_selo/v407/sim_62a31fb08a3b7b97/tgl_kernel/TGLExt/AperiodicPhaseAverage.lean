-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_046 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.PeriodAveragePrefix
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false

namespace ChatgptAudit.Aperiodic046

open TGLExt Matrix MeasureTheory Filter
open scoped Topology

noncomputable section

/-- The normalized interval average of one modular phase. No period is specified. -/
def phaseAverage (T r : ℝ) : ℂ :=
  T⁻¹ • (∫ t in (0 : ℝ)..T, modularPhase t r)

/-- The zero frequency survives every nondegenerate averaging interval. -/
theorem phase_average_zero (T : ℝ) (hT : T ≠ 0) :
    phaseAverage T 0 = 1 := by
  have hz (t : ℝ) : modularPhase t 0 = 1 := by
    simp [modularPhase]
  unfold phaseAverage
  simp_rw [hz]
  rw [intervalIntegral.integral_const, sub_zero, smul_smul,
    inv_mul_cancel₀ hT, one_smul]

/-- An exact primitive for a nonzero frequency; no endpoint phase is assumed. -/
theorem integral_phase_nonzero (T r : ℝ) (hr : r ≠ 0) :
    (∫ t in (0 : ℝ)..T, modularPhase t r) =
      (modularPhase T r - 1) / ((r : ℂ) * Complex.I) := by
  have hc : (r : ℂ) * Complex.I ≠ 0 :=
    mul_ne_zero (by exact_mod_cast hr) Complex.I_ne_zero
  have he (t : ℝ) :
      modularPhase t r = Complex.exp (((r : ℂ) * Complex.I) * t) := by
    unfold modularPhase
    congr 1
    push_cast
    ring
  simp_rw [he]
  rw [integral_exp_mul_complex hc]
  simp only [Complex.ofReal_zero, mul_zero, Complex.exp_zero]

/-- The nonresonant average is bounded by an explicit inverse-length estimate. -/
theorem phase_average_norm_le (T r : ℝ) (hT : 0 < T) (hr : r ≠ 0) :
    ‖phaseAverage T r‖ ≤ T⁻¹ * (2 / |r|) := by
  have hn : ‖modularPhase T r - 1‖ ≤ 2 := by
    calc
      ‖modularPhase T r - 1‖ ≤ ‖modularPhase T r‖ + ‖(1 : ℂ)‖ :=
        norm_sub_le _ _
      _ = 2 := by rw [modularPhase_norm, norm_one]; norm_num
  have hd : ‖(r : ℂ) * Complex.I‖ = |r| := by simp
  calc
    ‖phaseAverage T r‖ = T⁻¹ * (‖modularPhase T r - 1‖ / |r|) := by
      rw [phaseAverage, integral_phase_nonzero T r hr, norm_smul,
        norm_div, hd, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hT)]
    _ ≤ T⁻¹ * (2 / |r|) :=
      mul_le_mul_of_nonneg_left
        (div_le_div_of_nonneg_right hn (abs_nonneg r)) (inv_nonneg.mpr hT.le)

/-- Cesaro cancellation at every nonzero real frequency. -/
theorem phase_average_nonzero_limit (r : ℝ) (hr : r ≠ 0) :
    Tendsto (fun n : ℕ => phaseAverage ((n : ℝ) + 1) r)
      atTop (𝓝 0) := by
  apply squeeze_zero_norm (fun n : ℕ => phase_average_norm_le ((n : ℝ) + 1) r
    (by positivity) hr)
  have hi : Tendsto (fun n : ℕ => ((n : ℝ) + 1)⁻¹) atTop (𝓝 0) := by
    simpa only [one_div] using
      (tendsto_one_div_add_atTop_nhds_zero_nat :
        Tendsto (fun n : ℕ => 1 / ((n : ℝ) + 1)) atTop (𝓝 0))
  simpa only [zero_mul] using hi.mul_const (2 / |r|)

/-- Resonant and nonresonant frequencies are handled without a common period. -/
theorem phase_average_limit (r : ℝ) :
    Tendsto (fun n : ℕ => phaseAverage ((n : ℝ) + 1) r)
      atTop (𝓝 (if r = 0 then 1 else 0)) := by
  by_cases hr : r = 0
  · rw [if_pos hr]
    subst r
    have he : (fun n : ℕ => phaseAverage ((n : ℝ) + 1) 0) =
        fun _ : ℕ => (1 : ℂ) := by
      funext n
      exact phase_average_zero _ (ne_of_gt (by positivity))
    rw [he]
    exact tendsto_const_nhds
  · rw [if_neg hr]
    exact phase_average_nonzero_limit r hr

/-- The finite matrix average of the actual local modular flow. -/
def flowAverage (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  T⁻¹ • (∫ t in (0 : ℝ)..T, flowLevel P t N a)

theorem flow_average_entry (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    flowAverage P T N a i j =
      phaseAverage T (Real.log (towerW P N i) - Real.log (towerW P N j)) *
        a i j := by
  have hi := (matrixEntryCLM N i j).intervalIntegral_comp_comm (μ := volume)
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T)
  change (∫ t in (0 : ℝ)..T, flowLevel P t N a i j) =
    (∫ t in (0 : ℝ)..T, flowLevel P t N a) i j at hi
  change T⁻¹ • ((∫ t in (0 : ℝ)..T, flowLevel P t N a) i j) = _
  rw [← hi]
  simp only [flowLevel, intervalIntegral.integral_mul_const]
  rw [phaseAverage, smul_mul_assoc]

/-- The whole finite matrix converges to spectral pinching, including degenerate blocks. -/
theorem flow_average_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto (fun n : ℕ => flowAverage P ((n : ℝ) + 1) N a)
      atTop (𝓝 (specExpect (towerW P N) a)) := by
  apply tendsto_pi_nhds.mpr
  intro i
  apply tendsto_pi_nhds.mpr
  intro j
  have he : Real.log (towerW P N i) - Real.log (towerW P N j) = 0 ↔
      towerW P N i = towerW P N j := by
    rw [sub_eq_zero]
    exact ⟨Real.log_injOn_pos (towerW_pos P N i) (towerW_pos P N j),
      congrArg Real.log⟩
  have h := (phase_average_limit
    (Real.log (towerW P N i) - Real.log (towerW P N j))).mul_const (a i j)
  by_cases hij : towerW P N i = towerW P N j
  · have hr := he.mpr hij
    rw [if_pos hr, one_mul] at h
    simpa only [flow_average_entry, specExpect, Matrix.of_apply, if_pos hij] using h
  · have hr : Real.log (towerW P N i) - Real.log (towerW P N j) ≠ 0 :=
      fun hzero => hij (he.mp hzero)
    rw [if_neg hr, zero_mul] at h
    simpa only [flow_average_entry, specExpect, Matrix.of_apply, if_neg hij] using h

/-- The finite matrix average is exactly the average of its existing GNS image. -/
theorem local_average_eq_embedding (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    T⁻¹ • (∫ t in (0 : ℝ)..T, modularFlow P t (levelEmbedding P N a)) =
      levelEmbeddingCLM P N (flowAverage P T N a) := by
  have h (t : ℝ) : modularFlow P t (levelEmbedding P N a) =
      levelEmbeddingCLM P N (flowLevel P t N a) := by
    change modularFlow P t ((tof P N a : TowerPre P) : TowerHilbert P) = _
    rw [modularFlow_coe, flowPre_tof]
    rfl
  simp_rw [h]
  rw [(levelEmbeddingCLM P N).intervalIntegral_comp_comm
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T),
    flowAverage, (levelEmbeddingCLM P N).map_smul_of_tower]

/-- Local GNS vectors have an aperiodic Cesaro limit; this is not an expectation on M. -/
theorem local_average_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n : ℕ => ((n : ℝ) + 1)⁻¹ •
        (∫ t in (0 : ℝ)..((n : ℝ) + 1),
          modularFlow P t (levelEmbedding P N a)))
      atTop (𝓝 (levelEmbedding P N (specExpect (towerW P N) a))) := by
  have h := ((levelEmbeddingCLM P N).continuous.tendsto
    (specExpect (towerW P N) a)).comp (flow_average_limit P N a)
  have he : levelEmbeddingCLM P N (specExpect (towerW P N) a) =
      levelEmbedding P N (specExpect (towerW P N) a) := rfl
  rw [he] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun n =>
    (local_average_eq_embedding P ((n : ℝ) + 1) N a).symm)

#print axioms phaseAverage
#print axioms phase_average_zero
#print axioms integral_phase_nonzero
#print axioms phase_average_norm_le
#print axioms phase_average_nonzero_limit
#print axioms phase_average_limit
#print axioms flowAverage
#print axioms flow_average_entry
#print axioms flow_average_limit
#print axioms local_average_eq_embedding
#print axioms local_average_limit

end

end ChatgptAudit.Aperiodic046
