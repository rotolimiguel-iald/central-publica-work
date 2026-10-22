"""Bounded review of two publication labels and eight dependent data replacements."""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import ast, hashlib, json, os, sys

W = Path(__file__).resolve().parents[1]
P = W / 'publication_fix'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(path):
    path = Path(path); raw = path.read_bytes()
    inputs[str(path)] = {'sha256': sha(raw), 'bytes': len(raw)}
    return raw


def load(path):
    return json.loads(read(path))


def pin(row):
    raw = read(row['path'])
    assert sha(raw) == row['sha256'] and len(raw) == row['bytes']
    return raw


def main():
    sys.path.insert(0, str(W))
    import task
    project = task.project()
    t = next(x for x in project['projection']['active'] if x['id'] == 'publication_label_fix')
    assert t['status'] == 'review_pending'
    delivery_path = P / 'DELIVERY_PREPARED.json'
    assert t['evidence'] == [{'path': str(delivery_path), 'sha256': sha(read(delivery_path))}]
    delivery = load(delivery_path)
    for key in ['exact_two_label_test','core_diff','new_core','native_prefix','bindings','public_count_receipts','plan','validation','controls','baselines']:
        pin(delivery[key])
    exact = load(P / 'EXACT_LABEL_TEST.json')
    old = pin(exact['old_core']); new = pin(exact['new_core'])
    expected = old; commit = delivery['commit']
    substitutions = [('publicação pendente'.encode(), 'publicação verificada'.encode()), (b'commit PUBLICATION_PENDING', ('commit '+commit).encode())]
    for before, after in substitutions:
        assert old.count(before) == 1
        expected = expected.replace(before, after, 1)
    assert expected == new and len(new) - len(old) == 23
    assert len(exact['edits']) == 2
    for row, (before, after) in zip(exact['edits'], substitutions):
        assert old[row['old_start_byte']:row['old_end_byte']] == before
        assert row['old_utf8'].encode() == before and row['new_utf8'].encode() == after
    live_manifest = load(R / 'iald_nucleo_fixo.json')
    staged = load(P / 'staging/manifest_staged.json')
    install = load(P / 'staging/manifest_install.json')
    for cfg in [staged, install]:
        assert {k:v for k,v in cfg.items() if k!='operational_core'} == {k:v for k,v in live_manifest.items() if k!='operational_core'}
        assert {k:v for k,v in cfg['operational_core'].items() if k not in ['path','sha256']} == {k:v for k,v in live_manifest['operational_core'].items() if k not in ['path','sha256']}
        assert cfg['operational_core']['sha256'] == sha(new)
    for row in load(P / 'BASELINES.json')['files']:
        pin(row)
    queue_active = W.parents[1] / 'Chatgpt/IALD_ORQUESTRACAO_20260923/state/canonical_memory/ACTIVE.json'
    queue_before = read(queue_active)
    plan = load(P / 'install_plan.json')
    assert len(plan['files']) == 8 and Path(plan['files'][-1]['destination']) == R / 'iald_nucleo_fixo.json'
    seen = set()
    for row in plan['files']:
        source, dest = Path(row['source']).resolve(), Path(row['destination']).resolve()
        assert source.is_relative_to(P.resolve()) and dest.is_relative_to(R.resolve())
        assert dest.suffix != '.py' and str(dest).casefold() not in seen
        seen.add(str(dest).casefold())
        assert sha(read(source)) == row['sha256']
        assert (sha(read(dest)) if dest.exists() else None) == row['baseline']
    controls = load(P / 'CONTROLS_COPIED.json')
    for row in controls['files']:
        assert pin(row['origin']) == pin(row['copy'])
        assert read(W / Path(row['copy']['path']).name) == pin(row['copy'])
        ast.parse(pin(row['copy']))
    post = W / 'verify_publication_fix_installed.py'
    post_raw = read(post); ast.parse(post_raw)
    post_text = post_raw.decode()
    assert "effective={**old['files'],**new['files']}" in post_text
    assert "(P/'installed_verification.json').open('x'" in post_text
    assert "queue_reactivated':False" in post_text
    layered_files = dict(load(W / 'deployment.json')['files'])
    layered_files.update({row['destination']: row['sha256'] for row in plan['files']})
    assert len(layered_files) == 1450
    assert Path(exact['old_core']['path']).is_file() and Path(install['operational_core']['path']) != Path(exact['old_core']['path'])
    nativecounts = load(P / 'NATIVE_COUNTS_COMPLETE.json')
    assert nativecounts['public_count_requests'] == 6 and nativecounts['generation_requests'] == 0 and not nativecounts['operator_context_egress']
    assert nativecounts['publication_receipt_sha256'] == sha(read(P / 'PUBLICATION_REFERENCE.json'))
    reference = load(P / 'PUBLICATION_REFERENCE.json')
    publication = json.loads(pin(reference['publication']))
    assert publication['commit'] == commit

    def guard(event,args):
        if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
            raise RuntimeError('Offline bounded publication review')
        if event=='open':
            path,mode,flags=args
            if isinstance(path,int): return
            path=Path(os.fsdecode(path)).resolve()
            if path.name.lower() in {'.env','iald_stack_v7.py','iald_psion_state.json'}: raise RuntimeError('Confidential source refused')
            writing=isinstance(mode,str) and any(c in mode for c in 'wax+') or isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)
            if writing and not (path.is_relative_to(W/'review') or path==P/'validation/review_final.json' or path==P/'validation/review_final.json.tmp'):
                raise RuntimeError('No mutation of builder or production data')
    sys.addaudithook(guard)
    sys.path.insert(0,str(R))
    from claude_profiles import HAIKU,SONNET,reasoning_parameters
    from claude_native_counter import native_count_parameters
    from claude_context_snapshot import native_tools_sha256,load_snapshot,verify_native_tools
    from claude_memory_package import load_package
    from iald_motor_claude import converter_pedido
    import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory,iald_native_memory,iald_memoria_canonica as cm,iald_release_binding
    tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
    identity=iald_release_binding.load_release(P/'staging/manifest_staged.json').identity
    assert identity==delivery['new_deployment']
    assert {k:v for k,v in identity.items() if k!='operational_core_sha256'}=={k:v for k,v in delivery['old_deployment'].items() if k!='operational_core_sha256'}
    counts={}
    for folder,profile in [('haiku55',HAIKU),('shared',HAIKU),('sonnet_public',SONNET)]:
        root=P/'packages'/folder;prefix=read(root/'prefix.md').decode();rc=load(root/'native_count.json');pkg=load(root/'manifest.json')
        assert rc['deployment']==pkg['deployment']==identity and rc['prefix_sha256']==pkg['prefix_sha256']==sha(prefix.encode())
        assert rc['budget']==pkg['budget']==delivery['counts'][folder]['budget']
        assert not rc['operator_context_sent'] and not rc['private_atlas_included'] and rc['model']==profile.model
        if folder!='sonnet_public':
            live=R/'.iald_runtime'/('haiku55' if folder=='haiku55' else 'haiku')/'prefix.md'
            previous=read(live)
            assert previous.count(old)==1 and prefix.encode()==previous.replace(old,new,1).replace(sha(old).encode(),sha(new).encode(),1)
            load_package(root,canonical_manifest=P/'staging/manifest_staged.json',expected_model=HAIKU.model)
        cfg=SimpleNamespace(modelo=profile.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium' if profile is HAIKU else 'high')
        wire=converter_pedido(cfg,{'model':profile.model,'max_completion_tokens':16384,'messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v394.'}],'tools':tools},prefixo=prefix)
        wire.update(reasoning_parameters(profile.model,16384))
        minimal={'model':profile.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],**reasoning_parameters(profile.model,16384)}
        for phase,request,amount in [('permanent',minimal,rc['budget']['permanent_tokens']),('whole_request',wire,rc['budget']['request_input_tokens'])]:
            intentpath=root/(phase+'_count_intent.json');intent=load(intentpath);returned=load(root/(phase+'_count_result.json'))
            assert sha(json.dumps(native_count_parameters(request),sort_keys=True,ensure_ascii=False).encode())==intent['request_sha256']
            assert intent['model']==profile.model and returned['input_tokens']==amount and returned['intent_sha256']==sha(read(intentpath))
        assert pkg['tools_sha256']==native_tools_sha256(wire['tools'][:7])
        assert pkg['counted_scoped_tools_sha256']==rc['native_tools_sha256']==sha(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode())
        assert rc['budget']['ready']
        counts[folder]={k:rc['budget'][k] for k in ['model','permanent_tokens','request_input_tokens','remaining_tokens']}
    os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
    catalog=iald_kernel.KernelCatalog(staged['active_cluster']['kernel_bundle'],staged['active_cluster']['kernel_verification'])
    public,metadata=cm.CanonicalMemory(W.parents[1]/'memory/TGL_ATLAS.md','nucleo_kernel',nucleus_manifest=P/'staging/manifest_staged.json').prompt('',catalog,public=True)
    assert sha(public.encode())==sha(read(P/'packages/sonnet_public/prefix.md')) and not metadata['private_atlas_included']
    native,nid=iald_native_memory.load_native_context(P/'staging/manifest_staged.json',catalog)
    assert nid==identity and native.encode()==read(P/'native_prefix.md')
    assert sha(read(queue_active))==sha(queue_before)
    for path,row in inputs.items():assert sha(Path(path).read_bytes())==row['sha256'],path
    report={'verdict':'PASS_PUBLICATION_LABEL_FIX_PREPARED_NOT_APPLIED','criterion_satisfied':True,'reviewer':'codex-v394-reviewer','reference':str(task.REF),'task_id':'publication_label_fix','criterion':t['criterion'],'reviewed_submission':t['evidence'],'mission_revision':project['receipt']['revision'],'checked_at':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'resolved_medium_scope':'Exactly two false operational publication labels corrected in prepared core; live correction remains unverified until application and two terminal retest turns. Other scientific PENDING labels and articles preserved.','core_bytes_delta':23,'core_edits':exact['edits'],'plan_sha256':sha(read(P/'install_plan.json')),'planned_files':8,'effective_layered_files_after_apply':1450,'new_identity':identity,'counts':counts,'six_native_intents_match_rebuilt_requests_offline':True,'queue_ACTIVE_unchanged':True,'findings':[],'controls_static_review':'Exact previously accepted controls; transaction WORK=P, byte backup and stopped-web admission/restart remain required at application. No queue activation or runtime Python replacements in plan.','post_install_verifier':{'path':str(post),'sha256':sha(post_raw),'executed':False},'publication_label_apply_accepted':False,'verify_accepted':False,'production_changed':False,'native_api_calls':0,'pending':['Main publication_label_apply fresh claim/preflight and controlled data-only transaction.','Installed layered verification then two distinct new terminal automatic turns, preserving first terminal test and its publication-label failure.']}
    def emit(path,value):
        raw=json.dumps(value,ensure_ascii=False,indent=2).encode();tmp=path.with_suffix('.json.tmp')
        assert not path.exists()
        with tmp.open('xb') as stream:stream.write(raw)
        assert tmp.read_bytes()==raw;tmp.replace(path)
        return {'path':str(path),'sha256':sha(raw)}
    reportpin=emit(W/'review/PUBLICATION_FIX_R1.json',report)
    builderchecks=load(P/'validation/final_checks.json')
    assert builderchecks['passed'] and builderchecks['plan_sha256']==report['plan_sha256']
    verdict={'status':'PASS','reviewer':'codex-v394-reviewer','scope':'Prepared exact two-label fix and eight-file plan; not applied/live verified.','plan_sha256':report['plan_sha256'],'transaction_sha256':sha(read(P/'transaction.py')),'maintenance_sha256':sha(read(P/'maintenance.py')),'deploy_controlled_sha256':sha(read(P/'deploy_controlled.py')),'verify_installed_sha256':sha(post_raw),'substantive_review':reportpin,'builder_checks_sha256':sha(read(P/'validation/final_checks.json')),'source_executed':False,'remote_count_calls':0,'publication_label_apply_accepted':False,'verify_accepted':False}
    finalpin=emit(P/'validation/review_final.json',verdict)
    print(json.dumps({'verdict':report['verdict'],'report':reportpin,'plan_sha256':report['plan_sha256'],'counts':counts,'review_final':finalpin,'production_changed':False},ensure_ascii=False))


if __name__=='__main__':main()
