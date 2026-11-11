-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_009 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ContractedBianchi
import TGLExt.GeneralTensorReconstruction

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

theorem inverse_metric_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv)
    (hm : MetricCompatibleOn U g Gamma)
    (hl : ∀ x∈U, gInv x*g x=1) (hr : ∀ x∈U, g x*gInv x=1)
    (x : Coordinate4) (hx : x∈U) (k : Fin 4) :
    tensorFieldJet gInv x k= -Gamma x k*gInv x-gInv x*(Gamma x k)ᵀ := by
  have heq : Set.EqOn (fun y => gInv y*g y) (fun _ => 1) U := by
    intro y hy
    exact hl y hy
  have he := congrArg (fun J => J k) (tensorFieldJet_congr_on U hU _ _ heq x hx)
  rw [tensorFieldJet_mul _ _ x (smooth_matrix_differentiableAt U hU gInv hgi x hx)
    (smooth_matrix_differentiableAt U hU g hg x hx)] at he
  have hz : tensorFieldJet (fun _ => (1 : Matrix (Fin 4) (Fin 4) ℝ)) x k=0 := by
    ext a b
    simp [tensorFieldJet,coordinatePartial]
  rw [hz,metric_compatibility_formula U g Gamma hm x hx k] at he
  have he' := congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A*gInv x) he
  have hre : (tensorFieldJet gInv x k*g x+gInv x*((Gamma x k)ᵀ*g x+g x*Gamma x k))*gInv x =
      tensorFieldJet gInv x k+gInv x*(Gamma x k)ᵀ+Gamma x k*gInv x := by
    calc
      _ = tensorFieldJet gInv x k*(g x*gInv x)+
          (gInv x*(Gamma x k)ᵀ)*(g x*gInv x)+(gInv x*g x)*Gamma x k*gInv x := by noncomm_ring
      _ = _ := by rw [hl x hx,hr x hx,mul_one,mul_one,one_mul]
  rw [hre,zero_mul] at he'
  apply sub_eq_zero.mp
  calc
    tensorFieldJet gInv x k-(-Gamma x k*gInv x-gInv x*(Gamma x k)ᵀ) =
        tensorFieldJet gInv x k+gInv x*(Gamma x k)ᵀ+Gamma x k*gInv x := by rw [neg_mul]; abel
    _ = 0 := he'

theorem coordinatePartial_trace (A : TensorField4) (x : Coordinate4)
    (hA : ∀ i j, DifferentiableAt ℝ (fun y => A y i j) x) (k : Fin 4) :
    coordinatePartial (fun y => Matrix.trace (A y)) x k=Matrix.trace (tensorFieldJet A x k) :=
  coordinatePartial_sum (fun i y => A y i i) x (fun i => hA i i) k

theorem matrix_contraction_eq_trace (A B : Matrix (Fin 4) (Fin 4) ℝ) (hA : Aᵀ=A) :
    (∑ i, ∑ j, A i j*B i j)=Matrix.trace (A*B) := by
  change (∑ i, ∑ j, A i j*B i j)=∑ i, ∑ j, A i j*B j i
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  have he : A j i=A i j := congrArg (fun C : Matrix (Fin 4) (Fin 4) ℝ => C i j) hA
  rw [he]

theorem scalar_curvature_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (gInv : TensorField4) (Gamma : ConnectionField4)
    (hgi : SmoothMatrixOn U gInv) (hG : SmoothConnectionOn U Gamma) :
    ContDiffOn ℝ ∞ (coordinateScalarCurvature gInv Gamma) U := by
  have hR := coordinate_ricci_smooth U hU Gamma hG
  unfold SmoothMatrixOn at hgi hR
  unfold coordinateScalarCurvature
  fun_prop

