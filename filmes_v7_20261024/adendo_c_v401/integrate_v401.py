"""Install only the reviewed data/source/replay bytes and issue current receipts."""
import datetime
import os
import time
from manage_v401_data import B,C,S,V,N,W,ORDER,read,pin,sha,save,atomic,check,stable_seal

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def seal_guard():
    seal=stable_seal()
    capture=read(C/'SOURCE_CAPTURE.json')
    for row in capture['files']:
        from pathlib import Path
        assert pin(Path(row['canonical']['path']))==row['canonical'],'STOP: canonical source changed'
        assert pin(Path(row['isolated']['path']))==row['isolated'],'STOP: staged source changed'
    return seal

def integrate():
    preflight=check();seal=seal_guard();comparison=read(C/'NUMERIC_COMPARISON.json')
    assert comparison['status']=='PASS' and not comparison['unexpected_differences']
    assert not (C/'INTEGRATION.json').exists(),'Integration already recorded; inspect, do not rerun'
    baseline={x['relative']:x for x in read(C/'BASELINE_MANIFEST.json')['files']}
    for x in baseline.values():
        from pathlib import Path
        assert pin(Path(x['backup']['path']))==x['backup'],'Baseline changed'
    public=read(B/'replay/DELIVERY_C.json')['public_files']
    source=['um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','rodada_v401_stdout.txt']
    data=[x['file'] for x in comparison['files']]
    rels=['source/'+x for x in source]+['data/'+x for x in data]+['PROVENANCE_PUBLIC.json']+public
    rels+=['replay/TEST_OFFLINE.json','replay/TEST_BROWSER.json','replay/BROWSER_OK.png','replay/BROWSER_TAMPER.png']
    rels=list(dict.fromkeys(rels));plan=[]
    for x in comparison['files']:
        assert pin(S/'data'/x['file'])==x['after'],'Compared data changed'
    for rel in rels:
        target=V/rel;candidate=S/rel
        assert candidate.is_file(),rel
        if target.exists():
            assert rel in baseline and pin(target)==baseline[rel]['original'], 'CAS: '+rel
        plan.append({'relative':rel,'before':pin(target) if target.exists() else None,'candidate':pin(candidate)})
    for rel in ['export_data.py','extend_export.py','guard_export.py','replay/build_replay.py','replay/test_replay.py','replay/test_browser.cjs','replay/vendor_pyodide.py']:
        assert (V/rel).read_bytes()==(B/rel).read_bytes()==(S/rel).read_bytes(),rel
    save(C/'INTEGRATION_PLAN.json',{'source':'v401','source_sha256':seal['sha256']['um.py'],'preflight':preflight,'files':plan})
    stamp=str(time.time_ns());records=[]
    # Back up every file to be replaced before the first production replacement.
    for row in plan:
        p=V/row['relative'];q=S/row['relative'];different=not p.exists() or p.read_bytes()!=q.read_bytes()
        row['changed']=different
        if different and p.exists():
            backup=p.with_name(p.name+'.bak_v400_'+stamp);raw=p.read_bytes()
            backup.write_bytes(raw);assert backup.read_bytes()==raw;row['backup']=pin(backup)
    seal_guard()
    for row in plan:
        p=V/row['relative'];q=S/row['relative']
        if row['changed']:
            assert (pin(p) if p.exists() else None)==row['before'],'CAS during integration'
            raw=q.read_bytes();tmp=p.with_name(p.name+'.tmp_v401_'+stamp)
            tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;os.replace(tmp,p)
        assert p.read_bytes()==q.read_bytes()
        records.append({**row,'installed':pin(p)})
    seal_guard()
    save(C/'INTEGRATION.json',{'status':'PASS','source':'v401','source_sha256':seal['sha256']['um.py'],
         'created_at':now(),'preflight':preflight,'comparison':pin(C/'NUMERIC_COMPARISON.json'),
         'changed_files':sum(x['changed'] for x in records),'files':records,
         'preserved':'Original sources, renderer, audio, narration timelines, media, make and final manifests were not written.'})
    ready={'status':'DATA_READY','source':'v401','source_sha256':seal['sha256']['um.py'],'created_at':now(),
           'seal':pin(V/'source/um_absoluto_selo.json'),'seal_timestamp':seal['timestamp'],
           'comparison':pin(C/'NUMERIC_COMPARISON.json'),'integration':pin(C/'INTEGRATION.json'),
           'allowed_counts':comparison['authorized_counts'],'unexpected_scientific_differences':0,
           'anchors':comparison['anchors'],'replay':comparison['replay'],
           'source_files':[pin(V/'source'/n) for n in source],
           'data_files':[pin(V/'data'/n) for n in data],
           'root_provenance':pin(V/'PROVENANCE_PUBLIC.json'),
           'scope':'Data gate only. Renderer, audio, final media and final acceptance belong to their assigned reviewers. Exporter tolerances unchanged; all cross-version comparisons exact.',
           'freeze':'Source/data bytes are ready for the coordinator to freeze and render; no further changes planned.'}
    save(C/'DATA_READY.json',ready)
    print({'status':'DATA_READY','receipt':str(C/'DATA_READY.json'),'changed_files':sum(x['changed'] for x in records),'source_sha256':seal['sha256']['um.py']})

