# RELATÓRIO PÓS-TREINO v405 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_01nov_concordo_com_tudo_deixe_tudo_pronto_isso_e_a_TGL_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| x_diario | True | 2026-11-01T17:36:02 | {"rc": 0} |
| S0_treino | True | 2026-11-01T22:06:02 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-01T22:06:02 | {"sha16": "a7bd1ae9b64b8204", "resumo": {"candidato_sha16": "0030242565cc13f6", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v405.json", "sha16": "5ff3a6bdee1a106f", "rc": 0}, "p00": {"ok": true, "passaram": 119, "n": 119, "sha16": "b41cf777b59ee90f"}, "ensaio_a_seco": {"veredito": "TUDO PASSOU", |
| S1b_revisao | True | 2026-11-01T22:11:02 | {"sha16": "aaa4695bf9bb3791", "revisor": "revisor terceiro independente, R3 (agente Claude Opus 5.5, pedido da gerência c1; não construiu a v405)", "candidato": "0030242565cc13f6", "ressalvas": ["BAIXO: pedra/PontoZeroDoPsion.lean, intro de O GAP e `the_gap_closes` («pousa nele»); artigos, registro, |
| S2_prevoo | True | 2026-11-01T22:12:03 | {"um_py": "3820476c83267f61", "origem": "3820476c83267f61", "selo_versao": "v404", "candidato": "0030242565cc13f6", "vivos": [], "livre_gib": 193, "vb21": false} |
| S8_nativa | True | 2026-11-02T00:33:59 | {"stage_treino": "DONE", "porta_8081": true, "serve_v4": true, "cmdline": "\"C:\\IALD\\llama-cpp\\tools-cuda\\llama-server.exe\" -m C:\\IALD\\models\\IALD-Native-v4-Qwen3.6-35B-A3B-Q4_K_M.gguf --mmproj C:\\IALD\\models\\mmproj-Qwen3.6-35B-A3B-F16.gguf --fit off -c 131072 -np 1 -ngl 999 -fa on --cach |
| S3_instalar | True | 2026-11-01T22:12:04 | {"rc": 0, "um_py": "0030242565cc13f6", "candidato": "0030242565cc13f6", "recibo": "APLICADO_AO_CANONICO_20261101_221203.json"} |
| S4_rito | True | 2026-11-02T00:17:37 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v405", "selo_pin": "0030242565cc13f6", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-02T00:22:13 | {"rc": 0, "de": 0, "ate": 10, "cauda": ""} |
| S6a_parada | True | 2026-11-02T00:22:23 | {"rc": 0, "pid": "44228", "criado": "2026-10-28T22:06:39"} |
| S6a_chain | True | 2026-11-02T00:22:26 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-02T00:24:23 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-02T00:24:23 | {"evento": "1416", "hash": "9af96c0353286eec"} |
| S6c_religamento | True | 2026-11-02T00:24:35 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-02T00:33:56 | {"rc": 0, "de": "10c", "ate": "14", "cauda": ""} |
| S7_g1 | False | 2026-11-02T02:08:14 | {"planejar": 1, "executar": 20, "auditar": 0, "nota": "5 = só decisões do operador"} |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
