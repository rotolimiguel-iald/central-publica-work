"""Custody completed builds and submit only the R6 component for review."""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(ROOT/'work/memoria_missao_20261016'))
import activate as a
a.ROOT = OUT/'mission_resume_20261016'


def verify(attempt_id, expected, local=False):
    path = OUT/'orbital_rotation/attempts'/attempt_id
    receipt = json.loads((path/'RECEIPT.json').read_bytes())
    assert receipt['exit_code'] == 0
    assert receipt['readonly_dependencies_unchanged'] and receipt['dependency_cache_unchanged']
    checked = {}
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
                p = Path(value['path'])
                actual = hashlib.sha256(p.read_bytes()).hexdigest()
                assert actual == value['sha256'], str(p)
                checked[str(p)] = actual
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)
    walk(receipt)
    walk(json.loads(Path(receipt['dependency_cache']['path']).read_bytes()))
    output = (path/'AXIOMS.txt').read_text(encoding='utf-8')
    declarations = (re.findall(r'^LOCAL_DECL\t([^\t]+)\t([^\n]*)', output, re.M)
                    if local else re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output))
    assert len(declarations) == expected, len(declarations)
    for name, axioms in declarations:
        assert set(x.strip() for x in axioms.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'}, name
    text = Path(receipt['source']['path']).read_text(encoding='utf-8')
    assert not re.search(r'\bsorry\b|^axiom\b', text, re.M)
    return dict(receipt=pin(path/'RECEIPT.json'), source=pin(Path(receipt['source']['path'])),
        exit_code=0, seconds=receipt['seconds'], axioms=dict(declarations),
        checked_files=[dict(path=p,sha256=h) for p,h in checked.items()],
        local_verification=True, independent_rebuild=False,
        readonly_dependencies_unchanged=True, dependency_cache_unchanged=True)


def main():
    v = a.call('mission_cli.py', dict(operation='project',reference=str(a.REF),max_chars=60000), 'R37_CUSTODY_BEFORE')
    for task in ['R6','R8']:
        t = next(x for x in v['projection']['active'] if x['id']==task)
        a.call('mission_cli.py',dict(operation='check',reference=str(a.REF),task_id=task,
            actor=a.ACTOR,lease_id=t['lease']['id'],expected_revision=v['receipt']['revision'],
            projection_sha256=v['projection_sha256']),f'R37_{task}_PREFLIGHT')
    six = verify('20261016T124312_530135Z',16,True)
    eight = verify('20261016T124526_689718Z',2)
    delivery = OUT/'orbital_rotation/PHYSICAL_FOCK_NET_DELIVERY_R2.json'
    new(delivery,dict(unit='F1.FECHO_20261015',requirement='R6',author=a.ACTOR['id'],
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),statute='REAL',
        build=six,criterion='Weyl/CCR/R(K), standard vacuum, Gamma(J), Tomita and modularity on the same Fock realization.',
        scope='Concrete compact Maxwell net. Generic covariance theorem explicitly retains one-particle transport premise; the physical localization is built separately. Does not inhabit the full FockCertificate, supply a scaled trace/PF, derive H3 or identify a patented device.',
        production_modified=False,gate_moved=False))
    stress = OUT/'maxwell_global/REGULAR_STRESS_BOOST_DELIVERY_R3.json'
    new(stress,dict(unit='F1.FECHO_20261015',requirement='R8',author=a.ACTOR['id'],statute='REAL',
        build=eight,scope='Boost covariance of the point stress form on the same regular Fock domain; charge identity and complete MaxwellCertificate remain open.',
        production_modified=False,gate_moved=False))
    v = a.call('mission_cli.py', dict(operation='project',reference=str(a.REF),max_chars=60000), 'R37_CUSTODY_CURRENT')
    handles = list(v['projection']['flow']['handles'])
    statuses = {'20261016T124312_530135Z':'completed','20261016T123049_142793Z':'failed'}
    for ident,status in statuses.items():
        h = next(h for h in handles if h['id']=='build-'+ident)
        h.update(status=status,receipt=str(OUT/'orbital_rotation/attempts'/ident/'RECEIPT.json'))
    ident='20261016T124526_689718Z'
    assert not any(h['id']=='build-'+ident for h in handles)
    handles.append(dict(id='build-'+ident,kind='lean_build',task_id='R8',name='RegularFockStressBoostR3',
        status='completed',pid_at_start=190244,no_repeat=True,
        receipt=str(OUT/'orbital_rotation/attempts'/ident/'RECEIPT.json')))
    a.call('session_memory.py',dict(operation='transition',reference=str(a.REF),actor=a.ACTOR,
        expected_revision=v['receipt']['revision'],event_id='fecho-fock-stress-builds-r37',
        changes=dict(records=[dict(id='fecho-fock-stress-builds-r37',kind='fact',statute='REAL',
            text='R6 PhysicalFockNetRealizationR2: EXIT0, 16 declarations only trio. R8 RegularFockStressBoostR3: EXIT0, two printed declarations only trio. Both completed builds and dependencies verified; R6 to independent review, R8 charge/certificate still open.',
            sources=[a.source(delivery),a.source(stress)])],flow=dict(phase='fock_review_and_remaining_charge',
            next_action='Independent review R6; preserve R7 running identity; complete R8 charge and R4/R5 device bridge.',handles=handles))),
        'R37_HANDLES_TRANSITION')
    v = a.call('mission_cli.py', dict(operation='project',reference=str(a.REF),max_chars=60000), 'R37_R6_SUBMIT_CURRENT')
    task = next(t for t in v['projection']['active'] if t['id']=='R6')
    result = a.call('mission_cli.py',dict(operation='submit',reference=str(a.REF),actor=a.ACTOR,
        expected_revision=v['receipt']['revision'],projection_sha256=v['projection_sha256'],
        event_id='R6-physical-fock-r2-submit',task_id='R6',lease_id=task['lease']['id'],
        evidence=[a.pin(delivery),a.pin(OUT/'orbital_rotation/PhysicalFockNetRealizationR2.lean')]),'R6_R2_SUBMIT')
    print(json.dumps(dict(R6_files=len(six['checked_files']),R8_files=len(eight['checked_files']),
        R6_delivery=str(delivery),R8_delivery=str(stress),submit=result),ensure_ascii=False))


if __name__=='__main__':
    main()
