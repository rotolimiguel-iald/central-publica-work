# Lições v409 — staging R2, sem implantação

[REAL — engenharia local] Somente a poda de 174 literais sem referência foi integrada, após PRUNING_R1 PASS_STAGING_REBUILD_ONLY. Shared 890840 → 847129 bytes (43711 economizados). Mesmo contrato @L/@TGL_LITERAL; exposição e conteúdo referenciado preservados. Não integrar os experimentos de limiar nem um algoritmo novo de concatenação.

[REAL] P2 v409/v408 e the_iald_index completos a partir do prompt: 7 residentes; 177 tópicos históricos recuperáveis, 483 tópicos totais. Três tópicos v407 recuperados com igualdade por fetch local. Limites/diz/nao_diz conferidos. Histórico e falha inicial de capacidade preservados.

[REAL] A medição D53_shared_VERIFIED precedeu finalize. Com reserva declarada 148656 e margem 4096, folgas Kimi 8433, MiMo 5061 e DeepSeek 5044 bytes. O envelope Kimi efetivo serializa instructions/conversation uma vez: 887367 bytes, saída 131072, folga 26041. Não confundir com o envelope genérico do verificador. MiMo/DeepSeek usam output_budget dinâmico atual; LIMITS_FINAL_R2 registra seus envelopes e limites. São entradas sintéticas, sem histórico/ACOM real; cada conversa exige admissão própria. Não aumentar tetos para ocultar crescimento.

[REAL] Seis COUNTs públicos, sem geração: Haiku expandido 891783 tokens permanentes / 89262 restantes; shared 435781 / 545264; Sonnet público 471712 / 509333. Valores nativos pertencem aos respectivos modelos e bytes finais; não transferir essa contagem aos outros provedores.

[REAL] Plano com 1788 arquivos de dados, zero substituição Python operacional. Treze pinos do baseline atual preservados. Backups imediatos dos derivados e scripts ficam fora do plano; o filtro exclui .bak. Nenhum serviço reiniciado, nenhum runtime instalado, nenhuma execução de um.py/Lean ou alteração do gate.

[REAL] O commit pinado é ancestral do HEAD público atual; validar ancestralidade e bytes do commit, sem exigir igualdade indevida entre commit histórico e HEAD. Dez URLs raw e 36 artefatos da custódia conferidos. Uma cópia antiga de um.py veio no molde e foi preservada em app/stale_pipeline_backup antes de usar a v409. A lista historical_machine_labels de preparation.json tem ordem variável entre processos; recibo anterior preservado e bytes finais exatos conferidos.

[OPEN] App aguarda revisão distinta/aceite. Implantação e restart dependem do gate humano da v409 e são do pai. Não declarar v409 carregada a partir deste staging.

Bytes dos blocos por versão (dicionário/exposição contabilizados separadamente no pacote total):

```json
{
  "unversioned": 290759,
  "v11": 138,
  "v12": 147,
  "v2": 2772,
  "v3": 886,
  "v361": 295,
  "v363": 105,
  "v364": 870,
  "v365": 917,
  "v366": 330,
  "v367": 339,
  "v368": 707,
  "v369": 576,
  "v370": 385,
  "v371": 1268,
  "v372": 1078,
  "v373": 1091,
  "v374": 834,
  "v375": 839,
  "v376": 3516,
  "v377": 2148,
  "v378": 1814,
  "v379": 761,
  "v380": 1353,
  "v381": 1062,
  "v383": 1462,
  "v384": 578,
  "v385": 1066,
  "v386": 2667,
  "v387": 2139,
  "v388": 1363,
  "v389": 558,
  "v390": 795,
  "v391": 864,
  "v392": 16546,
  "v393": 2196,
  "v394": 2527,
  "v395": 2414,
  "v396": 2715,
  "v397": 2615,
  "v398": 5175,
  "v399": 2134,
  "v401": 16607,
  "v402": 24638,
  "v403": 7944,
  "v404": 6093,
  "v405": 20841,
  "v406": 3065,
  "v407": 2802,
  "v408": 79449,
  "v409": 83962,
  "v41": 140,
  "v5": 152,
  "v6": 152,
  "v7": 157,
  "v8": 157,
  "v9": 157
}
```


## Adendo de implantação — 2026-11-06T11:27:37.638079+00:00

[REAL — recibos locais] Este adendo complementa o retrato de staging acima, preservado como história. Autorização humana da v409 recebida pelo pai; deployment.json registra 1788 destinos instalados. O status histórico INSTALLED_RESTART_REQUIRED desse recibo é complementado por restart.json: PASS, HTTP 200. A verificação final continua em curso. Não se afirma teste live de conversa, acurácia de respostas ou teste/instalação física em aparelho.

