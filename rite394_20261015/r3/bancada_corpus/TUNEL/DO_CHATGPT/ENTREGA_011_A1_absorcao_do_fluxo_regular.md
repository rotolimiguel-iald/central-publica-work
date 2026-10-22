[REAL — 4 teoremas e 2 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A absorção do fluxo na representação regular existente

2026-09-14T19:41:18.316603-03:00

O campo unitário W já construído por operatorFieldLift satisfaz W S_t W*=Λ_t no mesmo L²(ℝ,H), com S_t f(x)=f(x−t). A família usa o fluxo da torre existente; não introduz um segundo espaço regular. O parâmetro auxiliar da família é matemático, não um acoplamento físico.

Não afirma W∈N, não identifica potências do gerador, não produz o traço.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\absorption_attempts\20260914_191653_842511\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1Absorption']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\independent_20260914_193845_449577\run.json`. `634` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularFlowAbsorption` | `4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9` | `0ea913d2b7eed95bf4d4be76514eebac253eeabf2c058f82ff9cdf3445e3d470` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularFlowField (P : TGLExt.SiteProfile) (a : ℝ) : TGLV350.StrongIntegral.Family
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularFlowField_lift_star (P : TGLExt.SiteProfile) (a : ℝ) :
  Eq.{1} (star.{0} (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P a)))
    (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P (Neg.neg.{0} a)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularFlowField_lift_mul (P : TGLExt.SiteProfile) (a b : ℝ) :
  Eq.{1}
    (HMul.hMul.{0, 0, 0} (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P a))
      (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P b)))
    (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P (HAdd.hAdd.{0, 0, 0} a b)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularFlowField_lift_zero (P : TGLExt.SiteProfile) :
  Eq.{1} (TGLV350.Regular.operatorFieldLift (TGLV350.Regular.regularFlowField P 0)) 1
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularFlowAbsorptionUnitary (P : TGLExt.SiteProfile) :
  ↥(unitary.{0}
      (ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))
        ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularUnitary_shift_conjugate (P : TGLExt.SiteProfile) (t : ℝ) :
  Eq.{1}
    (HMul.hMul.{0, 0, 0}
      (HMul.hMul.{0, 0, 0} (↑(TGLV350.Regular.regularFlowAbsorptionUnitary P)) (TGLV350.Regular.shift t))
      (star.{0} ↑(TGLV350.Regular.regularFlowAbsorptionUnitary P)))
    (TGLV350.Regular.regularUnitary P t)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ABSORCAO_A1B.json` — SHA256 `1379b184f64c62eeb947ad1c45b17ced2694eec0434eb70947b917ab922b5102`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\REVIEW_A1_ABSORCAO_FINAL.json` — SHA256 `29b14a61ac30ba96778d865acbbef0849bddfe48f87464b8b5a6db374d4acd21`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\compilation.json` — SHA256 `9e288a3631a337f06dfd301b815b837fa34acd2a1ed4501a5242a87d11e65c76`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_ABSORPTION.json` — SHA256 `9aad0fb3921a32d1976ae76e5ec697521638c5f5636bad166d8131e02998349d`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# A1: absorção do fluxo regular — seis declarações

2026-09-14T19:39:54.620133-03:00

**A1_REGULAR_FLOW_ABSORPTION_REVIEW_ACCEPTED__GENERATOR_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 6 declarações (4 teoremas, 2 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL — leitura integral] regularFlowField usa x↦modularFlowCLM P(a*x), com continuidade forte e norma ≤1 fornecidas pela isometria existente. As identidades de estrela, produto e zero do lift são especializações de operatorFieldLift; o parâmetro a serve apenas à composição dos campos. O unitário concreto W é o campo com a=1.

[REAL] regularUnitary_shift_conjugate prova W S_t W*=regularUnitary P t como igualdade de CLM no L² regular com fibra TowerHilbert P. A prova usa somente interseções finitas de eventos a.e. para cada f,t e transporte por subtração preservadora de medida. Não exige representante L² pontualmente contínuo nem um conjunto a.e. uniforme para todos os vetores. O cálculo efetivo é Δ_base^{ix}Δ_base^{-i(x−t)}=Δ_base^{it}, com o mesmo modularFlowCLM.

[REAL — ficha] REAPROVEITAMENTO_A1B_ABSORCAO foi lida integralmente e os fornecedores são pinados. Alguns excertos da ficha inicial são cabeçalhos truncados; o exame usa os enunciados completos dos fornecedores/fonte, não deduz tipos desses excertos. O módulo novo foi construído pelo principal e reproduzido pela árvore própria.

[REAL — histórico de leitura] O leitor próprio dos controles concluiu os checks e gravou negative_controls_read.json, mas seu print final falhou em cp1252 (U+2191). A leitura posterior em UTF-8 confirmou o JSON e o Type mismatch. negative_reader_console_erratum.json registra a falha de exibição; nenhum build/prova falhou ou foi repetido por isso.

[REAL] Execução própria rc0 em 37.76 s. 634 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularFlowAbsorption | `4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9` | `0ea913d2b7eed95bf4d4be76514eebac253eeabf2c058f82ff9cdf3445e3d470` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Nenhuma pertença W∈N é declarada ou assumida. O resultado não constrói h nem traço, não identifica ainda potências de um gerador positivo. W atua no Hilbert regular; não substitui J ou U_t do GNS do peso. O parâmetro auxiliar a não é parâmetro físico. Aceitação restrita a quatro teoremas e duas definições; core5, Fourier e grafo têm relatórios separados. Gate, memórias e fontes anteriores permanecem intocados.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\independent_20260914_193845_449577\run.json>) — SHA256 `9e113b1688af8dc26b0ee57c8fb8322eacb7f535f5934d31feae8b6562f3cae1`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\compilation.json>) — SHA256 `9e288a3631a337f06dfd301b815b837fa34acd2a1ed4501a5242a87d11e65c76`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_absorcao\independent_20260914_193845_449577\type_axiom_audit.json>) — SHA256 `d3662b379f5b7d897c5a6545e7cb275b3eab884894399e060081598ba056ecab`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ABSORCAO

