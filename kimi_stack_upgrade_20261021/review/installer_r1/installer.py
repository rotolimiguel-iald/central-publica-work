"""PREPARED ONLY: stdlib installer for parent execution AFTER real review/GO.

Usage: python -B installer.py --plan <json> --plan-sha256 <measured SHA> --apply
Without --apply, validates all and writes a dry-run receipt only.
No provider, job, restart, memory transition, Git or subprocess operation.
CAS here means baseline/hash rechecks under this installer's cooperative lock;
uncooperative external writers cannot be made transactional by os.replace.
"""
import argparse,datetime,hashlib,json,os,re,sys,uuid
from pathlib import Path

WORK=Path(__file__).resolve().parent.parent
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
SHA=re.compile(r'[a-f0-9]{64}\Z')
class Refusal(RuntimeError):pass
def need(ok,code):
    if not ok:raise Refusal(code)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pairs(items):
    obj={}
    for k,v in items:need(k not in obj,'duplicate_json_key');obj[k]=v
    return obj
def safe_path(value,root,*,file_required=False):
    need(type(value)is str,'path_required');p=Path(value)
    need(p.is_absolute(),'absolute_path_required')
    root=root.resolve(strict=True)
    # Reject symlink/junction aliases at EVERY component inside the allowed root.
    absolute=Path(os.path.abspath(p));need(absolute.is_relative_to(root),'path_outside_allowed_root')
    current=root
    for part in absolute.relative_to(root).parts:
        current=current/part
        need(not current.is_symlink() and not getattr(current,'is_junction',lambda:False)(),'link_or_junction_refused')
    need(absolute.resolve(strict=False)==absolute,'noncanonical_path_refused')
    if file_required:need(absolute.is_file(),'source_file_missing')
    return absolute
def destination(value):
    p=safe_path(value,BASE);modules=(BASE/'iald_orchestrator').resolve(strict=True)
    need(p.is_relative_to(modules) or p==BASE.resolve(strict=True)/'transport_cli.py','destination_not_module_or_transport_cli')
    need(p.parent.is_dir(),'destination_parent_missing')
    need(not p.exists() or p.is_file(),'destination_not_regular_file')
    return p
def exclusive(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    need(path.read_bytes()==raw,'exclusive_write_verification_failed')
def current_pin(path):
    try:
        p=destination(str(path));return digest(p.read_bytes()) if p.exists() else None
    except Exception:return 'UNREADABLE_OR_SCOPE_CHANGED'
def validate(plan_path,plan_sha,entries=None):
    need(type(plan_sha)is str and SHA.fullmatch(plan_sha),'plan_pin_required')
    plan_path=safe_path(str(plan_path),WORK,file_required=True);raw=plan_path.read_bytes()
    need(0<len(raw)<=2*1024*1024 and digest(raw)==plan_sha,'plan_size_or_pin_mismatch')
    plan=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs)
    need(type(plan)is dict and type(plan.get('files'))is list and 0<len(plan['files'])<=128,'invalid_files_plan')
    entries=[] if entries is None else entries;seen=set()
    for row in plan['files']:
        need(type(row)is dict and set(row)=={'source','destination','sha256','baseline'},'invalid_plan_item')
        need(type(row['sha256'])is str and SHA.fullmatch(row['sha256']),'source_pin_required')
        need(row['baseline'] is None or type(row['baseline'])is str and SHA.fullmatch(row['baseline']),'baseline_pin_required')
        src=safe_path(row['source'],WORK,file_required=True);dst=destination(row['destination'])
        key=os.path.normcase(str(dst));need(key not in seen,'duplicate_destination');seen.add(key)
        need(src!=dst,'source_destination_same')
        data=src.read_bytes();need(0<len(data)<=16*1024*1024,'source_size_limit')
        need(digest(data)==row['sha256'],'source_pin_mismatch')
        before=dst.read_bytes() if dst.exists() else None
        need((None if before is None else digest(before))==row['baseline'],'destination_baseline_mismatch')
        entries.append(dict(source=src,destination=dst,data=data,before=before,sha256=row['sha256'],baseline=row['baseline']))
    return entries
def recheck(entry):
    src=safe_path(str(entry['source']),WORK,file_required=True);dst=destination(str(entry['destination']))
    need(digest(src.read_bytes())==entry['sha256'],'source_changed_before_commit')
    before=dst.read_bytes() if dst.exists() else None
    need(before==entry['before'],'destination_changed_before_commit')
def public(entry):
    backup_sha=None
    if entry.get('backup'):
        try:backup_sha=digest(safe_path(str(entry['backup']),BASE,file_required=True).read_bytes())
        except Exception:backup_sha='UNREADABLE_OR_SCOPE_CHANGED'
    return dict(source=str(entry['source']),destination=str(entry['destination']),source_sha256=entry['sha256'],baseline=entry['baseline'],observed_current_sha256=current_pin(entry['destination']),backup=str(entry['backup']) if entry.get('backup') else None,backup_sha256=backup_sha)
