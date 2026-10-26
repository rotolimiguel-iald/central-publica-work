import TGLExt.F1Fecho394.HalfModularStripR3
import TGLExt.F1Fecho394.CanonicalWedge
/-! The strip for the actual canonical one-particle multiplier, with the
existing Fourier convention (sigma=4*pi^2*xi). The half-modular domain and
real boundary are derived from TW and B0; neither is supplied as an input. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped InnerProductSpace
namespace F1Fecho.CanonicalH1Strip
open AuditF13v31 TGLExt.ImportedSQ F1Rede.Canonical F1Rede.CanonicalWedge
open F1Fecho.StripPhase F1Fecho.StripIntegral F1Fecho.HalfModularStrip
open ChatgptAudit.PositiveEnergy016

theorem sigma_measurable : Measurable canonicalSigma := by
  unfold canonicalSigma
  fun_prop

theorem half_ae (f : TW.domain) :
    half canonicalSigma (Phi (f:H1)) =ᵐ[volume] (Phi (TW f) : ℝ→TransverseFiber) := by
  have ht := (TW_multiplier (f:H1) (TW f)).mp (TW.mem_graph f)
  filter_upwards [ht] with ξ hξ
  rw [hξ]
  unfold half canonicalSigma
  congr 1
  congr 1
  ring

theorem half_memLp (f : TW.domain) : MemLp (half canonicalSigma (Phi (f:H1))) 2 volume :=
  (memLp_congr_ae (half_ae f)).mpr (Lp.memLp (Phi (TW f)))

def coefficient (f g : H1) : ℂ→ℂ :=
  transform volume (fun ξ => inner ℂ (Phi f ξ) (Phi g ξ)) canonicalSigma

theorem coefficient_analytic (f g : TW.domain) :
    DiffContOnCl ℂ (coefficient f g) {z : ℂ | 0<z.im ∧ z.im<1} :=
  HalfModularStrip.coefficient_analytic volume canonicalSigma sigma_measurable
    (Phi (f:H1)) (Phi (g:H1)) (Lp.memLp _) (Lp.memLp _) (half_memLp f) (half_memLp g)

theorem coefficient_bounded (f g : TW.domain) : ∃ C : ℝ,
    ∀ z : ℂ, 0≤z.im → z.im≤1 → ‖coefficient f g z‖≤C := by
  have hb := moment_integrable volume canonicalSigma sigma_measurable
    (Phi (f:H1)) (Phi (g:H1)) (Lp.memLp _) (Lp.memLp _) (half_memLp f) (half_memLp g)
  exact ⟨_,fun z h0 h1 => transform_bound volume _ _ hb z h0 h1⟩

theorem coefficient_real (f g : H1) (t : ℝ) :
    coefficient f g t = inner ℂ f (B0 (2*Real.pi*t) g) := by
  have ht := canonical_modularGroupIsBoost (-t) g
  have he : -(2*Real.pi*(-t))=2*Real.pi*t := by ring
  rw [he] at ht
  unfold coefficient transform
  rw [← Phi.inner_map_map f (B0 (2*Real.pi*t) g),L2.inner_def]
  apply integral_congr_ae
  filter_upwards [ht] with ξ hξ
  try dsimp only
  rw [hξ,inner_smul_right]
  have hp : phase (t:ℂ) (canonicalSigma ξ) =
      Complex.exp (((-t*canonicalSigma ξ : ℝ) : ℂ)*Complex.I) := by
    unfold phase spectralPhase
    congr 1
    push_cast
    ring
  rw [hp]
  ring

theorem coefficient_top (f g : TW.domain) (t : ℝ) :
    coefficient f g ((t:ℂ)+Complex.I) = inner ℂ (TW f) (B0 (2*Real.pi*t) (TW g)) := by
  rw [← coefficient_real]
  change transform volume _ canonicalSigma ((t:ℂ)+Complex.I) = _
  rw [HalfModularStrip.coefficient_top]
  apply integral_congr_ae
  filter_upwards [half_ae f,half_ae g] with ξ hf hg
  try dsimp only
  rw [hf,hg]

end F1Fecho.CanonicalH1Strip
#print axioms F1Fecho.CanonicalH1Strip.half_memLp
#print axioms F1Fecho.CanonicalH1Strip.coefficient_analytic
#print axioms F1Fecho.CanonicalH1Strip.coefficient_bounded
#print axioms F1Fecho.CanonicalH1Strip.coefficient_real
#print axioms F1Fecho.CanonicalH1Strip.coefficient_top
