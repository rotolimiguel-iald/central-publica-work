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
import TGLExt.GeometricEinsteinReconstruction

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

abbrev VectorField4 := Coordinate4 → Coordinate4

def SmoothVectorOn (U : Set Coordinate4) (V : VectorField4) : Prop :=
  ∀ a, ContDiffOn ℝ ∞ (fun x => V x a) U

def vectorPartial (V : VectorField4) (x : Coordinate4) (i : Fin 4) : Coordinate4 :=
  fun a => coordinatePartial (fun y => V y a) x i

def covariantVectorDerivative (Gamma : ConnectionField4) (V : VectorField4)
    (x : Coordinate4) (i : Fin 4) : Coordinate4 :=
  vectorPartial V x i+(Gamma x i).mulVec (V x)

def covariantVectorGradient (Gamma : ConnectionField4) (V : VectorField4)
    (x : Coordinate4) : Tensor4 :=
  fun a i => covariantVectorDerivative Gamma V x i a

def mixedCovariantDerivative (Gamma : ConnectionField4) (B : TensorField4)
    (x : Coordinate4) (i : Fin 4) : Tensor4 :=
  tensorFieldJet B x i+Gamma x i*B x-B x*Gamma x i

def vectorExpansion (Gamma : ConnectionField4) (V : VectorField4) (x : Coordinate4) : ℝ :=
  Matrix.trace (covariantVectorGradient Gamma V x)

def vectorAcceleration (Gamma : ConnectionField4) (V : VectorField4) (x : Coordinate4) : Coordinate4 :=
  (covariantVectorGradient Gamma V x).mulVec (V x)

def scalarAlong (V : VectorField4) (f : Coordinate4 → ℝ) (x : Coordinate4) : ℝ :=
  ∑ i, V x i*coordinatePartial f x i

theorem smooth_vector_differentiableAt (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (x : Coordinate4) (hx : x∈U) :
    ∀ a, DifferentiableAt ℝ (fun y => V y a) x := by
  intro a
  exact ((hV a).differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)

theorem vectorPartial_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (i : Fin 4) :
    SmoothVectorOn U (fun x => vectorPartial V x i) := by
  intro a
  exact coordinatePartial_smooth U hU (fun x => V x a) (hV a) i

theorem vectorPartial_add (V W : VectorField4) (x : Coordinate4)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hW : ∀ a, DifferentiableAt ℝ (fun y => W y a) x) (i : Fin 4) :
    vectorPartial (fun y => V y+W y) x i=vectorPartial V x i+vectorPartial W x i := by
  funext a
  exact coordinatePartial_add (fun y => V y a) (fun y => W y a) x (hV a) (hW a) i

theorem vectorPartial_mulVec (A : TensorField4) (V : VectorField4) (x : Coordinate4)
    (hA : ∀ a b, DifferentiableAt ℝ (fun y => A y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) (i : Fin 4) :
    vectorPartial (fun y => (A y).mulVec (V y)) x i=
      (tensorFieldJet A x i).mulVec (V x)+(A x).mulVec (vectorPartial V x i) := by
  funext a
  change coordinatePartial (fun y => ∑ b, A y a b*V y b) x i=_
  rw [coordinatePartial_sum (fun b y => A y a b*V y b) x (fun b => (hA a b).mul (hV b)) i]
  simp only [coordinatePartial_mul _ _ x (hA _ _) (hV _) i,Matrix.mulVec,
    dotProduct,Pi.add_apply,Finset.sum_add_distrib,tensorFieldJet,vectorPartial]

theorem matrix_mulVec_smooth (U : Set Coordinate4) (A : TensorField4) (V : VectorField4)
    (hA : SmoothMatrixOn U A) (hV : SmoothVectorOn U V) :
    SmoothVectorOn U (fun x => (A x).mulVec (V x)) := by
  intro a
  change ContDiffOn ℝ ∞ (fun x => ∑ b, A x a b*V x b) U
  unfold SmoothMatrixOn at hA
  unfold SmoothVectorOn at hV
  fun_prop

theorem covariantVectorDerivative_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) (i : Fin 4) :
    SmoothVectorOn U (fun x => covariantVectorDerivative Gamma V x i) := by
  intro a
  exact (vectorPartial_smooth U hU V hV i a).add
    (matrix_mulVec_smooth U (fun x => Gamma x i) V (hG i) hV a)

theorem covariantVectorGradient_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothMatrixOn U (covariantVectorGradient Gamma V) := by
  intro a i
  exact covariantVectorDerivative_smooth U hU Gamma V hG hV i a

theorem vectorPartial_commute (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    vectorPartial (fun y => vectorPartial V y j) x i=
      vectorPartial (fun y => vectorPartial V y i) x j := by
  funext a
  exact coordinate_partials_commute (fun y => V y a) x
    ((hV a x hx).contDiffAt (hU.mem_nhds hx)) i j

theorem scalarAlong_eq_fderiv (V : VectorField4) (f : Coordinate4 → ℝ) (x : Coordinate4) :
    scalarAlong V f x=fderiv ℝ f x (V x) := by
  have hv : V x=∑ i : Fin 4, V x i • Pi.single i (1:ℝ) := by
    ext j
    simp [Pi.single_apply]
  rw [hv,map_sum]
  simp only [map_smul,smul_eq_mul]
  rfl

theorem vectorPartial_congr_on (U : Set Coordinate4) (hU : IsOpen U)
    (V W : VectorField4) (hVW : Set.EqOn V W U) (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    vectorPartial V x i=vectorPartial W x i := by
  funext a
  have he : (fun y => V y a) =ᶠ[𝓝 x] (fun y => W y a) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    rw [hVW hy]
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single i 1)) he.fderiv_eq

#print axioms smooth_vector_differentiableAt
#print axioms vectorPartial_smooth
#print axioms vectorPartial_add
#print axioms vectorPartial_mulVec
#print axioms matrix_mulVec_smooth
#print axioms covariantVectorDerivative_smooth
#print axioms covariantVectorGradient_smooth
#print axioms vectorPartial_commute
#print axioms scalarAlong_eq_fderiv
#print axioms vectorPartial_congr_on
end
end ChatgptAudit
