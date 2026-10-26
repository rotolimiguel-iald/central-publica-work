-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 063..066 (09/09/2026, noite), transposta em 10/09/2026 (ENTREGA_067 = elo do lote)
-- Os 21 modulos restantes da bancada (elos 83 -> 93 -> 98 da cadeia de copias integradas; 77 ja na v338).
--   063 (6 modulos, 113 teoremas): RESPOSTA GIBBS ANTES DA FONTE — protocolo misto (W = X + Z, medicao Z, s = v^2 t^2):
--     igualdade das respostas de entropia e energia de referencia na ordem quadratica; a fonte calculada da resposta com
--     conservacao por closed/wave; o seletor transporta o registro; O LIMITE LOCAL DE INTERACOES EXTENSIVAS (Lean);
--     a lei fisica de area e a metrica seguem entradas. [DERIVED, escrito]: Araki/GNS, tempo global, KMS no fecho C*.
--   065 (10 modulos, 108 teoremas): estabilidade do prefixo do caracter, resolucao finita, controle de malha do
--     registro, cotas de erro da resposta finita, precisao finita de Gibbs misto, janela de amostragem; METRICA DE
--     FISHER-LORENTZ SELECIONADA, variacao da densidade de materia escalar, ponte Fisher-Gibbs, CONSERVACAO sigma.
--   066 (5 modulos, 67 teoremas): sigma DOS MESMOS P (phi_j = sqrt(P_j/(1 - P_s))), resposta de Gibbs ASSINADA (dois
--     sinais com probabilidades positivas), esperanca negativa renormalizada, cobertura, reconstrucao por DEZ LIMITES
--     (SignedGibbsFiniteRecord); T e entrada; nao se identifica o observavel com stress de QFT.
--   Estatuto: [REAL] o compilado; [INPUT] a lei de area, a metrica, T, a acao/particao; [DERIVED + KNOWN] Araki, GNS,
--   KMS C*; [OPEN] correspondencia geral de selecao/materia/protocolo/area, realizacao interagente, anomalias, UV.
--   As ENTREGAS 067..087 sao MATEMATICA ESCRITA REVISADA (CAS, sem Lean) — registradas no diario e no Atlas como
--   [DERIVED], nao como flags; a propria bancada: "nao promover demonstracoes escritas a flags de compilacao".
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (98 -> 93 -> 83 -> 77...),
--   77 ja no kernel pulados; 21/21 hashes lidos dos bytes; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   21/21 contra o kernel v338, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TransverseGibbsResponse
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Analysis.Calculus.Deriv.Slope

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.MixedQuadraticGibbs
open TGLExt ChatgptAudit ChatgptAudit.Micro021 ChatgptAudit.Observable035
  ChatgptAudit.TransverseGibbs Filter Set
open scoped Topology ContDiff
noncomputable section

def mixedRadius (k s : ℝ) : ℝ := Real.sqrt ((k+s)^2+s^2)

def mixedZ (k s : ℝ) : ℝ :=
  (k+s) * (Real.tanh (mixedRadius k s) / mixedRadius k s)

def mixedWeights (k s : ℝ) (i : Fin 2) : ℝ :=
  (1 + signOutcome i * mixedZ k s) / 2

def mixedBase (k : ℝ) (i : Fin 2) : ℝ :=
  (1 + signOutcome i * Real.tanh k) / 2

theorem mixed_radius_positive {k : ℝ} (hk : 0 < k) (s : ℝ) :
    0 < mixedRadius k s := by
  apply Real.sqrt_pos.2
  have h1 := sq_nonneg (k+s)
  have h2 := sq_nonneg s
  nlinarith [sq_pos_of_pos hk]

theorem mixed_radius_zero {k : ℝ} (hk : 0 < k) : mixedRadius k 0 = k := by
  simp [mixedRadius, Real.sqrt_sq_eq_abs, abs_of_pos hk]

theorem mixed_radius_smooth {k : ℝ} (hk : 0 < k) :
    ContDiff ℝ ∞ (mixedRadius k) := by
  unfold mixedRadius
  apply (((contDiff_const.add contDiff_id).pow 2).add (contDiff_id.pow 2)).sqrt
  intro s
  have h := mixed_radius_positive hk s
  exact ne_of_gt (Real.sqrt_pos.mp h)

theorem mixed_radius_first_jet {k : ℝ} (hk : 0 < k) :
    HasDerivAt (mixedRadius k) 1 0 := by
  have h := (((((hasDerivAt_id (0 : ℝ)).const_add k).pow 2).add
    ((hasDerivAt_id (0 : ℝ)).pow 2)).sqrt
      (show (k+(0 : ℝ))^2+0^2 ≠ 0 by simpa using pow_ne_zero 2 (ne_of_gt hk)))
  convert! h using 1
  simp [Real.sqrt_sq_eq_abs, abs_of_pos hk, ne_of_gt hk]

