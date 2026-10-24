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
import TGLExt.FiniteCoherentSources
import TGLExt.MixedGibbsGravitationalBridge

set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.SigmaMatter
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.AngularTensorCodec
  ChatgptAudit.ProbeSource ChatgptAudit.MixedGibbsGravity
  ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section
variable {J : Type} [Fintype J]

/-- The total divergence is the aggregate force; individual waves need not vanish. -/
theorem finite_closed_stress_divergence
    (U : Set Coordinate4) (hU : IsOpen U)
    (g gi : TensorField4) (Gamma : ConnectionField4) (w : J → CovectorField4)
    (weight coupling : J → ℝ) (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gi)
    (hw : ∀ q, SmoothVectorOn U (w q))
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hl : ∀ x∈U, gi x*g x=1) (hr : ∀ x∈U, g x*gi x=1)
    (ht : ∀ x∈U, ∀ i j k, Gamma x i k j=Gamma x j k i)
    (hc : ∀ q, ClosedCovectorOn U (w q)) (x : Coordinate4) (hx : x∈U) (j : Fin 4) :
    tensorFieldDivergence gi Gamma (finiteCovectorStressField g gi w weight coupling) x j =
      ∑ q, weight q*coupling q*(covectorDivergence gi Gamma (w q) x*w q x j) := by
  rw [finite_covector_stress_divergence U hU g gi Gamma w weight coupling hg hgi hw x hx j]
  apply Finset.sum_congr rfl
  intro q _
  rw [covector_stress_divergence_closed g gi Gamma (w q) (coupling q) x
    (smooth_matrix_differentiableAt U hU g hg x hx)
    (smooth_matrix_differentiableAt U hU gi hgi x hx)
    (smooth_vector_differentiableAt U hU (w q) (hw q) x hx)
    (hl x hx) (inverse_symmetric_of_symmetric (g x) (gi x) (hs x hx) (hl x hx))
    (hm x hx) (fun i => inverse_metric_derivative U hU g gi Gamma hg hgi hm hl hr x hx i)
    (covector_derivative_symmetric Gamma (w q) x (hc q x hx) (ht x hx)) j]
  ring

theorem finite_stress_conserved_of_aggregate
    (U : Set Coordinate4) (hU : IsOpen U)
    (g gi : TensorField4) (Gamma : ConnectionField4) (w : J → CovectorField4)
    (weight coupling : J → ℝ) (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gi)
    (hw : ∀ q, SmoothVectorOn U (w q))
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hl : ∀ x∈U, gi x*g x=1) (hr : ∀ x∈U, g x*gi x=1)
    (ht : ∀ x∈U, ∀ i j k, Gamma x i k j=Gamma x j k i)
    (hc : ∀ q, ClosedCovectorOn U (w q))
    (hforce : ∀ x∈U, ∀ j, ∑ q,
      weight q*coupling q*(covectorDivergence gi Gamma (w q) x*w q x j)=0) :
    ∀ x∈U, ∀ j, tensorFieldDivergence gi Gamma
      (finiteCovectorStressField g gi w weight coupling) x j=0 := by
  intro x hx j
  rw [finite_closed_stress_divergence U hU g gi Gamma w weight coupling hg hgi hw
    hm hs hl hr ht hc x hx j]
  exact hforce x hx j

/-- A scalar potential is shared by its gradient and its wave equation. -/
def potentialFamily (phi : J → Coordinate4 → ℝ) : J → CovectorField4 :=
  fun q => potentialCovector (phi q)

omit [Fintype J] in
theorem potential_family_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U) (q : J) :
    SmoothVectorOn U (potentialFamily phi q) :=
  potential_covector_smooth U hU _ (hphi q)

omit [Fintype J] in
theorem potential_family_closed (U : Set Coordinate4) (hU : IsOpen U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U) (q : J) :
    ClosedCovectorOn U (potentialFamily phi q) :=
  potential_covector_closed U hU _ (hphi q)

/-- Differentiating the sphere constraint derives its tangent identity on the open domain. -/
theorem sphere_constraint_tangent (U : Set Coordinate4) (hU : IsOpen U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U)
    (hnorm : ∀ x∈U, ∑ q, (phi q x)^2=1) (x : Coordinate4) (hx : x∈U) (j : Fin 4) :
    ∑ q, phi q x*potentialFamily phi q x j=0 := by
  have hd (q : J) : DifferentiableAt ℝ (phi q) x :=
    ((hphi q).differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)
  have he : (fun y => ∑ q, (phi q y)^2) =ᶠ[𝓝 x] (fun _ => (1:ℝ)) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact hnorm y hy
  have hz : fderiv ℝ (fun y => ∑ q, (phi q y)^2) x=0 := by
    rw [he.fderiv_eq]
    simp
  have hsum : fderiv ℝ (fun y => ∑ q, (phi q y)^2) x=
      ∑ q, (2*phi q x) • fderiv ℝ (phi q) x := by
    calc fderiv ℝ (fun y => ∑ q, (phi q y)^2) x =
        ∑ q, fderiv ℝ (fun y => (phi q y)^2) x :=
          fderiv_fun_sum (fun q _ => (hd q).pow 2)
      _ = _ := by
        apply Finset.sum_congr rfl
        intro q _
        simpa using fderiv_fun_pow 2 (hd q)
  rw [hsum] at hz
  have hv := congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single j 1)) hz
  simp only [_root_.sum_apply,_root_.smul_apply,
    _root_.zero_apply,smul_eq_mul] at hv
  change (∑ q, (2*phi q x)*potentialFamily phi q x j)=0 at hv
  have hh : 2*(∑ q, phi q x*potentialFamily phi q x j)=0 := by
    rw [Finset.mul_sum]
    convert! hv using 1
    apply Finset.sum_congr rfl
    intro q _
    ring
  linarith

