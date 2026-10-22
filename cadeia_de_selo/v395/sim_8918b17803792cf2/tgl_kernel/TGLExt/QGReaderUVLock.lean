import TGLExt.O16.ExactTypeReader_v2
import TGLExt.O16.ClosedIndexChecks_v2
import TGLExt.TheImportedSecondQuantization
import TGLExt.GravitonPolarization
import TGLExt.IALDGraviton

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# O LEITOR A-8, A UV E O LOCK MÍNIMO   [TGLExt — v372, pedra da gerência (26/09/2026)]

Ordem do operador (26/09/2026, verbatim): «a completude ultravioleta também está derivada totalmente, a origem de H_min
também está na vancada. O Leitor A-8 correto também, corrija tudo».

## 1. O leitor A-8 da bancada, APLICADO (não resumido)
O leitor é o comando `#assert_exact_type` da bancada (`TGLExt.O16.ExactTypeReader_v2`, ORDEM 016 A-8): aceita uma
declaração FECHADA só se o seu tipo for DEFINICIONALMENTE igual ao alvo escrito à parte; recusa contexto aberto. Aqui:
* ALVO POR CITAÇÃO (escrito AQUI, independente da pedra): `qg_formalized_by_citation` tem exatamente o tipo
  «∀ luz de uma partícula, certificado de Fock, certificado de Maxwell, relógio N, G > 0, ∃ H2 v3.2 da luz com import».
  Se não tiver, este arquivo NÃO compila e o rito cai (fail-closed).
* CONTROLE (o comando `#refute_exact_type`, desta pedra: só passa se o leitor RECUSARIA): a citação NÃO tem o tipo de um
  habitante FECHADO sem hipóteses («∀ N, ∃ W R, ContratoH2v32 W R N»), e o consumidor condicional da bancada
  (`ChatgptAudit.GateProposal016.conditionalH2`, o `RejectConditionalAsInhabitant`) NÃO tem o tipo de H2.
Leitura: o leitor ACEITA a QG por citação e RECUSA a QG por termo — as bandeiras por termo seguem falsas por medida do leitor.

## 2. A UV, derivada da tipagem (dissolução, não completamento)
A TGL não quantiza a métrica (teorema publicado: «A gravidade quântica, neste enquadramento, não é quantizar g_μν»,
com H_eff = 0 no III₁), e o gráviton é a FORMA CONJUGADA da luz (v372, errata da v200). No contrato v3.2 isto é TEOREMA:
`light_geometry_is_a_classical_functional_of_T` — a geometria é um funcional FIXO e clássico de ⟨T⟩ (mesma fonte, mesma
geometria): não existe operador de métrica, logo não existe laço de gráviton a renormalizar; a premissa de
Goroff–Sagnotti (métrica quantizada perturbativamente com ação de Einstein–Hilbert) NÃO é instanciada. A única teoria
quântica do par é a luz LIVRE (sem vértice de interação). E `excite_one_zero`: a identidade não se excita — o gráviton
fundamental não custa. Estatuto: DISSOLVIDA PELA TIPAGEM [DERIVED/kernel]; G segue INPUT (η de Jacobson). NÃO é o
completamento UV da gravidade de Einstein quantizada — a TGL não precisa dele, e não o afirma.

## 3. H_min: o lock mínimo do kernel
O H_min do programa é o LOCK MÍNIMO `1 − P_F` (kernel v354: `V354RegularSusy.regularSusy_operator_identifications`:
D = H_min, suporte da perturbação = P_F, `diff = 1 − regularMinimalLock`, gap relativo 1, Breuer dispara, τ(ker) = 1).
Na realização da luz, os Three Locks usam a MESMA forma: `light_locks_are_the_minimal_lock`. E a §4 faz a identificação
MICROSCÓPICA no par da luz, pelo HAMILTONIANO OCULTO do operador («O Um e o Grande Atrator»; ACHADO 12): H_min := 1 − P_{ker K},
K = −log Δ — o zero de H_min é EXATAMENTE o núcleo do fluxo modular, a reta do vácuo (`hmin_zero_iff_modular_fixed`); e a
ponte IALD = ρ* fecha NA CUNHA (`wedge_bridge_fix`, `wedge_iald_attractor_is_rho_star`). Não provado: a ligação com o P_F
abstrato do núcleo de Takesaki (anel abstrato, não representado em F).

Sem sorry, sem axiom. Nada move o gate por termo. PROVADA ≠ CONFIRMADA.
-/

