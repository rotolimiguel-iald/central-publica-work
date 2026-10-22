"""Pin a source-only extension, then exercise it once; never compose centers."""
from pathlib import Path
import copy,hashlib,importlib.util,json,re,sys,tempfile,time
from datetime import datetime,timezone
from companion_gate_r2 import extract,verify,CompanionError
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj):
    with (HERE/name).open('xb') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False).encode())
def pin(p):return {'path':str(p),'sha256':sha(p)}
def main():
    for name in ['BINDING_COMPANION_R2.json','PLAN_COMPANION_R2.json','RESULT_COMPANION_R2.json']:
        if (HERE/name).exists():raise FileExistsError(name)
    old=json.loads((ROOT/'r5_operations/ACTUAL_GATE_LINK_R1.json').read_text(encoding='utf-8'))
    custody=json.loads((HERE/'CUSTODY_R2.json').read_text(encoding='utf-8'))
    for row in custody['sources']:
        for key in ['raw','derived_text']:
            if sha(row[key]['path'])!=row[key]['sha256']:raise ValueError('CUSTODY_CHANGED')
    readers={}
    for rid,file,enc in [('L1b_sh0es_r25','L1b_arxiv_2509_01667v1.html','utf-8'),('L6_sirenes','L6_ligo_P2400152.html','iso-8859-1')]:
        text=extract((HERE/file).read_bytes(),enc)
        if rid.startswith('L1b'):
            anchor=re.search(r'Combining JWST Cepheid measurements in 19 hosts .*? km/s/Mpc\.',text).group()
            meta={'H0':73.49,'published_sigma':.93,'sigma_transformation':'identity','statistical_likelihood_qualified':False}
        else:
            anchor=next(line for line in text.splitlines() if 'We analyze data from 142' in line)
            meta={'H0':76.6,'sigma_plus':13.,'sigma_minus':9.5,'reported_summary':'posterior median;68.3% credible interval',
                  'sigma_transformation':'DERIVED arithmetic half-width mean; local symmetric Gaussian approximation only',
                  'statistical_likelihood_qualified':False,'not_a_published_sampling_standard_deviation':True}
        readers[rid]={'source':{'relative_path':file,'sha256':sha(HERE/file)},'encoding':enc,'anchor':anchor,'source_metadata':meta}
    manifest={'status':'CANDIDATE_NOT_FROZEN_NOT_ADMITTED','spec_sha256':old['result']['spec_sha256'],
              'ancestor_binding_sha256':old['binding']['sha256'],'readers':readers}
    save('BINDING_COMPANION_R2.json',manifest)
    plan={'tests':['actual_existing_gate_plus_companion','source_one_byte_mutation','source_missing','anchor_short',
                   'anchor_wrong_context','asymmetry_swapped','spec_center_mismatch','ancestor_mismatch','manifest_pin_mismatch','missing_key'],
          'pins':[pin(HERE/'companion_gate_r2.py'),pin(Path(__file__)),pin(HERE/'BINDING_COMPANION_R2.json')],
          'limits':'documentary verification only; local source values are not statistically composed; no D-H act'}
    save('PLAN_COMPANION_R2.json',plan)
    started=datetime.now(timezone.utc).isoformat();tick=time.perf_counter()
    sys.path.insert(0,str(ROOT/'r5_operations/reused_gate'))
    for row in old['copies']:
        if sha(row['copy']['path'])!=row['copy']['sha256']:raise ValueError('OLD_GATE_CHANGED')
    spec=importlib.util.spec_from_file_location('reused_gate',ROOT/'r5_operations/reused_gate/f9_reader_gate_v1x_e1_bytes.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    source=Path(old['binding']['path'])
    gate=module.verify_v1x_binding(source,expected_binding_sha256=old['binding']['sha256'],
         allowed_source_root=source.parents[2]/'ORDEM_018',expected_spec_sha256=old['result']['spec_sha256'])
    output=verify(HERE/'BINDING_COMPANION_R2.json',sha(HERE/'BINDING_COMPANION_R2.json'),gate)
    assert output['n_alvos_declarados']==0 and output['required_sources_admitted'] is False and output['may_open_data'] is False
    checks=[{'name':plan['tests'][0],'pass':True}]
    # Every negative fixture uses a separate temporary copy; real sources are immutable.
    for case in plan['tests'][1:]:
        with tempfile.TemporaryDirectory(prefix='control_',dir=HERE) as tmp:
            root=Path(tmp).resolve();assert root.is_relative_to(HERE.resolve())
            m=copy.deepcopy(manifest);g=copy.deepcopy(gate)
            for r in m['readers'].values():
                f=r['source']['relative_path'];(root/f).write_bytes((HERE/f).read_bytes())
            if case=='source_one_byte_mutation':
                f=root/m['readers']['L1b_sh0es_r25']['source']['relative_path'];f.write_bytes(f.read_bytes()+b' ')
            if case=='source_missing':(root/m['readers']['L6_sirenes']['source']['relative_path']).unlink()
            if case=='anchor_short':m['readers']['L1b_sh0es_r25']['anchor']='73.49'
            if case=='anchor_wrong_context':m['readers']['L1b_sh0es_r25']['anchor']=m['readers']['L1b_sh0es_r25']['anchor'].replace('19 hosts','18 hosts')
            if case=='asymmetry_swapped':m['readers']['L6_sirenes']['source_metadata'].update(sigma_plus=9.5,sigma_minus=13.)
            if case=='spec_center_mismatch':g['spec_snapshot']['leitores']['L1b_sh0es_r25']['H0']=73.18
            if case=='ancestor_mismatch':g['binding_sha256']='0'*64
            if case=='missing_key':del m['readers']['L6_sirenes']['source_metadata']
            f=root/'manifest.json';f.write_text(json.dumps(m),encoding='utf-8')
            try:verify(f,'0'*64 if case=='manifest_pin_mismatch' else sha(f),g)
            except CompanionError as exc:checks.append({'name':case,'pass':True,'refusal':str(exc)})
            else:raise AssertionError('NOT_REFUSED: '+case)
    save('RESULT_COMPANION_R2.json',{'status':'PASS_DOCUMENTARY_EXTENSION_ONLY','started_utc':started,
         'ended_utc':datetime.now(timezone.utc).isoformat(),'seconds':time.perf_counter()-tick,'checks':checks,
         'new_plan':pin(HERE/'PLAN_COMPANION_R2.json'),'result':output,'old_spec_and_binding_edited':False,
         'statistical_execution':False,'operator_admission_created':False})
    print(json.dumps({'passed':len(checks),'result':output},ensure_ascii=False))
if __name__=='__main__':main()
