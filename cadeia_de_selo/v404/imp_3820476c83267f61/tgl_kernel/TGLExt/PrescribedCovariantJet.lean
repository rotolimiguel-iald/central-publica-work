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
import TGLExt.NullJetAlgebra

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow019
open Matrix Filter Topology Set ChatgptAudit.Flow018 ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def connectionInitialJet (Gamma : ConnectionField4) (p v : Coordinate4) :
    Coordinate4 →L[ℝ] Coordinate4 :=
  -∑ i : Fin 4, (ContinuousLinearMap.proj i).smulRight ((Gamma p i).mulVec v)

def affineInitialSeed (Gamma : ConnectionField4) (p v x : Coordinate4) : Coordinate4 :=
  v+connectionInitialJet Gamma p v (x-p)

theorem connection_initial_jet_apply (Gamma : ConnectionField4) (p v w : Coordinate4) :
    connectionInitialJet Gamma p v w= -((connectionAlong Gamma p w).mulVec v) := by
  ext a
  simp [connectionInitialJet,connectionAlong,Matrix.mulVec,dotProduct,Fin.sum_univ_four]
  ring

theorem vector_partial_of_derivative (V : VectorField4) (p : Coordinate4)
    (L : Coordinate4 →L[ℝ] Coordinate4) (hV : HasFDerivAt V L p) (i : Fin 4) :
    vectorPartial V p i=L (Pi.single i 1) := by
  funext a
  have hc := (ContinuousLinearMap.proj a : Coordinate4 →L[ℝ] ℝ).hasFDerivAt.comp p hV
  have hd : HasFDerivAt (fun y => V y a)
      ((ContinuousLinearMap.proj a : Coordinate4 →L[ℝ] ℝ).comp L) p := by
    convert hc using 1 <;> rfl
  unfold vectorPartial coordinatePartial
  rw [hd.fderiv]
  rfl

theorem gradient_action_derivative (Gamma : ConnectionField4) (V : VectorField4)
    (p : Coordinate4) (hV : DifferentiableAt ℝ V p) (w : Coordinate4) :
    (covariantVectorGradient Gamma V p).mulVec w=
      fderiv ℝ V p w+(connectionAlong Gamma p w).mulVec (V p) := by
  have hw : w=∑ i : Fin 4, w i • Pi.single i (1:ℝ) := by
    ext j
    simp [Pi.single_apply]
  have hf : fderiv ℝ V p w=∑ i : Fin 4, w i • vectorPartial V p i := by
    conv_lhs => rw [hw,map_sum]
    simp only [map_smul,vector_partial_of_derivative V p _ hV.hasFDerivAt]
  rw [hf]
  ext a
  simp only [covariantVectorGradient,covariantVectorDerivative,connectionAlong,Matrix.mulVec,
    dotProduct,Pi.add_apply,Matrix.add_apply,Matrix.smul_apply,Pi.smul_apply,smul_eq_mul,Fin.sum_univ_four]
  ring

theorem derivative_of_zero_covariant_gradient (Gamma : ConnectionField4) (V : VectorField4)
    (p : Coordinate4) (hV : DifferentiableAt ℝ V p)
    (hz : covariantVectorGradient Gamma V p=0) :
    HasFDerivAt V (connectionInitialJet Gamma p (V p)) p := by
  have he : fderiv ℝ V p=connectionInitialJet Gamma p (V p) := by
    apply ContinuousLinearMap.ext
    intro w
    have h := gradient_action_derivative Gamma V p hV w
    rw [hz,Matrix.zero_mulVec] at h
    rw [connection_initial_jet_apply]
    exact (eq_neg_iff_add_eq_zero).2 h.symm
  simpa only [he] using hV.hasFDerivAt

theorem affine_seed_initial (Gamma : ConnectionField4) (p v : Coordinate4) :
    affineInitialSeed Gamma p v p=v := by
  simp [affineInitialSeed]

theorem affine_seed_smooth (Gamma : ConnectionField4) (p v : Coordinate4) :
    ContDiff ℝ ∞ (affineInitialSeed Gamma p v) :=
  contDiff_const.add ((connectionInitialJet Gamma p v).contDiff.comp (contDiff_id.sub contDiff_const))

theorem affine_seed_derivative (Gamma : ConnectionField4) (p v x : Coordinate4) :
    HasFDerivAt (affineInitialSeed Gamma p v) (connectionInitialJet Gamma p v) x := by
  convert ((connectionInitialJet Gamma p v).hasFDerivAt.comp x
    ((hasFDerivAt_id x).sub_const p)).const_add v using 1 <;> rfl

theorem affine_seed_covariant_derivative_zero (Gamma : ConnectionField4) (p v : Coordinate4)
    (i : Fin 4) : covariantVectorDerivative Gamma (affineInitialSeed Gamma p v) p i=0 := by
  unfold covariantVectorDerivative
  rw [vector_partial_of_derivative _ _ _ (affine_seed_derivative Gamma p v p) i,
    affine_seed_initial,connection_initial_jet_apply]
  have he : connectionAlong Gamma p (Pi.single i 1)=Gamma p i := by
    fin_cases i <;> simp [connectionAlong,Pi.single_apply]
  rw [he]
  exact neg_add_cancel _

theorem affine_seed_gradient_zero (Gamma : ConnectionField4) (p v : Coordinate4) :
    covariantVectorGradient Gamma (affineInitialSeed Gamma p v) p=0 := by
  ext a i
  change covariantVectorDerivative Gamma (affineInitialSeed Gamma p v) p i a=0
  rw [affine_seed_covariant_derivative_zero]
  rfl

theorem affine_seed_energy_derivative_zero (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hg : SmoothMatrixOn U g)
    (hm : MetricCompatibleOn U g Gamma) (p v : Coordinate4) (hp : p∈U)
    (hgs : (g p)ᵀ=g p) :
    HasFDerivAt (fun x => tensorQuad (g x) (affineInitialSeed Gamma p v x)) (0 : Coordinate4 →L[ℝ] ℝ) p := by
  let R := affineInitialSeed Gamma p v
  have hR : SmoothVectorOn U R := contDiffOn_pi.1 (affine_seed_smooth Gamma p v).contDiffOn
  have hq := tensor_pair_smooth U g R R hg hR hR
  apply scalar_derivative_zero_from_partials _ p
    (((hq p hp).contDiffAt (hU.mem_nhds hp)).differentiableAt (by simp))
  intro i
  change coordinatePartial (fun x => tensorQuad (g x) (R x)) p i=0
  rw [metric_compatible_quad_derivative U g Gamma R hm p hp hgs
    (smooth_matrix_differentiableAt U hU g hg p hp)
    (smooth_vector_differentiableAt U hU R hR p hp) i]
  rw [affine_seed_covariant_derivative_zero]
  simp [tensorPair]

#print axioms connection_initial_jet_apply
#print axioms vector_partial_of_derivative
#print axioms gradient_action_derivative
#print axioms derivative_of_zero_covariant_gradient
#print axioms affine_seed_initial
#print axioms affine_seed_smooth
#print axioms affine_seed_derivative
#print axioms affine_seed_covariant_derivative_zero
#print axioms affine_seed_gradient_zero
#print axioms affine_seed_energy_derivative_zero
end
end ChatgptAudit.Flow019
