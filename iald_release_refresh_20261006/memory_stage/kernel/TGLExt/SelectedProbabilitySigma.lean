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
import TGLExt.SigmaMatterConservation

set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.SelectedSigma
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.AngularTensorCodec
  ChatgptAudit.ProbeSource ChatgptAudit.MixedGibbsGravity
  ChatgptAudit.Micro021 ChatgptAudit.SelectedFisher ChatgptAudit.SigmaMatter
open scoped ContDiff
noncomputable section
variable {J : Type} [Fintype J] {U : Set Coordinate4}

/-- The complement is read from the selected label itself. -/
def selectedComplement (P : SelectedProbabilityData (Option J) U) (x : Coordinate4) : ℝ :=
  1-P.probabilities x P.selected

def conditionalProbability (P : SelectedProbabilityData (Option J) U) (j : J) (x : Coordinate4) : ℝ :=
  P.probabilities x (some j)/selectedComplement P x

def sigmaPotential (P : SelectedProbabilityData (Option J) U) (j : J) (x : Coordinate4) : ℝ :=
  Real.sqrt (conditionalProbability P j x)

def sigmaCovectors (P : SelectedProbabilityData (Option J) U) : J → CovectorField4 :=
  potentialFamily (sigmaPotential P)

theorem conditional_probability_none (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) (x : Coordinate4) :
    conditionalProbability P j x=P.probabilities x (some j)/(1-P.probabilities x none) := by
  simp only [conditionalProbability,selectedComplement,hsel]