def deliver():
    preflight=check();seal=seal_guard();comparison=read(C/'NUMERIC_COMPARISON.json');integration=read(C/'INTEGRATION.json')
    for rec in integration['files']:assert pin(V/rec['relative'])==rec['installed']
    public=read(B/'replay/DELIVERY_C.json')['public_files'];manifest=read(V/'replay/replay-manifest.json')
    public_pins=[{'path':rel,'sha256':sha(V/rel),'bytes':(V/rel).stat().st_size} for rel in public]
    browser=read(V/'replay/TEST_BROWSER.json')
    full=V/'replay/DELIVERY_ADENDO_C_V401.json';assert not full.exists()
    evidence=[C/n for n in ['NUMERIC_COMPARISON.json','DATA_READY.json','INTEGRATION.json','BASELINE_MANIFEST.json','SOURCE_CAPTURE.json','DATA_EXECUTION.json','DATA_CLAIM_PREFLIGHT.json','BROWSER_INITIAL_NETWORK_DENIED.json','compare_v401.py','integrate_v401.py','manage_v401_data.py']]
    evidence += [V/rel for rel in public]
    evidence += [V/'replay'/n for n in ['TEST_OFFLINE.json','TEST_BROWSER.json','BROWSER_OK.png','BROWSER_TAMPER.png','build_replay.py','test_replay.py','test_browser.cjs','README.md']]
    evidence += [V/n for n in ['export_data.py','extend_export.py','guard_export.py']]
    evidence += [V/rec['relative'] for rec in integration['files'] if rec['relative'].startswith(('data/','source/'))]
    full_body={'status':'IMPLEMENTED_TESTED_AWAITING_INDEPENDENT_REVIEW','source':'v401','source_sha256':seal['sha256']['um.py'],
         'created_at':now(),'actor':'codex-video-replay','requirement':'V401_DATA','mission_reference':str(W/'SESSION_REFERENCE.json'),
         'order':pin(ORDER),'preflight':preflight,'source_details':manifest['source'],'seal':pin(V/'source/um_absoluto_selo.json'),
         'comparison':pin(C/'NUMERIC_COMPARISON.json'),'data_ready':pin(C/'DATA_READY.json'),
         'counts':comparison['authorized_counts'],'anchors':comparison['anchors'],
         'replay':{**comparison['replay'],'manifest':pin(V/'replay/replay-manifest.json'),
                   'source_excerpt_sha256':sha(V/'replay/um_nucleo_filme.py'),'scalar_excerpt_sha256':sha(V/'replay/um_scalar_excerpt.py'),
                   'negative_controls':[x for x in browser['checks'] if any(k in x['name'] for k in ['negative','tamper','missing'])],
                   'browser_execution':'Isolated candidate, CPU Chromium, external requests blocked; identical production bytes verified after copy.',
                   'visual':'BROWSER_OK.png inspected: v401 source and 61/61 displayed. Tamper screenshot retained with automated visible NOT_SEALED check.'},
         'public_files':public,'public_file_pins':public_pins,'evidence':[pin(p) for p in dict.fromkeys(evidence)],
         '_private_history':{'previous_full_receipt':pin(V/'replay/DELIVERY_ADENDO_C_V400.json'),'baseline':pin(C/'BASELINE_MANIFEST.json'),
                             'note':'Historical receipts, timestamps, negative controls and source versions preserved. This receipt is not in public_files.'},
         'limits':'Mathematics belongs to the kernel under its hypotheses. Replay recalculates numerical shadows, with 19 documentary HUD fields outside recalculation. No Lean rebuild, empirical confirmation, render, TTS, publication or self-acceptance.'}
    save(full,full_body)
    fixed=V/'replay/DELIVERY_C.json';old=pin(fixed);old_raw=fixed.read_bytes()
    backup=fixed.with_name(fixed.name+'.bak_v400_pointer_'+str(time.time_ns()));backup.write_bytes(old_raw);assert backup.read_bytes()==old_raw
    save(fixed,{'schema':'tgl.replay-current-pointer.v1','status':'CURRENT_V401_POINTER','source':'v401',
         'source_sha256':seal['sha256']['um.py'],'updated_at':now(),
         'full_receipt':{'path':full.relative_to(V).as_posix(),'sha256':sha(full),'bytes':full.stat().st_size},
         'public_files':public,'public_file_pins':public_pins,
         'validation_summary':{'anchors':comparison['anchors'],'unexpected_scientific_differences':0,'offline_tests':13,'browser_comparisons':61},
         '_private_history':{'previous_fixed_receipt':old,'byte_backup':pin(backup),'previous_source':'v400',
                            'publication':'NOT_PUBLIC: fixed pointer, full receipts, backups and history are excluded from public_files.'}})
    seal_guard()
    save(C/'DELIVERY_DATA.json',{'status':'DATA_READY_AWAITING_INDEPENDENT_REVIEW','source':'v401','source_sha256':seal['sha256']['um.py'],
         'created_at':now(),'full_receipt':pin(full),'fixed_pointer':pin(fixed),'comparison':pin(C/'NUMERIC_COMPARISON.json'),
         'data_ready':pin(C/'DATA_READY.json'),'integration':pin(C/'INTEGRATION.json'),'baseline':pin(C/'BASELINE_MANIFEST.json'),
         'final_canonical_seal':pin(N/'um_absoluto_selo.json'),'final_canonical_program':pin(N/'um.py'),
         'preflight':preflight,'no_self_acceptance':True})
    print({'status':'DELIVERED_FOR_REVIEW','full_receipt':str(full),'delivery':str(C/'DELIVERY_DATA.json')})

if __name__=='__main__':
    import sys
    {'integrate':integrate,'deliver':deliver}[sys.argv[1]]()
