-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_023 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.CovectorStressCalculus

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Coherent023
open Matrix Filter Topology Set
open scoped ContDiff
noncomputable section

def ClosedCovectorOn (U : Set Coordinate4) (w : CovectorField4) : Prop :=
  ∀ x∈U, ∀ i j, coordinatePartial (fun y => w y j) x i=coordinatePartial (fun y => w y i) x j

def CovectorWaveOn (U : Set Coordinate4) (gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) : Prop := ∀ x∈U, covectorDivergence gInv Gamma w x=0

def potentialCovector (potential : Coordinate4 → ℝ) : CovectorField4 :=
  fun x i => coordinatePartial potential x i

theorem covector_stress_divergence_point (g gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (coupling : ℝ) (x : Coordinate4)
    (hg : ∀ i j, DifferentiableAt ℝ (fun y => g y i j) x)
    (hgi : ∀ i j, DifferentiableAt ℝ (fun y => gInv y i j) x)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x)
    (hl : gInv x*g x=1) (hs : (gInv x)ᵀ=gInv x)
    (hm : ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0)
    (hd : ∀ i, tensorFieldJet gInv x i= -Gamma x i*gInv x-gInv x*(Gamma x i)ᵀ) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (covectorStressField g gInv w coupling) x j=
      coupling*(covectorDivergence gInv Gamma w x*w x j+
        ∑ i, ∑ k, gInv x i k*w x k*(covectorDerivative Gamma w x i j-covectorDerivative Gamma w x j i)) := by
  have hq := covector_squared_differentiable gInv w x hgi hw
  have hhalf : DifferentiableAt ℝ (fun y => tensorQuad (gInv y) (w y)/2) x := by
    have he : (fun y => tensorQuad (gInv y) (w y)/2)=
        (fun y => (1/2:ℝ)*tensorQuad (gInv y) (w y)) := by
      funext y
      ring
    rw [he]
    exact hq.const_mul (1/2:ℝ)
  have ho : ∀ i k, DifferentiableAt ℝ (fun y => Matrix.vecMulVec (w y) (w y) i k) x :=
    fun i k => (hw i).mul (hw k)
  have ht : ∀ i k, DifferentiableAt ℝ
      (fun y => (Matrix.vecMulVec (w y) (w y)-(tensorQuad (gInv y) (w y)/2) • g y) i k) x :=
    fun i k => (ho i k).sub (hhalf.mul (hg i k))
  change tensorFieldDivergence gInv Gamma
    (fun y => coupling • (Matrix.vecMulVec (w y) (w y)-(tensorQuad (gInv y) (w y)/2) • g y)) x j=_
  rw [tensorFieldDivergence_const_smul gInv Gamma coupling _ x ht j,
    tensorFieldDivergence_sub gInv Gamma (fun y => Matrix.vecMulVec (w y) (w y))
      (fun y => (tensorQuad (gInv y) (w y)/2) • g y) x ho (fun i k => hhalf.mul (hg i k)) j,
    outer_field_divergence gInv Gamma w x hw j,
    pure_trace_field_divergence g gInv Gamma (fun y => tensorQuad (gInv y) (w y)/2) x
      hhalf hg hl hm j,
    coordinate_partial_half _ x hq j,
    covector_squared_derivative gInv Gamma w x hgi hw hs j (hd j)]
  simp only [mul_sub,Finset.sum_sub_distrib]
  ring

theorem covector_derivative_symmetric (Gamma : ConnectionField4) (w : CovectorField4) (x : Coordinate4)
    (hclosed : ∀ i j, coordinatePartial (fun y => w y j) x i=coordinatePartial (fun y => w y i) x j)
    (ht : ∀ i j k, Gamma x i k j=Gamma x j k i) (i j : Fin 4) :
    covectorDerivative Gamma w x i j=covectorDerivative Gamma w x j i := by
  simp only [covectorDerivative,vectorPartial,Pi.sub_apply,Matrix.mulVec,dotProduct,Matrix.transpose_apply]
  rw [hclosed i j]
  congr 1
  apply Finset.sum_congr rfl
  intro k _
  rw [ht i j k]

