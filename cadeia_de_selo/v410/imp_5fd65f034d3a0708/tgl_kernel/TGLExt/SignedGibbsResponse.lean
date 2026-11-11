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
import TGLExt.MixedQuadraticGibbsResponse
import TGLExt.MixedGibbsGravitationalBridge

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.SignedGibbs
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.MixedQuadraticGibbs ChatgptAudit.Micro021
  ChatgptAudit.Observable035 ChatgptAudit.Coherent023
noncomputable section
open scoped ContDiff
variable {J : Type} [Fintype J]

/-- A signed control parameter changes the Gibbs preparation, not the sign of a probability. -/
def signedWeights (k amplitude velocity t : ℝ) : Fin 2 → ℝ :=
  mixedWeights k (amplitude*velocity^2*t^2)

theorem derivative_signed_clock_limit (f : ℝ → ℝ) (b amplitude velocity : ℝ)
    (hf : HasDerivAt f b 0) :
    Tendsto (fun t => (f (amplitude*velocity^2*t^2)-f 0)/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (b*amplitude*velocity^2)) := by
  have ho : HasDerivAt f b (amplitude*(0:ℝ)) := by simpa using hf
  have hcomp := ho.comp 0 ((hasDerivAt_id (0:ℝ)).const_mul amplitude)
  have hh : HasDerivAt (fun s => f (amplitude*s)) (b*amplitude) 0 := by
    convert! hcomp using 1
    simp
  simpa only [mul_assoc,mul_zero] using
    derivative_quadratic_clock_limit (fun s => f (amplitude*s)) (b*amplitude) velocity hh

theorem signed_weights_normalized (k amplitude velocity t : ℝ) :
    ∑ i, signedWeights k amplitude velocity t i=1 :=
  mixed_weights_normalized k _

theorem signed_weights_interior {k : ℝ} (hk : 0<k) (amplitude velocity t : ℝ) (i : Fin 2) :
    0<signedWeights k amplitude velocity t i ∧ signedWeights k amplitude velocity t i<1 :=
  mixed_weights_interior hk _ i

