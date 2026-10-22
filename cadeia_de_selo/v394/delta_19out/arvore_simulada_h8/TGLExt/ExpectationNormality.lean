-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_047 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.ExpectationContinuity
import TGLExt.GeneralExpectationPositive
import TGLExt.MonotoneOperatorLimit

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt Filter ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- A fixed commutation relation survives a strong limit along any nontrivial filter. -/
theorem strong_net_limit_commutes (P : SiteProfile)
    {ι : Type*} (l : Filter ι) [l.NeBot]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B Y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (B v)))
    (hcomm : ∀ i, Y * A i = A i * Y) :
    Y * B = B * Y := by
  ext v
  change Y (B v) = B (Y v)
  have he : (fun i => Y (A i v)) = (fun i => A i (Y v)) := by
    funext i
    simpa only [mul_apply_eq_comp] using
      congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T v) (hcomm i)
  have hl := (Y.continuous.tendsto (B v)).comp (hlim v)
  change Tendsto (fun i => Y (A i v)) l (𝓝 (Y (B v))) at hl
  rw [he] at hl
  exact tendsto_nhds_unique hl (hlim (Y v))

/-- The bicommutant defining M is strongly closed for arbitrary nets. -/
theorem factor_mem_of_net_strong_limit (P : SiteProfile)
    {ι : Type*} (l : Filter ι) [l.NeBot]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (B v))) :
    B ∈ theFactorObject P := by
  change B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro Y hY
  have hc (i : ι) : Y * A i = A i * Y ∧ star Y * A i = A i * star Y := by
    have hi := hmem i
    change A i ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hi
    rw [StarSubalgebra.mem_centralizer_iff] at hi
    exact hi Y hY
  exact ⟨strong_net_limit_commutes P l A B Y hlim (fun i => (hc i).1),
    strong_net_limit_commutes P l A B (star Y) hlim (fun i => (hc i).2)⟩

/-- Linearity and positivity imply monotonicity on the actual factor domain. -/
theorem expectation_order_preserving (P : SiteProfile) (I : ExpectationInput P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) (hAB : A ≤ B) :
    I.E A ≤ I.E B := by
  have h := general_expectation_nonnegative P I (B - A)
    ((theFactorObject P).sub_mem hB hA) (sub_nonneg.mpr hAB)
  rw [expectation_sub P I B A hB hA] at h
  exact sub_nonneg.mp h

/-- The supremum is constructed in M, and E preserves it for every bounded positive directed net. -/
theorem factor_monotone_supremum_and_expectation (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖A i‖ ≤ C) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ 0 ≤ B ∧ ‖B‖ ≤ C ∧
      IsLUB (Set.range A) B ∧
      IsLUB (Set.range (fun i => I.E (A i))) (I.E B) ∧
      (∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) ∧
      (∀ v, Tendsto (fun i => I.E (A i) v) atTop (𝓝 (I.E B v))) := by
  obtain ⟨B, hBpos, hBbound, hlim, hsup⟩ :=
    monotone_operator_limit A hpos hmono C hC hbound
  have hBmem := factor_mem_of_net_strong_limit P atTop A B hmem hlim
  have hElim := expectation_strong_tendsto_of_omega P I atTop A B
    hmem hBmem C hC hbound (hlim (hOmega P))
  have hEmono : Monotone (fun i => I.E (A i)) := by
    intro i j hij
    exact expectation_order_preserving P I (A i) (A j) (hmem i) (hmem j) (hmono hij)
  exact ⟨B, hBmem, hBpos, hBbound, hsup,
    monotone_strong_limit_isLUB (fun i => I.E (A i)) hEmono (I.E B) hElim,
    hlim, hElim⟩

/-- An order bound suffices: positivity converts it into a uniform norm bound. -/
theorem expectation_preserves_order_bounded_nets (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (hbound : ∀ i, A i ≤ D) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ IsLUB (Set.range A) B ∧
      IsLUB (Set.range (fun i => I.E (A i))) (I.E B) := by
  have hn (i : ι) : ‖A i‖ ≤ ‖D‖ :=
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hbound i)
  obtain ⟨B, hBmem, _, _, hsup, hEsup, _, _⟩ :=
    factor_monotone_supremum_and_expectation P I A hmem hpos hmono ‖D‖ (norm_nonneg D) hn
  exact ⟨B, hBmem, hsup, hEsup⟩

/-- Normality in the order sense: every positive increasing directed supremum is preserved. -/
theorem general_expectation_normal_order (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsLUB (Set.range A) B) :
    B ∈ theFactorObject P ∧ IsLUB (Set.range (fun i => I.E (A i))) (I.E B) := by
  obtain ⟨D, hDmem, hDsup, hEDsup⟩ :=
    expectation_preserves_order_bounded_nets P I A hmem hpos hmono B
      (fun i => hB.1 (Set.mem_range_self i))
  have he : D = B := hDsup.unique hB
  subst D
  exact ⟨hDmem, hEDsup⟩

/-- The aperiodic expectation constructed in046 is normal in this full directed-order sense. -/
theorem aperiodic_expectation_normal_order (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsLUB (Set.range A) B) :
    B ∈ theFactorObject P ∧
      IsLUB (Set.range (fun i => aperiodicExpectation P (A i))) (aperiodicExpectation P B) := by
  exact general_expectation_normal_order P (aperiodicExpectationInput P) A hmem hpos hmono B hB

#print axioms strong_net_limit_commutes
#print axioms factor_mem_of_net_strong_limit
#print axioms expectation_order_preserving
#print axioms factor_monotone_supremum_and_expectation
#print axioms expectation_preserves_order_bounded_nets
#print axioms general_expectation_normal_order
#print axioms aperiodic_expectation_normal_order

end

end ChatgptAudit.Expectation047
