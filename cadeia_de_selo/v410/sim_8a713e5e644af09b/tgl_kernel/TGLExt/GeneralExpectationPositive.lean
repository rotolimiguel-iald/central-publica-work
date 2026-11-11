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
import TGLExt.ExpectationAlgebra
import Mathlib.Analysis.InnerProductSpace.Positive

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Expectation047

open TGLExt Filter MeasureTheory
open ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- Simultaneous modular transport of both test vectors is the actual conjugation form. -/
theorem modular_conjugation_inner (P : SiteProfile) (t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    inner ℂ v (modularConjugation P t A w) =
      inner ℂ (modularFlow P (-t) v) (A (modularFlow P (-t) w)) := by
  have h := (modularFlowIsometry P t).inner_map_map
    (modularFlow P (-t) v) (A (modularFlow P (-t) w))
  change inner ℂ (modularFlow P t (modularFlow P (-t) v))
      (modularFlow P t (A (modularFlow P (-t) w))) = _ at h
  rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time] at h
  exact h

theorem modular_conjugation_inner_continuous (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    Continuous (fun t : ℝ => inner ℂ v (modularConjugation P t A w)) :=
  continuous_const.inner (modular_orbit_continuous A w)

/-- The continuous vector functional commutes with the finite-time average. -/
theorem period_average_inner (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    inner ℂ v (periodAverage P T hT A w) =
      T⁻¹ • (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)) := by
  rw [(period_average_operator T hT A).1]
  change (innerSL ℂ v)
      (T⁻¹ • (∫ t in (0 : ℝ)..T, modularConjugation P t A w)) = _
  rw [(innerSL ℂ v).map_smul_of_tower,
    ← (innerSL ℂ v).intervalIntegral_comp_comm
      ((modular_orbit_continuous A w).intervalIntegrable 0 T)]
  rfl

theorem period_average_re_inner (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (v w : TowerHilbert P) :
    (inner ℂ v (periodAverage P T hT A w)).re =
      T⁻¹ * (∫ t in (0 : ℝ)..T, (inner ℂ v (modularConjugation P t A w)).re) := by
  have hi := Complex.reCLM.intervalIntegral_comp_comm (μ := volume)
    ((modular_conjugation_inner_continuous P A v w).intervalIntegrable 0 T)
  change (∫ t in (0 : ℝ)..T, (inner ℂ v (modularConjugation P t A w)).re) =
    (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)).re at hi
  rw [period_average_inner P T hT A v w]
  change Complex.reCLM
      (T⁻¹ • (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w))) = _
  rw [Complex.reCLM.map_smul]
  change T⁻¹ * (∫ t in (0 : ℝ)..T, inner ℂ v (modularConjugation P t A w)).re = _
  rw [← hi]

/-- Positive input gives a nonnegative real diagonal form for every interval length T>0. -/
theorem period_average_re_inner_nonneg (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A.IsPositive)
    (v : TowerHilbert P) :
    0 ≤ (inner ℂ v (periodAverage P T hT A v)).re := by
  rw [period_average_re_inner P T hT A v v]
  apply mul_nonneg (inv_nonneg.mpr hT.le)
  apply intervalIntegral.integral_nonneg_of_forall hT.le
  intro t
  rw [modular_conjugation_inner]
  exact hA.re_inner_nonneg_right _

/-- Nonnegativity passes through the strong limit; any contract agrees with the constructed one. -/
theorem expectation_re_inner_nonneg (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : A.IsPositive) (v : TowerHilbert P) :
    0 ≤ (inner ℂ v (I.E A v)).re := by
  have he : I.E A = aperiodicExpectation P A :=
    the_expectation_is_unique I (aperiodicExpectationInput P) A hmem
  rw [he]
  have hv := (aperiodic_expectation_spec P A hmem).2.2 v
  have hi := (tendsto_const_nhds (x := v)).inner (𝕜 := ℂ) hv
  have hr := (Complex.continuous_re.tendsto
    (inner ℂ v (aperiodicExpectation P A v))).comp hi
  change Tendsto
    (fun n : ℕ => (inner ℂ v
      (periodAverage P ((n : ℝ) + 1) (by positivity) A v)).re)
    atTop (𝓝 (inner ℂ v (aperiodicExpectation P A v)).re) at hr
  exact le_of_tendsto_of_tendsto tendsto_const_nhds hr
    (Filter.Eventually.of_forall fun n =>
      period_average_re_inner_nonneg P ((n : ℝ) + 1) (by positivity) A hA v)

/-- Positivity on the factor is proved from averages and adjoint preservation. -/
theorem general_expectation_isPositive (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : A.IsPositive) :
    (I.E A).IsPositive := by
  apply ContinuousLinearMap.isPositive_def'.mpr
  constructor
  · change star (I.E A) = I.E A
    rw [← expectation_star P I A hmem, hA.isSelfAdjoint.star_eq]
  · intro v
    change 0 ≤ RCLike.re (inner ℂ (I.E A v) v)
    rw [inner_re_symm]
    exact expectation_re_inner_nonneg P I A hmem hA v

/-- The order-theoretic form of positivity, restricted to the actual factor. -/
theorem general_expectation_nonnegative (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : A ∈ theFactorObject P) (hA : 0 ≤ A) :
    0 ≤ I.E A := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  exact general_expectation_isPositive P I A hmem
    ((ContinuousLinearMap.nonneg_iff_isPositive A).mp hA)

#print axioms modular_conjugation_inner
#print axioms modular_conjugation_inner_continuous
#print axioms period_average_inner
#print axioms period_average_re_inner
#print axioms period_average_re_inner_nonneg
#print axioms expectation_re_inner_nonneg
#print axioms general_expectation_isPositive
#print axioms general_expectation_nonnegative

end

end ChatgptAudit.Expectation047
