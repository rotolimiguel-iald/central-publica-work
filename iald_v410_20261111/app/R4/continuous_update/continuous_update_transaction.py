"""Data-only future app activation, with existing maintenance primitive.

Cannot install Python/JS/runtime at the app root. New immutable release artifacts
are copied first; the sole mutable pointer is iald_nucleo_fixo.json, switched last.
No call happens merely by importing this module.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
from contextlib import closing
from continuous_source_prepare import digest,dump,immutable
from continuous_update_worker import replace_bytes

def load_module(row,name):
    path=Path(row['path'])
    if digest(path.read_bytes())!=row['sha256']: raise ValueError('Maintenance pin changed')
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module);return module

def quiet(root):
    root=Path(root);jobs=root/'.iald_runtime/chat_jobs/jobs.sqlite3'
    if not jobs.is_file(): raise ValueError('Missing job ledger')
    checks=[(jobs,"SELECT COUNT(*) FROM jobs WHERE status IN ('queued','running')")]
    checks += [(p,"SELECT COUNT(*) FROM calls WHERE status='reserved'") for p in
               [*root.glob('*.reservas.sqlite3'),root/'.iald_runtime/app_evaluation/public_spend.sqlite3'] if p.is_file()]
    wallet=root/'.iald_runtime/monthly_wallet/wallet.sqlite3'
    if wallet.is_file():
        checks += [(wallet,"SELECT COUNT(*) FROM tasks WHERE status='active'"),
                   (wallet,"SELECT COUNT(*) FROM calls WHERE status='pending'")]
    for path,query in checks:
        with closing(sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)) as db:
            if db.execute(query).fetchone()[0]: return False
    return True

def validate_plan(candidate,root):
    candidate=Path(candidate).resolve();root=Path(root).resolve()
    plan=json.loads((candidate/'install_plan.json').read_bytes())
    files=plan['files'];pointer=root/'iald_nucleo_fixo.json'
    if sum(Path(r['destination']).resolve()==pointer for r in files)!=1: raise ValueError('Exactly one manifest pointer required')
    release_root=(root/'canonical_releases'/plan['target_name']).resolve()
    if release_root.parent!=root/'canonical_releases': raise ValueError('Release root invalid')
    seen=set()
    for row in files:
        src=Path(row['source']).resolve(strict=True);dst=Path(row['destination']).resolve()
        if not src.is_relative_to(candidate): raise ValueError('Source outside candidate')
        if dst in seen: raise ValueError('Duplicate destination')
        seen.add(dst)
        if dst!=pointer and not dst.is_relative_to(release_root): raise ValueError('Runtime mutation forbidden')
        raw=src.read_bytes()
        if digest(raw)!=row['sha256'] or len(raw)!=row['bytes']: raise ValueError('Install source mismatch')
        actual=digest(dst.read_bytes()) if dst.is_file() else None
        if actual!=row['baseline']: raise ValueError('Install baseline changed')
        if dst!=pointer and actual is not None and actual!=row['sha256']:
            raise ValueError('Existing immutable artifact replacement forbidden')
    if not plan.get('capacity_certificates'): raise ValueError('Native capacity certificates required')
    for row in plan['capacity_certificates']:
        p=Path(row['path']).resolve(strict=True)
        if not p.is_relative_to(candidate) or digest(p.read_bytes())!=row['sha256']:
            raise ValueError('Capacity evidence invalid')
    return plan

def activate(candidate,cfg,adapter):
    candidate=Path(candidate).resolve();root=Path(cfg['runtime']).resolve()
    if not candidate.is_relative_to(adapter.root): raise ValueError('Candidate outside updater state')
    journal=candidate/'transaction.json'
    if journal.exists(): raise ValueError('Deployment already attempted; reconcile only')
    manifest_pin=adapter.verify_package(candidate)['manifest_sha256']
    descriptor=json.loads((candidate/'candidate.json').read_bytes())
    expected=json.loads((candidate/'expected_active.json').read_bytes())
    def gates():
        if not adapter.review(candidate,manifest_pin) or not adapter.authorize(descriptor):
            raise ValueError('Review/authorization gate not satisfied')
        if adapter.active()!=expected: raise ValueError('Active CAS failed')
        adapter.verify_package(candidate)
        return validate_plan(candidate,root)
    plan=gates()
    if not quiet(root): raise ValueError('App busy')
    maintenance=load_module(cfg['maintenance'],'updater_reviewed_maintenance')
    maintenance.ROOT=root
    identity=None;switched=False;old=None
    pointer=root/'iald_nucleo_fixo.json'
    pointer_row=next(r for r in plan['files'] if Path(r['destination']).resolve()==pointer)
    try:
        with maintenance.stopped_web(lambda: None if quiet(root) else (_ for _ in ()).throw(RuntimeError('Busy'))) as identity:
            try:
                maintenance.assert_quiesced();plan=gates()
                immutable(journal,dump({'phase':'INSTALLING','identity':identity,'manifest_sha256':manifest_pin}))
                old=pointer.read_bytes()
                if digest(old)!=pointer_row['baseline']: raise ValueError('Pointer CAS changed')
                immutable(candidate/'previous_catalog.json',old)
                for row in plan['files']:
                    dst=Path(row['destination']).resolve()
                    if dst==pointer: continue
                    immutable(dst,Path(row['source']).read_bytes())
                if digest(pointer.read_bytes())!=pointer_row['baseline']: raise ValueError('Pointer CAS changed')
                # Durable baseline before pointer swap; retained after success too.
                immutable(candidate/'previous_catalog.json',old)
                replace_bytes(pointer,Path(pointer_row['source']).read_bytes());switched=True
                for row in plan['files']:
                    if digest(Path(row['destination']).read_bytes())!=row['sha256']: raise ValueError('Installed bytes mismatch')
                verification=json.loads(adapter.command('verify_loaded',['--candidate',candidate]))
                if verification.get('verified') is not True: raise ValueError('Loaded release not verified while quiesced')
                immutable(candidate/'quiesced_loader_verification.json',dump(verification))
                identity['resume_allowed']=True
                replace_bytes(journal,dump({'phase':'INSTALLED','identity':identity,'manifest_sha256':manifest_pin}))
            except BaseException:
                if switched:
                    if digest(pointer.read_bytes())!=pointer_row['sha256']:
                        raise RuntimeError('Concurrent pointer modification; manual recovery required')
                    replace_bytes(pointer,old)
                identity['resume_allowed']=digest(pointer.read_bytes())==pointer_row['baseline']
                replace_bytes(journal,dump({'phase':'ROLLED_BACK' if identity['resume_allowed'] else 'UNCERTAIN',
                                           'identity':identity,'manifest_sha256':manifest_pin}))
                raise
    finally:
        if identity and identity.get('resume_allowed'):
            restart=maintenance.await_restart(identity)
            immutable(candidate/'restart.json',dump(restart))
    # A new process verifies package loaders/corpus identity, not only pointer bytes.
    verification=json.loads(adapter.command('verify_loaded',['--candidate',candidate]))
    if verification.get('verified') is not True: raise ValueError('Loaded release not verified')
    immutable(candidate/'loaded_verification.json',dump(verification))
    replace_bytes(journal,dump({'phase':'ACTIVE','identity':identity,'manifest_sha256':manifest_pin}))

def reconcile(candidate,cfg,adapter):
    candidate=Path(candidate);journal=candidate/'transaction.json'
    if not journal.exists(): return {'verified':False,'status':'NO_RECEIPT'}
    state=json.loads(journal.read_bytes());root=Path(cfg['runtime']);pointer=root/'iald_nucleo_fixo.json'
    plan=json.loads((candidate/'install_plan.json').read_bytes())
    if state['phase']=='ROLLED_BACK':
        valid=pointer.read_bytes()==(candidate/'previous_catalog.json').read_bytes() and (candidate/'restart.json').is_file()
        return {'verified':valid,'status':'ROLLED_BACK'}
    if state['phase']!='ACTIVE': return {'verified':False,'status':'UNCERTAIN'}
    valid=all(digest(Path(r['destination']).read_bytes())==r['sha256'] for r in plan['files'])
    valid=valid and (candidate/'restart.json').is_file() and (candidate/'loaded_verification.json').is_file()
    if valid: valid=json.loads(adapter.command('verify_loaded',['--candidate',candidate])).get('verified') is True
    return {'verified':valid,'status':'ACTIVE'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True)
    parser.add_argument('--operation',choices=('quiet','deploy','reconcile'),required=True)
    parser.add_argument('--candidate');parser.add_argument('--expected-active')
    args=parser.parse_args()
    from continuous_update_adapter import Adapter
    adapter=Adapter(args.config);cfg=adapter.cfg
    if args.operation=='quiet': result={'quiet':quiet(cfg['runtime'])}
    elif args.operation=='deploy': activate(args.candidate,cfg,adapter);result={'status':'DONE'}
    else: result=reconcile(args.candidate,cfg,adapter)
    print(json.dumps(result))

if __name__=='__main__': main()