/-- A shared eigenvalue cancels after summing the constrained fields, even when nonzero. -/
theorem sigma_aggregate_cancellation (U : Set Coordinate4) (hU : IsOpen U)
    (gi : TensorField4) (Gamma : ConnectionField4)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U)
    (hnorm : ∀ x∈U, ∑ q, (phi q x)^2=1) (lambda : Coordinate4 → ℝ) (c : ℝ)
    (heigen : ∀ q, ∀ x∈U,
      covectorDivergence gi Gamma (potentialFamily phi q) x=lambda x*phi q x) :
    ∀ x∈U, ∀ j, ∑ q,
      c*(covectorDivergence gi Gamma (potentialFamily phi q) x*potentialFamily phi q x j)=0 := by
  intro x hx j
  calc (∑ q, c*(covectorDivergence gi Gamma (potentialFamily phi q) x*potentialFamily phi q x j)) =
      c*lambda x*(∑ q, phi q x*potentialFamily phi q x j) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro q _
        rw [heigen q x hx]
        ring
    _ = 0 := by rw [sphere_constraint_tangent U hU phi hphi hnorm x hx j,mul_zero]

/-- Metric compatibility, inverse and torsion-free connection are derived from the metric. -/
theorem metric_finite_conserved_of_aggregate (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g) (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (w : J → CovectorField4) (weight coupling : J → ℝ)
    (hw : ∀ q, SmoothVectorOn U (w q)) (hc : ∀ q, ClosedCovectorOn U (w q))
    (hforce : ∀ x∈U, ∀ j, ∑ q, weight q*coupling q*
      (covectorDivergence (metricInverse g) (leviCivitaField g (metricInverse g)) (w q) x*w q x j)=0) :
    ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g) (leviCivitaField g (metricInverse g))
      (finiteCovectorStressField g (metricInverse g) w weight coupling) x j=0 := by
  have hi := constructed_metric_inverse_smooth U g hg hLor
  have hs : ∀ x∈U, (g x)ᵀ=g x := fun x hx => lorentz_metric_symmetric _ (hLor x hx)
  have hl : ∀ x∈U, metricInverse g x*g x=1 := fun x hx => constructed_metric_inverse_left g x (hLor x hx)
  have hr : ∀ x∈U, g x*metricInverse g x=1 := fun x hx => constructed_metric_inverse_right g x (hLor x hx)
  exact finite_stress_conserved_of_aggregate U hU g (metricInverse g)
    (leviCivitaField g (metricInverse g)) w weight coupling hg hi hw
    (levi_civita_field_metric_compatible U hU g (metricInverse g) hs hl hr) hs hl hr
    (levi_civita_field_torsion_free U hU g (metricInverse g) hs) hc hforce

theorem metric_sigma_stress_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g) (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U)
    (hnorm : ∀ x∈U, ∑ q, (phi q x)^2=1) (lambda : Coordinate4 → ℝ) (c : ℝ)
    (heigen : ∀ q, ∀ x∈U, covectorDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (potentialFamily phi q) x=lambda x*phi q x) :
    ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g) (leviCivitaField g (metricInverse g))
      (finiteCovectorStressField g (metricInverse g) (potentialFamily phi) (fun _ => 1) (fun _ => c)) x j=0 := by
  apply metric_finite_conserved_of_aggregate U hU g hg hLor (potentialFamily phi)
    (fun _ => 1) (fun _ => c) (potential_family_smooth U hU phi hphi) (potential_family_closed U hU phi hphi)
  simpa only [one_mul] using sigma_aggregate_cancellation U hU (metricInverse g)
    (leviCivitaField g (metricInverse g)) phi hphi hnorm lambda c heigen

def sigmaGibbsRecord {U : Set Coordinate4} (hU : IsOpen U) (metric : LorentzProbabilityRecord U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U) (k : ℝ) :
    GravitationalResponseRecord U :=
  gibbsRecord metric (fun _ : J => k) (potentialFamily phi) (potential_family_smooth U hU phi hphi)

