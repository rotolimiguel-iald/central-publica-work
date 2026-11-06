import TGLExt.F1Fecho394.BosonicGammaJR5
import TGLExt.F1Fecho394.CanonicalFockAssemblyR1
/-! The three antiunitary fields are now paid by the concrete Gamma(Jcandidate).
The remaining analytic fields stay explicit; this is not an inhabitant of the
whole FockCertificate, nor a Tomita/KMS identification from kinematics alone. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.Antilinear
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ
open F1Rede.BosonicFock F1Fecho.NetworkReuse
open TGLExt.ContratoQGv31 TGLExt.ContratoQGv32

structure RemainingAnalyticInput (L : LightOneParticle) where
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
  /-- a realização analítica de Tomita do par [Tomita–Takesaki]. -/
  tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (R (L.K rightWedge)).toStarSubalgebra F1Rede.BosonicFock.vacuum canonicalFockJ (fun t => F1Rede.BosonicFock.gamma (B0 (-(2 * Real.pi * t))))
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

attribute [instance] RemainingAnalyticInput.instCR RemainingAnalyticInput.instCS RemainingAnalyticInput.instCA

def RemainingAnalyticInput.toRemainingFock {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : RemainingFockInput L where
  J := canonicalFockJ
  J_invol := canonicalFockJ_involutive
  J_vac := canonicalFockJ_vacuum
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

def RemainingAnalyticInput.toCertificate {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : FockCertificate L := A.toRemainingFock.toCertificate

theorem assembled_J_is_concrete {L : LightOneParticle} (A : RemainingAnalyticInput L) :
    A.toCertificate.J = canonicalFockJ := rfl
theorem assembled_J_on_oneParticle {L : LightOneParticle} (A : RemainingAnalyticInput L)
    (x : H1) : A.toCertificate.J (A.toCertificate.ι x) =
      A.toCertificate.ι (F1Rede.CanonicalWedge.Jcandidate x) :=
  canonicalFockJ_oneParticle x
theorem assembled_J_involutive {L : LightOneParticle} (A : RemainingAnalyticInput L) :
    Function.Involutive A.toCertificate.J := canonicalFockJ_involutive
theorem assembled_J_preserves_existing_vacuum {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : A.toCertificate.J vacuum = vacuum := canonicalFockJ_vacuum

/-- Actual inhabitant of the antiunitary fragment, independent of the remaining
analytic input record. It acts on exactly F1Rede.BosonicFock.F. -/
theorem antiunitary_fragment_inhabited :
    ∃ j : F ≃ₛₗᵢ[starRingEnd ℂ] F,
      Function.Involutive j ∧ j vacuum = vacuum ∧
      (∀ x : H1, j (oneParticle x) = oneParticle (F1Rede.CanonicalWedge.Jcandidate x)) :=
  ⟨canonicalFockJ,canonicalFockJ_involutive,canonicalFockJ_vacuum,canonicalFockJ_oneParticle⟩

end F1Fecho.Antilinear

#print axioms F1Fecho.Antilinear.RemainingAnalyticInput.toCertificate
#print axioms F1Fecho.Antilinear.assembled_J_is_concrete
#print axioms F1Fecho.Antilinear.assembled_J_on_oneParticle
#print axioms F1Fecho.Antilinear.assembled_J_involutive
#print axioms F1Fecho.Antilinear.assembled_J_preserves_existing_vacuum
#print axioms F1Fecho.Antilinear.antiunitary_fragment_inhabited

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.Antilinear).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
