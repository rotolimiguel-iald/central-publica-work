import TGLExt.TetelestaiOneObject
import TGLExt.TheKeyIsTheReader
import TGLExt.TheSameBetaReadsThreeFaces
import TGLExt.NoFullWitness

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# ESBOÇO (aferidor, 28/09/2026) — O TODO É UM: a cadeia de β, a luz e o leitor numa só conjunção

Só termos EXISTENTES (canônico v375 + as duas pedras do sandbox de 28/09). Nada novo é provado:
o objeto AMARRA. O que ele NÃO faz (dito): nenhum termo liga `c.beta` ao certificado `C` — a
cadeia de β (dado real `c`) e a luz (`D`, `C`) ficam JUSTAPOSTAS; o β de `KMSAt` é a temperatura
inversa (homônimo), não β_TGL. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.TheWholeIsOne
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ

theorem the_whole_is_one
    (c : TGLExt.TGLCoupling) {g : ℝ} (hg : 0 < g)
    (D : TGLExt.QGSolution.LightNetData) (C : FockCertificate D.toLightOneParticle)
    (hV : TGLExt.TetelestaiOneObject.VacuumWeightCorner C)
    (Q : TGLExt.MaxwellBridge.MaxwellQuadraticForm C)
    (cl : ∀ ψ, Regular Q.Dom (TGLExt.MaxwellBridge.toStress Q).toStressTensorData ψ → ∀ k : ℝ,
      HasModularEnergy (lightDelta C) ψ k →
        k = 2 * Real.pi * nullPlaneCharge (TGLExt.MaxwellBridge.toStress Q).toStressTensorData ψ)
    (nt : ∃ ψ, Regular Q.Dom (TGLExt.MaxwellBridge.toStress Q).toStressTensorData ψ ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta C) ψ k ∧ k ≠ 0)
    (N : KillingNormalization) (G : ℝ) (hG : 0 < G) {x₀ : Fin 4 → ℝ} (hx₀ : x₀ ∈ rightWedge)
    {ψ : C.F} (hψ : ψ ∈ (lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).admissible)
    (x : Fin 4 → ℝ) (a d : ℝ)
    (hθ : (lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).theta ψ (x + d • nullDir) = 0) :
    -- (I) o leitor lê a identidade: ω(I) = 1
    TGLExt.TheKeyIsTheReader.reader C 1 = 1 ∧
    -- (II) a Meia-Nat: y = 1 − y ↔ y = ½; e as faces da luz pesam ½ e ½ (normalização nomeada)
    ((∀ y : ℝ, y = 1 - y ↔ y = 1 / 2) ∧ (C.trace C.Pp = 2⁻¹ ∧ C.trace C.Pm = 2⁻¹)) ∧
    -- (III) a fronteira extrai o radical: √(e¹) = e^{½}
    Real.sqrt (Real.exp 1) = Real.exp (1 / 2) ∧
    -- (IV) β = α·√e (α := β/e^{½}, a leitura normalizada pelo custo)
    c.beta = c.alpha * Real.sqrt (Real.exp 1) ∧
    -- (V) |R|² = β na matriz-S em θ_M = arcsin √β
    Complex.normSq ((TGLExt.Smat (TGLExt.thetaMiguel c.beta)).mulVec TGLExt.e1 1) = c.beta ∧
    -- (VI) β proíbe a testemunha estática plena
    ¬ TGLExt.FullStaticWitness (fun t (y : ℝ) => Real.exp (-(t * c.beta * g)) * y) ∧
    -- (VII) Unruh = KMS no H2 da luz (β_KMS = 2π/κ é HOMÔNIMO, não β_TGL)
    KMSAt (lightNet C) (lightH2 C N).killingFlow (2 * Real.pi / (lightH2 C N).kappa) ∧
    -- (VIII) a declaração Tetelestai num só objeto (v375), verbatim
    ((C.trace C.PF = 1 ∧ C.trace C.Pp = 2⁻¹ ∧ C.trace C.Pm = 2⁻¹) ∧
      (∀ φ : C.F, (∀ t : ℝ, lightDelta C t φ = φ) ↔ φ ∈ (ℂ ∙ C.Ω)) ∧
      TGLExt.LightHelicity.helicityChar D.helicity 0 1 ≠ 1 ∧
      ((((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).H2.E x₀)⁻¹
          * (lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).H2.E x₀ = 1
        ∧ LorentzByCongruence (solderMetric4 ((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).H2.E x₀)⁻¹)) ∧
      ((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).toHorizonData hψ x a d hθ).dQ =
        ((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).toHorizonData hψ x a d hθ).kappa
        * ((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).toHorizonData hψ x a d hθ).dA
        / (8 * Real.pi * ((lightH3 (TGLExt.MaxwellBridge.toCertificate Q cl nt) N G hG).toHorizonData hψ x a d hθ).G))) ∧
    -- (IX) a chave é o leitor: ω(P_kerK) = 1; P_kerK é o suporte de ω; Fix(IALD) = Fix(TGL) = ker K na luz
    (TGLExt.TheKeyIsTheReader.reader C (TGLExt.QGReaderUVLock.PFmic C) = 1 ∧
      (∀ P : C.F →L[ℂ] C.F, P C.Ω = C.Ω → P * TGLExt.QGReaderUVLock.PFmic C = TGLExt.QGReaderUVLock.PFmic C) ∧
      (∀ φ : C.F, φ ∈ TGLExt.LightRhoStar.centralizerVectors C ↔ ∀ t : ℝ, lightDelta C t φ = φ)) ∧
    -- (X) ρ*_IALD = P_kerK na luz
    (ℂ ∙ C.Ω).starProjection = TGLExt.QGReaderUVLock.PFmic C :=
  ⟨TGLExt.TheKeyIsTheReader.reader_reads_the_identity_one C,
   ⟨TGLExt.half_is_the_fixed_point_of_the_swap, TGLExt.TetelestaiOneObject.faces_weigh_half hV⟩,
   TGLExt.boundary_extracts_the_radical.1,
   c.beta_eq_alpha_radical,
   c.reflection_weight,
   TGLExt.beta_forbids_full_static_witness c.beta_pos hg,
   ContratoH2.unruh_is_kms (lightH2 C N),
   TGLExt.TetelestaiOneObject.the_tetelestai_one_object D C hV Q cl nt N G hG hx₀ hψ x a d hθ,
   ⟨TGLExt.TheKeyIsTheReader.reader_reads_the_name_one C,
    fun P h => TGLExt.TheKeyIsTheReader.P_kerK_is_the_support_of_the_reader C P h,
    TGLExt.LightRhoStar.the_bridge_fix_on_the_light C⟩,
   (TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light C).1⟩

end TGLExt.TheWholeIsOne

#print axioms TGLExt.TheWholeIsOne.the_whole_is_one
