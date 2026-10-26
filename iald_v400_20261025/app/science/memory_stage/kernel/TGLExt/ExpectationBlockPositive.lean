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
import TGLExt.GeneralExpectationPositive

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt Filter MeasureTheory
open ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- The quadratic form of a finite operator block on arbitrary Hilbert vectors. -/
def blockQuadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (v : Fin k → TowerHilbert P) : ℂ :=
  ∑ i, ∑ j, inner ℂ (v i) (A i j (v j))

/-- Full block positivity; this is not entrywise positivity. -/
def BlockPositive (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P)) : Prop :=
  (∀ i j, star (A i j) = A j i) ∧ ∀ v, 0 ≤ (blockQuadratic P k A v).re

theorem block_modular_quadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (t : ℝ) (v : Fin k → TowerHilbert P) :
    blockQuadratic P k (fun i j => modularConjugation P t (A i j)) v =
      blockQuadratic P k A (fun i => modularFlow P (-t) (v i)) := by
  simp only [blockQuadratic, modular_conjugation_inner]

/-- Finite sums and continuous real vector functionals commute with the actual averages. -/
theorem block_period_average_quadratic (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (T : ℝ) (hT : 0 < T) (v : Fin k → TowerHilbert P) :
    (blockQuadratic P k (fun i j => periodAverage P T hT (A i j)) v).re =
      T⁻¹ * (∫ t in (0 : ℝ)..T,
        (blockQuadratic P k A (fun i => modularFlow P (-t) (v i))).re) := by
  have hi (i j : Fin k) :
      IntervalIntegrable
        (fun t : ℝ => (inner ℂ (v i) (modularConjugation P t (A i j) (v j))).re)
        volume 0 T :=
    (Complex.continuous_re.comp
      (modular_conjugation_inner_continuous P (A i j) (v i) (v j))).intervalIntegrable 0 T
  have hsum (i : Fin k) :
      IntervalIntegrable
        (fun t : ℝ => ∑ j, (inner ℂ (v i)
          (modularConjugation P t (A i j) (v j))).re) volume 0 T := by
    apply Continuous.intervalIntegrable
    exact continuous_finsetSum Finset.univ (fun j _ =>
      Complex.continuous_re.comp
        (modular_conjugation_inner_continuous P (A i j) (v i) (v j)))
  simp_rw [← block_modular_quadratic P k A, blockQuadratic, Complex.re_sum,
    period_average_re_inner]
  rw [intervalIntegral.integral_finsetSum (fun i _ => hsum i)]
  simp_rw [intervalIntegral.integral_finsetSum (fun j _ => hi _ j),
    Finset.mul_sum]

theorem block_period_average_nonnegative (P : SiteProfile) (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hA : BlockPositive P k A) (T : ℝ) (hT : 0 < T)
    (v : Fin k → TowerHilbert P) :
    0 ≤ (blockQuadratic P k (fun i j => periodAverage P T hT (A i j)) v).re := by
  rw [block_period_average_quadratic P k A T hT v]
  exact mul_nonneg (inv_nonneg.mpr hT.le)
    (intervalIntegral.integral_nonneg_of_forall hT.le (fun t => hA.2 _))

/-- The block form converges because every entry converges strongly and the sums are finite. -/
theorem block_average_quadratic_tendsto (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hmem : ∀ i j, A i j ∈ theFactorObject P) (v : Fin k → TowerHilbert P) :
    Tendsto
      (fun n : ℕ => (blockQuadratic P k
        (fun i j => periodAverage P ((n : ℝ) + 1) (by positivity) (A i j)) v).re)
      atTop (𝓝 (blockQuadratic P k (fun i j => I.E (A i j)) v).re) := by
  have he (i j : Fin k) : I.E (A i j) = aperiodicExpectation P (A i j) :=
    the_expectation_is_unique I (aperiodicExpectationInput P) (A i j) (hmem i j)
  have hentry (i j : Fin k) :
      Tendsto (fun n : ℕ =>
        inner ℂ (v i) (periodAverage P ((n : ℝ) + 1) (by positivity) (A i j) (v j)))
        atTop (𝓝 (inner ℂ (v i) (I.E (A i j) (v j)))) := by
    rw [he i j]
    exact (tendsto_const_nhds (x := v i)).inner (𝕜 := ℂ)
      ((aperiodic_expectation_spec P (A i j) (hmem i j)).2.2 (v j))
  have hs := tendsto_finsetSum Finset.univ
    (fun i _ => tendsto_finsetSum Finset.univ (fun j _ => hentry i j))
  exact (Complex.continuous_re.tendsto _).comp hs

/-- Every finite amplification preserves the full Hilbert block form. -/
theorem general_expectation_block_positive (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (A : Matrix (Fin k) (Fin k) (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hmem : ∀ i j, A i j ∈ theFactorObject P) (hA : BlockPositive P k A) :
    BlockPositive P k (fun i j => I.E (A i j)) := by
  constructor
  · intro i j
    rw [← expectation_star P I (A i j) (hmem i j), hA.1 i j]
  · intro v
    exact le_of_tendsto_of_tendsto tendsto_const_nhds
      (block_average_quadratic_tendsto P I k A hmem v)
      (Filter.Eventually.of_forall fun n =>
        block_period_average_nonnegative P k A hA ((n : ℝ) + 1) (by positivity) v)

/-- Gram blocks are nonvacuous examples of the full condition. -/
theorem gram_block_quadratic (P : SiteProfile) (k : ℕ)
    (B : Fin k → TowerHilbert P →L[ℂ] TowerHilbert P)
    (v : Fin k → TowerHilbert P) :
    blockQuadratic P k (fun i j => star (B i) * B j) v =
      inner ℂ (∑ i, B i (v i)) (∑ j, B j (v j)) := by
  simp only [blockQuadratic, mul_apply_eq_comp,
    ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right,
    sum_inner, inner_sum]
  exact Finset.sum_comm

theorem gram_block_positive (P : SiteProfile) (k : ℕ)
    (B : Fin k → TowerHilbert P →L[ℂ] TowerHilbert P) :
    BlockPositive P k (fun i j => star (B i) * B j) := by
  constructor
  · intro i j
    simp only [star_mul, star_star]
  · intro v
    rw [gram_block_quadratic]
    exact inner_self_nonneg (𝕜 := ℂ) (x := ∑ i, B i (v i))

#print axioms blockQuadratic
#print axioms BlockPositive
#print axioms block_modular_quadratic
#print axioms block_period_average_quadratic
#print axioms block_period_average_nonnegative
#print axioms block_average_quadratic_tendsto
#print axioms general_expectation_block_positive
#print axioms gram_block_quadratic
#print axioms gram_block_positive

end

end ChatgptAudit.Expectation047