theorem signed_weights_at_zero {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    signedWeights k amplitude velocity 0=mixedBase k := by
  funext i
  simpa [signedWeights] using mixed_weights_zero hk i

theorem signed_weights_smooth {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) (i : Fin 2) :
    ContDiff ℝ ∞ (fun t => signedWeights k amplitude velocity t i) :=
  (mixed_weights_smooth hk i).comp (contDiff_const.mul (contDiff_id.pow 2))

theorem signed_weights_first_jet {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) (i : Fin 2) :
    HasDerivAt (fun t => signedWeights k amplitude velocity t i) 0 0 := by
  have ho : HasDerivAt (fun s => mixedWeights k s i)
      (signOutcome i/(2*Real.cosh k^2)) ((amplitude*velocity^2)*(0:ℝ)^2) := by
    simpa using mixed_weights_first_jet hk i
  have h := ho.comp 0 (((hasDerivAt_id (0:ℝ)).pow 2).const_mul (amplitude*velocity^2))
  convert! h using 1
  simp

def signedCurve (k : ℝ) (hk : 0<k) (amplitude velocity : ℝ) :
    DiagonalStateCurve (mixedBase k) where
  weights := signedWeights k amplitude velocity
  tangent := fun t i => deriv (fun s => signedWeights k amplitude velocity s i) t
  at_zero := fun i => congrFun (signed_weights_at_zero hk amplitude velocity) i
  trace_one := fun t => signed_weights_normalized k amplitude velocity t
  derivative_zero := fun i =>
    ((signed_weights_smooth hk amplitude velocity i).differentiable (by simp) 0).hasDerivAt
  derivative_past := Filter.Eventually.of_forall (fun t i =>
    ((signed_weights_smooth hk amplitude velocity i).differentiable (by simp) t).hasDerivAt)
  tangent_continuous := fun i =>
    ((signed_weights_smooth hk amplitude velocity i).continuous_deriv (by simp)).continuousAt

theorem signed_tangent_zero {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    (signedCurve k hk amplitude velocity).tangent 0=0 := by
  funext i
  exact (signed_weights_first_jet hk amplitude velocity i).deriv

theorem signed_fisher_zero {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    diagonalFisher (mixedBase k) ((signedCurve k hk amplitude velocity).tangent 0)=0 := by
  simp [signed_tangent_zero,diagonalFisher]

theorem signed_relative_entropy_limit {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (signedWeights k amplitude velocity t) (mixedBase k)/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 0) := by
  have h := relative_entropy_curve_quadratic_limit (signedCurve k hk amplitude velocity)
    (fun i => (mixed_base_interior k i).1)
  rw [signed_fisher_zero,zero_div] at h
  exact h

theorem signed_entropy_limit {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    Tendsto (fun t => (finiteEntropy (signedWeights k amplitude velocity t)-
      finiteEntropy (mixedBase k))/t^2) (𝓝[<] (0:ℝ))
      (𝓝 (-k/Real.cosh k^2*amplitude*velocity^2)) := by
  have h := derivative_signed_clock_limit (fun s => finiteEntropy (mixedWeights k s))
    (-k/Real.cosh k^2) amplitude velocity (mixed_entropy_first_jet hk)
  have hz : mixedWeights k 0=mixedBase k := funext (mixed_weights_zero hk)
  simpa only [signedWeights,hz] using h

theorem signed_modular_limit {k : ℝ} (hk : 0<k) (amplitude velocity : ℝ) :
    Tendsto (fun t => modularIncrement (mixedBase k) (signedWeights k amplitude velocity t)/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (-k/Real.cosh k^2*amplitude*velocity^2)) := by
  have h := (signed_relative_entropy_limit hk amplitude velocity).add
    (signed_entropy_limit hk amplitude velocity)
  simp only [zero_add] at h
  apply Filter.Tendsto.congr' (Filter.Eventually.of_forall (fun t => ?_)) h
  rw [relative_entropy_identity]
  ring

/-- This is a reconstructed response coefficient, not an assumption about a physical kinetic term. -/
def signedCoupling (k amplitude : ℝ) : ℝ := amplitude*k/(Real.pi*Real.cosh k^2)

theorem signed_response_coefficient (k amplitude velocity : ℝ) :
    -k/Real.cosh k^2*amplitude*velocity^2 = -Real.pi*signedCoupling k amplitude*velocity^2 := by
  unfold signedCoupling
  field_simp

theorem signed_coupling_negative {k amplitude : ℝ} (hk : 0<k) (ha : amplitude<0) :
    signedCoupling k amplitude<0 :=
  div_neg_of_neg_of_pos (mul_neg_of_neg_of_pos ha hk)
    (mul_pos Real.pi_pos (sq_pos_of_pos (Real.cosh_pos k)))

theorem signed_coupling_positive {k amplitude : ℝ} (hk : 0<k) (ha : 0<amplitude) :
    0<signedCoupling k amplitude :=
  div_pos (mul_pos ha hk) (mul_pos Real.pi_pos (sq_pos_of_pos (Real.cosh_pos k)))

theorem negative_clock_positive_entropy_response {k amplitude velocity : ℝ}
    (hk : 0<k) (ha : amplitude<0) (hv : velocity≠0) :
    0 < -k/Real.cosh k^2*amplitude*velocity^2 := by
  exact mul_pos (mul_pos_of_neg_of_neg (mixed_response_coefficient_negative hk) ha)
    (sq_pos_of_ne_zero hv)

def signedEntropyIncrement (k amplitude : J → ℝ) (w : J → Coordinate4)
    (d : Coordinate4) (t : ℝ) : ℝ :=
  ∑ j, (finiteEntropy (signedWeights (k j) (amplitude j) (covectorRead (w j) d) t)-
    finiteEntropy (mixedBase (k j)))

def signedModularIncrement (k amplitude : J → ℝ) (w : J → Coordinate4)
    (d : Coordinate4) (t : ℝ) : ℝ :=
  ∑ j, modularIncrement (mixedBase (k j))
    (signedWeights (k j) (amplitude j) (covectorRead (w j) d) t)

theorem finite_signed_entropy_limit (k amplitude : J → ℝ) (hk : ∀ j, 0<k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => signedEntropyIncrement k amplitude w d t/t^2)
      (𝓝[<] (0:ℝ))
      (𝓝 (∑ j, -Real.pi*signedCoupling (k j) (amplitude j)*(covectorRead (w j) d)^2)) := by
  have h := tendsto_finsetSum Finset.univ (fun j _ =>
    signed_entropy_limit (hk j) (amplitude j) (covectorRead (w j) d))
  simpa only [signedEntropyIncrement,Finset.sum_div,signed_response_coefficient] using h

theorem finite_signed_modular_limit (k amplitude : J → ℝ) (hk : ∀ j, 0<k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => signedModularIncrement k amplitude w d t/t^2)
      (𝓝[<] (0:ℝ))
      (𝓝 (∑ j, -Real.pi*signedCoupling (k j) (amplitude j)*(covectorRead (w j) d)^2)) := by
  have h := tendsto_finsetSum Finset.univ (fun j _ =>
    signed_modular_limit (hk j) (amplitude j) (covectorRead (w j) d))
  simpa only [signedModularIncrement,Finset.sum_div,signed_response_coefficient] using h

theorem signed_entropy_modular_difference (k amplitude : J → ℝ) (hk : ∀ j, 0<k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => (signedEntropyIncrement k amplitude w d t-
      signedModularIncrement k amplitude w d t)/t^2) (𝓝[<] (0:ℝ)) (𝓝 0) := by
  simpa only [sub_self,←sub_div] using
    (finite_signed_entropy_limit k amplitude hk w d).sub (finite_signed_modular_limit k amplitude hk w d)

#print axioms signedWeights
#print axioms derivative_signed_clock_limit
#print axioms signed_weights_normalized
#print axioms signed_weights_interior
#print axioms signed_weights_at_zero
#print axioms signed_weights_smooth
#print axioms signed_weights_first_jet
#print axioms signedCurve
#print axioms signed_tangent_zero
#print axioms signed_fisher_zero
#print axioms signed_relative_entropy_limit
#print axioms signed_entropy_limit
#print axioms signed_modular_limit
#print axioms signedCoupling
#print axioms signed_response_coefficient
#print axioms signed_coupling_negative
#print axioms signed_coupling_positive
#print axioms negative_clock_positive_entropy_response
#print axioms signedEntropyIncrement
#print axioms signedModularIncrement
#print axioms finite_signed_entropy_limit
#print axioms finite_signed_modular_limit
#print axioms signed_entropy_modular_difference
end
end ChatgptAudit.SignedGibbs
