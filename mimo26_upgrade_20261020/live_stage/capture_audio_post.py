"""Fourth job only; read runtime receipts/files and exact job custody, never send."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import zlib

sys.dont_write_bytecode=True
import capture_live as capture
W=Path(__file__).resolve().parent;P=W.parent;R=capture.R
job='4e46ab4c-d269-4987-a805-e6df94242a1d';conversation='c_mvh5yioxnp6r'
capture.JOBS={'AUDIO_POST':(job,conversation)}
release=P/'audio_followup'
deployment=json.loads((release/'deployment.json').read_bytes())
restart=json.loads((release/'restart.json').read_bytes())
plan_bytes=(release/'install_plan.json').read_bytes();plan=json.loads(plan_bytes)
assert hashlib.sha256(plan_bytes).hexdigest()==deployment['plan_sha256']
assert len(plan['files'])==1
provider=R/'iald_app_providers.py';pin=hashlib.sha256(provider.read_bytes()).hexdigest()
assert pin==deployment['files'][str(provider)]==plan['files'][0]['sha256']
assert restart['status']=='PASS' and restart['new_web_pid']==512472
baseline=json.loads((W/'AUDIO_OFFLINE_REPLAY.json').read_bytes())
prefix=R/'.iald_runtime/haiku/prefix.md';science_pin=hashlib.sha256(prefix.read_bytes()).hexdigest()
assert science_pin==baseline['scientific_prefix_sha256']
prior=json.loads((W/'AUDIO_RESULT.json').read_bytes())
with capture.connect(capture.M/'memory.sqlite3') as db:
    links=list(db.execute('SELECT DISTINCT context_id FROM events WHERE changes_json LIKE ?',('%'+job+'%',)))
    assert len(links)==1
    cid=links[0]['context_id']
    def objective(context):
        row=db.execute('SELECT objective_blob,objective_sha256 FROM contexts WHERE context_id=?',(context,)).fetchone()
        raw=zlib.decompress(row['objective_blob']);assert hashlib.sha256(raw).hexdigest()==row['objective_sha256'];return raw
    original=objective(prior['acom']['context_id']);post=objective(cid)
    assert original==post
verification={'installed_provider_sha256':pin,'provider_matches_deployment_and_plan':True,
    'runtime_science_sha256':science_pin,'science_matches_pre_patch_replay':True,
    'restart_receipt_status':restart['status'],'restart_receipt_new_web_pid':restart['new_web_pid'],
    'restart_receipt_sha256':hashlib.sha256((release/'restart.json').read_bytes()).hexdigest(),
    'same_audio_and_question_objective_bytes':True,'objective_sha256':hashlib.sha256(post).hexdigest(),
    'causality_measured':False,'scope':'Local file/receipt and exact job metric checks; PID comes from saved restart receipt, no process introspection or new service request.'}
result=capture.capture('AUDIO_POST',verification=verification)
all_results={name:json.loads((W/(name+'_RESULT.json')).read_bytes()) for name in ('IMAGE','AUDIO','VIDEO','AUDIO_POST')}
amounts={name:Decimal(str(value['known_cost_estimate_usd'])).quantize(Decimal('0.0000000001')) for name,value in all_results.items()}
total={'status':'FOUR_AUTHORIZED_JOBS_CAPTURED','jobs':{name:{'id':value['job']['id'],'known_cost_estimate_usd':str(amounts[name]),'model':value['model_real']} for name,value in all_results.items()},
    'known_cost_estimate_usd':str(sum(amounts.values())),'cost_scope':result['cost_scope'],
    'causality_measured':False,'remote_calls':0,'retry':False,'sources':{name+'_RESULT.json':hashlib.sha256((W/(name+'_RESULT.json')).read_bytes()).hexdigest() for name in all_results}}
with (W/'FOUR_CALLS_COST.json').open('x',encoding='utf-8') as f:json.dump(total,f,ensure_ascii=False,indent=2)
print(json.dumps({'job':job,'terminal':result['job']['status'],'warnings':len(result['terminal_warnings']),'model':result['model_real'],'text':result['text'],'fourth_cost_estimate_usd':str(amounts['AUDIO_POST']),'four_total_usd':total['known_cost_estimate_usd'],'provider_installed_hash_verified':True,'science_unchanged':True,'same_audio_question':True,'causality_measured':False},ensure_ascii=False))
