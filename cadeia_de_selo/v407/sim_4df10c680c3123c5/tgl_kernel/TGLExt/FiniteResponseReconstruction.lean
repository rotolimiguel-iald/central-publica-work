-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TensorNullCone
import TGLExt.SmoothMatrixCalculus

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.FiniteResponseRecord
open Matrix TGLExt
noncomputable section

abbrev ResponseSamples := Fin 10 → ℝ

def probeDirections : Fin 10 → Coordinate4 :=
  ![![1,0,0,0], ![0,1,0,0], ![0,0,1,0], ![0,0,0,1],
    ![1,1,0,0], ![1,0,1,0], ![1,0,0,1],
    ![0,1,1,0], ![0,1,0,1], ![0,0,1,1]]

def sampleResponse (q : Coordinate4 → ℝ) : ResponseSamples :=
  fun i => q (probeDirections i)

def decodeResponse (s : ResponseSamples) : Tensor4 :=
  !![s 0, (s 4-s 0-s 1)/2, (s 5-s 0-s 2)/2, (s 6-s 0-s 3)/2;
     (s 4-s 0-s 1)/2, s 1, (s 7-s 1-s 2)/2, (s 8-s 1-s 3)/2;
     (s 5-s 0-s 2)/2, (s 7-s 1-s 2)/2, s 2, (s 9-s 2-s 3)/2;
     (s 6-s 0-s 3)/2, (s 8-s 1-s 3)/2, (s 9-s 2-s 3)/2, s 3]

theorem ten_probe_directions : Fintype.card (Fin 10)=10 := by norm_num

theorem decoded_response_symmetric (s : ResponseSamples) :
    (decodeResponse s)ᵀ=decodeResponse s := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem quadratic_response_samples (A : Tensor4) (hs : Aᵀ=A) :
    sampleResponse (tensorQuad A) =
      ![A 0 0, A 1 1, A 2 2, A 3 3,
        A 0 0+A 1 1+2*A 0 1, A 0 0+A 2 2+2*A 0 2, A 0 0+A 3 3+2*A 0 3,
        A 1 1+A 2 2+2*A 1 2, A 1 1+A 3 3+2*A 1 3, A 2 2+A 3 3+2*A 2 3] := by
  funext i
  fin_cases i
  · change tensorQuad A ![1,0,0,0]=A 0 0
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,0,0]=A 1 1
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,1,0]=A 2 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,0,1]=A 3 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,1,0,0]=A 0 0+A 1 1+2*A 0 1
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,0,1,0]=A 0 0+A 2 2+2*A 0 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![1,0,0,1]=A 0 0+A 3 3+2*A 0 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,1,0]=A 1 1+A 2 2+2*A 1 2
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,1,0,1]=A 1 1+A 3 3+2*A 1 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]
  · change tensorQuad A ![0,0,1,1]=A 2 2+A 3 3+2*A 2 3
    rw [tensorQuad_components A hs]
    norm_num [symmetricForm4]

theorem decode_quadratic_response (A : Tensor4) (hs : Aᵀ=A) :
    decodeResponse (sampleResponse (tensorQuad A))=A := by
  rw [quadratic_response_samples A hs]
  have hsym (i j : Fin 4) : A j i=A i j :=
    congrArg (fun M : Tensor4 => M i j) hs
  ext i j
  fin_cases i <;> fin_cases j
  · change A 0 0=A 0 0
    rfl
  · change (A 0 0+A 1 1+2*A 0 1-A 0 0-A 1 1)/2=A 0 1
    ring
  · change (A 0 0+A 2 2+2*A 0 2-A 0 0-A 2 2)/2=A 0 2
    ring
  · change (A 0 0+A 3 3+2*A 0 3-A 0 0-A 3 3)/2=A 0 3
    ring
  · change (A 0 0+A 1 1+2*A 0 1-A 0 0-A 1 1)/2=A 1 0
    rw [hsym 0 1]
    ring
  · change A 1 1=A 1 1
    rfl
  · change (A 1 1+A 2 2+2*A 1 2-A 1 1-A 2 2)/2=A 1 2
    ring
  · change (A 1 1+A 3 3+2*A 1 3-A 1 1-A 3 3)/2=A 1 3
    ring
  · change (A 0 0+A 2 2+2*A 0 2-A 0 0-A 2 2)/2=A 2 0
    rw [hsym 0 2]
    ring
  · change (A 1 1+A 2 2+2*A 1 2-A 1 1-A 2 2)/2=A 2 1
    rw [hsym 1 2]
    ring
  · change A 2 2=A 2 2
    rfl
  · change (A 2 2+A 3 3+2*A 2 3-A 2 2-A 3 3)/2=A 2 3
    ring
  · change (A 0 0+A 3 3+2*A 0 3-A 0 0-A 3 3)/2=A 3 0
    rw [hsym 0 3]
    ring
  · change (A 1 1+A 3 3+2*A 1 3-A 1 1-A 3 3)/2=A 3 1
    rw [hsym 1 3]
    ring
  · change (A 2 2+A 3 3+2*A 2 3-A 2 2-A 3 3)/2=A 3 2
    rw [hsym 2 3]
    ring
  · change A 3 3=A 3 3
    rfl

