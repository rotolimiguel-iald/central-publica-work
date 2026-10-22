from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess

root=Path(r'C:\IALD\projetos_pyhton\IALD')
app=root/'iald-app'
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=app,text=True).strip()
artifacts=[]
for relative in ('android/app/build/outputs/bundle/release/app-release.aab','android/app/build/outputs/apk/release/app-release.apk'):
    p=app/relative
    artifacts.append(f'- `{p}`: {p.stat().st_size:,} bytes; SHA-256 `{hashlib.sha256(p.read_bytes()).hexdigest()}`.')

text=f'''# Continuação do app IALD — 13/09/2026

[REAL] Implementação e compilações verificadas nesta sessão. **Nenhum envio à Apple ou Google Play ocorreu ainda. Nenhum aparelho foi instalado nesta sessão.**

## Estado entregue

- Repositório PRIVADO: https://github.com/rotolimiguel-iald/iald-app
- Branch `codex/mobile-release`; commit lido do Git: `{commit}`.
- 108 arquivos auditados; servidor, .env, bancos de usuários, credenciais, keystore, entregas antigas e handoffs excluídos. Criação e push foram especificamente autorizados pelo operador após revisão automática.
- Android: versão 4.1, build 11, pacote `br.ia.IALD`, SDK alvo 36; `bundleRelease` e `assembleRelease` concluídos, APK verificado por apksigner (v2), AAB verificado por jarsigner. Os JS embarcados foram comparados byte a byte com `www/iald.js`.
- iOS: compilação de arquivo **SEM ASSINATURA** concluída no Xcode 26.6 via GitHub Actions: https://github.com/rotolimiguel-iald/iald-app/actions/runs/34784329531 . Log termina em `ARCHIVE SUCCEEDED`. O workflow preservou o log, não um IPA instalável. Isso não comprova o login Apple num aparelho.
- Esquema compartilhado `App`, projeto `ios/App/App.xcodeproj`, Team `48DLBH89QY`, bundle `br.ia.IALD`, versão 4.1 (11). `ci_post_clone.sh` instala npm e faz cap sync no Xcode Cloud.
- `npm ci` + `cap sync` reproduzidos em instalação limpa. O Capacitor CLI ajusta sozinho a dependência Swift do plugin Apple 7.1.0 para Capacitor 8; não houve patch manual persistente necessário. O aviso de versão não impediu o build iOS.
- Ícones/telas de abertura padrão substituídos pelos recursos originais da IALD. Manifesto de privacidade iOS inclui UserDefaults CA92.1.
- Chave Android criada com autorização específica em `C:\\Users\\rotol\\.iald_keys`; senha aleatória, ACL restrita, backup local do keystore e certificado público. Configuração em `android/keystore.properties` ignorada no Git. NÃO imprimir nem enviar as credenciais. Um backup no mesmo disco não substitui o backup externo do operador.

## Pacotes locais

{chr(10).join(artifacts)}

## Servidor e interface

Alterados com backups: `iald_web_server.py`, `iald_access_engine.py`, `app/iald.js`.

- Bearer tem precedência sobre cookie; identidade do app não vira cookie. Reset de senha ou exclusão de usuário revoga tokens. Sessões web antigas sem versão de autenticação precisam entrar novamente.
- JWT Apple exige assinatura RS256, audience, issuer, sub, iat e exp. O modo inseguro só funciona com `app.testing`.
- Rotas antigas `/api/access-status`, `/api/apple-auth`, `/api/request-access` devolvem HTTP 410.
- Desativado o static handler automático da raiz; os arquivos públicos são uma lista explícita. .env, fontes Python e banco de usuários não são servidos.
- Admin requer peer local, host local e ausência de cabeçalhos de proxy. Escrita de memória por ferramenta usa autorização explícita calculada no pedido, propagada ao worker. Filtragem de ferramentas é aplicada antes de executar chamadas do modelo.
- Sessão de app força superfície app no servidor, impedindo reativação comercial por `iald_surface=web`. Transferência de créditos, contratação e ferramentas de memória do operador removidas da lista do app.
- Recuperação de contas Apple/dispositivo cujos usuários foram removidos no reset anterior corrigida; históricos já resetados não bloqueiam a recuperação seguinte. Nenhum cadastro real foi criado/apagado pelos testes.
- Saída e expiração do app retornam ao portão nativo; não navegam mais para /login ou /logout locais inexistentes. Registro explícito do plugin Apple quando necessário. Removido fallback Math.random para identificador Android.
- Web recarregado via supervisor; modelo mantido (PID do modelo conferido antes/depois). HTTPS público e health local responderam 200; Apple sem token respondeu 400 com CORS `capacitor://localhost`.
- Streaming direto do modelo medido: HTTP 200, 4 chunks com texto, marcador DONE, primeiro texto em 0,57 s. Essa medição não equivale a teste completo no iPhone.
- 12 testes isolados de segurança e recuperação passaram, sem importar o servidor vivo ou tocar nos livros de créditos. Código/logs de trabalho: `C:\\IALD\\Central de Patentes\\work\\iald_mobile_release`.

## Bloqueio atual: login nos portais

O operador foi solicitado a entrar diretamente nas páginas abertas do navegador Codex, sem enviar senhas/códigos no chat. No último estado observado ambas ainda exibiam login:

- Apple: https://appstoreconnect.apple.com/apps/6760655636
- Google: https://play.google.com/console/

Após login, inspecionar configuração real da conta e continuar. NÃO pedir novamente autorização para a chave Android nem para o repositório privado: ambas foram concedidas explicitamente.

## Próximas ações necessárias

1. Apple: verificar Xcode Cloud existente. O onboarding inicial pode precisar de Xcode em um Mac; o handoff anterior simplificava isso. Se Cloud disponível, conectar apenas este repo privado, Archive/App, assinatura automática e TestFlight interno. Alternativa: build assinado no runner, somente após acesso autorizado aos certificados/perfis/API necessários; não enviar chaves sem autorização específica.
2. App Store Connect: conferir versão/build atuais e registros do app antes do envio; selecionar o operador para teste interno e verificar instalação/abertura no iPhone e iPad. Nunca confundir build não assinado com IPA instalável.
3. Google: conferir se a conta já tem app/pacote, chave de upload e verificações. Se já houver chave registrada, adaptar sem substituir cegamente. Para app novo, usar AAB acima em teste interno e Play App Signing; chave de upload perdida é redefinível, ao contrário da afirmação antiga do handoff.
4. Antes de revisão pública: verificar e concluir exclusão de conta/dados e revogação Apple (ainda não implementadas), política de privacidade e formulários das lojas, denúncia de conteúdo de IA, testes reais de login/streaming/anexos/exportação, respostas da revisão alinhadas ao comportamento. A carta antiga NÃO foi enviada e ainda contém condições pendentes.
5. A política em `https://iald.ia.br/privacidade.html` não pôde ser recuperada pela busca nesta sessão; conferir diretamente, sem declarar conteúdo validado. Não prometer aprovação pela Apple/Google.

## Limites honestos

Não foram verificados cadastro Google, requisitos específicos da conta, configuração de Xcode Cloud, certificado/perfil de distribuição Apple, fluxo Apple em aparelho ou instalação. O código de servidor não foi enviado ao GitHub. .env existente não foi impresso nem publicado. Treinamento/modelo não foram iniciados, parados ou reconfigurados.
'''

