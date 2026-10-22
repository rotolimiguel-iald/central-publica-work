"""Register one material stage; preserve complete criteria and all live handles."""
import datetime as dt
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg
from custody_fock_stress_r37 import verify

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'mission_material_progress_r51_20261016'


def main():
    target = OUT / 'PROGRESS_R51.json'
    if target.exists():
        raise RuntimeError('Existing immutable result: recover, never overwrite')
    config_path = Path(sys.argv[1]).resolve()
    cfg = json.loads(config_path.read_bytes())
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, projected = live.project()
    for task_id in ['R7', 'R8']:
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=task_id, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R51_RECORD_CHECK_'+task_id)
    components, custody = [], []
    for item in cfg['components']:
        attempt, count, folder, review = item
        d = OUT/'orbital_rotation/attempts'/attempt
        r = json.loads((d/'RECEIPT.json').read_bytes())
        assert r['exit_code'] == 0 and r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
        source = OUT/folder/Path(r['source']['path']).name
        assert pin(source)['sha256'] == pin(r['source']['path'])['sha256'] == r['source']['sha256']
        axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", (d/'AXIOMS.txt').read_text(encoding='utf-8'))
        assert len(axioms) == count
        assert all(set(a.strip() for a in text.split(',') if a.strip()) <=
                   {'propext', 'Classical.choice', 'Quot.sound'} for _, text in axioms)
        rp = OUT/'mission_review_20261016'/review
        reviewed = json.loads(rp.read_bytes())
        assert reviewed['verdict'].startswith('PASS')
        assert reviewed.get('requirement_satisfied') is not True
        components.append(dict(source=pin(source), build=pin(d/'RECEIPT.json'),
            review=pin(rp), axiom_lists=count, seconds=r['seconds'], full_requirement_accepted=False))
        custody.append(verify(attempt, count))
    custody_path = OUT/'COMPONENT_CUSTODY_R51.json'
    new(custody_path, dict(statute='REAL', components=custody, full_requirement_accepted=False))
    state, fetched = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R51_RECORD_GET')
    failures = []
    for stamp in cfg['failed_attempts']:
        p = OUT/'orbital_rotation/attempts'/stamp/'RECEIPT.json'
        r = json.loads(p.read_bytes())
        assert r['exit_code'] != 0
        h = next(x for x in state['p']['handles'] if x['id'] == 'build-'+stamp)
        assert h['status'] == 'failed'
        failures.append(dict(id=stamp, receipt=pin(p), exit_code=r['exit_code']))
    memory_delivery = ROOT/'work/memoria_missao_20261016/terminal_records_e3/DELIVERY_E3.json'
    installed = json.loads(memory_delivery.read_bytes())['installed_current']
    assert all(pin(x['path'])['sha256'] == x['sha256'] for x in installed)
    count = sum(x['axiom_lists'] for x in components)
    claims = cfg['claims']
    extra = [pin(p) for p in cfg.get('extra_evidence', [])]
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        at=dt.datetime.now(dt.timezone.utc).isoformat(), claim=claim,
        reference=pin(live.REFERENCE), revision=state['revision'], components=components,
        reviewed_axiom_lists=count, failed_attempts=failures, claims=claims,
        installed_memory=installed, pending_handles=current['projection']['unresolved_handles'],
        evidence=[pin(config_path), pin(projected), pin(fetched), pin(custody_path), pin(memory_delivery), pin(Path(__file__)), *extra],
        full_mission_complete=False, providers_called=False, production_science_modified=False, gate_moved=False)
    new(target, progress)
    text = '\n\n## 16/10/2026 — R51: extensao ciclica, projecoes e Wick no mesmo Fock\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicacao F1.FECHO_20261015.\n'
    text += f'\n[REAL] {len(components)} componentes compilados e revisados; {count} listas de axiomas somente no trio. Nenhum aceite integral de R7/R8.\n'
    text += ''.join(f'\n[{x["statute"]}] {x["text"]}\n' for x in claims)
    text += f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R51.txt', text)
    mem = OUT/'MEMORY_PROGRESS_R51.json'
    new(mem, dict(claim=claim, evidence=pin(target), surfaces=[append_bytes(p, text, MARKER) for p in surfaces]))
    entry = OUT/'MAP_ENTRY_PROGRESS_R51.json'
    new(entry, dict(tipo='ANOTACAO', rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='R51: extensao ciclica e fornecedores concretos com alcances separados',
        resultado=' '.join(x['text'] for x in claims), estatuto='REAL — componentes; OPEN — missao integral',
        status='EM_CURSO', veredito='COMPONENTS_PASS_WITH_SCOPE_MISSION_NOT_COMPLETE',
        defeito=cfg['remaining'], proximo_passo=cfg['next_action'], onde=str(OUT),
        artefatos=[str(target), str(mem)], olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO], 'MAP_RECEIPT_PROGRESS_R51.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',target,mem,
        '--nota',f'R51: {len(components)} componentes revisados, {count} listas no trio; criterios integrais preservados.'], 'BOARD_PROGRESS_R51.json')
    state,_ = live.call('session_memory.py', dict(operation='get',reference=str(live.REFERENCE)), 'R51_FINAL_GET')
    r, receipt = live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id=MARKER,
        changes=dict(records=[dict(id=MARKER, kind='fact', statute='REAL',
            text=f'R51: {len(components)} componentes revisados, {count} listas no trio. Extensao ciclica e fornecedores concretos registrados; R7/R8 integrais e missao permanecem abertos. M0-M3 implantados e oito alvos reconferidos. Fontes e pendencias no recibo.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],
            flow=dict(handles=state['p']['handles'],phase='actual_cyclic_trace_finite_split_and_local_wick',next_action=cfg['next_action']))), 'R51_FINAL_TRANSITION')
    verified, vr = live.call('session_memory.py',dict(operation='verify',reference=str(live.REFERENCE)), 'R51_FINAL_VERIFY')
    print(json.dumps(dict(progress=pin(target),revision=r['revision'],receipt=str(receipt),verify_receipt=str(vr),verify_ok=verified.get('ok')),ensure_ascii=False))


if __name__ == '__main__':
    main()
