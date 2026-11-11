-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_012 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.GeometricScreenTransport
import TGLExt.HorizonEinsteinReconstruction

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

def inducedArea (g : TensorField4) (curve : ℝ → Coordinate4) (S : ℝ → ScreenVectors) : ℝ → ℝ :=
  fun t => screenArea (screenGram (g (curve t)) (S t))

structure NullScreenAt (g B : Tensor4) (v : Coordinate4) (S : ScreenVectors) where
  frame : Tensor4
  inverse : Tensor4
  metric : ScreenMatrix
  right_inverse : frame*inverse=1
  gram : frameᵀ*g*frame=nullScreenGram metric
  first_column : ∀ a, frame a 0=v a
  columns : S=screenColumns frame
  first_screen_negative : metric 0 0 < 0
  determinant_positive : 0 < metric.det
  preserves_null_pairing : (frameᵀ*g*B*frame) 0 1=0

structure GeometricScreenAlong (g : TensorField4) (Gamma : ConnectionField4)
    (V : VectorField4) (curve : ℝ → Coordinate4) where
  vectors : ℝ → ScreenVectors
  continuous_zero : ∀ a i, ContinuousAt (fun t => vectors t a i) 0
  curve_tangent : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt curve (V (curve t)) t
  frames : ∀ᶠ t in 𝓝[<] (0:ℝ), Nonempty
    (NullScreenAt (g (curve t)) (covariantVectorGradient Gamma V (curve t))
      (V (curve t)) (vectors t))
  transport : ∀ᶠ t in 𝓝[<] (0:ℝ), HasMatrixDerivAt vectors
    ((covariantVectorGradient Gamma V (curve t)-connectionAlong Gamma (curve t) (V (curve t)))*vectors t) t

structure GeometricHorizonPencil (U : Set Coordinate4) (g : TensorField4)
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
  screen : GeometricScreenAlong g Gamma velocity curve
  area_positive_zero : 0<(screenGram (g x) (screen.vectors 0)).det
  heat : ℝ → ℝ
  heat_continuous : ContinuousAt heat 0
  heat_zero : heat 0=0
  heat_rate : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt heat
    (-rate*t*tensorQuad (T (curve t)) (velocity (curve t))*inducedArea g curve screen.vectors t) t
  clausius_to_second_order : Tendsto
    (fun t => horizonBalancePrimitive rate eta (inducedArea g curve screen.vectors) heat t/t^2)
      (𝓝[<] 0) (𝓝 0)

theorem null_screen_geodesic_column (g B : Tensor4) (v : Coordinate4) (S : ScreenVectors)
    (F : NullScreenAt g B v S) (ha : B.mulVec v=0) :
    ∀ a, (B*F.frame) a 0=0 := by
  intro a
  rw [Matrix.mul_apply]
  simp only [F.first_column]
  exact congrArg (fun w : Coordinate4 => w a) ha

