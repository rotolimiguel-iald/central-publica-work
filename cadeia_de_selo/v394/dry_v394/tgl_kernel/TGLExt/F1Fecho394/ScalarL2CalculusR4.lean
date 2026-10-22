import TGLExt.F1Fecho394.ScalarL2MultiplierR3
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unique
/-! The compact continuous functional calculus acts pointwise on a scalar
multiplier over any measure space. This specializes the earlier regular-line
calculus without imposing a new spectral representation as a hypothesis. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.ScalarL2
variable {X E : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (μ : Measure X) (g:X→unitInterval) (hg:AEStronglyMeasurable g μ)

def compactData (f:C(unitInterval,ℂ)) : Data μ where
  value x := f (g x)
  measurable := f.continuous.comp_aestronglyMeasurable hg
  bound := ‖f‖
  nonneg := norm_nonneg _
  bounded x := f.norm_coe_le_norm (g x)

def compactRepresentation : C(unitInterval,ℂ)→⋆ₐ[ℂ](Lp E 2 μ→L[ℂ]Lp E 2 μ) where
  toFun f := op μ (compactData μ g hg f)
  map_one' := op_one μ _ (fun x=>rfl)
  map_zero' := by
    ext1 u
    apply Lp.ext
    filter_upwards [op_ae μ (compactData μ g hg 0) u,Lp.coeFn_zero (E:=E) (p:=2) (μ:=μ)] with x hx hz
    change op μ (compactData μ g hg 0) u x=(0:Lp E 2 μ) x
    simpa only [compactData,ContinuousMap.zero_apply,zero_smul,hz,Pi.zero_apply] using hx
  map_add' f k := op_add μ _ _ _ (fun x=>rfl)
  map_mul' f k := op_mul μ _ _ _ (fun x=>rfl)
  commutes' c := by
    ext1 u
    apply Lp.ext
    filter_upwards [op_ae μ (compactData μ g hg (algebraMap ℂ C(unitInterval,ℂ) c)) u,
      Lp.coeFn_smul c u] with x hx hy
    change op μ (compactData μ g hg (algebraMap ℂ C(unitInterval,ℂ) c)) u x=(c•u) x
    rw [hx,hy]
    rfl
  map_star' f := op_star μ _ _ (fun x=>rfl)

theorem compactRepresentation_ae (f:C(unitInterval,ℂ)) (u:Lp E 2 μ) :
    compactRepresentation μ g hg f u =ᵐ[μ] fun x=>f (g x)•u x := op_ae μ _ u

def coordinate : C(unitInterval,ℂ) := ⟨fun x=>((x:ℝ):ℂ),by fun_prop⟩
def R : Lp E 2 μ→L[ℂ]Lp E 2 μ := compactRepresentation μ g hg coordinate

theorem cfc_ae (f:ℂ→ℂ) (hf:Continuous f) (u:Lp E 2 μ) :
    cfc f (R (E:=E) μ g hg) u =ᵐ[μ] fun x=>f ((g x:ℝ):ℂ)•u x := by
  let F:=compactRepresentation (E:=E) μ g hg
  have hc : Continuous F := (F.toLinearMap.mkContinuous 1 (by
    intro k
    change ‖op (E:=E) μ (compactData μ g hg k)‖≤1*‖k‖
    simpa only [one_mul,compactData] using norm_op (E:=E) μ (compactData μ g hg k))).continuous
  have he:=F.map_cfc f coordinate hf.continuousOn hc
  change F (cfc f coordinate)=cfc f (R (E:=E) μ g hg) at he
  rw [←he]
  have hv (z:unitInterval) : (cfc f coordinate) z=f ((z:ℝ):ℂ) := by
    have hv:=(ContinuousMap.evalStarAlgHom ℂ ℂ z).map_cfc f coordinate hf.continuousOn
    change (cfc f coordinate) z=cfc f ((z:ℝ):ℂ) at hv
    exact hv.trans (by simpa using cfc_algebraMap (A:=ℂ) ((z:ℝ):ℂ) f)
  filter_upwards [compactRepresentation_ae μ g hg (cfc f coordinate) u] with x hx
  rw [hx,hv]

end F1Fecho.ScalarL2
#print axioms F1Fecho.ScalarL2.compactRepresentation
#print axioms F1Fecho.ScalarL2.cfc_ae
