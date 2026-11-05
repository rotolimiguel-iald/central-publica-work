-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_021 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.MicroscopicEinsteinBridge

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set TGLExt ChatgptAudit.Flow020
open scoped ComplexOrder
noncomputable section

def halfWeights (_i : Fin 2) : ℝ := 1/2
def signedResponse : Fin 2 → ℝ := ![1,-1]
def thirdWeights : Fin 2 → ℝ := ![1/3,2/3]

theorem half_weights_positive : ∀ i, 0<halfWeights i := by
  intro i
  norm_num [halfWeights]

theorem half_weights_normalized : ∑ i, halfWeights i=1 := by
  norm_num [halfWeights,Fin.sum_univ_two]

theorem signed_response_trace_zero : ∑ i, signedResponse i=0 := by
  norm_num [signedResponse,Fin.sum_univ_two]

theorem half_response_fisher : diagonalFisher halfWeights signedResponse=4 := by
  norm_num [diagonalFisher,halfWeights,signedResponse,Fin.sum_univ_two]

def halfAffine := affineStateCurve halfWeights signedResponse half_weights_normalized signed_response_trace_zero
def halfQuadratic := quadraticStateCurve halfWeights signedResponse half_weights_normalized signed_response_trace_zero

theorem half_affine_entropy_derivative :
    HasDerivAt (fun t => finiteEntropy (halfAffine.weights t)) 0 0 := by
  have hd := finite_entropy_first_law halfWeights signedResponse half_weights_positive signed_response_trace_zero
  have he : (∑ i, signedResponse i*(-Real.log (halfWeights i)))=0 := by
    norm_num [signedResponse,halfWeights,Fin.sum_univ_two]
  rw [he] at hd
  exact hd

theorem half_affine_relative_coefficient :
    Tendsto (fun t => diagonalRelativeEntropy (halfAffine.weights t) halfWeights/t^2)
      (𝓝[<] 0) (𝓝 2) := by
  have hh := affine_relative_entropy_quadratic_limit halfWeights signedResponse
    half_weights_normalized signed_response_trace_zero half_weights_positive
  simpa only [halfAffine,half_response_fisher,show (4:ℝ)/2=2 from by norm_num] using hh

