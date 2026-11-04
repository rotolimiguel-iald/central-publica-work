import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.MeasureTheory.Function.LpSpace.Complete
import Mathlib.Tactic
/-! Scalar multipliers on an arbitrary measure space. This is the measure-space
generalization needed for tensor spectral coordinates; it does not change Fock. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.ScalarL2
variable {X E : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (μ : Measure X)

structure Data where
  value : X→ℂ
  measurable : AEStronglyMeasurable value μ
  bound : ℝ
  nonneg : 0≤bound
  bounded : ∀x, ‖value x‖≤bound

variable (d : Data μ)
theorem mem (f:Lp E 2 μ) : MemLp (fun x=>d.value x • f x) 2 μ :=
  (Lp.memLp f).of_le_mul (d.measurable.smul (Lp.aestronglyMeasurable f))
    (Eventually.of_forall fun x=> by
      rw [norm_smul]
      exact mul_le_mul_of_nonneg_right (d.bounded x) (norm_nonneg _))

def applyLp (f:Lp E 2 μ) : Lp E 2 μ := (mem μ d f).toLp _
theorem apply_ae (f:Lp E 2 μ) : applyLp μ d f =ᵐ[μ] fun x=>d.value x • f x :=
  (mem μ d f).coeFn_toLp

def linear : Lp E 2 μ→ₗ[ℂ]Lp E 2 μ where
  toFun := applyLp μ d
  map_add' f g := by
    apply Lp.ext
    filter_upwards [apply_ae μ d (f+g),apply_ae μ d f,apply_ae μ d g,
      Lp.coeFn_add f g,Lp.coeFn_add (applyLp μ d f) (applyLp μ d g)] with x h1 h2 h3 h4 h5
    simp only [Pi.add_apply] at h4 h5
    rw [h1,h5,h2,h3,h4,smul_add]
  map_smul' c f := by
    apply Lp.ext
    filter_upwards [apply_ae μ d (c•f),apply_ae μ d f,Lp.coeFn_smul c f,
      Lp.coeFn_smul c (applyLp μ d f)] with x h1 h2 h3 h4
    simp only [Pi.smul_apply] at h3 h4
    simp only [RingHom.id_apply]
    rw [h1,h4,h2,h3,smul_smul,smul_smul,mul_comm]

theorem norm_apply (f:Lp E 2 μ) : ‖applyLp μ d f‖≤d.bound*‖f‖ := by
  apply Lp.norm_le_mul_norm_of_ae_le_mul
  filter_upwards [apply_ae μ d f] with x hx
  rw [hx,norm_smul]
  exact mul_le_mul_of_nonneg_right (d.bounded x) (norm_nonneg _)

def op : Lp E 2 μ→L[ℂ]Lp E 2 μ := (linear μ d).mkContinuous d.bound (norm_apply μ d)
theorem op_ae (f:Lp E 2 μ) : op μ d f =ᵐ[μ] fun x=>d.value x • f x := apply_ae μ d f
theorem norm_op : ‖op (E:=E) μ d‖≤d.bound :=
  ContinuousLinearMap.opNorm_le_bound _ d.nonneg (norm_apply μ d)

theorem op_eq (e:Data μ) (h:∀x,d.value x=e.value x) : op (E:=E) μ d=op μ e := by
  ext1 f
  apply Lp.ext
  filter_upwards [op_ae μ d f,op_ae μ e f] with x hx hy
  rw [hx,hy,h]

theorem op_one (h:∀x,d.value x=1) : op (E:=E) μ d=1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [op_ae μ d f] with x hx
  change op μ d f x=f x
  simpa only [h,one_smul] using hx

theorem op_add (e k:Data μ) (h:∀x,k.value x=d.value x+e.value x) :
    op (E:=E) μ k=op μ d+op μ e := by
  ext1 f
  apply Lp.ext
  filter_upwards [op_ae μ k f,op_ae μ d f,op_ae μ e f,
    Lp.coeFn_add (op μ d f) (op μ e f)] with x hk hd he ha
  change op μ k f x=(op μ d f+op μ e f) x
  simp only [Pi.add_apply] at ha
  rw [hk,ha,hd,he,h,add_smul]

theorem op_mul (e k:Data μ) (h:∀x,k.value x=d.value x*e.value x) :
    op (E:=E) μ k=op μ d*op μ e := by
  ext1 f
  apply Lp.ext
  filter_upwards [op_ae μ k f,op_ae μ d (op μ e f),op_ae μ e f] with x hk hd he
  change op μ k f x=op μ d (op μ e f) x
  rw [hk,hd,he,h,smul_smul]

theorem op_star (e:Data μ) (h:∀x,e.value x=star (d.value x)) :
    op (E:=E) μ e=star (op (E:=E) μ d) := by
  apply (ContinuousLinearMap.eq_adjoint_iff _ _).mpr
  intro f g
  rw [L2.inner_def,L2.inner_def]
  apply integral_congr_ae
  filter_upwards [op_ae μ e f,op_ae μ d g] with x he hd
  rw [he,hd,inner_smul_left,inner_smul_right,h]
  simp

theorem op_injective (h:∀x,d.value x≠0) : Function.Injective (op (E:=E) μ d) := by
  intro f g he
  apply Lp.ext
  filter_upwards [op_ae μ d f,op_ae μ d g] with x hf hg
  apply smul_right_injective E (h x)
  exact hf.symm.trans ((congrArg (fun v:Lp E 2 μ=>v x) he).trans hg)

end F1Fecho.ScalarL2
#print axioms F1Fecho.ScalarL2.norm_op
#print axioms F1Fecho.ScalarL2.op_mul
#print axioms F1Fecho.ScalarL2.op_star
#print axioms F1Fecho.ScalarL2.op_injective
