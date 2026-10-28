"""Record the direct editorial acceptance without changing the approved media."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys

E = Path(__file__).resolve().parent
W = E.parent
T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_E')
sys.path.insert(0, str(W))
from bootstrap import ACTOR, REF, cli
import mission


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def create(p, content):
    b = content.encode('utf-8') if isinstance(content, str) else (json.dumps(content, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if p.exists():
        if p.read_bytes() == b:
            return
        raise RuntimeError('Existing receipt differs: ' + str(p))
    temp = p.with_name(p.name + '.tmp_' + str(os.getpid()))
    with temp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == b and len(b) > 0
    # Windows rename is atomic here and refuses an existing destination.
    os.rename(temp, p)


def main():
    project = mission.call({'operation': 'project', 'max_chars': 300000})
    assert not project['projection']['hold']
    assert not project['projection']['unresolved_handles']
    result = E / 'CONSTRUCTION_DELIVERY_V402.json'
    d = read(result)
    review = read(E / 'FINAL_INTEGRATION_REVIEW.json')
    assert review['status'] == 'PASS_WITH_SCOPE'
    assert pin(result) == review['construction']
    assert pin(T / 'RESULTADO.json') == review['result']
    for key in ('delivery', 'manifest'):
        assert pin(Path(d[key]['path'])) == d[key]
    previews = read(E / 'FORMULA_LISTENING_PREVIEWS.json')
    for row in previews['previews']:
        assert pin(Path(row['preview']['path'])) == row['preview']
    capture = read(E / 'SOURCE_CAPTURE.json')
    source_rows = [capture['canonical_seal']] + [r['canonical'] for r in capture['files']]
    checks = [{'path': r['path'], 'expected_sha256': r['sha256'],
               'actual_sha256': pin(Path(r['path']))['sha256']} for r in source_rows]
    source_unchanged = all(r['actual_sha256'] == r['expected_sha256'] for r in checks)
    verbatim = E / 'OPERADOR_ACEITE_LOCUCAO_20261027.txt'
    create(verbatim, 'ótimo, gostei, prossiga')
    acceptance = {
        'schema': 'iald.video-editorial-acceptance/v1',
        'status': 'OPERATOR_EDITORIAL_ACCEPTANCE_RECORDED',
        'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'recorded_by': ACTOR,
        'origin': 'Direct human message in this Codex conversation, following the revised formula narration and PT/EN previews.',
        'original': pin(verbatim), 'statute': 'INPUT',
        'scope': 'Aceite editorial da locução explicativa das fórmulas apresentada em PT/EN e continuidade da entrega V7 já construída.',
        'scope_limits': [
            'Não é alegação de audição integral nem benchmark de pronúncia.',
            'Não é aceite das prévias anteriores de voz pessoal; estas permanecem separadas.',
            'A publicação continua atribuída à gerência pelo Adendo E; esta sessão não publicou.',
            'Não substitui revisão independente da missão nem altera estatuto científico ou gate.'
        ],
        'construction': pin(result), 'independent_review': pin(E / 'FINAL_INTEGRATION_REVIEW.json'),
        'public_pointer': d['delivery'], 'public_manifest': d['manifest'],
        'preview_receipt': pin(E / 'FORMULA_LISTENING_PREVIEWS.json'),
        'previews': [r['preview'] for r in previews['previews']],
        'source_unchanged_at_acceptance': source_unchanged, 'source_checks': checks,
        'mission_reference': str(REF), 'observed_revision': project['receipt']['revision'],
        'next_action': ('Gerência integra/publica o pacote aprovado por hash conforme Adendo E.' if source_unchanged else
                        'Fonte canônica avançou/divergiu; gerência decide reancoragem antes de publicar. Aceite editorial da versão apresentada preservado.'),
        'new_tts_requests': 0, 'new_renders': 0, 'media_modified': False, 'publication_performed': False
    }
    create(E / 'OPERATOR_EDITORIAL_ACCEPTANCE.json', acceptance)
    create(T / 'ACEITE_OPERADOR_LOCUCAO_20261027.json', acceptance)
    note = (
        '# Aceite editorial — locução V7 PT/EN\n\n'
        '[INPUT] O operador respondeu «ótimo, gostei, prossiga» à entrega da locução explicativa e às prévias PT/EN.\n'
        'O texto original, seu hash e o vínculo aos artefatos estão em ACEITE_OPERADOR_LOCUCAO_20261027.json.\n'
        '[REAL] A correção já está incorporada aos dois filmes; pacote e revisão independente mantiveram seus hashes.\n'
        + ('[REAL] Fontes canônicas conferidas e ainda coincidentes com a construção v402.\n' if source_unchanged else
           '[OPEN] Fonte canônica divergente: consultar source_checks e reancorar pela gerência antes de publicar.\n')
        + 'Próximo passo: integração/publicação pela gerência, conforme Adendo E, reutilizando RESULTADO.json e PUBLIC_DELIVERY_V7.json.\n'
        'Nenhum novo render, envio TTS, alteração dos filmes ou publicação foi realizado neste aceite.\n'
        'As prévias de voz pessoal continuam separadas; este aceite se refere à locução explicativa apresentada.\n'
    )
    create(T / 'ACEITE_OPERADOR_LOCUCAO_20261027.md', note)
    create(E / 'MEMORY_EDITORIAL_ACCEPTANCE_TEXT.txt', note)
    state = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'get', 'reference': str(REF)})['result']
    transition = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {
        'operation': 'transition', 'reference': str(REF), 'actor': ACTOR,
        'expected_revision': state['revision'], 'event_id': 'ordem022-v402-operator-editorial-acceptance-20261027',
        'changes': {
            'records': [{'id': 'v402_operator_editorial_acceptance_20261027', 'kind': 'fact', 'statute': 'INPUT',
                         'text': 'Operador: «ótimo, gostei, prossiga», após entrega da locução explicativa PT/EN. Aceite editorial registrado com vínculo aos arquivos apresentados. Filmes já corrigidos; continuidade por integração/publicação pela gerência. Voz pessoal não incluída neste aceite; não repetir renders/TTS encerrados.',
                         'sources': [{'kind': 'artifact', 'ref': str(verbatim), 'sha256': pin(verbatim)['sha256']},
                                     {'kind': 'artifact', 'ref': str(T / 'ACEITE_OPERADOR_LOCUCAO_20261027.json'), 'sha256': pin(T / 'ACEITE_OPERADOR_LOCUCAO_20261027.json')['sha256']}]}],
            'flow': {'phase': 'v402_editorial_acceptance_recorded_for_management',
                     'next_action': acceptance['next_action'] + ' Voz pessoal permanece separada para decisão própria; renders/TTS encerrados não se repetem.'}
        }
    })
    assert transition['ok'], transition
    create(E / 'OPERATOR_ACCEPTANCE_ACOM.json', transition)
    print(json.dumps({'status': acceptance['status'], 'source_unchanged': source_unchanged,
                      'handoff': str(T / 'ACEITE_OPERADOR_LOCUCAO_20261027.json'),
                      'transition': transition['result'].get('receipt', transition['result'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
