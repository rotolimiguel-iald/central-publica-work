"""Anchor the authorized ADENDO B in this film mission; no rendering."""
from pathlib import Path
import hashlib, json, os, subprocess, sys

B = Path(__file__).resolve().parent
W = B.parent
sys.path.insert(0, str(W))
import mission

ACTOR = 'codex-video-v7'
SOURCE = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_B_selo_corrente_v401.md')
PY = r'C:\Python314\python.exe'

def save(name, data):
    p = B / name
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if p.exists():
        assert p.read_bytes() == raw, f'Existing receipt differs: {p}'
        return
    temp = p.with_suffix(p.suffix + '.tmp')
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw
    os.replace(temp, p)

def main():
    source = {'path': str(SOURCE), 'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    save('AUTHORIZATION.json', {
        'statute': 'INPUT', 'source_order': source,
        'request_id': '70185653-afa4-4dc0-8127-5518ca979312',
        'official_source_thread': '01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
        'official_user_turn': '01a17470-e5e5-7400-aafd-3cbb89a4ed41',
        'verification': 'read_thread returned a userMessage relaying gerencia a7 and naming this exact order and SHA256; disk SHA256 matched.',
        'own_reference': mission.REF,
        'scope': 'Current-seal rerender with explicit STOP on changed film numbers or seal version; no publication or personal voice incorporation.'
    })
    for name, args in [
        ('MAP_BEFORE.json', [r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'ver', 'site.filmes.v7.ordem022']),
        ('BOARD_BEFORE.json', [r'C:\IALD\PROGRAMA_IALD\iald.py', 'ver', 'F0.FILMES_V7_20261024']),
    ]:
        r = subprocess.run([PY, '-B', '-X', 'utf8', *args], capture_output=True, text=True, encoding='utf-8', check=True)
        save(name, json.loads(r.stdout))
    r = subprocess.run([PY, '-B', '-X', 'utf8', r'C:\IALD\NOS_VIVO\consultar.py', '--unidade', 'F0.FILMES_V7_20261024'], capture_output=True, text=True, encoding='utf-8', check=True)
    save('NOS_BEFORE.json', {'stdout': r.stdout, 'exit_code': r.returncode})
    p = mission.project()
    tasks = p['projection']['active'] + p['projection']['settled']
    if not any(t['id'] == 'ADENDO_B' for t in tasks):
        result = mission.call({'operation': 'extend', **mission.current(ACTOR),
            'event_id': 'ordem022-adendo-b-extend-current-seal',
            'requirements': [{'id': 'ADENDO_B', 'criterion': 'Renderizar V7 contra selo corrente lido no início e antes da entrega; preservar estilo e narração existente, 64+ âncoras, replay offline e manifestos atuais. PARAR e relatar se algum número do filme mudar ou a versão avançar, sem sobrescrever entrega anterior; gerência decide continuidade. Voz pessoal e publicação excluídas.', 'depends_on': []}],
            'reason': 'ADENDO B autenticado e retomado após desvio de escopo na compactação; nenhuma execução B existente na projeção.',
            'sources': [source]})
        save('MISSION_EXTEND.json', result)
    p = mission.project()
    t = next(t for t in p['projection']['active'] + p['projection']['settled'] if t['id'] == 'ADENDO_B')
    if not t.get('lease'):
        save('MISSION_CLAIM.json', mission.call({'operation': 'claim', **mission.current(ACTOR), 'task_id': 'ADENDO_B', 'lease_seconds': 43200, 'event_id': 'ordem022-adendo-b-claim-current-seal'}))
    p = mission.project()
    t = next(t for t in p['projection']['active'] + p['projection']['settled'] if t['id'] == 'ADENDO_B')
    result = mission.call({'operation': 'check', **mission.current(ACTOR), 'task_id': 'ADENDO_B', 'lease_id': t['lease']['id'], 'max_chars': 100000})
    assert result['ready'], result
    save('PREFLIGHT.json', result)
    save('EXECUTION_RECOVERY.json', {'receipt': p['receipt'], 'flow': p['projection']['flow'], 'terminal_handles': p['projection'].get('terminal_handles', []), 'finding': 'No active execution handle; no ADENDO B render dispatched by this session. All prior rendering handles are terminal and remain preserved.'})
    print(json.dumps({'status': 'READY_FOR_READ_ONLY_COMPARISON', 'receipt': result['receipt']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
