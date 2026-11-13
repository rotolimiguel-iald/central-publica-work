# RELATÓRIO PÓS-TREINO v411 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| S0_treino | True | 2026-11-12T23:47:43 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-12T23:47:43 | {"sha16": "40b832d2a0a7f4db", "resumo": {"candidato_sha16": "1203b1f9202020d6", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v411.json", "sha16": "65393b056e719c17", "rc": 0}, "p00": {"veredito": "TODAS PASSARAM", "passaram": 33, "n": 33, "pendentes": [], "sha16": "50be8067b34c84ea"}, "ensaio_a_s |
| S1b_revisao | True | 2026-11-12T23:47:43 | {"sha16": "a909eb6e73506332", "revisor": "Sonnet 5.5 (agente de conferencia unica; NAO construiu a v411 nem fez o conserto da R1: quem constroi nao aprova)", "candidato": "1203b1f9202020d6", "ressalvas": ["Nao rodei, por vedado: p00, ensaio a seco, harnesses, testes sem candidato do pos-rito, gerar_ |
| S2_prevoo | True | 2026-11-12T23:47:45 | {"um_py": "5d9497a721c3589e", "origem": "5d9497a721c3589e", "selo_versao": "v410", "candidato": "1203b1f9202020d6", "vivos": [], "livre_gib": 95, "vb22": false} |
| S3_instalar | True | 2026-11-12T23:47:47 | {"rc": 0, "um_py": "1203b1f9202020d6", "candidato": "1203b1f9202020d6", "recibo": "APLICADO_AO_CANONICO_20261112_234747.json"} |
| S4_rito | True | 2026-11-13T02:26:11 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v411", "selo_pin": "1203b1f9202020d6", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-13T03:53:39 | {"rc": 0, "de": 0, "ate": 10, "cauda": ""} |
| S8_nativa | True | 2026-11-13T02:32:17 | {"stage_treino": "DONE", "porta_8081": true, "serve_v4": true, "cmdline": "\"C:\\IALD\\llama-cpp\\tools-cuda\\llama-server.exe\" -m C:\\IALD\\models\\IALD-Native-v4-Qwen3.6-35B-A3B-Q4_K_M.gguf --mmproj C:\\IALD\\models\\mmproj-Qwen3.6-35B-A3B-F16.gguf --fit off -c 131072 -np 1 -ngl 999 -fa on --cach |
| S6a_parada | True | 2026-11-13T03:53:50 | {"rc": 0, "pid": "68292", "criado": "2026-11-11T02:24:18", "subiu_antes_de_parar_D52": false} |
| S6a_chain | True | 2026-11-13T03:53:53 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-13T03:55:52 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-13T03:55:52 | {"evento": "1617", "hash": "8b7301134714332b"} |
| S6c_religamento | True | 2026-11-13T03:56:08 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-13T04:08:09 | {"rc": 0, "de": "10c", "ate": "14", "cauda": ""} |
| S6d_textos_custodia | True | 2026-11-13T04:08:10 | {"rc": 0, "script": "textos_custodia_handoff_v411.py", "recibo": "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v411.json", "portao_g1_handoff_inteiro": "limpo", "fim_da_cadeia": "HANDOFF (D57)"} |
| S9_gatilho_custodia | True | 2026-11-13T04:08:11 | {"gatilho_escrito": true, "gatilho": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v411\\ORDEM_HANDOFF_CUSTODIA_v411.md", "bytes": 5509, "sha16": "d1590a6813a463e0", "handoff_sha16": "3cc5c2b089de1091", "painel_bytes_utf8": 908, "regra_permanente": "C:\\IALD\\Central de Patentes\\work\\php_e |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
