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
import TGLExt.AperiodicPhaseAverage

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Matrix MeasureTheory Filter
open scoped Topology

noncomputable section

/-- Projecting a finite-time average is exactly the local finite matrix average. -/
theorem period_average_prefix_vector (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (N : ℕ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (periodAverage P T hT A) (hOmega P) =
      levelEmbeddingCLM P N (flowAverage P T N (expectationMatrix P N A)) := by
  rw [expectation_omega, (period_average_operator T hT A).1]
  have ho (t : ℝ) : modularConjugation P t A (hOmega P) =
      modularFlow P t (A (hOmega P)) := by
    change modularFlow P t (A (modularFlow P (-t) (hOmega P))) = _
    rw [modularFlow_fixes_omega]
  simp_rw [ho]
  rw [(levelProject P N).map_smul_of_tower,
    ← (levelProject P N).intervalIntegral_comp_comm
      ((modularFlow_strongly_continuous (A (hOmega P))).intervalIntegrable 0 T)]
  simp_rw [project_flow_commutes, ← expectation_omega]
  change T⁻¹ • (∫ t in (0 : ℝ)..T,
    modularFlow P t (towerPi P (expectationMatrix P N A) (hOmega P))) = _
  simp_rw [towerPi_omega]
  exact local_average_eq_embedding P T N (expectationMatrix P N A)

/-- Each finite cut of the time averages has the spectral-pinching limit. -/
theorem period_average_prefix_omega_limit (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    Tendsto
      (fun n : ℕ => towerExpectation P N
        (periodAverage P ((n : ℝ) + 1) (by positivity) A) (hOmega P))
      atTop (𝓝 (levelEmbedding P N
        (specExpect (towerW P N) (expectationMatrix P N A)))) := by
  have h := ((levelEmbeddingCLM P N).continuous.tendsto
      (specExpect (towerW P N) (expectationMatrix P N A))).comp
    (flow_average_limit P N (expectationMatrix P N A))
  have he : levelEmbeddingCLM P N
      (specExpect (towerW P N) (expectationMatrix P N A)) =
      levelEmbedding P N (specExpect (towerW P N) (expectationMatrix P N A)) := rfl
  rw [he] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun n =>
    (period_average_prefix_vector P ((n : ℝ) + 1) (by positivity) N A).symm)

/-- A limit on Ω forces the exact prefix identity; existence of that limit is separate. -/
theorem aperiodic_average_prefix_of_limit (P : SiteProfile) (N : ℕ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : Tendsto
      (fun n : ℕ => periodAverage P ((n : ℝ) + 1) (by positivity) A (hOmega P))
      atTop (𝓝 (B (hOmega P)))) :
    towerExpectation P N B =
      towerPi P (specExpect (towerW P N) (expectationMatrix P N A)) := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (towerPi_mem_factor _)
  rw [towerPi_omega]
  have h : Tendsto
      (fun n : ℕ => towerExpectation P N
        (periodAverage P ((n : ℝ) + 1) (by positivity) A) (hOmega P))
      atTop (𝓝 (towerExpectation P N B (hOmega P))) := by
    have hcomp := ((levelProject P N).continuous.tendsto (B (hOmega P))).comp hlim
    have he : levelProject P N (B (hOmega P)) =
        towerExpectation P N B (hOmega P) := by rw [expectation_omega]
    rw [he] at hcomp
    apply hcomp.congr'
    exact Filter.Eventually.of_forall (fun n : ℕ => by
      change levelProject P N
          (periodAverage P ((n : ℝ) + 1) (by positivity) A (hOmega P)) =
        towerExpectation P N
          (periodAverage P ((n : ℝ) + 1) (by positivity) A) (hOmega P)
      rw [expectation_omega])
  exact tendsto_nhds_unique h (period_average_prefix_omega_limit P N A)

#print axioms period_average_prefix_vector
#print axioms period_average_prefix_omega_limit
#print axioms aperiodic_average_prefix_of_limit

end

end ChatgptAudit.Aperiodic046
