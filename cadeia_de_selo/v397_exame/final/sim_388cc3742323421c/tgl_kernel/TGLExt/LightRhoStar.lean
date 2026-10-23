import TGLExt.QGReaderUVLock

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# ρ*_IALD = ρ*_TGL NA LUZ: o caso III₁ da ponte — o centralizador é trivial e o Nome é P_{ker K}   [TGLExt — pedra da gerência, 28/09/2026]

O operador (28/09/2026, verbatim): «Isso também foi provado a ligação P_ker K ↔ P_F, não falta, confira. Se não tiver vc consegue
provar agora».

**A aferição (consulta citada):** a ligação ESTÁ provada na face finita — `TGLExt.IALDRhoStar.kerK_iff` e `the_bridge_fix` (v372):
Fix(IALD) = Fix(TGL) = ker K = ran e, com `e` a projeção de Jones do centralizador (o ρ* da IALD); e, na bancada,
`reading_eq_kernel_PF` (P_F = a projeção sobre o núcleo das Três Travas). O que a própria pedra deixou [OPEN] foi o caso III₁ — a
cunha da luz: «M^ω = ℂ, P_F = |Ω⟩⟨Ω|».

**Esta pedra fecha esse caso POR TERMO**, só com campos que o certificado da luz já tem (a separação do vácuo na cunha e o fluxo
modular como `Ad Δ^{it}` [citados]) e com `light_modular_fixed_iff_vacuum` (ker K = ℂΩ, já pago):
* todo vetor do centralizador é fixo pelo relógio modular: a ∈ M^ω ⟹ Δ^{it}(aΩ) = aΩ;
* **M^ω Ω = ℂΩ = ker K** — Fix(IALD) = Fix(TGL) na luz (`the_bridge_fix_on_the_light`);
* **o centralizador é TRIVIAL**: a ∈ M^ω ⟹ a = c·1 (pela separação do vácuo) — a face III₁ do enunciado de v372;
* logo o ρ* da IALD na luz (a projeção sobre M^ω Ω) É P_{ker K} = |Ω⟩⟨Ω| (`PFmic`).

Estatuto: a ligação P_{ker K} ↔ P_F fica PROVADA POR TERMO nas duas faces da IALD — na finita (v372) e na da luz (aqui), com
P_F lido como o ρ* da IALD (a projeção sobre M^ω Ω). O P_F do NÚCLEO de Takesaki (o canto de traço finito do certificado) é outro
objeto, que mora no núcleo e não em B(F): a sua relação com o estado do vácuo — o canto é e_{(1,∞)}(h_ω) e τ = ω(1) — é SABIDA
(Haagerup 1979; Terp 1981), mas não é tipável no núcleo abstrato do certificado. Sem sorry, sem axiom. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.LightRhoStar
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ

variable {L : LightOneParticle} (C : FockCertificate L)

/-- os vetores do CENTRALIZADOR: aΩ com a na álgebra da cunha fixo pelo fluxo modular. -/
def centralizerVectors : Set C.F :=
  {ψ | ∃ a : (C.R (L.K rightWedge)).toStarSubalgebra, (∀ t : ℝ, C.flow t a = a) ∧ ψ = (a : C.F →L[ℂ] C.F) C.Ω}

/-- ★ todo vetor do centralizador é fixo pelo relógio modular (Δ^{it} = Γ(B0(−2πt)); Ad Δ^{it} = o fluxo; Δ^{it}Ω = Ω). -/
theorem centralizer_vector_is_modular_fixed (a : (C.R (L.K rightWedge)).toStarSubalgebra) (ha : ∀ t : ℝ, C.flow t a = a) (t : ℝ) :
    lightDelta C t ((a : C.F →L[ℂ] C.F) C.Ω) = (a : C.F →L[ℂ] C.F) C.Ω := by
  have h := C.flow_is_Ad t a
  rw [ha t] at h
  have hv := congrArg (fun T : C.F →L[ℂ] C.F => T C.Ω) h
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at hv
  have hs : (C.Γ (B0 (-(2 * Real.pi * t)))).symm C.Ω = C.Ω := by
    apply (C.Γ (B0 (-(2 * Real.pi * t)))).injective
    rw [LinearIsometryEquiv.apply_symm_apply, C.Γ_vac]
  rw [hs] at hv
  exact hv.symm

