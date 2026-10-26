"""Read sealed counts, enforce ADENDO B's numerical stop, preserve v400."""
from pathlib import Path
import hashlib, json, os, re, sys
from datetime import datetime, timezone

B = Path(__file__).resolve().parent
W = B.parent
N = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
R = N.parent / 'video_um'
V = R / 'delivery_v7'
T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_B')
sys.path.insert(0, str(W))
import mission
from bootstrap_b import save

def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'path': str(p), 'sha256': digest, 'bytes': p.stat().st_size}

def write_new(p, raw):
    assert not p.exists(), f'Never overwrite a prior result: {p}'
    temp = p.with_suffix(p.suffix + '.tmp')
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw
    os.replace(temp, p)

def main():
    pr = mission.project()
    task = next(t for t in pr['projection']['active'] + pr['projection']['settled'] if t['id'] == 'ADENDO_B')
    check = mission.call({'operation': 'check', **mission.current('codex-video-v7'), 'task_id': 'ADENDO_B', 'lease_id': task['lease']['id'], 'max_chars': 100000})
    assert check['ready']
    save('COMPARISON_PREFLIGHT.json', check)
    seal_path = N / 'um_absoluto_selo.json'
    seal_start = seal_path.read_bytes()
    seal = json.loads(seal_start)
    source_pins = [pin(N / name) for name in ('um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json')]
    for p in source_pins:
        assert seal['sha256'][Path(p['path']).name] == p['sha256'], p
    result_data = json.loads((N / 'um_absoluto.json').read_bytes())
    kernel = json.loads((N / 'tgl_kernel_proof_manifest.json').read_bytes())
    proof = result_data['core']['estatuto_da_prova_v391']['prova_1_kernel']
    protected = [R / 'PUBLIC_DELIVERY_V7.json', V / 'PUBLIC_DELIVERY_V7.json', V / 'data/hud.json', V / 'PROVENANCE_PUBLIC.json', V / 'RENDER_MANIFEST.json']
    before = [pin(p) for p in protected]
    hud = json.loads((V / 'data/hud.json').read_bytes())
    by_id = {x['id']: x for x in hud['items']}
    rows = [
        ('Kernel staircase clean', ['theorems', 'proof_ladder_clean'], by_id['proof_ladder_clean']['value'], proof['n_theorems_clean'], 'um_absoluto.json:/core/estatuto_da_prova_v391/prova_1_kernel/n_theorems_clean'),
        ('Kernel staircase total', ['proof_ladder_total'], by_id['proof_ladder_total']['value'], proof['n_theorems_expected'], 'um_absoluto.json:/core/estatuto_da_prova_v391/prova_1_kernel/n_theorems_expected'),
        ('Formal files', ['n_formal', 'formal_count'], by_id['formal_count']['value'], len(kernel['formal_files_sha256']), 'len(tgl_kernel_proof_manifest.json:/formal_files_sha256)'),
        ('Audited declarations', ['declaration_count'], by_id['declaration_count']['value'], len(kernel['axiom_report']), 'len(tgl_kernel_proof_manifest.json:/axiom_report)'),
    ]
    assert proof['declaracoes_auditadas'] == len(kernel['axiom_report'])
    diffs = [{'label': label, 'hud_ids': ids, 'before': old, 'after': new, 'delta': new-old, 'current_selector': selector} for label, ids, old, new, selector in rows if old != new]
    assert diffs, 'This report is only for the observed STOP condition.'
    stdout = N / ('rodada_' + seal['um_version'] + '_stdout.txt')
    stdout_matches = [{'line': i, 'text': line} for i, line in enumerate(stdout.read_text(encoding='utf-8').splitlines(), 1) if re.search(r'teoremas limpos:\s*' + str(proof['n_theorems_clean']) + '/' + str(proof['n_theorems_expected']), line)]
    assert stdout_matches, 'Current stdout did not corroborate proof count.'
    jobs = []
    for p in sorted((V / 'cinema/render/jobs').glob('*.json')):
        if p.name.endswith('.progress.json'):
            continue
        j = json.loads(p.read_bytes())
        jobs.append({'receipt': str(p), 'id': j.get('id'), 'source': j.get('metadata', {}).get('source'), 'finished_at': j.get('finished_at'), 'encoded': j.get('render', {}).get('encoded'), 'total': j.get('metadata', {}).get('total')})
    current_jobs = [j for j in jobs if j['source'] == seal['um_version']]
    assert not current_jobs, 'Recover existing current-version jobs instead of assuming no execution.'
    assert not pr['projection']['flow'].get('handles'), 'Unresolved handle; recover it before continuing.'
    save('NUMERIC_DIFFERENCES.json', {'status': 'STOP_NUMERIC_CHANGE', 'source': seal['um_version'], 'source_sha256': seal['sha256']['um.py'], 'baseline': pin(V / 'data/hud.json'), 'source_pins': source_pins, 'differences': diffs, 'stdout': pin(stdout), 'stdout_corroboration': stdout_matches, 'method': 'Read-only comparison of displayed documentary kernel counts against hash-verified sealed JSON and proof manifest. No um import, no full candidate HUD generation, no new proof execution.', 'scope': 'Four scalar differences in three displayed quantities. Other film values have not been exhaustively revalidated for this stopped adendum.'})
    save('RENDER_RECOVERY.json', {'jobs': jobs, 'current_version_jobs': current_jobs, 'active_memory_handles': pr['projection']['flow'].get('handles'), 'render_dispatched_this_adendum': False, 'process_inventory': 'CIM access unavailable; no global process-absence claim. Known filesystem receipts and own mission handles inspected.'})
    seal_end = seal_path.read_bytes()
    end = json.loads(seal_end)
    assert seal_end == seal_start, 'Seal changed during diagnosis; report explicit version conflict.'
    after = [pin(p) for p in protected]
    assert before == after, 'Protected delivery bytes changed during diagnosis.'
    save('PRESERVATION.json', {'protected_before': before, 'protected_after': after, 'all_equal': True, 'seal_start': {'version': seal['um_version'], 'source_sha256': seal['sha256']['um.py'], 'sha256': hashlib.sha256(seal_start).hexdigest()}, 'seal_end': {'version': end['um_version'], 'source_sha256': end['sha256']['um.py'], 'sha256': hashlib.sha256(seal_end).hexdigest()}, 'seal_unchanged': True})
    report = [
        '# ORDEM 022 — ADENDO B: parada numérica antes do render',
        '[REAL] Fonte corrente lida e reconferida: ' + seal['um_version'] + ', selo ' + seal['timestamp'] + '.',
        'um.py SHA256: ' + seal['sha256']['um.py'] + '.',
        'Entrega existente: ' + hud['seal_version'] + '; não sobrescrita.',
        'Escada exibida: ' + str(rows[0][2]) + '/' + str(rows[1][2]) + ' → ' + str(rows[0][3]) + '/' + str(rows[1][3]) + '.',
        'Arquivos formais: ' + str(rows[2][2]) + ' → ' + str(rows[2][3]) + '.',
        'Declarações auditadas: ' + str(rows[3][2]) + ' → ' + str(rows[3][3]) + '.',
        'São quatro escalares em três grandezas do HUD; origem e seletores em NUMERIC_DIFFERENCES.json.',
        'A escada nova estava antecipada no adendo; aplica-se a cláusula explícita de PARAR se qualquer número do filme mudar.',
        'Nenhum render B, import de um.py, execução Lean ou nova síntese TTS foi iniciado.',
        'Recibos de render existentes e handles próprios foram recuperados; nenhum job da versão corrente encontrado.',
        'PUBLIC_DELIVERY_V7.json permanece v400, sem reemissão que aparentasse render v401 inexistente.',
        'Selo permaneceu v401 durante o diagnóstico; manifestos, HUD e proveniência v400 preservados por hash.',
        '[OPEN] Gerência a7 decide a continuidade e o tratamento dessas contagens no novo render.',
        'Voz pessoal continua em prévias PT/EN separadas; sua audição não bloqueia o render com as vozes existentes.',
        'Sem publicação, commit/push, alteração de ciência, kernel, Atlas, Nós ou gate.',
    ]
    assert len(report) <= 20
    write_new(T / 'RELATORIO.md', ('\n'.join(report) + '\n').encode('utf-8'))
    out = {
        'status': 'STOPPED_NUMERIC_CHANGE_REQUIRES_MANAGEMENT_DECISION', 'statute': 'REAL',
        'created_at': datetime.now(timezone.utc).isoformat(), 'request_id': '70185653-afa4-4dc0-8127-5518ca979312',
        'unit': 'F0.FILMES_V7_20261024', 'source': seal['um_version'], 'source_sha256': seal['sha256']['um.py'], 'seal_timestamp': seal['timestamp'],
        'rendered_version': hud['seal_version'], 'rendered_source_sha256': hud['seal_pin'], 'render_started': False, 'import_um_executed': False,
        'numeric_differences': diffs, 'full_scientific_revalidation': 'NOT_RUN_AFTER_STOP', 'anchors_all_ok': None,
        'source_order': json.loads((B / 'AUTHORIZATION.json').read_bytes())['source_order'],
        'decision_required': 'Gerência a7 decide como aplicar as mudanças de contagem antes de continuar o render, conforme a cláusula explícita do ADENDO B. A escada 9561/9561 já era mencionada, mas não se presumiu dispensa da parada.',
        'manifest': pin(R / 'PUBLIC_DELIVERY_V7.json'), 'manifest_reissued': False,
        'manifest_note': 'v400 preservada; não rotulada como v401 sem render correspondente.',
        'voice_previews': 'PRESERVED_SEPARATELY_AWAITING_OPERATOR_LISTENING_NOT_A_RENDER_DEPENDENCY',
        'new_tts_calls': 0, 'publication_performed': False, 'own_reference': mission.REF,
        'evidence': [pin(B / name) for name in ('AUTHORIZATION.json', 'NUMERIC_DIFFERENCES.json', 'RENDER_RECOVERY.json', 'PRESERVATION.json')] + [pin(T / 'RELATORIO.md')],
    }
    write_new(T / 'RESULTADO.json', (json.dumps(out, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({'status': out['status'], 'differences': diffs, 'result': pin(T / 'RESULTADO.json'), 'report_lines': len(report)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