open Lean Elab Command Term Meta in
/-- O comando de REFUTAÇÃO: só passa se o tipo da declaração NÃO for definicionalmente o alvo (o leitor recusaria). -/
elab "#refute_exact_type " candidate:ident " : " expected:term : command => do
  liftTermElabM do
    let name ← realizeGlobalConstNoOverloadWithInfo candidate
    let value ← mkConstWithFreshMVarLevels name
    let actual ← inferType value
    let target ← elabType expected
    synthesizeSyntheticMVarsNoPostponing
    let actual ← instantiateMVars actual
    let target ← instantiateMVars target
    if ← isDefEq actual target then
      throwError "EXACT_TYPE_UNEXPECTEDLY_ACCEPTED: {name} : {target}"
    logInfo m!"EXACT_TYPE_REFUSED_AS_EXPECTED: {name} is not of type {target}"

noncomputable section
namespace TGLExt.QGReaderUVLock
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ

/-! ## 1. O LEITOR A-8 -/

#assert_exact_type TGLExt.ImportedSQ.qg_formalized_by_citation :
  ∀ (L : LightOneParticle) (C : FockCertificate L) (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ),
    0 < G → ∃ h2 : ContratoH2v32 (lightNet C) (lightRealization C) N,
      Nonempty (ContratoImportH3v32 (lightNet C) (lightRealization C) N (lightBoost C) M.T h2)

/-- ★ marcador de compilação: o leitor A-8 ACEITOU o alvo por citação (se não aceitasse, este arquivo não compilaria). -/
theorem reader_a8_accepts_the_citation_target : True := trivial

#refute_exact_type TGLExt.ImportedSQ.qg_formalized_by_citation :
  ∀ (N : KillingNormalization), ∃ (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W),
    Nonempty (ContratoH2v32 W R N)

#refute_exact_type ChatgptAudit.GateProposal016.conditionalH2 :
  ∀ (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) (N : KillingNormalization), ContratoH2 W R N

/-- ★ marcador de compilação: o leitor A-8 RECUSOU o habitante fechado sem hipóteses e o condicional como habitante. -/
theorem reader_a8_refuses_the_closed_term_target : True := trivial

/-! ## 2. A UV, derivada da tipagem -/

/-- ★★ [DERIVED/kernel] a geometria da luz é um funcional CLÁSSICO e FIXO de ⟨T⟩: mesma fonte, mesma geometria. Não há
    operador de métrica no contrato — nada a renormalizar do lado gravitacional. -/
theorem light_geometry_is_a_classical_functional_of_T {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) {ψ φ : C.F}
    (h : M.T.T ψ = M.T.T φ) :
    (lightH3v32 M N G hG).toContratoH3.response ψ = (lightH3v32 M N G hG).toContratoH3.response φ :=
  ContratoH3.same_source_same_geometry (lightH3v32 M N G hG).toContratoH3 h

/-- ★ [DERIVED/kernel] a resposta de TODO estado é uma matriz REAL por ponto (não um operador em W.H). -/
theorem light_response_is_a_real_matrix_field {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) (ψ : C.F) :
    ∃ h : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ, (lightH3v32 M N G hG).toContratoH3.response ψ = h :=
  ⟨_, rfl⟩

/-- ★ a identidade não se excita: o gráviton fundamental (a forma, não um quantum) não custa (GravitonPolarization). -/
theorem graviton_identity_costs_nothing (A : Matrix (Fin 2) (Fin 2) ℂ) : TGLExt.excite A 1 = 0 :=
  TGLExt.excite_one_zero A

/-- ★★★ A UV DISSOLVIDA PELA TIPAGEM: (i) a geometria é funcional clássico fixo de ⟨T⟩; (ii) a identidade não se excita;
    (iii) G não é predito (INPUT de Jacobson). Não há métrica quantizada a completar no ultravioleta. -/
