# RELATÓRIO PÓS-TREINO v408 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| S0_treino | True | 2026-11-05T03:14:08 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-05T03:14:08 | {"sha16": "66bae002d8cbc7d4", "resumo": {"candidato_sha16": "e7bc6b10e8ff76be", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v408.json", "sha16": "1dc9e93142422f6b", "rc": 0}, "p00": {"ok": true, "passaram": 118, "n": 118, "pendentes": [], "sha16": "5e4d86c15bccf6a5"}, "ensaio_a_seco": {"veredito |
| S1b_revisao | True | 2026-11-05T03:14:08 | {"sha16": "02178e96d3758f00", "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R2; nao construi a v408; mesma familia da R1, mesma instancia de trabalho)", "candidato": "e7bc6b10e8ff76be", "ressalvas": ["R2 (ultima rodada). Fora de revisao_terceiro/ so' escrevi a copia temporaria axioma |
| S2_prevoo | True | 2026-11-05T03:14:09 | {"um_py": "833121339e649f71", "origem": "833121339e649f71", "selo_versao": "v407", "candidato": "e7bc6b10e8ff76be", "vivos": [], "livre_gib": 139, "vb21": false} |
| S3_instalar | True | 2026-11-05T03:14:09 | {"rc": 0, "um_py": "e7bc6b10e8ff76be", "candidato": "e7bc6b10e8ff76be", "recibo": "APLICADO_AO_CANONICO_20261105_031409.json"} |
| S4_rito | True | 2026-11-05T05:05:09 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v408", "selo_pin": "e7bc6b10e8ff76be", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-05T05:09:18 | {"rc": 0, "de": 0, "ate": 10, "cauda": ""} |
| S6a_parada | True | 2026-11-05T05:09:27 | {"rc": 0, "pid": "47656", "criado": "2026-11-04T21:20:02", "subiu_antes_de_parar_D52": false} |
| S6a_chain | True | 2026-11-05T05:09:29 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-05T05:11:07 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-05T05:11:07 | {"evento": "1473", "hash": "22fd56397613658d"} |
| S6c_religamento | True | 2026-11-05T05:11:20 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-05T05:19:42 | {"rc": 0, "de": "10c", "ate": "14", "cauda": ""} |
| S6d_textos_custodia | False | 2026-11-05T05:19:42 | {"rc": 1, "script": "textos_custodia_handoff_v408.py", "recibo": null} |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