theorem mixed_z_smooth {k : ℝ} (hk : 0 < k) :
    ContDiff ℝ ∞ (mixedZ k) :=
  (contDiff_const.add contDiff_id).mul
    ((tanh_smooth.comp (mixed_radius_smooth hk)).div (mixed_radius_smooth hk)
      (fun s => ne_of_gt (mixed_radius_positive hk s)))

theorem mixed_z_zero {k : ℝ} (hk : 0 < k) : mixedZ k 0 = Real.tanh k := by
  simp only [mixedZ, add_zero, mixed_radius_zero hk]
  field_simp

theorem mixed_z_first_jet {k : ℝ} (hk : 0 < k) :
    HasDerivAt (mixedZ k) (1 / Real.cosh k ^ 2) 0 := by
  have hr : HasDerivAt (mixedRadius k) 1 0 := mixed_radius_first_jet hk
  have ho : HasDerivAt Real.tanh (1 / Real.cosh k ^ 2) (mixedRadius k 0) := by
    rw [mixed_radius_zero hk]
    exact tanh_derivative k
  have ht := ho.comp 0 hr
  have hf := ht.div hr (ne_of_gt (mixed_radius_positive hk 0))
  have h := ((hasDerivAt_id (0 : ℝ)).const_add k).mul hf
  convert! h using 1
  dsimp only [Function.comp_def, Pi.div_apply, id_eq]
  simp only [mixed_radius_zero hk, add_zero, one_mul]
  field_simp [ne_of_gt hk]
  ring

theorem mixed_z_strict_bound {k : ℝ} (hk : 0 < k) (s : ℝ) :
    |mixedZ k s| < 1 := by
  have hr := mixed_radius_positive hk s
  have hs : |k+s| ≤ mixedRadius k s := by
    have he : mixedRadius k s ^ 2 = (k+s)^2+s^2 :=
      Real.sq_sqrt (add_nonneg (sq_nonneg (k+s)) (sq_nonneg s))
    nlinarith [sq_abs (k+s), abs_nonneg (k+s), sq_nonneg s]
  simp only [mixedZ, abs_mul, abs_div, abs_of_pos hr]
  calc
    |k+s| * (|Real.tanh (mixedRadius k s)| / mixedRadius k s) =
        (|k+s| / mixedRadius k s) * |Real.tanh (mixedRadius k s)| := by ring
    _ ≤ 1 * |Real.tanh (mixedRadius k s)| :=
      mul_le_mul_of_nonneg_right ((div_le_one hr).2 hs) (abs_nonneg _)
    _ < 1 := by simpa using Real.abs_tanh_lt_one (mixedRadius k s)

theorem mixed_weights_smooth {k : ℝ} (hk : 0 < k) (i : Fin 2) :
    ContDiff ℝ ∞ (fun s => mixedWeights k s i) :=
  (contDiff_const.add (contDiff_const.mul (mixed_z_smooth hk))).div_const 2

theorem mixed_weights_normalized (k s : ℝ) : ∑ i, mixedWeights k s i = 1 := by
  simp [mixedWeights, Fin.sum_univ_two, signOutcome]
  ring

theorem mixed_weights_interior {k : ℝ} (hk : 0 < k) (s : ℝ) (i : Fin 2) :
    0 < mixedWeights k s i ∧ mixedWeights k s i < 1 := by
  have h := abs_lt.mp (mixed_z_strict_bound hk s)
  fin_cases i <;> norm_num [mixedWeights, signOutcome] <;> constructor <;> linarith

theorem mixed_base_interior (k : ℝ) (i : Fin 2) :
    0 < mixedBase k i ∧ mixedBase k i < 1 := by
  have h := abs_lt.mp (Real.abs_tanh_lt_one k)
  fin_cases i <;> norm_num [mixedBase, signOutcome] <;> constructor <;> linarith

theorem mixed_weights_zero {k : ℝ} (hk : 0 < k) (i : Fin 2) :
    mixedWeights k 0 i = mixedBase k i := by
  rw [mixedWeights, mixed_z_zero hk]
  rfl

theorem mixed_weights_first_jet {k : ℝ} (hk : 0 < k) (i : Fin 2) :
    HasDerivAt (fun s => mixedWeights k s i)
      (signOutcome i / (2 * Real.cosh k ^ 2)) 0 := by
  have h := (((mixed_z_first_jet hk).const_mul (signOutcome i)).const_add 1).div_const 2
  convert! h using 1
  ring