[OPEN — ficha anterior à equivalência do grupo regular com a translação]

# A1(b): absorção do fluxo pela coordenada regular

2026-09-14T18:20:06.336840-03:00

Consumidor: `regular_unitary_positive_generator`, LACUNAS_A1.md:31. A rota explícita está em ROTA_GERADOR_REGULAR_A1B.

```text
Build W : unitary (RegularHilbert (TowerHilbert P) →L[Complex] RegularHilbert (TowerHilbert P)) from the existing field x ↦ modularFlowCLM P x. For every P,t, prove W.val * shift t * star W.val = regularUnitary P t. Use operatorFieldLift; prove its adjoint/group/zero identities with field argument scale a only to supply W and its inverse. No new L2, Fourier, modular flow, or GNS. W need not belong to the regular core; do not assert this.
```

O campo é uma instanciação do operatorFieldLift já existente. a é argumento auxiliar da composição de campos; não é parâmetro físico, nem beta. Duas definições (família, unitário) e quatro lemas usados na construção e no consumo. W não é presumido elemento de N. Sem declarar Fourier, traço ou gerador como construídos.

## Fornecedores

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:12` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_constant (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:16` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
def regularUnitary (P : SiteProfile) (t : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2Translation.lean:19` — `1fc45298e186caf37d2b04779e64f3e000e7384511bede3bdce57ab9b429b267`

```lean
theorem shift_ae (t : ℝ) (f : RegularHilbert H) :
    shift t f =ᵐ[volume] fun x : ℝ => f (x-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheModularFlowIsAHorizon.lean:29` — `df9dac92716643a471172afce44a2a158736b2988d51c42ff814505d339b3e7d`

```lean
theorem modularFlowCLM_mul (s t : ℝ) :
    modularFlowCLM P s * modularFlowCLM P t = modularFlowCLM P (s + t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheModularFlowIsAHorizon.lean:40` — `df9dac92716643a471172afce44a2a158736b2988d51c42ff814505d339b3e7d`

```lean
theorem modularFlowCLM_star (t : ℝ) : star (modularFlowCLM P t) = modularFlowCLM P (-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:68` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
theorem modularFlowCLM_isometry (P : SiteProfile) (t : ℝ) :
    modularFlowCLM P t = (modularFlowIsometry P t).toContinuousLinearMap
```

## Buscas

Seis modalidades e recorte adicional em outras bancadas nos JSONs pinados. Foram localizados os fornecedores genéricos e o alvo nomeado nas entregas, não a identidade completa nos recortes consultados. O alcance do índice não é todo o computador. Nenhum fornecedor antigo será alterado. A aceitação exige compilação própria, axiomas e revisão, em entrega separada dos5lemas de ação no core.
