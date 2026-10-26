-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_056 ESPONTANEA (08/09/2026), transposta em 08/09/2026
-- Lote 055..056 (6 modulos; origem: ordem direta do operador a bancada para demonstrar no modelo completo).
--   055 — SELETOR RELATIVO NA TORRE INFINITA: com a preparacao ja existente geometricAmplitude (b_n = 2^-n/24)
--     e os pesos da torre, a leitura de verossimilhanca do cociclo SEPARA todas as configuracoes infinitas
--     quando t != 0 (contraste a(x) = log(1+3x/2) - log(1-3x) com 2a(x/2) < a(x): cada a_n domina toda a cauda;
--     codigo binario injetivo); a leitura coincide com os logaritmos dos pesos efetivos e com o gerador de
--     verossimilhanca do kernel (existing_global_generator_bound / density_normalized / cocycle_limit);
--     a densidade existente e o estado preparado. [DERIVED, analitico, NAO Lean]: A = C*(P_n), D = W*(P_n)
--     recuperados pelo cociclo; [DERIVED + KNOWN]: esperanca D no fator inteiro (Takesaki). D e comutativa,
--     M e o ambiente: W*(u) = D nao e W*(u) = M. Vale para geometricAmplitude e t != 0, nao para todo perfil.
--   056 — METRICAS DA TORRE E LIMITES DA RECONSTRUCAO: d_t(x,y) = |g_t(x) - g_t(y)| e metrica (t != 0) e a
--     escala e livre; Fisher radial F(r) = sum b_n^2/[q_n(1-q_n)] com 1/96 <= F <= 4/357 e F(0) = 1/96 (soma e
--     cotas Lean; identificacao probabilistica global analitica); entropia relativa/t^4 -> F(0)/2 = 1/192;
--     NEGATIVOS: a familia de um parametro tem Gram 2x2 de determinante ZERO (nao gera area por renomear
--     coordenadas); o gerador relativo como Dirac tem distancia de comutadores INFINITA entre configuracoes
--     distintas (comutador zero com as coordenadas); o gauge relativo exp(isP_n) preserva ambos os estados e o
--     cociclo (liberdade residual), e seu gerador NAO e central ([P_0, E_01] = E_01 != 0).
--   Estatuto: [REAL] o compilado; [DERIVED] reconstrucao da algebra diagonal, interpretacao global de Fisher,
--   4||xi_r||^2 = F(r), arcsin, distancia de Connes; [OPEN] geometria fisica 3+1, area-entropia geometrica,
--   calor fisico, acao gravitacional, Einstein-Cartan sem hipoteses. Nenhum nome ligado a H3/area/gate.
-- Auditoria da gerencia (sessao d554e796, 08/09/2026): hashes 10/10 + 13/13; 2/2 auditores da bancada exit 0;
--   sem revisao cientifica independente na bancada (declarado) — a gerencia leu os enunciados;
--   recompilacao INDEPENDENTE 6/6, axiomas no trio; guarda de colisao; fontes lidas das SUBPASTAS da entrega.
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SpectralMetricGeometry
import TGLExt.DiagonalRelativeEntropy
import TGLExt.SummableRelativeQuartic
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.Geometry056
open Filter Topology Set TGLExt ChatgptAudit.CocycleRealization
  ChatgptAudit.Response028 ChatgptAudit.Micro021
noncomputable section

def radialWeight (r : ℝ) (n : ℕ) : ℝ :=
  1/3-geometricAmplitude.value n*r

def radialFisherTerm (r : ℝ) (n : ℕ) : ℝ :=
  (geometricAmplitude.value n)^2/(radialWeight r n*(1-radialWeight r n))

def radialFisher (r : ℝ) : ℝ := ∑' n, radialFisherTerm r n

def regularSpeed (t : ℝ) : ℝ := 2*t/(1+t^2)^2

def timeFisher (t : ℝ) : ℝ :=
  (regularSpeed t)^2*radialFisher (regularParameter t)

theorem radial_weight_is_existing (t : ℝ) (n : ℕ) :
    radialWeight (regularParameter t) n=(amplitudeProfile geometricAmplitude t).w n := rfl

theorem geometric_amplitude_sharp_bound (n : ℕ) :
    geometricAmplitude.value n ≤ 1/24 := by
  have hp : (1/2:ℝ)^n ≤ 1 := pow_le_one₀ (by norm_num) (by norm_num)
  change (1/24:ℝ)*(1/2)^n ≤ 1/24
  linarith

