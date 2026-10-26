import TGLExt.F1Fecho394.BosonicFockContinuity
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.F1Fecho394.CanonicalOutput
import TGLExt.F1Fecho394.ConcreteLightRayNet
import TGLExt.QGSolutionComplete
import TGLExt.MaxwellLiteratureBridge
/-!
Concrete wiring, not a claim that the remaining imported fields are inhabited.
The canonical H1, standard wedge and bosonic Fock are reused without rebuilding.
Only genuinely remaining Fock fields are inputs. The scalar light-ray net is
retained as a separately typed construction; no scalar-to-4D identification is
claimed. Gamma(J) and exponential-vector totality belong to preexisting jobs.
No new axiom, no physical H3 derivation, no global solution or device equivalence.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.NetworkReuse
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open TGLExt.ContratoQGv32 TGLExt.ImportedSQ TGLExt.QGSolution
open F1Rede.BosonicFock

structure CanonicalNetInput extends LightNetData where
  wedge_glue : toLightNetData.K rightWedge =
    F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule

def CanonicalNetInput.toStandardWedge (D : CanonicalNetInput) :
    AuditF13v31.LightNetStandardWedgeDataBGL where
  toLightNetData := D.toLightNetData
  out := F1Rede.CanonicalWedge.spectralOutput
  wedge_glue := D.wedge_glue

theorem canonical_wedge_nonzero (D : CanonicalNetInput) :
    ∃ f : H1, f ∈ D.K rightWedge ∧ f ≠ 0 := by
  obtain ⟨f,hf,hn⟩ := F1Rede.CanonicalWedge.spectralOutput_nonzero
  refine ⟨f,?_,hn⟩
  rw [D.wedge_glue]
  exact hf

theorem zero_wedge_refused (D : CanonicalNetInput) : D.K rightWedge ≠ ⊥ := by
  intro h
  obtain ⟨f,hf,hn⟩ := canonical_wedge_nonzero D
  rw [h] at hf
  exact hn hf

def canonicalWedgeInFock : Submodule ℝ F :=
  F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule.map
    (oneParticle.toLinearMap.restrictScalars ℝ)

theorem canonicalWedgeInFock_nonzero :
    ∃ f : F, f ∈ canonicalWedgeInFock ∧ f ≠ 0 := by
  obtain ⟨x,hx,hn⟩ := F1Rede.CanonicalWedge.spectralOutput_nonzero
  refine ⟨oneParticle x,⟨x,hx,rfl⟩,?_⟩
  intro hz
  apply hn
  apply oneParticle.injective
  simpa using hz

theorem concrete_kinematics_inhabited :
    ‖vacuum‖ = 1 ∧ ¬ FiniteDimensional ℂ F :=
  ⟨vacuum_norm,infinite_dimensional⟩

theorem scalar_halfline_still_nonzero (a : ℝ) :
    (F1Rede.LightRay.halfline a).toClosedSubmodule ≠ ⊥ :=
  F1Rede.LightRay.halfline_ne_bot a

