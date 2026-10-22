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
import TGLExt.GeneralSourceResponseReconstruction
import TGLExt.MixedGibbsGravitationalBridge

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.ResponseError
open Matrix TGLExt ChatgptAudit ChatgptAudit.FiniteResponseRecord
  ChatgptAudit.FullSourceResponse ChatgptAudit.SignedCoverage
  ChatgptAudit.GravitationalRecord ChatgptAudit.MixedGibbsGravity
noncomputable section

def SampleErrorBound (delta : ℝ) (s r : ResponseSamples) : Prop :=
  ∀ i, |s i-r i| ≤ delta

def TensorErrorBound (delta : ℝ) (A B : Tensor4) : Prop :=
  ∀ i j, |A i j-B i j| ≤ delta

theorem three_term_error {a b c x y z delta : ℝ}
    (ha : |a-x|≤delta) (hb : |b-y|≤delta) (hc : |c-z|≤delta) :
    |(a-b-c)/2-(x-y-z)/2|≤3*delta/2 := by
  obtain ⟨ha0,ha1⟩ := abs_le.mp ha
  obtain ⟨hb0,hb1⟩ := abs_le.mp hb
  obtain ⟨hc0,hc1⟩ := abs_le.mp hc
  apply abs_le.mpr
  constructor <;> linarith

theorem decoded_response_error {delta : ℝ} (hd : 0≤delta) (s r : ResponseSamples)
    (hs : SampleErrorBound delta s r) :
    TensorErrorBound (3*delta/2) (decodeResponse s) (decodeResponse r) := by
  have hdiag (i : Fin 10) : |s i-r i|≤3*delta/2 := (hs i).trans (by linarith)
  have hpair (a b c : Fin 10) :
      |(s a-s b-s c)/2-(r a-r b-r c)/2|≤3*delta/2 :=
    three_term_error (hs a) (hs b) (hs c)
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [decodeResponse]
  all_goals first | exact hdiag _ | exact hpair _ _ _

theorem normalized_samples_error {delta : ℝ} (s r : ResponseSamples)
    (hs : SampleErrorBound delta s r) :
    SampleErrorBound (delta/Real.pi) (normalizedSamples s) (normalizedSamples r) := by
  intro i
  simp only [normalizedSamples,←sub_div,abs_div,abs_neg,abs_of_pos Real.pi_pos]
  exact div_le_div_of_nonneg_right (hs i) Real.pi_pos.le

theorem trace_product_error {B epsilon : ℝ} (hB : 0≤B)
    (gi A C : Tensor4) (hgi : ∀ i j, |gi i j|≤B)
    (hAC : TensorErrorBound epsilon A C) :
    |Matrix.trace (gi*A)-Matrix.trace (gi*C)|≤16*B*epsilon := by
  rw [←Matrix.trace_sub,←Matrix.mul_sub]
  simp only [Matrix.trace,Matrix.diag,Matrix.mul_apply]
  calc
    |∑ i : Fin 4, ∑ j : Fin 4, gi i j*(A-C) j i|
        ≤ ∑ i : Fin 4, ∑ j : Fin 4, |gi i j*(A-C) j i| :=
      (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum (fun i _ =>
        Finset.abs_sum_le_sum_abs _ _))
    _ ≤ ∑ _i : Fin 4, ∑ _j : Fin 4, B*epsilon := by
      apply Finset.sum_le_sum
      intro i _
      apply Finset.sum_le_sum
      intro j _
      rw [abs_mul]
      exact mul_le_mul (hgi i j) (hAC j i) (abs_nonneg _) hB
    _ = 16*B*epsilon := by simp; ring