theorem sigma_gibbs_metric {U : Set Coordinate4} (hU : IsOpen U) (metric : LorentzProbabilityRecord U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U) (k : ℝ) :
    recordMetric (sigmaGibbsRecord hU metric phi hphi k)=decodeRecord metric.data := rfl

theorem sigma_gibbs_source {U : Set Coordinate4} (hU : IsOpen U) (metric : LorentzProbabilityRecord U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U) (k : ℝ) (hk : 0<k) :
    recordSource (sigmaGibbsRecord hU metric phi hphi k)=
      finiteCovectorStressField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data))
        (potentialFamily phi) (fun _ => 1) (fun _ => k/(Real.pi*Real.cosh k^2)) :=
  gibbs_record_source metric (fun _ => k) (fun _ => hk) (potentialFamily phi)
    (potential_family_smooth U hU phi hphi)

theorem sigma_gibbs_conserved {U : Set Coordinate4} (hU : IsOpen U) (metric : LorentzProbabilityRecord U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U)
    (hnorm : ∀ x∈U, ∑ q, (phi q x)^2=1) (lambda : Coordinate4 → ℝ) (k : ℝ) (hk : 0<k)
    (heigen : ∀ q, ∀ x∈U, covectorDivergence (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data)))
      (potentialFamily phi q) x=lambda x*phi q x) :
    ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data)))
      (recordSource (sigmaGibbsRecord hU metric phi hphi k)) x j=0 := by
  rw [sigma_gibbs_source hU metric phi hphi k hk]
  exact metric_sigma_stress_conserved U hU _ (decoded_record_smooth metric.data) metric.lorentz
    phi hphi hnorm lambda _ heigen

/-- Area matching is retained; conservation is supplied by the aggregate sigma identity. -/
theorem sigma_gibbs_einstein_from_area {U : Set Coordinate4} (hU : IsOpen U) (hconn : IsPreconnected U)
    (metric : LorentzProbabilityRecord U)
    (phi : J → Coordinate4 → ℝ) (hphi : ∀ q, ContDiffOn ℝ ∞ (phi q) U)
    (hnorm : ∀ x∈U, ∑ q, (phi q x)^2=1) (lambda : Coordinate4 → ℝ) (k : ℝ) (hk : 0<k)
    (heigen : ∀ q, ∀ x∈U, covectorDivergence (metricInverse (decodeRecord metric.data))
      (leviCivitaField (decodeRecord metric.data) (metricInverse (decodeRecord metric.data)))
      (potentialFamily phi q) x=lambda x*phi q x)
    (screens : MetricScreenFamily U (recordMetric (sigmaGibbsRecord hU metric phi hphi k)))
    (eta : ℝ) (heta : eta≠0)
    (harea : ∀ x (hx : x∈U) v (hv : v≠0)
      (hn : tensorQuad (recordMetric (sigmaGibbsRecord hU metric phi hphi k) x) v=0),
      Tendsto (fun t => (gibbsEntropyIncrement (fun _ : J => k) (fun q => potentialFamily phi q x) v t-eta*
        (inducedArea (recordMetric (sigmaGibbsRecord hU metric phi hphi k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors t-
         inducedArea (recordMetric (sigmaGibbsRecord hU metric phi hphi k)) (screens x hx v hv hn).curve
          (screens x hx v hv hn).screen.vectors 0))/t^2) (𝓝[<] (0:ℝ)) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric (sigmaGibbsRecord hU metric phi hphi k))
        (metricInverse (recordMetric (sigmaGibbsRecord hU metric phi hphi k)))
        (leviCivitaField (recordMetric (sigmaGibbsRecord hU metric phi hphi k))
          (metricInverse (recordMetric (sigmaGibbsRecord hU metric phi hphi k)))) x +
        cosmological • recordMetric (sigmaGibbsRecord hU metric phi hphi k) x =
          (2*Real.pi/eta) • recordSource (sigmaGibbsRecord hU metric phi hphi k) x := by
  apply record_einstein_from_area U hU hconn (sigmaGibbsRecord hU metric phi hphi k) screens eta heta
  · exact sigma_gibbs_conserved hU metric phi hphi hnorm lambda k hk heigen
  · intro x hx v hv hn
    exact gibbs_area_transfers_to_record metric (fun _ : J => k) (fun _ => hk)
      (potentialFamily phi) (potential_family_smooth U hU phi hphi) x v hx hn eta _ (harea x hx v hv hn)

#print axioms finite_closed_stress_divergence
#print axioms finite_stress_conserved_of_aggregate
#print axioms potentialFamily
#print axioms potential_family_smooth
#print axioms potential_family_closed
#print axioms sphere_constraint_tangent
#print axioms sigma_aggregate_cancellation
#print axioms metric_finite_conserved_of_aggregate
#print axioms metric_sigma_stress_conserved
#print axioms sigmaGibbsRecord
#print axioms sigma_gibbs_metric
#print axioms sigma_gibbs_source
#print axioms sigma_gibbs_conserved
#print axioms sigma_gibbs_einstein_from_area
end
end ChatgptAudit.SigmaMatter
