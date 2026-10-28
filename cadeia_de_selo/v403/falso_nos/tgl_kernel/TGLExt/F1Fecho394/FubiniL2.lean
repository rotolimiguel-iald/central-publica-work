import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.SeparableMeasure
import Mathlib.MeasureTheory.Function.LpSpace.Complete
import Mathlib.Tactic
import TGLExt.LightNetStandardWedgeDataBGL
set_option autoImplicit false
set_option maxHeartbeats 1200000
open MeasureTheory Filter Topology
open scoped ENNReal


namespace F1Rede

theorem measurable_of_distances {X Y : Type*} [MeasurableSpace X]
    [MetricSpace Y] [SecondCountableTopology Y] [MeasurableSpace Y] [BorelSpace Y]
    (f : X → Y) (hf : ∀ y, Measurable (fun x => dist (f x) y)) : Measurable f := by
  apply measurable_of_isOpen
  intro s hs
  let B : Set (Set Y) := {b | ∃ y r, b = Metric.ball y r ∧ b ⊆ s}
  have hB : ∀ b ∈ B, IsOpen b := by
    rintro b ⟨y,r,rfl,_⟩
    exact Metric.isOpen_ball
  have hBs : ⋃₀ B = s := by
    apply Set.Subset.antisymm
    · rintro y ⟨b, ⟨z,r,rfl,hsub⟩,hy⟩
      exact hsub hy
    · intro y hy
      obtain ⟨r,hr,hsub⟩ := Metric.isOpen_iff.mp hs y hy
      exact ⟨Metric.ball y r, ⟨y,r,rfl,hsub⟩, Metric.mem_ball_self hr⟩
  obtain ⟨C,hC,hCB,hCover⟩ := TopologicalSpace.isOpen_sUnion_countable B hB
  rw [← hBs, ← hCover, Set.preimage_sUnion]
  apply MeasurableSet.biUnion hC
  intro b hb
  obtain ⟨y,r,rfl,_⟩ := hCB hb
  exact measurableSet_lt (hf y) measurable_const

variable {α β E : Type*} [MeasurableSpace α] [MeasurableSpace β]
  [NormedAddCommGroup E] {μ : Measure α} {ν : Measure β} [SFinite μ] [SFinite ν]

theorem memLp_section_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, MemLp (fun x => f (x,y)) 2 μ := by
  have hint := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)
  filter_upwards [hint.prod_left_ae] with y hy
  exact (memLp_two_iff_integrable_sq_norm
    ((Lp.stronglyMeasurable f).comp_measurable (measurable_id.prodMk measurable_const)).aestronglyMeasurable).mpr hy

noncomputable def sectionLp (f : Lp E 2 (μ.prod ν)) (y : β) : Lp E 2 μ := by
  classical
  exact if h : MemLp (fun x => f (x,y)) 2 μ then h.toLp (fun x => f (x,y)) else 0

theorem sectionLp_coe_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, (sectionLp f y : α → E) =ᵐ[μ] fun x => f (x,y) := by
  classical
  filter_upwards [memLp_section_ae f] with y hy
  simp only [sectionLp, dif_pos hy]
  exact hy.coeFn_toLp