theorem sample_decoded_response (s : ResponseSamples) :
    sampleResponse (tensorQuad (decodeResponse s))=s := by
  rw [quadratic_response_samples _ (decoded_response_symmetric s)]
  funext i
  fin_cases i
  · change s 0=s 0
    rfl
  · change s 1=s 1
    rfl
  · change s 2=s 2
    rfl
  · change s 3=s 3
    rfl
  · change s 0+s 1+2*((s 4-s 0-s 1)/2)=s 4
    ring
  · change s 0+s 2+2*((s 5-s 0-s 2)/2)=s 5
    ring
  · change s 0+s 3+2*((s 6-s 0-s 3)/2)=s 6
    ring
  · change s 1+s 2+2*((s 7-s 1-s 2)/2)=s 7
    ring
  · change s 1+s 3+2*((s 8-s 1-s 3)/2)=s 8
    ring
  · change s 2+s 3+2*((s 9-s 2-s 3)/2)=s 9
    ring

theorem response_samples_determine_symmetric_tensor (A B : Tensor4)
    (hA : Aᵀ=A) (hB : Bᵀ=B)
    (hs : sampleResponse (tensorQuad A)=sampleResponse (tensorQuad B)) : A=B := by
  rw [← decode_quadratic_response A hA, hs, decode_quadratic_response B hB]

theorem decoded_response_injective : Function.Injective decodeResponse := by
  intro s t h
  simpa only [sample_decoded_response] using congrArg (fun A => sampleResponse (tensorQuad A)) h

theorem response_samples_equality_iff (A B : Tensor4) (hA : Aᵀ=A) (hB : Bᵀ=B) :
    sampleResponse (tensorQuad A)=sampleResponse (tensorQuad B) ↔ A=B := by
  exact ⟨response_samples_determine_symmetric_tensor A B hA hB, fun h => congrArg (fun M => sampleResponse (tensorQuad M)) h⟩

/-- A response law is a substantive hypothesis; it is not inferred from ten arbitrary numbers. -/
theorem finite_response_reconstructs_given_tensor (q : Coordinate4 → ℝ) (A : Tensor4)
    (hA : Aᵀ=A) (hq : ∀ d, q d=tensorQuad A d) :
    decodeResponse (sampleResponse q)=A := by
  have he : q=tensorQuad A := funext hq
  rw [he, decode_quadratic_response A hA]

theorem reconstructed_quadratic_matches_all_directions (q : Coordinate4 → ℝ)
    (A : Tensor4) (hA : Aᵀ=A) (hq : ∀ d, q d=tensorQuad A d) :
    ∀ d, tensorQuad (decodeResponse (sampleResponse q)) d=q d := by
  rw [finite_response_reconstructs_given_tensor q A hA hq]
  exact fun d => (hq d).symm

#print axioms ResponseSamples
#print axioms probeDirections
#print axioms sampleResponse
#print axioms decodeResponse
#print axioms ten_probe_directions
#print axioms decoded_response_symmetric
#print axioms quadratic_response_samples
#print axioms decode_quadratic_response
#print axioms sample_decoded_response
#print axioms response_samples_determine_symmetric_tensor
#print axioms decoded_response_injective
#print axioms response_samples_equality_iff
#print axioms finite_response_reconstructs_given_tensor
#print axioms reconstructed_quadratic_matches_all_directions
end
end ChatgptAudit.FiniteResponseRecord