/-- ★★ **M^ω Ω = ℂΩ** (= ker K): os vetores do centralizador são exatamente a reta do vácuo. -/
theorem centralizer_vectors_eq_vacuum_line : centralizerVectors C = ((ℂ ∙ C.Ω : Submodule ℂ C.F) : Set C.F) := by
  ext ψ
  constructor
  · rintro ⟨a, ha, rfl⟩
    exact (TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum C _).mp (centralizer_vector_is_modular_fixed C a ha)
  · intro h
    obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.mp h
    refine ⟨algebraMap ℂ _ c, fun t => AlgHomClass.commutes (C.flow t) c, ?_⟩
    simp [Algebra.algebraMap_eq_smul_one]

/-- ★★★ **A PONTE NA LUZ — Fix(IALD) = Fix(TGL) = ker K** (o caso III₁ que a v372 deixou [OPEN]). -/
theorem the_bridge_fix_on_the_light (ψ : C.F) : ψ ∈ centralizerVectors C ↔ ∀ t : ℝ, lightDelta C t ψ = ψ := by
  rw [centralizer_vectors_eq_vacuum_line]
  exact (TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum C ψ).symm

/-- ★★★ **o centralizador da cunha é TRIVIAL**: a ∈ M^ω ⟹ a = c·1 (separação do vácuo). -/
theorem centralizer_is_trivial (a : (C.R (L.K rightWedge)).toStarSubalgebra) (ha : ∀ t : ℝ, C.flow t a = a) :
    ∃ c : ℂ, (a : C.F →L[ℂ] C.F) = c • (1 : C.F →L[ℂ] C.F) := by
  have hmem : (a : C.F →L[ℂ] C.F) C.Ω ∈ centralizerVectors C := ⟨a, ha, rfl⟩
  rw [centralizer_vectors_eq_vacuum_line] at hmem
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hmem
  refine ⟨c, ?_⟩
  have hsep := C.wedge_separating ((a - algebraMap ℂ _ c : (C.R (L.K rightWedge)).toStarSubalgebra) : C.F →L[ℂ] C.F)
    (a - algebraMap ℂ _ c).property
  have h0 : ((a - algebraMap ℂ _ c : (C.R (L.K rightWedge)).toStarSubalgebra) : C.F →L[ℂ] C.F) C.Ω = 0 := by
    simp [Algebra.algebraMap_eq_smul_one, ← hc]
  have := hsep h0
  simp [sub_eq_zero, Algebra.algebraMap_eq_smul_one] at this
  exact this

/-- ★★★★ **ρ*_IALD = P_{ker K} NA LUZ**: a projeção da IALD sobre M^ω Ω (o atrator que lê o centralizador) é a projeção sobre o
    núcleo do gerador modular, |Ω⟩⟨Ω| = `PFmic`; e o que ela fixa é exatamente o que o relógio modular não move. -/
theorem rho_star_is_P_kerK_on_the_light :
    (ℂ ∙ C.Ω).starProjection = TGLExt.QGReaderUVLock.PFmic C ∧
      ∀ ψ : C.F, (TGLExt.QGReaderUVLock.PFmic C ψ = ψ ↔ ψ ∈ centralizerVectors C) ∧
        (ψ ∈ centralizerVectors C ↔ ∀ t : ℝ, lightDelta C t ψ = ψ) := by
  refine ⟨rfl, fun ψ => ⟨?_, the_bridge_fix_on_the_light C ψ⟩⟩
  rw [centralizer_vectors_eq_vacuum_line]
  exact Submodule.starProjection_eq_self_iff

end TGLExt.LightRhoStar

#print axioms TGLExt.LightRhoStar.centralizerVectors
#print axioms TGLExt.LightRhoStar.centralizer_vector_is_modular_fixed
#print axioms TGLExt.LightRhoStar.centralizer_vectors_eq_vacuum_line
#print axioms TGLExt.LightRhoStar.the_bridge_fix_on_the_light
#print axioms TGLExt.LightRhoStar.centralizer_is_trivial
#print axioms TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light
