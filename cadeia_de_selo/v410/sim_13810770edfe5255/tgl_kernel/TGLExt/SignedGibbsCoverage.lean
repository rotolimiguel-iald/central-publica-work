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
import TGLExt.SignedGibbsResponse
import TGLExt.GeneralSourceResponseReconstruction

set_option autoImplicit false
set_option maxHeartbeats 2200000
namespace ChatgptAudit.SignedGibbsCoverage
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.SignedGibbs ChatgptAudit.SignedCoverage
  ChatgptAudit.Coherent023 ChatgptAudit.FullSourceResponse
  ChatgptAudit.FiniteResponseRecord ChatgptAudit.GeneralMetric
noncomputable section

abbrev ProbeIndex := Fin 4 × Fin 2

def calibratedAmplitude (k c : ℝ) : ℝ := c*Real.pi*Real.cosh k^2/k

def probeSign (j : ProbeIndex) : ℝ := if j.2=0 then 1 else -1

def probeCovector (A : Tensor4) (j : ProbeIndex) : Coordinate4 :=
  if j.2=0 then plusCovector A j.1 else minusCovector A j.1

def entropyProbe (k : ℝ) (A : Tensor4) (d : Coordinate4) (t : ℝ) : ℝ :=
  signedEntropyIncrement (fun _ : ProbeIndex => k)
    (fun j => calibratedAmplitude k (probeSign j)) (probeCovector A) d t

def modularProbe (k : ℝ) (A : Tensor4) (d : Coordinate4) (t : ℝ) : ℝ :=
  signedModularIncrement (fun _ : ProbeIndex => k)
    (fun j => calibratedAmplitude k (probeSign j)) (probeCovector A) d t

theorem calibrated_coupling {k : ℝ} (hk : 0<k) (c : ℝ) :
    signedCoupling k (calibratedAmplitude k c)=c := by
  unfold signedCoupling calibratedAmplitude
  field_simp [ne_of_gt hk,Real.pi_ne_zero,ne_of_gt (Real.cosh_pos k)]

theorem all_probe_probabilities_positive {k : ℝ} (hk : 0<k)
    (A : Tensor4) (d : Coordinate4) (t : ℝ) (j : ProbeIndex) (i : Fin 2) :
    0<signedWeights k (calibratedAmplitude k (probeSign j))
      (covectorRead (probeCovector A j) d) t i ∧
    signedWeights k (calibratedAmplitude k (probeSign j))
      (covectorRead (probeCovector A j) d) t i<1 :=
  signed_weights_interior hk _ _ _ i

theorem all_probe_probabilities_normalized (k : ℝ) (A : Tensor4)
    (d : Coordinate4) (t : ℝ) (j : ProbeIndex) :
    ∑ i, signedWeights k (calibratedAmplitude k (probeSign j))
      (covectorRead (probeCovector A j) d) t i=1 :=
  signed_weights_normalized _ _ _ _

theorem outer_quadratic (w d : Coordinate4) :
    tensorQuad (Matrix.vecMulVec w w) d=(covectorRead w d)^2 := by
  simp only [tensorQuad,Matrix.vecMulVec,Matrix.of_apply,Matrix.mulVec,
    dotProduct,covectorRead,Fin.sum_univ_four]
  ring

theorem quadratic_sub (A B : Tensor4) (d : Coordinate4) :
    tensorQuad (A-B) d=tensorQuad A d-tensorQuad B d := by
  simp only [tensorQuad,Matrix.sub_mulVec,dotProduct_sub]

theorem quadratic_sum (A : Fin 4 → Tensor4) (d : Coordinate4) :
    tensorQuad (∑ i,A i) d=∑ i,tensorQuad (A i) d := by
  simp only [tensorQuad,Matrix.sum_mulVec,dotProduct_sum]

