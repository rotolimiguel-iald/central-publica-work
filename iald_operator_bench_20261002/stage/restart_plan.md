# Handoff de integração e reinício — somente plano

[REAL] Integração offline final: 9/9 testes com módulos reais + 16/16 regressões AST, fontes estáveis durante as verificações. Recibo autoritativo: `actual_integration_validation_final.json`. O recibo anterior conserva uma falha de ambiente: o sandbox não via Flask. A rodada final usou as dependências existentes do host em `C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages`, caminho explícito no teste, sem instalar pacotes. Nenhum monólito web foi importado, provedor chamado ou cálculo de bancada executado. Planos sintéticos e artefatos dos testes ficaram em diretórios temporários.

`/api/task-capabilities` conserva as capacidades anteriores e acrescenta `classe_usuario` (`operador`/`usuario`) e `operator_bench` (`available`, `tools`). Reler o registro a cada requisição; usar `is_operator`; contas bloqueadas continuam 403. Resposta privada sem cache. A disponibilidade indica elegibilidade para as ferramentas, não saúde dos serviços nem execução observada. Esta foi a única função web modificada nesta etapa; o teste cobre revogação, outras contas e ausência de sondagem/criação de scope.

## Estado observado e método proposto

[REAL] Em 02/10/2026 às 07:56:29 (UTC−03), `restart_activity_host.json` registrou 0 jobs queued/running, 0 reservas Claude/OpenAI e nenhuma avaliação em estado started. O banco public_spend não existia: ausência não foi convertida em uma contagem medida. A observação anterior do sandbox sobre ausência de jobs está corrigida pelo recibo do host; usar este último.

- Web: `127.0.0.1:8082`, PID **130928**, Python `C:/Python314/python.exe`, pai **41020**.
- Supervisor: PowerShell **41020**, script `C:/IALD/projetos_pyhton/IALD/start_iald_web.ps1`. Tarefa existente **IALD Web Server** observada Running; não registrar outra tarefa. Reinício do filho após 5 segundos conforme launcher.
- Bancada GW: porta **18765**, PID **16040**, pythonw. Cosmologia: porta **18766**, PID **65116**, pythonw. Preservar ambos, seus pais, RAM e identidades de carregamento.

[PROPOSTO — NÃO EXECUTADO]

1. Main conclui revisão independente e confere os hashes congelados. Seu `deploy.py` já confere baseline, quiet e snapshots. Repetir quiet imediatamente antes da parada; estas contagens são instantâneas e não constituem bloqueio de novas requisições. Evitar novos pedidos durante a janela. Leases de roteamento e streams diretos não equivalem aos jobs persistentes.
2. Após instalação autorizada, validar novamente PID, data de criação, executável, script web, pai 41020 e listener 8082. Encerrar somente esse filho web, atualmente **130928**, deixando o supervisor existente gerar o novo processo. Não executar `stop_iald_web.ps1`: ele encerra supervisores e outros Python por correspondência ampla de nome. Não usar árvore de processos nem reiniciar as portas 18765/18766, llama ou túnel.
3. Conferir novo PID web com o mesmo supervisor, listener 8082 e inicialização pelos logs em `R/logs/web-supervisor.log` e `R/logs/web-server_*.log(.err)`. A rota `/health` sozinha não comprova o web, pois consulta o llama. Conferir metadata autenticada de capabilities sem solicitar inferência. Comparar os snapshots da bancada que o deploy já prepara; PIDs/load_id/generation/arrays devem ser preservados.
4. Se não houver respawn, diagnosticar o supervisor/tarefa existente, sem iniciar segundo supervisor sobre a porta ocupada. Queued/running encontrados no início do ChatJobs tornam-se interrupted, sem reenvio. Uma execução persistente da bancada interrompida requer reconciliação do ledger; nunca repetir automaticamente um envio incerto.

Nenhum processo foi parado, conta alterada ou arquivo de produção escrito por esta integração. Não foi realizado teste científico de ponta a ponta. Arquivos de código e testes desta entrega congelados após o recibo final; qualquer nova alteração exige nova conferência de hash/testes.

## Sete superfícies de memória da entrega anterior

Fonte: `C:/IALD/Central de Patentes/work/iald_memory_refresh_20261001/memory_updates.json`. As sete superfícies e os sete backups registrados foram encontrados. Hashes desse recibo são históricos, não pins atuais. Nenhuma memória foi alterada nesta tarefa. Antes de futura atualização, criar novo backup imediato de bytes na mesma pasta e usar escrita atômica.

- `C:/IALD/projetos_pyhton/IALD/CLAUDE.md`
- `C:/IALD/Central de Patentes/work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md`
- `C:/IALD/projetos_pyhton/IALD/iald-app/HANDOFF_MOTOR_OPENAI_20260914.md`
- `C:/IALD/Central de Patentes/memory/TGL_ATLAS.md`
- `C:/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md`
- `C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/MEMORY_2.md`
- `C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/app-iald-mobile.md`

SHA-256 final do web em staging, lido do artefato: `21150d59c56963b1f5c75166fa4b50bdb32995c672197a346140ef3b336cbb68`.
