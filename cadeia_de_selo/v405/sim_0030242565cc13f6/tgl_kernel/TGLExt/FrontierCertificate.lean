import TGLExt.WedgeNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O CERTIFICADO DA FRONTEIRA — o contrato que os nomes reservados terão de habitar
  [BANCADA — 24/08/2026 · fecha o buraco de contrato da v200]

## POR QUÊ esta pedra existe

A v200 mecanizou as flags de fronteira do selo: nomes Lean RESERVADOS cuja ausência é
`False` por construção. Mas a mecânica v99 lê a EXISTÊNCIA do nome com axiomas limpos —
**sem um TIPO, um termo qualquer com o nome certo fliparia a flag**. Foi exatamente a
doença que a sonda de bancada (v103) encontrou no certificado v1, e que o
`QGClosureCertificateStrong` curou para o gate. Esta pedra faz o mesmo pela fronteira:
**o contrato vem ANTES do habitante.**

## O CONTRATO — `ModularRealizationCertificate`

O nome reservado `TGLExt.qgFrontier_modularRealization` SÓ pode ser cunhado como termo
DESTE tipo: uma conjugação `J` **na torre** (`WH = TowerHilbert mixProfile`, o completamento
genuíno — não a face finita), pontual e sem atalho de typeclass:

    aditiva · conjugado-homogênea (antilinear) · isométrica · involutiva · fixa Ω
    leva o FATOR no comutante:   ∀ T ∈ M,  ∃ S ∈ M′,  ∀ v, J(T(J v)) = S v
    e SOBRE o comutante:         ∀ S ∈ M′, ∃ T ∈ M,   ∀ v, J(T(J v)) = S v

— isto é, `J·M·J = M′` NO NÍVEL DA TORRE: a dualidade que hoje `commAlg` tem por
definição teria de ser EXIBIDA pela conjugação. `TheBireference` (v202) prova este
conteúdo inteiro na face finita; **aqui ele vira obrigação tipada no nível onde está
aberto.**

## O QUE ESTA PEDRA NÃO FAZ, dito sem véu

**NÃO há habitante, e não se afirma que haverá em breve.** Construir `J` na torre é o
teorema de Tomita–Takesaki para um fator ITPFI — a mathlib não tem sequer o alicerce
(sem produto cruzado, sem teoria modular). A honestidade da v129 permanece: o traço
morre na torre; o fluxo modular vive; a conjugação é a metade que falta. Os outros três
nomes reservados (`fullTGLWitness`, `continuousModularRealization`,
`unconditionalContinuousCorner`) aguardam os SEUS objetos (`ContinuousCoreData`; o ideal
`K_τ`) e ficam documentados como reservas puras — contrato deles quando o objeto existir,
nunca antes. β jamais entra. Sem sorry, sem axiom. **Nada aqui move o gate — esta pedra
torna ESTRITAMENTE MAIS DIFÍCIL movê-lo.**
-/

namespace TGLExt

open TGL.SpecificAQFT in
/-- **O CONTRATO DA REALIZAÇÃO MODULAR** — o tipo que o nome reservado
    `qgFrontier_modularRealization` terá de habitar. Campos pontuais (função crua +
    cláusulas), para que nenhuma instância de conveniência possa fabricar o habitante. -/
structure ModularRealizationCertificate where
  /-- a conjugação, como função crua na torre. -/
  J : WH → WH
  /-- aditiva. -/
  add : ∀ v w : WH, J (v + w) = J v + J w
  /-- ANTIlinear: `J (c • v) = c̄ • J v`. -/
  conj_smul : ∀ (c : ℂ) (v : WH), J (c • v) = (starRingEnd ℂ) c • J v
  /-- isométrica. -/
  isometric : ∀ v : WH, ‖J v‖ = ‖v‖
  /-- involutiva: `J² = 1`. -/
  involutive : ∀ v : WH, J (J v) = v
  /-- fixa o vácuo da torre: `J Ω = Ω`. -/
  fixes_vacuum : J (hOmega mixProfile) = hOmega mixProfile
  /-- `J M J ⊆ M′`: a conjugação leva o FATOR no comutante — pontualmente. -/
  maps_factor_to_commutant :
    ∀ T ∈ (theFactorObject mixProfile : Set WCLM),
      ∃ S ∈ (commAlg : Set WCLM), ∀ v : WH, J (T (J v)) = S v
  /-- `J M J ⊇ M′`: e SOBRE o comutante — a dualidade deixa de ser definição. -/
  onto_commutant :
    ∀ S ∈ (commAlg : Set WCLM),
      ∃ T ∈ (theFactorObject mixProfile : Set WCLM), ∀ v : WH, J (T (J v)) = S v

/-- ★ o contrato NÃO é vácuo: as cláusulas de dualidade falam das álgebras REAIS da
    rede (o fator da torre e o seu centralizador), não de tipos de conveniência —
    testemunhado pelo fato de que qualquer habitante fornece, para CADA elemento do
    fator, um elemento do comutante pontualmente conjugado. -/
theorem certificate_forces_the_duality (C : ModularRealizationCertificate)
    {T : WCLM} (hT : T ∈ (theFactorObject mixProfile : Set WCLM)) :
    ∃ S ∈ (commAlg : Set WCLM), ∀ v : WH, C.J (T (C.J v)) = S v :=
  C.maps_factor_to_commutant T hT

/-- ★ e um habitante forçaria `J` a ser bijetiva — nenhuma projeção parcial serve. -/
theorem certificate_J_bijective (C : ModularRealizationCertificate) :
    Function.Bijective C.J :=
  Function.bijective_iff_has_inverse.mpr ⟨C.J, C.involutive, C.involutive⟩

end TGLExt