theorem eight_probe_quadratic (A : Tensor4) (hs : Aᵀ=A) (d : Coordinate4) :
    (∑ j : ProbeIndex, probeSign j*(covectorRead (probeCovector A j) d)^2)=
      tensorQuad A d := by
  rw [Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two,probeSign,probeCovector]
  have h10 : (1 : Fin 2)≠0 := by decide
  simp only [if_true,h10,if_false,one_mul,neg_one_mul,←sub_eq_add_neg]
  conv_rhs => rw [←signed_polarization A hs,quadratic_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [quadratic_sub,outer_quadratic,outer_quadratic]

theorem eight_probe_response (A : Tensor4) (hs : Aᵀ=A) (d : Coordinate4) :
    (∑ j : ProbeIndex, -Real.pi*probeSign j*(covectorRead (probeCovector A j) d)^2)=
      -Real.pi*tensorQuad A d := by
  simp only [mul_assoc,←Finset.mul_sum,eight_probe_quadratic A hs d]

theorem entropy_probe_limit {k : ℝ} (hk : 0<k) (A : Tensor4)
    (hs : Aᵀ=A) (d : Coordinate4) :
    Tendsto (fun t => entropyProbe k A d t/t^2) (𝓝[<] (0:ℝ))
      (𝓝 (-Real.pi*tensorQuad A d)) := by
  have h := finite_signed_entropy_limit (fun _ : ProbeIndex => k)
    (fun j => calibratedAmplitude k (probeSign j)) (fun _ => hk) (probeCovector A) d
  simpa only [entropyProbe,calibrated_coupling hk,eight_probe_response A hs d] using h

theorem modular_probe_limit {k : ℝ} (hk : 0<k) (A : Tensor4)
    (hs : Aᵀ=A) (d : Coordinate4) :
    Tendsto (fun t => modularProbe k A d t/t^2) (𝓝[<] (0:ℝ))
      (𝓝 (-Real.pi*tensorQuad A d)) := by
  have h := finite_signed_modular_limit (fun _ : ProbeIndex => k)
    (fun j => calibratedAmplitude k (probeSign j)) (fun _ => hk) (probeCovector A) d
  simpa only [modularProbe,calibrated_coupling hk,eight_probe_response A hs d] using h

theorem source_entropy_limit {k : ℝ} (hk : 0<k) (g gi T : Tensor4)
    (hg : gᵀ=g) (hT : Tᵀ=T) (d : Coordinate4) :
    Tendsto (fun t => entropyProbe k (traceReverse g gi T) d t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (calibratedPointResponse g gi T d)) := by
  rw [calibrated_point_response_all_directions g gi T d hg hT]
  exact entropy_probe_limit hk _ (trace_reverse_symmetric g gi T hg hT) d

theorem source_modular_limit {k : ℝ} (hk : 0<k) (g gi T : Tensor4)
    (hg : gᵀ=g) (hT : Tᵀ=T) (d : Coordinate4) :
    Tendsto (fun t => modularProbe k (traceReverse g gi T) d t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (calibratedPointResponse g gi T d)) := by
  rw [calibrated_point_response_all_directions g gi T d hg hT]
  exact modular_probe_limit hk _ (trace_reverse_symmetric g gi T hg hT) d

/-- Ten observed limits reconstruct a calibrated input source; no matter dynamics is inferred. -/
theorem measured_gibbs_limits_reconstruct_source {k : ℝ} (hk : 0<k)
    (g gi T : Tensor4) (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T)
    (q : Coordinate4 → ℝ)
    (hlim : ∀ d,Tendsto (fun t => entropyProbe k (traceReverse g gi T) d t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (q d))) :
    decodeSource g gi (sampleResponse q)=T := by
  have he : q=calibratedPointResponse g gi T := by
    funext d
    exact tendsto_nhds_unique (hlim d) (source_entropy_limit hk g gi T hg hT d)
  rw [he]
  exact ten_responses_reconstruct_source g gi T hi hg hT

#print axioms ProbeIndex
#print axioms calibratedAmplitude
#print axioms probeSign
#print axioms probeCovector
#print axioms entropyProbe
#print axioms modularProbe
#print axioms calibrated_coupling
#print axioms all_probe_probabilities_positive
#print axioms all_probe_probabilities_normalized
#print axioms outer_quadratic
#print axioms quadratic_sub
#print axioms quadratic_sum
#print axioms eight_probe_quadratic
#print axioms eight_probe_response
#print axioms entropy_probe_limit
#print axioms modular_probe_limit
#print axioms source_entropy_limit
#print axioms source_modular_limit
#print axioms measured_gibbs_limits_reconstruct_source
end
end ChatgptAudit.SignedGibbsCoverage
