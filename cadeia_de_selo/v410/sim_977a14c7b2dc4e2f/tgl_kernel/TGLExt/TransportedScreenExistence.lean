-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ScreenPairTransport
import TGLExt.ScreenFrameCompletion

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen014
open Matrix Filter Topology Set
open scoped Matrix.Norms.Elementwise
noncomputable section

def frameWithVelocity (v : Coordinate4) (F : Tensor4) : Tensor4 :=
  fun a => ![v a,F a 1,F a 2,F a 3]

theorem velocity_frame_first (v : Coordinate4) (F : Tensor4) :
    ∀ a, frameWithVelocity v F a 0=v a := fun _ => rfl

theorem velocity_frame_screen (v : Coordinate4) (F : Tensor4) :
    screenColumns (frameWithVelocity v F)=screenColumns F := by
  ext a i
  fin_cases i <;> rfl

theorem screen_gram_symmetric (g : Tensor4) (hg : gᵀ=g) (S : ScreenVectors) :
    (screenGram g S)ᵀ=screenGram g S := by
  simp only [screenGram,Matrix.transpose_mul,Matrix.transpose_transpose,hg,Matrix.mul_assoc]

theorem screen_gram_continuous_components (g : ℝ → Tensor4) (S : ℝ → ScreenVectors) (t : ℝ)
    (hg : ∀ a b, ContinuousAt (fun s => g s a b) t)
    (hS : ∀ a i, ContinuousAt (fun s => S s a i) t) :
    ∀ i j, ContinuousAt (fun s => screenGram (g s) (S s) i j) t := by
  have hcol (i : Fin 4) (a : Fin 2) :
      ContinuousAt (fun s => ((S s)ᵀ*g s) a i) t := by
    simp only [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
    exact ((((hS 0 a).mul (hg 0 i)).add ((hS 1 a).mul (hg 1 i))).add
      ((hS 2 a).mul (hg 2 i))).add ((hS 3 a).mul (hg 3 i))
  intro a b
  change ContinuousAt (fun s => ∑ i, ((S s)ᵀ*g s) a i*S s i b) t
  simp only [Fin.sum_univ_four]
  exact ((((hcol 0 a).mul (hS 0 b)).add ((hcol 1 a).mul (hS 1 b))).add
    ((hcol 2 a).mul (hS 2 b))).add ((hcol 3 a).mul (hS 3 b))

theorem normalized_initial_pair (g : Tensor4) (v : Coordinate4)
    (F : Screen013.NormalizedNullFrame g v) (j : Fin 4) :
    tensorPair g v (fun a => F.frame a j)=(nullScreenGram (-1)) 0 j := by
  have h := congrArg (fun M : Tensor4 => M 0 j) F.gram
  rw [frame_pair_entry] at h
  have hv : (fun a => F.frame a 0)=v := funext F.first_column
  rwa [hv] at h

theorem flow_raw_gram_row (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ y∈U, (g y)ᵀ=g y)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (F : Screen013.NormalizedNullFrame (g x) (V x))
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F.frame)
    (t : ℝ) (ht : t∈Ioo (-P.radius) P.radius) :
    ∀ j, ((frameWithVelocity (V (P.curve t)) (P.frame t))ᵀ*g (P.curve t)*
      frameWithVelocity (V (P.curve t)) (P.frame t)) 0 j=(nullScreenGram (-1)) 0 j := by
  have hp (j : Fin 4) := (frame_flow_pair_preserved U hU g Gamma V hm hgs hg hV hn hgeo
    x F.frame P j t ht).trans (normalized_initial_pair (g x) (V x) F j)
  intro j
  rw [frame_pair_entry]
  fin_cases j
  · change tensorQuad (g (P.curve t)) (V (P.curve t))=0
    exact hn _ (P.curve_mem t ht)
  · exact hp 1
  · exact hp 2
  · exact hp 3