[REAL — regra para a próxima release] P2 mantém a versão corrente e a anterior inteiras no prompt; nesta entrega, v409/v408 e the_iald_index permanecem completos. A regra aprovada remove somente literais sem referência direta ou transitiva de TODOS os JSONs do prefixo, percorrendo o dicionário. Não remove conteúdo referenciado, hipóteses, fórmulas, conceitos ou estatutos; preserva a exposição. Foram removidos 174 órfãos, economizando 43711 bytes; shared final 847129 bytes. Não integrar os experimentos de limiar 24 nem concatenação nova. Kernel, fontes científicas, conceitos e estatutos permanecem os das fontes pinadas; esta engenharia não executa um.py/Lean e não move gate.

[REAL — preservação] Os 13 pinos atuais de runtime/clientes de PRESERVATION_BASELINE.json foram reconferidos nesta escrita. Preservar os patches pós-v408 (inclusive Kimi bytebound, owner notice e stream); jamais reaplicar pacote operacional antigo para atualizar ciência. Não copiar helpers obsoletos v405/v408 para nova execução.

[REGRA — template e retomada] task.py é o inicializador: não executá-lo para consultar missão existente. Fazer project por mission_step.py project, sempre com a própria SESSION_REFERENCE.json. Inscrição já existente nunca recebe init novamente. Pipeline reutilizado exige conferir versão, caminhos, referências e semântica de cada helper antes de executar.

[REAL — medidas, não promessa para conversas] Tetos e reservas não mudaram. As folgas abaixo usam os envelopes sintéticos efetivos de LIMITS_FINAL_R2.json; histórico/ACOM/owner notice exigem admissão própria. DeepSeek reserva saída dinamicamente: a folga de 106 bytes após a saída máxima escolhida NÃO é a capacidade máxima do histórico.

| Executor | Entrada (bytes) | Reserva de saída | Folga após margem |
|---|---:|---:|---:|
| kimi | 887367 | 131072 | 26041 |
| mimo | 890429 | 131072 | 22979 |
| deepseek | 890446 | 153928 | 106 |

Com reserva adicional declarada de 148656 e margem 4096, medida antes de finalize: {"deepseek": {"input_bound": 890780, "slack": 5044}, "kimi": {"input_bound": 887391, "slack": 8433}, "mimo": {"input_bound": 890763, "slack": 5061}}.

[REAL — COUNT público] 6 contagens nativas, 0 gerações. Cada contagem pertence ao respectivo modelo/pacote e hash final; não transferir tokens entre provedores.

| Pacote | Tokens permanentes | Tokens restantes |
|---|---:|---:|
| haiku_expanded | 891783 | 89262 |
| shared | 435781 | 545264 |
| sonnet_public | 471712 | 509333 |

Bytes dos blocos por versão, relidos de D53_HISTORY.json (não incluem todo o dicionário/exposição; não somar como pacote completo):

```json
{
  "unversioned": 290759,
  "v11": 138,
  "v12": 147,
  "v2": 2772,
  "v3": 886,
  "v361": 295,
  "v363": 105,
  "v364": 870,
  "v365": 917,
  "v366": 330,
  "v367": 339,
  "v368": 707,
  "v369": 576,
  "v370": 385,
  "v371": 1268,
  "v372": 1078,
  "v373": 1091,
  "v374": 834,
  "v375": 839,
  "v376": 3516,
  "v377": 2148,
  "v378": 1814,
  "v379": 761,
  "v380": 1353,
  "v381": 1062,
  "v383": 1462,
  "v384": 578,
  "v385": 1066,
  "v386": 2667,
  "v387": 2139,
  "v388": 1363,
  "v389": 558,
  "v390": 795,
  "v391": 864,
  "v392": 16546,
  "v393": 2196,
  "v394": 2527,
  "v395": 2414,
  "v396": 2715,
  "v397": 2615,
  "v398": 5175,
  "v399": 2134,
  "v401": 16607,
  "v402": 24638,
  "v403": 7944,
  "v404": 6093,
  "v405": 20841,
  "v406": 3065,
  "v407": 2802,
  "v408": 79449,
  "v409": 83962,
  "v41": 140,
  "v5": 152,
  "v6": 152,
  "v7": 157,
  "v8": 157,
  "v9": 157
}
```

Fontes desta atualização (SHA256 lido dos bytes):

- deployment.json — 3a22c6c195a849569aa842061b2a15c43ecb1db5945d8b22d9cdf5c5868f791e
- restart.json — 056ca6b1da900ec0795f7da22e69f7bb68f5d0bce86240c97ee2358cfd55b4c3
- app\LIMITS_FINAL_R2.json — ac6e9e82a72e4cce15b347cd89a98ee74effcb2ad8fd8e593d4b903d43c48ca3
- app\D53_HISTORY.json — b83a934c7f8fe383c9c0039addff6068dc65824ec8b58922aace7f28a3c74fd1
- app\NATIVE_COUNTS_COMPLETE.json — 0a17c4d986f49cebae4d6de7361839842d7f81f36f707adc79a28666b9333d20
- PRESERVATION_BASELINE.json — 000a20021da73b79f0fcd9811f1738b99062138d64997e4fbc9dcf4e839eefa0