theorem radial_weight_bounds {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) (n : ℕ) :
    7/24 ≤ radialWeight r n ∧ radialWeight r n ≤ 1/3 := by
  have h0 := geometricAmplitude.nonnegative n
  have h1 := geometric_amplitude_sharp_bound n
  have hm := mul_le_mul_of_nonneg_left hb h0
  have hn := mul_nonneg h0 hr
  dsimp [radialWeight]
  constructor <;> nlinarith

theorem radial_variance_bounds {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) (n : ℕ) :
    119/576  ≤  radialWeight r n*(1-radialWeight r n) ∧
      radialWeight r n*(1-radialWeight r n) ≤ 2/9 := by
  obtain ⟨h0,h1⟩ := radial_weight_bounds hr hb n
  have hl := mul_nonneg (sub_nonneg.mpr h0)
    (show 0 ≤ 1-radialWeight r n-7/24 by linarith)
  have hu := mul_nonneg (sub_nonneg.mpr h1)
    (show 0 ≤ 1-1/3-radialWeight r n by linarith)
  constructor <;> nlinarith

theorem radial_fisher_term_bounds {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) (n : ℕ) :
    (9/2)*(geometricAmplitude.value n)^2  ≤  radialFisherTerm r n ∧
      radialFisherTerm r n ≤ (576/119)*(geometricAmplitude.value n)^2 := by
  obtain ⟨h0,h1⟩ := radial_variance_bounds hr hb n
  have hp : 0<radialWeight r n*(1-radialWeight r n) := by linarith
  have hsq := sq_nonneg (geometricAmplitude.value n)
  unfold radialFisherTerm
  constructor
  · apply (le_div_iff₀ hp).mpr
    have hh := mul_le_mul_of_nonneg_left h1 hsq
    nlinarith
  · apply (div_le_iff₀ hp).mpr
    have hh := mul_le_mul_of_nonneg_left h0 hsq
    nlinarith

theorem radial_fisher_term_nonnegative {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) (n : ℕ) :
    0 ≤ radialFisherTerm r n := by
  have h := (radial_fisher_term_bounds hr hb n).1
  have hn : 0 ≤ (9/2:ℝ)*(geometricAmplitude.value n)^2 := by positivity
  linarith

theorem radial_fisher_summable {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) :
    Summable (radialFisherTerm r) :=
  Summable.of_nonneg_of_le (radial_fisher_term_nonnegative hr hb)
    (fun n => (radial_fisher_term_bounds hr hb n).2)
    ((amplitude_square_summable geometricAmplitude).mul_left (576/119))

theorem radial_fisher_bounds {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) :
    1/96 ≤ radialFisher r ∧ radialFisher r ≤ 4/357 := by
  have hl := Summable.tsum_le_tsum (fun n => (radial_fisher_term_bounds hr hb n).1)
    ((amplitude_square_summable geometricAmplitude).mul_left (9/2))
    (radial_fisher_summable hr hb)
  have hu := Summable.tsum_le_tsum (fun n => (radial_fisher_term_bounds hr hb n).2)
    (radial_fisher_summable hr hb)
    ((amplitude_square_summable geometricAmplitude).mul_left (576/119))
  rw [tsum_mul_left] at hl hu
  change (9/2)*amplitudeSquareMass geometricAmplitude ≤ radialFisher r at hl
  change radialFisher r ≤ (576/119)*amplitudeSquareMass geometricAmplitude at hu
  rw [geometric_amplitude_square_mass] at hl hu
  constructor <;> linarith

theorem radial_fisher_positive {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) :
    0<radialFisher r := lt_of_lt_of_le (by norm_num) (radial_fisher_bounds hr hb).1

theorem radial_fisher_prefix_limit {r : ℝ} (hr : 0 ≤ r) (hb : r ≤ 1) :
    Tendsto (fun N => ∑ n∈Finset.range (N+1),radialFisherTerm r n)
      atTop (𝓝 (radialFisher r)) :=
  (radial_fisher_summable hr hb).hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)

theorem regular_parameter_derivative (t : ℝ) :
    HasDerivAt regularParameter (regularSpeed t) t := by
  have h := ((hasDerivAt_id t).pow 2).div
    ((hasDerivAt_const t (1:ℝ)).add ((hasDerivAt_id t).pow 2))
    (ne_of_gt (show 0<1+t^2 by positivity))
  convert! h using 1
  simp [regularSpeed]
  ring

theorem radial_weight_derivative (r : ℝ) (n : ℕ) :
    HasDerivAt (fun s => radialWeight s n) (-geometricAmplitude.value n) r := by
  convert! (hasDerivAt_const r (1/3:ℝ)).sub
    ((hasDerivAt_id r).const_mul (geometricAmplitude.value n)) using 1
  simp

