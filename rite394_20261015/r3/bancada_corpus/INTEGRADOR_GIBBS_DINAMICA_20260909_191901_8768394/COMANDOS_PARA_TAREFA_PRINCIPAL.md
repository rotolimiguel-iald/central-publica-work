# Comandos posteriores à confirmação da tarefa principal

[REAL] Preparação estática em pasta nova; os três scripts foram copiados byte a byte. Não houve integração ou compilação nesta preparação. `um.py` foi apenas analisado com AST e `literal_eval`.

[OPEN] A tarefa principal deve ler esta configuração e, se confirmar seus pins e o escopo, gravar uma **nova** `CONFIG_83_APROVADA.json` com `root_confirmed: true` e sua própria fundamentação. A configuração não confirmada permanece intacta.

Acumulado medido pelo `BUILD_PLAN.json` predecessor e declarações das seis fontes: 83 módulos, 1178 teoremas, 328 outras declarações, 1506 auditorias. Há 12 instâncias locais nomeadas nesse total.

Os comandos abaixo são instruções para a tarefa principal e **não foram executados**:

```powershell
$taskPython = 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $taskPython -B 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394\integrate_approved_copy.py' 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394\CONFIG_83_APROVADA.json'
```

O comando de integração imprime a nova pasta `COPIA_INTEGRADA_...`. Usar exatamente esse caminho no argumento seguinte:

```powershell
& $taskPython -B 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394\prepare_successor.py' '<PASTA_NOVA_COPIA_INTEGRADA_RETORNADA>' 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582\BUILD_SUCCESSOR_20260909_174751_385895\BUILD_PLAN.json' 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582\BUILD_SUCCESSOR_20260909_174751_385895\TRANSPOSED_RESULT.json'
```

A preparação sucessora imprime o novo `BUILD_PLAN.json`. Usar exatamente o caminho retornado:

```powershell
& $taskPython -B 'C:\IALD\Central de Patentes\Chatgpt\INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394\run_successor.py' '<BUILD_PLAN_JSON_RETORNADO>'
```

O script de integração exige confirmação e falha com a configuração entregue. A compilação sucessora, quando autorizada pela tarefa principal, preservará 77 módulos por proveniência de cache e compilará seis folhas mais raiz e duas auditorias. Não executa nem importa `um.py`.
