-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_010 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.LocalHorizonBalance

set_option autoImplicit false
set_option maxHeartbeats 3600000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

/-- Explicit local geometric and thermodynamic inputs. Existence is not asserted here. -/
structure LocalHorizonPencil (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (T : TensorField4) (eta : ℝ) (x v : Coordinate4) where
  neighborhood : Set Coordinate4
  neighborhood_open : IsOpen neighborhood
  neighborhood_subset : neighborhood ⊆ U
  point_mem : x∈neighborhood
  velocity : VectorField4
  velocity_smooth : SmoothVectorOn neighborhood velocity
  velocity_at_point : velocity x=v
  velocity_null : ∀ y∈neighborhood, tensorQuad (g y) (velocity y)=0
  geodesic : Set.EqOn (vectorAcceleration Gamma velocity) (fun _ => 0) neighborhood
  equilibrium_gradient : covariantVectorGradient Gamma velocity x=0
  curve : ℝ → Coordinate4
  curve_zero : curve 0=x
  curve_tangent : HasDerivAt curve v 0
  rate : ℝ
  rate_nonzero : rate≠0
  area : ℝ → ℝ
  area_continuous : ContinuousAt area 0
  area_nonzero : area 0≠0
  heat : ℝ → ℝ
  heat_continuous : ContinuousAt heat 0
  heat_zero : heat 0=0
  area_rate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt area
    (vectorExpansion Gamma velocity (curve t)*area t) t
  heat_rate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt heat
    (-rate*t*tensorQuad (T (curve t)) (velocity (curve t))*area t) t
  clausius_to_second_order : Tendsto
    (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0) (𝓝 0)

theorem tensor_quad_field_continuous (T : TensorField4) (V : VectorField4) (x : Coordinate4)
    (hT : ∀ a b, ContinuousAt (fun y => T y a b) x)
    (hV : ∀ a, ContinuousAt (fun y => V y a) x) :
    ContinuousAt (fun y => tensorQuad (T y) (V y)) x := by
  unfold tensorQuad Matrix.mulVec dotProduct
  fun_prop

theorem pencil_ricci_balance (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (T : TensorField4) (eta : ℝ) (heta : eta≠0)
    (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (x v : Coordinate4) (ht : ∀ i j a, Gamma x i a j=Gamma x j a i)
    (P : LocalHorizonPencil U g Gamma T eta x v) :
    tensorQuad (coordinateRicci Gamma x) v=(2*Real.pi/eta)*tensorQuad (T x) v := by
  have hx : x∈U := P.neighborhood_subset P.point_mem
  have hGn : SmoothConnectionOn P.neighborhood Gamma :=
    fun i a b => (hG i a b).mono P.neighborhood_subset
  have hdV := smooth_vector_differentiableAt P.neighborhood P.neighborhood_open
    P.velocity P.velocity_smooth x P.point_mem
  have hqt := tensor_quad_field_continuous T P.velocity x
    (fun a b => ((hT a b).differentiableAt (hU.mem_nhds hx)).continuousAt)
    (fun a => (hdV a).continuousAt)
  have hqtc : ContinuousAt (fun t => tensorQuad (T (P.curve t)) (P.velocity (P.curve t))) 0 := by
    have he : ContinuousAt (fun y => tensorQuad (T y) (P.velocity y)) (P.curve 0) := by
      simpa only [P.curve_zero] using hqt
    exact he.comp P.curve_tangent.continuousAt
  have hcv : HasDerivAt P.curve (P.velocity x) 0 := by
    rw [P.velocity_at_point]
    exact P.curve_tangent
  have htheta := curve_expansion_focusing P.neighborhood P.neighborhood_open
    Gamma P.velocity hGn P.velocity_smooth P.geodesic x P.point_mem ht
    P.equilibrium_gradient P.curve P.curve_zero hcv
  have hz : vectorExpansion Gamma P.velocity (P.curve 0)=0 := by
    rw [P.curve_zero,vectorExpansion,P.equilibrium_gradient]
    simp
  have hb := heat_area_clausius_implies_local P.rate eta _
    (fun t => vectorExpansion Gamma P.velocity (P.curve t)) P.area
    (fun t => tensorQuad (T (P.curve t)) (P.velocity (P.curve t))) P.heat
    htheta hz P.area_continuous hqtc P.heat_continuous P.heat_zero
    P.area_rate P.heat_rate P.clausius_to_second_order
  have hr := local_clausius_forces_ricci P.rate eta _
    (fun t => vectorExpansion Gamma P.velocity (P.curve t)) P.area
    (fun t => tensorQuad (T (P.curve t)) (P.velocity (P.curve t)))
    P.rate_nonzero heta P.area_nonzero htheta hz P.area_continuous hqtc hb
  simpa only [P.curve_zero,P.velocity_at_point] using hr

theorem horizon_einstein_reconstruction (U : Set Coordinate4) (hU : IsOpen U)
    (hconn : IsPreconnected U) (E D T : TensorField4) (eta : ℝ) (heta : eta≠0)
    (hED : ∀ x∈U, E x*D x=1) (hDE : ∀ x∈U, D x*E x=1)
    (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (frameLeviCivita E D) T x j=0)
    (pencils : ∀ x∈U, ∀ v, tensorQuad (frameMetricField E x) v=0 →
      Nonempty (LocalHorizonPencil U (frameMetricField E) (frameLeviCivita E D) T eta x v)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor E D x+cosmological • frameMetricField E x=(2*Real.pi/eta) • T x := by
  have hG := levi_civita_field_smooth U hU (frameMetricField E) (inverseFrameMetricField D)
    (frame_metric_smooth U E hE) (inverse_frame_metric_smooth U D hD)
  have ht := levi_civita_field_torsion_free U hU (frameMetricField E) (inverseFrameMetricField D)
    (fun x _ => frame_metric_symmetric E x)
  apply geometric_einstein_equation_from_ricci_null_balance U hU hconn E D T (2*Real.pi/eta)
    hED hDE hE hD hT hsT
  · intro x hx v hv
    obtain ⟨P⟩ := pencils x hx v hv
    have hr := pencil_ricci_balance U hU (frameMetricField E) (frameLeviCivita E D) T
      eta heta hG hT x v (ht x hx) P
    rw [tensorQuad_sub_smul,hr]
    ring
  · exact hdT

theorem entropy_density_einstein_coefficient (newton : ℝ) (hG : newton≠0) :
    2*Real.pi/((4*newton)⁻¹)=8*Real.pi*newton := by
  field_simp
  ring

#print axioms tensor_quad_field_continuous
#print axioms pencil_ricci_balance
#print axioms horizon_einstein_reconstruction
#print axioms entropy_density_einstein_coefficient
end
end ChatgptAudit
