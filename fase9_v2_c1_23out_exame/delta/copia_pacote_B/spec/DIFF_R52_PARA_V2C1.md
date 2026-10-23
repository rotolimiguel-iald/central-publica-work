# DIFF R5.2-E1 -> V2-c1 «O Teste da Unica Palavra» (cada mudanca atribuida)

Pai: R5.2-E1 `81a970926345832a` (spec canonico `406d9d2dde90d6d2`). Filha: `e7c47cbcbbcd3a7a` (spec canonico `db1ccecbc1718e69`). Patch linha a linha (JSON ordenado, indent 1): `spec/DIFF_R52_PARA_V2C1.patch` (652 linhas).

Legenda: **OP-a..d** = decisao do operador de 23/10/2026 (verbatim sha256 `363da49371de4d8f`); **C1-...** = ordem da gerencia c1 (reversivel ate o congelamento).

| secao | tipo | atribuicao | o que mudou |
|---|---|---|---|
| `S5_propagacao` | nova | C1-S5 fundo propagado | secao nova: propaga H0, Omega_m, Omega_r do fundo na covariancia marginal (S5 do levantamento) |
| `alcance` | nova | OP-a ALCANCE | secao nova: FALSIFIED_AT_5SIGMA = beta_TGL refutado na natureza, voz unica, sem saida posterior; validade do kernel fora de jogo; pre-registro = devido processo |
| `calibracao_de_cauda` | nova | C1-CAL calibracao de cauda | secao nova |
| `decisoes_padrao_da_gerencia` | alterada | OP-c D-H | D-H: pendente -> admitido |
| `decisoes_padrao_da_gerencia` | alterada | OP-d D-J | D-J: pendente -> decidido |
| `decisoes_padrao_da_gerencia` | alterada | OP-b X13 | NAT22_X13: pendente -> decidido |
| `especificacao_do_runner` | alterada | C1-E5 modo observado | R0-R8 reescritos para o modo observado |
| `estado` | alterada | C1-ID versao/estado | texto do estado |
| `estatisticas` | alterada | OP-b X13 | background: 'NAT22 pending' -> marginalizado pelo executor (X13 = SIM) |
| `estatisticas_do_executor` | nova | OP-b X13 | secao nova: o texto da V2 descreve o que o executor faz (fundo marginalizado; z_delta pelo perfil com log-det; ln B com n >= 100; ln B(TGL/beta-livre) = 1,97) |
| `estatisticas_do_executor` | nova | C1-CAL calibracao de cauda | linha 'z_calibrado': a funcao le o z equivalente do p calibrado |
| `estatisticas_executor_observado_sujeito_NAT22` | removida | OP-b X13 | removida (NAT22 pendente -> decidido) |
| `freeze_preflight` | alterada | OP-b X13 | X13 satisfeito |
| `freeze_preflight` | alterada | OP-c D-H | D-H satisfeito |
| `freeze_preflight` | alterada | C1-TRAVA recibo de congelamento | a guarda documental vira a trava executavel (recibo de congelamento + recibo de abertura) |
| `funcao_de_veredito` | alterada | OP-d D-J | nome, fonte e sha256 (3 trocas literais no texto: nome, docstring, base do token); final_token; testes de ramo regenerados |
| `funcao_de_veredito` | alterada | OP-c D-H | n_alvos_declarados_rule: 2 (L1b, L6) -> 0; se_abrir_hoje |
| `funcao_de_veredito` | alterada | C1-CAL calibracao de cauda | entrada_calibrada: a funcao le z equivalente de p calibrado; logica e limiares NAO mudam |
| `funcao_de_veredito_proposta` | alterada | OP-d D-J | final_token_name e status |
| `funcao_de_veredito_proposta` | alterada | OP-c D-H | n_alvos_declarados: 2 -> 0 |
| `generated_from` | alterada | C1-ID versao/estado | entram o pai (R5.2-E1) e a fala do operador de 23/10 |
| `id` | alterada | C1-ID versao/estado | novo id |
| `leitores` | alterada | OP-c D-H | os 8 leitores: source_admission PENDING_D_H -> ADMITTED_BY_OPERATOR_D_H_23OUT2026; L1b e L6 passam de DECLARADO_UNVERIFIED a REAL_DOCUMENTARY_HASH_ONLY; caminhos viram relativos ao pacote (copias dos bytes, hashes identicos) |
| `nao_decide` | alterada | OP-a ALCANCE | 'beta (a regra matriz)' vira 'a derivacao de beta ... e a validade do kernel' (o teste decide beta na natureza, nao a derivacao); saem D-H e NAT22/X13 (decididos); entra a creditacao |
| `pending_operator_decisions` | alterada | OP-b X13 | X13 sai da lista (decidido) |
| `pending_operator_decisions` | alterada | OP-c D-H | D-H sai da lista (decidido) |
| `pending_operator_decisions` | alterada | OP-d D-J | D-J sai da lista (decidido) |
| `pending_operator_decisions` | alterada | C1-TRAVA recibo de congelamento | entram os dois recibos |
| `registro_dh` | nova | OP-c D-H | secao nova: aponta o registro D-H pinado (8 leitores, sha256, regra de extracao testada contra os bytes; L1b e L6 baixados em 23/10) |
| `runner_contract` | alterada | C1-E1 fornecedor real do fundo | fornecedor real do fundo BG1 (nao mock) |
| `runner_contract` | alterada | C1-E2 reproducao do fundo | reproducao do fundo: H0 e sigma; diverge interrompe |
| `runner_contract` | alterada | C1-E3 quadraturas 100/200 | tolerancia 1e-6 e recusa entre as quadraturas 100/200 |
| `runner_contract` | alterada | C1-E4 registro D-H pinado | n_alvos e fontes admitidas vem do registro D-H pinado |
| `runner_contract` | alterada | C1-E5 modo observado | ordem PODER_ANTES_DE_ABRIR -> fonte lida uma vez -> funcao pinada; proibido ALVOS a mao |
| `runner_contract` | alterada | AUD-B4/B3/B5/B6 (auditoria C08, confirmada pela gerencia) | abertura unica por marcador; mapa monotono; constantes S5 cobradas; python -B e pycache |
| `sistematicas` | alterada | C1-S5 fundo propagado | entrada S5 |
| `sistematicas` | alterada | C1-CAL calibracao de cauda | entrada calibracao |
| `source_admission` | alterada | OP-c D-H | PENDING -> ADMITTED; as travas passam a ser os dois recibos |
| `state` | alterada | C1-ID versao/estado | RASCUNHO_NAO_CONGELADO -> PREPARADO_NAO_CONGELADO |
| `supersede` | alterada | C1-ID versao/estado | aponta a R5.2-E1 como pai |
| `token` | nova | OP-d D-J | secao nova: token TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL + a ordem do sufixo |
| `token_base_provisorio` | removida | OP-d D-J | removida |
| `token_estado` | removida | OP-d D-J | removida |
| `trava_de_congelamento` | nova | C1-TRAVA recibo de congelamento | secao nova |

## O que NAO mudou (conferido por igualdade canonica)

`base`, `beta`, `lei` (K congelado = 1,0838071748529643), `hipoteses`, `familias`, `fundos`, `poder_previo`, `covariancia` (grade, amplitudes, extremos pinados), `novidade_de_uso`, `contaminacao_declarada`, `D5_*`, `observable_TGL_H0_map`, `f34_duas_testemunhas`, `source_pin_verification_R4`, `mu_do_rito`, `gate`. Na funcao de veredito: **a logica de precedencia e todos os limiares sao os da R5.2** (so mudam o nome, a docstring e a base do token).

Secoes inalteradas: `D5_local_compression`, `D5_sensitivities_from_c1_audit`, `achados`, `base`, `beta`, `contaminacao_declarada`, `covariancia`, `f34_duas_testemunhas`, `familias`, `fontes_lidas_sha256`, `fundos`, `gate`, `hipoteses`, `lei`, `mu_do_rito`, `novidade_de_uso`, `observable_TGL_H0_map`, `poder_previo`, `source_pin_verification_R4`
