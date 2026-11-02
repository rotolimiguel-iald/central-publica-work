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
import TGLExt.TomitaClosability
import Mathlib.Analysis.Normed.Operator.Completeness
import Mathlib.Topology.MetricSpace.Cauchy

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Filter
open scoped Topology

noncomputable section

/-- Convergence on the cyclic vector propagates to each local right orbit. -/
theorem omega_limit_on_local (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (z : TowerHilbert P)
    (hz : Tendsto (fun n => C n (hOmega P)) atTop (𝓝 z))
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n => C n ((tof P N a : TowerPre P) : TowerHilbert P))
      atTop (𝓝 (rTowerPi P a z)) := by
  rw [← rTowerPi_omega (P := P) N a]
  have he : (fun n => C n (rTowerPi P a (hOmega P))) =
      (fun n => rTowerPi P a (C n (hOmega P))) := by
    funext n
    simpa only [mul_apply_eq_comp] using
      congrArg (fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A (hOmega P))
        (factor_comm_rTowerPi (hmem n) a)
  rw [he]
  exact ((rTowerPi P a).continuous.tendsto z).comp hz

/-- A common operator bound extends local Cauchy convergence to every Hilbert vector. -/
theorem bounded_local_cauchy (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound)
    (hnorm : ∀ n, ‖C n‖ ≤ bound)
    (hlocal : ∀ w : TowerPre P,
      CauchySeq (fun n => C n (w : TowerHilbert P)))
    (v : TowerHilbert P) :
    CauchySeq (fun n => C n v) := by
  apply Metric.cauchySeq_iff.mpr
  intro ε hε
  have hden : 0 < 4 * (bound + 1) := by positivity
  obtain ⟨w, hw⟩ := (towerPre_denseRange (P := P)).exists_dist_lt v
    (div_pos hε hden)
  have hshort : bound * dist v (w : TowerHilbert P) < ε / 4 := by
    have hmul := (lt_div_iff₀ hden).mp hw
    nlinarith [(dist_nonneg : 0 ≤ dist v (w : TowerHilbert P))]
  obtain ⟨N, hN⟩ := Metric.cauchySeq_iff.mp (hlocal w) (ε / 2) (by positivity)
  refine ⟨N, ?_⟩
  intro m hm n hn
  have hmshort : dist (C m v) (C m (w : TowerHilbert P)) < ε / 4 :=
    lt_of_le_of_lt
      ((C m).dist_le_opNorm v (w : TowerHilbert P) |>.trans
        (mul_le_mul_of_nonneg_right (hnorm m)
          (dist_nonneg : 0 ≤ dist v (w : TowerHilbert P)))) hshort
  have hnshort : dist (C n (w : TowerHilbert P)) (C n v) < ε / 4 := by
    rw [dist_comm]
    exact lt_of_le_of_lt
      ((C n).dist_le_opNorm v (w : TowerHilbert P) |>.trans
        (mul_le_mul_of_nonneg_right (hnorm n)
          (dist_nonneg : 0 ≤ dist v (w : TowerHilbert P)))) hshort
  have hmid := hN m hm n hn
  have htri := dist_triangle (C m v) (C m (w : TowerHilbert P)) (C n v)
  have htri' := dist_triangle (C m (w : TowerHilbert P))
    (C n (w : TowerHilbert P)) (C n v)
  linarith

/-- Strong limits preserve a fixed commutation relation, without a norm limit. -/
theorem strong_limit_commutes (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B Y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v)))
    (hcomm : ∀ n, Y * C n = C n * Y) :
    Y * B = B * Y := by
  ext v
  change Y (B v) = B (Y v)
  have he : (fun n => Y (C n v)) = (fun n => C n (Y v)) := by
    funext n
    simpa only [mul_apply_eq_comp] using
      congrArg (fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A v) (hcomm n)
  have hl := (Y.continuous.tendsto (B v)).comp (hlim v)
  change Tendsto (fun n => Y (C n v)) atTop (𝓝 (Y (B v))) at hl
  rw [he] at hl
  exact tendsto_nhds_unique hl (hlim (Y v))

/-- Membership in the factor passes to a strong limit through its defining bicommutant. -/
theorem factor_mem_of_strong_limit (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (hlim : ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v))) :
    B ∈ theFactorObject P := by
  change B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro Y hY
  have hc (n : ℕ) : Y * C n = C n * Y ∧ star Y * C n = C n * star Y := by
    have hn := hmem n
    change C n ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hn
    rw [StarSubalgebra.mem_centralizer_iff] at hn
    exact hn Y hY
  exact ⟨strong_limit_commutes P C B Y hlim (fun n => (hc n).1),
    strong_limit_commutes P C B (star Y) hlim (fun n => (hc n).2)⟩

/-- Construct a bounded operator in the factor from a bounded sequence and its limit on Ω.
The strong limit and the operator itself are conclusions, not inputs. -/
theorem bounded_omega_limit_lift (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (hnorm : ∀ n, ‖C n‖ ≤ bound)
    (z : TowerHilbert P)
    (hz : Tendsto (fun n => C n (hOmega P)) atTop (𝓝 z)) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ ‖B‖ ≤ bound ∧ B (hOmega P) = z ∧
      ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v)) := by
  have hlocal (w : TowerPre P) :
      CauchySeq (fun n => C n (w : TowerHilbert P)) := by
    obtain ⟨N, a, rfl⟩ := exists_tof w
    exact (omega_limit_on_local P C hmem z hz N a).cauchySeq
  have hex (v : TowerHilbert P) :
      ∃ y, Tendsto (fun n => C n v) atTop (𝓝 y) :=
    cauchySeq_tendsto_of_complete
      (bounded_local_cauchy P C bound hbound hnorm hlocal v)
  choose f hf using hex
  have hrange : Bornology.IsBounded (Set.range C) := by
    refine isBounded_iff_forall_norm_le.mpr ⟨bound, ?_⟩
    rintro D ⟨n, rfl⟩
    exact hnorm n
  let B : TowerHilbert P →L[ℂ] TowerHilbert P :=
    ContinuousLinearMap.ofTendstoOfBoundedRange f C (tendsto_pi_nhds.mpr hf) hrange
  have hBlim (v : TowerHilbert P) :
      Tendsto (fun n => C n v) atTop (𝓝 (B v)) := hf v
  have hBnorm : ‖B‖ ≤ bound := by
    apply B.opNorm_le_bound hbound
    intro v
    exact le_of_tendsto (hBlim v).norm
      (Filter.Eventually.of_forall fun n => (C n).le_of_opNorm_le (hnorm n) v)
  exact ⟨B, factor_mem_of_strong_limit P C B hmem hBlim, hBnorm,
    tendsto_nhds_unique (hBlim (hOmega P)) hz, hBlim⟩

/-- The constructed factor element is uniquely determined by its value on Ω. -/
theorem omega_lift_unique (P : SiteProfile)
    (B D : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hB : B ∈ theFactorObject P) (hD : D ∈ theFactorObject P)
    (z : TowerHilbert P) (hBz : B (hOmega P) = z) (hDz : D (hOmega P) = z) :
    B = D := by
  apply sub_eq_zero.mp
  apply factor_omega_separating ((theFactorObject P).sub_mem hB hD)
  change B (hOmega P) - D (hOmega P) = 0
  rw [hBz, hDz, sub_self]

#print axioms omega_limit_on_local
#print axioms bounded_local_cauchy
#print axioms strong_limit_commutes
#print axioms factor_mem_of_strong_limit
#print axioms bounded_omega_limit_lift
#print axioms omega_lift_unique

end

end ChatgptAudit.Aperiodic046
