"""Read-only package/runtime verification; writes evidence in release_stage only."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import prepare_release as release


def pinned_json(ref,work):
    path=release.within(Path(ref['path']),work)
    raw=path.read_bytes()
    if release.digest(raw)!=ref['sha256']:raise release.Refusal('Test/evidence pin differs: '+path.name)
    return json.loads(raw)


def main():
    here=Path(__file__).resolve().parent;work=here.parent
    plan_path=here/'install_plan.json';raw=plan_path.read_bytes();plan=json.loads(raw)
    config=release.read_json(here/'FINAL_CONFIG.json')
    state,science=release.inspect(config,work,Path(plan['runtime_root']))
    if state['status']!='READY_FOR_STAGING_FREEZE':raise release.Refusal('Final inputs no longer ready')
    if len(plan['files'])!=18:raise release.Refusal('Wrong frozen file count')
    expected={row['destination']:row for row in state['files']}
    syntax=[]
    for row in plan['files']:
        current=expected[row['destination']]
        for key in ('destination','baseline','sha256','sourcehash','bytes'):
            if row[key]!=current[key]:raise release.Refusal('Frozen plan differs from current pins')
        source=release.within(Path(row['source']),here/'tree')
        data=source.read_bytes()
        if release.digest(data)!=row['sha256']:raise release.Refusal('Frozen tree hash differs')
        if source.suffix=='.py':ast.parse(data);syntax.append(str(source))
    actual_tree={str(path.resolve()) for path in (here/'tree').rglob('*') if path.is_file()}
    if actual_tree!={str(Path(row['source']).resolve()) for row in plan['files']}:
        raise release.Refusal('Unlisted file in release tree')
    if release.digest((here/'SCIENCE_BASELINE.json').read_bytes())!=plan['science_comparison_sha256']:
        raise release.Refusal('Frozen science comparison pin changed')
    if json.loads((here/'SCIENCE_BASELINE.json').read_bytes())!=science:
        raise release.Refusal('Science changed since freeze')
    if plan['receipts']!=state['receipts']:raise release.Refusal('Receipt set changed since freeze')
    backend=release.read_json(work/'backend_stage/BACKEND_R4_HANDOFF.json')
    for evidence in backend['test_results']:
        path=work/'backend_stage'/evidence['receipt']
        if release.digest(path.read_bytes())!=evidence['sha256']:raise release.Refusal('Backend test receipt changed')
    host=release.read_json(work/'host_stage/HOST_FINAL_RECEIPT.json')
    for evidence in [host['tests'],*host['evidence']]:
        path=release.within(Path(evidence['path']),work/'host_stage')
        if release.digest(path.read_bytes())!=evidence['sha256']:raise release.Refusal('Host evidence changed')
    client=release.read_json(work/'client_stage/release_R6/DELIVERY_PREPARED_R6_FINAL.json')
    for evidence in client['tests'].values():pinned_json(evidence,work)
    mobile=pinned_json(client['mobile_workflow_tests'],work)
    routing=release.read_json(work/'routing_stage/REPORT.json')
    run=subprocess.run([sys.executable,'-X','utf8',str(here/'test_prepare_release.py')],
                       capture_output=True,text=True,encoding='utf-8')
    if run.returncode:raise release.Refusal('Preparer regression failed')
    log=(run.stdout+run.stderr).encode('utf-8')
    validation=here/'validation'
    release.atomic_new(validation/'preparer_tests.txt',log)
    summary=dict(status='PINNED_OFFLINE_EVIDENCE_NOT_INDEPENDENT_ACCEPTANCE',
        backend=dict(revision='R4',reported_suite_cases=backend['tests'],evidence=backend['test_results']),
        routing=dict(reported_tests=routing['tests'],reported_exit_code=routing['test_exit_code']),
        host=dict(reported_tests=host['host_tests'],boundary=host['boundary']),
        client=dict(revision='R6_FINAL',reported_assertions=client['assertions'],evidence=client['tests']),
        mobile_runner=dict(prepared_only=True,evidence=client['mobile_workflow_tests'],reported_receipt=mobile),
        preparer=dict(replayed_tests=13,exit_code=run.returncode,log_sha256=release.digest(log)),
        counts_policy='No aggregate sum: cases, assertions and controls may overlap across suites',
        paid_provider_calls_in_this_verification=0,builds=False,push=False,runtime_writes=False)
    summary_raw=json.dumps(summary,ensure_ascii=False,indent=2).encode('utf-8')
    release.atomic_new(validation/'TEST_SUMMARY.json',summary_raw)
    checks=dict(passed=True,status='PASS_MECHANICAL_STAGING_CHECKS_PENDING_PLANCK_REVIEW',
        plan_path=str(plan_path),plan_sha256=release.digest(raw),files=18,unique_destinations=18,
        frozen_tree_matches=True,runtime_baselines_match=True,final_receipt_pins_match=True,
        science_files=len(science['files']),science_preserved=True,science_executed=False,
        python_syntax_files=len(syntax),python_syntax_paths=syntax,
        test_summary_path=str(validation/'TEST_SUMMARY.json'),test_summary_sha256=release.digest(summary_raw),
        independent_review_complete=False,installed=False,runtime_writes=False,builds=False,push=False,
        limitation='Mechanical validation only; Planck must independently review this exact plan hash before any transaction')
    checks_raw=json.dumps(checks,ensure_ascii=False,indent=2).encode('utf-8')
    release.atomic_new(validation/'final_checks.json',checks_raw)
    request=dict(status='AWAITING_INDEPENDENT_PLANCK_REVIEW',recipient_requested='Planck',
        delivery='Local file for parent forwarding; no direct thread handle or external message used',
        reference=str(work/'SESSION_REFERENCE.json'),unit='F9.MIMO_MEDIA_CAPACITY_20261020',
        plan=dict(path=str(plan_path),sha256=release.digest(raw),files=18),
        final_checks=dict(path=str(validation/'final_checks.json'),sha256=release.digest(checks_raw)),
        test_summary=dict(path=str(validation/'TEST_SUMMARY.json'),sha256=release.digest(summary_raw)),
        review_scope=['Exact 18-file plan and current R baselines; no science changes',
            'Owner/generation/conversation scoping; MiMo2/Auto3; upload/delete race and no retry',
            'Full-prefix/history media context, no silent frame cap; dynamic output floor',
            'Single existing wallet/global reservation; no duplicated debits or assumed cache',
            'Typed and legacy inline clients; four JS bytes and two native version files'],
        prohibited_effects='No deployment, build, push or publication requested by this review handoff')
    release.atomic_new(here/'PLANCK_REVIEW_REQUEST.json',json.dumps(request,ensure_ascii=False,indent=2).encode('utf-8'))
    print(json.dumps(dict(status=checks['status'],plan_sha256=checks['plan_sha256'],files=18,
                         science_files=checks['science_files'],final_checks_sha256=release.digest(checks_raw),
                         review_request=str(here/'PLANCK_REVIEW_REQUEST.json'),runtime_writes=False),indent=2))


if __name__=='__main__':main()