theorem mixed_base_exp_formula (k : ℝ) :
    mixedBase k 0 = Real.exp k / (Real.exp k + Real.exp (-k)) ∧
    mixedBase k 1 = Real.exp (-k) / (Real.exp k + Real.exp (-k)) := by
  have hn : Real.exp k + Real.exp (-k) ≠ 0 :=
    ne_of_gt (add_pos (Real.exp_pos k) (Real.exp_pos (-k)))
  constructor <;> norm_num [mixedBase, signOutcome, Real.tanh_eq] <;>
    field_simp <;> ring

theorem mixed_base_log_ratio (k : ℝ) :
    Real.log (mixedBase k 1) - Real.log (mixedBase k 0) = -2*k := by
  rw [(mixed_base_exp_formula k).1, (mixed_base_exp_formula k).2]
  rw [Real.log_div (Real.exp_ne_zero _) (ne_of_gt (add_pos (Real.exp_pos _) (Real.exp_pos _))),
    Real.log_div (Real.exp_ne_zero _) (ne_of_gt (add_pos (Real.exp_pos _) (Real.exp_pos _)))]
  simp only [Real.log_exp]
  ring

theorem mixed_entropy_binary (k s : ℝ) :
    finiteEntropy (mixedWeights k s) = Real.binEntropy (mixedWeights k s 0) := by
  have he : mixedWeights k s = siteW (mixedWeights k s 0) := by
    funext i
    fin_cases i <;> norm_num [mixedWeights, siteW, signOutcome]
    ring
  rw [he, site_entropy_binary]
  rfl

theorem mixed_entropy_first_jet {k : ℝ} (hk : 0 < k) :
    HasDerivAt (fun s => finiteEntropy (mixedWeights k s))
      (-k / Real.cosh k ^ 2) 0 := by
  have hq := mixed_weights_first_jet hk 0
  have hp := mixed_weights_interior hk 0 0
  have h := (Real.hasDerivAt_binEntropy (ne_of_gt hp.1) (ne_of_lt hp.2)).comp (0 : ℝ) hq
  convert! h using 1
  · ext s
    exact mixed_entropy_binary k s
  · have hbase : 1 - mixedBase k 0 = mixedBase k 1 := by
      norm_num [mixedBase, signOutcome]
      ring
    rw [mixed_weights_zero hk, hbase, mixed_base_log_ratio]
    norm_num [signOutcome]
    ring

