"""Publish a local stop receipt; never changes a media/public delivery file."""
import json
import subprocess
from inspect_gate_stop import F, W, T, V, N, ORDER, REQUEST, current, create, pin, read, mission, cli, REF, ACTOR


def run_cli(name, command):
    r = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8', *command], capture_output=True, text=True, encoding='utf-8')
    create(F / name, {'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)


def main():
    assert not (T / 'RESULTADO.json').exists(), 'Recover the existing final receipt instead of repeating'
    review_path = F / 'INDEPENDENT_STOP_REVIEW.json'
    review = read(review_path)
    assert review['verdict'].startswith('PASS'), review
    p = mission.call({'operation': 'project', 'max_chars': 350000})
    task = next(t for t in p['projection']['active'] if t['id'] == 'ADENDO_F_V403')
    check = mission.call({'operation': 'check', **current(), 'task_id': task['id'], 'lease_id': task['lease']['id'], 'max_chars': 350000})
    assert check['ready']
    create(F / 'FINAL_PREFLIGHT.json', check)
    result = read(F / 'GATE_NARRATION_STOP.json')
    for key in ('preserved_v402_pointer', 'preserved_v402_manifest'):
        assert pin(__import__('pathlib').Path(result[key]['path'])) == result[key]
    result['independent_review'] = pin(review_path)
    result['origin_verified'] = pin(F / 'ORIGIN_VERIFIED.json')
    result['final_source'] = {'program': pin(N / 'um.py'), 'seal': pin(N / 'um_absoluto_selo.json'), 'version': read(N / 'um_absoluto_selo.json')['um_version']}
    result['source_unchanged_during_inspection'] = result['final_source']['program'] == result['current_source']['program'] and result['final_source']['seal'] == result['current_source']['seal']
    result['review_scope'] = 'Confirmação independente da condição de parada e frases existentes; não é aceite de render v403 ou de nova redação.'
    create(T / 'RESULTADO.json', result)
    create(F / 'FINAL_STOP_DELIVERY.json', result)
    pt = [r for r in result['phrases'] if r['language'] == 'pt-BR']
    en = [r for r in result['phrases'] if r['language'] == 'en']
    lines = [
        '# ORDEM 022 — ADENDO F: parada anterior ao render v403',
        '[REAL] STOP_GATE_NARRATION_REQUIRES_MANAGEMENT; request_id ' + REQUEST + '.',
        'O Adendo F exige parar se a V7 mencionar as bandeiras do gate; as duas cenas abaixo acionam essa condição.',
        'Filme 1, segmento horizon, 144–168s: ' + pt[0]['text'],
        'EN: ' + en[0]['text'],
        'Filme 2, segmento einstein, 288–324s: ' + pt[1]['text'],
        'EN: ' + en[1]['text'],
        'Os intervalos são os segmentos completos, não o início exato da segunda fala. FR/zh-Hans também constam no RESULTADO.json.',
        '[REAL] Frases verificadas no plano final v402 e nas legendas; revisão independente em INDEPENDENT_STOP_REVIEW.json, pinada no resultado.',
        '[REAL] Selo/programa atuais v403 lidos e conferidos; nenhuma execução/importação de um.py.',
        '[REAL] Zero render e zero TTS novos; nenhum custo novo de TTS incorrido e nenhuma publicação.',
        '[REAL] Filmes, ponteiro e manifesto v402 preservados; PUBLIC_DELIVERY_V7.json não reemitido porque o render foi interrompido antes de começar.',
        '[OPEN] Comparação integral dos demais números não executada após a condição obrigatória de parada.',
        '[OPEN] Gerência deve decidir as frases do gate; eventual necessidade/custo de TTS será apresentada antes de qualquer envio.',
        'O aceite editorial PT/EN anterior permanece; esta entrega não o revoga e não altera o gate científico.'
    ]
    assert len(lines) <= 20
    create(T / 'RELATORIO.md', '\n'.join(lines) + '\n')
    create(F / 'MEMORY_DEPOSIT_TEXT.txt', '[REAL] Adendo F v403: parada obrigatória antes de render/TTS. A V7 aprovada contém nos dois filmes a frase sobre 15 bandeiras calculadas e 3 literais do gate; frases integrais PT/EN/FR/zh-Hans, segmentos, legendas e hashes estão no RESULTADO.json do ADENDO_F. Revisão independente conferiu o diagnóstico. Filmes e manifesto v402 preservados; zero novas sínteses/renderizações/publicações. [OPEN] Gerência decide a redação do gate antes da comparação restante e da estimativa de eventual TTS. O aceite editorial anterior permanece.\n')
    src = [{'path': str(T / 'RESULTADO.json'), 'sha256': pin(T / 'RESULTADO.json')['sha256']}, {'path': str(ORDER), 'sha256': pin(ORDER)['sha256']}]
    blocked = mission.call({'operation': 'block', **current(), 'task_id': task['id'], 'reason': 'Condição de parada explícita do Adendo F: ambas as narrações contêm frases sobre as bandeiras do gate. Decisão da gerência requerida antes de render/TTS.', 'sources': src, 'event_id': REQUEST + '-gate-phrase-stop'})
    create(F / 'MISSION_BLOCKED.json', blocked)
    state = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'get', 'reference': str(REF)})['result']
    tr = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'transition', 'reference': str(REF), 'actor': ACTOR, 'expected_revision': state['revision'], 'event_id': REQUEST + '-stop-delivery', 'changes': {
        'records': [{'id': 'v403_adendo_f_gate_phrase_stop', 'kind': 'fact', 'statute': 'REAL', 'text': 'Adendo F v403 interrompido antes do render pela frase existente sobre 15 bandeiras calculadas e 3 literais do gate, em ambos os filmes e quatro línguas. Revisão independente do diagnóstico; v402 preservada. Não houve novo TTS/render/importação do programa/publicação. Demais números não comparados após a parada; gerência decide redação antes de eventual custo TTS.', 'sources': [{'kind': 'artifact', 'ref': str(T / 'RESULTADO.json'), 'sha256': pin(T / 'RESULTADO.json')['sha256']}]}],
        'flow': {'phase': 'v403_stopped_gate_narration_management_decision', 'next_action': 'Gerência lê ADENDO_F/RESULTADO.json e decide as duas frases do gate. Depois comparar demais números e apresentar custo de eventual TTS antes do único render v403 autorizado. Não repetir unidades encerradas.'}}})
    assert tr['ok']
    create(F / 'STOP_DELIVERY_ACOM.json', tr)
    route = {'tipo': 'RESULTADO', 'rota_id': 'site.filmes.v7.ordem022', 'dominio': 'SITE_E_PUBLICACAO', 'titulo': 'Adendo F v403: parada por frases existentes sobre o gate', 'resultado': 'Duas cenas, quatro línguas: gate com 15 bandeiras calculadas e 3 literais. Zero novo render/TTS. V402 preservada.', 'veredito': result['status'], 'estatuto': 'REAL', 'status': 'EXAMINADA', 'olhou_dados': False, 'defeito': 'Redação das bandeiras do gate depende da gerência conforme Adendo F.', 'nao_refazer': 'Não repetir render/TTS v402 nem iniciar v403 antes da decisão da gerência; reutilizar este diagnóstico.', 'proximo_passo': 'Gerência decide redação; eventual custo TTS antes de envio.', 'onde': str(F), 'artefatos': [str(T / 'RESULTADO.json'), str(review_path)], 'refs': [], 'nota': 'Parada editorial explícita, sem alteração de ciência ou gate.'}
    create(F / 'STOP_ROUTE.json', route)
    run_cli('BOARD_STOP.json', [r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F0.FILMES_V7_20261024', '--quem', ACTOR['id'], '--status', 'BLOQUEADA', '--evidencia', str(T / 'RESULTADO.json'), str(review_path), '--nota', 'Adendo F exige decisão da gerência sobre duas frases do gate; nenhum render/TTS iniciado.'])
    run_cli('ROUTE_STOP.json', [r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(F / 'STOP_ROUTE.json'), '--quem', ACTOR['id']])
    print(json.dumps({'status': result['status'], 'result': pin(T / 'RESULTADO.json'), 'report_lines': len(lines)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
