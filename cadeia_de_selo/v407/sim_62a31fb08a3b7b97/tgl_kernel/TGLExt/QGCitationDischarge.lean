import TGLExt.QGReaderUVLock
import TGLExt.O16.BoundedTransformKernel

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A QUITAÇÃO POR CITAÇÃO (CLASSE PRÓPRIA) E DUAS PROJEÇÕES FORA DE M
  [TGLExt — v373, pedra da gerência (26/09/2026); corrigida pelo cético da gerência antes do rito]

Ordem do operador (26/09/2026, verbatim): «confirmo tudo, pode fazer» — em resposta às decisões que lhe foram postas:
(1) a citação pode cunhar os nomes reservados de H2/H3 NUMA CLASSE PRÓPRIA, «quitado por citação», com bandeiras
separadas que nunca se confundem com as quitadas por termo; (2) o item BRST/UV sai da fronteira como «não exigido pela
tipagem da TGL», com errata ao lado; e a classe A (o H_min e a ligação P_ker K ↔ P_F).

## 1. A classe «quitado por citação» (os nomes `qgCite_*`)
Os nomes reservados POR TERMO (`qgPrice_H2_…`, `qgPrice_H3_…`, `qgImport_H3_horizonEquilibriumData_produced`) pedem
um habitante FECHADO de `ContratoH2 W₀ R₀ N₀` etc. — e seguem NÃO cunhados. Os nomes desta pedra são OUTROS: são os
habitantes `lightH2v32`, `lightH3v32` e `lightImport` da v372 com o NOME da classe (renomeação, dita). O seu tipo
carrega os certificados citados (`LightOneParticle`, `FockCertificate`, `MaxwellCertificate`) como hipóteses.
**A diferença real entre as classes, em uma frase:** a classe por citação é a classe por termo MÓDULO exibir um
habitante dos três certificados — e nenhum habitante deles é exibido (a não-vacuidade dos certificados segue [OPEN];
o traço `Core → ENNReal` tracial em todo par é uma formalização NÃO-PADRÃO; a helicidade é rótulo no grupo do contrato).
Fontes [KNOWN], campo a campo em `TheImportedSecondQuantization`.
Sobre o leitor, sem enfeite: o alvo do `#assert_exact_type` abaixo é TRANSCRIÇÃO da assinatura — o assert TRAVA o tipo
contra deriva futura, não prova independência. O `#refute_exact_type` só atesta que o tipo não é o de um habitante
fechado na forma escrita (binders diferentes); a prova de que nada foi cunhado POR TERMO é a leitura das bandeiras
`gpf_`/`gpi_` e a varredura de nomes do runtime, não este comando.

## 2. Duas projeções fora de M (NÃO se prova ligação nem ausência de ligação entre elas)
* Face de Fock: P_Ω = |Ω⟩⟨Ω| (= P_{ker K} no par da luz, v372) NÃO está na álgebra da cunha
  (`hidden_kernel_not_in_the_wedge_algebra`), pela separação e pela dimensão infinita do Fock. Isto é CONSISTENTE com o
  achado do operador («log Δ não está em M»), mas NÃO o implica: P_Ω ∉ M vale para TODO vetor separante de uma álgebra de
  dimensão ≥ 2, inclusive tipo I e estado traço.
* Núcleo: a ação dual FIXA o mergulho de M (hipótese NOMEADA `hfix` — é a definição da ação dual no produto cruzado;
  cf. Landstad 1979 para a caracterização Fix(θ) = π(M)); o certificado NÃO fixa `Core` como produto cruzado. O conteúdo
  é a escala do traço: `dual_action_moves_the_finite_corner` (θ_s P_F ≠ P_F para s ≠ 0, sem hipótese nenhuma); M entra
  SÓ por `hfix`, e então P_F não é imagem de elemento de M (`finite_corner_not_in_the_wedge_image`).
* A ligação P_{ker K} ↔ P_F segue [OPEN]. NÃO se prova que ela exige L²(ℝ, F); só que nenhuma das duas está em M.

