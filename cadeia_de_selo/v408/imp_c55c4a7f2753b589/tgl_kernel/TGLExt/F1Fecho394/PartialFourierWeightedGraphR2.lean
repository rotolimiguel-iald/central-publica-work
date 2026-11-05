import TGLExt.F1Fecho394.PartialFourierRepresentativeR4

/-! Transfer of a genuine section Fourier identity to the actual L2 multiplier
graph. Both vectors are already L2; section integrability is explicit. No
weighted-domain assertion is assumed in the conclusion. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped FourierTransform
namespace F1Fecho.PartialFourierRepresentative
open FourierFubini
variable {X E : Type} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
variable (μ : Measure X) [SFinite μ] [IsSeparable μ]
local instance : InnerProductSpace ℝ E := InnerProductSpace.complexToReal

theorem curry_weighted_ae (f g : Lp E 2 (μ.prod (volume : Measure ℝ)))
    (w : ℝ → ℂ)
    (hfg : g =ᵐ[μ.prod volume] fun z => w z.2 • f z) :
    (F1Rede.fubiniL2Equiv (𝕜:=ℂ) g : ℝ → Lp E 2 μ) =ᵐ[volume]
      fun p => w p • F1Rede.fubiniL2Equiv (𝕜:=ℂ) f p := by
  filter_upwards [F1Rede.curryLp_coe_ae g,F1Rede.curryLp_coe_ae f,
    F1Rede.ae_ae_reverse hfg] with p hg hf h
  change (F1Rede.fubiniL2Equiv (𝕜:=ℂ) g p : X → E) =ᵐ[μ] _ at hg
  change (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f p : X → E) =ᵐ[μ] _ at hf
  apply Lp.ext
  filter_upwards [hg,hf,h,Lp.coeFn_smul (w p)
    (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f p)] with x hgx hfx hx hs
  simpa only [Pi.smul_apply,hgx,hfx,hx] using hs.symm

theorem partial_weighted_graph
    (f g : Lp E 2 (μ.prod (volume : Measure ℝ)))
    (hf : ∀ᵐ x ∂μ, Integrable (fun r : ℝ => f (x,r)))
    (hg : ∀ᵐ x ∂μ, Integrable (fun r : ℝ => g (x,r)))
    (w : ℝ → ℂ) (hw : Continuous w)
    (hbalance : ∀ᵐ x ∂μ, ∀ᵐ p ∂(volume : Measure ℝ),
      𝓕 (fun r : ℝ => g (x,r)) p = w p • 𝓕 (fun r : ℝ => f (x,r)) p) :
    (outerFourier μ (F1Rede.fubiniL2Equiv (𝕜:=ℂ) g) : ℝ → Lp E 2 μ) =ᵐ[volume]
      fun p => w p • outerFourier μ (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f) p := by
  have hs : ∀ᵐ x ∂μ, ∀ᵐ p ∂(volume : Measure ℝ),
      partialTransform μ g (x,p)=w p • partialTransform μ f (x,p) := by
    filter_upwards [partial_section_fourier_ae μ f hf,
      partial_section_fourier_ae μ g hg,hbalance] with x hfx hgx hb
    filter_upwards [hfx,hgx,hb] with p hfp hgp hbp
    rw [hfp,hgp,hbp]
  have hm : StronglyMeasurable (fun z : X×ℝ => w z.2 • partialTransform μ f z) :=
    (hw.stronglyMeasurable.comp_measurable measurable_snd).smul
      (Lp.stronglyMeasurable (partialTransform μ f))
  have he := (Lp.stronglyMeasurable (partialTransform μ g)).measurableSet_eq_fun hm
  have hp : partialTransform μ g =ᵐ[μ.prod volume]
      fun z => w z.2 • partialTransform μ f z := (Measure.ae_prod_iff_ae_ae he).mpr hs
  have h := curry_weighted_ae μ (partialTransform μ f) (partialTransform μ g) w hp
  simpa only [partialTransform,LinearIsometryEquiv.apply_symm_apply] using h

end F1Fecho.PartialFourierRepresentative
#print axioms F1Fecho.PartialFourierRepresentative.curry_weighted_ae
#print axioms F1Fecho.PartialFourierRepresentative.partial_weighted_graph
