import TGLExt.F1Fecho394.RealSubspaceRegularizerUniquenessR2
import TGLExt.F1Fecho394.CanonicalOneParticleBWR2
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.GaussianResolventAverageR6

/-! A closed real subspace of the canonical wedge is the whole wedge if its
complex span is dense and it is boost invariant. The bounded regularizers and
their Tomita images are constructed here from the already proved Gaussian
average. Physical localization must still supply density and boost invariance.
Ordinary complex density is never substituted for a graph-core argument. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.CanonicalWedgeUniqueness
open TGLExt.ImportedSQ F1Rede.CanonicalWedge ChatgptAudit.Continuous049
open TGLV350.Regular GaussianResolventAverage GaussianResolventRegularizer GaussianLogScalar

local instance : Module ℝ (H1→L[ℂ]H1) := Module.restrictScalars ℝ ℂ _

abbrev gaussian (n:ℕ) : H1→L[ℂ]H1 :=
  average OneParticleBW.R OneParticleBW.R_nonneg OneParticleBW.R_le_one
    OneParticleBW.R_injective OneParticleBW.R_complement_injective (scale n)

theorem factor_exists (n:ℕ) : ∃ F:H1→L[ℂ]H1,
    spectral OneParticleBW.R ((scale n)^2/4)=OneParticleBW.R*F := by
  exact ⟨_,spectral_factor OneParticleBW.R OneParticleBW.R_nonneg
    OneParticleBW.R_le_one ((scale n)^2/4)
    (div_pos (sq_pos_of_ne_zero (scale_ne_zero n)) (by norm_num))⟩

/-- A witness of the explicitly constructed CFC factor; no factor is assumed. -/
def factor (n:ℕ) : H1→L[ℂ]H1 := (factor_exists n).choose

def rootImage (n:ℕ) : H1→L[ℂ]H1 :=
  WB rootParameter * WA rootParameter * factor n

def tomitaImage (n:ℕ) : H1→SL[starRingEnd ℂ]H1 :=
  Jcandidate.toContinuousLinearEquiv.toContinuousLinearMap.comp (rootImage n)

theorem gaussian_factor (n:ℕ) : gaussian n=OneParticleBW.R*factor n := by
  rw [gaussian,average_eq_spectral _ _ _ _ _ _ (scale_ne_zero n)]
  exact (factor_exists n).choose_spec

theorem gaussian_root_graph (n:ℕ) (x:H1) :
    (gaussian n x,rootImage n x)∈TW.graph := by
  rw [gaussian_factor,OneParticleBW.R_eq]
  apply (bounded_graph_param_iff _ _ _ _ _).mpr
  refine ⟨WA rootParameter (factor n x),?_,?_⟩
  · rfl
  · rfl

theorem gaussian_mem_of_boost_invariant
    (M:Submodule ℝ H1) (hM:IsClosed (M:Set H1))
    (hboost:∀s x,x∈M→B0 s x∈M) (n:ℕ) (x:H1) (hx:x∈M) :
    gaussian n x∈M := by
  letI : InnerProductSpace ℝ H1 := InnerProductSpace.complexToReal
  change (∫t:ℝ,gaussianWeight t •
    resolventImaginaryPower OneParticleBW.R OneParticleBW.R_nonneg
      OneParticleBW.R_le_one OneParticleBW.R_injective
      OneParticleBW.R_complement_injective (scale n*t) x)∈M
  apply ClosedGraphRegularization.integral_mem M hM
  · exact ClosedGraphRegularization.weighted_orbit_integrable _
      (fun y=>(resolventImaginaryPower_strongly_continuous _ _ _ _ _ y).comp
        (continuous_const.mul continuous_id)) _ gaussianWeight_integrable x
  · apply ae_of_all
    intro t
    apply M.smul_mem
    change OneParticleBW.modularFlow (scale n*t) x∈M
    rw [OneParticleBW.modularFlow_eq_boost]
    exact hboost _ x hx

theorem tomitaImage_eq_on_KWR (n:ℕ) (x:H1)
    (hx:x∈KWR.toClosedSubmodule) : tomitaImage n x=gaussian n x := by
  have hk : gaussian n x∈KWR.toClosedSubmodule :=
    gaussian_mem_of_boost_invariant KWR.toClosedSubmodule.toSubmodule
      KWR.toClosedSubmodule.isClosed CanonicalWedgeFlow.boost_mem_KWR n x hx
  obtain ⟨hd,hfix⟩ := (KWR_mem _).mp hk
  have he : TW ⟨gaussian n x,hd⟩=rootImage n x :=
    TW.mem_graph_snd_inj (TW.mem_graph ⟨gaussian n x,hd⟩)
      (gaussian_root_graph n x) rfl
  change Jcandidate (TW ⟨gaussian n x,hd⟩)=gaussian n x at hfix
  rw [he] at hfix
  exact hfix

theorem eq_KWR_of_dense_and_boost_invariant
    (M:Submodule ℝ H1) (hM:IsClosed (M:Set H1))
    (hMK:M≤KWR.toClosedSubmodule.toSubmodule)
    (hd:(Submodule.span ℂ (M:Set H1)).topologicalClosure=⊤)
    (hboost:∀s x,x∈M→B0 s x∈M) : M=KWR.toClosedSubmodule.toSubmodule := by
  apply RealSubspaceRegularizerUniqueness.eq_of_regularizers M _ hM hMK hd
    gaussian tomitaImage
  · exact gaussian_mem_of_boost_invariant M hM hboost
  · exact tomitaImage_eq_on_KWR
  · exact average_tendsto _ _ _ _ _

end F1Fecho.CanonicalWedgeUniqueness
#print axioms F1Fecho.CanonicalWedgeUniqueness.gaussian_factor
#print axioms F1Fecho.CanonicalWedgeUniqueness.gaussian_root_graph
#print axioms F1Fecho.CanonicalWedgeUniqueness.gaussian_mem_of_boost_invariant
#print axioms F1Fecho.CanonicalWedgeUniqueness.tomitaImage_eq_on_KWR
#print axioms F1Fecho.CanonicalWedgeUniqueness.eq_KWR_of_dense_and_boost_invariant
