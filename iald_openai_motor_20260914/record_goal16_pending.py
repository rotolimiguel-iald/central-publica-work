"""Record concrete progress and pending approvals without claiming publication."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import requests
from goal16_records import ROOT, WORK, record, write_new

messages = [
    'Solicito a consulta de eventual D-U-N-S existente ou a emissão gratuita para IALD LTDA, CNPJ 62.757.606/0001-23, Goiânia/GO, Brasil, para cadastro no Google Play Console. Não desejo contratar serviços pagos. Qual é o formulário necessário?',
    'Olá, Erica. A consulta é sobre a IALD LTDA, CNPJ 62.757.606/0001-23, para o Google Play Console. Queremos saber se já existe um D-U-N-S ou como solicitar a emissão gratuita. Podemos aguardar o prazo normal de 30 dias úteis; não autorizamos serviço pago. Você consegue consultar ou indicar o formulário gratuito correto?'
]
record('duns_inquiry_20260915.json', {
    'task': 'T5 — consulta gratuita à CIAL', 'status': '[REAL]',
    'sent_on': '2026-09-15', 'destination': 'https://pt.cialdnb.com/duns-number',
    'channel': 'Intercom, Sara Flores bot → Erica, suporte humano',
    'selection': ['Google', 'Solicitar Número D-U-N-S®', 'Posso esperar 30 dias úteis',
                  'Sim, gostaria de falar com o Suporte ao Cliente'],
    'contact_sent': {'name': 'Luiz Antonio Rotoli Miguel', 'email': 'contato@iald.ia.br',
                     'company': 'IALD LTDA'},
    'messages_sent': messages,
    'verification': 'Messages appear in sent conversation; first marked read. Erica joined and greeted.',
    'automated_form_link': 'https://www.dunsguide.com/pt/signup?redirected_from=duns_application',
    'duns_number_received': False, 'paid_service_contracted': False,
    'play_console': {'url': 'https://play.google.com/console/signup',
                     'state': 'Signed in; create-developer-account screen still shown; no internal release.'},
}, '[REAL] Consulta/emissão gratuita do D-U-N-S enviada no chat oficial da CIAL com CNPJ '
   '62.757.606/0001-23. Usados nome do operador e e-mail público contato@iald.ia.br. Fluxo Google, '
   'prazo normal de 30 dias úteis; pedido explicitamente exclui serviços pagos. Bot indicou '
   'Dunsguide signup; atendente Erica entrou na conversa, cumprimento recebido e consulta '
   'esclarecida. [OPEN] Ainda sem número ou formulário confirmado pela atendente. Play Console '
   'autenticado voltou à tela Criar conta de desenvolvedor, sem conta concluída nem release interno.')

record('chave_admin_openai_20260915_pending.json', {
    'task': 'T2 — chave de custos aguarda autorização específica', 'status': '[INPUT]',
    'saved': False, 'created': False, 'name': 'IALD Custos', 'validity_days': 30,
    'prepared_permissions': {'Usage API Scope': 'Read', 'scope': 'api.usage.read',
                             'other_permissions': 'None'},
    'approval_status': 'USER_QUESTION_PENDING',
    'auto_review_reason': 'Prior authorization was for Chat Completions server key, not this administrative credential.',
    'helper_session_id': 89066,
    'cli_fix_receipt': 'balance_cli_fix_20260915.json',
    'fonte_gasto': 'registro da IALD (só o uso que passa por este servidor)',
    'avisos': ['sem chave de administrador (IALD_OPENAI_ADMIN_KEY)'],
}, '[INPUT] Chave IALD Custos preparada com somente Usage API Scope: Read e validade 30 dias. '
   'Criação rejeitada pela revisão automática, que considerou a autorização anterior limitada '
   'a Chat Completions. Pergunta específica enviada ao operador; chave NÃO criada/salva. '
   'Formulário local de uso único iniciado, sem segredo nestes recibos. Helper CLI corrigido e '
   'testado; --mostrar ainda informa ausência de chave admin. Após aprovação: criar UMA chave, '
   'salvar somente no formulário existente se ainda ativo, esperar ≥1 min e conferir Costs API.')

with requests.get('https://iald.ia.br/privacidade.html', timeout=20) as response:
    response.raise_for_status()
    body = response.content
    policy_text = body.decode('utf-8', 'replace')
draft = WORK / 'privacy_draft.html'
record('privacy16_pending.json', {
    'task': 'T6 — política de privacidade', 'status': '[INPUT]',
    'url': 'https://iald.ia.br/privacidade.html', 'http_status': 200,
    'published_sha256': hashlib.sha256(body).hexdigest(),
    'legacy_no_sharing_claim_present': 'Nenhum dado é compartilhado com terceiros' in policy_text,
    'openai_mentioned': 'openai' in policy_text.lower(),
    'draft': str(draft), 'draft_sha256': hashlib.sha256(draft.read_bytes()).hexdigest(),
    'hosting_panel': None, 'operator_question': 'Em qual painel você publica iald.ia.br?',
    'published_by_this_task': False,
    'additional_pending': 'Retention/exclusion procedure in draft still requires factual confirmation.'
}, '[REAL] Política pública relida por HTTP 200; recibo registra conteúdo/hash e presença da '
   'alegação antiga. Minuta preservada. [INPUT] Perguntado novamente o painel responsável por '
   'iald.ia.br; resposta pendente. Pela ordem T6, nada publicado sem esse destino. [LEGAL] '
   'Procedimento de retenção/exclusão ainda precisa corresponder à operação real.')

android = json.loads((WORK / 'android16_verification.json').read_bytes())
audit = json.loads((WORK / 'mobile16_audit.json').read_bytes())
summary = '''[REAL] Ordem ORDEM_CODEX_20260915_BUILD16_SALDO.md em andamento. T1: saldo US$ 9,90
lido em 15/09 às 15:15:59 UTC e registrado; nível atenção. Recarga já ligada (5→10 USD,
máximo mensal 10); projeto IALD sem spend limit. Nenhuma mudança financeira. T3: chave
IALD Servidor existente agora tem Chat Completions + Moderations Request, validade 14/10
preservada; não mudou IALD_MODERACAO nem reiniciou servidor. T4: Android 4.1 (16) compilado
e assinado; APK/AAB preservados em work/iald_openai_motor_20260914/artifacts/. 173 arquivos
auditados; JS aprovado edc227affb0550ec… preservado; versões iOS/Android 16 preparadas.
Certificado comparado a APKs 11/14/15, iguais; APK13 não encontrado nas pastas consultadas.
T5: consulta gratuita à CIAL enviada (CNPJ, nome, contato@iald.ia.br), atendente Erica entrou;
ainda não recebido D-U-N-S. Google mostra cadastro incompleto.

[INPUT] Duas autorizações específicas pendentes após rejeições automáticas: chave admin
IALD Custos (somente api.usage.read, 30 dias); publicar 173 arquivos no repositório privado
rotolimiguel-iald/iald-app/codex/mobile-release e APK na rota autenticada. Chave admin não
criada; APK16 NÃO copiado a downloads/ e nenhum commit/push da build16. Apple exige login
pelo iPhone; pergunta enviada. T6 aguarda painel de publicação do site e confirmação factual
da retenção. Objetivo inteiro permanece ativo, NÃO concluído.

Retomada: recibos saldo_openai_ancora_20260915.json, moderations_permission_20260915.json,
balance_cli_fix_20260915.json, android16_verification.json, mobile16_audit.json,
duns_inquiry_20260915.json, chave_admin_openai_20260915_pending.json e privacy16_pending.json.
NÃO repetir prepare_mobile16.py ou record_android16.py (artefatos/recibos já existem).
Após autorização de publicação: conferir CAS/auditoria; rodar deliver_android16.py e
publish_mobile16.py, então acompanhar Xcode Cloud e adicionar ao grupo IALD Equipe.
Após autorização da chave: conferir modal IALD Custos ainda preparado; salvar somente no
helper local vivo (session 89066 no momento da criação), sem expor segredo; CLI --mostrar
foi corrigido para ler a Costs API sem importar o servidor. Não criar segunda chave.
Não reiniciar servidor nem llama. Nenhuma nova afirmação formal ou mudança de gate.
'''
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
surfaces = [
    WORK / 'HANDOFF_RUNTIME.md',
    ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
    WORK.parent.parent / 'memory/TGL_ATLAS.md',
    WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
    Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
    Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md'),
]
snapshots = {p: p.read_bytes() for p in surfaces}
for p, before in snapshots.items():
    assert p.read_bytes() == before, 'Parallel memory edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, before)
    assert backup.read_bytes() == before
    newline = '\r\n' if b'\r\n' in before else '\n'
    addition = '\n\n### 15/09/2026 — Build 16 e saldo: progresso e autorizações pendentes\n\n' + summary
    after = before + addition.replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == before, 'Parallel memory edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after and len(after) > len(before)
print(json.dumps({'recorded': ['T2 pending', 'T5 inquiry sent', 'T6 pending'],
                  'memory_surfaces_updated': len(surfaces)}, ensure_ascii=False))
