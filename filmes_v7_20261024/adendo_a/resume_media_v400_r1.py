"""Resume known pre-encode Namespace failure, preserving original worker and assets."""
from pathlib import Path
import ast, copy, inspect, json, os, runpy, sys

A=Path(__file__).resolve().parent
m=runpy.run_path(str(A/'media_v400_worker.py'))
g=m['main'].__globals__
old_args=m['args_for']

def corrected_args(film=None,job=None):
    args=old_args(film,job)
    args.action='film' if film else 'loop'
    return args

def test_contract():
    tree=ast.parse((g['R']/'cinema/media_v7.py').read_text(encoding='utf-8'))
    names={'encode_film','encode_loop','prepare_video','reuse_prepared_video','prepare_assets','validate_delivery'}
    needed={n.attr for fn in tree.body if isinstance(fn,ast.FunctionDef) and fn.name in names
            for n in ast.walk(fn) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='args'}
    args=corrected_args(1,Path('fixture.json'))
    assert not (needed-set(vars(args))),needed-set(vars(args))
    assert args.action=='film' and corrected_args().action=='loop'
    return {'status':'PASS','required_fields':sorted(needed),'actual_helper_api_checked':True,'encoding_executed':False}

def resume_initialize():
    load,pin,verify=g['load'],g['pin'],g['verify']
    check=g['preflight']()
    previous=load(A/'MEDIA_WATCH.json')
    assert previous['status']=='FAILED_STOPPED'
    assert previous['error']=="'Namespace' object has no attribute 'action'"
    assert previous['completed']=={} and previous['prepared']=={}
    assert not list((g['R']/'render/.pipeline').glob('*.lock'))
    old_baseline=load(A/'MEDIA_V400_BASELINE.json')
    g['baseline']=old_baseline
    g['guard']()
    assets=load(A/'ASSETS_V400.json')
    assert assets['status']=='COMPLETE'
    verify(assets['audit'])
    for p in assets['stills']:verify(p)
    audit=load(Path(assets['audit']['file']))
    outputs=[]
    for stage in audit['stages']:
        assert stage['status']=='COMPLETE'
        for p in stage['inputs']+stage['outputs']+[stage['parameters']['script'],stage['parameters']['ffmpeg']]:verify(p)
        assert g['M']['cache_key'](stage['inputs'],stage['parameters'])==stage['key']
        outputs.extend(stage['outputs'])
    assert len(outputs)==25
    history=A/'namespace_failure_r0'
    history.mkdir(exist_ok=False)
    copied=[]
    for name in ['MEDIA_WATCH.json','MEDIA_V400_BASELINE.json','media_v400_worker.py','MEDIA_WORKER.stdout.log',
                 'MEDIA_WORKER.stderr.log','ASSETS_V400.json','ENCODE_ASSETS.json']:
        source=A/name;destination=history/name
        with destination.open('xb') as f:f.write(source.read_bytes())
        assert g['sha'](destination)==g['sha'](source)
        copied.append({'original':pin(source),'preserved':pin(destination)})
    baseline=copy.deepcopy(old_baseline)
    baseline['frozen_files'].append(pin(Path(__file__)))
    baseline['resume']={'original_baseline':pin(A/'MEDIA_V400_BASELINE.json'),'launcher':pin(Path(__file__)),
                        'failure':pin(history/'MEDIA_WATCH.json'),'assets_reused':25,'preflight':check}
    g['baseline']=baseline
    g['BASE']=A/'MEDIA_V400_RESUME_R1_BASELINE.json'
    g['save_original'](g['BASE'],baseline)
    g['timings']=previous['timings']
    g['save_original'](A/'MEDIA_NAMESPACE_REPAIR_R1.json',{
        'status':'VERIFIED_READY_TO_RESUME','source':'v400','source_sha256':baseline['source_sha256'],
        'failure_known_before_encoding':True,'error':previous['error'],
        'correction':'Supply Namespace.action=film to encode_film (loop for non-film arguments).',
        'original_worker_unchanged':True,'original_baseline_unchanged':True,
        'verified_assets_reused':25,'assets_regenerated':False,'preserved':copied,
        'tests':test_contract(),'resume_baseline':pin(g['BASE'])})

if __name__=='__main__':
    if '--self-test' in sys.argv:
        print(json.dumps(test_contract()));sys.exit(0)
    g['args_for']=corrected_args
    g['initialize']=resume_initialize
    source=inspect.getsource(m['main'])
    assert source.count('assets=False')==1
    # Resume checkpoint: verified completed assets are skipped, not regenerated.
    source=source.replace('assets=False','assets=True')
    exec(compile(source,str(Path(__file__))+'::resumed_main','exec'),g)
    g['main']()
