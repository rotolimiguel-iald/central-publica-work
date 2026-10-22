"""Record the human support reply and the newly encountered account agreement."""
from datetime import datetime
from pathlib import Path
from goal16_records import ROOT, WORK, record, write_new

note = ('[REAL] A atendente Erica confirmou o formulário gratuito em '
        'https://www.dunsguide.com/pt/signup?redirected_from=duns_application. Orientou selecionar '
        'Solicitar número DUNS, não Adicionar empresa; preencher formulário da etapa 1 e anexá-lo '
        'na etapa 3, sem balanços financeiros. Informou prazo normal de 30 dias. No formulário, '
        'selecionados Brasil → Google → Posso esperar 30 dias úteis. A próxima etapa é Criar conta, '
        'com e-mail, aceite de Termos/Política e reCAPTCHA. [INPUT/LEGAL] Cadastro preparado com '
        'contato@iald.ia.br; termos não aceitos, CAPTCHA não acionado, conta não criada. Pergunta '
        'específica enviada ao operador para cadastro gratuito/aceite/verificação. Termos consultados: '
        'https://www.iubenda.com/termos-e-condicoes/42598177. Nenhum serviço pago, número DUNS '
        'ou pedido de emissão concluído. Recibo duns_support_reply_20260915.json supersede a '
        'pendência anterior de formulário não confirmado; permanece pendente o cadastro/solicitação.')
record('duns_support_reply_20260915.json', {
    'task': 'T5 — retorno humano e cadastro gratuito preparado', 'status': '[REAL]',
    'agent': 'Erica', 'form_url': 'https://www.dunsguide.com/pt/signup?redirected_from=duns_application',
    'support_instructions': {'free': True, 'normal_processing_days': 30,
                             'financial_statements_required': False,
                             'choose': 'Solicitar número DUNS',
                             'form_flow': 'Fill step 1 form; attach it in step 3.'},
    'observed_signup': {'country': 'Brasil', 'reason': 'Preciso fornecer isso ao Google',
                        'urgency': 'Posso esperar 30 dias úteis', 'email': 'contato@iald.ia.br',
                        'terms_accepted': False, 'captcha_completed': False, 'account_created': False},
    'terms_url': 'https://www.dunsguide.com/pt/terms-and-conditions',
    'terms_document_url': 'https://www.iubenda.com/termos-e-condicoes/42598177',
    'privacy_url': 'https://www.dunsguide.com/pt/privacy-policy',
    'operator_approval': 'PENDING_SPECIFIC_ACCOUNT_TERMS_AND_CAPTCHA',
    'duns_received': False, 'paid_service': False,
}, note)

surfaces = [WORK / 'HANDOFF_RUNTIME.md', ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md', WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
snapshots = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for p, before in snapshots.items():
    assert p.read_bytes() == before, 'Parallel edit: ' + str(p)
    write_new(p.with_name(p.name + '.bak_' + stamp), before)
    newline = '\r\n' if b'\r\n' in before else '\n'
    after = before + ('\n\n### 15/09/2026 — Adendo T5: formulário gratuito confirmado\n\n' + note + '\n').replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == before, 'Parallel edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after
print('DUNS_SUPPORT_REPLY_RECORDED_WITH_BYTE_BACKUPS')