def flowScreenCertificate (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ y∈U, (g y)ᵀ=g y)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (F : Screen013.NormalizedNullFrame (g x) (V x))
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F.frame)
    (t : ℝ) (ht : t∈Ioo (-P.radius) P.radius)
    (hnegative : screenGram (g (P.curve t)) (screenColumns (P.frame t)) 0 0 < 0)
    (hdet : 0 < (screenGram (g (P.curve t)) (screenColumns (P.frame t))).det) :
    NullScreenAt (g (P.curve t)) (covariantVectorGradient Gamma V (P.curve t))
      (V (P.curve t)) (screenColumns (P.frame t)) := by
  let Ft := frameWithVelocity (V (P.curve t)) (P.frame t)
  let G := Ftᵀ*g (P.curve t)*Ft
  let h := screenGram (g (P.curve t)) (screenColumns (P.frame t))
  have hGt : Gᵀ=G := by
    simp only [G,Matrix.transpose_mul,Matrix.transpose_transpose,hgs _ (P.curve_mem t ht),Matrix.mul_assoc]
  have hh : screenBlock G=h := by
    change screenBlock (Ftᵀ*g (P.curve t)*Ft)=h
    rw [← screen_gram_in_frame,velocity_frame_screen]
  have hr := flow_raw_gram_row U hU g Gamma V hm hgs hg hV hn hgeo x F P t ht
  have hshape : G=rawScreenGram (G 1 1) (G 1 2) (G 1 3) h := by
    rw [← hh]
    exact raw_gram_shape G hGt (hr 0) (hr 1) (hr 2) (hr 3)
  have hs : hᵀ=h := screen_gram_symmetric _ (hgs _ (P.curve_mem t ht)) _
  have hcert := completedNullScreen (g (P.curve t)) (covariantVectorGradient Gamma V (P.curve t))
    (V (P.curve t)) Ft (G 1 1) (G 1 2) (G 1 3) h hs hshape
    (velocity_frame_first _ _) hnegative hdet
    (null_field_direction_pairing U hU g Gamma V hm (P.curve t) (P.curve_mem t ht)
      (hgs _ (P.curve_mem t ht))
      (smooth_matrix_differentiableAt U hU g hg _ (P.curve_mem t ht))
      (smooth_vector_differentiableAt U hU V hV _ (P.curve_mem t ht)) hn)
  rw [velocity_frame_screen] at hcert
  exact hcert

theorem flow_screen_positive_near_zero (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (x : Coordinate4) (hx : x∈U)
    (F : Screen013.NormalizedNullFrame (g x) (V x))
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F.frame) :
    ∀ᶠ t in 𝓝 (0:ℝ),
      screenGram (g (P.curve t)) (screenColumns (P.frame t)) 0 0 < 0 ∧
      0 < (screenGram (g (P.curve t)) (screenColumns (P.frame t))).det := by
  have hc := local_frame_flow_continuous_zero U V _ x F.frame P
  have hg' (a b : Fin 4) : ContinuousAt (fun s => g (P.curve s) a b) 0 := by
    have hga : ContinuousAt (fun y => g y a b) (P.curve 0) := by
      rw [P.curve_zero]
      exact (smooth_matrix_differentiableAt U hU g hg x hx a b).continuousAt
    exact hga.comp hc.1
  have hs (a : Fin 4) (i : Fin 2) :
      ContinuousAt (fun s => screenColumns (P.frame s) a i) 0 := hc.2 a (screenIndex i)
  have hh := screen_gram_continuous_components (fun s => g (P.curve s))
    (fun s => screenColumns (P.frame s)) 0 hg' hs
  have hinit : screenGram (g (P.curve 0)) (screenColumns (P.frame 0))=-1 := by
    rw [P.curve_zero,P.frame_zero,Screen013.normalized_frame_screen_gram]
  have hd : ContinuousAt (fun s => (screenGram (g (P.curve s)) (screenColumns (P.frame s))).det) 0 := by
    simp only [Matrix.det_fin_two]
    exact ((hh 0 0).mul (hh 1 1)).sub ((hh 0 1).mul (hh 1 0))
  have hneg := (hh 0 0).eventually (isOpen_Iio.mem_nhds
    (show screenGram (g (P.curve 0)) (screenColumns (P.frame 0)) 0 0 < 0 by rw [hinit]; norm_num))
  have hpos := hd.eventually (isOpen_Ioi.mem_nhds
    (show 0 < (screenGram (g (P.curve 0)) (screenColumns (P.frame 0))).det by
      rw [hinit]; norm_num [Matrix.det_fin_two]))
  filter_upwards [hneg,hpos] with t ht hp
  exact ⟨ht,hp⟩

