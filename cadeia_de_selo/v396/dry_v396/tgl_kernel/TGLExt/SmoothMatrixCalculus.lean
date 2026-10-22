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
import TGLExt.TensorFieldLinearity
import Mathlib.Analysis.Calculus.FDeriv.Symmetric

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

def SmoothMatrixOn (U : Set Coordinate4) (A : TensorField4) : Prop :=
  ∀ j k, ContDiffOn ℝ ∞ (fun x => A x j k) U

theorem coordinatePartial_add (f g : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 4) :
    coordinatePartial (fun y => f y+g y) x i = coordinatePartial f x i+coordinatePartial g x i := by
  unfold coordinatePartial
  rw [fderiv_fun_add hf hg]
  rfl

theorem coordinatePartial_sub (f g : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 4) :
    coordinatePartial (fun y => f y-g y) x i = coordinatePartial f x i-coordinatePartial g x i := by
  unfold coordinatePartial
  rw [fderiv_fun_sub hf hg]
  rfl

theorem coordinatePartial_sum (f : Fin 4 → Coordinate4 → ℝ) (x : Coordinate4)
    (hf : ∀ k, DifferentiableAt ℝ (f k) x) (i : Fin 4) :
    coordinatePartial (fun y => ∑ k, f k y) x i=∑ k, coordinatePartial (f k) x i := by
  unfold coordinatePartial
  rw [fderiv_fun_sum (fun k _ => hf k)]
  simp

theorem coordinatePartial_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (f : Coordinate4 → ℝ) (hf : ContDiffOn ℝ ∞ f U) (i : Fin 4) :
    ContDiffOn ℝ ∞ (fun x => coordinatePartial f x i) U := by
  have hd : ContDiffOn ℝ ∞ (fderiv ℝ f) U := hf.fderiv_of_isOpen hU (by simp)
  exact hd.clm_apply contDiffOn_const

theorem coordinatePartial_second_eq (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : ContDiffAt ℝ ∞ f x) (i j : Fin 4) :
    coordinatePartial (fun y => coordinatePartial f y j) x i =
      fderiv ℝ (fderiv ℝ f) x (Pi.single i 1) (Pi.single j 1) := by
  have hd : DifferentiableAt ℝ (fderiv ℝ f) x :=
    (hf.fderiv_right (m := 1) (by exact WithTop.coe_le_coe.mpr (show (2 : ℕ∞) ≤ ⊤ from le_top))).differentiableAt (by norm_num)
  unfold coordinatePartial
  rw [fderiv_clm_apply hd (differentiableAt_const (Pi.single j 1))]
  simp

theorem coordinate_partials_commute (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : ContDiffAt ℝ ∞ f x) (i j : Fin 4) :
    coordinatePartial (fun y => coordinatePartial f y j) x i =
      coordinatePartial (fun y => coordinatePartial f y i) x j := by
  rw [coordinatePartial_second_eq f x hf i j,coordinatePartial_second_eq f x hf j i]
  exact (hf.isSymmSndFDerivAt (by
    simp only [minSmoothness_of_isRCLikeNormedField]
    exact WithTop.coe_le_coe.mpr le_top)).eq _ _

theorem smooth_matrix_differentiableAt (U : Set Coordinate4) (hU : IsOpen U)
    (A : TensorField4) (hA : SmoothMatrixOn U A) (x : Coordinate4) (hx : x∈U) :
    ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x := by
  intro j k
  exact ((hA j k).differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)

theorem tensorFieldJet_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (A : TensorField4) (hA : SmoothMatrixOn U A) (i : Fin 4) :
    SmoothMatrixOn U (fun x => tensorFieldJet A x i) := by
  intro j k
  exact coordinatePartial_smooth U hU (fun x => A x j k) (hA j k) i

theorem tensorFieldJet_add (A B : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x)
    (hB : ∀ j k, DifferentiableAt ℝ (fun y => B y j k) x) :
    tensorFieldJet (fun y => A y+B y) x=tensorFieldJet A x+tensorFieldJet B x := by
  funext i
  ext j k
  exact coordinatePartial_add (fun y => A y j k) (fun y => B y j k) x (hA j k) (hB j k) i

theorem tensorFieldJet_transpose (A : TensorField4) (x : Coordinate4) (i : Fin 4) :
    tensorFieldJet (fun y => (A y)ᵀ) x i=(tensorFieldJet A x i)ᵀ := rfl

theorem tensorFieldJet_mul (A B : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x)
    (hB : ∀ j k, DifferentiableAt ℝ (fun y => B y j k) x) (i : Fin 4) :
    tensorFieldJet (fun y => A y*B y) x i=tensorFieldJet A x i*B x+A x*tensorFieldJet B x i := by
  ext j k
  change coordinatePartial (fun y => ∑ l, A y j l*B y l k) x i = _
  rw [coordinatePartial_sum (fun l y => A y j l*B y l k) x (fun l => (hA j l).mul (hB l k)) i]
  simp only [coordinatePartial_mul _ _ x (hA _ _) (hB _ _) i,Matrix.add_apply,
    Matrix.mul_apply,Finset.sum_add_distrib,tensorFieldJet]

theorem tensorFieldJet_commute (U : Set Coordinate4) (hU : IsOpen U)
    (A : TensorField4) (hA : SmoothMatrixOn U A) (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    tensorFieldJet (fun y => tensorFieldJet A y j) x i=
      tensorFieldJet (fun y => tensorFieldJet A y i) x j := by
  ext k l
  exact coordinate_partials_commute (fun y => A y k l) x
    ((hA k l x hx).contDiffAt (hU.mem_nhds hx)) i j


theorem SmoothMatrixOn.add (U : Set Coordinate4) (A B : TensorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B) :
    SmoothMatrixOn U (fun x => A x+B x) := by
  intro i j
  exact (hA i j).add (hB i j)

theorem SmoothMatrixOn.sub (U : Set Coordinate4) (A B : TensorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B) :
    SmoothMatrixOn U (fun x => A x-B x) := by
  intro i j
  exact (hA i j).sub (hB i j)

theorem SmoothMatrixOn.mul (U : Set Coordinate4) (A B : TensorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B) :
    SmoothMatrixOn U (fun x => A x*B x) := by
  intro i j
  change ContDiffOn ℝ ∞ (fun x => ∑ k, A x i k*B x k j) U
  unfold SmoothMatrixOn at hA hB
  fun_prop

theorem SmoothMatrixOn.transpose (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) : SmoothMatrixOn U (fun x => (A x)ᵀ) := by
  intro i j
  exact hA j i

#print axioms SmoothMatrixOn.add
#print axioms SmoothMatrixOn.sub
#print axioms SmoothMatrixOn.mul
#print axioms SmoothMatrixOn.transpose

#print axioms coordinatePartial_add
#print axioms coordinatePartial_sub
#print axioms coordinatePartial_sum
#print axioms coordinatePartial_smooth
#print axioms coordinatePartial_second_eq
#print axioms coordinate_partials_commute
#print axioms smooth_matrix_differentiableAt
#print axioms tensorFieldJet_smooth
#print axioms tensorFieldJet_add
#print axioms tensorFieldJet_transpose
#print axioms tensorFieldJet_mul
#print axioms tensorFieldJet_commute
end
end ChatgptAudit