theorem induced_area_continuous (g : TensorField4) (curve : ℝ → Coordinate4)
    (S : ℝ → ScreenVectors) (t : ℝ)
    (hg : ∀ a b, ContinuousAt (fun s => g (curve s) a b) t)
    (hS : ∀ a i, ContinuousAt (fun s => S s a i) t) :
    ContinuousAt (inducedArea g curve S) t := by
  have hcol (i : Fin 4) (a : Fin 2) :
      ContinuousAt (fun s => ((S s)ᵀ*g (curve s)) a i) t := by
    simp only [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
    exact ((((hS 0 a).mul (hg 0 i)).add ((hS 1 a).mul (hg 1 i))).add
      ((hS 2 a).mul (hg 2 i))).add ((hS 3 a).mul (hg 3 i))
  have hgram (a b : Fin 2) :
      ContinuousAt (fun s => screenGram (g (curve s)) (S s) a b) t := by
    change ContinuousAt (fun s => ∑ i, ((S s)ᵀ*g (curve s)) a i*S s i b) t
    simp only [Fin.sum_univ_four]
    exact ((((hcol 0 a).mul (hS 0 b)).add ((hcol 1 a).mul (hS 1 b))).add
      ((hcol 2 a).mul (hS 2 b))).add ((hcol 3 a).mul (hS 3 b))
  unfold inducedArea screenArea
  apply Real.continuous_sqrt.continuousAt.comp
  simp only [Matrix.det_fin_two]
  exact ((hgram 0 0).mul (hgram 1 1)).sub ((hgram 0 1).mul (hgram 1 0))

theorem geometric_pencil_area_continuous (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (T : TensorField4) (eta : ℝ)
    (hg : SmoothMatrixOn U g) (x v : Coordinate4)
    (P : GeometricHorizonPencil U g Gamma T eta x v) :
    ContinuousAt (inducedArea g P.curve P.screen.vectors) 0 := by
  apply induced_area_continuous g P.curve P.screen.vectors 0
  · intro a b
    have hd := smooth_matrix_differentiableAt U hU g hg x (P.neighborhood_subset P.point_mem) a b
    have hdc : ContinuousAt (fun y => g y a b) (P.curve 0) := by
      rw [P.curve_zero]
      exact hd.continuousAt
    exact hdc.comp P.curve_tangent.continuousAt
  · exact P.screen.continuous_zero

theorem geometric_pencil_area_rate (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (T : TensorField4) (eta : ℝ)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma) (x v : Coordinate4)
    (P : GeometricHorizonPencil U g Gamma T eta x v) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (inducedArea g P.curve P.screen.vectors)
      (vectorExpansion Gamma P.velocity (P.curve t)*inducedArea g P.curve P.screen.vectors t) t := by
  have hmem : P.neighborhood∈𝓝 (P.curve 0) := by
    rw [P.curve_zero]
    exact P.neighborhood_open.mem_nhds P.point_mem
  have hc := P.curve_tangent.continuousAt.eventually hmem
  have hmn : MetricCompatibleOn P.neighborhood g Gamma :=
    fun y hy => hm y (P.neighborhood_subset hy)
  filter_upwards [hc.filter_mono nhdsWithin_le_nhds,P.screen.curve_tangent,
    P.screen.frames,P.screen.transport] with t ht hct hf hst
  obtain ⟨F⟩ := hf
  have hk := null_screen_geodesic_column _ _ _ _ F (P.geodesic ht)
  exact coordinate_screen_area_derivative P.neighborhood g Gamma P.velocity hmn (P.curve t) ht
    (smooth_matrix_differentiableAt U hU g hg (P.curve t) (P.neighborhood_subset ht))
    P.curve t hct rfl P.screen.vectors F.inverse F.frame F.metric F.right_inverse F.gram
    F.columns F.determinant_positive hk F.preserves_null_pairing hst

def geometricHorizonToLocal (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (T : TensorField4) (eta : ℝ)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma) (x v : Coordinate4)
    (P : GeometricHorizonPencil U g Gamma T eta x v) :
    LocalHorizonPencil U g Gamma T eta x v where
  neighborhood := P.neighborhood
  neighborhood_open := P.neighborhood_open
  neighborhood_subset := P.neighborhood_subset
  point_mem := P.point_mem
  velocity := P.velocity
  velocity_smooth := P.velocity_smooth
  velocity_at_point := P.velocity_at_point
  velocity_null := P.velocity_null
  geodesic := P.geodesic
  equilibrium_gradient := P.equilibrium_gradient
  curve := P.curve
  curve_zero := P.curve_zero
  curve_tangent := P.curve_tangent
  rate := P.rate
  rate_nonzero := P.rate_nonzero
  area := inducedArea g P.curve P.screen.vectors
  area_continuous := geometric_pencil_area_continuous U hU g Gamma T eta hg x v P
  area_nonzero := by
    unfold inducedArea
    rw [P.curve_zero]
    exact ne_of_gt (screen_area_positive _ P.area_positive_zero)
  heat := P.heat
  heat_continuous := P.heat_continuous
  heat_zero := P.heat_zero
  area_rate := geometric_pencil_area_rate U hU g Gamma T eta hg hm x v P
  heat_rate := P.heat_rate
  clausius_to_second_order := P.clausius_to_second_order

theorem geometric_area_einstein_reconstruction (U : Set Coordinate4) (hU : IsOpen U)
    (hconn : IsPreconnected U) (E D T : TensorField4) (eta : ℝ) (heta : eta≠0)
    (hED : ∀ x∈U, E x*D x=1) (hDE : ∀ x∈U, D x*E x=1)
    (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (frameLeviCivita E D) T x j=0)
    (pencils : ∀ x∈U, ∀ v, v≠0 → tensorQuad (frameMetricField E x) v=0 →
      Nonempty (GeometricHorizonPencil U (frameMetricField E) (frameLeviCivita E D) T eta x v)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor E D x+cosmological • frameMetricField E x=(2*Real.pi/eta) • T x := by
  let g := frameMetricField E
  let gi := inverseFrameMetricField D
  let Gamma := frameLeviCivita E D
  have hg : SmoothMatrixOn U g := frame_metric_smooth U E hE
  have hgi : SmoothMatrixOn U gi := inverse_frame_metric_smooth U D hD
  have hG : SmoothConnectionOn U Gamma := levi_civita_field_smooth U hU g gi hg hgi
  have hgs : ∀ x∈U, (g x)ᵀ=g x := fun x _ => frame_metric_symmetric E x
  have hm : MetricCompatibleOn U g Gamma := levi_civita_field_metric_compatible U hU g gi hgs
    (fun x hx => inverse_frame_metric_left E D x (hED x hx) (hDE x hx))
    (fun x hx => inverse_frame_metric_right E D x (hED x hx) (hDE x hx))
  have ht := levi_civita_field_torsion_free U hU g gi hgs
  apply geometric_einstein_equation_from_ricci_null_balance U hU hconn E D T (2*Real.pi/eta)
    hED hDE hE hD hT hsT
  · intro x hx v hv
    by_cases hz : v=0
    · subst v
      simp [tensorQuad,Matrix.mulVec,dotProduct]
    · obtain ⟨P⟩ := pencils x hx v hz hv
      have hr := pencil_ricci_balance U hU g Gamma T eta heta hG hT x v (ht x hx)
        (geometricHorizonToLocal U hU g Gamma T eta hg hm x v P)
      rw [tensorQuad_sub_smul,hr]
      ring
  · exact hdT

#print axioms null_screen_geodesic_column
#print axioms induced_area_continuous
#print axioms geometric_pencil_area_continuous
#print axioms geometric_pencil_area_rate
#print axioms geometricHorizonToLocal
#print axioms geometric_area_einstein_reconstruction
end
end ChatgptAudit