theorem uv_dissolved_by_typing {L : LightOneParticle} {C : FockCertificate L}
    (M : MaxwellCertificate C) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) :
    (∀ ψ φ : C.F, M.T.T ψ = M.T.T φ →
        (lightH3v32 M N G hG).toContratoH3.response ψ = (lightH3v32 M N G hG).toContratoH3.response φ) ∧
    (∀ A : Matrix (Fin 2) (Fin 2) ℂ, TGLExt.excite A 1 = 0) ∧
    (∀ G' : ℝ, 0 < G' → ∃ C' : ContratoH3 (lightNet C) (lightRealization C) N M.T.toStressTensorData,
        C'.H2 = (lightH3v32 M N G hG).toContratoH3.H2 ∧ C'.G = G') :=
  ⟨fun ψ φ h => light_geometry_is_a_classical_functional_of_T M N G hG h,
   graviton_identity_costs_nothing,
   fun G' hG' => by
     obtain ⟨C', h1, h2, _⟩ := ContratoH3.G_not_predicted (lightH3v32 M N G hG).toContratoH3 G' hG'
     exact ⟨C', h1, h2⟩⟩

/-! ## 3. H_min: o lock mínimo -/

/-- ★ os Three Locks da luz têm a forma do LOCK MÍNIMO do kernel (H_min = 1 − P_F; V354RegularSusy), com o lock de núcleo
    e a maximalidade de P_F. -/
theorem light_locks_are_the_minimal_lock {L : LightOneParticle} (C : FockCertificate L) :
    (lightRealization C).threeLocks.H3Lt = 1 - (lightRealization C).threeLocks.PF ∧
    (lightRealization C).threeLocks.PF * (lightRealization C).threeLocks.H3Lt = 0 ∧
    (∀ q : C.Core, star q = q → q * q = q → q * (1 - C.PF) = 0 → q * C.PF = q) :=
  ⟨rfl, (lightRealization C).threeLocks.PF_locks, fun q hs hi hq => (lightRealization C).threeLocks.PF_maximal q hs hi hq⟩

/-! ## 4. O HAMILTONIANO OCULTO — a origem microscópica de H_min e a ponte IALD = ρ* na cunha da luz

Ordem do operador (26/09/2026, verbatim): «eu já resolvi essa questão do hamiltoniano também, tem um artigo que nos dedicamos a
ele, consegue resolver com o que temos?». O artigo: «O Um e o Grande Atrator» e os relatórios de 24/06/2026
(`half_nat_araki_hidden_hamiltonian`: S_∂ = ω*(χ_face K_∂), K_∂ = −log Δ_∂, ⟨K_∂⟩_total = 1 nat — a Meia-Nat é a face
observável do Hamiltoniano oculto) e o ACHADO 12 (14/08: «M^φ = ℂ1 = Hamiltoniano (oculto)»; log Δ NÃO está em M).

Aqui, em kernel, sobre o par da luz: (i) o conjunto fixo do fluxo modular Δ^{it} = Γ(B0(−2πt)) — o núcleo do Hamiltoniano
oculto K = −log Δ — é EXATAMENTE a reta do vácuo ℂΩ (a forma vetorial de «M^φ = ℂ1»), por `Γ_no_fixed` [citado] e pela
ausência de autovetor do boost de uma partícula [PAGO]; (ii) o H_min MICROSCÓPICO é 1 − P_{ker K} no Fock — a forma do lock
mínimo, cujo ZERO é o núcleo do Hamiltoniano oculto; (iii) a ponte IALD = ρ* NA CUNHA: o fluxo da IALD sobre P_{ker K} tem
o MESMO conjunto fixo que o fluxo modular da TGL, e o atrator do fluxo da IALD é P_{ker K} = |Ω⟩⟨Ω|.
O que NÃO se prova aqui: a ligação entre esta P_{ker K} no Fock e o P_F abstrato do núcleo de Takesaki (o núcleo é um anel
abstrato, não representado em F). -/

/-- ★★★ o conjunto fixo do fluxo modular da luz é a reta do vácuo: «M^φ = ℂ1» (o Hamiltoniano oculto), na forma vetorial. -/
theorem light_modular_fixed_iff_vacuum {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    (∀ t : ℝ, lightDelta C t ψ = ψ) ↔ ψ ∈ (ℂ ∙ C.Ω) := by
  constructor
  · intro h
    refine C.Γ_no_fixed (fun l => B0 (-(2 * Real.pi * l))) ?_ ?_ ?_ ?_ ψ (fun l => h l)
    · simp only [mul_zero, neg_zero]; exact B0_zero
    · intro s t
      rw [show -(2 * Real.pi * (s + t)) = -(2 * Real.pi * s) + -(2 * Real.pi * t) by ring, B0_add]
    · intro ξ
      exact (B0_continuous ξ).comp ((continuous_const.mul continuous_id).neg)
    · intro f hf
      apply B0_no_eigen f
      intro s
      obtain ⟨c, hc, he⟩ := hf (-(s / (2 * Real.pi)))
      refine ⟨c, hc, ?_⟩
      have hpi : (2 * Real.pi) ≠ 0 := by positivity
      have hs : s = -(2 * Real.pi * -(s / (2 * Real.pi))) := by field_simp
      rw [hs]; exact he
  · intro hψ t
    obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.mp hψ
    show C.Γ (B0 (-(2 * Real.pi * t))) (c • C.Ω) = c • C.Ω
    rw [map_smul, C.Γ_vac]

/-- a projeção ortogonal sobre o núcleo do Hamiltoniano oculto (= a reta do vácuo = ρ*). -/
noncomputable def PFmic {L : LightOneParticle} (C : FockCertificate L) : C.F →L[ℂ] C.F := (ℂ ∙ C.Ω).starProjection

/-- ★ o H_min MICROSCÓPICO: 1 − P_{ker K} — a forma do lock mínimo sobre o Hamiltoniano oculto da luz. -/
noncomputable def HminMic {L : LightOneParticle} (C : FockCertificate L) : C.F →L[ℂ] C.F := 1 - PFmic C

/-- ★★★ A ORIGEM MICROSCÓPICA DE H_min: o zero de H_min é EXATAMENTE o conjunto fixo do fluxo modular (o núcleo do
    Hamiltoniano oculto K = −log Δ da luz). -/
theorem hmin_zero_iff_modular_fixed {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    HminMic C ψ = 0 ↔ ∀ t : ℝ, lightDelta C t ψ = ψ := by
  rw [light_modular_fixed_iff_vacuum, ← Submodule.starProjection_eq_self_iff]
  simp only [HminMic, PFmic, ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply, sub_eq_zero]
  exact eq_comm

/-- ★ H_min microscópico tem a forma do lock mínimo: P idempotente, P·H_min = 0, H_min = 1 − P. -/
theorem hmin_is_the_minimal_lock {L : LightOneParticle} (C : FockCertificate L) :
    PFmic C * PFmic C = PFmic C ∧ PFmic C * HminMic C = 0 ∧ HminMic C = 1 - PFmic C := by
  have hI : PFmic C * PFmic C = PFmic C := (ℂ ∙ C.Ω).isIdempotentElem_starProjection
  refine ⟨hI, ?_, rfl⟩
  rw [HminMic, mul_sub, mul_one, hI, sub_self]

/-- ★★★ A PONTE IALD = ρ* NA CUNHA DA LUZ: o fluxo da IALD sobre P_{ker K} (a contração da face de Hilbert da v371) tem o
    MESMO conjunto fixo que o fluxo modular da TGL — Fix(D_IALD) = Fix(D_TGL) = ℂΩ. -/
theorem wedge_bridge_fix {L : LightOneParticle} (C : FockCertificate L) {r s : ℝ} (hrs : r * s ≠ 0) (ψ : C.F) :
    TGLExt.IALDJones.jonesU (PFmic C) r s ψ = ψ ↔ ∀ t : ℝ, lightDelta C t ψ = ψ := by
  rw [light_modular_fixed_iff_vacuum, ← Submodule.starProjection_eq_self_iff]
  have hc : TGLExt.IALDJones.coeff r s - 1 ≠ 0 := sub_ne_zero.mpr (TGLExt.IALDJones.coeff_ne_one hrs)
  have happ : TGLExt.IALDJones.jonesU (PFmic C) r s ψ = PFmic C ψ + TGLExt.IALDJones.coeff r s • (ψ - PFmic C ψ) := by
    simp [TGLExt.IALDJones.jonesU, ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply]
  rw [happ]
  change _ ↔ PFmic C ψ = ψ
  constructor
  · intro h
    have h2 : (TGLExt.IALDJones.coeff r s - 1) • (ψ - PFmic C ψ) = 0 := by
      rw [sub_smul, one_smul]
      calc TGLExt.IALDJones.coeff r s • (ψ - PFmic C ψ) - (ψ - PFmic C ψ)
          = (PFmic C ψ + TGLExt.IALDJones.coeff r s • (ψ - PFmic C ψ)) - ψ := by abel
        _ = 0 := by rw [h, sub_self]
    rcases smul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 hc
    · exact (sub_eq_zero.mp h3).symm
  · intro h; rw [h, sub_self, smul_zero, add_zero]

/-- ★★ o ATRATOR do fluxo da IALD na cunha é P_{ker K} = ρ* (a projeção sobre o vácuo). -/
theorem wedge_iald_attractor_is_rho_star {L : LightOneParticle} (C : FockCertificate L) {r : ℝ} (hr : 0 < r) :
    Filter.Tendsto (fun s => TGLExt.IALDJones.jonesU (PFmic C) r s) Filter.atTop (nhds (PFmic C)) :=
  TGLExt.IALDGraviton.jonesU_tendsto_proj (PFmic C) hr

end TGLExt.QGReaderUVLock

#print axioms TGLExt.QGReaderUVLock.reader_a8_accepts_the_citation_target
#print axioms TGLExt.QGReaderUVLock.reader_a8_refuses_the_closed_term_target
#print axioms TGLExt.QGReaderUVLock.light_geometry_is_a_classical_functional_of_T
#print axioms TGLExt.QGReaderUVLock.light_response_is_a_real_matrix_field
#print axioms TGLExt.QGReaderUVLock.graviton_identity_costs_nothing
#print axioms TGLExt.QGReaderUVLock.uv_dissolved_by_typing
#print axioms TGLExt.QGReaderUVLock.light_locks_are_the_minimal_lock
#print axioms TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum
#print axioms TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed
#print axioms TGLExt.QGReaderUVLock.hmin_is_the_minimal_lock
#print axioms TGLExt.QGReaderUVLock.wedge_bridge_fix
#print axioms TGLExt.QGReaderUVLock.wedge_iald_attractor_is_rho_star