theorem actual_weight_derivative (t : ℝ) (n : ℕ) :
    HasDerivAt (fun s => (amplitudeProfile geometricAmplitude s).w n)
      (-geometricAmplitude.value n*regularSpeed t) t :=
  (radial_weight_derivative (regularParameter t) n).comp t (regular_parameter_derivative t)

theorem regular_speed_ne_zero {t : ℝ} (ht : t≠0) : regularSpeed t≠0 := by
  unfold regularSpeed
  exact div_ne_zero (mul_ne_zero (by norm_num) ht) (ne_of_gt (by positivity))

theorem time_fisher_positive {t : ℝ} (ht : t≠0) : 0<timeFisher t :=
  mul_pos (sq_pos_of_ne_zero (regular_speed_ne_zero ht))
    (radial_fisher_positive (regular_parameter_nonnegative t) (regular_parameter_lt_one t).le)

theorem time_fisher_zero : timeFisher 0=0 := by
  simp [timeFisher,regularSpeed]

theorem bernoulli_score_mean_zero {q b : ℝ} (hq : 0<q) (h1 : q<1) :
    q*(-b/q)+(1-q)*(b/(1-q))=0 := by
  have hn : 1-q≠0 := ne_of_gt (sub_pos.mpr h1)
  field_simp
  ring

theorem bernoulli_score_variance {q b : ℝ} (hq : 0<q) (h1 : q<1) :
    q*(-b/q)^2+(1-q)*(b/(1-q))^2=b^2/(q*(1-q)) := by
  have hq0 : q≠0 := ne_of_gt hq
  have hn : 1-q≠0 := ne_of_gt (sub_pos.mpr h1)
  field_simp
  ring

theorem fisher_angular_coefficient {q a : ℝ} (hq : 0<q) (h1 : q<1) :
    (2*Real.sqrt (q*(1-q))*a)^2/(q*(1-q))=4*a^2 := by
  have hp : 0<q*(1-q) := mul_pos hq (sub_pos.mpr h1)
  rw [div_eq_iff (ne_of_gt hp)]
  nlinarith [Real.sq_sqrt hp.le]

def oneParameterGram (h u v : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![h*u^2,h*u*v;h*u*v,h*v^2]

theorem one_parameter_has_zero_two_area (h u v : ℝ) :
    Matrix.det (oneParameterGram h u v)=0 := by
  simp [oneParameterGram,Matrix.det_fin_two]
  ring


theorem radial_fisher_at_reference : radialFisher 0=1/96 := by
  have ht : ∀ n, radialFisherTerm 0 n=(9/2)*(geometricAmplitude.value n)^2 := by
    intro n
    dsimp [radialFisherTerm,radialWeight]
    ring
  unfold radialFisher
  simp_rw [ht]
  rw [tsum_mul_left]
  change (9/2)*amplitudeSquareMass geometricAmplitude=1/96
  rw [geometric_amplitude_square_mass]
  norm_num

theorem actual_relative_entropy_recovers_fisher :
    Tendsto (fun t : ℝ => amplitudeRelativeEntropy geometricAmplitude t/t^4)
      (𝓝[≠] 0) (𝓝 (radialFisher 0/2)) := by
  have h := ChatgptAudit.Quartic037.amplitude_relative_quartic_limit geometricAmplitude
  rw [geometric_amplitude_square_mass] at h
  rw [radial_fisher_at_reference]
  norm_num at h ⊢
  exact h

#print axioms radialWeight
#print axioms radialFisherTerm
#print axioms radialFisher
#print axioms regularSpeed
#print axioms timeFisher
#print axioms radial_weight_is_existing
#print axioms geometric_amplitude_sharp_bound
#print axioms radial_weight_bounds
#print axioms radial_variance_bounds
#print axioms radial_fisher_term_bounds
#print axioms radial_fisher_term_nonnegative
#print axioms radial_fisher_summable
#print axioms radial_fisher_bounds
#print axioms radial_fisher_positive
#print axioms radial_fisher_prefix_limit
#print axioms regular_parameter_derivative
#print axioms radial_weight_derivative
#print axioms actual_weight_derivative
#print axioms regular_speed_ne_zero
#print axioms time_fisher_positive
#print axioms time_fisher_zero
#print axioms bernoulli_score_mean_zero
#print axioms bernoulli_score_variance
#print axioms fisher_angular_coefficient
#print axioms oneParameterGram
#print axioms one_parameter_has_zero_two_area
#print axioms radial_fisher_at_reference
#print axioms actual_relative_entropy_recovers_fisher

end
end ChatgptAudit.Geometry056