theorem scalar_curvature_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hl : ∀ x∈U, gInv x*g x=1) (hr : ∀ x∈U, g x*gInv x=1)
    (x : Coordinate4) (hx : x∈U) (k : Fin 4) :
    coordinatePartial (coordinateScalarCurvature gInv Gamma) x k =
      Matrix.trace (gInv x*covariantTensorJet (coordinateRicci Gamma x)
        (tensorFieldJet (coordinateRicci Gamma) x) (Gamma x) k) := by
  have heq : coordinateScalarCurvature gInv Gamma =ᶠ[𝓝 x]
      (fun y => Matrix.trace (gInv y*coordinateRicci Gamma y)) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact matrix_contraction_eq_trace (gInv y) (coordinateRicci Gamma y)
      (inverse_symmetric_of_symmetric (g y) (gInv y) (hs y hy) (hl y hy))
  have hp : coordinatePartial (coordinateScalarCurvature gInv Gamma) x k=
      coordinatePartial (fun y => Matrix.trace (gInv y*coordinateRicci Gamma y)) x k :=
    congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single k 1)) heq.fderiv_eq
  rw [hp,coordinatePartial_trace _ x
    (smooth_matrix_differentiableAt U hU _ (SmoothMatrixOn.mul U _ _ hgi
      (coordinate_ricci_smooth U hU Gamma hG)) x hx) k,
    tensorFieldJet_mul _ _ x (smooth_matrix_differentiableAt U hU gInv hgi x hx)
      (smooth_matrix_differentiableAt U hU _ (coordinate_ricci_smooth U hU Gamma hG) x hx),
    inverse_metric_derivative U hU g gInv Gamma hg hgi hm hl hr x hx k]
  simp only [covariantTensorJet,Matrix.sub_mul,Matrix.neg_mul,Matrix.mul_sub,
    Matrix.trace_add,Matrix.trace_sub,Matrix.trace_neg]
  rw [← Matrix.trace_mul_cycle (gInv x) (coordinateRicci Gamma x) (Gamma x k)]
  simp only [Matrix.mul_assoc]
  abel

theorem geometric_contracted_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (hl : ∀ x∈U, gInv x*g x=1) (hr : ∀ x∈U, g x*gInv x=1)
    (x : Coordinate4) (hx : x∈U) (j : Fin 4) :
    2*tensorFieldDivergence gInv Gamma (coordinateRicci Gamma) x j=
      coordinatePartial (coordinateScalarCurvature gInv Gamma) x j := by
  have he := contracted_bianchi_algebra (gInv x) (lowerCovariantCurvatureDerivative g Gamma x)
    (lower_covariant_first_skew U hU g Gamma hg hG hm hs x hx)
    (lower_covariant_last_skew g Gamma x)
    (lower_second_bianchi U hU g Gamma hG ht x hx) j
  have hR := lower_covariant_ricci_contraction U hU g gInv Gamma hG x hx (hl x hx)
  simp only [← hR] at he
  rw [scalar_curvature_derivative U hU g gInv Gamma hg hgi hG hm hs hl hr x hx j]
  simpa only [tensorFieldDivergence,tensorJetDivergence,Matrix.trace,Matrix.diag,Matrix.mul_apply] using he

theorem geometric_einstein_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) (hG : SmoothConnectionOn U Gamma) :
    SmoothMatrixOn U (geometricEinsteinTensor g gInv Gamma) := by
  intro i j
  exact (coordinate_ricci_smooth U hU Gamma hG i j).sub
    (((scalar_curvature_smooth U hU gInv Gamma hgi hG).div_const 2).mul (hg i j))