def atomic(path,data,append=False):
    old=path.read_bytes() if path.exists() else b''
    if old:
        backup=path.with_name(path.name+'.bak_'+stamp)
        backup.write_bytes(old)
        assert backup.read_bytes()==old
    new=old+data if append else data
    tmp=path.with_name(path.name+'.tmp_release')
    tmp.write_bytes(new)
    assert tmp.stat().st_size==len(new)>0
    tmp.replace(path)
    assert path.read_bytes()==new

path=app/'HANDOFF_CODEX_PROSSIGA_20260913.md'
atomic(path,text.encode('utf-8'))
note=('\n\n## Adendo 13/09/2026 — compilação/distribuição pelo Codex\n\n'
      '[REAL] Android 4.1 (11) assinado e verificado; iOS compilado SEM ASSINATURA no Xcode 26.6, '
      'run 34784329531 concluído com sucesso. Repositório privado iald-app criado com autorização expressa. '
      'Servidor corrigido/recarregado, modelo preservado; 12 testes isolados passaram. '
      '**Apple/Google ainda não receberam os pacotes e nenhum aparelho foi instalado nesta sessão.** '
      'Acesso aos portais aguarda login do operador. Próximas ações, evidências, hashes e limites em '
      '`iald-app/HANDOFF_CODEX_PROSSIGA_20260913.md` (na pasta do app, o arquivo está ao lado deste handoff).\n')
atomic(app/'HANDOFF_CODEX.md',note.encode('utf-8'),append=True)
atomic(root/'CLAUDE.md',note.encode('utf-8'),append=True)
print(path)
