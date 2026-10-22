# B3 — revisão independente final

2026-09-14T17:00:13.174550-03:00 · **B3_DEV_REVIEW**

[REAL] **Aceito no escopo B3. Nenhum P0, P1 ou P2 encontrado.** Os dois módulos e o auditor autoral foram lidos integralmente e reproduzidos por Lake na raiz curta `s`, com auditor próprio de tipos, universos e axiomas. **22 alvos: 14 teoremas, 7 definições e 1 estrutura**, todos restritos a `propext`, `Classical.choice`, `Quot.sound`. Nenhum aviso novo nos módulos B3 ou auditores.

## Reprodução e proveniência

Comando próprio: `lake build TGLExt.TheSameBetaReadsThreeFaces TGLExt.SectorFluidClosure TGLExt.SectorFriedmann TGLExt.AuditSector TGLExt.ReviewSector`, rc0, Lean 4.31.0. Raiz: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`. Tentativa: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b3\independent_20260914_165408_099251`. Foram acrescentadas e recompiladas **17 fontes da cadeia B1** que faltavam em `s`, as três fontes B3 e o auditor próprio: **21 novos objetos**. Os **92 objetos próprios herdados de B2**, suas traces e fontes permaneceram idênticos; total privado medido: 113 objetos. Não foram copiados objetos autorais de TGL/TGLExt.

Mathlib e oito pacotes auxiliares são o cache privado já pinado/reutilizado em B1/B2; não houve reconstrução independente desses pacotes nem da toolchain. A proveniência integral e os mapas de hashes herdados estão ligados em `compilation.json`. O ambiente remove LEAN_PATH/LEAN_SRC_PATH externos; as traces novas não incluem o build autoral ou a raiz B1. As permissões `safe.directory` são apenas nove caminhos privados exatos no ambiente desse processo, sem alteração global. Nenhuma falha nesta tentativa B3; as falhas históricas de preparação B2 continuam preservadas no relatório selado B2.

As fontes novas e seus três objetos correspondentes coincidem byte a byte com o candidato autoral. Relatórios B1/B2, compilation/run B1, manifesto B1, manifesto/recibo B2 e todos os objetos B2 protegidos foram relidos após o build e não mudaram. Só houve acréscimos em `s` e escritas em `revisao_b3`.

## Significado, hipóteses e consumidor

`SectorFluid` contém setores finitos, `rho_nonneg`, `w : ι → ℝ` constante no tempo e **`H_nx` como campo HasDerivAt nomeado**. É uma hipótese de não troca; a prova não a deriva de física microscópica. A multiplicação por `1+c.beta*(1+w_i)` conserva a mesma equação por ser constante no tempo; somas e pressão diferenciável são construídas efetivamente. Não se afirma positividade de cada densidade corrigida para w arbitrário: isso exigiria controlar o respectivo fator. Este limite já consta da ficha.

`corrected_closure` prova a identidade aditiva, e `three_sector_closure` invoca os fornecedores `closure_identity`/`hubble_form`, com o mesmo `c.beta` da estrutura B1. `wEff` é definido como pressão total/densidade total. A leitura `rhoTot*|1+wEff|=enthalpy` usa exatamente **rhoTot>0 e enthalpy≥0**; não há promessa para denominador zero ou entalpia negativa. A identidade aditiva não precisa dessas restrições.

O consumidor `tgl_friedmann_from_sector_closure` **chama o teorema B2 `flrw_friedmann_from_general_metric`** para a métrica e o stress corrigido concretos. A hipótese de conservação desse fornecedor é descarregada por `sector_covariant_conservation`, que usa a divergência tensorial B2 e a continuidade demonstrada a partir de H_nx. **H_null continua INPUT explícito sobre o stress corrigido**, assim como U aberto/preconexo, escala a suave/positiva, tempos em I e G>0. Não há campo que pressuponha a conclusão escalar pretendida. U pode ser vazio: não se declara existência de uma solução física em domínio não vazio.

O resultado geral mantém uma única constante existencial Λ e a convenção herdada `G+Λg=κT`:

`H²=(8πG/3)·rhoTot·(1+beta·|1+wEff|)−Λ/3`;
`H′=−4πG·(correctedTotalRho+correctedTotalPressure)`.

O corolário sem Λ exige **`H_zero_cosmological : cosmological=0`** e a equação métrica tensorial hE explicitamente. É uma especialização condicional, não uma prova de Λ=0. A calibração eta=1/(4G) reutiliza `flrw_newton_coefficient`, mantendo G>0 como INPUT. Não se divide por H nem se exclui H=0. A comparação da segunda equação com a rota de fator sobre o total pertence a B4, não a este aceite.

[DERIVED — inspeção semântica] Não foi encontrada premissa contraditória ou conclusão disfarçada. Como checagem de consistência, setores constantes com w=-1, rho>0 e a constante têm H_nx compatível e o balanço nulo admite a constante Λ correspondente; nenhum novo teorema de existência foi compilado nessa revisão.

## Ficha e controles

