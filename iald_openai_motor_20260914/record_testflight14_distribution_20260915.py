"""Record the verified Apple distribution, preserving build 16 as outstanding."""
from datetime import datetime
from pathlib import Path
import sys
from goal16_records import ROOT, WORK, record, write_new

sys.stdout.reconfigure(encoding='utf-8')
surfaces = [ROOT / 'CLAUDE.md', WORK / 'HANDOFF_RUNTIME.md',
            ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md',
            WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
snapshots = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
group_url = ('https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/'
             'apps/6760655636/testflight/groups/0f9c8943-18f0-4f10-82ad-89a5832b9dec/builds')
build_url = ('https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/'
             'apps/6760655636/testflight/ios/c9725ecf-e531-4fcb-934e-30d9819dec10')
cloud_url = ('https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/'
             'xcode-cloud/products/3BFB990A-9532-45B2-9FAB-EDBD9D9EBD78/'
             'builds/9e43d661-b97c-47b4-8706-76b771d3c5a6/summary')
notes = ('Teste interno da IALD no iPhone e no iPad.\n\n'
         '1. Entrar na conta e retomar a sessão.\n'
         '2. Iniciar e continuar conversas, conferindo a exibição progressiva das respostas.\n'
         '3. Conferir o consentimento para uso da OpenAI quando solicitado e a opção de revogação.\n'
         '4. Verificar os painéis de créditos e uso, os limites disponíveis e os avisos de cota.\n'
         '5. Testar a denúncia de respostas.\n'
         '6. Conferir a interface, a navegação, os ícones e a adaptação à tela do iPad.\n\n'
         'Os créditos TGLC são unidades fictícias de teste beta, sem valor comercial. '
         'Informe eventuais falhas e os passos para reproduzi-las.')
note = ('[REAL] Operador entrou na Apple; autenticação conferida no App Store Connect. '
        'Xcode Cloud 14, Archive iOS processado com sucesso, corresponde ao commit '
        'cf00db8ddbf7f95e8585db6093899314b7270f42 (atualização denominada build 15 no '
        'repositório). A numeração automática Apple é 4.1 (14). Salvo O que testar '
        'em português e adicionada a compilação ao grupo interno IALD Equipe. '
        'Lista do grupo confirmou 4.1 (14) Em testes, 1 tester e 2 compilações '
        '(13 e 14). Instalação observada do tester ainda 4.1 (13); atualização '
        'no aparelho NÃO verificada. [INPUT] Isso resolve a autenticação e a '
        'distribuição da revisão já enviada; NÃO conclui a ordem da build 16. '
        'Build 16 segue local, aguardando a autorização específica já solicitada '
        'para 173 arquivos no repositório privado e APK autenticado. Demais '
        'pendências de chave de custos, Dunsguide e painel da política permanecem. '
        'Nenhum novo push, build, chave, reinício ou alteração de gate nesta etapa. '
        'Recibo: testflight14_distribution_20260915.json. Grupo: ' + group_url)
report = {
    'task': 'Apple autenticada; atualização anterior distribuída no TestFlight',
    'status': '[REAL]', 'authentication_verified': True,
    'cloud_build_number': 14, 'cloud_result': 'Processada com sucesso',
    'cloud_action': 'Archive - iOS', 'cloud_url': cloud_url,
    'source_commit_observed_in_cloud': 'cf00db8ddbf7f95e8585db6093899314b7270f42',
    'source_release_label': 15, 'testflight_version': '4.1', 'testflight_build': 14,
    'build_url': build_url, 'what_to_test': notes, 'notes_saved': True,
    'group': {'name': 'IALD Equipe', 'type': 'Interno', 'testers': 1,
              'builds': ['4.1 (14)', '4.1 (13)'], 'build_14_status': 'Em testes', 'url': group_url},
    'latest_observed_tester_installation': '4.1 (13)',
    'build_14_device_installation_verified': False,
    'build_16_goal_complete': False, 'build_16_publication': 'PENDING_EXISTING_SPECIFIC_APPROVAL',
    'new_push_or_compilation_this_turn': False, 'server_restarted': False,
}
for path, before in snapshots.items():
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
record('testflight14_distribution_20260915.json', report, note,
       before_memory=snapshots[ROOT / 'CLAUDE.md'])
for path in surfaces[1:]:
    before = snapshots[path]
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
    backup = path.with_name(path.name + '.bak_' + stamp)
    write_new(backup, before)
    assert backup.read_bytes() == before
    newline = '\r\n' if b'\r\n' in before else '\n'
    append = '\n\n### 15/09/2026 — Apple autenticada; TestFlight 4.1 (14) em testes\n\n' + note + '\n'
    after = before + append.replace('\n', newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    write_new(temp, after)
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
    temp.replace(path)
    assert path.read_bytes() == after and len(after) > len(before)
print('TESTFLIGHT14_RECORDED; BYTE_BACKUPS_VERIFIED; BUILD16_STILL_PENDING')
