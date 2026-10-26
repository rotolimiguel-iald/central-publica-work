"""Record the explicit numerical STOP without claiming a v401 delivery."""
from pathlib import Path
import hashlib, json, subprocess, sys

B = Path(__file__).resolve().parent
W = B.parent
sys.path.insert(0, str(W))
import mission
from bootstrap import cli, REF, ACTOR
from bootstrap_b import save

T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_B')
PY = r'C:\Python314\python.exe'

def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    result = T / 'RESULTADO.json'
    d = json.loads(result.read_bytes())
    assert d['status'] == 'STOPPED_NUMERIC_CHANGE_REQUIRES_MANAGEMENT_DECISION'
    assert not d['render_started'] and not d['manifest_reissued']
    for e in d['evidence'] + [d['manifest']]:
        assert pin(Path(e['path']))['sha256'] == e['sha256'], e['path']
    assert len((T / 'RELATORIO.md').read_text(encoding='utf-8').splitlines()) <= 20
    p = mission.project()
    task = next(t for t in p['projection']['active'] + p['projection']['settled'] if t['id'] == 'ADENDO_B')
    if task['status'] != 'blocked':
        blocked = mission.call({'operation': 'block', **mission.current(ACTOR['id']), 'task_id': 'ADENDO_B', 'lease_id': task['lease']['id'], 'event_id': 'ordem022-adendo-b-numeric-stop', 'reason': 'Cláusula explícita PARAR do ADENDO B: escada 9541/9541→9561/9561, arquivos formais 1429→1430 e declarações 29296→29318. Gerência decide antes de render; entrega v400 preservada.', 'sources': [pin(result), d['source_order']]})
        save('MISSION_BLOCKED.json', blocked)
    state = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'get', 'reference': str(REF)})['result']
    tr = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {
        'operation': 'transition', 'reference': str(REF), 'actor': ACTOR,
        'expected_revision': state['revision'], 'event_id': 'ordem022-adendo-b-stop-' + pin(result)['sha256'][:16],
        'changes': {
            'records': [{'id': 'adendo_b_numeric_stop_v401', 'kind': 'fact', 'statute': 'REAL',
                'text': 'ADENDO B retomado e diagnosticado antes de render. Selo v401 e pinos dos artefatos conferidos. HUD v400 contém escada 9541/9541, 1429 arquivos e 29296 declarações; fonte v401 registra 9561/9561, 1430 e 29318. Parada explícita da ordem aplicada; nenhum novo render/import/TTS/publicação, manifestos v400 preservados. Voz pessoal segue independente, não condiciona render com vozes existentes. Decisão de continuidade cabe à gerência.',
                'sources': [{'kind': 'artifact', 'ref': str(result), 'sha256': pin(result)['sha256']}]}],
            'flow': {'phase': 'adendo_b_stopped_numeric_change_awaiting_management', 'next_action': 'Gerência a7 avalia ADENDO_B/RESULTADO.json e decide o tratamento das contagens antes de renderizar. Manter v400 e prévias de voz. Não repetir execuções terminais/incertas.', 'handles': state['p']['handles']}
        }})
    save('ACOM_STOP.json', tr)
    route = {'tipo': 'RESULTADO', 'rota_id': 'site.filmes.v7.ordem022', 'dominio': 'SITE_E_PUBLICACAO', 'titulo': 'ADENDO B parado antes do render por mudança de contagens',
        'resultado': 'v401 verificada; HUD v400: escada 9541/9541→9561/9561, arquivos 1429→1430, declarações 29296→29318. Cláusula PARAR aplicada; nenhum render B.',
        'veredito': d['status'], 'estatuto': 'REAL', 'status': 'EXAMINADA', 'olhou_dados': False,
        'defeito': 'Continuidade do render depende de decisão da gerência sobre as contagens, conforme ordem; não é falha científica inferida.',
        'nao_refazer': 'Preservar v400 e recibos A. Nenhum job B foi iniciado; não repetir jobs terminais ou TTS incerto.',
        'proximo_passo': 'Gerência a7 decide a continuidade após ler RESULTADO e RELATORIO do ADENDO B.',
        'onde': str(T), 'artefatos': [str(result), str(T / 'RELATORIO.md'), str(B / 'NUMERIC_DIFFERENCES.json')], 'refs': [],
        'nota': 'Contagens documentais do filme; sem nova prova, alteração de gate ou publicação. Voz pessoal independente.'}
    save('STOP_ROUTE.json', route)
    for name, args in [
        ('BOARD_STOPPED.json', [r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F0.FILMES_V7_20261024', '--quem', ACTOR['id'], '--status', 'BLOQUEADA', '--evidencia', str(result), '--nota', 'ADENDO B exige PARAR por contagens alteradas; aguarda decisão da gerência a7, não audição das prévias.']),
        ('MAP_STOPPED.json', [r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(B / 'STOP_ROUTE.json'), '--quem', ACTOR['id']]),
    ]:
        r = subprocess.run([PY, '-B', '-X', 'utf8', *args], capture_output=True, text=True, encoding='utf-8', check=True)
        out = json.loads(r.stdout)
        assert out.get('ok', True), out
        save(name, out)
    final = mission.project()
    task = next(t for t in final['projection']['active'] + final['projection']['settled'] if t['id'] == 'ADENDO_B')
    save('FINAL_STATE.json', {'receipt': final['receipt'], 'task_status': task['status'], 'flow': final['projection']['flow'], 'result': pin(result), 'self_accepted': False})
    print(json.dumps({'status': 'STOP_RECORDED', 'revision': final['receipt']['revision'], 'task_status': task['status'], 'result': str(result)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
