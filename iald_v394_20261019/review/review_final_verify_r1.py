"""Final software integration review: receipts/jobs/memory append, no model calls."""
from pathlib import Path
from datetime import datetime, timezone
from contextlib import closing
import hashlib, json, sqlite3, sys

W=Path(__file__).resolve().parents[1]
R=Path(r'C:\IALD\projetos_pyhton\IALD')
inputs={}
sha=lambda b:hashlib.sha256(b).hexdigest()


def read(path):
    path=Path(path);raw=path.read_bytes();inputs[str(path)]={'sha256':sha(raw),'bytes':len(raw)};return raw


def load(path):return json.loads(read(path))


def main():
    sys.path.insert(0,str(W));import task
    project=task.project();t=next(x for x in project['projection']['active'] if x['id']=='verify')
    assert t['status']=='review_pending','Await actual final submit with memory receipt'
    for row in t['evidence']:assert sha(read(row['path']))==row['sha256']
    evidence_names={Path(x['path']).name for x in t['evidence']}
    assert 'MEMORY_DELIVERY.json' in evidence_names and 'delivery.json' in evidence_names
    delivery=load(W/'delivery.json');live=load(W/'live_validation.json');memory=load(W/'MEMORY_DELIVERY.json')
    assert delivery['status']==live['status']==memory['status']=='PASS'
    for row in delivery['evidence']+live['observations']:
        assert sha(read(row['path']))==row['sha256']
    assert all(live['checks'].values()) and not live['science_executed_or_confirmed']
    jobs=load(W/'LIVE_FINAL_JOBS.json');reload=load(W/'LIVE_RECOVERY_CHECK.json')
    assert jobs['jobs']==live['jobs'] and len(jobs['jobs'])==2 and not jobs['provider_retry_performed']
    job_observations=[]
    with closing(sqlite3.connect((R/'.iald_runtime/chat_jobs/jobs.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
        for job in jobs['jobs']:
            row=db.execute('SELECT id,conversation_id,status,error,cancel_requested,seq FROM jobs WHERE id=?',(job['id'],)).fetchone()
            assert row and row[1]==jobs['conversation_id'] and row[2]=='completed' and row[3] is None and row[4]==0 and row[5]==job['events']
            assert db.execute('SELECT COUNT(*) FROM events WHERE job=?',(job['id'],)).fetchone()[0]==row[5]
            job_observations.append({'id':row[0],'conversation':row[1],'status':row[2],'error':row[3],'events':row[5],'recorded_elapsed_seconds':job['elapsed_seconds']})
    publication=read(W/'LIVE_FINAL_PUBLICATION_OBSERVED.txt').decode('utf-8')
    haja=read(W/'LIVE_FINAL_HAJALUZ_OBSERVED.txt').decode('utf-8')
    for text in ['v394','Luiz Antonio Rotoli Miguel','237ef12c','Commit científico publicado e verificado']:
        assert text in publication
    assert 'Prompt: Haja luz.' in haja and 'v394' in haja and 'Nenhum programa' in haja
    for text in [publication,haja]:assert 'PUBLICATION_PENDING' not in text and 'publicação pendente' not in text
    assert reload['status']=='PASS' and not reload['has_obsolete_pending_label']
    assert all(reload[k] for k in ['has_final_prompt','has_loaded_v394','has_published_commit_response','has_haja_luz_reply'])
    first=load(W/'LIVE_TEST_FIRST_JOB.json');assert first['id'] not in {x['id'] for x in jobs['jobs']} and first['status']=='completed' and first['has_error'] is False
    assert (W/'LIVE_TEST_FIRST_OBSERVED.txt').is_file()
    installed=load(W/'publication_fix/installed_verification.json')
    assert delivery['identity']==installed['identity'] and installed['files_verified']==delivery['effective_files_verified']==1450
    assert installed['haiku_permanent_tokens']==delivery['haiku_permanent_tokens']==879535
    dep=load(W/'publication_fix/deployment.json')
    for path,digest in dep['files'].items():assert sha(read(path))==digest
    queue=W.parents[1]/'Chatgpt/IALD_ORQUESTRACAO_20260923/state/canonical_memory/ACTIVE.json'
    active=load(queue);assert active==load(W/'queue_activation.json')['pointer'] and active['generation']==delivery['queue_generation']
    surfaces=[];assert len(memory['surfaces'])==8
    for row in memory['surfaces']:
        current=read(row['path']);backup=read(row['backup'])
        assert row['status']=='appended' and sha(current)==row['sha256']
        assert current.startswith(backup) and len(current)>len(backup)
        appended=current[len(backup):]
        assert memory['marker'].encode() in appended
        assert b'1450' in appended and b'879535' in appended and b'27654' in appended
        surfaces.append({'path':row['path'],'sha256':row['sha256'],'backup':row['backup'],'backup_sha256':sha(backup),'append_bytes':len(appended),'original_prefix_byte_preserved':True})
    for channel in ['web','ios_internal','ios_external','android']:
        row=delivery['matrix'][channel]
        assert row['science_release']=='v394' and not row['new_binary_required'] and not row['new_binary_built']
        assert not row['client_resources_changed'] and not row['physical_installation_verified'] and not row['store_distribution_reinspected']
    assert not delivery['science_executed'] and not delivery['scientific_gate_changed'] and not delivery['accounts_wallet_consents_changed']
    bench=load(W/'bancada_verified_after.json')
    assert bench['status']=='PASS_READ_ONLY_STATE' and not bench['restart_performed'] and not bench['calculation_requested']
    assert bench['canone']['gate_effect']=='NONE'
    route=load(W/'route_delivery.json')
    assert route['ok'] is True and any(row['seq']==1268 and row['tipo']=='RESULTADO' and row['rota_id']=='infra.app.v394_20261019' for row in route['gravados'])
    for path,row in inputs.items():assert sha(Path(path).read_bytes())==row['sha256'],path
    report={'verdict':'PASS_FINAL_SOFTWARE_INTEGRATION','criterion_satisfied':True,'reviewer':'codex-v394-reviewer','checked_at':datetime.now(timezone.utc).isoformat(),'reference':str(task.REF),'task_id':'verify','criterion':t['criterion'],'reviewed_submission':t['evidence'],'baseline_revision':project['receipt']['revision'],'inputs':inputs,'terminal_jobs_independently_read':job_observations,'rendered_observation_scope':'Authenticated UI and reload observations are pinned main-session evidence, corroborated by independent persisted completed-job records; reviewer did not rerun remote tests.','memory_surfaces_verified':surfaces,'route_receipt_checked_not_reexecuted':route,'effective_files_prior_installed_verification':1450,'patch_current_hashes_rechecked':8,'delivery_matrix':delivery['matrix'],'findings':[],'limits':['Software/backend integration only; not physical confirmation or a new scientific proof. Scientific gate unchanged.','No new client binaries/distribution or physical-device installation verified.','Two synthetic automatic MiMo turns and persistence do not guarantee every provider/dialogue or establish causal ACOM improvement.','Original failed-label first test preserved; corrected final turns are distinct completed calls, not retries of uncertain requests.'],'reviewer_remote_calls':0,'source_execution':False,'models_called':0,'physical_confirmation':False}
    dest=W/'review/FINAL_VERIFY_R1.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=dest.with_suffix('.json.tmp')
    with tmp.open('xb') as stream:stream.write(raw)
    assert tmp.read_bytes()==raw and not dest.exists();tmp.replace(dest)
    print(json.dumps({'verdict':report['verdict'],'jobs':len(job_observations),'memory_surfaces':len(surfaces),'report':str(dest),'sha256':sha(raw),'mission_revision':project['receipt']['revision']},ensure_ascii=False))


if __name__=='__main__':main()
