import TGLExt.F1Fecho394.CanonicalFockAntiAssemblyR4
import TGLExt.F1Fecho394.FieldWeylR3
import TGLExt.F1Fecho394.WedgeCyclicR3
/-! Concrete regular Weyl algebra and boost-flow consumer on the SAME Fock.
Ten former input fields are now supplied by derived terms. RemainingWeylInput
is still an uninhabited-by-this-file analytic record; no whole FockCertificate,
KMS/Tomita pair, physical Maxwell source or Takesaki identification is asserted.
The convention is W(f)=D(i f), preserving the one-particle Tomita sign.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.NetworkWeyl
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ
open F1Rede.BosonicFock F1Fecho.NetworkReuse F1Fecho.Antilinear
open TGLExt.ContratoQGv31 TGLExt.ContratoQGv32

structure RemainingWeylInput (D : CanonicalNetInput) where
  /-- a condição espectral é preservada pela segunda quantização [KNOWN]. -/
  Γ_positive : OneParticlePositiveEnergy →
    ∀ a ∈ forwardCone, ∀ ψ : F, ∃ G : ℂ → ℂ, DiffContOnCl ℂ G upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖G z‖ ≤ M) ∧ (∀ t : ℝ, G t = ⟪ψ, F1Rede.BosonicFock.gamma (U1 (t • a)) ψ⟫_ℂ)
  /-- sem espectro pontual em uma partícula ⟹ só o vácuo é fixo no Fock [KNOWN; demonstração escrita da
      bancada, DIAMANTE_MODULAR 16/09, por Fubini]. -/
  Γ_no_fixed : ∀ u : ℝ → (H1 ≃ₗᵢ[ℂ] H1),
    u 0 = LinearIsometryEquiv.refl ℂ H1 → (∀ s t, u (s + t) = (u t).trans (u s)) →
    (∀ ξ, Continuous (fun s => u s ξ)) →
    (∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0) →
    ∀ ψ : F, (∀ l : ℝ, F1Rede.BosonicFock.gamma (u l) ψ = ψ) → ψ ∈ (ℂ ∙ F1Rede.BosonicFock.vacuum)
  wedge_nonabelian : ∃ a ∈ FieldWeyl.R (D.K rightWedge), ∃ b ∈ FieldWeyl.R (D.K rightWedge), a * b ≠ b * a
  /-- ★ BISOGNANO–WICHMANN da luz: o boost segundo-quantizado em 2πt satisfaz KMS a β = 1 na cunha
      [Bisognano–Wichmann 1975/76; BGL 2002 + Araki 1963]. -/
  bw_kms : KMSBody (FieldWeyl.R (D.K rightWedge)) F1Rede.BosonicFock.vacuum (fun t => F1Rede.BosonicFock.gamma (B0 (2 * Real.pi * t))) 1
  /-- a realização analítica de Tomita do par [Tomita–Takesaki]. -/
  tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra F1Rede.BosonicFock.vacuum canonicalFockJ (fun t => F1Rede.BosonicFock.gamma (B0 (-(2 * Real.pi * t))))
  /-- o núcleo de Takesaki [Takesaki 1973]. -/
  Core : Type
  [instCR : Ring Core]
  [instCS : StarRing Core]
  [instCA : Algebra ℂ Core]
  embedding : (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra →⋆ₐ[ℂ] Core
  embedding_injective : Function.Injective embedding
  dualAction : ℝ → (Core ≃⋆ₐ[ℂ] Core)
  dualAction_zero : dualAction 0 = StarAlgEquiv.refl
  dualAction_add : ∀ s t : ℝ, dualAction (s + t) = (dualAction s).trans (dualAction t)
  trace : Core → ENNReal
  trace_zero : trace 0 = 0
  trace_tracial : ∀ x y : Core, trace (x * y) = trace (y * x)
  trace_star : ∀ x : Core, trace (star x) = trace x
  trace_dual_scaling : ∀ (s : ℝ) (x : Core),
    trace ((dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * trace x
  /-- uma projeção finita não nula do núcleo II_∞, partida em duas metades de traço igual [Connes 1973]. -/
  PF : Core
  PF_sa : star PF = PF
  PF_idem : PF * PF = PF
  PF_ne : PF ≠ 0
  PF_pos : 0 < trace PF
  PF_fin : trace PF < ⊤
  Pp : Core
  Pm : Core
  Pp_sa : star Pp = Pp
  Pp_idem : Pp * Pp = Pp
  Pm_sa : star Pm = Pm
  Pm_idem : Pm * Pm = Pm
  split : Pp + Pm = PF
  orth : Pp * Pm = 0
  trace_additive : trace PF = trace Pp + trace Pm
  equal_halves : trace Pp = trace Pm

attribute [instance] RemainingWeylInput.instCR RemainingWeylInput.instCS RemainingWeylInput.instCA

def RemainingWeylInput.toAnalytic {D : CanonicalNetInput}
    (A : RemainingWeylInput D) : RemainingAnalyticInput D.toLightNetData.toLightOneParticle where
  Γ_positive := A.Γ_positive
  Γ_no_fixed := A.Γ_no_fixed
  wedge_cyclic := by
    rw [TGLExt.QGSolution.toLightOneParticle_K]
    simpa only [F1Fecho.WedgeCyclic.vacuumOrbit, ← D.wedge_glue] using
      F1Fecho.WedgeCyclic.vacuum_cyclic F1Rede.CanonicalWedge.spectralOutput.KWR
  wedge_separating := by
    rw [TGLExt.QGSolution.toLightOneParticle_K]
    simpa only [← D.wedge_glue] using
      F1Fecho.WedgeCyclic.vacuum_separating F1Rede.CanonicalWedge.spectralOutput.KWR
  wedge_nonabelian := A.wedge_nonabelian
  bw_kms := A.bw_kms
  tomita := A.tomita
  Core := A.Core
  embedding := A.embedding
  embedding_injective := A.embedding_injective
  dualAction := A.dualAction
  dualAction_zero := A.dualAction_zero
  dualAction_add := A.dualAction_add
  trace := A.trace
  trace_zero := A.trace_zero
  trace_tracial := A.trace_tracial
  trace_star := A.trace_star
  trace_dual_scaling := A.trace_dual_scaling
  PF := A.PF
  PF_sa := A.PF_sa
  PF_idem := A.PF_idem
  PF_ne := A.PF_ne
  PF_pos := A.PF_pos
  PF_fin := A.PF_fin
  Pp := A.Pp
  Pm := A.Pm
  Pp_sa := A.Pp_sa
  Pp_idem := A.Pp_idem
  Pm_sa := A.Pm_sa
  Pm_idem := A.Pm_idem
  split := A.split
  orth := A.orth
  trace_additive := A.trace_additive
  equal_halves := A.equal_halves
  instCR := A.instCR
  instCS := A.instCS
  instCA := A.instCA
  R := FieldWeyl.R
  R_mono := FieldWeyl.R_mono
  R_local := FieldWeyl.R_local
  R_cov := FieldWeyl.R_covariance
  flow := FieldWeyl.wedgeFlow D.toLightNetData
  flow_zero := FieldWeyl.wedgeFlow_zero D.toLightNetData
  flow_add := FieldWeyl.wedgeFlow_add D.toLightNetData
  flow_is_Ad := FieldWeyl.wedgeFlow_is_Ad D.toLightNetData

def RemainingWeylInput.toCertificate {D : CanonicalNetInput}
    (A : RemainingWeylInput D) : FockCertificate D.toLightNetData.toLightOneParticle :=
  A.toAnalytic.toCertificate

theorem assembled_R_is_concrete {D : CanonicalNetInput} (A : RemainingWeylInput D) :
    A.toCertificate.R = FieldWeyl.R := rfl

theorem assembled_flow_is_concrete {D : CanonicalNetInput} (A : RemainingWeylInput D) :
    A.toCertificate.flow = FieldWeyl.wedgeFlow D.toLightNetData := rfl

theorem assembled_generator_regular {D : CanonicalNetInput} (A : RemainingWeylInput D)
    (v : F) : Continuous (fun f : H1 => FieldWeyl.W f v) := FieldWeyl.W_strongly_continuous v

theorem assembled_generator_mem {D : CanonicalNetInput} (A : RemainingWeylInput D)
    (K : Submodule ℝ H1) (f : H1) (hf : f ∈ K) : FieldWeyl.W f ∈ A.toCertificate.R K :=
  FieldWeyl.W_mem_R K f hf

end F1Fecho.NetworkWeyl
#print axioms F1Fecho.NetworkWeyl.RemainingWeylInput.toCertificate
#print axioms F1Fecho.NetworkWeyl.assembled_R_is_concrete
#print axioms F1Fecho.NetworkWeyl.assembled_flow_is_concrete
#print axioms F1Fecho.NetworkWeyl.assembled_generator_regular
#print axioms F1Fecho.NetworkWeyl.assembled_generator_mem
