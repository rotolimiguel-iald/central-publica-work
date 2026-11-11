import TGLExt.StrongFrame

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA AQFT COMPLETA: o contrato tipado da metade v2
  [TGLExt — v104, o incremento 22 do programa SemifiniteAnalysis]

A MAIOR LACUNA MATEMÁTICA DA TGL, bem-posta: o nome reservado
`qgClosureCertificateV2` (a testemunha canônica do transporte de
fronteira) nunca teve um TIPO. Esta pedra o dá — `FullWitnessData`,
o contrato MÁXIMO tipável na mathlib de hoje:

* a base é o certificado FORTE (v103: Dirac genuinamente ilimitado,
  fibra ∞-dim, frame não-constante);
* a AÇÃO EXTERNA vira AÇÃO GEOMÉTRICA DE GRUPO: lei de grupo
  (`act_one`, `act_mul`), monotonia nas regiões (`act_mono`),
  NÃO-TRIVIALIDADE geométrica (`geometric_nontrivial` — mata a ação
  constante do v101, POR TEOREMA: `isotone_cannot_feed_witness_geometry`);
* o QUADRADO DE COVARIÂNCIA (`covariant_inclusions`):
  U_g ∘ ι_{O₁→O₂} = ι_{gO₁→gO₂} ∘ U_g — a rede é covariante;
* a LEI DO FLUXO por região (`flow_law`, v102 elevado a exigência):
  σ_{s+t} = σ_s ∘ σ_t — o transporte modular é a família com lei.

O QUE AINDA NÃO É TIPÁVEL (nomeado, SEM VÉU — é o programa):
fator III₁ das álgebras locais (teoria modular de vN ausente na
mathlib), afiliação semifinita, H3 DERIVADO da dinâmica, spin-2
contínuo, e a identificação de G com o grupo de Poincaré. A
TESTEMUNHA EXISTE NA MATEMÁTICA [KNOWN]: o campo escalar livre
satisfaz TUDO isto (Bisognano–Wichmann; Araki) — o que falta é a
FORMALIZAÇÃO, não a existência. O nome `qgClosureCertificateV2`
segue RESERVADO: só será construído quando o tipo capturar o
espírito inteiro (a lição do v103 vale uma escada acima).

★ `strongFromWitness` — toda testemunha completa REDUZ ao
certificado forte (a ponte de tipos);
★ `constant_action_cannot_witness` / `isotone_cannot_feed_witness_geometry`
— os dentes: a ação constante e o habitante v101 NÃO testemunham.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [DATA — O CONTRATO DA TESTEMUNHA COMPLETA, metade tipável] a rede
    FORTE com ação geométrica de grupo, covariância das inclusões e lei
    do fluxo. A metade não-tipável (III₁, afiliação, H3 derivado,
    spin-2 contínuo, Poincaré) está nomeada no cabeçalho e NÃO é
    substituída por proxies falsos. -/
structure FullWitnessData extends QGClosureCertificateStrong where
  [instG : Group core.net.G]
  act_one : ∀ O, core.net.act 1 O = O
  act_mul : ∀ g h O,
    core.net.act (g * h) O = core.net.act g (core.net.act h O)
  act_mono : ∀ (g : core.net.G) {O₁ O₂ : Region},
    leR O₁ O₂ → leR (core.net.act g O₁) (core.net.act g O₂)
  geometric_nontrivial : ∃ (g : core.net.G) (O : Region),
    core.net.act g O ≠ O
  flow_law : ∀ (O : Region) (s t : ℝ) (x : H O),
    core.net.internal O (s + t) x
      = core.net.internal O s (core.net.internal O t x)
  covariant_inclusions : ∀ (g : core.net.G)
      {O₁ O₂ : Region} (hle : leR O₁ O₂) (x : H O₁),
    core.net.external g O₂ (core.net.incl hle x)
      = core.net.incl (act_mono g hle) (core.net.external g O₁ x)

/-- [KERNEL] ★ A PONTE DE TIPOS: toda testemunha completa reduz ao
    certificado forte — o v2 CONTÉM o v1 endurecido. -/
def strongFromWitness (w : FullWitnessData) : QGClosureCertificateStrong :=
  w.toQGClosureCertificateStrong

/-- [KERNEL] ★ o dente abstrato: a ação CONSTANTE não testemunha
    geometria (nenhum g move nenhuma região). -/
theorem constant_action_cannot_witness {Region G : Type} :
    ¬ ∃ (g : G) (O : Region), (fun (_ : G) (O' : Region) => O') g O ≠ O := by
  rintro ⟨g, O, h⟩
  exact h rfl

/-- [KERNEL] ★ o dente VIVO: a rede v101 age TRIVIALMENTE nas regiões
    (act g O = O por definição) — theIsotoneNet NÃO testemunha
    `geometric_nontrivial`. A face geométrica está genuinamente ABERTA. -/
theorem isotone_cannot_feed_witness_geometry :
    ¬ ∃ (g : Bool) (n : ℕ), theIsotoneNet.net.act g n ≠ n := by
  rintro ⟨g, n, h⟩
  exact h rfl

end

end TGLExt
