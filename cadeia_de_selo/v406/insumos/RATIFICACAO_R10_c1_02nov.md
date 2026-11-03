# RATIFICAÇÃO R10 DA GERÊNCIA c1 — a passagem para o contínuo (os 21 campos) e o certificado de Fock físico

> **Estado deste documento: RATIFICADO (02/11/2026); o R3 formal fechou no sandbox, ver §4** (a recompilação no sandbox ainda roda; a linha «Compilação no sandbox» abaixo fica vazia até o `DONE.txt`). A ratificação é ato da gerência, distinto da construção (bancada do ChatGPT, 15–16/10/2026) e das duas revisões (Sonnet, 02/11/2026). Não é confirmação da teoria, não move gate, não entra no um.py: entrar é o bloco 3, por versão decidida pelo operador.

## 1. O que foi ratificado, e por quem construído e revisado

| papel | quem | artefato |
|---|---|---|
| construção | bancada do ChatGPT (missão F1.FECHO_20261015, R7) | `B\takesaki_fock\CanonicalFockModularCoreInputR1.lean` (`modularCoreInput`, `physicalFockCertificate`), `B\orbital_rotation\PhysicalCanonicalNetCompleteR1.lean` (`physicalCanonicalNet`) |
| aceite da bancada | agente do Codex (`codex-mission-memory-review`) | `R52_R7_FULL_REVIEW_R1.json`: `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE`, 21 campos |
| revisão distinta (1ª por outra família de modelo) | Sonnet (agente desta sessão, por decisão do operador: «designe para o Sonnet revisar tudo») | `revisoes\REVISAO_R10_CADEIA_DO_TRACO_SONNET_02nov.md` (sha16 `1aa44a0cbeab51af`): 21 campos, nenhum SUSPEITO; 17 HONESTO, 4 HONESTO COM RESSALVA (trace, PF, Pp, Pm) |
| leitura própria da gerência | c1 (este documento) | as definições abaixo, lidas na fonte em 02/11/2026 |
| recompilação do fonte no sandbox do kernel v405 (R3 formal) | script `integrar_fecho_bancada_02nov.py` (tarefa agendada `IALD_integracao_R3`) | `integracao_R3_20261102_184921\{MANIFEST,SUMMARY,CHECK_axioms}.json/txt` |

`B` = `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\`.

## 2. O que a gerência leu com os próprios olhos [REAL]

1. **O traço** (`CanonicalFockCyclicTraceCompletionR3.lean:31-32`): `cyclicTraceCandidate a := ⨆ (p : PositiveInput) (_ : ShiftRelated (positiveAsCore p) a), value p`, o supremo do peso positivo `value` sobre os positivos shift-equivalentes a `a`. **`ShiftRelated`** (`TGLExt\V354TraceShiftEquivalence.lean:11-13`): `∃ n > 0, ∃ r s, a r = r b ∧ s a = b s ∧ aⁿ = r s ∧ bⁿ = s r`. A ciclicidade `trace (x y) = trace (y x)` é da relação (`ShiftRelated.cyclic`, r = x, s = y, n = 1): o conteúdo está em `positiveShift_value_compatible` (o peso positivo é invariante entre positivos shift-equivalentes) e em `cyclicTraceCandidate_positive` (nos positivos o traço É `value`). É a mesma rota já aceita no kernel para a torre (V354), transportada ao Fock com insumos próprios (peso dual, lei quadrática pelo Tomita do peso, canto de Weyl).
2. **O «1» de P_F** (`CanonicalFockFiniteProjectionR3.lean:121-130`, `dual_calibration`): `value (positiveDual (log (value X).toReal) X) = 1`, pela escala `e^{−s}` da ação dual. A unidade do traço do núcleo é POSTA pela calibração: o traço é único a menos de escala e a escala corre com a ação dual. É a forma matemática da frase do operador «o um absoluto é a luz comprimida pelo ACOM em UM absoluto», e é consistente com «um Um posto».
3. **As metades** (`CanonicalFockNormalizedSplitR5.lean:225-233`, `normalized_split_exists`): `∃ q r` projeções, `q r = 0`, `value (q + r) = 1`, `value q = value r`, por um lema genérico alimentado por `dual_calibration` e `finite_split_support` (equivalência de Murray–von Neumann + tracialidade, segundo o revisor; a gerência leu o enunciado e a montagem, não o lema genérico linha a linha). O habitante usa `Classical.choose` sobre essa existência: PF/Pp/Pm são escolhidos, não canônicos; o tipo não pede canonicidade.
4. **O habitante** (`CanonicalFockModularCoreInputR1.lean:77-100`): os 21 campos preenchidos, `trace := cyclicTraceCandidate`, `PF := positiveAsCore (add leftPositive rightPositive)`, `trace PF = 1` (`modularCoreInput_PF_trace`), `trace_additive` e `equal_halves` por `value_add` e pelo split; `physicalFockCertificate := physicalModularCoreInput.toCertificate` (l.127) sobre `physicalCanonicalNet`.
5. **A rede física** (`PhysicalCanonicalNetCompleteR1.lean:212-222`): `K := compactPhysicalNet` (campos localizados de suporte compacto da frente Maxwell), com `K_mono`, `K_local`, `K_translate`, `K_boost` e `wedge_glue` como TEOREMAS; `physical_canonical_net_nonzero` e `physical_canonical_net_zero_refused` para a cunha.
6. **O recibo** (`orbital_rotation\attempts\20261016T210640_174717Z\RECEIPT.json`): `exit_code 0`, Lean 4.31.0, 65,8 s; `AXIOMS.txt` com 0 `sorryAx` e `modularCoreInput` no trio; 474 fontes com sha256, todas no disco e íntegras (conferido por script em 02/11).

## 3. As ressalvas, ditas antes de qualquer uso [OPEN / KNOWN / DECLARADO]

- **K(O) ≠ ⊥ para O compacto não está provado** (busca do revisor, citada no relatório dele). A não-trivialidade da rede é teorema só na cunha. O tipo `CanonicalNetInput` não exige mais; a física (álgebras locais não triviais, Reeh–Schlieder) fica [KNOWN/OPEN]. Registrado como pendência do bloco 2.
- **«Núcleo II_∞»** no docstring do campo `PF` (`CanonicalModularCoreAssemblyR1.lean:54`) não é provado nem exigido pelo tipo: lê-se [KNOWN/DECLARADO], não como resultado do habitante.
- **O traço não é funcional linear** nem aditivo fora do cone positivo (escopo declarado do parecer R7); o tipo não pede. Fora dos positivos, onde não há positivo na classe, o valor é 0 [DERIVADO pelo revisor, não checado no Lean].
- **R7 foi Codex revisando Codex**; a revisão Sonnet de 02/11 é a primeira por outra família de modelo, sem compilação própria; a compilação independente é o R3 desta sessão.
- **12 linhas `#eval IO.FS`** (instrumentação) em dois módulos: removidas pelo driver na integração; não afetam provas.
- **R4/R5 da missão da bancada** (identificação do dispositivo físico: MQC, Supercondutor ou Ψ-NET) seguem bloqueados pelo operador e NÃO entram nos 21 campos nem nesta ratificação.