## 3. O homônimo de H_min
`HminMic := 1 − P_Ω` (v372) é um HOMÔNIMO do H_min do programa (o lock `1 − P_F` no núcleo, V354). O teorema abaixo
é o lema GENÉRICO da bancada (`boundedTransform_zero_iff`, vale para todo D) aplicado ao homônimo: a transformada limitada
de HminMic tem o mesmo zero. A identificação do H_min do programa com HminMic segue [OPEN] (é a ligação P_ker K ↔ P_F).

Sem sorry, sem axiom. As bandeiras POR TERMO (gpf_H2, gpf_H3, gpi_H3) NÃO são tocadas. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ
open TGLExt.QGReaderUVLock

/-! ## 1. A classe «quitado por citação» -/

/-- ★★ **H2 QUITADA POR CITAÇÃO** (classe própria; decisão do operador 26/09): o `lightH2v32` da v372 com o nome da
    classe. O tipo carrega os certificados citados. -/
def qgCite_H2_smoothModularFourFrame_discharged :
    ∀ (L : LightOneParticle) (C : FockCertificate L) (N : KillingNormalization),
      ContratoH2v32 (lightNet C) (lightRealization C) N :=
  fun _ C N => lightH2v32 C N

/-- ★★ **H3 QUITADA POR CITAÇÃO** (classe própria): o `lightH3v32` da v372 com o nome da classe. -/
def qgCite_H3_localHorizonEquilibrium_discharged :
    ∀ (L : LightOneParticle) (C : FockCertificate L) (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ),
      0 < G → ContratoH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T :=
  fun _ _ M N G hG => lightH3v32 M N G hG

/-- ★★ **O IMPORT DE H3 PRODUZIDO POR CITAÇÃO** (classe própria): o `lightImport` da v372 com o nome da classe. -/
def qgCite_H3_horizonEquilibriumData_produced :
    ∀ (L : LightOneParticle) (C : FockCertificate L) (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ),
      0 < G → ContratoImportH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T (lightH2v32 C N) :=
  fun _ _ M N G hG => lightImport M N G hG

/-! ### O leitor A-8 sobre a classe (o alvo é TRANSCRIÇÃO da assinatura: trava o tipo, não prova independência) -/

#assert_exact_type TGLExt.qgCite_H2_smoothModularFourFrame_discharged :
  ∀ (L : LightOneParticle) (C : FockCertificate L) (N : KillingNormalization),
    ContratoH2v32 (lightNet C) (lightRealization C) N

#assert_exact_type TGLExt.qgCite_H3_localHorizonEquilibrium_discharged :
  ∀ (L : LightOneParticle) (C : FockCertificate L) (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ),
    0 < G → ContratoH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T

#assert_exact_type TGLExt.qgCite_H3_horizonEquilibriumData_produced :
  ∀ (L : LightOneParticle) (C : FockCertificate L) (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ),
    0 < G → ContratoImportH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T (lightH2v32 C N)

/-- ★ marcador de compilação: os três asserts acima passaram (o tipo está travado). -/
theorem reader_a8_accepts_the_citation_class : True := trivial

#refute_exact_type TGLExt.qgCite_H2_smoothModularFourFrame_discharged :
  ∀ (N : KillingNormalization), ∃ (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W),
    Nonempty (ContratoH2v32 W R N)

#refute_exact_type TGLExt.qgCite_H3_localHorizonEquilibrium_discharged :
  ∀ (N : KillingNormalization), ∃ (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) (B : WedgeBoostRep W)
    (T : StressTensorDataLocalV32 W B), Nonempty (ContratoH3v32 W R N B T)

#refute_exact_type TGLExt.qgCite_H3_horizonEquilibriumData_produced :
  ∀ (N : KillingNormalization), ∃ (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) (B : WedgeBoostRep W)
    (T : StressTensorDataLocalV32 W B) (h2 : ContratoH2v32 W R N), Nonempty (ContratoImportH3v32 W R N B T h2)