def rollback(written,stamp):
    outcomes=[]
    for entry in reversed(written):
        dst=entry['destination'];record=dict(destination=str(dst))
        try:
            # Never clobber a later third-party write in an attempted rollback.
            need(current_pin(dst)==entry['sha256'],'rollback_current_pin_conflict')
            if entry['before'] is None:
                retained=(WORK/'envelope'/'rollback_new'/stamp/dst.relative_to(BASE)).resolve()
                need(retained.is_relative_to(WORK.resolve()),'rollback_retention_outside_work')
                need(not retained.exists(),'rollback_retention_exists');retained.parent.mkdir(parents=True,exist_ok=True)
                destination(str(dst));os.replace(dst,retained)
                need(not dst.exists() and digest(retained.read_bytes())==entry['sha256'],'rollback_new_file_verification_failed')
                record.update(status='NEW_FILE_RETAINED_TARGET_ABSENT',retained=str(retained))
            else:
                backup=entry['backup'];raw=backup.read_bytes();need(raw==entry['before'] and digest(raw)==entry['baseline'],'rollback_backup_corrupt')
                temp=dst.with_name(dst.name+'.restore_'+stamp);exclusive(temp,raw)
                need(current_pin(dst)==entry['sha256'],'rollback_pin_changed_before_replace');os.replace(temp,dst)
                need(current_pin(dst)==entry['baseline'],'rollback_restore_verification_failed')
                record['status']='BASELINE_RESTORED'
        except Exception as exc:record.update(status='ROLLBACK_REFUSED_NEEDS_PARENT',error=error_code(exc))
        record['observed_after_sha256']=current_pin(dst);outcomes.append(record)
    return outcomes
def error_code(exc):return str(exc) if isinstance(exc,Refusal) else type(exc).__name__+':'+str(getattr(exc,'errno',''))
def run(plan_path,plan_sha,receipt_path,apply=False):
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'_'+uuid.uuid4().hex
    # Receipt location must be safe BEFORE attempting runtime work.
    out=safe_path(str(receipt_path),WORK);need(not out.exists(),'receipt_already_exists');need(out.parent.is_dir(),'receipt_parent_missing')
    report=dict(status='VALIDATION_STARTED',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),plan=str(plan_path),plan_sha256=plan_sha,apply=apply,pins=[],rollback=[],restart_executed=False,provider_calls=0)
    entries=[];written=[];lock=None;locked=False;exit_code=2
    try:
        validate(plan_path,plan_sha,entries) # Validate ALL sources/baselines before ANY target mutation.
        if not apply:
            report['status']='VALIDATED_NOT_APPLIED';exit_code=0
        else:
            lock=BASE/'iald_orchestrator'/'.reviewed_install.lock'
            fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);locked=True
            with os.fdopen(fd,'wb') as f:f.write(stamp.encode());f.flush();os.fsync(f.fileno())
            # Revalidate whole plan under cooperative lock, before first backup/write.
            entries=validate(plan_path,plan_sha)
            for entry in entries:
                recheck(entry);dst=entry['destination']
                if entry['before'] is not None:
                    backup=dst.with_name(dst.name+'.bak_'+stamp);exclusive(backup,entry['before']);entry['backup']=backup
                    need(digest(backup.read_bytes())==entry['baseline'],'backup_pin_mismatch')
                temp=dst.with_name(dst.name+'.tmp_'+stamp);exclusive(temp,entry['data']);recheck(entry)
                os.replace(temp,dst);written.append(entry)
                need(current_pin(dst)==entry['sha256'],'installed_file_pin_mismatch')
            # Detect a source or earlier target changing during the multi-file batch.
            for entry in entries:
                need(digest(safe_path(str(entry['source']),WORK,file_required=True).read_bytes())==entry['sha256'],'source_changed_during_install')
                need(current_pin(entry['destination'])==entry['sha256'],'target_changed_during_install')
            report['status']='INSTALLED_VERIFIED_NO_RESTART';exit_code=0
    except BaseException as exc:
        report.update(status='FAILED_NO_COMPLETE_INSTALL',error=error_code(exc))
        if written:
            report['rollback']=rollback(written,stamp)
            report['status']='FAILED_ROLLED_BACK' if all(r['status']!='ROLLBACK_REFUSED_NEEDS_PARENT' for r in report['rollback']) else 'FAILED_ROLLBACK_CONFLICT_NEEDS_PARENT'
    finally:
        report['pins']=[public(entry) for entry in entries]
        if locked:
            try:
                need(lock.read_bytes()==stamp.encode(),'lock_ownership_changed');lock.unlink()
            except Exception as exc:report['lock_cleanup_error']=error_code(exc);exit_code=2
        raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8');temp=out.with_name(out.name+'.tmp_'+stamp)
        exclusive(temp,raw);need(not out.exists(),'receipt_appeared_before_commit');os.replace(temp,out)
        need(out.read_bytes()==raw,'receipt_verification_failed')
    return report,exit_code
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--plan',required=True);parser.add_argument('--plan-sha256',required=True);parser.add_argument('--receipt');parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    receipt=Path(args.receipt) if args.receipt else WORK/'envelope'/('INSTALL_RECEIPT_'+uuid.uuid4().hex+'.json')
    try:
        report,code=run(Path(args.plan),args.plan_sha256,receipt,args.apply)
        print(json.dumps(dict(status=report['status'],receipt=str(receipt),pins=report['pins']),ensure_ascii=False));sys.exit(code)
    except Exception as exc:
        print(json.dumps(dict(status='INSTALLER_OR_RECEIPT_FAILURE',error=error_code(exc)),ensure_ascii=False));sys.exit(2)
