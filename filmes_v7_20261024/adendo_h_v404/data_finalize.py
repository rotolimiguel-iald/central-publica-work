"""Pin effective data deliverables and submit candidate only; never accept."""
import json,sys,datetime
import context as c
from data_manage import ACTOR,FILES,check

def main():
 preflight=check();c.stable_seal()
 comparison=c.read(c.H/'NUMERIC_COMPARISON.json');assert comparison['status']=='PASS_NUMERIC_PENDING_DISTINCT_REVIEW' and not comparison['unexpected_differences']
 tests=c.read(c.S/'replay/TEST_OFFLINE.json');assert tests['status']=='PASS'
 assert tests['manifest_sha256']==c.sha(c.S/'replay/replay-manifest.json')
 assert tests['source_sha256']==c.sha(c.S/'source/um.py')
 assert c.read(c.H/'DATA_REPRODUCIBILITY.json')['exact_byte_equality']
 assert c.read(c.H/'DATA_GUARD_CONTROLS.json')['status']=='PASS'
 baseline=c.read(c.H/'DATA_BASELINE_MANIFEST.json')
 changes=[]
 for row in baseline['files']:
  for key in ('original','copy'):
   p=c.Path(row[key]['path'])
   if c.pin(p)!=row[key]:changes.append({'kind':key,'path':str(p),'before':row[key],'after':c.pin(p)})
 assert not changes,changes
 effective=[c.S/'data'/n for n in FILES]
 effective += [c.S/n for n in ['PROVENANCE_PUBLIC.json','export_data.py','extend_export.py','guard_export.py','web/replay-demo.html']]
 effective += [c.S/'source'/n for n in c.read(c.H/'SOURCE_INTAKE.json')['files']]
 replay_names=['build_replay.py','test_replay.py','replay-manifest.json','um_nucleo_filme.py','um_scalar_excerpt.py','replay_runner.py','anchors.json','replay-trust.mjs','PYODIDE_VENDOR.json','PYODIDE_LICENSE.txt','TEST_OFFLINE.json']
 effective += [c.S/'replay'/n for n in replay_names]
 effective += [p for p in (c.S/'web/vendor/pyodide').iterdir() if p.is_file() and '.bak_' not in p.name]
 pins=[c.pin(p) for p in effective]
 inherited=[c.pin(p) for p in (c.S/'replay').iterdir() if p.is_file() and p not in effective and '.bak_' not in p.name]
 report={'status':'PASS_DATA_CANDIDATE_PENDING_DISTINCT_REVIEW','actor':ACTOR,'reference':str(c.REF),'task_id':'V404_DATA','source':'v404','files':pins,'counts':comparison['counts'],'gate':comparison['gate'],'numeric_comparison':c.pin(c.H/'NUMERIC_COMPARISON.json'),'source_capture':c.pin(c.H/'SOURCE_CAPTURE.json'),'baseline':c.pin(c.H/'DATA_BASELINE_MANIFEST.json'),'production_and_baseline_pins_unchanged':not changes,'reproducibility':c.pin(c.H/'DATA_REPRODUCIBILITY.json'),'guard_controls':c.pin(c.H/'DATA_GUARD_CONTROLS.json'),'offline_tests':c.pin(c.S/'replay/TEST_OFFLINE.json'),'first_comparison':c.pin(c.H/'DATA_FIRST_COMPARISON.json'),'gate_source_before_after':c.pin(c.H/'DATA_GATE_SOURCE_DIFF.json'),'replay_excerpt_bytes_unchanged':all(x['identical_bytes'] for x in comparison['replay_text']),'nature_v397_identical':comparison['nature_record_identical'],'preflight':preflight,'failure_preserved':c.pin(c.H/'DATA_PREPARE_FAILURE_R1.json'),'release_for_render':False,'accepted':False,'inherited_not_current_evidence':inherited,'limits':['Candidate data only; no production installation, TTS, render, source edits, Lean or network.','Distinct reviewer required; this submission does not release parent for render.','Browser test not rerun: parent-owned web runtime/trust outside data write set. New trust emitted at candidate_v404/replay/replay-trust.mjs for integration by parent.','Replay builder reads production worker bytes for pin only; no web runtime mutation.','Inherited replay receipts/scripts listed separately are historical, not current v404 validation.','Initial baseline copy traversed nested replay fixture paths and failed Windows path-length guard; partial copies/temp preserved, not effective delivery. Corrected copier reads top-level data/replay files.','64 exporter anchors and 34 numerical replay anchors check their scoped calculations, not empirical confirmation.'], 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 c.save(c.H/'DATA_DELIVERY.json',report)
 # Preserve exact receipt and re-read current mission before the candidate submission.
 ready=check();p=c.project();task=next(t for t in p['projection']['active'] if t['id']=='V404_DATA')
 out=c.mission.call({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':'V404_DATA','lease_id':task['lease']['id'],'event_id':'v404-data-submit','evidence':[{'path':str(path),'sha256':c.sha(path)} for path in [c.H/'DATA_DELIVERY.json',c.H/'NUMERIC_COMPARISON.json']], 'note':'Dados/replay candidatos. Comparação integral sem divergência não autorizada; sem liberação de render até revisão distinta.'})
 c.save(c.H/'DATA_SUBMIT.json',out)
 post=c.project();t=next(t for t in post['projection']['active'] if t['id']=='V404_DATA')
 c.save(c.H/'DATA_SUBMIT_VERIFIED.json',{'receipt':post['receipt'],'task':t,'render_released':False})
 print(json.dumps({'status':report['status'],'task_status':t['status'],'files':len(pins),'delivery':str(c.H/'DATA_DELIVERY.json'),'receipt_revision':post['receipt']['revision']}))
if __name__=='__main__':main()
