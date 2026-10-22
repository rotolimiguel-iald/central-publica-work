from datetime import datetime
import json
import os
from pathlib import Path
import tempfile

WORK = Path(__file__).parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD')
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S')
installation = json.loads((WORK / 'installation_20260914_172801.json').read_bytes())
production = json.loads((WORK / 'production_verification_20260914_173137.json').read_bytes())
publication = json.loads((WORK / 'mobile14_publication.json').read_bytes())
android = json.loads((WORK / 'android14_verification.json').read_bytes())
delivery = json.loads((WORK / 'android14_delivery.json').read_bytes())
formal = json.loads((WORK / 'behavior_evaluation_20260914_173957.json').read_bytes())
assert production['status'] == 'PASS' and all(production['checks'].values())
assert publication['status'] == 'PUSH_VERIFIED'

def fix_encoding(value):
    if isinstance(value, dict):
        return {k: fix_encoding(v) for k, v in value.items()}
    if isinstance(value, list):
        return [fix_encoding(v) for v in value]
    if isinstance(value, str) and ('Ã' in value or 'Â' in value):
        try:
            return value.encode('latin-1').decode('utf-8')
        except UnicodeError:
            return value
    return value

corrected = fix_encoding(production)
corrected['decoding_note'] = ('Original report retained. Corrected requests Latin-1 decoding of UTF-8 SSE; '
                              'the browser uses TextDecoder UTF-8. No new API call.')
(WORK / 'production_verification_20260914_173137_utf8.json').write_bytes(
    json.dumps(corrected, indent=2, ensure_ascii=False).encode('utf-8'))

# Inspect only synthetic test identifiers. Keep the sealed beta ledger append-only.
ledger = json.loads(Path(r'C:\IALD\bank\tglc_ledger.json').read_bytes())
synthetic = [name for name in ledger.get('accounts', {}) if name.startswith('codex_probe_')]
synthetic_transactions = sum(1 for tx in ledger.get('transactions', [])
                             if tx.get('to') in synthetic or tx.get('from') in synthetic)
