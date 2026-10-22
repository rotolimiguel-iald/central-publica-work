from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
from hashlib import sha256

WORK = Path(__file__).parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD')
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S')
ios = json.loads((WORK / 'ios14_compile/verification.json').read_bytes())
assert ios['conclusion'] == 'success'
policy = (WORK / 'privacy_public_current.html').read_bytes().decode('utf-8')
assert 'Nenhum dado é compartilhado com terceiros' in policy
assert 'openai' not in policy.lower()
draft = (WORK / 'privacy_draft.html').read_bytes()
assert b'OpenAI' in draft and b'Minuta' in draft
entry = f'''

### {now.strftime('%d/%m/%Y %H:%M %z')} — Build 14 compilada no iOS; política publicada requer atualização

[REAL] A compilação iOS da build 14 concluiu com sucesso no workflow existente `Validate iOS archive`, run {ios['databaseId']}, commit `{ios['headSha']}`. O log contém `ARCHIVE SUCCEEDED`; SHA-256 lido do log: `{ios['log_sha256']}`. Escopo: **archive sem assinatura**, não é IPA instalável nem confirmação de distribuição TestFlight. Recibos: `work/iald_openai_motor_20260914/ios14_compile/run.json`, `verification.json` e `build-ios.log`. Run: {ios['url']}.

[REAL] A sessão Apple continua na tela de login (`authResult=FAILED`), com botão de entrada pelo iPhone. Autenticação solicitada ao operador e aba mantida aberta. As tentativas pelo controle do navegador retornaram “Click target is no longer available”, inclusive com o botão visível; não foi ultrapassada a autenticação. Essa etapa continua dependente do operador. APK/AAB build 14 e motor OpenAI previamente testados permanecem prontos. Motor padrão não foi alterado.

[REAL — incompatibilidade concreta] GET `https://iald.ia.br/privacidade.html` respondeu HTTP 200 e ainda publica a versão de março, sem menção à OpenAI, com a frase “Nenhum dado é compartilhado com terceiros”. A cópia recebida tem SHA-256 `{sha256((WORK / 'privacy_public_current.html').read_bytes()).hexdigest()}`. O arquivo local em `C:/IALD/Site/IALD/privacidade.html` tem as mesmas alegações antigas; diferença de bytes na publicação inclui transformação de e-mail pela Cloudflare. O túnel local inspecionado serve `demo.iald.ia.br` e `central.iald.ia.br`; não serve o domínio raiz. Repositório público `IALD_site` existe, mas não contém esta página nem tem GitHub Pages configurado. Não publicar por suposição nesse repositório.

[REAL — minuta preparada] `work/iald_openai_motor_20260914/privacy_draft.html` descreve autenticação, dados de perfil/conversa/anexos, compartilhamento OpenAI condicionado a consentimento, revogação, pesquisa na internet, infraestrutura Cloudflare, registros de uso/denúncias e exclusão. Documentação oficial OpenAI e Apple consultada. A política atual e o site não foram modificados. A minuta contém marcação visível de NÃO PUBLICADA e ponto pendente sobre retenção: não foi demonstrada expiração automática uniforme dos registros/backups. Não prometer eliminação automática nem retenção zero sem implementação/evidência.

[OPEN] Operador consultado sobre o painel em que publica `iald.ia.br` (Cloudflare Pages, Hostinger ou outro); resposta pendente. Finalizar prazos/procedimento de retenção, publicar a política pelo destino verdadeiro e conferir o conteúdo público antes da ativação geral. Concluir login Apple, conferir Xcode Cloud/TestFlight e informações de privacidade do app. Sem essas evidências, o objetivo permanece incompleto. Nenhuma chave nova, alteração de permissão, treinamento de pesos ou mudança de gate nesta etapa.
'''
paths = [Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
         Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),
         SOURCE / 'CLAUDE.md', SOURCE / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
         WORK / 'HANDOFF_RUNTIME.md',
         Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
         Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
for path in paths:
    old = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    addition = entry
    if path.name == 'MEMORY.md':
        addition = (f'\n\n[{now.strftime("%d/%m/%Y %H:%M %z")} — REAL] Build 14 também compilou no iOS '
            '(run 34895174291, archive sem assinatura; TestFlight pendente de login Apple). '
            'Política pública ainda nega compartilhamento externo; minuta OpenAI pronta, publicação depende '
            'de identificar painel do site e concluir retenção. Recibos e estado em '
            '`C:/IALD/Central de Patentes/work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md`.\n')
    data = old + addition.encode('utf-8')
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(name)
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data and len(data) > len(old)
    if path.read_bytes() != old:
        raise RuntimeError('Concurrent edit; append refused: ' + str(path))
    os.replace(temporary, path)
    assert path.read_bytes() == data
print('IOS_SUCCESS_AND_PRIVACY_BLOCKERS_RECORDED_WITH_BYTE_BACKUPS')
