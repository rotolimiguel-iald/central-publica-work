# Contrato de integração

`iald_chat_push.register(app, directory, *, authenticate, csrf_check, ios_environment='production', cipher=None, apns=None, fcm=None, transport=None)` registra rotas e devolve `store()`, inicializado apenas no primeiro acesso autorizado. Não existe `register_routes`. `PushStore(directory, cipher=None, apns=None, fcm=None, transport=None)` é a alternativa sem Flask. O pai injeta `notify=lambda owner, job_id: store().notify(owner, job_id)` na construção de `ChatJobs`.

`authenticate()` devolve `(username_autenticado, session_id_estável)` ou `None`. Proposta do pai: exigir `g.app_bearer is True`; obter username da autenticação existente; usar o identificador canônico de sessão validado pelo runtime, incluindo expiração e revogação. [INPUT — atualização do pai] A implementação final usa sid canônico de bearer assinado; a proposta anterior de hash do header foi substituída. O módulo só persiste hashes próprios de owner/session. Não enviar o header para logs. `csrf_check()` precisa devolver **True booleano**, exigindo JSON e Origin na allowlist nativa existente; ausências/valores inesperados falham. Não expor estes endpoints ao cliente web comum. O middleware do pai continua responsável por validar validade/revogação do bearer, CORS, HTTPS, timeout de leitura e limites globais de requisição. Retornar `None` na ausência de autenticação; exceções arbitrárias são mascaradas como 503.

| Método / caminho | JSON | Resultado |
|---|---|---|
| POST `/api/native-push/bindings` | `installation_id` UUID persistente aleatório, `platform` ios/android, `consent: true` | `id`, plataforma, ambiente do servidor, registered/revoked |
| PUT `/api/native-push/bindings/<id>/token` | `provider` apns/fcm e `token` | registered |
| DELETE `/api/native-push/bindings/<id>` | `{}` | revoked |
| POST `/api/native-push/revoke-session` | `{}` | `{revoked: true}` para a sessão autenticada; idempotente |

O corpo não aceita owner/username/ambiente/URL. Cada vínculo exige o mesmo owner **e sessão**. DELETE cria uma revogação permanente do vínculo: uma gravação de token já em trânsito não pode reativá-lo. Na troca de conta, o token passa ao vínculo mais recente e revoga o anterior. `revoke_session(owner, session_id)` deve ser chamado pelo pai antes de logout, revogação/expiração de sessão e exclusão do token de autenticação. `purge(owner)` remove dados na exclusão da conta. Não usar `stop()` ao apenas minimizar o app: isso cancelaria o vínculo desejado; usar em logout, desativação explícita ou troca de usuário. Aguardar `stop()` antes de iniciar outro controlador. Se falhar a revogação offline, o servidor precisa concluir a revogação no fluxo autenticado; um push genérico já enviado não pode ser recolhido.

Integração pronta em `../client`: o builder incorpora `client/registration.mjs`, `notification_settings.js` e `native_notifications_integration.js` em um único asset `app/iald.js`. O host usa o seguinte contrato interno:

```javascript
const notifications = await connectNotifications({
  requestJSON: existingAuthenticatedJSONAdapter,
  installationId: persistentRandomUUID,
  consent: true,                 // gesto do usuário ou preferência explícita restaurada
  nativeReady: rolloutReady,     // false enquanto configuração/build estiver pendente
  prompt: true,                  // true SOMENTE no gesto de ativação; false na restauração
  onJobs: refreshAuthenticatedJobs,
  openJob: ({ jobId, conversationId, signal }) => openExistingConversation(conversationId, { jobId, signal }),
  onStatus: showSafeNotificationState,
});
```

`requestJSON(path,{method,body,signal})` deve serializar JSON, usar a origem HTTPS fixa do app, incluir autenticação/Origin/CSRF existentes, rejeitar HTTP não 2xx, aplicar timeout e respeitar AbortSignal. Nenhum segredo no localStorage; somente UUID aleatório de instalação e preferência por usuário. Ao restaurar sessão, preservar o mesmo session_id para recuperar o binding e o toque de inicialização; na troca de sessão/conta usar outro controlador. Não abrir navegador/URL recebida no push.

O módulo faz GET `/api/chat-jobs/<job_id>` autenticado, exige `status=completed` e usa **conversation_id desse GET** para navegar. Ignora username, conversa e URL do payload. GET `/api/chat-jobs` reconcilia ao abrir/retomar, mesmo sem permissão de push. APIs injetadas recebem sinal de cancelamento e o host deve conferi-lo antes de mudar de conversa. Payload só leva IDs opacos/versionamento e alerta genérico; não leva texto da resposta/pergunta ou identidade do usuário.

`notify` deve ser chamado exclusivamente para resposta elegível, concluída e já persistida. O ChatJobs auditado chama após conclusão sem aviso de falha. Recibo de dispatch é confirmado em SQLite antes da requisição. Diagnóstico contém somente estado, HTTP status e horários; não contém chave, bearer, token de aparelho, URL, request/body/header ou exceção do provedor. `receipts(owner,job_id)` é introspecção interna, sem rota criada. Estados: accepted (aceitação HTTP, não entrega), rejected (HTTP recusado), invalid_token, blocked_configuration, uncertain. Timeout/crash não provoca reenvio automático. Eventos são limitados a uma tentativa por vínculo/job; configuração ausente também exige tratamento explícito do operador, sem replay implícito depois de habilitá-la.

**Limites concretos:** o callback separado não é uma outbox transacional com a tabela de jobs. Há uma janela de crash entre persistir a conclusão e chamar notify; ela pode perder o aviso. Falha de push não elimina a resposta salva. O pai precisa dessa distinção no produto; garantia de entrega/exatamente uma vez não é oferecida. O módulo não executa nem reinicia geração, não chama provedor de IA, não mantém WebView em background e não agenda notificação local para fingir conclusão. APNs/FCM e o sistema operacional podem atrasar ou suprimir alertas; retomada deve sempre recuperar jobs.

A guarda Android nativa `IaldPushReadiness.getStatus()` exige build habilitado e Firebase inicializado antes de permitir `register()` do plugin. Um build padrão deixa push desligado (`-PialdPushEnabled=true` é habilitação explícita após configuração). `nativeReady` continua false por padrão em ambas as plataformas. O plugin está em patch de dependência separado: não instalar/aplicar enquanto a etapa nativa não estiver autorizada. O canal Android nasce no MainActivity, sem executar geração nem pedir permissão. Capabilities/entitlements iOS não são ativados por código JavaScript.

A integração consulta GET `/api/native-push/status`, fornecido pelo runtime do pai. Exige flag da plataforma exatamente true. O logout aguarda a revogação da sessão com o bearer capturado antes de apagá-lo; erro mantém a sessão local para nova tentativa explícita. O token nunca é substituído pelo de outro usuário durante a revogação. O endpoint idempotente cobre também vínculos de uma execução anterior do app, sem depender de um controlador ativo.
