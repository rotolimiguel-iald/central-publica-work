[REAL — 3 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Afiliação do gerador regular pela preservação do grafo

2026-09-14T20:01:48.208422-03:00

Pareamentos locais de operadores que comutam com caracteres, já provados, dão comutação com o multiplicador real limitado. A conjugação por V e N duplo comutante igual N mostram que o MESMO resolvente R pertence ao core. Todo B em N comutante preserva o grafo (1−R)x=Ry do gerador existente; em particular, unitários e seus adjuntos dão a invariância de domínio exigida pelo critério de afiliação. Não se presume V ou W no core nem se fabrica outra forma afiliada.

Afiliação é afirmada pelo critério de preservação do mesmo grafo fechado e densamente definido, com fornecedores anteriores explícitos. Escala dual e construção do traço são obrigações posteriores. Este delta não fornece RegularCoreTraceData nem identifica h com o operador modular no GNS.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | NÃO PAGO por esta entrega. |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\regular_affiliation_attempts\20260914_194213_988062\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RegularAffiliation']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\independent_20260914_195807_303135\run.json`. `646` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularGeneratorAffiliation` | `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e` | `18cc5596a146aa267bb3f9f84a052acc22cb44f8043bbbda8005e9c561e13d4f` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.character_commutation_realScalarMultiplier {H : Type} [NormedAddCommGroup.{0} H]
  [InnerProductSpace.{0, 0} ℂ H] [CompleteSpace.{0} H]
  (B :
    ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert H)
      ↥(TGLV350.Regular.RegularHilbert H))
  (hB :
    ∀ (s : ℝ),
      Eq.{1} (HMul.hMul.{0, 0, 0} (TGLV350.Regular.characterMultiplier s) B)
        (HMul.hMul.{0, 0, 0} B (TGLV350.Regular.characterMultiplier s)))
  (g : ℝ → ℝ) (hg : Continuous.{0, 0} g) (h0 : ∀ (x : ℝ), LE.le.{0} 0 (g x)) (h1 : ∀ (x : ℝ), LE.le.{0} (g x) 1) :
  Eq.{1} (HMul.hMul.{0, 0, 0} (TGLV350.Regular.realScalarMultiplier g hg h0 h1) B)
    (HMul.hMul.{0, 0, 0} B (TGLV350.Regular.realScalarMultiplier g hg h0 h1))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularSpectralResolvent_mem (P : TGLExt.SiteProfile) :
  Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (TGLV350.Regular.regularSpectralResolvent P)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularPositiveGenerator_commutant_graph (P : TGLExt.SiteProfile)
  (B :
    ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))
      ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P)))
  (hB : Membership.mem.{0, 0} (VonNeumannAlgebra.commutant.{0} (TGLV350.Regular.regularCoreAlgebra P)) B)
  (x y : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P)))
  (hxy :
    Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
      (Prod.mk.{0, 0} x y)) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
    (Prod.mk.{0, 0} (B x) (B y))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_AFILIACAO_REGULAR_A1B.json` — SHA256 `d1562e937478b7729a07cc819e39a61878d0a8420d655149eeaec718e728cbc5`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\REVIEW_A1_REGULAR_AFFILIATION_FINAL.json` — SHA256 `2cf3f8f9b6b3dcede35a804d2b6ea8811444efeb9ba3529923cb6990b41d7c86`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\compilation.json` — SHA256 `fa00d5881f16f87ebb1f9090621ae5a326b3a3779af87b70964c305eb2fcc8c9`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_AFFILIATION.json` — SHA256 `4a2e76cd4bb3eeff01f49b189e67815bccd5cc428c13a423c0da1d56af7d6ecf`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — afiliação do gerador regular existente

2026-09-14T19:59:26.236557-03:00

