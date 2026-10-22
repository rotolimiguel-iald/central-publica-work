# Preparação da sucessão da cópia 83

[REAL — leitura estática] `CONFIG_91_NAO_CONFIRMADA.json` reúne oito folhas e `CONFIG_92_NAO_CONFIRMADA.json` reúne nove. Cada arquivo é um snapshot preservado, com `root_confirmed:false`. Os inventários e recibos homônimos registram os hashes e as contagens lidos. Nenhuma aprovação externa foi atribuída.

| Snapshot | Delta | Acumulado | Instâncias locais acumuladas |
|---|---:|---:|---:|
| 91 | 88 teoremas + 20 outras declarações = 108 | 1266 + 348 = 1614 | 12 |
| 92 | 96 teoremas + 22 outras declarações = 118 | 1274 + 350 = 1624 | 12 |

O acumulado é medido nas declarações do `BUILD_PLAN.json` da sucessão 83. O `INTEGRATION_RESULT.json` da mesma cópia registra apenas o delta anterior de seis folhas; não é o inventário cumulativo.

Os três scripts de integração, preparação e execução foram copiados byte a byte de `INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394`. A proveniência e os hashes constam dos recibos de preparação. O programa `um.py` não foi executado nem importado. Nesta etapa tampouco foram executados integrador, preparador sucessor ou compilador Lean.

## Passos reservados à tarefa principal

1. Escolher o snapshot final, ler as fontes e os recibos, conferir os pins e registrar sua confirmação em **novo arquivo**, por exemplo `CONFIG_92_APROVADA.json`, sem alterar a configuração não confirmada. Se houver uma décima folha, gerar um inventário e uma configuração 93 novos antes disso.
2. Executar o integrador com essa nova configuração. Ele cria outra pasta de cópia e não usa o canônico vivo como base.
3. Preparar o plano sucessor com a pasta retornada pelo integrador e os dois artefatos congelados da sucessão 83 indicados abaixo.
4. Executar o plano sucessor. A aprovação das folhas antes da transposição não substitui esta compilação conjunta.
5. Após o PASS conjunto, executar o auditor correspondente ao snapshot efetivamente integrado.

As formas dos comandos são apresentadas a seguir com marcadores explícitos. Não foram executadas:

```powershell
$py = 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$prep = 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415'
$prior = 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394\BUILD_SUCCESSOR_20260909_192313_320129'
& $py -B ($prep + '\integrate_approved_copy.py') '<CONFIGURACAO_NOVA_CONFIRMADA>'
& $py -B ($prep + '\prepare_successor.py') '<PASTA_RETORNADA_PELO_INTEGRADOR>' ($prior + '\BUILD_PLAN.json') ($prior + '\TRANSPOSED_RESULT.json')
& $py -B ($prep + '\run_successor.py') '<BUILD_PLAN_RETORNADO_PELO_PREPARADOR>'
& $py -B '<AUDITOR_CORRESPONDENTE_AO_SNAPSHOT>' '<PASTA_RETORNADA_PELO_INTEGRADOR>' $prep
```

## Auditor preparado para 92

`C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_INTEGRACAO_92_20260909_202159_690738/audit_integration_92.py` foi derivado do auditor 83 congelado. A lista exata de substituições e os hashes de origem/destino estão em `PROVENIENCIA_ADAPTACAO.json` na mesma pasta. O programa foi analisado por AST, sem execução.

O auditor 92 espera a genealogia de deltas 63, 9, 5, 6, 9; 698 arquivos embutidos, dos quais 694 Lean; 1624 declarações explícitas e 5766 entradas em `FullTGLAudit`. A biblioteca anterior tem 83 módulos; a nova rodada terá nove processos de folhas e três agregadores. Esses números são medidos no inventário de entrada e na genealogia auditada.

Foi acrescentada uma exigência: ausência do recibo de preparação ou do resultado conjunto impede PASS. Os limites anteriores continuam declarados, inclusive reaproveitamento de cache e ausência de recompilação integral de todas as dependências externas.

[OPEN — etapa seguinte] As configurações e o auditor preparados não atestam uma integração futura. Também não alteram selo, gate, flags individuais, memórias canônicas ou o estatuto físico da teoria.
