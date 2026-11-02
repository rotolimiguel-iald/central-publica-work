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
import TGLExt.ProbeResponseRecord
import TGLExt.SelectorRecordReconstruction

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.MixedGibbsGravity
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.AngularTensorCodec
  ChatgptAudit.ProbeSource ChatgptAudit.MixedQuadraticGibbs
  ChatgptAudit.Micro021 ChatgptAudit.SelectorRecord ChatgptAudit.SelectedAtlas
  ChatgptAudit.UnifiedRecorded
open scoped ContDiff
noncomputable section
variable {J : Type} [Fintype J] {U : Set Coordinate4}

/-- The positive response is derived from the fixed mixed Gibbs protocol, not from T. -/
def gibbsSlope (k : ℝ) : ℝ := Real.sqrt (2*k/Real.cosh k^2)

/-- Sum of the entropies of finitely many independent, normalized two-outcome probes. -/
def gibbsEntropyIncrement (k : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) (t : ℝ) : ℝ :=
  ∑ j, (finiteEntropy (quadraticWeights (k j) (covectorRead (w j) d) t)-finiteEntropy (mixedBase (k j)))

def gibbsModularIncrement (k : J → ℝ) (w : J → Coordinate4) (d : Coordinate4) (t : ℝ) : ℝ :=
  ∑ j, modularIncrement (mixedBase (k j)) (quadraticWeights (k j) (covectorRead (w j) d) t)