theorem measurable_section_eLpNorm (f : α × β → E) (hf : StronglyMeasurable f) :
    Measurable (fun y => eLpNorm (fun x => f (x,y)) 2 μ) := by
  simp_rw [eLpNorm_eq_lintegral_rpow_enorm_toReal (by norm_num : (2:ℝ≥0∞) ≠ 0)
    (by norm_num : (2:ℝ≥0∞) ≠ ⊤)]
  exact ((hf.enorm.pow_const _).lintegral_prod_left').pow_const _

theorem measurableSet_good_sections (f : Lp E 2 (μ.prod ν)) :
    MeasurableSet {y | MemLp (fun x => f (x,y)) 2 μ} := by
  have heq : {y | MemLp (fun x => f (x,y)) 2 μ} =
      {y | eLpNorm (fun x => f (x,y)) 2 μ < ⊤} := by
    ext y
    exact and_iff_right ((Lp.stronglyMeasurable f).comp_measurable
      (measurable_id.prodMk measurable_const)).aestronglyMeasurable
  rw [heq]
  exact measurableSet_lt (measurable_section_eLpNorm f (Lp.stronglyMeasurable f)) measurable_const

theorem sectionLp_dist (f : Lp E 2 (μ.prod ν)) (g : Lp E 2 μ) (y : β)
    (hy : MemLp (fun x => f (x,y)) 2 μ) :
    dist (sectionLp f y) g = (eLpNorm (fun x => f (x,y) - g x) 2 μ).toReal := by
  classical
  rw [sectionLp, dif_pos hy, Lp.dist_def]
  congr 1
  apply eLpNorm_congr_ae
  exact hy.coeFn_toLp.sub ae_eq_rfl

theorem sectionLp_stronglyMeasurable [IsSeparable μ] [TopologicalSpace.SeparableSpace E]
    (f : Lp E 2 (μ.prod ν)) : StronglyMeasurable (sectionLp f) := by
  classical
  letI : Fact ((2:ℝ≥0∞) ≠ ⊤) := ⟨by norm_num⟩
  borelize ↥(Lp E 2 μ)
  apply Measurable.stronglyMeasurable
  apply measurable_of_distances
  intro g
  have hm : Measurable (fun y => (eLpNorm (fun x => f (x,y) - g x) 2 μ).toReal) :=
    (measurable_section_eLpNorm (fun z => f z - g z.1)
      ((Lp.stronglyMeasurable f).sub ((Lp.stronglyMeasurable g).comp_measurable measurable_fst))).ennreal_toReal
  have hp : Measurable (fun y => if MemLp (fun x => f (x,y)) 2 μ then
      (eLpNorm (fun x => f (x,y) - g x) 2 μ).toReal else dist 0 g) :=
    hm.piecewise (measurableSet_good_sections f) (measurable_const (a := dist 0 g))
  convert hp using 1
  ext y
  by_cases hy : MemLp (fun x => f (x,y)) 2 μ
  · simp only [hy, if_true]
    exact sectionLp_dist f g y hy
  · simp [sectionLp, hy]

section RealInner
variable [InnerProductSpace ℝ E]

theorem norm_sq_integral (f : Lp E 2 μ) :
    ‖f‖^2 = ∫ x, ‖f x‖^2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, L2.inner_def]
  simp only [real_inner_self_eq_norm_sq]

theorem sectionLp_norm_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, ‖sectionLp f y‖^2 = ∫ x, ‖f (x,y)‖^2 ∂μ := by
  filter_upwards [sectionLp_coe_ae f] with y hy
  rw [norm_sq_integral]
  exact integral_congr_ae (hy.mono fun x hx => by simpa only using congrArg (fun z : E => ‖z‖^2) hx)

theorem norm_sq_disintegration (f : Lp E 2 (μ.prod ν)) :
    ‖f‖^2 = ∫ y, ‖sectionLp f y‖^2 ∂ν := by
  rw [norm_sq_integral, integral_prod_symm]
  · exact integral_congr_ae ((sectionLp_norm_ae f).mono fun _ hy => hy.symm)
  · exact (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)


variable [IsSeparable μ] [TopologicalSpace.SeparableSpace E]

theorem sectionLp_memLp (f : Lp E 2 (μ.prod ν)) : MemLp (sectionLp f) 2 ν := by
  apply (memLp_two_iff_integrable_sq_norm (sectionLp_stronglyMeasurable f).aestronglyMeasurable).mpr
  have hint := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)
  exact hint.integral_prod_right.congr ((sectionLp_norm_ae f).mono fun y hy => hy.symm)

noncomputable def curryLp (f : Lp E 2 (μ.prod ν)) : Lp (Lp E 2 μ) 2 ν :=
  (sectionLp_memLp f).toLp (sectionLp f)

