"""Custody existing results and classify already observed full-main deltas."""
from pathlib import Path
import ast,datetime as dt,hashlib,json,os
from diary_r1 import ROOT,new,pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/full_rite'
dest=out/'reconciliation_r1';dest.mkdir(exist_ok=False)
run=ROOT/'work/rite394_20261015/r3'
source=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\results.json')
raw=source.read_bytes();text=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')
raw_hash=hashlib.sha256(raw).hexdigest();text_hash=hashlib.sha256(text.encode()).hexdigest()
baseline=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394/baseline/um_absoluto.json'
base=json.loads(baseline.read_bytes())['core'];actual=json.loads((run/'um_absoluto.json').read_bytes())['core']
history=out/'run_20261015T165543_615709Z/cache/auditoria/AUDITORIA_28SET_REGISTRO.json'
historical=json.loads(history.read_bytes())
assert raw_hash in json.dumps(historical) and text_hash in json.dumps(historical)
assert text_hash[:16] in json.dumps(base['joint_coincidence_result'])
target=dest/'results_existing_bytes.json'
tmp=target.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw;os.rename(tmp,target)
assert pin(source)['sha256']==raw_hash
review=json.loads((out/'FULL_RITE_OUTPUT_REVIEW_R2.json').read_bytes())
categories={
 'evidence_audit':'Existing results.json was not staged where the legacy reader searches.',
 'joint_coincidence_result':'Missing staged copy of the already existing results; custody is supplied separately, not a new experiment.',
 'the_iald_index':'Short-name source regex cannot account for generated/Unicode declarations or namespace collisions. Exact compiled-module index candidate is tested separately.',
 'joint_coincidence_result_v2':'Downstream of missing legacy results input; no scientific value overwritten here.',
 'joint_coincidence_result_v3':'Downstream of missing legacy results input; no scientific value overwritten here.',
 'tetelestai_conference_v375':'Exact #print axioms commands in the new audit were counted as trace_tracial proof consumers by legacy text scanner.',
 'tetelestai_conference_v376':'Same trace_tracial scanner dependency as v375.',
 'three_stress_tests_v387':'Current ladder advances; missing legacy results also changes verdict counters. These causes must be separated in the next receipt.',
 'text_label_errata_v389':'New embedded v394 modules were absent from the historical version ledger; complete that ledger, preserving the v389 cut.',
 'estatuto_da_prova_v391':'Version, live counts and program self-hash advance with the candidate; historical core is preserved.',
 'pedras_v392':'Live ladder advances with the new verified modules.',
 'varredura_e_sorry_v392':'Live source count advances with new modules.',
 'beta_escala_errata_v392':'Downstream of evidence_audit missing-input result.',
 'parametros_nomeados_v392':'Downstream of v376 scanner result.',
 'sn_ia_v388_viability_v392':'s12 reads joint_coincidence_result_v3 inventory; restore existing source before diagnosing a scientific difference.',
 'pedras_v393':'Live ladder advances with the new verified modules.',
 'kh_n1_cobertura_v393':'Historical minimum and current expanded proof coverage are distinct; next audit must record both.'}
delta=review['historical_verdict_changes_to_reconcile']
assert set(delta)==set(categories),(set(delta)-set(categories),set(categories)-set(delta))
new(dest/'RECONCILIATION.json',dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 status='DIAGNOSED_NOT_YET_REEXECUTED',deltas=categories,
 results_custody=dict(original=pin(source),copy=pin(target),raw_sha256=raw_hash,
 normalized_text_sha256=text_hash,crlf_count=raw.count(b'\r\n'),
 comparison='The old report used normalized-text SHA. It equals the current normalized-text SHA; the 28-Sep custody already pins the current raw-byte SHA. No byte change is established by comparing these two hash schemes.'),
 evidence=[pin(p) for p in [baseline,history,run/'um_absoluto.json',out/'FULL_RITE_OUTPUT_REVIEW_R2.json']],
 offline='DES_Y3 refused by the explicit no-network policy; no observation fetched. Existing no-network outcome remains visible.',
 no_scientific_composite_run=True,originals_unchanged=True,script=pin(__file__)))
print(json.dumps(dict(receipt=pin(dest/'RECONCILIATION.json'),delta_count=len(delta),raw_sha256=raw_hash,text_sha256=text_hash)))
