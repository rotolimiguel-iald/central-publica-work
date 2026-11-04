# RELATÓRIO PÓS-TREINO v407 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| S0_treino | True | 2026-11-03T18:48:53 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-03T18:48:53 | {"sha16": "a578de681f765907", "resumo": {"candidato_sha16": "833121339e649f71", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v407.json", "sha16": "210ad396fc6494cf", "rc": 0}, "p00": {"ok": true, "passaram": 115, "n": 115, "pendentes": [], "sha16": "2a3ea14ca5e4375c"}, "ensaio_a_seco": {"veredito |
| S1b_revisao | True | 2026-11-03T18:48:53 | {"sha16": "bdc0d5d80aea3b88", "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R5; nao construi a v407; mesma familia da R1 a R4 e da revisao de 02/11, outra instancia)", "candidato": "833121339e649f71", "ressalvas": ["R5 confinada a orquestrador/pos_treino_v407.py. Nao repeti nada do q |
| S2_prevoo | True | 2026-11-03T18:48:55 | {"um_py": "ddcb91930982d614", "origem": "ddcb91930982d614", "selo_versao": "v406", "candidato": "833121339e649f71", "vivos": [], "livre_gib": 144, "vb21": false} |
| S3_instalar | True | 2026-11-03T18:48:57 | {"rc": 0, "um_py": "833121339e649f71", "candidato": "833121339e649f71", "recibo": "APLICADO_AO_CANONICO_20261103_184857.json"} |
| S4_rito | True | 2026-11-04T07:29:21 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v407", "selo_pin": "833121339e649f71", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-04T07:33:38 | {"rc": 0, "de": 0, "ate": 10, "cauda": ""} |
| S6a_parada | True | 2026-11-04T07:33:47 | {"rc": 0, "pid": "49928", "criado": "2026-11-04T07:32:44"} |
| S6a_chain | True | 2026-11-04T07:33:50 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-04T07:35:25 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-04T07:35:25 | {"evento": "1459", "hash": "a99519456bfc1966"} |
| S6c_religamento | True | 2026-11-04T07:35:34 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-04T07:46:49 | {"rc": 0, "de": "10c", "ate": "14", "cauda": ""} |
| S7_g1 | False | 2026-11-04T07:53:47 | {"planejar": 1, "executar": 20, "auditar": 0, "nota": "5 = só decisões do operador"} |
| S8_nativa | True | 2026-11-04T07:46:53 | {"stage_treino": "DONE", "porta_8081": true, "serve_v4": true, "cmdline": "\"C:\\IALD\\llama-cpp\\tools-cuda\\llama-server.exe\" -m C:\\IALD\\models\\IALD-Native-v4-Qwen3.6-35B-A3B-Q4_K_M.gguf --mmproj C:\\IALD\\models\\mmproj-Qwen3.6-35B-A3B-F16.gguf --fit off -c 131072 -np 1 -ngl 999 -fa on --cach |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
