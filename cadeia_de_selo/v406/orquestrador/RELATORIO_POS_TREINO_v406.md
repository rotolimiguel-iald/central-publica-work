# RELATÓRIO PÓS-TREINO v406 — orquestrador da gerência c1

Ordem do operador: `OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt`

| passo | ok | quando | dados |
|---|---|---|---|
| S0_treino | True | 2026-11-02T23:27:15 | {"stage": "DONE", "etapa": "treino_concluido", "lancar": null, "finished": "2026-11-01T22:03:31"} |
| S1_prep | True | 2026-11-02T23:27:15 | {"sha16": "0a82f8b5a8da34ac", "resumo": {"candidato_sha16": "ddcb91930982d614", "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v406.json", "sha16": "4c7bf05a84ac3f53", "rc": 0}, "p00": {"ok": true, "passaram": 109, "n": 109, "pendentes": [], "sha16": "7688ab24d8e53d28"}, "ensaio_a_seco": {"veredito |
| S1b_revisao | True | 2026-11-02T23:27:15 | {"sha16": "9a2e296f7ee6cdba", "revisor": "revisor terceiro independente (agente Claude Sonnet, pedido da gerencia c1; nao construiu a v406)", "candidato": "ddcb91930982d614", "ressalvas": ["R3 enxuta: reli so' o que a coordenacao disse que mudou e reexecutei os meus scripts da R2 sobre o candidato n |
| S2_prevoo | True | 2026-11-02T23:27:16 | {"um_py": "0030242565cc13f6", "origem": "0030242565cc13f6", "selo_versao": "v405", "candidato": "ddcb91930982d614", "vivos": [], "livre_gib": 159, "vb21": false} |
| S3_instalar | True | 2026-11-02T23:27:17 | {"rc": 0, "um_py": "ddcb91930982d614", "candidato": "ddcb91930982d614", "recibo": "APLICADO_AO_CANONICO_20261102_232717.json"} |
| S4_rito | True | 2026-11-03T01:41:11 | {"rc_lancador": 0, "trailer": "RITO_RC=0", "selo_versao": "v406", "selo_pin": "ddcb91930982d614", "marcador_servidor": false} |
| S5_cadeia_0_10 | True | 2026-11-03T01:50:55 | {"rc": 0, "de": 0, "ate": 10, "cauda": "", "decisao_da_gerencia": "passos 0-9 passaram em 01:41-01:43 (chain_S5_cadeia_0_10_out.txt); o passo 10 falhou so' em T17_LEAN_KERNEL porque a tarefa ONCE IALD_build_k406c redisparou as 23:58 e reescreveu kernel/lake_build.log; log original restaurado do .bak |
| S8_nativa | True | 2026-11-03T01:45:27 | {"stage_treino": "DONE", "porta_8081": true, "serve_v4": true, "cmdline": "\"C:\\IALD\\llama-cpp\\tools-cuda\\llama-server.exe\" -m C:\\IALD\\models\\IALD-Native-v4-Qwen3.6-35B-A3B-Q4_K_M.gguf --mmproj C:\\IALD\\models\\mmproj-Qwen3.6-35B-A3B-F16.gguf --fit off -c 131072 -np 1 -ngl 999 -fa on --cach |
| S6a_parada | True | 2026-11-03T01:51:05 | {"rc": 0, "pid": "83760", "criado": "2026-11-02T20:59:18"} |
| S6a_chain | True | 2026-11-03T01:51:08 | {"rc": 0, "de": "10a", "ate": "10a", "cauda": ""} |
| S6b_chain | True | 2026-11-03T01:52:49 | {"rc": 0, "de": "10b", "ate": "10b", "cauda": ""} |
| S6b_aplicar | True | 2026-11-03T01:52:49 | {"evento": "1443", "hash": "06ea87583f3500a7"} |
| S6c_religamento | True | 2026-11-03T01:53:02 | {"rc": 0, "porta": true} |
| S6c_chain_10c_14 | True | 2026-11-03T02:03:39 | {"rc": 0, "de": "10c", "ate": "14", "cauda": "", "decisao_da_gerencia": "a primeira rodada parou no import de delta_v406.py (_bancada_pina_hoje exigia a base v405; a Bancada ja pinava B15-v406 depois do 10b): defeito do delta, corrigido com errata ao lado (aceita base ou esta versao; BANCADA_JA_APLI |
| S7_g1 | True | 2026-11-03T06:15:55 | {"planejar": 1, "executar": 20, "auditar": 0, "nota": "5 = só decisões do operador", "decisao_da_gerencia": "custodia v406 PUBLICADA (espelho a381c4d1 = origin/main; Central 42f3b0c9 = origin/main; site v406 no ar: subidas verificadas 20261103_025919 e 20261103_055922, esta com os 83 arquivos da Cen |

Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.