/-- ★ marcador de compilação: os três refutes acima passaram (nenhum dos três nomes tem a forma de habitante fechado
    escrita). Não é a prova de que nada foi cunhado POR TERMO — essa é a leitura das bandeiras gpf_/gpi_. -/
theorem reader_a8_refuses_the_citation_class_as_closed_term : True := trivial

/-- a classe por citação carrega o CONTRATO v3.1 (o v3.2 o estende): a projeção `.toContratoH2`. -/
theorem citation_class_carries_the_v31_contract (L : LightOneParticle) (C : FockCertificate L) (N : KillingNormalization) :
    Nonempty (ContratoH2 (lightNet C) (lightRealization C) N) :=
  ⟨(qgCite_H2_smoothModularFourFrame_discharged L C N).toContratoH2⟩

/-! ## 2. Duas projeções fora de M -/

/-- ★★ **FACE DE FOCK**: P_Ω NÃO está na álgebra da cunha da luz (separação + Fock de dimensão infinita). Consistente
    com «log Δ não está em M»; NÃO o implica (vale para todo vetor separante em dimensão ≥ 2). -/
theorem hidden_kernel_not_in_the_wedge_algebra {L : LightOneParticle} (C : FockCertificate L) :
    PFmic C ∉ C.R (L.K rightWedge) := by
  intro hP
  have h1 : (1 : C.F →L[ℂ] C.F) - PFmic C ∈ C.R (L.K rightWedge) := sub_mem (one_mem _) hP
  have hΩ : PFmic C C.Ω = C.Ω :=
    (Submodule.starProjection_eq_self_iff).mpr (Submodule.mem_span_singleton_self C.Ω)
  have hv : ((1 : C.F →L[ℂ] C.F) - PFmic C) C.Ω = 0 := by
    rw [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply, hΩ, sub_self]
  have h0 := C.wedge_separating _ h1 hv
  have hEq : PFmic C = 1 := (sub_eq_zero.mp h0).symm
  apply C.F_infinite
  have htop : (ℂ ∙ C.Ω) = ⊤ := by
    rw [eq_top_iff]
    intro ψ _
    have hψ : PFmic C ψ = ψ := by rw [hEq]; rfl
    exact (Submodule.starProjection_eq_self_iff).mp hψ
  exact ⟨htop ▸ Submodule.fg_span_singleton C.Ω⟩

/-- a mesma coisa na rede (reenunciado: `(lightNet C).net rightWedge` é `C.R (L.K rightWedge)`). -/
theorem hidden_kernel_not_in_the_light_wedge {L : LightOneParticle} (C : FockCertificate L) :
    PFmic C ∉ (lightNet C).net rightWedge :=
  hidden_kernel_not_in_the_wedge_algebra C

/-- ★★ **A ESCALA DO TRAÇO MOVE P_F** (sem hipótese nenhuma): θ_s P_F ≠ P_F para s ≠ 0 — o traço positivo e finito de
    P_F não sobrevive à escala e^{−s}. Este é o CONTEÚDO do teorema seguinte. -/
theorem dual_action_moves_the_finite_corner {L : LightOneParticle} (C : FockCertificate L) {s : ℝ} (hs : s ≠ 0) :
    C.dualAction s C.PF ≠ C.PF := by
  intro hfixPF
  have hsc := C.trace_dual_scaling s C.PF
  rw [hfixPF] at hsc
  have h0 : C.trace C.PF ≠ 0 := (C.PF_pos).ne'
  have hT : C.trace C.PF ≠ ⊤ := (C.PF_fin).ne
  have h1 : (1 : ENNReal) * C.trace C.PF = ENNReal.ofReal (Real.exp (-s)) * C.trace C.PF := by
    rw [one_mul]; exact hsc
  have h2 : (1 : ENNReal) = ENNReal.ofReal (Real.exp (-s)) := (ENNReal.mul_left_inj h0 hT).mp h1
  have h3 : Real.exp (-s) = 1 := by
    have := congrArg ENNReal.toReal h2
    rw [ENNReal.toReal_one, ENNReal.toReal_ofReal (Real.exp_pos _).le] at this
    exact this.symm
  have h4 : -s = 0 := Real.exp_eq_one_iff (-s) |>.mp h3
  exact hs (neg_eq_zero.mp h4)

