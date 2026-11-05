-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_019 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.NullCongruenceControls

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Flow018 ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def nullCorrection (g : Tensor4) (u n : Coordinate4) : Coordinate4 :=
  u-(tensorQuad g u/(2*tensorPair g u n)) • n

theorem quadratic_sub_null_direction (g : Tensor4) (u n : Coordinate4) (c : ℝ) :
    tensorQuad g (u-c • n)=tensorQuad g u-
      c*(tensorPair g u n+tensorPair g n u)+c^2*tensorQuad g n := by
  simp only [tensorQuad,tensorPair,Matrix.mulVec,dotProduct,Pi.sub_apply,Pi.smul_apply,
    smul_eq_mul,Fin.sum_univ_four]
  ring

theorem null_correction_null (g : Tensor4) (u n : Coordinate4) (hg : gᵀ=g)
    (hn : tensorQuad g n=0) (hd : tensorPair g u n≠0) :
    tensorQuad g (nullCorrection g u n)=0 := by
  rw [nullCorrection,quadratic_sub_null_direction,tensor_pair_symmetric g hg n u,hn]
  field_simp
  ring

theorem null_correction_fixes_null (g : Tensor4) (u n : Coordinate4)
    (hu : tensorQuad g u=0) : nullCorrection g u n=u := by
  simp [nullCorrection,hu]

theorem tensor_pair_smooth (U : Set Coordinate4) (g : TensorField4) (V W : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V) (hW : SmoothVectorOn U W) :
    ContDiffOn ℝ ∞ (fun x => tensorPair (g x) (V x) (W x)) U := by
  change ContDiffOn ℝ ∞ (fun x => ∑ a, V x a*(∑ b, g x a b*W x b)) U
  unfold SmoothMatrixOn at hg
  unfold SmoothVectorOn at hV hW
  fun_prop

theorem null_correction_smooth (U : Set Coordinate4) (g : TensorField4) (V W : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V) (hW : SmoothVectorOn U W)
    (hd : ∀ x∈U, tensorPair (g x) (V x) (W x)≠0) :
    SmoothVectorOn U (fun x => nullCorrection (g x) (V x) (W x)) := by
  have hq := tensor_pair_smooth U g V V hg hV hV
  have hb := tensor_pair_smooth U g V W hg hV hW
  have hc : ContDiffOn ℝ ∞ (fun x => tensorQuad (g x) (V x)/(2*tensorPair (g x) (V x) (W x))) U :=
    hq.div (contDiffOn_const.mul hb) (fun x hx => mul_ne_zero (by norm_num) (hd x hx))
  intro a
  exact (hV a).sub (hc.mul (hW a))

theorem scalar_derivative_zero_from_partials (f : Coordinate4 → ℝ) (p : Coordinate4)
    (hf : DifferentiableAt ℝ f p) (hp : ∀ i, coordinatePartial f p i=0) :
    HasFDerivAt f (0 : Coordinate4 →L[ℝ] ℝ) p := by
  have hz : fderiv ℝ f p=0 := by
    apply ContinuousLinearMap.ext
    intro w
    rw [←scalarAlong_eq_fderiv (fun _ => w) f p]
    simp only [scalarAlong,hp,mul_zero,Finset.sum_const_zero,_root_.zero_apply]
  simpa only [hz] using hf.hasFDerivAt

theorem zero_jet_quotient (f d : Coordinate4 → ℝ) (p : Coordinate4)
    (hf : HasFDerivAt f (0 : Coordinate4 →L[ℝ] ℝ) p) (hf0 : f p=0) (hd : DifferentiableAt ℝ d p) (hd0 : d p≠0) :
    HasFDerivAt (fun x => f x/d x) (0 : Coordinate4 →L[ℝ] ℝ) p := by
  convert hf.mul (hd.inv hd0).hasFDerivAt using 1 <;> first | rfl | simp [hf0]

theorem null_correction_preserves_derivative (g : TensorField4) (V W : VectorField4)
    (p : Coordinate4) (L : Coordinate4 →L[ℝ] Coordinate4) (hV : HasFDerivAt V L p)
    (hW : DifferentiableAt ℝ W p)
    (hq : HasFDerivAt (fun x => tensorQuad (g x) (V x)) (0 : Coordinate4 →L[ℝ] ℝ) p)
    (hq0 : tensorQuad (g p) (V p)=0)
    (hb : DifferentiableAt ℝ (fun x => 2*tensorPair (g x) (V x) (W x)) p)
    (hb0 : 2*tensorPair (g p) (V p) (W p)≠0) :
    HasFDerivAt (fun x => nullCorrection (g x) (V x) (W x)) L p := by
  have hc := zero_jet_quotient (fun x => tensorQuad (g x) (V x))
    (fun x => 2*tensorPair (g x) (V x) (W x)) p hq hq0 hb hb0
  have hh := hc.smul hW.hasFDerivAt
  have hz : HasFDerivAt
      (fun x => (tensorQuad (g x) (V x)/(2*tensorPair (g x) (V x) (W x))) • W x) (0 : Coordinate4 →L[ℝ] Coordinate4) p := by
    simpa [hq0] using hh
  convert hV.sub hz using 1 <;> first | rfl | simp only [sub_zero]

#print axioms quadratic_sub_null_direction
#print axioms null_correction_null
#print axioms null_correction_fixes_null
#print axioms tensor_pair_smooth
#print axioms null_correction_smooth
#print axioms scalar_derivative_zero_from_partials
#print axioms zero_jet_quotient
#print axioms null_correction_preserves_derivative
end
end ChatgptAudit.Flow019