def geometricScreenFromFlow (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ y∈U, (g y)ᵀ=g y)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (hx : x∈U) (F : Screen013.NormalizedNullFrame (g x) (V x))
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F.frame) :
    GeometricScreenAlong g Gamma V P.curve := by
  have hi0 : ∀ᶠ t in 𝓝 (0:ℝ), t∈Ioo (-P.radius) P.radius :=
    Ioo_mem_nhds (neg_neg_of_pos P.radius_positive) P.radius_positive
  have hi := hi0.filter_mono (nhdsWithin_le_nhds (s := Iio (0:ℝ)))
  have hp := (flow_screen_positive_near_zero U hU g Gamma V hg x hx F P).filter_mono (nhdsWithin_le_nhds (s := Iio (0:ℝ)))
  refine {
    vectors := fun t => screenColumns (P.frame t)
    continuous_zero := fun a i => (local_frame_flow_continuous_zero U V _ x F.frame P).2 a (screenIndex i)
    curve_tangent := ?_
    frames := ?_
    transport := ?_ }
  · filter_upwards [hi] with t ht
    exact P.tangent t ht
  · filter_upwards [hi,hp] with t ht hpos
    exact ⟨flowScreenCertificate U hU g Gamma V hm hgs hg hV hn hgeo x F P t ht hpos.1 hpos.2⟩
  · filter_upwards [hi] with t ht
    intro a i
    exact P.transport t ht a (screenIndex i)

theorem flow_screen_area_derivative_zero (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ y∈U, (g y)ᵀ=g y)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (_hx : x∈U) (F : Screen013.NormalizedNullFrame (g x) (V x))
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F.frame) :
    HasDerivAt (inducedArea g P.curve (fun t => screenColumns (P.frame t)))
      (vectorExpansion Gamma V x) 0 := by
  have h0 : (0:ℝ)∈Ioo (-P.radius) P.radius :=
    ⟨neg_neg_of_pos P.radius_positive,P.radius_positive⟩
  have hinit : screenGram (g (P.curve 0)) (screenColumns (P.frame 0))=-1 := by
    rw [P.curve_zero,P.frame_zero,Screen013.normalized_frame_screen_gram]
  have hn0 : screenGram (g (P.curve 0)) (screenColumns (P.frame 0)) 0 0 < 0 := by
    rw [hinit]; norm_num
  have hd0 : 0 < (screenGram (g (P.curve 0)) (screenColumns (P.frame 0))).det := by
    rw [hinit]; norm_num [Matrix.det_fin_two]
  have Fc := flowScreenCertificate U hU g Gamma V hm hgs hg hV hn hgeo x F P 0 h0 hn0 hd0
  have hk := null_screen_geodesic_column _ _ _ _ Fc (hgeo (P.curve_mem 0 h0))
  have htr : HasMatrixDerivAt (fun t => screenColumns (P.frame t))
      ((covariantVectorGradient Gamma V (P.curve 0)-connectionAlong Gamma (P.curve 0) (V (P.curve 0)))*
        screenColumns (P.frame 0)) 0 := fun a i => P.transport 0 h0 a (screenIndex i)
  have hd := coordinate_screen_area_derivative U g Gamma V hm (P.curve 0) (P.curve_mem 0 h0)
    (smooth_matrix_differentiableAt U hU g hg _ (P.curve_mem 0 h0))
    P.curve 0 (P.tangent 0 h0) rfl (fun t => screenColumns (P.frame t))
    Fc.inverse Fc.frame Fc.metric Fc.right_inverse Fc.gram Fc.columns Fc.determinant_positive
    hk Fc.preserves_null_pairing htr
  rw [hinit,Screen013.negative_identity_screen_area,mul_one,P.curve_zero] at hd
  exact hd

theorem geometric_screen_area_rate (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hm : MetricCompatibleOn U g Gamma)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (curve : ℝ → Coordinate4) (S : GeometricScreenAlong g Gamma V curve)
    (hmem : ∀ᶠ t in 𝓝[<] (0:ℝ), curve t∈U) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (inducedArea g curve S.vectors)
      (vectorExpansion Gamma V (curve t)*inducedArea g curve S.vectors t) t := by
  filter_upwards [hmem,S.curve_tangent,S.frames,S.transport] with t ht hc hf hs
  obtain ⟨F⟩ := hf
  have hk := null_screen_geodesic_column _ _ _ _ F (hgeo ht)
  exact coordinate_screen_area_derivative U g Gamma V hm (curve t) ht
    (smooth_matrix_differentiableAt U hU g hg (curve t) ht)
    curve t hc rfl S.vectors F.inverse F.frame F.metric F.right_inverse F.gram
    F.columns F.determinant_positive hk F.preserves_null_pairing hs

