"""Parent review of the data author's complete comparison and pinned sources."""
from context import *
import ast,copy

def main():
 check();stable_seal();report=read(H/'NUMERIC_COMPARISON.json');delivery=read(H/'DATA_DELIVERY.json')
 assert delivery['actor']['id']!=ACTOR['id']
 assert report['status']=='PASS_NUMERIC_PENDING_DISTINCT_REVIEW' and report['unexpected_differences']==[]
 assert pin(H/'NUMERIC_COMPARISON.json')==delivery['numeric_comparison']
 core=read(S/'source/um_absoluto.json')['core'];proof=read(S/'source/tgl_kernel_proof_manifest.json')
 p=core['estatuto_da_prova_v391']['prova_1_kernel'];g=core['bandeiras_do_gate_v403']['values']
 measured={'proof_ladder_clean':p['n_theorems_clean'],'proof_ladder_total':p['n_theorems_expected'],'formal_count':len(proof['formal_files_sha256']),'declaration_count':len(proof['axiom_report'])}
 assert report['counts']==measured and report['gate']['source_values']==g
 assert proof['formal_files_sha256']==core['kernel_formalization']['formal_files_sha256']
 assert proof['axiom_report']==core['kernel_formalization']['axiom_report']
 prior=read(B/'source/um_absoluto.json')['core']
 assert core['teste_de_veracidade_fase9_v397']==prior['teste_de_veracidade_fase9_v397']
 assert core['qg_closure']['gate']==prior['qg_closure']['gate']
 for item in report['files']:
  assert pin(B/'data'/item['file'])==item['before'] and pin(S/'data'/item['file'])==item['after'] and not item['unexpected']
 # Independent direct comparisons outside the amended gate branch.
 before=read(B/'data/frames.json');after=read(S/'data/frames.json')
 oldgate=before.pop('gate');newgate=after.pop('gate');assert before==after
 assert len(oldgate['flags'])==len(newgate['flags'])==g['n_flags']
 for a,b in zip(oldgate['flags'],newgate['flags']):
  x=copy.deepcopy(a)
  if x['name'] in g['informative']:x['origin']='computed from recorded inputs'
  assert x==b
 assert newgate['computed_count']==g['n_calculated'] and newgate['literal_count']==g['n_literal']
 oldhud=read(B/'data/hud.json');newhud=read(S/'data/hud.json')
 allowed=set(measured)|{'theorems','n_formal','um_sha16','flags_computed','flags_literal'}
 assert len(oldhud['items'])==len(newhud['items'])
 for a,b in zip(oldhud['items'],newhud['items']):
  assert a['id']==b['id']
  if a['id'] not in allowed:assert a==b
 assert {k:v for k,v in oldhud['extra'].items() if k not in allowed}=={k:v for k,v in newhud['extra'].items() if k not in allowed}
 for n in ['um_nucleo_filme.py','um_scalar_excerpt.py']:assert (B/'replay'/n).read_bytes()==(S/'replay'/n).read_bytes()
 assert all(x['identical_bytes'] for x in report['replay_text']) and all(x['refused'] for x in report['negative_controls'])
 assert read(H/'DATA_REPRODUCIBILITY.json')['exact_byte_equality']
 assert read(H/'DATA_GUARD_CONTROLS.json')['status']=='PASS'
 offline=read(S/'replay/TEST_OFFLINE.json');assert offline['status']=='PASS' and offline['source']=='v404'
 prov=read(S/'data/PROVENANCE_PUBLIC.json');assert prov['anchors_all_ok'] and len(prov['anchors'])>=64
 for anchor in prov['anchors']:assert anchor['ok'] is True and 0<=anchor['residual']<=anchor['tol']
 # Source-review scope: the sole changed scientific function is the G-authorized gate,
 # whose three formerly literal informative flags now consume their recorded inputs.
 assert [x['name'] for x in report['source_sections'] if not x['identical_bytes']]==['prove_qg_closure_gate']
 review={'status':'PASS_WITH_SCOPE','actor':ACTOR['id'],'source':'v404','source_sha256':sha(S/'source/um.py'),'comparison':pin(H/'NUMERIC_COMPARISON.json'),'data_delivery':pin(H/'DATA_DELIVERY.json'),'expected_counts_read_from_sealed_sources':measured,'gate_counts':g,'unexpected_differences':[],'anchors':len(prov['anchors']),'anchors_all_ok':True,'scope':'Distinct parent review of complete exact tree comparison, exporter patch, gate source diff, source-derived counts, frozen nature result, replay bytes and negative controls. No new Lean proof or empirical test; browser receipt remains separate.','inputs':[pin(H/n) for n in ['data_compare.py','data_verify.py','DATA_GATE_SOURCE_DIFF.json','DATA_REPRODUCIBILITY.json','DATA_GUARD_CONTROLS.json']]}
 create(H/'PARENT_DATA_REVIEW.json',review)
 evidence=[{'path':str(H/'PARENT_DATA_REVIEW.json'),'sha256':sha(H/'PARENT_DATA_REVIEW.json')}]
 if not (H/'DATA_ACCEPT.json').exists():create(H/'DATA_ACCEPT.json',mission.call({'operation':'accept',**current(),'task_id':'V404_DATA','review_evidence':evidence,'event_id':'ordem022-v404-data-parent-accept'}))
 # Candidate data only; no production replacement. The media consumer later uses
 # a separate installed-data receipt so the audio plan's pinned input stays immutable.
 datafiles=[pin(S/'data'/n) for n in ['hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','STDOUT_LINES.json','MANIFEST.json','film1.json','film2.json']]
 create(H/'DATA_READY.json',{'status':'DATA_READY','source':'v404','source_sha256':review['source_sha256'],'comparison':pin(H/'NUMERIC_COMPARISON.json'),'parent_review':pin(H/'PARENT_DATA_REVIEW.json'),'unexpected_scientific_differences':0,'data_files':datafiles,'anchors':{'total':len(prov['anchors']),'all_ok':True},'scope':'Candidate data accepted. Browser test and production integration are separate prerequisites before render.'})
 print(json.dumps({'status':'DATA_READY_CANDIDATE','counts':measured,'anchors':len(prov['anchors'])}))
if __name__=='__main__':main()
