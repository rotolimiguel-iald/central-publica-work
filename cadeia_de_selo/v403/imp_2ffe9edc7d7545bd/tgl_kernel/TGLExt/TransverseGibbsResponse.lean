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
import TGLExt.RelativeEntropyFisherLimit
import TGLExt.PauliProbabilityModel
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.ContDiff.Deriv

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.TransverseGibbs
open TGLExt ChatgptAudit ChatgptAudit.Micro021 ChatgptAudit.Observable035 Filter
open scoped Topology ContDiff
noncomputable section

def susceptibility (k : ℝ) : ℝ :=
  if k = 0 then 1 else Real.tanh |k| / |k|

def transverseRadius (k s : ℝ) : ℝ := Real.sqrt (k^2+s^2)

def radialFactor (k s : ℝ) : ℝ :=
  Real.tanh (transverseRadius k s) / transverseRadius k s

def transverseMagnetization (k s : ℝ) : ℝ :=
  if k = 0 then Real.tanh s else s * radialFactor k s

def transverseWeights (k s : ℝ) (i : Fin 2) : ℝ :=
  (1 + signOutcome i * transverseMagnetization k s) / 2

theorem tanh_smooth : ContDiff ℝ ∞ Real.tanh := by
  have he : Real.tanh = fun x : ℝ => Real.sinh x / Real.cosh x :=
    funext (fun x => Real.tanh_eq_sinh_div_cosh x)
  rw [he]
  exact Real.contDiff_sinh.div Real.contDiff_cosh (fun x => ne_of_gt (Real.cosh_pos x))

theorem tanh_derivative (s : ℝ) :
    HasDerivAt Real.tanh (1 / Real.cosh s ^ 2) s := by
  have h := (Real.hasDerivAt_sinh s).div (Real.hasDerivAt_cosh s)
    (ne_of_gt (Real.cosh_pos s))
  convert! h using 1
  · ext x
    exact Real.tanh_eq_sinh_div_cosh x
  · have he := Real.cosh_sq_sub_sinh_sq s
    field_simp
    nlinarith

theorem radius_positive {k : ℝ} (hk : k ≠ 0) (s : ℝ) :
    0 < transverseRadius k s := by
  apply Real.sqrt_pos.2
  have h := sq_pos_of_ne_zero hk
  nlinarith [sq_nonneg s]

theorem radius_zero (k : ℝ) : transverseRadius k 0 = |k| := by
  simp [transverseRadius, Real.sqrt_sq_eq_abs]

theorem radius_smooth {k : ℝ} (hk : k ≠ 0) :
    ContDiff ℝ ∞ (transverseRadius k) := by
  unfold transverseRadius
  apply (contDiff_const.add (contDiff_id.pow 2)).sqrt
  intro s
  have h := sq_pos_of_ne_zero hk
  nlinarith [sq_nonneg s]

theorem radial_factor_smooth {k : ℝ} (hk : k ≠ 0) :
    ContDiff ℝ ∞ (radialFactor k) :=
  (tanh_smooth.comp (radius_smooth hk)).div (radius_smooth hk)
    (fun s => ne_of_gt (radius_positive hk s))

theorem radius_first_jet {k : ℝ} (hk : k ≠ 0) :
    HasDerivAt (transverseRadius k) 0 0 := by
  have h := (((hasDerivAt_id (0 : ℝ)).pow 2).const_add (k^2)).sqrt
    (show k^2+(0 : ℝ)^2 ≠ 0 by simpa using pow_ne_zero 2 hk)
  convert! h using 1
  simp

theorem radial_factor_first_jet {k : ℝ} (hk : k ≠ 0) :
    HasDerivAt (radialFactor k) 0 0 := by
  have hr := radius_first_jet hk
  have ht := (tanh_derivative (transverseRadius k 0)).comp 0 hr
  convert! ht.div hr (ne_of_gt (radius_positive hk 0)) using 1
  simp

theorem magnetization_smooth (k : ℝ) :
    ContDiff ℝ ∞ (transverseMagnetization k) := by
  change ContDiff ℝ ∞ (fun s => if k = 0 then Real.tanh s else s * radialFactor k s)
  by_cases hk : k = 0
  · simpa [transverseMagnetization, hk] using tanh_smooth
  · simpa [transverseMagnetization, hk] using contDiff_id.mul (radial_factor_smooth hk)

theorem magnetization_zero (k : ℝ) : transverseMagnetization k 0 = 0 := by
  simp [transverseMagnetization]

theorem magnetization_first_jet (k : ℝ) :
    HasDerivAt (transverseMagnetization k) (susceptibility k) 0 := by
  change HasDerivAt (fun s => if k = 0 then Real.tanh s else s * radialFactor k s)
    (susceptibility k) 0
  by_cases hk : k = 0
  · simpa [transverseMagnetization, susceptibility, hk] using tanh_derivative 0
  · have h := (hasDerivAt_id (0 : ℝ)).mul (radial_factor_first_jet hk)
    simp only [hk, if_false]
    convert! h using 1
    simp [susceptibility, hk, radialFactor, radius_zero]