theorem selected_complement_sum (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (x : Coordinate4) :
    selectedComplement P x=∑ j, P.probabilities x (some j) := by
  have hn := P.normalized x
  rw [Fintype.sum_option] at hn
  dsimp [selectedComplement]
  rw [hsel]
  linarith

variable [Nonempty J]

theorem selected_complement_positive (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (x : Coordinate4) (hx : x∈U) :
    0<selectedComplement P x := by
  rw [selected_complement_sum P hsel x]
  exact Finset.sum_pos (fun j _ => P.positive x hx (some j)) Finset.univ_nonempty

theorem conditional_probability_positive (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) (x : Coordinate4) (hx : x∈U) :
    0<conditionalProbability P j x :=
  div_pos (P.positive x hx (some j)) (selected_complement_positive P hsel x hx)

theorem conditional_probability_normalized (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (x : Coordinate4) (hx : x∈U) :
    ∑ j, conditionalProbability P j x=1 := by
  simp only [conditionalProbability]
  rw [← Finset.sum_div,← selected_complement_sum P hsel x]
  exact div_self (ne_of_gt (selected_complement_positive P hsel x hx))

theorem conditional_probability_smooth (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) :
    ContDiffOn ℝ ∞ (conditionalProbability P j) U := by
  apply (P.smooth (some j)).div (contDiffOn_const.sub (P.smooth P.selected))
  intro x hx
  exact ne_of_gt (selected_complement_positive P hsel x hx)

theorem sigma_potential_positive (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) (x : Coordinate4) (hx : x∈U) :
    0<sigmaPotential P j x :=
  Real.sqrt_pos.2 (conditional_probability_positive P hsel j x hx)

theorem sigma_potential_square (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) (x : Coordinate4) (hx : x∈U) :
    (sigmaPotential P j x)^2=conditionalProbability P j x :=
  Real.sq_sqrt (le_of_lt (conditional_probability_positive P hsel j x hx))

theorem sigma_potential_normalized (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (x : Coordinate4) (hx : x∈U) :
    ∑ j, (sigmaPotential P j x)^2=1 := by
  simp_rw [sigma_potential_square P hsel _ x hx]
  exact conditional_probability_normalized P hsel x hx

theorem sigma_potential_smooth (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (j : J) :
    ContDiffOn ℝ ∞ (sigmaPotential P j) U :=
  (conditional_probability_smooth P hsel j).sqrt
    (fun x hx => ne_of_gt (conditional_probability_positive P hsel j x hx))

theorem sigma_covectors_smooth (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (j : J) :
    SmoothVectorOn U (sigmaCovectors P j) :=
  potential_family_smooth U hU (sigmaPotential P) (sigma_potential_smooth P hsel) j

theorem sigma_covectors_closed (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (j : J) :
    ClosedCovectorOn U (sigmaCovectors P j) :=
  potential_family_closed U hU (sigmaPotential P) (sigma_potential_smooth P hsel) j

theorem sigma_tangent_constraint (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    ∑ j, sigmaPotential P j x * sigmaCovectors P j x i=0 :=
  sphere_constraint_tangent U hU (sigmaPotential P) (sigma_potential_smooth P hsel)
    (sigma_potential_normalized P hsel) x hx i

/-- Geometry and sigma probes are both derived from P before imposing field/area equations. -/
def selectedSigmaRecord (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) : GravitationalResponseRecord U :=
  sigmaGibbsRecord hU (selectedLorentzRecord P hU)
    (sigmaPotential P) (sigma_potential_smooth P hsel) k

theorem selected_sigma_metric (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) :
    recordMetric (selectedSigmaRecord P hsel hU k)=selectedMetric P :=
  selected_record_decodes_derived_metric P hU

theorem selected_sigma_source (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) (hk : 0<k) :
    recordSource (selectedSigmaRecord P hsel hU k)=
      finiteCovectorStressField (selectedMetric P) (metricInverse (selectedMetric P))
        (sigmaCovectors P) (fun _ => 1) (fun _ => k/(Real.pi*Real.cosh k^2)) := by
  have h := sigma_gibbs_source hU (selectedLorentzRecord P hU)
    (sigmaPotential P) (sigma_potential_smooth P hsel) k hk
  simpa only [selectedSigmaRecord,sigmaCovectors,selected_record_decodes_derived_metric] using h

theorem selected_sigma_entropy_null_limit (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) (hk : 0<k)
    (x v : Coordinate4) (hn : tensorQuad (selectedMetric P x) v=0) :
    Tendsto (fun t => gibbsEntropyIncrement (fun _ : J => k) (fun j => sigmaCovectors P j x) v t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (selectedSigmaRecord P hsel hU k) x) v)) := by
  apply gibbs_entropy_null_limit (selectedLorentzRecord P hU) (fun _ : J => k) (fun _ => hk)
    (sigmaCovectors P) (sigma_covectors_smooth P hsel hU) x v
  simpa only [gibbs_record_metric,selected_record_decodes_derived_metric] using hn

theorem selected_sigma_modular_null_limit (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) (hk : 0<k)
    (x v : Coordinate4) (hn : tensorQuad (selectedMetric P x) v=0) :
    Tendsto (fun t => gibbsModularIncrement (fun _ : J => k) (fun j => sigmaCovectors P j x) v t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (-Real.pi*tensorQuad (recordSource (selectedSigmaRecord P hsel hU k) x) v)) := by
  apply gibbs_modular_null_limit (selectedLorentzRecord P hU) (fun _ : J => k) (fun _ => hk)
    (sigmaCovectors P) (sigma_covectors_smooth P hsel hU) x v
  simpa only [gibbs_record_metric,selected_record_decodes_derived_metric] using hn

/-- The sigma equations are a condition on P; conservation is derived, not a second input. -/
theorem selected_sigma_conserved (P : SelectedProbabilityData (Option J) U)
    (hsel : P.selected=none) (hU : IsOpen U) (k : ℝ) (hk : 0<k)
    (lambda : Coordinate4 → ℝ)
    (heigen : ∀ j, ∀ x∈U, covectorDivergence (metricInverse (selectedMetric P))
      (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P)))
      (sigmaCovectors P j) x=lambda x*sigmaPotential P j x) :
    ∀ x∈U, ∀ i, tensorFieldDivergence (metricInverse (selectedMetric P))
      (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P)))
      (recordSource (selectedSigmaRecord P hsel hU k)) x i=0 := by
  have hh : ∀ j, ∀ x∈U, covectorDivergence
      (metricInverse (decodeRecord (selectedLorentzRecord P hU).data))
      (leviCivitaField (decodeRecord (selectedLorentzRecord P hU).data)
        (metricInverse (decodeRecord (selectedLorentzRecord P hU).data)))
      (potentialFamily (sigmaPotential P) j) x=lambda x*sigmaPotential P j x := by
    simpa only [selected_record_decodes_derived_metric,sigmaCovectors] using heigen
  have h := sigma_gibbs_conserved hU (selectedLorentzRecord P hU)
    (sigmaPotential P) (sigma_potential_smooth P hsel)
    (sigma_potential_normalized P hsel) lambda k hk hh
  simpa only [selectedSigmaRecord,selected_record_decodes_derived_metric] using h

/-- Area matching remains an explicit postulate of physical correspondence. -/
theorem selected_sigma_einstein_from_area
    (P : SelectedProbabilityData (Option J) U) (hsel : P.selected=none)
    (hU : IsOpen U) (hconn : IsPreconnected U) (k : ℝ) (hk : 0<k)
    (lambda : Coordinate4 → ℝ)
    (heigen : ∀ j, ∀ x∈U, covectorDivergence (metricInverse (selectedMetric P))
      (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P)))
      (sigmaCovectors P j) x=lambda x*sigmaPotential P j x)
    (screens : MetricScreenFamily U (recordMetric (selectedSigmaRecord P hsel hU k)))
    (eta : ℝ) (heta : eta≠0)
    (harea : ∀ x (hx : x∈U) v (hv : v≠0)
      (hn : tensorQuad (recordMetric (selectedSigmaRecord P hsel hU k) x) v=0),
      Tendsto (fun t => (gibbsEntropyIncrement (fun _ : J => k) (fun j => sigmaCovectors P j x) v t-eta*
        (inducedArea (recordMetric (selectedSigmaRecord P hsel hU k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors t-
         inducedArea (recordMetric (selectedSigmaRecord P hsel hU k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors 0))/t^2) (𝓝[<] (0:ℝ)) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (selectedMetric P) (metricInverse (selectedMetric P))
        (leviCivitaField (selectedMetric P) (metricInverse (selectedMetric P))) x +
        cosmological • selectedMetric P x =
          (2*Real.pi/eta) • recordSource (selectedSigmaRecord P hsel hU k) x := by
  have h : ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric (selectedSigmaRecord P hsel hU k))
        (metricInverse (recordMetric (selectedSigmaRecord P hsel hU k)))
        (leviCivitaField (recordMetric (selectedSigmaRecord P hsel hU k))
          (metricInverse (recordMetric (selectedSigmaRecord P hsel hU k)))) x +
        cosmological • recordMetric (selectedSigmaRecord P hsel hU k) x =
          (2*Real.pi/eta) • recordSource (selectedSigmaRecord P hsel hU k) x := by
    apply sigma_gibbs_einstein_from_area hU hconn (selectedLorentzRecord P hU)
      (sigmaPotential P) (sigma_potential_smooth P hsel) (sigma_potential_normalized P hsel)
      lambda k hk ?_ screens eta heta harea
    simpa only [selected_record_decodes_derived_metric,sigmaCovectors] using heigen
  simpa only [selected_sigma_metric] using h

#print axioms selectedComplement
#print axioms conditionalProbability
#print axioms sigmaPotential
#print axioms sigmaCovectors
#print axioms conditional_probability_none
#print axioms selected_complement_sum
#print axioms selected_complement_positive
#print axioms conditional_probability_positive
#print axioms conditional_probability_normalized
#print axioms conditional_probability_smooth
#print axioms sigma_potential_positive
#print axioms sigma_potential_square
#print axioms sigma_potential_normalized
#print axioms sigma_potential_smooth
#print axioms sigma_covectors_smooth
#print axioms sigma_covectors_closed
#print axioms sigma_tangent_constraint
#print axioms selectedSigmaRecord
#print axioms selected_sigma_metric
#print axioms selected_sigma_source
#print axioms selected_sigma_entropy_null_limit
#print axioms selected_sigma_modular_null_limit
#print axioms selected_sigma_conserved
#print axioms selected_sigma_einstein_from_area
end
end ChatgptAudit.SelectedSigma