**A1_REGULAR_AFFILIATION_REVIEW_ACCEPTED__DUAL_SCALING_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 3 declarações (3 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Fonte e ficha foram lidas integralmente. O primeiro teorema consome character_commutation_local_pairing já reproduzido, cuja igualdade AE decorre da unicidade Fourier dos pareamentos L¹. Para cada par de vetores, integra os pareamentos com o multiplicador limitado g∈[0,1]; a orientação do adjunto respeita o produto interno complexo, linear no segundo argumento. Só há interseção finita de eventos AE. Não é necessário decompor B em um campo nem supor separabilidade da fibra.

[REAL] Para B∈N′, C=V⁻¹BV comuta com todos os caracteres: s=2πt abrange todas as frequências, e a conjugação existente V·character=regularUnitary·V é usada com regularUnitary∈N. Aplicado ao sigmoid, o primeiro teorema dá comutação de C com o multiplicador M. Conjugação e N″=N fornecem a pertença do mesmo regularSpectralResolvent em regularCoreAlgebra, sem assumir que V ou W pertençam ao core.

[REAL] O teorema final conserva o grafo de regularPositiveGenerator, escrito exatamente como (1−R)x=Ry. A comutação RB=BR leva a (1−R)Bx=RBy para todo B∈N′ e todo par original do grafo. Assim preserva domínio e valor do operador parcial fechado já construído, não apenas um subconjunto denso ou uma forma afiliada substituta.

[DERIVED — leitura do critério] Para unitários de N′, aplicar a mesma preservação ao unitário e ao seu adjunto dá invariância em ambos os sentidos. Junto ao fechamento e domínio denso já pagos para h, esta é a afiliação pelo critério de comutação do grafo. O delta não cria uma instância abstrata AffiliatedPositiveForm nem precisa dela para essa afirmação.

[REAL] As três declarações não recebem afiliação, pertença do resolvente ou identificação de potências como novas premissas concretas. A ficha antecede o DEV; buscas são recortes, não exaustividade universal. O negativo autoral de fator 2 na segunda componente do grafo é lido com diagnóstico e pins, sem executá-lo novamente.

[REAL] Execução própria rc0 em 38.7 s. 646 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularGeneratorAffiliation | `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e` | `18cc5596a146aa267bb3f9f84a052acc22cb44f8043bbbda8005e9c561e13d4f` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Aceite separado de três teoremas e nenhuma definição; não altera os deltas anteriores nem agrega suas contagens. Afiliação aqui é a preservação do mesmo grafo por N′; não é construção de traço, escala sob a ação dual, nem identificação automática com o operador modular do peso. Escala dual e traço A1(b) continuam abertos. Gate, canônico, programa terminal e memórias não foram tocados. A compilação reaproveita objetos próprios anteriores e cache de pacotes pinado; nenhuma biblioteca inteira foi recompilada e nenhum objeto autoral/DEV foi herdado.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\independent_20260914_195807_303135\run.json>) — SHA256 `b07bd2f568c76299791253278717d5cdc7c65d2de6cafd23bf2c729c2b6a8f2c`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\compilation.json>) — SHA256 `fa00d5881f16f87ebb1f9090621ae5a326b3a3779af87b70964c305eb2fcc8c9`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_afiliacao\independent_20260914_195807_303135\type_axiom_audit.json>) — SHA256 `f992f4e2166ab234af396a034da01260570b551df336926733bc535b92a47fa8`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR

[OPEN — ficha anterior à afiliação do mesmo gerador regular]

# A1(b): o resolvente pertence ao core

2026-09-14T19:37:20.302875-03:00

Prove on the existing regular space: regularSpectralResolvent P belongs to regularCoreAlgebra P; every B in its commutant preserves the graph of the already constructed positive generator. Reuse local pairings from character commutation, conjugation by V=W F^-1 and the double commutant. No simple-function approximation machinery, new affiliated-form object or replacement generator. This is the commutant criterion of affiliation of the closed operator; dual scaling and trace remain separate.

A prova usa character_commutation_local_pairing antes de tentar reconstruir funções simples. O critério de afiliação é a preservação do grafo por todo operador do comutante. O grafo anterior é mantido intacto; não se confunde com as formas afiliadas de outro contrato.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CharacterLocality.lean:40` — `7a5d2f1b70b3d61307045c4460034e3821976c8b30b02d5bcf165d157f33419a`

```lean
theorem character_commutation_local_pairing
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (f g : RegularHilbert H) :
    (fun x : ℝ => inner ℂ ((B.adjoint f) x) (g x)) =ᵐ[volume]
      (fun x : ℝ => inner ℂ (f x) ((B g) x))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:30` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:65` — `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`

```lean
theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:20` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_equation (R : H →L[ℂ] H) (hi : Function.Injective R) (x y : H) :
    (x,y) ∈ (resolventGraphOperator R hi).graph ↔ (1-R) x = R y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularGeneratedAlgebra.lean:57` — `252b0fa3d5e37c42827efccfc26a555db80ac5c20a6f94269060ce2b3dcb5f71`

```lean
theorem regularUnitary_mem (P : SiteProfile) (t : ℝ) :
    regularUnitary P t ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:133` — `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`

```lean
theorem mem_commutant_iff {S : VonNeumannAlgebra H} {z : H →L[ℂ] H} :
    z ∈ S.commutant ↔ ∀ g ∈ S, g * z = z * g
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:139` — `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`

```lean
theorem commutant_commutant (S : VonNeumannAlgebra H) : S.commutant.commutant = S
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_affiliation\20260914_193659_398254\searches.json. Ausência nominal nos recortes não é ausência universal.