theorem first_order_does_not_imply_second_order :
    HasDerivAt (fun t => finiteEntropy (halfAffine.weights t)) 0 0 ∧
    Tendsto (fun t => diagonalRelativeEntropy (halfAffine.weights t) halfWeights/t) (𝓝[<] 0) (𝓝 0) ∧
    ¬ Tendsto (fun t => diagonalRelativeEntropy (halfAffine.weights t) halfWeights/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  refine ⟨half_affine_entropy_derivative,relative_entropy_first_order_zero halfAffine half_weights_positive,?_⟩
  intro hh
  have he := tendsto_nhds_unique half_affine_relative_coefficient hh
  norm_num at he

theorem quadratic_response_is_not_frozen (t : ℝ) (ht : t≠0) :
    halfQuadratic.weights t≠halfWeights := by
  intro he
  have hh := congrArg (fun w : Fin 2 → ℝ => w 0) he
  norm_num [halfQuadratic,quadraticStateCurve,halfWeights,signedResponse] at hh
  exact ht hh

theorem half_quadratic_relative_zero :
    Tendsto (fun t => diagonalRelativeEntropy (halfQuadratic.weights t) halfWeights/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  quadratic_relative_entropy_zero halfWeights signedResponse half_weights_normalized
    signed_response_trace_zero half_weights_positive

theorem third_weights_positive : ∀ i, 0<thirdWeights i := by
  intro i
  fin_cases i <;> norm_num [thirdWeights]

theorem third_weights_normalized : ∑ i, thirdWeights i=1 := by
  norm_num [thirdWeights,Fin.sum_univ_two]

theorem third_modular_response :
    (∑ i, signedResponse i*(-Real.log (thirdWeights i)))=Real.log 2 := by
  calc
    _=Real.log ((2:ℝ)/3)-Real.log ((1:ℝ)/3) := by
      norm_num [signedResponse,thirdWeights,Fin.sum_univ_two]
      ring
    _=Real.log (((2:ℝ)/3)/((1:ℝ)/3)) :=
      (Real.log_div (by norm_num : (2:ℝ)/3≠0) (by norm_num : (1:ℝ)/3≠0)).symm
    _=Real.log 2 := by norm_num

def thirdQuadratic := quadraticStateCurve thirdWeights signedResponse
  third_weights_normalized signed_response_trace_zero

theorem nontracial_quadratic_response :
    Tendsto (fun t => (finiteEntropy (thirdQuadratic.weights t)-finiteEntropy thirdWeights)/t^2)
      (𝓝[<] 0) (𝓝 (Real.log 2)) ∧
    Tendsto (fun t => modularIncrement thirdWeights (thirdQuadratic.weights t)/t^2)
      (𝓝[<] 0) (𝓝 (Real.log 2)) ∧
    Tendsto (fun t => diagonalRelativeEntropy (thirdQuadratic.weights t) thirdWeights/t^2)
      (𝓝[<] 0) (𝓝 0) ∧ 0<Real.log 2 := by
  refine ⟨?_,?_,?_,Real.log_pos (by norm_num)⟩
  · simpa only [thirdQuadratic,third_modular_response] using
      quadratic_entropy_limit thirdWeights signedResponse third_weights_normalized
        signed_response_trace_zero third_weights_positive
  · simpa only [thirdQuadratic,third_modular_response] using
      quadratic_modular_limit thirdWeights signedResponse third_weights_normalized signed_response_trace_zero
  · exact quadratic_relative_entropy_zero thirdWeights signedResponse third_weights_normalized
      signed_response_trace_zero third_weights_positive

theorem state_curve_purification_near {ι : Type} [Fintype ι] [DecidableEq ι]
    {p : ι → ℝ} (X : DiagonalStateCurve p) (hp : ∀ i, 0<p i) :
    ∀ᶠ t in 𝓝 (0:ℝ),
      (pureCutDensity (X.weights t)).PosSemidef ∧
      Matrix.trace (pureCutDensity (X.weights t))=1 ∧
      pureCutDensity (X.weights t)*pureCutDensity (X.weights t)=pureCutDensity (X.weights t) ∧
      partialTraceRight (pureCutDensity (X.weights t))=
        Matrix.diagonal (fun i => (X.weights t i:ℂ)) := by
  filter_upwards [state_curve_positive_near X hp] with t ht
  have hn := fun i => le_of_lt (ht i)
  exact ⟨pure_cut_positive _,pure_cut_trace_one _ hn (X.trace_one t),
    pure_cut_idempotent _ hn (X.trace_one t),pure_cut_right_reduction _ hn⟩

theorem tower_quadratic_relative_zero (P : SiteProfile) (N : ℕ)
    (q : chainIdx N → ℝ) (hq : ∑ i, q i=0) :
    Tendsto (fun t => diagonalRelativeEntropy
      ((quadraticStateCurve (towerW P N) q (towerW_sum P N) hq).weights t) (towerW P N)/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  quadratic_relative_entropy_zero (towerW P N) q (towerW_sum P N) hq (towerW_pos P N)

theorem half_modular_response_zero :
    (∑ i, signedResponse i*(-Real.log (halfWeights i)))=0 := by
  norm_num [signedResponse,halfWeights,Fin.sum_univ_two]

def flatVacuumMatching : QuadraticScreenMatching (Fin 2) flatConstructedScreen (fun _ => 0)
    1 (2*Real.pi) isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth)
    (fun _ _ => differentiableOn_const _) where
  reference := halfWeights
  response := signedResponse
  positive := half_weights_positive
  normalized := half_weights_normalized
  trace_response := signed_response_trace_zero
  heat_matching := by
    let Q := constructedHeat flatConstructedScreen (fun _ => 0) 1 isOpen_univ
      (frame_metric_smooth univ flatSolder flat_solder_smooth) (fun _ _ => differentiableOn_const _)
    have hQ : Tendsto (fun t => Q t/t^2) (𝓝[<] 0) (𝓝 0) := by
      simpa [Q,tensorQuad] using constructed_heat_quadratic_limit flatConstructedScreen (fun _ => 0)
        1 isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth)
        (fun _ _ => differentiableOn_const _)
    have hK : Tendsto (fun t => modularIncrement halfWeights (halfQuadratic.weights t)/t^2)
        (𝓝[<] 0) (𝓝 0) := by
      simpa only [halfQuadratic,half_modular_response_zero] using quadratic_modular_limit halfWeights signedResponse
        half_weights_normalized signed_response_trace_zero
    have hc : Tendsto (fun _ : ℝ => (1:ℝ)/(2*Real.pi)) (𝓝[<] 0) (𝓝 ((1:ℝ)/(2*Real.pi))) :=
      tendsto_const_nhds
    change Tendsto (fun t => microscopicHeatError halfQuadratic 1 Q t/t^2) _ _
    have hf : (fun t => microscopicHeatError halfQuadratic 1 Q t/t^2)=
        (fun t => Q t/t^2-(1/(2*Real.pi))*(modularIncrement halfWeights (halfQuadratic.weights t)/t^2)) := by
      funext t
      unfold microscopicHeatError
      ring
    rw [hf]
    simpa only [mul_zero,sub_zero] using hQ.sub (hc.mul hK)
  area_matching := by
    let A := inducedArea (frameMetricField flatSolder) flatConstructedScreen.curve
      flatConstructedScreen.screen.vectors
    have hG : SmoothConnectionOn univ (frameLeviCivita flatSolder flatSolder) := by
      rw [flat_connection_zero]
      exact fun _ _ _ => contDiffOn_const
    have ht : ∀ i j a, (frameLeviCivita flatSolder flatSolder) 0 i a j=
        (frameLeviCivita flatSolder flatSolder) 0 j a i := by
      simp only [flat_connection_zero,Matrix.zero_apply,implies_true]
    have hA0 : A 0=1 :=
      ChatgptAudit.Flow019.equilibrium_screen_area_initial _ _ _ _ _ flatConstructedScreen
    have hA : Tendsto (fun t => (A t-A 0)/t^2) (𝓝[<] 0) (𝓝 0) := by
      rw [hA0]
      have hh := screen_area_quadratic_limit univ isOpen_univ (frameMetricField flatSolder)
        (frameLeviCivita flatSolder flatSolder) (frame_metric_smooth univ flatSolder flat_solder_smooth)
        hG 0 horizonControlDirection flatConstructedScreen ht
      simpa only [flat_ricci_zero,tensorQuad,Matrix.zero_mulVec,dotProduct_zero,neg_zero,zero_div] using hh
    have hS : Tendsto (fun t => (finiteEntropy (halfQuadratic.weights t)-finiteEntropy halfWeights)/t^2)
        (𝓝[<] 0) (𝓝 0) := by
      simpa only [halfQuadratic,half_modular_response_zero] using quadratic_entropy_limit halfWeights signedResponse
        half_weights_normalized signed_response_trace_zero half_weights_positive
    have hc : Tendsto (fun _ : ℝ => 2*Real.pi) (𝓝[<] 0) (𝓝 (2*Real.pi)) := tendsto_const_nhds
    change Tendsto (fun t => microscopicAreaError halfQuadratic (2*Real.pi) A t/t^2) _ _
    have hf : (fun t => microscopicAreaError halfQuadratic (2*Real.pi) A t/t^2)=
        (fun t => (finiteEntropy (halfQuadratic.weights t)-finiteEntropy halfWeights)/t^2-
          (2*Real.pi)*((A t-A 0)/t^2)) := by
      funext t
      unfold microscopicAreaError
      ring
    rw [hf]
    simpa only [mul_zero,sub_zero] using hS.sub (hc.mul hA)

theorem flat_nonzero_matter_has_no_quadratic_matching (ι : Type) [Fintype ι] :
    ¬ Nonempty (QuadraticScreenMatching ι flatConstructedScreen controlMatter 1 (2*Real.pi)
      isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth) control_matter_differentiable) := by
  rintro ⟨M⟩
  have hh := matching_produces_clausius flatConstructedScreen controlMatter 1 (2*Real.pi)
    isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth) control_matter_differentiable M
  exact flat_nonzero_matter_not_clausius hh

