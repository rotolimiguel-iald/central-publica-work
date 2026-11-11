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
