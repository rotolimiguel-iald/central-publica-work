# Configuração a cargo do pai

[REAL — implementação em staging] `iald_chat_push.py` não lê ambiente, chaves nem arquivos de configuração. Recebe objetos; a leitura/importação de segredos pertence ao pai. Não há fallback para token em texto claro.

```python
from iald_chat_push import APNs, FCM, register

# secrets é o cofre do pai, com bytes cifrados por DPAPI no usuário do serviço.
apns = APNs(
    key_id=config['apns']['key_id'],
    team_id=config['apns']['team_id'],
    private_key=lambda: secrets.unseal_bytes(config['apns']['key_ref']),
)
fcm = FCM(
    project_id=config['fcm']['project_id'],
    access_token=lambda: oauth_provider.current_token(),
)
push_store = register(
    app, runtime_directory / 'native_push',
    authenticate=authenticated_owner_and_session,
    csrf_check=validate_existing_csrf_or_native_request,
    ios_environment=config['apns']['environment'],
    apns=apns, fcm=fcm,
)
# Na construção lazy de ChatJobs, pelo pai:
# ChatJobs(job_directory, notify=lambda owner, job_id: push_store().notify(owner, job_id))
```

Os nomes `secrets`, `oauth_provider`, `config` e callbacks são adaptadores a fornecer, não módulos já existentes nem imports executados nesta entrega. Usar `apns=None`/`fcm=None` enquanto a respectiva configuração estiver bloqueada. `register` importa Flask somente ao ser chamado e devolve a factory lazy, também em `app.extensions['iald_chat_push']`. Tokens ficam em `native_push.sqlite3`; a cifra padrão é DPAPI no escopo do usuário Windows atual. O processo deve rodar sob o mesmo usuário que importou os segredos, com perfil carregado e ACL restrita no diretório. Não usar DPAPI no escopo da máquina nem fallback aberto.

Proposta de arquivo de configuração restrito, sem segredos em claro:

```json
{
  "schema_version": 1,
  "apns": {
    "enabled": false,
    "key_id": "PREENCHER_NO_IMPORTADOR",
    "team_id": "PREENCHER_NO_IMPORTADOR",
    "topic": "br.ia.IALD",
    "environment": "production",
    "key_ref": "apns-signing-key.dpapi"
  },
  "fcm": {
    "enabled": false,
    "project_id": "iald-app-notificacoes",
    "credential_ref": "fcm-service-account.dpapi"
  }
}
```

O importador do pai valida `key_ref`/`credential_ref` como nomes locais permitidos dentro do cofre fixo, nunca caminhos vindos do cliente, e escreve os blobs atomicamente com ACL do serviço. O JSON de conta de serviço FCM inteiro deve entrar cifrado; `google-services.json` do Android é configuração do cliente e **não** credencial de envio do servidor. Preferir identidade de workload se o ambiente já a oferecer. O callback FCM devolve bearer de curta duração, obtido com escopo `https://www.googleapis.com/auth/firebase.messaging`; renovar antes de expirar e nunca persistir/logar o bearer. O módulo não implementa importador nem contratação/criação de chaves.

APNs assina JWT ES256 via `PyJWT[crypto]`, cache em memória por até 40 minutos; erro de assinatura bloqueia antes do envio. Key ID e Team ID precisam ter 10 caracteres alfanuméricos maiúsculos. O tópico está limitado a `br.ia.IALD`. Debug usa ambiente `development`; TestFlight/App Store usa `production`. Configurar uma implantação/rota de teste separada se precisar admitir ambos; não aceitar ambiente informado livremente pelo navegador. A capability e o perfil assinado precisam concordar com esse ambiente.

[REAL — probe local] O Python `C:\Python314\python.exe` desta sessão não tem HTTPX, h2, PyJWT, cryptography, google-auth ou Flask instalados. Isso não mede o virtualenv do servidor. Dependências de runtime propostas: `httpx[http2]`, `PyJWT[crypto]`, Flask já usado pelo servidor; `google-auth` apenas no adaptador FCM do pai. Nenhum pacote instalado aqui; versões/lock devem ser resolvidos no ambiente de release e auditados pelo responsável. Testes do transporte usam fakes e não validam negociação TLS/HTTP2 real.

[INPUT — coordenação] O pai informou projeto Firebase `iald-app-notificacoes` em preparação, com Gemini/Analytics desligados; credenciais FCM ainda serão configuradas por ele. Ativação APNs no App ID segue aguardando autorização específica após bloqueio da revisão automática por invalidar perfis. Esta entrega não realizou nenhuma dessas ações.
