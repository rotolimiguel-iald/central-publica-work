import TGLExt.F1Fecho394.FubiniL2
import TGLExt.F1Fecho394.TensorL2EquivalenceR3

/-! Actual interchange of vector L2 variables, using the established Fubini
isometry and the measure-preserving swap. Rank-one formulas are proved on
representatives and will support Fourier interchange by density. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.FubiniTranspose
variable {X Y E : Type} [MeasurableSpace X] [MeasurableSpace Y]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
variable (μ : Measure X) (ν : Measure Y) [SFinite μ] [SFinite ν]
  [IsSeparable μ] [IsSeparable ν]
local instance : InnerProductSpace ℝ E := InnerProductSpace.complexToReal

def flip : Lp E 2 (μ.prod ν) →ₗᵢ[ℂ] Lp E 2 (ν.prod μ) :=
  Lp.compMeasurePreservingₗᵢ ℂ Prod.swap Measure.measurePreserving_swap

theorem flip_ae (f : Lp E 2 (μ.prod ν)) :
    flip μ ν f =ᵐ[ν.prod μ] fun p => f (p.2,p.1) :=
  Lp.coeFn_compMeasurePreserving f Measure.measurePreserving_swap

def transpose : Lp (Lp E 2 μ) 2 ν →ₗᵢ[ℂ] Lp (Lp E 2 ν) 2 μ :=
  (F1Rede.fubiniL2Equiv (𝕜:=ℂ) (μ:=ν) (ν:=μ)).toLinearIsometry.comp
    ((flip μ ν).comp
      (F1Rede.fubiniL2Equiv (𝕜:=ℂ) (μ:=μ) (ν:=ν)).symm.toLinearIsometry)

theorem transpose_fubini_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ x ∂μ, (transpose μ ν (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f) x : Y → E)
      =ᵐ[ν] fun y => f (x,y) := by
  change ∀ᵐ x ∂μ, (F1Rede.fubiniL2Equiv (𝕜:=ℂ) (flip μ ν
    ((F1Rede.fubiniL2Equiv (𝕜:=ℂ)).symm (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f))) x : Y → E)
      =ᵐ[ν] fun y => f (x,y)
  rw [LinearIsometryEquiv.symm_apply_apply]
  filter_upwards [F1Rede.curryLp_coe_ae (flip μ ν f),
    F1Rede.ae_ae_reverse (flip_ae μ ν f)] with x hc hf
  exact hc.trans hf

theorem product_memLp (a : Lp ℂ 2 ν) (e : Lp E 2 μ) :
    MemLp (fun p : X × Y => a p.2 • e p.1) 2 (μ.prod ν) := by
  have hm := ((Lp.stronglyMeasurable a).comp_measurable measurable_snd).smul
    ((Lp.stronglyMeasurable e).comp_measurable measurable_fst)
  apply (memLp_two_iff_integrable_sq_norm hm.aestronglyMeasurable).mpr
  have ha := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable a)).mp (Lp.memLp a)
  have he := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable e)).mp (Lp.memLp e)
  simpa only [Function.comp_apply,norm_smul,mul_pow,mul_comm] using he.mul_prod ha

def product (a : Lp ℂ 2 ν) (e : Lp E 2 μ) : Lp E 2 (μ.prod ν) :=
  (product_memLp μ ν a e).toLp (fun p => a p.2 • e p.1)

theorem product_ae (a : Lp ℂ 2 ν) (e : Lp E 2 μ) :
    product μ ν a e =ᵐ[μ.prod ν] fun p => a p.2 • e p.1 :=
  (product_memLp μ ν a e).coeFn_toLp

theorem fubini_product (a : Lp ℂ 2 ν) (e : Lp E 2 μ) :
    F1Rede.fubiniL2Equiv (𝕜:=ℂ) (product μ ν a e)=TensorL2.pointwise ν (a,e) := by
  apply Lp.ext
  filter_upwards [F1Rede.curryLp_coe_ae (product μ ν a e),
    F1Rede.ae_ae_reverse (product_ae μ ν a e),TensorL2.pointwise_ae ν (a,e)] with y hf hp ht
  rw [ht]
  apply Lp.ext
  filter_upwards [hf,hp,Lp.coeFn_smul (a y) e] with x hx hy hs
  exact (hx.trans hy).trans hs.symm

theorem transpose_rank_one_ae (a : Lp ℂ 2 ν) (e : Lp E 2 μ) :
    transpose μ ν (TensorL2.pointwise ν (a,e)) =ᵐ[μ]
      fun x => TensorL2.pointwise ν (a,e x) := by
  rw [← fubini_product μ ν a e]
  filter_upwards [transpose_fubini_ae μ ν (product μ ν a e),
    Measure.ae_ae_of_ae_prod (product_ae μ ν a e)] with x ht hp
  apply Lp.ext
  exact (ht.trans hp).trans (TensorL2.pointwise_ae ν (a,e x)).symm

end F1Fecho.FubiniTranspose
#print axioms F1Fecho.FubiniTranspose.transpose_fubini_ae
#print axioms F1Fecho.FubiniTranspose.product_memLp
#print axioms F1Fecho.FubiniTranspose.fubini_product
#print axioms F1Fecho.FubiniTranspose.transpose_rank_one_ae