theorem modular_increment_is_generator_trace {ι : Type} [Fintype ι] [DecidableEq ι]
    (p r : ι → ℝ) :
    (modularIncrement p r : ℂ)=Matrix.trace
      (Matrix.diagonal (fun i => ((r i-p i : ℝ):ℂ))*diagonalModularGenerator p) := by
  unfold modularIncrement diagonalModularGenerator
  rw [Matrix.diagonal_mul_diagonal,Matrix.trace_diagonal]
  simp only [Complex.ofReal_sum]
  apply Finset.sum_congr rfl
  intro i _
  exact Complex.ofReal_mul _ _

#print axioms modular_increment_is_generator_trace

#print axioms half_modular_response_zero
#print axioms flatVacuumMatching
#print axioms flat_nonzero_matter_has_no_quadratic_matching

#print axioms half_weights_positive
#print axioms half_weights_normalized
#print axioms signed_response_trace_zero
#print axioms half_response_fisher
#print axioms half_affine_entropy_derivative
#print axioms half_affine_relative_coefficient
#print axioms first_order_does_not_imply_second_order
#print axioms quadratic_response_is_not_frozen
#print axioms half_quadratic_relative_zero
#print axioms third_weights_positive
#print axioms third_weights_normalized
#print axioms third_modular_response
#print axioms nontracial_quadratic_response
#print axioms state_curve_purification_near
#print axioms tower_quadratic_relative_zero
end
end ChatgptAudit.Micro021
