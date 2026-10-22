"""Record the Apple-confirmed next build number without claiming a new build."""
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
settings_url = ('https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/'
                'xcode-cloud/products/3BFB990A-9532-45B2-9FAB-EDBD9D9EBD78/settings/build-number')
note = ('[REAL] Xcode Cloud da IALD: próximo número de compilação alterado de 15 para 16, '
        'conforme a ordem da build 16. A interface confirmou “Você alterou o próximo número '
        'da compilação para 16” e mostrou 16 como valor atual. Nenhuma compilação iniciada '
        'ou arquivo enviado. [REAL] Workflow preservado: push em codex/mobile-release; '
        'Archive iOS para App Store Connect; sem pós-ação automática. Latest Release agora '
        'mostra Xcode 27 (27A266a) e macOS Golden Gate 27 (26A428), diferente do ambiente '
        '26.6 que gerou a compilação anterior; próxima execução ainda precisa ser verificada. '
        '[INPUT] Publicação dos 173 arquivos/APK segue aguardando a autorização solicitada. '
        'TestFlight 4.1 (14) permanece a entrega atual. Nenhuma alteração de credencial, '
        'serviço, arquivo do app ou gate. Recibo xcode_next_build16_20260915.json.')
report = {
    'task': 'Xcode Cloud preparado para numerar a próxima compilação como 16',
    'status': '[REAL]', 'settings_url': settings_url, 'before': 15, 'after': 16,
    'verification': 'Success notice and next build number field both show 16.',
    'workflow_changed': False, 'trigger': 'Push on codex/mobile-release',
    'automatic_testflight_post_action': False,
    'environment_observed': {'selection': 'Latest Release', 'xcode': '27 (27A266a)',
                             'macos': 'Golden Gate 27 (26A428)', 'changed_by_this_task': False},
    'new_build_started': False, 'new_files_uploaded': False, 'build16_complete': False,
    'next_action': 'After pending publication approval, run audited delivery/push; verify cloud build16 and group.',
    'previous_resumed_goal_turn': 'PROGRESS: Apple login verified; TestFlight14 distributed',
    'current_resumed_goal_turn': 'PROGRESS: Next Cloud number set to16; publication blocker persists',
    'resumed_blocker_audit_turn': 2,
    'documentation': 'https://developer.apple.com/documentation/xcode/setting-the-next-build-number-for-xcode-cloud-builds/',
}
for p, before in snapshots.items():
    assert p.read_bytes() == before, 'Parallel edit: ' + str(p)
record('xcode_next_build16_20260915.json', report, note,
       before_memory=snapshots[ROOT / 'CLAUDE.md'])
for p in surfaces[1:]:
    before = snapshots[p]
    assert p.read_bytes() == before, 'Parallel edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, before)
    assert backup.read_bytes() == before
    newline = '\r\n' if b'\r\n' in before else '\n'
    append = '\n\n### 15/09/2026 — Xcode Cloud: próxima compilação 16\n\n' + note + '\n'
    after = before + append.replace('\n', newline).encode('utf-8')
    temp = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temp, after)
    assert p.read_bytes() == before, 'Parallel edit: ' + str(p)
    temp.replace(p)
    assert p.read_bytes() == after and len(after) > len(before)
print('XCODE_NEXT_BUILD16_RECORDED; BYTE_BACKUPS_VERIFIED; NO_BUILD_STARTED')