theorem trace_reverse_error {B G epsilon : ℝ} (hB : 0≤B)
    (g gi A C : Tensor4) (hg : ∀ i j, |g i j|≤G) (hgi : ∀ i j, |gi i j|≤B)
    (hAC : TensorErrorBound epsilon A C) :
    TensorErrorBound ((1+8*G*B)*epsilon) (traceReverse g gi A) (traceReverse g gi C) := by
  have ht := trace_product_error hB gi A C hgi hAC
  have heps : 0 ≤ epsilon := (abs_nonneg _).trans (hAC 0 0)
  intro i j
  change |(A i j-(Matrix.trace (gi*A)/2)*g i j)-
    (C i j-(Matrix.trace (gi*C)/2)*g i j)|≤_
  have he : (A i j-(Matrix.trace (gi*A)/2)*g i j)-
      (C i j-(Matrix.trace (gi*C)/2)*g i j)=
      (A i j-C i j)-(Matrix.trace (gi*A)-Matrix.trace (gi*C))/2*g i j := by ring
  rw [he]
  calc
    |(A i j-C i j)-(Matrix.trace (gi*A)-Matrix.trace (gi*C))/2*g i j|
        ≤ |A i j-C i j|+|(Matrix.trace (gi*A)-Matrix.trace (gi*C))/2*g i j| :=
      abs_sub _ _
    _ ≤ epsilon+(16*B*epsilon/2)*G := by
      apply add_le_add (hAC i j)
      rw [abs_mul,abs_div,abs_of_pos (show (0:ℝ)<2 by norm_num)]
      exact mul_le_mul (div_le_div_of_nonneg_right ht (by norm_num)) (hg i j)
        (abs_nonneg _) (by positivity)
    _ = (1+8*G*B)*epsilon := by ring

/-- The metric and its inverse are fixed here. This is not a stability claim for curvature. -/
theorem decoded_source_error {delta B G : ℝ} (hd : 0≤delta) (hB : 0≤B)
    (g gi : Tensor4) (hg : ∀ i j, |g i j|≤G) (hgi : ∀ i j, |gi i j|≤B)
    (s r : ResponseSamples) (hs : SampleErrorBound delta s r) :
    TensorErrorBound ((1+8*G*B)*(3*delta/(2*Real.pi)))
      (decodeSource g gi s) (decodeSource g gi r) := by
  have h := trace_reverse_error hB g gi _ _ hg hgi
    (decoded_response_error (by positivity) _ _ (normalized_samples_error s r hs))
  convert! h using 1; ring

theorem finite_difference_response_error {observed exact response t noise remainder : ℝ}
    (ht : t≠0) (hnoise : |observed-exact|≤noise)
    (hremainder : |exact-response*t^2|≤remainder*t^4) :
    |observed/t^2-response|≤noise/t^2+remainder*t^2 := by
  have h0 : 0<t^2 := sq_pos_of_ne_zero ht
  have h : |observed-response*t^2|≤noise+remainder*t^4 := by
    calc
      |observed-response*t^2|≤|observed-exact|+|exact-response*t^2| :=
        abs_sub_le _ _ _
      _ ≤ noise+remainder*t^4 := add_le_add hnoise hremainder
  have hh := div_le_div_of_nonneg_right h h0.le
  have he : observed/t^2-response=(observed-response*t^2)/t^2 := by
    field_simp [ht]
  rw [he,abs_div,abs_of_pos h0]
  calc
    _ ≤ (noise+remainder*t^4)/t^2 := hh
    _ = noise/t^2+remainder*t^2 := by field_simp [ht]

theorem measured_samples_error {t noise remainder : ℝ} (ht : t≠0)
    (observed exact response : ResponseSamples)
    (hn : ∀ i, |observed i-exact i|≤noise)
    (hr : ∀ i, |exact i-response i*t^2|≤remainder*t^4) :
    SampleErrorBound (noise/t^2+remainder*t^2) (fun i => observed i/t^2) response :=
  fun i => finite_difference_response_error ht (hn i) (hr i)

theorem measured_source_error {t noise remainder B G : ℝ} (ht : t≠0)
    (hn0 : 0≤noise) (hr0 : 0≤remainder) (hB : 0≤B)
    (g gi : Tensor4) (hg : ∀ i j, |g i j|≤G) (hgi : ∀ i j, |gi i j|≤B)
    (observed exact response : ResponseSamples)
    (hn : ∀ i, |observed i-exact i|≤noise)
    (hr : ∀ i, |exact i-response i*t^2|≤remainder*t^4) :
    TensorErrorBound ((1+8*G*B)*(3*(noise/t^2+remainder*t^2)/(2*Real.pi)))
      (decodeSource g gi (fun i => observed i/t^2)) (decodeSource g gi response) :=
  decoded_source_error (by positivity) hB g gi hg hgi _ _
    (measured_samples_error ht observed exact response hn hr)

#print axioms SampleErrorBound
#print axioms TensorErrorBound
#print axioms three_term_error
#print axioms decoded_response_error
#print axioms normalized_samples_error
#print axioms trace_product_error
#print axioms trace_reverse_error
#print axioms decoded_source_error
#print axioms finite_difference_response_error
#print axioms measured_samples_error
#print axioms measured_source_error
end
end ChatgptAudit.ResponseError
