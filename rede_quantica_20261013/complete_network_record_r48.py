"""Resume only the rejected map registration; preserve all R48 evidence bytes."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT


def main():
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    failed = OUT / 'MAP_RECEIPT_PROGRESS_R48.json'
    refusal = json.loads(failed.read_bytes())
    assert refusal['exit_code'] != 0
    assert 'confirmou cancelame' in refusal['result']['erro']
    progress, memory = OUT / 'PROGRESS_R48.json', OUT / 'MEMORY_PROGRESS_R48.json'
    m = json.loads(memory.read_bytes())
    assert pin(progress) == m['evidence']
    for s in m['surfaces']:
        original = Path(s['backup']['path']).read_bytes()
        current = Path(s['surface']['path']).read_bytes()
        assert pin(s['backup']['path']) == s['backup']
        assert current.startswith(original)
        assert len(current) - len(original) == s['append_bytes']
        assert pin(s['surface']['path']) == s['surface']
    current, projected = live.project()
    assert not current['projection']['unresolved_handles']
    entry = json.loads((OUT / 'MAP_ENTRY_PROGRESS_R48.json').read_bytes())
    old = 'leitura oficial confirmou cancelamento'
    assert entry['resultado'].count(old) == 1
    entry['resultado'] = entry['resultado'].replace(old, 'leitura oficial verificou cancelamento')
    revised = OUT / 'MAP_ENTRY_PROGRESS_R48_REGISTRATION_R2.json'
    if revised.exists():
        assert json.loads(revised.read_bytes()) == entry
    else:
        new(revised, entry)
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', revised, '--quem', WHO],
                      'MAP_RECEIPT_PROGRESS_R48_REGISTRATION_R2.json')
    board = reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
                      '--evidencia', progress, memory, '--nota',
                      'R48: sete componentes revisados, 33 listas no trio; criterios integrais preservados.'],
                     'BOARD_PROGRESS_R48.json')
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R48_FINAL_GET')
    cfg = json.loads((OUT / 'R48_REGISTER_INPUT.json').read_bytes())
    result, receipt = live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id='mission_material_progress_r48_20261016',
        changes=dict(records=[dict(id='mission_material_progress_r48_20261016', kind='fact', statute='REAL',
            text='R48: sete componentes revisados, 33 listas no trio. Cortes concretos, Regular, testemunha nao nula e certificado condicionado registrados. Dois pedidos nunca despachados cancelados como supridos. R7/R8 integrais e missao permanecem abertos. M0-M3 implantados; oito alvos reconferidos.',
            sources=[dict(kind='artifact', ref=str(progress), sha256=pin(progress)['sha256'])])],
            flow=dict(handles=state['p']['handles'], phase='actual_trace_and_nonzero_witness_progress',
                      next_action=cfg['next_action']))), 'R48_FINAL_TRANSITION')
    verified, vr = live.call('session_memory.py', dict(operation='verify', reference=str(live.REFERENCE)), 'R48_FINAL_VERIFY')
    completion = OUT / 'PROGRESS_R48_REGISTRATION_COMPLETED.json'
    new(completion, dict(progress=pin(progress), memory=pin(memory), prior_refusal=pin(failed),
        resumed_map_entry=pin(revised), map=mapped, board=board, revision=result['revision'],
        receipt=pin(receipt), verification=pin(vr), recovery_script=pin(Path(__file__)),
        note='Only administrative wording in a new map entry changed; no scientific claim, original evidence, or memory append repeated.',
        full_mission_complete=False))
    print(json.dumps(dict(completion=pin(completion), revision=result['revision'], verify=verified), ensure_ascii=False))


if __name__ == '__main__':
    main()
