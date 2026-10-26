-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_008 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.LorentzMetricField
import TGLExt.MetricFieldConnection
import TGLExt.TensorFieldLinearity

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix
noncomputable section

theorem conserved_null_tensor_is_constant_metric_multiple
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (E D A : TensorField4)
    (hED : ∀ x∈U, E x*D x=1) (hDE : ∀ x∈U, D x*E x=1)
    (hE : ∀ i j, DifferentiableOn ℝ (fun x => E x i j) U)
    (hD : ∀ i j, DifferentiableOn ℝ (fun x => D x i j) U)
    (hA : ∀ i j, DifferentiableOn ℝ (fun x => A x i j) U)
    (hs : ∀ x∈U, (A x)ᵀ=A x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (frameMetricField E x) v=0 → tensorQuad (A x) v=0)
    (hd : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D)) A x j=0) :
    ∃ c : ℝ, ∀ x∈U, A x=c • frameMetricField E x := by
  have heq : Set.EqOn A (fun x => frameScalar D A x • frameMetricField E x) U := by
    intro x hx
    exact null_tensor_eq_frame_scalar E D A x (hED x hx) (hDE x hx) (hs x hx) (hn x hx)
  have hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D))
      (fun x => frameScalar D A x • frameMetricField E x) x j=0 := by
    intro x hx j
    rw [← tensorFieldDivergence_congr_on U hU (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D)) A
      (fun x => frameScalar D A x • frameMetricField E x) heq x hx]
    exact hd x hx j
  obtain ⟨c,hc⟩ := levi_civita_conserved_scalar_is_constant U hU hconn
    (frameMetricField E) (inverseFrameMetricField D)
    (fun x _ => frame_metric_symmetric E x)
    (fun x hx => inverse_frame_metric_left E D x (hED x hx) (hDE x hx))
    (fun x hx => inverse_frame_metric_right E D x (hED x hx) (hDE x hx))
    (frameScalar D A) (frame_scalar_differentiableOn U D A hD hA)
    (frame_metric_differentiableOn U E hE) hdiv
  refine ⟨c,?_⟩
  intro x hx
  exact (heq hx).trans (congrArg (fun z : ℝ => z • frameMetricField E x) (hc x hx))

theorem conserved_null_balance_has_constant_term
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (E D G T : TensorField4) (coupling : ℝ)
    (hED : ∀ x∈U, E x*D x=1) (hDE : ∀ x∈U, D x*E x=1)
    (hE : ∀ i j, DifferentiableOn ℝ (fun x => E x i j) U)
    (hD : ∀ i j, DifferentiableOn ℝ (fun x => D x i j) U)
    (hG : ∀ i j, DifferentiableOn ℝ (fun x => G x i j) U)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsG : ∀ x∈U, (G x)ᵀ=G x) (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (frameMetricField E x) v=0 →
      tensorQuad (G x-coupling • T x) v=0)
    (hdG : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D)) G x j=0)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D)) T x j=0) :
    ∃ cosmological : ℝ, ∀ x∈U, G x+cosmological • frameMetricField E x=coupling • T x := by
  have hA : ∀ i j, DifferentiableOn ℝ (fun x => (G x-coupling • T x) i j) U := by
    intro i j
    exact (hG i j).sub ((hT i j).const_mul coupling)
  have hs : ∀ x∈U, (G x-coupling • T x)ᵀ=G x-coupling • T x := by
    intro x hx
    simp only [Matrix.transpose_sub,Matrix.transpose_smul,hsG x hx,hsT x hx]
  have hd : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField D)
      (leviCivitaField (frameMetricField E) (inverseFrameMetricField D))
      (fun y => G y-coupling • T y) x j=0 := by
    intro x hx j
    have hgAt : ∀ i k, DifferentiableAt ℝ (fun y => G y i k) x :=
      fun i k => (hG i k).differentiableAt (hU.mem_nhds hx)
    have htAt : ∀ i k, DifferentiableAt ℝ (fun y => T y i k) x :=
      fun i k => (hT i k).differentiableAt (hU.mem_nhds hx)
    rw [tensorFieldDivergence_sub _ _ G (fun y => coupling • T y) x hgAt
      (fun i k => (htAt i k).const_mul coupling) j,
      tensorFieldDivergence_const_smul _ _ coupling T x htAt j,hdG x hx j,hdT x hx j,
      mul_zero,sub_zero]
  obtain ⟨c,hc⟩ := conserved_null_tensor_is_constant_metric_multiple U hU hconn E D
    (fun x => G x-coupling • T x) hED hDE hE hD hA hs hn hd
  refine ⟨-c,?_⟩
  intro x hx
  rw [neg_smul,← hc x hx]
  abel

#print axioms conserved_null_tensor_is_constant_metric_multiple
#print axioms conserved_null_balance_has_constant_term
end
end ChatgptAudit