theorem covector_stress_divergence_closed (g gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (coupling : ℝ) (x : Coordinate4)
    (hg : ∀ i j, DifferentiableAt ℝ (fun y => g y i j) x)
    (hgi : ∀ i j, DifferentiableAt ℝ (fun y => gInv y i j) x)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x)
    (hl : gInv x*g x=1) (hs : (gInv x)ᵀ=gInv x)
    (hm : ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0)
    (hd : ∀ i, tensorFieldJet gInv x i= -Gamma x i*gInv x-gInv x*(Gamma x i)ᵀ)
    (hW : ∀ i j, covectorDerivative Gamma w x i j=covectorDerivative Gamma w x j i) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (covectorStressField g gInv w coupling) x j=
      coupling*(covectorDivergence gInv Gamma w x*w x j) := by
  have hh := covector_stress_divergence_point g gInv Gamma w coupling x hg hgi hw hl hs hm hd j
  have hz : (∑ i, ∑ k, gInv x i k*w x k*
      (covectorDerivative Gamma w x i j-covectorDerivative Gamma w x j i))=0 := by
    apply Finset.sum_eq_zero
    intro i _
    apply Finset.sum_eq_zero
    intro k _
    rw [hW i j,sub_self,mul_zero]
  simpa only [hz,add_zero] using hh

theorem covector_stress_conservation_iff_wave_at (g gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (coupling : ℝ) (x : Coordinate4)
    (hg : ∀ i j, DifferentiableAt ℝ (fun y => g y i j) x)
    (hgi : ∀ i j, DifferentiableAt ℝ (fun y => gInv y i j) x)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x)
    (hl : gInv x*g x=1) (hs : (gInv x)ᵀ=gInv x)
    (hm : ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0)
    (hd : ∀ i, tensorFieldJet gInv x i= -Gamma x i*gInv x-gInv x*(Gamma x i)ᵀ)
    (hW : ∀ i j, covectorDerivative Gamma w x i j=covectorDerivative Gamma w x j i)
    (hc : coupling≠0) (hw0 : w x≠0) :
    (∀ j, tensorFieldDivergence gInv Gamma (covectorStressField g gInv w coupling) x j=0) ↔
      covectorDivergence gInv Gamma w x=0 := by
  constructor
  · intro hh
    by_contra hn
    apply hw0
    funext j
    have hj := hh j
    rw [covector_stress_divergence_closed g gInv Gamma w coupling x hg hgi hw hl hs hm hd hW j] at hj
    exact (mul_eq_zero.mp ((mul_eq_zero.mp hj).resolve_left hc)).resolve_left hn
  · intro hh j
    rw [covector_stress_divergence_closed g gInv Gamma w coupling x hg hgi hw hl hs hm hd hW j,
      hh,zero_mul,mul_zero]

theorem covector_stress_conserved_on (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4) (w : CovectorField4) (coupling : ℝ)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv) (hw : SmoothVectorOn U w)
    (hm : MetricCompatibleOn U g Gamma) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hl : ∀ x∈U, gInv x*g x=1) (hr : ∀ x∈U, g x*gInv x=1)
    (ht : ∀ x∈U, ∀ i j k, Gamma x i k j=Gamma x j k i)
    (hclosed : ClosedCovectorOn U w) (hwave : CovectorWaveOn U gInv Gamma w) :
    ∀ x∈U, ∀ j, tensorFieldDivergence gInv Gamma (covectorStressField g gInv w coupling) x j=0 := by
  intro x hx j
  rw [covector_stress_divergence_closed g gInv Gamma w coupling x
    (smooth_matrix_differentiableAt U hU g hg x hx)
    (smooth_matrix_differentiableAt U hU gInv hgi x hx)
    (smooth_vector_differentiableAt U hU w hw x hx) (hl x hx)
    (inverse_symmetric_of_symmetric (g x) (gInv x) (hs x hx) (hl x hx))
    (hm x hx) (fun i => inverse_metric_derivative U hU g gInv Gamma hg hgi hm hl hr x hx i)
    (covector_derivative_symmetric Gamma w x (hclosed x hx) (ht x hx)) j,
    hwave x hx,zero_mul,mul_zero]

theorem potential_covector_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (potential : Coordinate4 → ℝ) (hp : ContDiffOn ℝ ∞ potential U) :
    SmoothVectorOn U (potentialCovector potential) := by
  intro i
  exact coordinatePartial_smooth U hU potential hp i

theorem potential_covector_closed (U : Set Coordinate4) (hU : IsOpen U)
    (potential : Coordinate4 → ℝ) (hp : ContDiffOn ℝ ∞ potential U) :
    ClosedCovectorOn U (potentialCovector potential) := by
  intro x hx i j
  exact coordinate_partials_commute potential x (hp.contDiffAt (hU.mem_nhds hx)) i j

#print axioms covector_stress_divergence_point
#print axioms covector_derivative_symmetric
#print axioms covector_stress_divergence_closed
#print axioms covector_stress_conservation_iff_wave_at
#print axioms covector_stress_conserved_on
#print axioms potential_covector_smooth
#print axioms potential_covector_closed
end
end ChatgptAudit.Coherent023
