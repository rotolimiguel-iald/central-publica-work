"""Submit the authorized v402 construction; never accept or publish it."""
from pathlib import Path
import hashlib, json, os, sys, time
C = Path(__file__).resolve().parent
sys.path.insert(0, str(C.parent))
import mission
from bootstrap import cli, REF, ACTOR
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'
T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_E')
def read(p): return json.loads(p.read_bytes())
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def pin(p): return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}
def save(p, d):
    raw = (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode()
    if p.exists():
        old = p.read_bytes()
        if old == raw: return
        backup = p.with_name(p.name + '.bak_' + str(time.time_ns()))
        backup.write_bytes(old); assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp'); tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw and raw; os.replace(tmp, p)
def seal_guard():
    capture = read(C / 'SOURCE_CAPTURE.json')
    assert pin(N / 'um_absoluto_selo.json') == capture['canonical_seal'], 'STOP: seal advanced'
    assert read(N / 'um_absoluto_selo.json')['um_version'] == 'v402'
    return capture['source_sha256']
def validate_integration_review(review, source, submitter, result, construction):
    """Bind a distinct review to the exact completed construction, without accepting it."""
    assert review['status'] == 'PASS_WITH_SCOPE'
    assert review['source'] == 'v402' and review['source_sha256'] == source
    reviewer = review.get('reviewer', review.get('actor'))
    if isinstance(reviewer, dict): reviewer = reviewer.get('id')
    assert isinstance(reviewer, str) and reviewer.strip() and reviewer != submitter, 'Distinct reviewer required'
    assert result.read_bytes() == construction.read_bytes(), 'Construction and tunnel result differ'
    expected = sha(result); targets = {result.resolve(), construction.resolve()}
    matches = []
    def walk(value):
        if isinstance(value, dict):
            path = value.get('path', value.get('file'))
            if isinstance(path, str) and Path(path).resolve() in targets and 'sha256' in value:
                assert value['sha256'] == expected, 'Review pins another construction'
                if 'bytes' in value: assert value['bytes'] == result.stat().st_size
                matches.append(path)
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(review)
    assert matches, 'Review must pin RESULTADO.json or CONSTRUCTION_DELIVERY_V402.json'
def main():
    source = seal_guard()
    result = T / 'RESULTADO.json'; d = read(result)
    assert d['status'] == 'BUILT_FOR_MANAGEMENT_REVIEW'
    assert d['source'] == 'v402' and d['source_sha256'] == source
    assert d['manifest']['sha256'] == sha(V / 'PUBLIC_DELIVERY_V7.json')
    review = C / 'FINAL_INTEGRATION_REVIEW.json'; rv = read(review)
    validate_integration_review(rv, source, ACTOR['id'], result, C / 'CONSTRUCTION_DELIVERY_V402.json')
    assert pin(V.parent / 'PUBLIC_DELIVERY_V7.json') == d['delivery'], 'Root pointer changed after reviewed construction'
    for e in d['evidence']:
        assert sha(Path(e['path'])) == e['sha256'], e['path']
    p = mission.project()
    task = next(t for t in p['projection']['active'] + p['projection']['settled'] if t['id'] == 'ADENDO_E_V402')
    evidence = [{'path': str(f), 'sha256': sha(f)} for f in [result, T / 'RELATORIO.md', review, V.parent / 'PUBLIC_DELIVERY_V7.json']]
    if task['status'] == 'review_pending':
        assert task['submitted_by'] == ACTOR['id'] and task['evidence'] == evidence
    else:
        context = {'actor': ACTOR, 'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'], 'task_id': task['id'], 'lease_id': task['lease']['id']}
        assert mission.call({'operation': 'check', **context, 'max_chars': 100000})['ready']
        seal_guard()
        sub = mission.call({'operation': 'submit', **context, 'event_id': 'ordem022-adendo-e-submit-' + sha(result)[:16], 'evidence': evidence, 'note': 'Construção v402 e revisão independente documentadas; aceite final, integração e publicação pela gerência.'})
        save(C / 'SUBMISSION_ADENDO_E.json', sub)
    state = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'get', 'reference': str(REF)})['result']
    handles = state['p']['handles']; manifest = read(V / 'RENDER_MANIFEST.json')
    for kind, r in manifest['jobs'].items():
        matches = [p for p in (V / 'cinema/render/jobs').glob(kind + '_*.json') if sha(p) == r['job_sha256']]
        assert len(matches) == 1
        job = read(matches[0]); assert job['render']['encoded'] == job['metadata']['total']
        assert job['metadata']['source'] == 'v402' and job['metadata']['source_sha256'] == source
        h = next((h for h in handles if h['id'] == job['id']), None)
        if h is None:
            h = {'id': job['id'], 'kind': 'local_render', 'task_id': 'ADENDO_E_V402'}; handles.append(h)
        h.update(status='completed', evidence=str(matches[0]), version='v402')
    assert read(C / 'MEDIA_WATCH.json')['status'] == 'COMPLETE'
    for h in handles:
        if h['id'] in ('v402-adendo-e-pipeline-20261027', 'v402-media-worker-20261027'):
            h.update(status='completed', evidence=str(result), evidence_sha256=sha(result))
    seal_guard()
    transition = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'transition', 'reference': str(REF), 'actor': ACTOR, 'expected_revision': state['revision'], 'event_id': 'ordem022-adendo-e-delivery-' + sha(result)[:16], 'changes': {
        'records': [{'id': 'v402_adendo_e_construction_delivery', 'kind': 'fact', 'statute': 'REAL', 'text': 'ADENDO E concluído tecnicamente: filmes e loop renderizados da fonte v402 com quatro contagens documentais autorizadas; nenhuma outra divergência numérica. Narração EN/PT e quatro legendas com correções D e leitura explicativa das fórmulas por ordem humana; contagens de geração medidas no recibo de áudio. Replay, exportações e player conferidos. Prévias pessoais separadas. Entrega à gerência sem publicação, autoaceite ou mudança do gate; parada B preservada.', 'sources': [{'kind': 'artifact', 'ref': str(result), 'sha256': sha(result)}]}],
        'flow': {'phase': 'v402_construction_submitted_for_management_review', 'next_action': 'Gerência a7 revisa e integra/publica por hash. Operador ouve prévias pessoais PT/EN antes de inclusão; não repetir renders/TTS encerrados.', 'handles': handles}}})
    assert transition['ok'], transition
    save(C / 'TRANSITION_DELIVERY.json', transition)
    route = {'tipo': 'RESULTADO', 'rota_id': 'site.filmes.v7.ordem022', 'dominio': 'SITE_E_PUBLICACAO', 'titulo': 'Filmes V7 da fonte v402 entregues para integração', 'resultado': f"v402; quatro contagens documentais autorizadas; {d['public_files']} arquivos públicos pinados;64verificações de proveniência; nenhuma outra divergência numérica.", 'veredito': 'BUILT_FOR_MANAGEMENT_REVIEW', 'estatuto': 'REAL', 'status': 'EXAMINADA', 'olhou_dados': False, 'defeito': 'Sem novo benchmark GPU integrada ou audição subjetiva integral; prévias pessoais aguardam operador.', 'nao_refazer': 'Reutilizar entrega v402 e caches de áudio verificados. Não repetir render ou TTS encerrados.', 'proximo_passo': 'Gerência a7 revisa, integra por hash e publica.', 'onde': str(V), 'artefatos': [str(result), str(V.parent / 'PUBLIC_DELIVERY_V7.json')], 'refs': [], 'nota': 'Construção operacional, sem alteração de ciência ou gate.'}
    save(C / 'FINAL_ROUTE.json', route)
    print(json.dumps({'status': 'SUBMITTED_NOT_SELF_ACCEPTED', 'revision': transition['result'].get('revision'), 'route': str(C / 'FINAL_ROUTE.json')}, ensure_ascii=False))
if __name__ == '__main__': main()