Cláusula B3 da ORDEM 012, linhas 117–123, confrontada com os enunciados. A ficha coincide com as hipóteses e consumidores efetivos: 14 locadores de fornecedores conferidos por hash e linha. Metadados locais medidos colocam a ficha antes das três fontes; são evidência de cronologia do filesystem, não selo externo de tempo. Buscas autorais e limites foram lidos, sem refazê-los ou alegar exaustividade. Os consumidores Python são apenas propostas citadas na ficha: não houve leitura/execução de um.py nem revisão de sua instalação.

`AUDITORIA_B3.json` e seus streams foram relidos e pinados. `BadSectorClosure` troca +beta por −beta; `BadSectorAbs` troca entalpia por seu negativo. Ambos terminam rc1 por **Type mismatch**, com imports reconhecidos, sem erro de sintaxe/ambiente. São controles **executados pelo autor**, não novas execuções minhas. As 22 saídas autorais coincidem com o auditor próprio. A preservação autoral de 941 fontes/um foi relida como [DECLARADO]; não se reabriu esse inventário. Foram preservados 2 avisos dos fornecedores B1 recompilados, detalhados no JSON; nenhum é aviso B3.

## Pins e evidência

| Arquivo | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---|---|
| SectorFluidClosure | `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3` | `9c4f8400d1ff399c396e00b17c8af7ddf22f21fc2c5d133b93d90c641b11ea5a` |
| SectorFriedmann | `7c115dd6a8d71333d8811a6efbf7d46d4363e25d18b23f8c7e678e951c0b9dfa` | `844dbc122da8bba8e3328b2a498c50819be18c22e57f805f3a55459064785289` |
| AuditSector | `4aa3174a76989847aed15152d1b7bf84e0b7808b7d6ab50728876bf3b17ddb65` | `95ece8c78a451be61bd948e914848f8856d1ccb21baa32153902b7d7f4403ba6` |

- [Revisão JSON](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/REVIEW_B3_FINAL.json>) — SHA256 `df0a2465e4821cd650d2cd783bc22b865ffd9091ccdd8632a576824bfb875ef7`.
- [Compilação independente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/compilation.json>) — SHA256 `588747431fef8fc6b0813956c2a50c0400e7df9bb76a816986115902f11daf9c`.
- [Run rc0](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/independent_20260914_165408_099251/run.json>) — SHA256 `66d5b718ea2cc12d1bf53d7d1511e226f92272022ba53504030f2fcdc248a310`.
- [Snapshot e dependências](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/independent_20260914_165408_099251/snapshot.json>) — SHA256 `10c894d0ef3cfcc70e862114dd5a17e59d9fbea13da918caad8bcf376b4cbb7b`.
- [Inspeção semântica](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/independent_20260914_165408_099251/semantic_inspection.json>) e [ficha/contrato](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b3/independent_20260914_165408_099251/contract_and_fiche.json>).

## Alvos auditados

- `ChatgptAudit.FLRW.SectorFluid`
- `ChatgptAudit.FLRW.SectorFluid.totalRho`
- `ChatgptAudit.FLRW.SectorFluid.totalPressure`
- `ChatgptAudit.FLRW.SectorFluid.enthalpy`
- `ChatgptAudit.FLRW.SectorFluid.wEff`
- `ChatgptAudit.FLRW.SectorFluid.correctedRho`
- `ChatgptAudit.FLRW.SectorFluid.correctedTotalRho`
- `ChatgptAudit.FLRW.SectorFluid.correctedTotalPressure`
- `ChatgptAudit.FLRW.SectorFluid.enthalpy_eq`
- `ChatgptAudit.FLRW.SectorFluid.sector_rescaling_preserves_continuity`
- `ChatgptAudit.FLRW.SectorFluid.corrected_closure`
- `ChatgptAudit.FLRW.SectorFluid.weighted_continuity`
- `ChatgptAudit.FLRW.SectorFluid.total_continuity`
- `ChatgptAudit.FLRW.SectorFluid.corrected_rho_deriv`
- `ChatgptAudit.FLRW.SectorFluid.corrected_pressure_differentiable`
- `ChatgptAudit.FLRW.SectorFluid.corrected_continuity`
- `ChatgptAudit.FLRW.SectorFluid.effective_enthalpy`
- `ChatgptAudit.FLRW.SectorFluid.multiplicative_closure`
- `ChatgptAudit.FLRW.SectorFluid.three_sector_closure`
- `ChatgptAudit.FLRW.sector_covariant_conservation`
- `ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure`
- `ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological`

**Escopo encerrado:** DEV B3, com a ligação condicional B1→conservação setorial→B2. Sem pendência de análise/recompilação deste delta. Não é aceite de integração, alteração de gate, B4–B6, TGL-S/TGL-L, fecho global ou confirmação empírica. Fontes autorais, B1/B2 selados, memórias e dados não foram alterados.

Registro de preparação do parecer: a primeira chamada do finalizador Python falhou por usar `lambda` como nome de argumento, antes de gravar o parecer. Script/log preservados em `finish_b3_preparation_failure.json`; versão v2 corrigida executou. Não foi falha Lean e não houve nova compilação. `all_attempts_exit_zero` em compilation refere-se às execuções Lake B3.