## 4. Compilação no sandbox (R3 formal) — preenchido em 20261102_194026

- Sandbox: `C:\t\k405c\final` (cópia do kernel v405 + mathlib pinada); driver `integrar_fecho_bancada_02nov.py` (sha16 `0a6d570b9db924ca`), tarefa agendada `IALD_integracao_R3`; duas passadas (`integracao_R3_20261102_184921`: 285 compilados, 1 falha por blocos `#eval` multilinha removidos pela metade, 14 bloqueados; `integracao_R3_20261102_192452`: os 15 restantes, retomando os 285).
- Fontes: 475 (474 do recibo + a raiz), todas conferidas por sha256 contra o recibo da bancada; 174 idênticas ao kernel (a menos de linhas em branco); 1 «conflito» (`CanonicalGammaNoFixedR4`: só os literais de nomes de módulo dentro de um bloco `run_cmd`; o kernel prevalece; nenhum módulo novo o importa); **300 módulos novos recompilados do fonte, 0 falhas, 0 bloqueados** (soma das duas passadas); logs por módulo em `MANIFEST.json`.
- `#print axioms` (`CHECK_axioms.txt`, rc 0): `modularCoreInput`, `physicalModularCoreInput`, **`physicalFockCertificate`** e `physical_trace` dependem só de `[propext, Classical.choice, Quot.sound]`.
- O `.olean` de `TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1` existe no sandbox; a candidata `CanonicalFullTGLWitnessR1` (`canonicalFullTGLWitness := ⟨lightNet physicalFockCertificate, lightRealization physicalFockCertificate⟩`) compila sobre ele (resultado registrado à parte).

## 5. Veredito

**RATIFICADO pela gerência c1 em 02/11/2026**, como validade (termo no kernel, recompilado do fonte no sandbox do kernel v405, só o trio de axiomas): `RemainingModularCoreInput D` está habitado por construção genuína para todo `D : CanonicalNetInput` (`modularCoreInput`), e `FockCertificate` está habitado sobre a rede física `physicalCanonicalNet` (`physicalFockCertificate`), com as ressalvas do §3 ditas e mantidas (K(O) ≠ ⊥ só na cunha; «núcleo II_∞» como [KNOWN/DECLARADO]; traço ENNReal cíclico, não linear; R7 Codex×Codex; R4/R5 fora). NOT_FALSIFIED nunca é CONFIRMED; a confirmação segue creditação; o gate não se move; o que entra no um.py (bloco 3, v406) é decisão do operador, já dada em 02/11 («compile a nova versão … rode, publique e atualize tudo»).