theorem linear_factor_second_jet (f : ℝ → ℝ) (hf : ContDiff ℝ ∞ f)
    (hz : HasDerivAt f 0 0) :
    HasDerivAt (deriv (fun s => s*f s)) 0 0 := by
  have hd : Differentiable ℝ f := hf.differentiable (by simp)
  have hdd : Differentiable ℝ (deriv f) :=
    (hf.of_le (show (2 : ℕ∞ω) ≤ ∞ by decide)).differentiable_deriv_two
  have he : deriv (fun s => s*f s) = fun s => f s+s*deriv f s := by
    funext s
    have h := (hasDerivAt_id s).mul (hd s).hasDerivAt
    convert! h.deriv using 1
    simp
  rw [he]
  have h := hz.add ((hasDerivAt_id (0 : ℝ)).mul (hdd 0).hasDerivAt)
  convert! h using 1
  simp [hz.deriv]

theorem tanh_second_jet : HasDerivAt (deriv Real.tanh) 0 0 := by
  have he : deriv Real.tanh = fun s => 1 / Real.cosh s ^ 2 :=
    funext (fun s => (tanh_derivative s).deriv)
  rw [he]
  have h := (hasDerivAt_const (0 : ℝ) (1 : ℝ)).div
    ((Real.hasDerivAt_cosh 0).pow 2) (by norm_num)
  convert! h using 1
  simp

theorem magnetization_second_jet (k : ℝ) :
    HasDerivAt (deriv (transverseMagnetization k)) 0 0 := by
  change HasDerivAt (deriv (fun s => if k = 0 then Real.tanh s else s * radialFactor k s)) 0 0
  by_cases hk : k = 0
  · simpa [transverseMagnetization, hk] using tanh_second_jet
  · simpa [transverseMagnetization, hk] using
      linear_factor_second_jet (radialFactor k) (radial_factor_smooth hk)
        (radial_factor_first_jet hk)

theorem magnetization_strict_bound (k s : ℝ) :
    |transverseMagnetization k s| < 1 := by
  by_cases hk : k = 0
  · simpa [transverseMagnetization, hk] using Real.abs_tanh_lt_one s
  · have hr := radius_positive hk s
    have hs : |s| ≤ transverseRadius k s := by
      have he : transverseRadius k s ^ 2 = k^2+s^2 := by
        exact Real.sq_sqrt (add_nonneg (sq_nonneg k) (sq_nonneg s))
      nlinarith [sq_abs s, abs_nonneg s, sq_nonneg k]
    simp only [transverseMagnetization, hk, if_false, radialFactor,
      abs_mul, abs_div, abs_of_pos hr]
    calc
      |s| * (|Real.tanh (transverseRadius k s)| / transverseRadius k s) =
          (|s| / transverseRadius k s) * |Real.tanh (transverseRadius k s)| := by ring
      _ ≤ 1 * |Real.tanh (transverseRadius k s)| :=
        mul_le_mul_of_nonneg_right ((div_le_one hr).2 hs) (abs_nonneg _)
      _ < 1 := by simpa using Real.abs_tanh_lt_one (transverseRadius k s)

theorem weights_smooth (k : ℝ) (i : Fin 2) :
    ContDiff ℝ ∞ (fun s => transverseWeights k s i) :=
  (contDiff_const.add (contDiff_const.mul (magnetization_smooth k))).div_const 2

theorem weights_normalized (k s : ℝ) : ∑ i, transverseWeights k s i = 1 := by
  simp [Fin.sum_univ_two, transverseWeights, signOutcome]
  ring

theorem weights_interior (k s : ℝ) (i : Fin 2) :
    0 < transverseWeights k s i ∧ transverseWeights k s i < 1 := by
  have h := abs_lt.mp (magnetization_strict_bound k s)
  fin_cases i <;> norm_num [transverseWeights, signOutcome] <;> constructor <;> linarith

theorem weights_zero (k : ℝ) (i : Fin 2) :
    transverseWeights k 0 i = 1/2 := by
  simp [transverseWeights, magnetization_zero]

theorem weights_first_jet (k : ℝ) (i : Fin 2) :
    HasDerivAt (fun s => transverseWeights k s i)
      (signOutcome i * susceptibility k / 2) 0 := by
  simpa [transverseWeights] using
    (((magnetization_first_jet k).const_mul (signOutcome i)).const_add 1).div_const 2

def responseWeights (k velocity t : ℝ) : Fin 2 → ℝ :=
  transverseWeights k (velocity*t)

theorem response_weights_smooth (k velocity : ℝ) (i : Fin 2) :
    ContDiff ℝ ∞ (fun t => responseWeights k velocity t i) :=
  (weights_smooth k i).comp (contDiff_const.mul contDiff_id)