theorem geometric_einstein_conserved (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (hl : ∀ x∈U, gInv x*g x=1) (hr : ∀ x∈U, g x*gInv x=1)
    (x : Coordinate4) (hx : x∈U) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (geometricEinsteinTensor g gInv Gamma) x j=0 := by
  have hS : DifferentiableAt ℝ (coordinateScalarCurvature gInv Gamma) x :=
    ((scalar_curvature_smooth U hU gInv Gamma hgi hG).differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)
  have hf : DifferentiableAt ℝ (fun y => coordinateScalarCurvature gInv Gamma y/2) x :=
    (((scalar_curvature_smooth U hU gInv Gamma hgi hG).div_const (2:ℝ)).differentiableOn
      (by simp)).differentiableAt (hU.mem_nhds hx)
  have hga := smooth_matrix_differentiableAt U hU g hg x hx
  have hRa := smooth_matrix_differentiableAt U hU _ (coordinate_ricci_smooth U hU Gamma hG) x hx
  have hp : coordinatePartial (fun y => coordinateScalarCurvature gInv Gamma y/2) x j =
      coordinatePartial (coordinateScalarCurvature gInv Gamma) x j/2 := by
    simp only [div_eq_mul_inv]
    rw [coordinatePartial_mul (coordinateScalarCurvature gInv Gamma) (fun _ => (2:ℝ)⁻¹) x hS
      (differentiableAt_const _) j]
    simp [coordinatePartial]
  change tensorFieldDivergence gInv Gamma
    (fun y => coordinateRicci Gamma y-(coordinateScalarCurvature gInv Gamma y/2) • g y) x j=0
  rw [tensorFieldDivergence_sub gInv Gamma (coordinateRicci Gamma)
    (fun y => (coordinateScalarCurvature gInv Gamma y/2) • g y) x hRa (fun a b => hf.mul (hga a b)) j,
    pure_trace_field_divergence g gInv Gamma (fun y => coordinateScalarCurvature gInv Gamma y/2)
      x hf hga (hl x hx) (hm x hx) j,hp]
  linarith [geometric_contracted_bianchi U hU g gInv Gamma hg hgi hG hm hs ht hl hr x hx j]


def frameLeviCivita (E D : TensorField4) : ConnectionField4 :=
  leviCivitaField (frameMetricField E) (inverseFrameMetricField D)

def frameEinsteinTensor (E D : TensorField4) : TensorField4 :=
  geometricEinsteinTensor (frameMetricField E) (inverseFrameMetricField D) (frameLeviCivita E D)

theorem frame_metric_smooth (U : Set Coordinate4) (E : TensorField4) (hE : SmoothMatrixOn U E) :
    SmoothMatrixOn U (frameMetricField E) := by
  have hEta : SmoothMatrixOn U (fun _ => TGLExt.eta4) := by
    intro i j
    exact contDiffOn_const
  exact SmoothMatrixOn.mul U _ _
    (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U E hE) hEta) hE

theorem inverse_frame_metric_smooth (U : Set Coordinate4) (D : TensorField4) (hD : SmoothMatrixOn U D) :
    SmoothMatrixOn U (inverseFrameMetricField D) := by
  have hEta : SmoothMatrixOn U (fun _ => TGLExt.eta4) := by
    intro i j
    exact contDiffOn_const
  exact SmoothMatrixOn.mul U _ _
    (SmoothMatrixOn.mul U _ _ hD hEta) (SmoothMatrixOn.transpose U D hD)

theorem levi_civita_field_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) :
    SmoothConnectionOn U (leviCivitaField g gInv) := by
  have hd : ∀ k a b, ContDiffOn ℝ ∞ (fun y => tensorFieldJet g y k a b) U :=
    fun k => tensorFieldJet_smooth U hU g hg k
  intro i a b
  unfold leviCivitaField leviCivitaJet
  simp only [Matrix.mul_apply,lowerChristoffelJet]
  unfold SmoothMatrixOn at hgi
  fun_prop

theorem tensorQuad_sub_smul (A B : Tensor4) (c : ℝ) (v : SpacetimeVector) :
    tensorQuad (A-c • B) v=tensorQuad A v-c*tensorQuad B v := by
  simp only [tensorQuad,Matrix.sub_mulVec,Matrix.smul_mulVec,dotProduct_sub,dotProduct_smul,smul_eq_mul]

