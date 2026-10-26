import AxisCompactProfileDensityR4
import SmoothScreenDualTensorR5
import SmoothCompactGraphExtensionR1
import SpacetimeMomentumSplitR2
import PhysicalSchwartzMaxwellR1
import Mathlib.Analysis.Calculus.ContDiff.WithLp

/-! Actual spacetime Schwartz tests recover every compact smooth momentum
profile avoiding the gauge axis. Density is concluded from the measured-null
axis cutoff, not assumed as a property of the physical smearing map. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016
open scoped ContDiff

theorem axisCompactProfile_mem_range_physicalSmear (h : H1)
    (hh : AxisCompactProfile h) : h∈Set.range physicalSmearCLM := by
  trace "density stage 0: unpack chart profile"
  change F1Fecho.SmoothLinearMomentumCutoff.AwaySmoothCompactProfile transverseProjection (orbitalMeasure 0) h at hh
  obtain ⟨g,he,hc,hd,ε,hε,hv⟩:=hh
  trace "density stage 1: profile unpacked"
  let v : MomentumCoordinates→Fin 2→ℂ := fun y=>WithLp.ofLp (g y)
  have hvd : ContDiff ℝ ∞ v := PiLp.contDiff_ofLp.comp hd
  trace "density stage 2: ofLp smooth"
  have hvc : HasCompactSupport v := hc.comp_left (by rfl)
  have hv0 : ∀y : MomentumCoordinates, ‖y.1‖≤ε → v y=0 := by
    intro y hy
    have hz:=hv y hy
    change WithLp.ofLp (g y)=0
    rw [hz]
    rfl
  trace "density stage 3: profile dual"
  let d : MomentumCoordinates→TensorValue := fun y μ ν=>screenDualTensor y.1 (v y) μ ν
  have hdd : ContDiff ℝ ∞ d := screenDualProfile_smooth v hvd ε hε hv0
  trace "density stage 3a: dual smooth"
  have hdc : HasCompactSupport d := screenDualProfile_compact v hvc
  trace "density stage 3b: dual compact"
  have hex : ∃F : ℝ×MomentumCoordinates→TensorValue,
      ContDiff ℝ ∞ F ∧ HasCompactSupport F ∧ ∀y,F (shellEnergy y,y)=d y :=
    F1Fecho.SmoothGraphExtension.exists_extension (E:=MomentumCoordinates) (V:=TensorValue)
      d hdd hdc shellEnergy shellEnergy_continuous
  obtain ⟨F,hFd,hFc,hF⟩:=hex
  trace "density stage 4: graph extended"
  let G : Spacetime→TensorValue := F ∘ splitMomentum
  have hGd : ContDiff ℝ ∞ G := hFd.comp splitMomentum.contDiff
  have hGc : HasCompactSupport G := hFc.comp_homeomorph splitMomentum.toHomeomorph
  let test : SchwartzTensor := hGc.toSchwartzMap hGd
  trace "density stage 5: test built"
  obtain ⟨f,hf⟩:=physicalFourier_surjective test
  refine ⟨f,?_⟩
  trace "density stage 6: Fourier inverse chosen"
  apply Lp.ext
  filter_upwards [physicalSmear_ae f,he,transverseProjection_ne_zero_ae] with y hy hyh hya
  trace "density stage 7: ae representatives"
  rw [hy,hyh]
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
    (cartesianStrength y j μ ν:ℂ)*(physicalFourierCLM f) (shellEmbedding y) μ ν=g y j
  trace "density stage 8: coefficient expression"
  rw [hf]
  have htest : test (shellEmbedding y)=screenDualTensor y.1 (v y) := by
    change F (splitMomentum (shellEmbedding y))=screenDualTensor y.1 (v y)
    rw [splitMomentum_shell,hF]
  rw [htest]
  trace "density stage 9: tensor inverse"
  exact screenDualTensor_right_inverse y hya (v y) j

theorem physicalSmear_denseRange : DenseRange physicalSmearCLM :=
  axisCompactProfile_dense.mono (fun h hh=>axisCompactProfile_mem_range_physicalSmear h hh)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_mem_range_physicalSmear
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_denseRange