theorem derivative_quadratic_clock_limit (f : ℝ → ℝ) (a velocity : ℝ)
    (hf : HasDerivAt f a 0) :
    Tendsto (fun t => (f (velocity^2*t^2)-f 0)/t^2) (𝓝[<] 0) (𝓝 (a*velocity^2)) := by
  by_cases hv : velocity = 0
  · simp [hv]
  · have hu : Tendsto (fun t : ℝ => velocity^2*t^2) (𝓝[<] 0) (𝓝[>] 0) := by
      apply tendsto_nhdsWithin_iff.mpr
      constructor
      · simpa using (((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).const_mul
          (velocity^2)).tendsto.mono_left nhdsWithin_le_nhds
      · filter_upwards [self_mem_nhdsWithin] with t ht
        exact mul_pos (sq_pos_of_ne_zero hv) (sq_pos_of_ne_zero (ne_of_lt ht))
    have h := (hf.tendsto_slope_zero_right.comp hu).mul_const (velocity^2)
    apply Filter.Tendsto.congr' ?_ h
    filter_upwards [self_mem_nhdsWithin] with t ht
    simp only [Function.comp_def, zero_add, smul_eq_mul]
    field_simp [pow_ne_zero 2 hv, pow_ne_zero 2 (show t ≠ 0 from ne_of_lt ht)]

def quadraticWeights (k velocity t : ℝ) : Fin 2 → ℝ :=
  mixedWeights k (velocity^2*t^2)

theorem quadratic_weights_smooth {k : ℝ} (hk : 0 < k) (velocity : ℝ) (i : Fin 2) :
    ContDiff ℝ ∞ (fun t => quadraticWeights k velocity t i) :=
  (mixed_weights_smooth hk i).comp (contDiff_const.mul (contDiff_id.pow 2))

theorem quadratic_weights_first_jet {k : ℝ} (hk : 0 < k) (velocity : ℝ) (i : Fin 2) :
    HasDerivAt (fun t => quadraticWeights k velocity t i) 0 0 := by
  have ho : HasDerivAt (fun s => mixedWeights k s i)
      (signOutcome i / (2 * Real.cosh k ^ 2)) (velocity^2*(0 : ℝ)^2) := by
    simpa using mixed_weights_first_jet hk i
  have h := ho.comp 0 (((hasDerivAt_id (0 : ℝ)).pow 2).const_mul (velocity^2))
  convert! h using 1
  simp

def mixedCurve (k : ℝ) (hk : 0 < k) (velocity : ℝ) :
    DiagonalStateCurve (mixedBase k) where
  weights := quadraticWeights k velocity
  tangent := fun t i => deriv (fun s => quadraticWeights k velocity s i) t
  at_zero := by intro i; simpa [quadraticWeights] using mixed_weights_zero hk i
  trace_one := fun t => mixed_weights_normalized k (velocity^2*t^2)
  derivative_zero := fun i =>
    ((quadratic_weights_smooth hk velocity i).differentiable (by simp) 0).hasDerivAt
  derivative_past := Filter.Eventually.of_forall (fun t i =>
    ((quadratic_weights_smooth hk velocity i).differentiable (by simp) t).hasDerivAt)
  tangent_continuous := fun i =>
    ((quadratic_weights_smooth hk velocity i).continuous_deriv (by simp)).continuousAt

theorem quadratic_tangent_zero {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    (mixedCurve k hk velocity).tangent 0 = 0 := by
  funext i
  exact (quadratic_weights_first_jet hk velocity i).deriv

theorem quadratic_fisher_zero {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    diagonalFisher (mixedBase k) ((mixedCurve k hk velocity).tangent 0) = 0 := by
  simp [quadratic_tangent_zero, diagonalFisher]

theorem quadratic_relative_entropy_limit {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (quadraticWeights k velocity t) (mixedBase k) / t^2)
      (𝓝[<] 0) (𝓝 0) := by
  have h := relative_entropy_curve_quadratic_limit (mixedCurve k hk velocity)
    (fun i => (mixed_base_interior k i).1)
  rw [quadratic_fisher_zero, zero_div] at h
  exact h

theorem quadratic_entropy_limit {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    Tendsto (fun t => (finiteEntropy (quadraticWeights k velocity t) -
      finiteEntropy (mixedBase k)) / t^2) (𝓝[<] 0)
      (𝓝 (-k / Real.cosh k ^ 2 * velocity^2)) := by
  have h := derivative_quadratic_clock_limit
    (fun s => finiteEntropy (mixedWeights k s)) (-k / Real.cosh k ^ 2) velocity
    (mixed_entropy_first_jet hk)
  have hz : mixedWeights k 0 = mixedBase k := funext (mixed_weights_zero hk)
  simpa only [quadraticWeights, hz] using h

theorem quadratic_modular_increment_limit {k : ℝ} (hk : 0 < k) (velocity : ℝ) :
    Tendsto (fun t => modularIncrement (mixedBase k) (quadraticWeights k velocity t) / t^2)
      (𝓝[<] 0) (𝓝 (-k / Real.cosh k ^ 2 * velocity^2)) := by
  have h := (quadratic_relative_entropy_limit hk velocity).add (quadratic_entropy_limit hk velocity)
  simp only [zero_add] at h
  apply Filter.Tendsto.congr' (Filter.Eventually.of_forall (fun t => ?_)) h
  rw [relative_entropy_identity]
  ring

theorem mixed_response_coefficient_negative {k : ℝ} (hk : 0 < k) :
    -k / Real.cosh k ^ 2 < 0 :=
  div_neg_of_neg_of_pos (neg_lt_zero.mpr hk) (sq_pos_of_pos (Real.cosh_pos k))

#print axioms mixedRadius
#print axioms mixedZ
#print axioms mixedWeights
#print axioms mixedBase
#print axioms mixed_radius_positive
#print axioms mixed_radius_zero
#print axioms mixed_radius_smooth
#print axioms mixed_radius_first_jet
#print axioms mixed_z_smooth
#print axioms mixed_z_zero
#print axioms mixed_z_first_jet
#print axioms mixed_z_strict_bound
#print axioms mixed_weights_smooth
#print axioms mixed_weights_normalized
#print axioms mixed_weights_interior
#print axioms mixed_base_interior
#print axioms mixed_weights_zero
#print axioms mixed_weights_first_jet
#print axioms mixed_base_exp_formula
#print axioms mixed_base_log_ratio
#print axioms mixed_entropy_binary
#print axioms mixed_entropy_first_jet
#print axioms derivative_quadratic_clock_limit
#print axioms quadraticWeights
#print axioms quadratic_weights_smooth
#print axioms quadratic_weights_first_jet
#print axioms mixedCurve
#print axioms quadratic_tangent_zero
#print axioms quadratic_fisher_zero
#print axioms quadratic_relative_entropy_limit
#print axioms quadratic_entropy_limit
#print axioms quadratic_modular_increment_limit
#print axioms mixed_response_coefficient_negative
end
end ChatgptAudit.MixedQuadraticGibbs
