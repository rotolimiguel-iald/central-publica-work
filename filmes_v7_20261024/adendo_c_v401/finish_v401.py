"""Collate the validated v401 film construction without publishing it."""
from pathlib import Path
import hashlib, json, os, sys, time

C = Path(__file__).resolve().parent
W = C.parent
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'
T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_C')
sys.path.insert(0, str(W))
import mission
from coverage_validation import validate_samples
from finalizer_guards import (validate_frozen_data, validate_replay, validate_audio,
                              validate_public_pointer, validate_final_receipts)

def read(p): return json.loads(p.read_bytes())
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def pin(p): return {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
def atomic(p, raw):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        old = p.read_bytes()
        if old == raw: return
        backup = p.with_name(p.name + '.bak_' + str(time.time_ns()))
        backup.write_bytes(old); assert backup.read_bytes() == old
    q = p.with_suffix(p.suffix + '.tmp'); q.write_bytes(raw); assert q.read_bytes() == raw and raw; os.replace(q, p)
def save(p, d): atomic(p, (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode())

def main():
    pr = mission.project()
    task = next(t for t in pr['projection']['active'] + pr['projection']['settled'] if t['id'] == 'ADENDO_C_V401')
    assert mission.call({'operation': 'check', **mission.current('codex-video-v7'), 'task_id': task['id'], 'lease_id': task['lease']['id'], 'max_chars': 100000})['ready']
    validate_frozen_data(C, V, N)
    seal = read(N / 'um_absoluto_selo.json'); capture = read(C / 'SOURCE_CAPTURE.json')
    h = read(V / 'data/hud.json'); m = read(V / 'PUBLIC_DELIVERY_V7.json'); pointer = read(V.parent / 'PUBLIC_DELIVERY_V7.json')
    assert seal['um_version'] == h['seal_version'] == m['source'] == m['version'] == pointer['source'] == 'v401'
    source = seal['sha256']['um.py']
    assert h['seal_pin'] == m['source_sha256'] == pointer['source_sha256'] == capture['source_sha256'] == source
    assert pin(N / 'um_absoluto_selo.json') == capture['canonical_seal'], 'STOP: seal advanced since preparation'
    assert pointer['sha256'] == sha(V / 'PUBLIC_DELIVERY_V7.json')
    validate_public_pointer(m, pointer, V)
    validate_replay(V, source)
    validate_final_receipts(C, V, source)
    assert read(C / 'FINAL_MAKE.json')['status'] == 'PASS'
    assert read(C / 'MEDIA_WATCH.json')['status'] == 'COMPLETE'
    numeric = read(C / 'PARENT_NUMERIC_REVIEW.json')
    assert numeric['status'] == 'PASS_WITH_SCOPE' and numeric['unexpected_differences'] == []
    assert read(C / 'FINAL_PLAYER_V401.json')['status'] == 'PASS_OBSERVED_UI'
    prov = read(V / 'PROVENANCE_PUBLIC.json')
    assert prov['anchors_all_ok'] and len(prov['anchors']) >= 64
    browser = read(V / 'replay/TEST_BROWSER.json'); offline = read(V / 'replay/TEST_OFFLINE.json')
    assert browser['status'] == offline['status'] == 'PASS'
    assert browser['source_sha256'] == offline['source_sha256'] == source and all(c['ok'] for c in browser['checks'])
    assert offline['tests'] == 13
    audio = validate_audio(C, V, source)
    assert read(V / 'render/MEDIA_VALIDATION.json')['status'] == 'PASS'
    old_sources = [read(C / 'baseline_manifest_v400/PUBLIC_DELIVERY_V7.json')['source_sha256'], read(W / 'adendo_a/baseline_v399/source/um_absoluto_selo.json')['sha256']['um.py']]
    old_pin_hits = []
    public_bytes = 0
    for e in m['public_files']:
        p = V / e['path']; assert p.resolve().is_relative_to(V.resolve())
        assert p.stat().st_size == e['bytes'] and sha(p) == e['sha256'], e['path']
        assert not any(k in p.parts for k in ['private', 'source', 'cache', 'voice_sample', 'voice_test'])
        assert '.bak_' not in p.name and '.tmp' not in p.name
        raw = p.read_bytes(); public_bytes += len(raw)
        for old in old_sources:
            if old[:8].encode() in raw: old_pin_hits.append({'path': e['path'], 'old_pin': old})
    assert not old_pin_hits, old_pin_hits
    manifest = read(V / 'RENDER_MANIFEST.json'); jobs, coverage, costs = {}, {}, {}
    for kind, j in manifest['jobs'].items():
        assert j['metadata']['source'] == 'v401' and j['metadata']['source_sha256'] == source
        assert j['render']['encoded'] == j['metadata']['total'] == round(j['metadata']['duration'] * 60)
        timeline = read(V / f"data/film{j['metadata']['film']}.json")
        duration = timeline['total_seconds'] if j['metadata']['film'] == 1 else timeline['duration']
        coverage[kind] = validate_samples(kind, j['metadata'], j['render']['samples'], duration)
        costs[kind] = {k: j['render'][k] for k in ['elapsed_s', 'scene_cpu_submit_seconds', 'overlay_cpu_seconds']}
        jobs[kind] = {'job_sha256': j['job_sha256'], 'frames': j['render']['encoded'], 'metadata': j['metadata']}
    evidence = [C / name for name in ['AUTHORIZATION.json', 'SOURCE_CAPTURE.json', 'NUMERIC_COMPARISON.json', 'PARENT_NUMERIC_REVIEW.json', 'DATA_READY.json', 'DELIVERY_DATA.json', 'AUDIO_READY.json', 'DELIVERY_E.json', 'FINAL_MAKE.json', 'FINAL_PLAYER_V401.json']]
    evidence += [V / name for name in ['replay/TEST_BROWSER.json', 'replay/TEST_OFFLINE.json', 'replay/DELIVERY_ADENDO_C_V401.json', 'audit/DELIVERY_D_V401.json', 'render/MEDIA_VALIDATION.json', 'data/STDOUT_LINES.json', 'RENDER_MANIFEST.json', 'make_v7.py']]
    result = {'status': 'BUILT_FOR_MANAGEMENT_REVIEW', 'source': 'v401', 'source_sha256': source, 'seal_timestamp': h['seal_timestamp'], 'mission_reference': str(W / 'SESSION_REFERENCE.json'), 'request_id': '875c5047-6702-4b45-8c97-d796f3ece19e', 'delivery': pin(V.parent / 'PUBLIC_DELIVERY_V7.json'), 'manifest': pin(V / 'PUBLIC_DELIVERY_V7.json'), 'public_files': len(m['public_files']), 'public_bytes': public_bytes, 'anchors': len(prov['anchors']), 'anchors_all_ok': True, 'authorized_kernel_counts': numeric['expected_counts_read_from_sealed_sources'], 'unexpected_numeric_differences': [], 'public_old_pin_occurrences': old_pin_hits, 'jobs': jobs, 'coverage': coverage, 'costs': costs, 'evidence': [pin(p) for p in evidence], 'personal_voice': 'Separate PT/EN previews awaiting operator listening; excluded from films.', 'publication': 'NOT_PERFORMED', 'historical_stop': pin(Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_B\RESULTADO.json')), 'limitations': ['Construction awaits management integration/publication.', 'No new Lean compilation, empirical test or change of scientific gate.', 'Full-frame render; CPU submission/overlay timings are not isolated GPU costs.', '64 provenance checks are not independent proofs; browser replay retains documentary fields not recomputed.', 'Integrated-GPU performance and subjective pronunciation were not newly measured.']}
    assert pin(N / 'um_absoluto_selo.json') == capture['canonical_seal'], 'STOP: seal advanced during final verification'
    save(C / 'CONSTRUCTION_DELIVERY_V401.json', result); save(T / 'RESULTADO.json', result)
    counts = result['authorized_kernel_counts']
    lines = ['# ORDEM 022 — ADENDO C · filmes V7, fonte v401',
        '[REAL] Construção concluída para revisão, integração por hash e publicação pela gerência a7.',
        f"Fonte v401: {source}; selo {h['seal_timestamp']}, relido antes da entrega.",
        f"Contagens autorizadas: escada {counts['proof_ladder_clean']}/{counts['proof_ladder_total']}; arquivos {counts['formal_count']}; declarações {counts['declaration_count']}.",
        'Nenhuma outra divergência numérica admitida; metadados e posições de fonte reancorados.',
        f"{len(prov['anchors'])} âncoras aprovadas; stdout v401 e recorte Python exato com hashes atuais.",
        'Replay offline e controles de adulteração aprovados; recibos distinguem campos calculados de documentais.',
        'Dois filmes:224s/360s, captura4K60; loop16s; desenho e duração preservados.',
        f"Narração EN/PT: {audio['counts']['new_v401_units']} unidades novas da contagem e {audio['counts']['reused_v400_units']} reutilizadas, conforme recibo de áudio.",
        'Quatro idiomas de legendas e capítulos conferidos; prévias pessoais continuam fora dos filmes.',
        f"{len(m['public_files'])} arquivos públicos pinados;16vídeos e25imagens validados; masters4K privados.",
        'Nenhuma ocorrência dos pins antigos nos arquivos públicos; entrega v400 preservada em baseline/backups.',
        f"Captura: F1 {costs['film1']['elapsed_s']:.3f}s; F2 {costs['film2']['elapsed_s']:.3f}s; loop {costs['loop']['elapsed_s']:.3f}s.",
        'Custos CPU por camada no RESULTADO; não se alega render incremental ou custo GPU isolado.',
        'Player, troca EN/PT, busca temporal, capítulos e cartão final verificados na interface local.',
        'Limites: sem novo benchmark GPU integrada ou audição subjetiva integral; nenhuma nova prova científica.',
        f"PUBLIC_DELIVERY_V7.json reemitido; SHA256 {result['delivery']['sha256']}.",
        'ADENDO B preservado; sem publicação, commit/push ou alteração de Nós, Atlas, espelho, site e gate.']
    assert len(lines) <= 20; atomic(T / 'RELATORIO.md', ('\n'.join(lines) + '\n').encode())
    print(json.dumps({'status': result['status'], 'files': result['public_files'], 'result': pin(T / 'RESULTADO.json'), 'report_lines': len(lines)}))

if __name__ == '__main__': main()
