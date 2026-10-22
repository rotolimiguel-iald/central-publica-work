# Revisao transporte/pacote — mudancas necessarias

## P1 F1 — Cliente herdado ainda permite retries do SDK

C:\IALD\Central de Patentes\work\iald_tudo_20260921\claude_guarded_transport.py:27

Contradiz contrato no-retry do transporte; erros retryable podem reenviar geracao automaticamente apesar de messages.stream ser chamado uma vez no wrapper.

Correcao proposta: Criar cliente derivado com max_retries=0 explicitamente, preservando timeout, inclusive cliente injetado; nao alterar cliente compartilhado. Testar opcoes reais,nao apenas call_count do mock.

Evidencia: `{"adapter_max_retries": 2, "client_constructed_max_retries": 2, "stream_calls_at_python_boundary": 1, "actual_http_calls": 0, "interpretation": "A chamada Python unica nao desabilita retries internos do SDK."}`

## P1 F2 — Falha local apos abertura do stream e classificada sem cobranca

C:\IALD\Central de Patentes\work\iald_tudo_20260921\claude_guarded_transport.py:65

_resposta_de_excecao converte ValueError/RuntimeError local em claude_erro_local; recusa_sem_cobranca aceita esse codigo, embora geracao ja tenha sido iniciada. Integracao pode liberar reserva de pedido possivelmente cobrado.

Correcao proposta: Distinguir erro apos tentativa de geracao com codigo nao liberavel/estado de cobranca ambiguo e conservar decisao de contexto; testar real recusa_sem_cobranca apos manager.__enter__.

Evidencia: `{"entered_stream": 1, "closed_stream": 1, "response_status": 500, "error_code": "claude_erro_local", "adapter_says_certainly_no_charge": true, "decision": null}`

## P2 F3 — Reserva planejada pode ser validada com margem e saida menores

C:\IALD\Central de Patentes\work\iald_tudo_20260921\claude_memory_package.py:39

Manifesto aritmeticamente consistente com margem0/saida1 e aceito como >=10k dinamico,mas transporte usa margem1024 e pode pedir4096,restando5880. Hash do prefixo e igualdade de budget nao garantem perfil de reserva exigido.

Correcao proposta: Validar perfil reservado explicitamente (saida4096,margem1024,ou politica de minimo equivalente) antes de testar >=10000; nao usar so os valores declarados no proprio manifesto.

Evidencia: `{"loader_accepted": true, "declared_output": 1, "declared_margin": 0, "reported_dynamic_tokens": 10999, "dynamic_at_output4096_margin1024": 5880, "permanent_tokens": 188000}`

## P2 F4 — Selecao divergente no payload vira erro interno em vez de recusa de autorizacao

C:\IALD\Central de Patentes\work\iald_tudo_20260921\claude_guarded_transport.py:69

profile_call levanta PermissionError para payload model diferente; excecao cai no handler generico,produz HTTP500 claude_erro_local. Nao ha bypass nem envio,mas o cliente recebe falha de servidor em vez de403.

Correcao proposta: Tratar PermissionError de preflight como403 claude_model_forbidden e preferir validar divergencia antes de construir cliente.

Evidencia: `{"status": 500, "code": "claude_erro_local", "count_calls": 0, "generation_calls": 0, "bypass": false}`

13 testes fornecidos passaram,mas nao cobriam essas fronteiras. Testes adicionais offline exercitaram configuracao real do adaptador,recusa_sem_cobranca,manifesto com reserva reduzida,mismatch de modelo e SSE real sucesso/falha parcial. Sem API/credenciais/producao. tools_sha256 nao e comparado com ferramentas por estes modulos; autenticacao/consentimento/reserva sao obrigacoes do chamador,nao auditadas aqui.
