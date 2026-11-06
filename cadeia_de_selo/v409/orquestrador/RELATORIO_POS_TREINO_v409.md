# RELATÓRIO PÓS-TREINO v409 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| S0_treino | True | 2026-11-05T23:46:51 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-05T23:46:51 | {"sha16": "2a3149a13e68291c", "resumo": {"candidato_sha16": "53284ba461ecd940", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v409.json", "sha16": "12a71b3cc86924ab", "rc": 0}, "p00": {"ok": true, "passaram": 189, "n": 189, "pendentes": [], "sha16": "69714da377dcfa4a"}, "ensaio_a_seco": {"veredito |
| S1b_revisao | True | 2026-11-05T23:46:51 | {"sha16": "88d1c01c81dc60de", "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R3, a ultima; nao construi a v409; mesma instancia de trabalho da R1 e da R2)", "candidato": "53284ba461ecd940", "ressalvas": ["R3 = ultima rodada (D58). R1 e R2 guardadas em bytes ao lado (REVISAO_TERCEIRO_v |
| S2_prevoo | True | 2026-11-05T23:46:52 | {"um_py": "e7bc6b10e8ff76be", "origem": "e7bc6b10e8ff76be", "selo_versao": "v408", "candidato": "53284ba461ecd940", "vivos": [], "livre_gib": 106, "vb21": false} |
| S3_instalar | True | 2026-11-05T23:46:53 | {"rc": 0, "um_py": "53284ba461ecd940", "candidato": "53284ba461ecd940", "recibo": "APLICADO_AO_CANONICO_20261105_234652.json"} |
| S4_rito | True | 2026-11-06T01:36:23 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v409", "selo_pin": "53284ba461ecd940", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-06T01:41:07 | {"rc": 0, "de": 0, "ate": 10, "cauda": ""} |
| S6a_parada | True | 2026-11-06T01:41:17 | {"rc": 0, "pid": "45344", "criado": "2026-11-05T17:16:56", "subiu_antes_de_parar_D52": false} |
| S6a_chain | True | 2026-11-06T01:41:19 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-06T01:42:57 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-06T01:42:57 | {"evento": "1491", "hash": "0cee635b5a77d5c4"} |
| S6c_religamento | True | 2026-11-06T01:43:10 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-06T01:53:39 | {"rc": 0, "de": "10c", "ate": "14", "cauda": ""} |
| S6d_textos_custodia | True | 2026-11-06T01:53:39 | {"rc": 0, "script": "textos_custodia_handoff_v409.py", "recibo": "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json", "portao_g1_handoff_inteiro": "limpo", "fim_da_cadeia": "HANDOFF (D57)"} |
| S8_nativa | True | 2026-11-06T01:53:40 | {"stage_treino": "DONE", "porta_8081": true, "serve_v4": true, "cmdline": "\"C:\\IALD\\llama-cpp\\tools-cuda\\llama-server.exe\" -m C:\\IALD\\models\\IALD-Native-v4-Qwen3.6-35B-A3B-Q4_K_M.gguf --mmproj C:\\IALD\\models\\mmproj-Qwen3.6-35B-A3B-F16.gguf --fit off -c 131072 -np 1 -ngl 999 -fa on --cach |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
