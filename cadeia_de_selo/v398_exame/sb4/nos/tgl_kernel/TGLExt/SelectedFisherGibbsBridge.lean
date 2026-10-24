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
import TGLExt.SelectedFisherLorentzMetric
import TGLExt.MixedGibbsGravitationalBridge

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.SelectedFisherGibbs
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.AngularTensorCodec
  ChatgptAudit.ProbeSource ChatgptAudit.MixedGibbsGravity
  ChatgptAudit.Micro021 ChatgptAudit.SelectorRecord ChatgptAudit.SelectedAtlas
  ChatgptAudit.SelectedFisher ChatgptAudit.FisherField
open scoped ContDiff
noncomputable section
variable {ι : Type} [Fintype ι] {U : Set Coordinate4}

/-- The source covectors are derivatives of the same input probability observations. -/
def probabilityCovectors (P : SelectedProbabilityData ι U) : ι → CovectorField4 :=
  fun i => potentialCovector (fun x => P.probabilities x i)

theorem probability_covectors_smooth (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (i : ι) : SmoothVectorOn U (probabilityCovectors P i) :=
  potential_covector_smooth U hU _ (P.smooth i)

theorem probability_covectors_closed (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (i : ι) : ClosedCovectorOn U (probabilityCovectors P i) :=
  potential_covector_closed U hU _ (P.smooth i)

/-- Both metric and source probes are constructed from P before any balance law is imposed. -/
def selectedGibbsRecord (P : SelectedProbabilityData ι U) (hU : IsOpen U) (k : ι → ℝ) :
    GravitationalResponseRecord U :=
  gibbsRecord (selectedLorentzRecord P hU) k (probabilityCovectors P)
    (probability_covectors_smooth P hU)

theorem selected_gibbs_metric (P : SelectedProbabilityData ι U) (hU : IsOpen U) (k : ι → ℝ) :
    recordMetric (selectedGibbsRecord P hU k)=selectedMetric P :=
  selected_record_decodes_derived_metric P hU

theorem selected_gibbs_source (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (k : ι → ℝ) (hk : ∀ i, 0<k i) :
    recordSource (selectedGibbsRecord P hU k)=
      finiteCovectorStressField (selectedMetric P) (metricInverse (selectedMetric P))
        (probabilityCovectors P) (fun _ => 1) (fun i => k i/(Real.pi*Real.cosh (k i)^2)) := by
  have h := gibbs_record_source (selectedLorentzRecord P hU) k hk
    (probabilityCovectors P) (probability_covectors_smooth P hU)
  simpa only [selectedGibbsRecord,selected_record_decodes_derived_metric] using h

theorem selected_gibbs_entropy_null_limit (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (k : ι → ℝ) (hk : ∀ i, 0<k i) (x v : Coordinate4)
    (hn : tensorQuad (selectedMetric P x) v=0) :
    Tendsto (fun t => gibbsEntropyIncrement k (fun i => probabilityCovectors P i x) v t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (selectedGibbsRecord P hU k) x) v)) := by
  apply gibbs_entropy_null_limit (selectedLorentzRecord P hU) k hk
    (probabilityCovectors P) (probability_covectors_smooth P hU) x v
  simpa only [gibbs_record_metric,selected_record_decodes_derived_metric] using hn

theorem selected_gibbs_modular_null_limit (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (k : ι → ℝ) (hk : ∀ i, 0<k i) (x v : Coordinate4)
    (hn : tensorQuad (selectedMetric P x) v=0) :
    Tendsto (fun t => gibbsModularIncrement k (fun i => probabilityCovectors P i x) v t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (selectedGibbsRecord P hU k) x) v)) := by
  apply gibbs_modular_null_limit (selectedLorentzRecord P hU) k hk
    (probabilityCovectors P) (probability_covectors_smooth P hU) x v
  simpa only [gibbs_record_metric,selected_record_decodes_derived_metric] using hn

/-- Smooth gradients are closed automatically; their wave equations are additional conditions. -/
theorem selected_gibbs_source_conserved (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (k : ι → ℝ)
    (hwave : ∀ i, CovectorWaveOn U (metricInverse (selectedMetric P))
      (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P))) (probabilityCovectors P i)) :
    ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse (recordMetric (selectedGibbsRecord P hU k)))
      (leviCivitaField (recordMetric (selectedGibbsRecord P hU k))
        (metricInverse (recordMetric (selectedGibbsRecord P hU k))))
      (recordSource (selectedGibbsRecord P hU k)) x j=0 := by
  apply probe_record_conserved hU (selectedLorentzRecord P hU) (fun i => gibbsSlope (k i))
    (probabilityCovectors P) (probability_covectors_smooth P hU) (probability_covectors_closed P hU)
  simpa only [selected_record_decodes_derived_metric] using hwave

/-- Conditional Einstein equation for data P. This is not variation of an action in P. -/
theorem selected_gibbs_einstein_from_wave_area
    (P : SelectedProbabilityData ι U) (hU : IsOpen U) (hconn : IsPreconnected U)
    (k : ι → ℝ) (hk : ∀ i, 0<k i)
    (hwave : ∀ i, CovectorWaveOn U (metricInverse (selectedMetric P))
      (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P))) (probabilityCovectors P i))
    (screens : MetricScreenFamily U (recordMetric (selectedGibbsRecord P hU k)))
    (eta : ℝ) (heta : eta≠0)
    (harea : ∀ x (hx : x∈U) v (hv : v≠0)
      (hn : tensorQuad (recordMetric (selectedGibbsRecord P hU k) x) v=0),
      Tendsto (fun t => (gibbsEntropyIncrement k (fun i => probabilityCovectors P i x) v t-eta*
        (inducedArea (recordMetric (selectedGibbsRecord P hU k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors t-
         inducedArea (recordMetric (selectedGibbsRecord P hU k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors 0))/t^2) (𝓝[<] (0:ℝ)) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric (selectedGibbsRecord P hU k))
        (metricInverse (recordMetric (selectedGibbsRecord P hU k)))
        (leviCivitaField (recordMetric (selectedGibbsRecord P hU k))
          (metricInverse (recordMetric (selectedGibbsRecord P hU k)))) x +
        cosmological • recordMetric (selectedGibbsRecord P hU k) x =
          (2*Real.pi/eta) • recordSource (selectedGibbsRecord P hU k) x := by
  apply gibbs_einstein_from_observed_area hU hconn (selectedLorentzRecord P hU) k hk
    (probabilityCovectors P) (probability_covectors_smooth P hU) (probability_covectors_closed P hU)
    ?_ screens eta heta harea
  simpa only [selected_record_decodes_derived_metric] using hwave

#print axioms probabilityCovectors
#print axioms probability_covectors_smooth
#print axioms probability_covectors_closed
#print axioms selectedGibbsRecord
#print axioms selected_gibbs_metric
#print axioms selected_gibbs_source
#print axioms selected_gibbs_entropy_null_limit
#print axioms selected_gibbs_modular_null_limit
#print axioms selected_gibbs_source_conserved
#print axioms selected_gibbs_einstein_from_wave_area
end
end ChatgptAudit.SelectedFisherGibbs