/-- All fields below remain named inputs on the already constructed Fock.
This record has no asserted inhabitant. Kinematic fields are deliberately absent. -/
structure RemainingFockInput (L : LightOneParticle) where
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
  /-- a álgebra de Weyl de um subespaço real [Araki 1963]. -/
  R : Submodule ℝ H1 → VonNeumannAlgebra F
  R_mono : ∀ K K' : Submodule ℝ H1, K ≤ K' → (R K : Set (F →L[ℂ] F)) ⊆ R K'
  R_local : ∀ K K' : Submodule ℝ H1, (∀ f ∈ K, ∀ g ∈ K', (⟪f, g⟫_ℂ).im = 0) →
    ∀ x ∈ R K, ∀ y ∈ R K', Commute x y
  /-- covariância funtorial: se u leva K em K', Ad F1Rede.BosonicFock.gamma(u) leva R K em R K'. -/
  R_cov : ∀ (u : H1 ≃ₗᵢ[ℂ] H1) (K K' : Submodule ℝ H1), (∀ f, f ∈ K ↔ u f ∈ K') →
    ∀ x : F →L[ℂ] F, x ∈ R K ↔ (F1Rede.BosonicFock.gamma u).conjStarAlgEquiv x ∈ R K'
  /-- Reeh–Schlieder na cunha (K(W) padrão) [Araki 1963; BGL 2002]. -/
  wedge_cyclic : Dense ((Submodule.span ℂ
      ((fun T : F →L[ℂ] F => T F1Rede.BosonicFock.vacuum) '' (R (L.K rightWedge) : Set (F →L[ℂ] F))) : Submodule ℂ F) : Set F)
  wedge_separating : ∀ a ∈ R (L.K rightWedge), (a : F →L[ℂ] F) F1Rede.BosonicFock.vacuum = 0 → a = 0
  wedge_nonabelian : ∃ a ∈ R (L.K rightWedge), ∃ b ∈ R (L.K rightWedge), a * b ≠ b * a
  /-- ★ BISOGNANO–WICHMANN da luz: o boost segundo-quantizado em 2πt satisfaz KMS a β = 1 na cunha
      [Bisognano–Wichmann 1975/76; BGL 2002 + Araki 1963]. -/
  bw_kms : KMSBody (R (L.K rightWedge)) F1Rede.BosonicFock.vacuum (fun t => F1Rede.BosonicFock.gamma (B0 (2 * Real.pi * t))) 1
  /-- a conjugação modular [Tomita–Takesaki; BGL 2002 — o PCT]. -/
  J : F ≃ₛₗᵢ[starRingEnd ℂ] F
  J_invol : ∀ ξ : F, J (J ξ) = ξ
  J_vac : J F1Rede.BosonicFock.vacuum = F1Rede.BosonicFock.vacuum
  /-- a realização analítica de Tomita do par [Tomita–Takesaki]. -/
  tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (R (L.K rightWedge)).toStarSubalgebra F1Rede.BosonicFock.vacuum J (fun t => F1Rede.BosonicFock.gamma (B0 (-(2 * Real.pi * t))))
  /-- o fluxo modular como automorfismo da cunha (Ad Δ^{it} preserva M) [Tomita–Takesaki]. -/
  flow : ℝ → ((R (L.K rightWedge)).toStarSubalgebra ≃⋆ₐ[ℂ] (R (L.K rightWedge)).toStarSubalgebra)
  flow_zero : flow 0 = StarAlgEquiv.refl
  flow_add : ∀ s t : ℝ, flow (s + t) = (flow s).trans (flow t)
  flow_is_Ad : ∀ (t : ℝ) (a : (R (L.K rightWedge)).toStarSubalgebra),
    ((flow t) a).val = (F1Rede.BosonicFock.gamma (B0 (-(2 * Real.pi * t)))).conjStarAlgEquiv a.val
  /-- o núcleo de Takesaki [Takesaki 1973]. -/
  Core : Type
  [instCR : Ring Core]
  [instCS : StarRing Core]
  [instCA : Algebra ℂ Core]
  embedding : (R (L.K rightWedge)).toStarSubalgebra →⋆ₐ[ℂ] Core
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

attribute [instance] RemainingFockInput.instCR RemainingFockInput.instCS RemainingFockInput.instCA

def RemainingFockInput.toCertificate {L : LightOneParticle}
    (A : RemainingFockInput L) : FockCertificate L where
  F := F
  instN := inferInstance
  instI := inferInstance
  instC := inferInstance
  Ω := vacuum
  Ω_norm := vacuum_norm
  F_infinite := infinite_dimensional
  Γ := gamma
  Γ_refl := gamma_refl
  Γ_trans := gamma_trans
  Γ_vac := gamma_vacuum
  ι := oneParticle
  Γ_one_particle := gamma_oneParticle
  Γ_strong := gamma_strong_real
  Γ_strong4 := gamma_strong_spacetime
  Γ_positive := A.Γ_positive
  Γ_no_fixed := A.Γ_no_fixed
  R := A.R
  R_mono := A.R_mono
  R_local := A.R_local
  R_cov := A.R_cov
  wedge_cyclic := A.wedge_cyclic
  wedge_separating := A.wedge_separating
  wedge_nonabelian := A.wedge_nonabelian
  bw_kms := A.bw_kms
  J := A.J
  J_invol := A.J_invol
  J_vac := A.J_vac
  tomita := A.tomita
  flow := A.flow
  flow_zero := A.flow_zero
  flow_add := A.flow_add
  flow_is_Ad := A.flow_is_Ad
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

theorem assembled_F_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.F = F := rfl
theorem assembled_gamma_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.Γ = gamma := rfl
theorem assembled_inclusion_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.ι = oneParticle := rfl
theorem assembled_boost_is_concrete {L : LightOneParticle} (A : RemainingFockInput L)
    (s : ℝ) (f : F) : (lightBoost A.toCertificate).V s f = gamma (B0 s) f := rfl
theorem assembled_modular_parameter {L : LightOneParticle} (A : RemainingFockInput L)
    (t : ℝ) : lightDelta A.toCertificate t = gamma (B0 (-(2*Real.pi*t))) := rfl

/-- Existing H2/H3 consumer instantiated on this concrete kinematic Fock.
Maxwell and the remaining analytic fields stay explicit hypotheses. -/
theorem canonical_contract_from_named_imports (D : CanonicalNetInput)
    (A : RemainingFockInput D.toLightNetData.toLightOneParticle)
    (M : MaxwellCertificate A.toCertificate) (N : KillingNormalization)
    (G : ℝ) (hG : 0 < G) :
    ∃ h2 : ContratoH2v32 (lightNet A.toCertificate) (lightRealization A.toCertificate) N,
      Nonempty (ContratoImportH3v32 (lightNet A.toCertificate) (lightRealization A.toCertificate)
        N (lightBoost A.toCertificate) M.T h2) :=
  qg_contract_from_the_cited_net D.toLightNetData A.toCertificate M N G hG

end F1Fecho.NetworkReuse

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.NetworkReuse).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
