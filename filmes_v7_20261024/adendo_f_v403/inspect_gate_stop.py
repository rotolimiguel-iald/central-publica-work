"""Inspect existing narration only; obey the Adendo F stop before rendering."""
import datetime
import json
from pathlib import Path
import sys

F = Path(__file__).resolve().parent
W = F.parent
sys.path[:0] = [str(W), str(W / 'adendo_e_v402')]
from record_operator_acceptance import create, pin, read
from bootstrap import cli, REF, ACTOR
import mission

ORDER = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_F_render_v403_autorizado.md')
T = ORDER.parent.parent / 'DO_CHATGPT/ORDEM_022/ADENDO_F'
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'
REQUEST = 'ordem022-adendo-f-v403-20261028'


def current():
    p = mission.call({'operation': 'project', 'max_chars': 350000})
    return {'actor': ACTOR, 'expected_revision': p['receipt']['revision'],
            'projection_sha256': p['projection_sha256']}


def main():
    assert pin(ORDER)['sha256'] == 'b7a7626fa0c100b2e56f2a41b6bb48400be6d273a6cd4848331a0cc6e3cd13ed'
    assert not (F / 'GATE_NARRATION_STOP.json').exists(), 'Recover existing result; do not repeat intake'
    s = [{'path': str(ORDER), 'sha256': pin(ORDER)['sha256']}]
    requirement = {'id': 'ADENDO_F_V403', 'criterion': 'Conferir Adendo F v403 contra V7 aprovada. Parar e informar frase sobre bandeiras do gate, outra divergência numérica ou avanço do selo; antes de novo TTS informar custo e aguardar decisão. Um único render autorizado somente após condições satisfeitas; revisão distinta e entrega local, sem publicação.', 'depends_on': []}
    r = mission.call({'operation': 'extend', **current(), 'event_id': REQUEST + '-extend',
                      'requirements': [requirement], 'reason': 'Novo adendo da gerência autenticado pela coordenadora; preserva aceite editorial e impõe condições explícitas de parada.', 'sources': s})
    create(F / 'MISSION_EXTEND.json', r)
    r = mission.call({'operation': 'claim', **current(), 'task_id': requirement['id'], 'lease_seconds': 43200, 'event_id': REQUEST + '-claim'})
    create(F / 'MISSION_CLAIM.json', r)
    p = mission.call({'operation': 'project', 'max_chars': 350000})
    task = next(t for t in p['projection']['active'] if t['id'] == requirement['id'])
    r = mission.call({'operation': 'check', **current(), 'task_id': task['id'], 'lease_id': task['lease']['id'], 'max_chars': 350000})
    assert r['ready']
    create(F / 'PREFLIGHT.json', r)
    plan_path = V / 'audio/NARRATION_PLAN_v402_formula_final.json'
    plan = read(plan_path)
    assert plan['seal_version'] == 'v402'
    hits = []
    for film, data in plan['films'].items():
        for segment in data['segments']:
            for i, cue in enumerate(segment['cues']):
                for lang, text in cue.items():
                    if isinstance(text, str) and (('gate' in text.lower() and 'flag' in text.lower()) or ('gate' in text.lower() and 'bandeira' in text.lower()) or ('porte' in text.lower() and 'indicateur' in text.lower()) or ('门控' in text and '标志' in text)):
                        hits.append({'film': film, 'segment_key': segment['key'], 'segment_index': segment['index'],
                                     'segment_start': segment['start'], 'segment_end': segment['end'],
                                     'cue_index': i, 'language': lang, 'text': text})
    assert hits, 'No stop phrase found; inspect other conditions before any render'
    subtitle_hits = []
    for p in sorted((V / 'subs').rglob('*.vtt')):
        for i, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
            if ('gate' in line.lower() and ('flag' in line.lower() or 'bandeira' in line.lower())) or ('porte' in line.lower() and 'indicateur' in line.lower()) or ('门控' in line and '标志' in line):
                subtitle_hits.append({'path': str(p), 'line': i, 'text': line, 'sha256': pin(p)['sha256']})
    seal = read(N / 'um_absoluto_selo.json')
    actual_program = pin(N / 'um.py')
    assert actual_program['sha256'] == seal['sha256']['um.py']
    scope = {
        'request_id': REQUEST, 'status': 'STOP_GATE_NARRATION_REQUIRES_MANAGEMENT',
        'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'actor': ACTOR, 'mission_reference': str(REF), 'order': pin(ORDER),
        'trigger': 'Se a V7 tiver alguma frase sobre as bandeiras do gate, PARE e diga qual: nada disso entra sem a gerência.',
        'existing_narration_plan': pin(plan_path), 'existing_templates': pin(V / 'audio/script_templates.json'),
        'phrases': hits, 'subtitle_occurrences': subtitle_hits,
        'current_source': {'version': seal['um_version'], 'timestamp': seal['timestamp'], 'program': actual_program, 'seal': pin(N / 'um_absoluto_selo.json')},
        'source_version_matches_adendo': seal['um_version'] == 'v403',
        'preserved_v402_pointer': pin(V.parent / 'PUBLIC_DELIVERY_V7.json'),
        'preserved_v402_manifest': pin(V / 'PUBLIC_DELIVERY_V7.json'),
        'other_numeric_comparison': 'NOT_RUN_AFTER_MANDATORY_GATE_PHRASE_STOP',
        'um_imported_or_executed': False, 'new_render_count': 0, 'new_tts_requests': 0,
        'new_tts_cost_incurred': 0, 'tts_cost_estimate': 'DEFERRED_UNTIL_MANAGEMENT_DECIDES_THE_GATE_TEXT',
        'public_manifest_reemitted': False, 'publication_performed': False,
        'next_action': 'Gerência decide o texto das frases do gate e autoriza a continuidade; então comparar demais números, estimar eventual TTS antes de enviá-lo e executar o único render autorizado.'
    }
    create(F / 'GATE_NARRATION_STOP.json', scope)
    create(F / 'RESULTADO_CANDIDATO.json', scope)
    print(json.dumps({'status': scope['status'], 'phrases': hits, 'subtitle_occurrences': len(subtitle_hits), 'source': seal['um_version']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