theorem curryLp_coe_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, (curryLp f y : α → E) =ᵐ[μ] fun x => f (x,y) := by
  filter_upwards [(sectionLp_memLp f).coeFn_toLp, sectionLp_coe_ae f] with y hy hz
  simpa only [curryLp, hy] using hz

theorem curryLp_norm (f : Lp E 2 (μ.prod ν)) : ‖curryLp f‖ = ‖f‖ := by
  have heq : ‖curryLp f‖^2 = ‖f‖^2 := by
    rw [norm_sq_integral, norm_sq_disintegration]
    apply integral_congr_ae
    filter_upwards [(sectionLp_memLp f).coeFn_toLp] with y hy
    exact congrArg (fun v : Lp E 2 μ => ‖v‖^2) hy
  nlinarith [norm_nonneg (curryLp f), norm_nonneg f]

theorem ae_ae_reverse {p : α × β → Prop} (h : ∀ᵐ z ∂μ.prod ν, p z) :
    ∀ᵐ y ∂ν, ∀ᵐ x ∂μ, p (x,y) := by
  exact Measure.ae_ae_of_ae_prod (Measure.measurePreserving_swap.quasiMeasurePreserving.ae h)

theorem curryLp_add (f g : Lp E 2 (μ.prod ν)) : curryLp (f+g) = curryLp f + curryLp g := by
  apply Lp.ext
  filter_upwards [curryLp_coe_ae (f+g), curryLp_coe_ae f, curryLp_coe_ae g,
    ae_ae_reverse (Lp.coeFn_add f g), Lp.coeFn_add (curryLp f) (curryLp g)] with y hfg hf hg hadd hout
  rw [hout]
  apply Lp.ext
  filter_upwards [hfg, hf, hg, hadd, Lp.coeFn_add (curryLp f y) (curryLp g y)] with x hfgx hfx hgx haddx hsum
  simp only [Pi.add_apply] at haddx hsum
  simpa only [Pi.add_apply, hfgx, haddx, hfx, hgx] using hsum.symm

variable {𝕜 : Type*} [NormedField 𝕜] [NormedSpace 𝕜 E]

theorem curryLp_smul (c : 𝕜) (f : Lp E 2 (μ.prod ν)) : curryLp (c • f) = c • curryLp f := by
  apply Lp.ext
  filter_upwards [curryLp_coe_ae (c • f), curryLp_coe_ae f,
    ae_ae_reverse (Lp.coeFn_smul c f), Lp.coeFn_smul c (curryLp f)] with y hcf hf hsmul hout
  rw [hout]
  apply Lp.ext
  filter_upwards [hcf, hf, hsmul, Lp.coeFn_smul c (curryLp f y)] with x hcfx hfx hsmulx hsum
  simp only [Pi.smul_apply] at hsmulx hsum
  simpa only [Pi.smul_apply, hcfx, hsmulx, hfx] using hsum.symm

noncomputable def curryLinearIsometry : Lp E 2 (μ.prod ν) →ₗᵢ[𝕜] Lp (Lp E 2 μ) 2 ν where
  toFun := curryLp
  map_add' := curryLp_add
  map_smul' := curryLp_smul
  norm_map' := curryLp_norm

