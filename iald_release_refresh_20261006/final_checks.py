"""Pin the memory-only deployment to current tests and independent review."""
from pathlib import Path
import json, ast
from transaction import digest,write_evidence
W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD')
read=lambda p:json.loads(Path(p).read_bytes())

def main():
    plan=read(W/'install_plan.json');s=W/'memory_stage';b=W/'memory_build'
    files={'memory':W/'audit/memory_review.json',
        'local':sorted(b.glob('local_validation_*.json'))[-1],
        'providers':sorted(b.glob('provider_checks_*.json'))[-1],
        'count':Path(read(s/'haiku_runtime/manifest.json')['measurement_receipt'])}
    receipts={k:read(p) for k,p in files.items()}
    for k in ('memory','local','providers'):assert receipts[k]['status']=='PASS',k
    prefix=digest((s/'haiku_prefix.md').read_bytes())
    for k in ('local','providers'):assert receipts[k]['prefix_sha256']==prefix,k
    assert receipts['count']['draft_sha256']==prefix and receipts['count']['budget']['ready']
    assert receipts['count']['budget']['remaining_tokens']>=10000
    for name,pin in receipts['local']['script_hashes'].items():assert digest((b/name).read_bytes())==pin,name
    for name,pin in receipts['providers']['source_pins'].items():assert digest(Path(name).read_bytes())==pin,name
    for name,pin in receipts['memory']['input_pins'].items():assert digest(Path(name).read_bytes())==pin['sha256'],name
    assert plan['memory_review_sha256']==digest(files['memory'].read_bytes())
    for item in plan['files']:
        raw=Path(item['source']).read_bytes();assert digest(raw)==item['sha256'] and len(raw)==item['bytes']
        assert Path(item['destination']).suffix!='.py' or Path(item['destination']).parent!=R
    baseline=read(W/'baseline.json')
    for row in baseline['files']:assert digest((R/row['name']).read_bytes())==row['sha256'],row['name']
    prior=read(read(R/'iald_nucleo_fixo.json')['jev_control']['path']);new=read(W/'control/jev_control_v389.json')
    for key in ('schema','switching','core_record','core_pointer','anchors'):assert prior[key]==new[key],key
    scripts=('transaction.py','prepare_install.py','restart_web.ps1','verify_live.py','record_delivery.py')
    for name in scripts:
        if name.endswith('.py'):ast.parse((W/name).read_bytes())
    report={'passed':True,'plan_sha256':digest((W/'install_plan.json').read_bytes()),
        'test_suites':{'memory_integration':receipts['local']['tests'],'provider_budget':receipts['providers']['tests']},
        'total_tests':receipts['local']['tests']+receipts['providers']['tests'],
        'scientific_review_checks':receipts['memory']['checks_passed'],
        'control_semantics_and_anchors_unchanged':True,'runtime_source_unchanged':True,
        'provider_generation_calls':0,'native_count_requests_total':sum(read(path)['count_requests'] for path in W.glob('count_*.json')),'client_files_changed':False,
        'receipts':{k:{'path':str(p),'sha256':digest(p.read_bytes())} for k,p in files.items()},
        'operational_scripts':{name:digest((W/name).read_bytes()) for name in scripts},
        'memory_builder_scripts':{str(p):digest(p.read_bytes()) for p in b.glob('*.py')}}
    write_evidence(W/'validation/final_checks.json',report)
    print(json.dumps({k:report[k] for k in ('passed','plan_sha256','total_tests','scientific_review_checks')}))
if __name__=='__main__':main()