def responseCurve (k velocity : ℝ) : DiagonalStateCurve (fun _ : Fin 2 => (1/2 : ℝ)) where
  weights := responseWeights k velocity
  tangent := fun t i => deriv (fun s => responseWeights k velocity s i) t
  at_zero := by intro i; simpa [responseWeights] using weights_zero k i
  trace_one := fun t => weights_normalized k (velocity*t)
  derivative_zero := fun i =>
    ((response_weights_smooth k velocity i).differentiable (by simp) 0).hasDerivAt
  derivative_past := Filter.Eventually.of_forall (fun t i =>
    ((response_weights_smooth k velocity i).differentiable (by simp) t).hasDerivAt)
  tangent_continuous := fun i =>
    ((response_weights_smooth k velocity i).continuous_deriv (by simp)).continuousAt

theorem response_first_jet (k velocity : ℝ) (i : Fin 2) :
    HasDerivAt (fun t => responseWeights k velocity t i)
      (velocity * signOutcome i * susceptibility k / 2) 0 := by
  have ho : HasDerivAt (fun s => transverseWeights k s i)
      (signOutcome i * susceptibility k / 2) (velocity * (0 : ℝ)) := by
    simpa using weights_first_jet k i
  have h := ho.comp 0 ((hasDerivAt_id (0 : ℝ)).const_mul velocity)
  convert! h using 1
  ring

theorem response_tangent_zero (k velocity : ℝ) (i : Fin 2) :
    (responseCurve k velocity).tangent 0 i =
      velocity * signOutcome i * susceptibility k / 2 :=
  (response_first_jet k velocity i).deriv

theorem response_fisher (k velocity : ℝ) :
    diagonalFisher (fun _ : Fin 2 => (1/2 : ℝ))
      ((responseCurve k velocity).tangent 0) = (susceptibility k * velocity)^2 := by
  simp [diagonalFisher, Fin.sum_univ_two, response_tangent_zero, signOutcome]
  ring

theorem response_relative_entropy_limit (k velocity : ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (responseWeights k velocity t)
      (fun _ : Fin 2 => (1/2 : ℝ)) / t^2) (𝓝[<] 0)
      (𝓝 ((susceptibility k * velocity)^2 / 2)) := by
  have h := relative_entropy_curve_quadratic_limit (responseCurve k velocity)
    (by intro i; norm_num)
  rw [response_fisher] at h
  exact h

theorem uniform_modular_increment_zero (k velocity t : ℝ) :
    modularIncrement (fun _ : Fin 2 => (1/2 : ℝ)) (responseWeights k velocity t) = 0 := by
  simp [modularIncrement, Fin.sum_univ_two, responseWeights, transverseWeights, signOutcome]
  ring

theorem entropy_response_identity (k velocity t : ℝ) :
    finiteEntropy (responseWeights k velocity t) -
      finiteEntropy (fun _ : Fin 2 => (1/2 : ℝ)) =
      -diagonalRelativeEntropy (responseWeights k velocity t)
        (fun _ : Fin 2 => (1/2 : ℝ)) := by
  rw [relative_entropy_identity, uniform_modular_increment_zero]
  ring

theorem response_entropy_quadratic_limit (k velocity : ℝ) :
    Tendsto (fun t => (finiteEntropy (responseWeights k velocity t) -
      finiteEntropy (fun _ : Fin 2 => (1/2 : ℝ))) / t^2) (𝓝[<] 0)
      (𝓝 (-((susceptibility k * velocity)^2 / 2))) := by
  simpa only [entropy_response_identity, neg_div] using
    (response_relative_entropy_limit k velocity).neg

#print axioms susceptibility
#print axioms transverseRadius
#print axioms radialFactor
#print axioms transverseMagnetization
#print axioms transverseWeights
#print axioms tanh_smooth
#print axioms tanh_derivative
#print axioms radius_positive
#print axioms radius_zero
#print axioms radius_smooth
#print axioms radial_factor_smooth
#print axioms radius_first_jet
#print axioms radial_factor_first_jet
#print axioms magnetization_smooth
#print axioms magnetization_zero
#print axioms magnetization_first_jet
#print axioms linear_factor_second_jet
#print axioms tanh_second_jet
#print axioms magnetization_second_jet
#print axioms magnetization_strict_bound
#print axioms weights_smooth
#print axioms weights_normalized
#print axioms weights_interior
#print axioms weights_zero
#print axioms weights_first_jet
#print axioms responseWeights
#print axioms response_weights_smooth
#print axioms responseCurve
#print axioms response_first_jet
#print axioms response_tangent_zero
#print axioms response_fisher
#print axioms response_relative_entropy_limit
#print axioms uniform_modular_increment_zero
#print axioms entropy_response_identity
#print axioms response_entropy_quadratic_limit
end
end ChatgptAudit.TransverseGibbs