theorem rectangle_memLp (g : Lp E 2 μ) {s : Set β} (hs : MeasurableSet s) (hsf : ν s ≠ ⊤) :
    MemLp ((Prod.snd ⁻¹' s).indicator (fun z : α × β => g z.1)) 2 (μ.prod ν) := by
  classical
  have hm := ((Lp.stronglyMeasurable g).comp_measurable measurable_fst).indicator (hs.preimage measurable_snd)
  apply (memLp_two_iff_integrable_sq_norm hm.aestronglyMeasurable).mpr
  have hg := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable g)).mp (Lp.memLp g)
  have hs1 : Integrable (s.indicator (fun _ : β => (1:ℝ))) ν :=
    (integrable_indicator_iff hs).mpr (integrableOn_const (C := (1:ℝ)) hsf)
  have heq : (fun z : α × β => ‖(Prod.snd ⁻¹' s).indicator (fun z => g z.1) z‖ ^ 2) =
      (fun z : α × β => ‖g z.1‖ ^ 2 * s.indicator (fun _ => (1:ℝ)) z.2) := by
    funext z
    by_cases hz : z.2 ∈ s <;> simp [Set.indicator, hz]
  change Integrable (fun z : α × β => ‖(Prod.snd ⁻¹' s).indicator (fun z => g z.1) z‖ ^ 2) (μ.prod ν)
  rw [heq]
  exact hg.mul_prod hs1

theorem indicator_in_range (g : Lp E 2 μ) {s : Set β} (hs : MeasurableSet s) (hsf : ν s ≠ ⊤) :
    ∃ f : Lp E 2 (μ.prod ν), curryLp f = indicatorConstLp 2 hs hsf g := by
  classical
  let hrect := rectangle_memLp g hs hsf
  let f := hrect.toLp ((Prod.snd ⁻¹' s).indicator (fun z : α × β => g z.1))
  refine ⟨f, Lp.ext ?_⟩
  filter_upwards [curryLp_coe_ae f, ae_ae_reverse hrect.coeFn_toLp,
    (indicatorConstLp_coeFn (p := 2) (hs := hs) (hμs := hsf) (c := g))] with y hy hf hi
  rw [hi]
  by_cases hys : y ∈ s
  · simp only [Set.indicator_of_mem hys]
    apply Lp.ext
    filter_upwards [hy, hf] with x hxy hfx
    simpa [Set.indicator, hys] using hxy.trans hfx
  · simp only [Set.indicator_of_notMem hys]
    apply Lp.ext
    filter_upwards [hy, hf, Lp.coeFn_zero (E := E) (p := 2) (μ := μ)] with x hxy hfx hz
    rw [hz]
    simpa [Set.indicator, hys] using hxy.trans hfx

variable [CompleteSpace E]

theorem curryLinearIsometry_surjective :
    Function.Surjective (curryLinearIsometry (𝕜 := 𝕜) (E := E) (μ := μ) (ν := ν)) := by
  let L := curryLinearIsometry (𝕜 := 𝕜) (E := E) (μ := μ) (ν := ν)
  apply Lp.induction (by norm_num : (2:ℝ≥0∞) ≠ ⊤) (fun y => ∃ x, L x = y)
  · intro c s hs hsf
    rw [Lp.simpleFunc.coe_indicatorConst]
    exact indicator_in_range c hs hsf.ne
  · intro f g hf hg hdisj hfr hgr
    obtain ⟨x,hx⟩ := hfr
    obtain ⟨y,hy⟩ := hgr
    exact ⟨x+y, by rw [map_add, hx, hy]⟩
  · exact L.isometry.isClosedEmbedding.isClosed_range

noncomputable def fubiniL2Equiv : Lp E 2 (μ.prod ν) ≃ₗᵢ[𝕜] Lp (Lp E 2 μ) 2 ν :=
  LinearIsometryEquiv.ofSurjective curryLinearIsometry curryLinearIsometry_surjective
end RealInner

namespace Canonical
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open AuditF13v31

/-- Actual vector-valued Fubini currification on the unchanged canonical momentum Hilbert space.
It is constructed from measurable sections, disintegration of the squared norm, and density of
finite-measure indicators; its existence is not an input field. -/
noncomputable def canonicalFub : Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert := by
  letI : InnerProductSpace ℝ Fib := InnerProductSpace.complexToReal
  exact fubiniL2Equiv (𝕜 := ℂ) (μ := (volume : Measure Transverse)) (ν := (volume : Measure ℝ))

/-- The new equivalence really sends f(q,r) to r ↦ [q ↦ f(q,r)] almost everywhere. -/
theorem canonicalFub_sections (f : Lp Fib 2 momentumMeasure) :
    ∀ᵐ r ∂(volume : Measure ℝ), (canonicalFub f r : Transverse → Fib) =ᵐ[volume]
      fun q => f (q,r) := by
  letI : InnerProductSpace ℝ Fib := InnerProductSpace.complexToReal
  exact curryLp_coe_ae f

/-- D1a.1 now has an actual partial Fourier equivalence on H1, without changing H1 or its measure. -/
noncomputable def canonicalPartialFourier : H1 ≃ₗᵢ[ℂ] RapidityHilbert :=
  partialFourier canonicalFub


/-- Currification preserves the actual rapidity translation; no arbitrary Hilbert-space identification. -/
theorem canonicalFub_shift (s : ℝ) (f : Lp Fib 2 momentumMeasure) :
    canonicalFub (productRapidityShift s f) = TGLV350.Regular.shift s (canonicalFub f) := by
  apply Lp.ext
  filter_upwards [canonicalFub_sections (productRapidityShift s f),
    TGLV350.Regular.shift_ae s (canonicalFub f),
    (measurePreserving_sub_right (volume : Measure ℝ) s).quasiMeasurePreserving.ae
      (canonicalFub_sections f),
    ae_ae_reverse (μ := (volume : Measure Transverse)) (ν := (volume : Measure ℝ))
      (productRapidityShift_ae s f)] with r hc hs hf hp
  rw [hs]
  apply Lp.ext
  filter_upwards [hc, hf, hp] with q hqc hqf hqp
  rw [hqc, hqf, hqp]
  simp only [coordinateShift, sub_eq_add_neg]

/-- The canonical orbital boost becomes translation before the partial Fourier transform. -/
theorem canonical_toRapidity_boost (s : ℝ) (f : H1) :
    canonicalFub (toRapidity (B0 s f)) = TGLV350.Regular.shift s (canonicalFub (toRapidity f)) := by
  change canonicalFub (orbitalL2Pullback 0 (orbitalScalarBoost 0 s f)) = _
  rw [orbitalScalarBoost_intertwines, canonicalFub_shift]
  rfl

/-- Fourier convention is pinned by the existing V351 translation theorem (the factor is 2*pi*s). -/
theorem canonicalPartialFourier_boost (s : ℝ) (f : H1) :
    canonicalPartialFourier (B0 s f) =
      TGLV350.Regular.characterMultiplier (2 * Real.pi * s) (canonicalPartialFourier f) := by
  change Lp.fourierTransformₗᵢ ℝ TransverseFiber (canonicalFub (toRapidity (B0 s f))) = _
  rw [canonical_toRapidity_boost, TGLV350.Regular.fourier_shift]
  rfl

/-- The symbol compatible with B0(-2*pi*t) and mathlib's Fourier normalization. -/
noncomputable def canonicalSigma (ξ : ℝ) : ℝ := 4 * Real.pi ^ 2 * ξ

/-- The modular-group field of D1a.3 has a concrete spectral representation; no claim about J or S. -/
theorem canonical_modularGroupIsBoost : ModularGroupIsBoost canonicalPartialFourier canonicalSigma := by
  intro t f
  rw [canonicalPartialFourier_boost]
  filter_upwards [TGLV350.Regular.characterMultiplier_ae
    (2 * Real.pi * (-(2 * Real.pi * t))) (canonicalPartialFourier f)] with ξ hξ
  rw [hξ]
  congr 1
  unfold canonicalSigma
  congr 1
  push_cast
  ring
#print axioms canonicalFub

#print axioms canonicalFub_sections
#print axioms canonicalPartialFourier
#print axioms canonicalFub_shift
#print axioms canonicalPartialFourier_boost
#print axioms canonical_modularGroupIsBoost
end Canonical
#print axioms memLp_section_ae
#print axioms sectionLp_coe_ae
#print axioms norm_sq_integral
#print axioms sectionLp_norm_ae
#print axioms norm_sq_disintegration
#print axioms sectionLp_stronglyMeasurable
#print axioms sectionLp_memLp
#print axioms curryLp_coe_ae
#print axioms curryLp_norm
#print axioms curryLinearIsometry
#print axioms fubiniL2Equiv
end F1Rede