def gibbsRecord (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    GravitationalResponseRecord U :=
  probeRecord metric (fun j => gibbsSlope (k j)) w hw

theorem gibbs_slope_sq (k : ℝ) (hk : 0 < k) : gibbsSlope k^2=2*k/Real.cosh k^2 := by
  apply Real.sq_sqrt
  positivity

theorem gibbs_slope_positive (k : ℝ) (hk : 0 < k) : 0 < gibbsSlope k := by
  unfold gibbsSlope
  positivity

theorem gibbs_coupling (k : ℝ) (hk : 0 < k) :
    responseCoupling (gibbsSlope k)=k/(Real.pi*Real.cosh k^2) := by
  rw [responseCoupling,gibbs_slope_sq k hk]
  ring

theorem gibbs_response_coefficient (k velocity : ℝ) (hk : 0 < k) :
    -(gibbsSlope k*velocity)^2/2 = -k/Real.cosh k^2*velocity^2 := by
  rw [mul_pow,gibbs_slope_sq k hk]
  ring

theorem gibbs_entropy_response_limit (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => gibbsEntropyIncrement k w d t/t^2) (𝓝[<] (0 : ℝ))
      (𝓝 (probeEntropyResponse (fun j => gibbsSlope (k j)) w d)) := by
  have h := tendsto_finsetSum Finset.univ (fun j _ =>
    quadratic_entropy_limit (hk j) (covectorRead (w j) d))
  simpa only [gibbsEntropyIncrement,Finset.sum_div,probeEntropyResponse,
    gibbs_response_coefficient _ _ (hk _)] using h

theorem gibbs_modular_response_limit (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => gibbsModularIncrement k w d t/t^2) (𝓝[<] (0 : ℝ))
      (𝓝 (probeEntropyResponse (fun j => gibbsSlope (k j)) w d)) := by
  have h := tendsto_finsetSum Finset.univ (fun j _ =>
    quadratic_modular_increment_limit (hk j) (covectorRead (w j) d))
  simpa only [gibbsModularIncrement,Finset.sum_div,probeEntropyResponse,
    gibbs_response_coefficient _ _ (hk _)] using h

theorem gibbs_entropy_modular_difference (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → Coordinate4) (d : Coordinate4) :
    Tendsto (fun t => (gibbsEntropyIncrement k w d t-gibbsModularIncrement k w d t)/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0) := by
  simpa only [sub_self,←sub_div] using
    (gibbs_entropy_response_limit k hk w d).sub (gibbs_modular_response_limit k hk w d)

theorem gibbs_record_metric (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    recordMetric (gibbsRecord metric k w hw)=decodeRecord metric.data := rfl

theorem gibbs_record_source (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (hk : ∀ j, 0 < k j) (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    recordSource (gibbsRecord metric k w hw)=
      finiteCovectorStressField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))
        w (fun _ => 1) (fun j => k j/(Real.pi*Real.cosh (k j)^2)) := by
  rw [gibbsRecord,probe_record_source]
  simp only [gibbs_coupling _ (hk _)]

theorem gibbs_entropy_null_limit (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (hk : ∀ j, 0 < k j) (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (x d : Coordinate4) (hn : tensorQuad (recordMetric (gibbsRecord metric k w hw) x) d=0) :
    Tendsto (fun t => gibbsEntropyIncrement k (fun j => w j x) d t/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (gibbsRecord metric k w hw) x) d)) := by
  have h := gibbs_entropy_response_limit k hk (fun j => w j x) d
  rw [probe_record_null_response metric (fun j => gibbsSlope (k j)) w hw x d hn] at h
  exact h

theorem gibbs_modular_null_limit (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (hk : ∀ j, 0 < k j) (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (x d : Coordinate4) (hn : tensorQuad (recordMetric (gibbsRecord metric k w hw) x) d=0) :
    Tendsto (fun t => gibbsModularIncrement k (fun j => w j x) d t/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (gibbsRecord metric k w hw) x) d)) := by
  have h := gibbs_modular_response_limit k hk (fun j => w j x) d
  rw [probe_record_null_response metric (fun j => gibbsSlope (k j)) w hw x d hn] at h
  exact h

/-- Transfer of area matching uses equality of response coefficients, not equality of states. -/
theorem gibbs_area_transfers_to_record (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (hk : ∀ j, 0 < k j) (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (x d : Coordinate4) (hx : x∈U)
    (hn : tensorQuad (recordMetric (gibbsRecord metric k w hw) x) d=0)
    (eta : ℝ) (area : ℝ → ℝ)
    (ha : Tendsto (fun t => (gibbsEntropyIncrement k (fun j => w j x) d t-
      eta*(area t-area 0))/t^2) (𝓝[<] (0 : ℝ)) (𝓝 0)) :
    Tendsto (fun t => microscopicAreaError (recordPreparation (gibbsRecord metric k w hw) x d)
      eta area t/t^2) (𝓝[<] (0 : ℝ)) (𝓝 0) := by
  have h := ((record_preparation_entropy_null (gibbsRecord metric k w hw) x d hx hn).sub
    (gibbs_entropy_null_limit metric k hk w hw x d hn)).add ha
  simp only [sub_self,zero_add] at h
  convert! h using 1
  funext t
  unfold microscopicAreaError
  ring

/-- The physical area correspondence remains an explicit hypothesis. Conservation is paid
by the closed and wave equations of the probe covectors; no source tensor is an input. -/
theorem gibbs_einstein_from_observed_area
    (hU : IsOpen U) (hconn : IsPreconnected U)
    (metric : LorentzProbabilityRecord U) (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (hc : ∀ j, ClosedCovectorOn U (w j))
    (hwave : ∀ j, CovectorWaveOn U (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))) (w j))
    (screens : MetricScreenFamily U (recordMetric (gibbsRecord metric k w hw)))
    (eta : ℝ) (heta : eta≠0)
    (harea : ∀ x (hx : x∈U) d (hv : d≠0)
      (hn : tensorQuad (recordMetric (gibbsRecord metric k w hw) x) d=0),
      Tendsto (fun t => (gibbsEntropyIncrement k (fun j => w j x) d t-eta*
        (inducedArea (recordMetric (gibbsRecord metric k w hw)) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors t-
         inducedArea (recordMetric (gibbsRecord metric k w hw)) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors 0))/t^2) (𝓝[<] (0 : ℝ)) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric (gibbsRecord metric k w hw))
        (metricInverse (recordMetric (gibbsRecord metric k w hw)))
        (leviCivitaField (recordMetric (gibbsRecord metric k w hw))
          (metricInverse (recordMetric (gibbsRecord metric k w hw)))) x +
        cosmological • recordMetric (gibbsRecord metric k w hw) x =
          (2*Real.pi/eta) • recordSource (gibbsRecord metric k w hw) x := by
  apply record_einstein_from_area U hU hconn (gibbsRecord metric k w hw) screens eta heta
  · exact probe_record_conserved hU metric (fun j => gibbsSlope (k j)) w hw hc hwave
  · intro x hx d hv hn
    exact gibbs_area_transfers_to_record metric k hk w hw x d hx hn eta _ (harea x hx d hv hn)

theorem gibbs_selector_recovers_fields [Nonempty U] (parameter : ℝ) (hp : parameter≠0)
    (metric : LorentzProbabilityRecord U) (k : J → ℝ)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j)) :
    let R := gibbsRecord metric k w hw
    let D := reconstructedRecord (operatorCharacter parameter R)
    EqOn (recordMetric D) (recordMetric R) U ∧ EqOn (recordSource D) (recordSource R) U :=
  selector_reconstructs_metric_and_source parameter hp (gibbsRecord metric k w hw)

theorem gibbs_selector_einstein_from_observed_area [Nonempty U]
    (parameter : ℝ) (hp : parameter≠0) (hU : IsOpen U) (hconn : IsPreconnected U)
    (metric : LorentzProbabilityRecord U) (k : J → ℝ) (hk : ∀ j, 0 < k j)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (hc : ∀ j, ClosedCovectorOn U (w j))
    (hwave : ∀ j, CovectorWaveOn U (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))) (w j))
    (screens : MetricScreenFamily U (recordMetric (gibbsRecord metric k w hw)))
    (eta : ℝ) (heta : eta≠0)
    (harea : ∀ x (hx : x∈U) d (hv : d≠0)
      (hn : tensorQuad (recordMetric (gibbsRecord metric k w hw) x) d=0),
      Tendsto (fun t => (gibbsEntropyIncrement k (fun j => w j x) d t-eta*
        (inducedArea (recordMetric (gibbsRecord metric k w hw)) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors t-
         inducedArea (recordMetric (gibbsRecord metric k w hw)) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors 0))/t^2) (𝓝[<] (0 : ℝ)) (𝓝 0)) :
    let D := reconstructedRecord (operatorCharacter parameter (gibbsRecord metric k w hw))
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric D) (metricInverse (recordMetric D))
        (leviCivitaField (recordMetric D) (metricInverse (recordMetric D))) x +
        cosmological • recordMetric D x=(2*Real.pi/eta) • recordSource D x := by
  apply selector_reconstructs_einstein_from_area parameter hp hU hconn
    (gibbsRecord metric k w hw) screens eta heta
  · exact probe_record_conserved hU metric (fun j => gibbsSlope (k j)) w hw hc hwave
  · intro x hx d hv hn
    apply (unified_area_matching_iff (gibbsRecord metric k w hw) x d eta _).mpr
    exact gibbs_area_transfers_to_record metric k hk w hw x d hx hn eta _ (harea x hx d hv hn)

#print axioms gibbsSlope
#print axioms gibbsEntropyIncrement
#print axioms gibbsModularIncrement
#print axioms gibbsRecord
#print axioms gibbs_slope_sq
#print axioms gibbs_slope_positive
#print axioms gibbs_coupling
#print axioms gibbs_response_coefficient
#print axioms gibbs_entropy_response_limit
#print axioms gibbs_modular_response_limit
#print axioms gibbs_entropy_modular_difference
#print axioms gibbs_record_metric
#print axioms gibbs_record_source
#print axioms gibbs_entropy_null_limit
#print axioms gibbs_modular_null_limit
#print axioms gibbs_area_transfers_to_record
#print axioms gibbs_einstein_from_observed_area
#print axioms gibbs_selector_recovers_fields
#print axioms gibbs_selector_einstein_from_observed_area
end
end ChatgptAudit.MixedGibbsGravity