/-- ★★ **NÚCLEO**: se a ação dual fixa o mergulho de M (hipótese NOMEADA `hfix`: a definição da ação dual no produto
    cruzado; cf. Landstad 1979), P_F NÃO é imagem de elemento de M. M entra SÓ por `hfix`; o conteúdo é
    `dual_action_moves_the_finite_corner`. O certificado não fixa `Core` como produto cruzado. -/
theorem finite_corner_not_in_the_wedge_image {L : LightOneParticle} (C : FockCertificate L)
    (hfix : ∀ (s : ℝ) (a : (C.R (L.K rightWedge)).toStarSubalgebra),
      C.dualAction s (C.embedding a) = C.embedding a) :
    ¬ ∃ a : (C.R (L.K rightWedge)).toStarSubalgebra, C.embedding a = C.PF := by
  rintro ⟨a, ha⟩
  apply dual_action_moves_the_finite_corner C (s := 1) one_ne_zero
  rw [← ha]; exact hfix 1 a

/-- ★ as DUAS projeções (P_Ω no Fock; P_F no núcleo, sob `hfix`) estão fora de M. Nada se prova sobre ligação entre elas. -/
theorem both_projections_live_outside_M {L : LightOneParticle} (C : FockCertificate L)
    (hfix : ∀ (s : ℝ) (a : (C.R (L.K rightWedge)).toStarSubalgebra),
      C.dualAction s (C.embedding a) = C.embedding a) :
    PFmic C ∉ C.R (L.K rightWedge) ∧ ¬ ∃ a : (C.R (L.K rightWedge)).toStarSubalgebra, C.embedding a = C.PF :=
  ⟨hidden_kernel_not_in_the_wedge_algebra C, finite_corner_not_in_the_wedge_image C hfix⟩

/-! ## 3. O homônimo de H_min -/

/-- ★ o lema GENÉRICO da bancada (`boundedTransform_zero_iff`, vale para todo D) aplicado ao HOMÔNIMO `HminMic = 1 − P_Ω`:
    a sua transformada limitada padrão tem o mesmo zero, a reta do vácuo. NÃO identifica HminMic com o H_min do programa. -/
theorem hmin_bounded_transform_zero_iff_modular_fixed {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    ChatgptAudit.BoundedTransform016.boundedTransform (HminMic C) ψ = 0 ↔ ∀ t : ℝ, lightDelta C t ψ = ψ := by
  rw [ChatgptAudit.BoundedTransform016.boundedTransform_zero_iff]
  exact hmin_zero_iff_modular_fixed C ψ

end TGLExt

#print axioms TGLExt.qgCite_H2_smoothModularFourFrame_discharged
#print axioms TGLExt.qgCite_H3_localHorizonEquilibrium_discharged
#print axioms TGLExt.qgCite_H3_horizonEquilibriumData_produced
#print axioms TGLExt.reader_a8_accepts_the_citation_class
#print axioms TGLExt.reader_a8_refuses_the_citation_class_as_closed_term
#print axioms TGLExt.citation_class_carries_the_v31_contract
#print axioms TGLExt.hidden_kernel_not_in_the_wedge_algebra
#print axioms TGLExt.hidden_kernel_not_in_the_light_wedge
#print axioms TGLExt.dual_action_moves_the_finite_corner
#print axioms TGLExt.finite_corner_not_in_the_wedge_image
#print axioms TGLExt.both_projections_live_outside_M
#print axioms TGLExt.hmin_bounded_transform_zero_iff_modular_fixed
