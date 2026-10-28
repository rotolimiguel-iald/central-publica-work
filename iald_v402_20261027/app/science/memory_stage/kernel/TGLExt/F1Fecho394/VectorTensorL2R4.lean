import TGLExt.F1Fecho394.TensorL2EquivalenceR3
import TGLExt.F1Fecho394.CompletedTensorStructureR3
/-! Vector-valued L2 tensor transport, assembled from the scalar L2 unitary and
completed tensor associativity. The Hilbert tensor norm and sectors are unchanged. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory UniformSpace
open scoped TensorProduct ENNReal
namespace F1Fecho.VectorTensorL2
open CompletedTensor
variable {X E F : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
variable (μ : Measure X)

def unitary : CT (Lp E 2 μ) F≃ₗᵢ[ℂ]Lp (CT E F) 2 μ :=
  (congr (TensorL2.unitary (E:=E) μ).symm (.refl ℂ F)).trans
    (collapseLeft.trans (assoc.trans (completeRight.trans (TensorL2.unitary μ))))

theorem separated (a : Lp ℂ 2 μ) (x:E) (y:F) :
    unitary μ (CompletedTensor.pure (TensorL2.pointwise μ (a,x),y))=
      TensorL2.pointwise μ (a,CompletedTensor.pure (x,y)) := by
  have h : (TensorL2.unitary (E:=E) μ).symm (TensorL2.pointwise μ (a,x))=
      TensorL2.pure μ (a,x) := by
    rw [← TensorL2.unitary_pure,LinearIsometryEquiv.symm_apply_apply]
  simp only [unitary,LinearIsometryEquiv.trans_apply,congr_pure,LinearIsometryEquiv.coe_refl,Function.id_def,h]
  change TensorL2.unitary μ (completeRight (assoc (collapseLeft
    (CompletedTensor.pure (((a⊗ₜ[ℂ]x : Lp ℂ 2 μ⊗[ℂ]E):Completion (Lp ℂ 2 μ⊗[ℂ]E)),y)))))=_
  rw [collapseLeft_pure,assoc_pure,completeRight_pure]
  exact TensorL2.unitary_pure (E:=CT E F) μ a (CompletedTensor.pure (x,y))

def attach (y:F) : E→L[ℂ]CT E F :=
  Completion.toComplL.comp ((bilinear (E:=E) (F:=F)).flip y)
lemma attach_apply (x:E) (y:F) : attach y x=CompletedTensor.pure (x,y) := rfl

theorem separated_attach (a : Lp ℂ 2 μ) (x:E) (y:F) :
    (attach y).compLp (TensorL2.pointwise μ (a,x))=TensorL2.pointwise μ (a,CompletedTensor.pure (x,y)) := by
  apply Lp.ext
  filter_upwards [(attach y).coeFn_compLp (TensorL2.pointwise μ (a,x)),
    TensorL2.pointwise_ae μ (a,x),TensorL2.pointwise_ae μ (a,CompletedTensor.pure (x,y))] with z ha hx hy
  rw [ha,hx,hy,map_smul]
  rfl

theorem pure_apply (f:Lp E 2 μ) (y:F) :
    unitary μ (CompletedTensor.pure (f,y))=(attach y).compLp f := by
  let L : Lp E 2 μ→L[ℂ]Lp (CT E F) 2 μ :=
    (unitary μ).toLinearIsometry.toContinuousLinearMap.comp
      (Completion.toComplL.comp ((bilinear (E:=Lp E 2 μ) (F:=F)).flip y))
  let M : Lp E 2 μ→L[ℂ]Lp (CT E F) 2 μ := (attach (E:=E) y).compLpL 2 μ
  change L f=M f
  refine Lp.induction (by norm_num : (2:ENNReal)≠∞) (fun f => L f=M f) ?_ ?_
    (isClosed_eq L.continuous M.continuous) f
  · intro x s hs hμs
    change unitary μ (CompletedTensor.pure (indicatorConstLp 2 hs hμs.ne x,y))=
      (attach y).compLp (indicatorConstLp 2 hs hμs.ne x)
    rw [← TensorL2.pointwise_indicator μ x hs hμs.ne,separated,separated_attach]
  · intro a b ha hb hd hLa hLb
    rw [map_add,map_add,hLa,hLb]

theorem pure_ae (f:Lp E 2 μ) (y:F) : unitary μ (CompletedTensor.pure (f,y)) =ᵐ[μ]
    fun x => CompletedTensor.pure (f x,y) := by
  rw [pure_apply]
  exact (attach y).coeFn_compLp f
end F1Fecho.VectorTensorL2
#print axioms F1Fecho.VectorTensorL2.separated
#print axioms F1Fecho.VectorTensorL2.pure_apply
#print axioms F1Fecho.VectorTensorL2.pure_ae
