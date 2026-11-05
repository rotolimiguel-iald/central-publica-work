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
import TGLExt.SignedGibbsCoverage

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.SignedGibbsFinite
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.SignedGibbsCoverage ChatgptAudit.FullSourceResponse
  ChatgptAudit.FiniteResponseRecord ChatgptAudit.GeneralMetric ChatgptAudit.SignedCoverage
noncomputable section

/-- Exactly ten entropy limits suffice; no response function on all directions is an input. -/
theorem ten_entropy_limits_reconstruct_source {k : ℝ} (hk : 0<k)
    (g gi T : Tensor4) (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T)
    (s : ResponseSamples)
    (hlim : ∀ i : Fin 10,
      Tendsto (fun t => entropyProbe k (traceReverse g gi T) (probeDirections i) t/t^2)
        (𝓝[<] (0:ℝ)) (𝓝 (s i))) :
    decodeSource g gi s=T := by
  have hs : s=sampleResponse (calibratedPointResponse g gi T) := by
    funext i
    exact tendsto_nhds_unique (hlim i)
      (source_entropy_limit hk g gi T hg hT (probeDirections i))
  rw [hs]
  exact ten_responses_reconstruct_source g gi T hi hg hT

/-- The same finite readout is sufficient for ten modular limits. -/
theorem ten_modular_limits_reconstruct_source {k : ℝ} (hk : 0<k)
    (g gi T : Tensor4) (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T)
    (s : ResponseSamples)
    (hlim : ∀ i : Fin 10,
      Tendsto (fun t => modularProbe k (traceReverse g gi T) (probeDirections i) t/t^2)
        (𝓝[<] (0:ℝ)) (𝓝 (s i))) :
    decodeSource g gi s=T := by
  have hs : s=sampleResponse (calibratedPointResponse g gi T) := by
    funext i
    exact tendsto_nhds_unique (hlim i)
      (source_modular_limit hk g gi T hg hT (probeDirections i))
  rw [hs]
  exact ten_responses_reconstruct_source g gi T hi hg hT

#print axioms ten_entropy_limits_reconstruct_source
#print axioms ten_modular_limits_reconstruct_source
end
end ChatgptAudit.SignedGibbsFinite
