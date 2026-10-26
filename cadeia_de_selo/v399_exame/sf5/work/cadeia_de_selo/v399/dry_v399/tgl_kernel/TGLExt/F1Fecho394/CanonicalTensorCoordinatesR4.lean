import TGLExt.F1Fecho394.TensorL2ProductR3
import TGLExt.F1Fecho394.BosonicSectors
import TGLExt.F1Fecho394.CanonicalOutput
/-! Constructed product spectral coordinates for the EXISTING tensor powers.
The symmetric sectors and the Fock direct sum are not replaced. The index n
here describes the positive particle number n+1; the vacuum is separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
open MeasureTheory UniformSpace TopologicalSpace
open scoped TensorProduct ENNReal
namespace F1Fecho.TensorCoordinates
open CompletedTensor F1Rede.BosonicSectors F1Rede.BosonicTwoParticle
open TGLExt.ImportedSQ AuditF13v31 F1Rede.CanonicalWedge
open ChatgptAudit.WignerRapidityMeasure016

local instance : SeparableSpace TransverseFiber := by
  letI : Fact ((2:ℝ≥0∞)≠∞) := ⟨by norm_num⟩
  change SeparableSpace (Lp Fib 2 (volume : Measure Transverse))
  infer_instance

def completionCollapse {E:Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [CompleteSpace E] : Completion E≃ₗᵢ[ℂ]E :=
  (LinearEquiv.refl ℂ E).extendOfIsometry
    (Completion.toComplₗᵢ (𝕜:=ℂ) (E:=E)).toLinearMap (LinearMap.id)
    Completion.denseRange_coe denseRange_id (fun x=>by simp)

theorem completionCollapse_coe {E:Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [CompleteSpace E] (x:E) : completionCollapse (x:Completion E)=x :=
  LinearEquiv.extendOfIsometry_eq _ _ _ _ _ _ x

structure SpectralData where
  Index : Type
  [measurable : MeasurableSpace Index]
  [countable : MeasurableSpace.CountablyGenerated Index]
  measure : Measure Index
  [sfinite : SFinite measure]
  Fiber : Type
  [normed : NormedAddCommGroup Fiber]
  [inner : InnerProductSpace ℂ Fiber]
  [complete : CompleteSpace Fiber]
  [separable : SeparableSpace Fiber]
attribute [instance] SpectralData.measurable SpectralData.countable SpectralData.sfinite
  SpectralData.normed SpectralData.inner SpectralData.complete SpectralData.separable

def data : ℕ→SpectralData
  | 0 => { Index:=ℝ,measure:=volume,Fiber:=TransverseFiber }
  | n+1 => {
      Index:=(data n).Index×ℝ
      measure:=(data n).measure.prod volume
      Fiber:=CT TransverseFiber (data n).Fiber
      separable:=TensorL2Product.tensor_separable }

abbrev Space (n:ℕ) := Lp (data n).Fiber 2 (data n).measure

def first : TensorHilbert 1≃ₗᵢ[ℂ]Space 0 :=
  (comm (E:=H1) (F:=ℂ)).trans
    ((completionEquiv (TensorProduct.lidIsometry ℂ H1)).trans
      (completionCollapse.trans Phi))

theorem first_pure (f:H1) : first (pureCompleted 1 f)=Phi f := by
  change Phi (completionCollapse (completionEquiv (TensorProduct.lidIsometry ℂ H1)
    (comm (CompletedTensor.pure (f,(1:ℂ))))))=_
  rw [comm_pure]
  simp only [CompletedTensor.pure,completionEquiv_coe,TensorProduct.lidIsometry_apply,
    TensorProduct.lid_tmul,one_smul,completionCollapse_coe]

def coordinates : (n:ℕ)→TensorHilbert (n+1)≃ₗᵢ[ℂ]Space n
  | 0 => first
  | n+1 => (completeRight (E:=H1) (F:=Algebraic (n+1))).trans
      ((congr Phi (coordinates n)).trans
        (TensorL2Product.unitary (volume:Measure ℝ) (data n).measure))

theorem coordinates_succ_tmul (n:ℕ) (f:H1) (v:Algebraic (n+1)) :
    coordinates (n+1) (CompletedTensor.pure (f,v)) =
      TensorL2Product.unitary (volume:Measure ℝ) (data n).measure
        (CompletedTensor.pure (Phi f,coordinates n (v:TensorHilbert (n+1)))) := by
  change TensorL2Product.unitary _ _
    (congr Phi (coordinates n) (completeRight (CompletedTensor.pure (f,v))))=_
  rw [completeRight_pure,congr_pure]

theorem coordinates_succ_ae (n:ℕ) (f:H1) (v:Algebraic (n+1)) :
    coordinates (n+1) (CompletedTensor.pure (f,v)) =ᵐ[(data (n+1)).measure]
      fun p=>CompletedTensor.pure (Phi f p.2,coordinates n (v:TensorHilbert (n+1)) p.1) := by
  rw [coordinates_succ_tmul]
  exact TensorL2Product.unitary_ae (E:=TransverseFiber) (F:=(data n).Fiber)
    (volume:Measure ℝ) (data n).measure (Phi f) (coordinates n (v:TensorHilbert (n+1)))

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.completionCollapse_coe
#print axioms F1Fecho.TensorCoordinates.first_pure
#print axioms F1Fecho.TensorCoordinates.coordinates
#print axioms F1Fecho.TensorCoordinates.coordinates_succ_ae