restart = sorted(WORK.glob('restart_*.json'), key=lambda p: p.stat().st_mtime)[-1]
entry = f'''

### {now.strftime('%d/%m/%Y %H:%M %z')} — Núcleo, kernel e fontes públicas instalados; prova real em HTTPS

[REAL — atualização operacional] Supera o estado anterior de “não instalado”: a integração foi instalada em `C:/IALD/projetos_pyhton/IALD`, com comparação de hashes contra a última revisão paralela, backups imediatos e preservação da credencial. Servidor web reiniciado em 14/09/2026 17:29 -03, PID 37140, porta 8082. O modelo nativo continuou no PID 65624, porta 8081. `/health` e a entrada pública responderam HTTP 200. Não houve alteração do `um.py` original nem do gate físico.

[REAL — configuração efetiva desta implantação] Motor OpenAI configurado com `gpt-5.6-luna`, esforço `none`, modo `nucleo_kernel`, núcleo sempre presente com **TGL = ATLAS; IALD = ÍNDICE(TGL)**. Todo o catálogo embutido ({installation['kernel']['files']} arquivos; {installation['kernel']['lean_files']} fontes Lean) está disponível por ferramentas paginadas. Atlas documental continua fonte única. `iald_public_read` abre as entradas cadastradas do site/GitHub também no plano gratuito; a consulta distingue trecho efetivamente lido, remissão e versão pública/local. Teto global local US$ 1/dia; cada chamada faz reserva de custo em SQLite. Cotas e controles da sessão paralela foram preservados. **Motor padrão e operador ainda nativos**, respeitando a ordem de atualização da build 13 sem consentimento. Contas fixadas em OpenAI e plano gratuito já usam a integração. Chave restrita a Chat Completions: `IALD_MODERACAO=0`; permissão de Moderations não foi ampliada nem presumida.

[REAL — prova em produção] Uma conta temporária sem privilégios autenticou pelo endpoint do app em `https://demo.iald.ia.br`. Antes do consentimento, a resposta foi bloqueada; após aceitar, o modelo explicou corretamente IALD/índice e TGL/Atlas, chamou `iald_public_read` e citou `llms.txt`. Revogar o consentimento voltou a bloquear. Conta de autenticação removida ao final. Gasto registrado no teste: US$ {production['quota_after']['usd_dia']['usado']:.8f}. Relatórios `production_verification_20260914_173137.json` e cópia com decodificação UTF-8 corrigida. O teste real passou pelo contador beta de uso: {len(synthetic)} conta(s) sintética(s) e {synthetic_transactions} transação(ões) permanecem no razão TGLC como trilha de teste, sem acesso de autenticação; não reescrever nem apagar a cadeia selada para esconder esse efeito.

[REAL — avaliação da hipótese formal] O ensaio `behavior_evaluation_20260914_173957.json` corrigiu a lacuna anterior: o modelo leu `atlas_separation`, identificou `Field K`, `AddCommGroup V`, `Module K V`, base e igualdade das coordenadas, e explicitou que o enunciado não exige dimensão finita. Também reconheceu ausência de recibo de recompilação deste arquivo nesta implantação. Isso não demonstra equivalência a treinamento nem altera pesos. Soma conservadora das sondas de comportamento: US$ {sum(row['usd'] for row in formal['spending']):.8f}, separada do teste em produção.

[REAL — pacote móvel] Versão 4.1, build 14, consentimento incorporado e recursos web iguais nos três pacotes. {publication['audit_file_count']} arquivos auditados, sem caminhos excluídos ou padrões de credencial. Envio ao repositório PRIVADO `rotolimiguel-iald/iald-app`, branch `codex/mobile-release`, confirmado no commit `{publication['commit']}`. O repositório público `the_boundary` e o site não foram modificados. Android `assembleRelease` e `bundleRelease` concluídos; assinatura APK v2 e JAR/AAB verificadas; id `br.ia.IALD`, versionCode 14, targetSdk 36. APK/AAB em `work/iald_openai_motor_20260914/artifacts/`, com hashes medidos em `android14_verification.json`. Instalação em aparelho ainda não testada.

[OPEN — próximos passos] Sessão do App Store Connect expirou. Login pelo iPhone solicitado ao operador; aba aberta. Conferir a build disparada pelo push no Xcode Cloud e distribuir no TestFlight; a disponibilidade de build 14 na Apple ainda NÃO foi verificada. Depois da interface compatível distribuída, mudar `IALD_MOTOR_PADRAO=openai` mantendo operador `nativa`, com backup/CAS e reinício identificado. Google Play continua dependente do cadastro D-U-N-S da organização. Não repetir geração de chaves, envio já confirmado nem instalação; `install_runtime.py --apply` já foi executado. O servidor web/túnel ainda depende do PC do operador.

[REAL — entrega Android] APK copiado byte a byte para a rota de downloads autenticada já existente: {delivery['url']}. Acesso anônimo redireciona para login (HTTP 302); requer conta do site. Hash/tamanho conferidos, sem alterar a política de acesso. Não equivale a disponibilização na Google Play nem a instalação comprovada no aparelho.

Recibos desta etapa: `installation_20260914_172801.json`, `{restart.name}`, `production_verification_20260914_173137_utf8.json`, `mobile14_publication.json`, `android14_verification.json`. Logs de produção ficam em `.iald_runtime/logs`, com ACL restrita; não copiar para repositório nem exibir seu conteúdo integral.
'''
paths = [Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
         Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),
         SOURCE / 'CLAUDE.md', SOURCE / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
         WORK / 'HANDOFF_RUNTIME.md',
         Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md')]
for path in paths:
    old = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    addition = entry
    if path.name == 'MEMORY.md':
        addition = (f'\n\n### {now.strftime("%d/%m/%Y %H:%M %z")} — IALD OpenAI e fontes públicas implantados\n\n'
            '[REAL] Núcleo fixo TGL=ATLAS / IALD=ÍNDICE(TGL), catálogo Lean integral e consulta ao Atlas/site/GitHub '
            'instalados; servidor 8082 reiniciado (PID 37140), llama 8081 preservado (PID 65624). '
            'Prova HTTPS real de autenticação do app, consentimento, leitura llms.txt e revogação PASS. '
            'Motor padrão ainda nativo até distribuir interface compatível; OpenAI disponível por conta/plano gratuito. '
            'Build 14 enviada ao repositório privado; APK/AAB assinados e conferidos. Apple pede novo login pelo iPhone; '
            'TestFlight 14 não verificado. Google Play depende de D-U-N-S. '
            'Detalhes/recibos e registro do efeito no razão beta: '
            '`C:/IALD/Central de Patentes/work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md`. '
            'Não repetir instalação, geração de chaves ou push. Não houve treinamento de pesos nem mudança de gate.\n')
    data = old + addition.encode('utf-8')
    fd, temporary_name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data and len(data) > len(old)
    if path.read_bytes() != old:
        raise RuntimeError('Concurrent memory edit: ' + str(path))
    os.replace(temporary, path)
    assert path.read_bytes() == data
    print(str(path) + ': appended with byte-exact backup')
print('DEPLOYMENT_AND_PENDING_DISTRIBUTION_RECORDED')