theorem geometric_einstein_equation_from_ricci_null_balance
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (E D T : TensorField4) (coupling : ℝ)
    (hED : ∀ x∈U, E x*D x=1) (hDE : ∀ x∈U, D x*E x=1)
    (hE : SmoothMatrixOn U E) (hD : SmoothMatrixOn U D)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (frameMetricField E x) v=0 →
      tensorQuad (coordinateRicci (frameLeviCivita E D) x-coupling • T x) v=0)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (frameLeviCivita E D) T x j=0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor E D x+cosmological • frameMetricField E x=coupling • T x := by
  let g := frameMetricField E
  let gi := inverseFrameMetricField D
  let Gamma := frameLeviCivita E D
  have hg : SmoothMatrixOn U g := frame_metric_smooth U E hE
  have hgi : SmoothMatrixOn U gi := inverse_frame_metric_smooth U D hD
  have hG : SmoothConnectionOn U Gamma := levi_civita_field_smooth U hU g gi hg hgi
  have hgs : ∀ x∈U, (g x)ᵀ=g x := fun x _ => frame_metric_symmetric E x
  have hl : ∀ x∈U, gi x*g x=1 := fun x hx => inverse_frame_metric_left E D x (hED x hx) (hDE x hx)
  have hr : ∀ x∈U, g x*gi x=1 := fun x hx => inverse_frame_metric_right E D x (hED x hx) (hDE x hx)
  have hm : MetricCompatibleOn U g Gamma := levi_civita_field_metric_compatible U hU g gi hgs hl hr
  have ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i :=
    levi_civita_field_torsion_free U hU g gi hgs
  have hEin : ∀ i j, DifferentiableOn ℝ (fun x => frameEinsteinTensor E D x i j) U :=
    fun i j => (geometric_einstein_smooth U hU g gi Gamma hg hgi hG i j).differentiableOn (by simp)
  have hsEin : ∀ x∈U, (frameEinsteinTensor E D x)ᵀ=frameEinsteinTensor E D x :=
    fun x hx => geometric_einstein_symmetric U hU g gi Gamma hg hG hm ht x hx (hgs x hx) (hl x hx)
  have hdEin : ∀ x∈U, ∀ j, tensorFieldDivergence gi Gamma (frameEinsteinTensor E D) x j=0 :=
    fun x hx j => geometric_einstein_conserved U hU g gi Gamma hg hgi hG hm hgs ht hl hr x hx j
  have hnEin : ∀ x∈U, ∀ v, tensorQuad (frameMetricField E x) v=0 →
      tensorQuad (frameEinsteinTensor E D x-coupling • T x) v=0 := by
    intro x hx v hv
    have he : frameEinsteinTensor E D x-coupling • T x =
        (coordinateRicci Gamma x-coupling • T x)-
          (coordinateScalarCurvature gi Gamma x/2) • g x := by
      unfold frameEinsteinTensor geometricEinsteinTensor
      change (coordinateRicci Gamma x-(coordinateScalarCurvature gi Gamma x/2) • g x)-coupling • T x = _
      abel
    rw [he,tensorQuad_sub_smul]
    change tensorQuad (coordinateRicci Gamma x-coupling • T x) v-
      (coordinateScalarCurvature gi Gamma x/2)*tensorQuad (frameMetricField E x) v=0
    rw [hv,mul_zero,sub_zero]
    exact hn x hx v hv
  exact conserved_null_balance_has_constant_term U hU hconn E D (frameEinsteinTensor E D) T coupling
    hED hDE (fun i j => (hE i j).differentiableOn (by simp))
    (fun i j => (hD i j).differentiableOn (by simp)) hEin hT hsEin hsT hnEin hdEin hdT

#print axioms frameLeviCivita
#print axioms frameEinsteinTensor
#print axioms frame_metric_smooth
#print axioms inverse_frame_metric_smooth
#print axioms levi_civita_field_smooth
#print axioms tensorQuad_sub_smul
#print axioms geometric_einstein_equation_from_ricci_null_balance

#print axioms inverse_metric_derivative
#print axioms coordinatePartial_trace
#print axioms matrix_contraction_eq_trace
#print axioms scalar_curvature_smooth
#print axioms scalar_curvature_derivative
#print axioms geometric_contracted_bianchi
#print axioms geometric_einstein_smooth
#print axioms geometric_einstein_conserved
end
end ChatgptAudit