theorem local_levi_civita_transported_screen (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (V : VectorField4)
    (hED : ∀ y∈U, E y*D y=1) (hDE : ∀ y∈U, D y*E y=1)
    (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (frameMetricField E y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration (frameLeviCivita E D) V) (fun _ => 0) U)
    (x : Coordinate4) (hx : x∈U) (hv : V x≠0) :
    ∃ curve : ℝ → Coordinate4, curve 0=x ∧ HasDerivAt curve (V x) 0 ∧
      ∃ S : GeometricScreenAlong (frameMetricField E) (frameLeviCivita E D) V curve,
        screenGram (frameMetricField E x) (S.vectors 0)=-1 ∧
        ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (inducedArea (frameMetricField E) curve S.vectors)
          (vectorExpansion (frameLeviCivita E D) V (curve t)*
            inducedArea (frameMetricField E) curve S.vectors t) t := by
  let g := frameMetricField E
  let gi := inverseFrameMetricField D
  let Gamma := frameLeviCivita E D
  have hg : SmoothMatrixOn U g := frame_metric_smooth U E hE
  have hgi : SmoothMatrixOn U gi := inverse_frame_metric_smooth U D hD
  have hG : SmoothConnectionOn U Gamma := levi_civita_field_smooth U hU g gi hg hgi
  have hgs : ∀ y∈U, (g y)ᵀ=g y := fun y _ => frame_metric_symmetric E y
  have hm : MetricCompatibleOn U g Gamma := levi_civita_field_metric_compatible U hU g gi hgs
    (fun y hy => inverse_frame_metric_left E D y (hED y hy) (hDE y hy))
    (fun y hy => inverse_frame_metric_right E D y (hED y hy) (hDE y hy))
  let F := Screen013.solderedNullFrame (E x) (D x) (hED x hx) (hDE x hx) (V x) hv (hn x hx)
  let P := localFrameFlow U hU V (transportGenerator Gamma V) hV
    (transport_generator_smooth U hU Gamma V hG hV) x hx F.frame
  let S := geometricScreenFromFlow U hU g Gamma V hm hgs hg hV hn hgeo x hx F P
  have h0 : (0:ℝ)∈Ioo (-P.radius) P.radius :=
    ⟨neg_neg_of_pos P.radius_positive,P.radius_positive⟩
  have hc0 : HasDerivAt P.curve (V x) 0 := by
    have hd := P.tangent 0 h0
    rwa [P.curve_zero] at hd
  have hinit : screenGram (g x) (S.vectors 0)=-1 := by
    change screenGram (g x) (screenColumns (P.frame 0))=-1
    rw [P.frame_zero,Screen013.normalized_frame_screen_gram]
  have hmem : ∀ᶠ t in 𝓝[<] (0:ℝ), P.curve t∈U := by
    have hi0 : ∀ᶠ t in 𝓝 (0:ℝ), t∈Ioo (-P.radius) P.radius := Ioo_mem_nhds h0.1 h0.2
    have hi := hi0.filter_mono (nhdsWithin_le_nhds (s := Iio (0:ℝ)))
    filter_upwards [hi] with t ht
    exact P.curve_mem t ht
  exact ⟨P.curve,P.curve_zero,hc0,S,hinit,
    geometric_screen_area_rate U hU g Gamma V hg hm hgeo P.curve S hmem⟩

#print axioms velocity_frame_first
#print axioms velocity_frame_screen
#print axioms screen_gram_symmetric
#print axioms screen_gram_continuous_components
#print axioms normalized_initial_pair
#print axioms flow_raw_gram_row
#print axioms flowScreenCertificate
#print axioms flow_screen_positive_near_zero
#print axioms geometricScreenFromFlow
#print axioms flow_screen_area_derivative_zero
#print axioms geometric_screen_area_rate
#print axioms local_levi_civita_transported_screen
end
end ChatgptAudit.Screen014
