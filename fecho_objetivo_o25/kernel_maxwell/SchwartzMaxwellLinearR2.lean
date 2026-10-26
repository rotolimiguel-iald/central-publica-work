import SchwartzMaxwellSmearingR4

/-! Complex linearity of the global Schwartz-to-H1 map. The later Segal map
is real-linear; no complex-linearity assertion about the self-adjoint field. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Matrix SchwartzMap
open ChatgptAudit.WignerRapidityMeasure016 TGLExt.ImportedSQ

theorem globalCoefficient_add (f g : SchwartzTensor) :
    globalCoefficient (f+g)=globalCoefficient f+globalCoefficient g := by
  funext y
  apply PiLp.ext
  intro j
  simp [globalCoefficient,mul_add,Finset.sum_add_distrib]

theorem globalCoefficient_smul (c : ℂ) (f : SchwartzTensor) :
    globalCoefficient (c•f)=c•globalCoefficient f := by
  funext y
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑ μ,∑ ν,(cartesianStrength y j μ ν:ℂ)*
    (c*f (shellEmbedding y) μ ν))=c*((1/2:ℂ)*(∑ μ,∑ ν,
      (cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν))
  have he : (∑ μ,∑ ν,(cartesianStrength y j μ ν:ℂ)*(c*f (shellEmbedding y) μ ν))=
      c*(∑ μ,∑ ν,(cartesianStrength y j μ ν:ℂ)*f (shellEmbedding y) μ ν) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro μ _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro ν _
    ring
  rw [he]
  ring

theorem momentumSmear_add (f g : SchwartzTensor) :
    momentumSmear (f+g)=momentumSmear f+momentumSmear g := by
  apply Lp.ext
  filter_upwards [(globalCoefficient_memLp (f+g)).coeFn_toLp,
    (globalCoefficient_memLp f).coeFn_toLp,(globalCoefficient_memLp g).coeFn_toLp,
    Lp.coeFn_add (momentumSmear f) (momentumSmear g)] with y h1 h2 h3 h4
  rw [h1,h4]
  simp only [Pi.add_apply]
  rw [h2,h3]
  exact congrFun (globalCoefficient_add f g) y

theorem momentumSmear_smul (c : ℂ) (f : SchwartzTensor) :
    momentumSmear (c•f)=c•momentumSmear f := by
  apply Lp.ext
  filter_upwards [(globalCoefficient_memLp (c•f)).coeFn_toLp,
    (globalCoefficient_memLp f).coeFn_toLp,Lp.coeFn_smul c (momentumSmear f)] with y h1 h2 h3
  rw [h1,h3]
  simp only [Pi.smul_apply]
  rw [h2]
  exact congrFun (globalCoefficient_smul c f) y

def spacetimeSmearLinear : SchwartzTensor →ₗ[ℂ] H1 where
  toFun := spacetimeSmear
  map_add' f g := by simp only [spacetimeSmear,minkowskiFourier_add,momentumSmear_add]
  map_smul' c f := by simp only [spacetimeSmear,minkowskiFourier_smul,momentumSmear_smul,RingHom.id_apply]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_add
#print axioms F1Fecho.MaxwellGlobal.globalCoefficient_smul
#print axioms F1Fecho.MaxwellGlobal.spacetimeSmearLinear
