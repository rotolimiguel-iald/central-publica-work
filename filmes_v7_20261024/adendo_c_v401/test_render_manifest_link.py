"""Focused transition controls, using real completed receipts in a private copy."""
from pathlib import Path
from unittest.mock import patch
import ast
import copy
import datetime
import json
import os
import finalizer_guards as g

C = Path(__file__).resolve().parent
V = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7')


def main():
    source = g.read(C/'SOURCE_CAPTURE.json')['source_sha256']
    watch = g.read(C/'MEDIA_WATCH.json'); delivery = g.read(C/'DELIVERY_E.json')
    g.require_current(watch, source, {'COMPLETE'})
    g.require_current(delivery, source, {'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST'})
    g.verify_pin(delivery['render_manifest'], V/'RENDER_MANIFEST.json')
    before = g.read(V/'RENDER_MANIFEST.json'); original_bytes = (V/'RENDER_MANIFEST.json').read_bytes()
    protected = [C/'DELIVERY_E.json',C/'MEDIA_WATCH.json',C/'media_v401_worker.py',C/'DATA_READY.json',
                 C/'SOURCE_CAPTURE.json',V/'RENDER_MANIFEST.json',V/'make_v7.py']
    preserved = [g.file_pin(p) for p in protected]
    # Evaluate only the builder's read-only parameter assignments, never collect_public/main.
    make_tree = ast.parse((V/'make_v7.py').read_bytes())
    collect = next(n for n in make_tree.body if isinstance(n,ast.FunctionDef) and n.name=='collect_public')
    variables = {'scene_source','finish_source','parameter_lines','params'}
    assignments = [n for n in collect.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in variables for t in n.targets)]
    assert {t.id for n in assignments for t in n.targets if isinstance(t,ast.Name)} == variables
    namespace = {'ROOT':V}
    exec(compile(ast.Module(body=assignments,type_ignores=[]),'read_only_make_parameters','exec'),namespace)
    jobs = {}
    for kind,entry in delivery['jobs'].items():
        job = g.read(g.verify_pin(entry))
        jobs[kind] = {'job_sha256':entry['sha256'],'metadata':job['metadata'],'encoded_sha256':job['sha256'],
                      'render':job['render'],'source_files':job['source_files']}
    projected = {'schema':'tgl.render.v7','source':'v401','version':'v401','source_sha256':source,
                 'parameters':namespace['params'],'jobs':jobs}
    expected_comparison = g.compare_render_manifests(before,projected,source)
    root=C/'manifest_link_fixture';assert not root.exists();root.mkdir()
    c=root/'receipts';v=root/'delivery';c.mkdir();v.mkdir()
    def write(p,obj):p.write_bytes((json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())
    current=v/'RENDER_MANIFEST.json';current.write_bytes(original_bytes)
    (v/'make_v7.py').write_bytes((V/'make_v7.py').read_bytes())
    fixture_delivery=copy.deepcopy(delivery);fixture_delivery['render_manifest']=g.file_pin(current)
    write(c/'DELIVERY_E.json',fixture_delivery);write(c/'MEDIA_WATCH.json',watch)
    results=[]
    def test(name,callback,rejected=False):
        try: value=callback()
        except (AssertionError,KeyError,ValueError,FileNotFoundError) as exc:
            assert rejected,(name,str(exc));results.append({'name':name,'passed':True,'observed':'rejected','detail':str(exc)[:220]});return None
        assert not rejected,'Unexpected acceptance: '+name
        results.append({'name':name,'passed':True,'observed':'accepted'});return value
    test('real_completed_E_pin_matches_current_manifest',lambda:g.verify_pin(delivery['render_manifest'],V/'RENDER_MANIFEST.json'))
    test('actual_make_parameters_and_jobs_match_except_worker_annotation',lambda:g.compare_render_manifests(before,projected,source))
    stage=test('snapshot_before_make_fixture',lambda:g.preserve_render_manifest_before_make(c,v,source))
    snapshot=c/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json';assert snapshot.read_bytes()==original_bytes
    test('byte_exact_snapshot',lambda:g.verify_pin(stage['snapshot'],snapshot))
    write(current,projected)
    link=test('post_make_fixture_link',lambda:g.build_render_manifest_link(c,v,source,stage))
    write(c/'FINAL_RENDER_MANIFEST_LINK.json',link)
    test('finish_link_guard',lambda:g.validate_render_manifest_link(c,v,source))
    test('resume_preserves_original_snapshot_after_rewrite',lambda:g.preserve_render_manifest_before_make(c,v,source))
    assert snapshot.read_bytes()==original_bytes
    for label,mutate in [
        ('encoded_count',lambda d:d['jobs']['film1']['render'].__setitem__('encoded',1)),
        ('parameter',lambda d:d['parameters'].__setitem__('grading','changed')),
        ('source_file_pin',lambda d:d['jobs']['film1'].__setitem__('source_files',{})),
        ('source_program_pin',lambda d:d.__setitem__('source_sha256','0'*64)),
        ('unrelated_metadata',lambda d:d.__setitem__('unapproved_metadata',True)),
        ('changed_worker_annotation',lambda d:d.__setitem__('adendo_worker',{'changed':True})),
        ('nonfinite',lambda d:d['jobs']['film1']['render'].__setitem__('elapsed_s',float('nan')))]:
        changed=copy.deepcopy(projected);mutate(changed)
        test(label+'_rejected',lambda d=changed:g.compare_render_manifests(before,d,source),True)
    snapshot.write_bytes(original_bytes+b'\n')
    test('tampered_snapshot_rejected',lambda:g.validate_render_manifest_link(c,v,source),True)
    snapshot.write_bytes(original_bytes)
    pending=copy.deepcopy(watch);pending['status']='VALIDATING';write(c/'MEDIA_WATCH.json',pending)
    test('incomplete_worker_rejected',lambda:g.preserve_render_manifest_before_make(c,v,source),True)
    write(c/'MEDIA_WATCH.json',watch)
    changed=copy.deepcopy(fixture_delivery);changed['render_manifest']['sha256']='0'*64;write(c/'DELIVERY_E.json',changed)
    test('changed_E_receipt_rejected',lambda:g.validate_render_manifest_link(c,v,source),True)
    write(c/'DELIVERY_E.json',fixture_delivery)
    # Serializing again after signing is still a byte change and requires a fresh link.
    current.write_bytes(json.dumps(projected,ensure_ascii=False,indent=2).encode())
    test('final_bytes_changed_after_link_rejected',lambda:g.validate_render_manifest_link(c,v,source),True)
    write(current,projected)
    test('restored_link_guard',lambda:g.validate_render_manifest_link(c,v,source))
    for p in ['finalize_make.py','finish_v401.py','finalizer_guards.py']:
        test('syntax_'+p,lambda name=p:compile((C/name).read_bytes(),str(C/name),'exec'))
    assert preserved == [g.file_pin(p) for p in protected]
    assert not (C/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json').exists() and not (C/'FINAL_RENDER_MANIFEST_LINK.json').exists(), 'Production transition was unexpectedly run'
    receipt={'status':'PASS_FOCUSED_CODE_AND_REAL_STAGE_RECEIPTS','source':'v401','source_sha256':source,
             'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':len(results),'results':results,
             'actual_stage':{'delivery_e':g.file_pin(C/'DELIVERY_E.json'),'media_watch':g.file_pin(C/'MEDIA_WATCH.json'),
                             'manifest':g.file_pin(V/'RENDER_MANIFEST.json'),'make_projection_comparison':expected_comparison},
             'protected_unchanged':preserved,'code':[g.file_pin(C/p) for p in ['finalize_make.py','finish_v401.py','finalizer_guards.py']],
             'scope':'Complete real E stage read and pinned. Only read-only builder parameter expressions and guard helpers evaluated; transition writes confined to a private C fixture. No actual make/finalizer/render/TTS invocation and no production snapshot/link emitted. Parent finalize_make will create the real snapshot before make and link after make.'}
    path=C/'MANIFEST_LINK_REVIEW.json';assert not path.exists();raw=(json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    tmp=path.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,path)
    print(json.dumps({'status':receipt['status'],'tests':len(results),'protected_files':len(preserved),'projected_semantics':expected_comparison}))


if __name__=='__main__':main()
