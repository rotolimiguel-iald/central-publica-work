"""Stage an explicit 18-file release after all four final receipts arrive.

No runtime writes, imports from application code, processes, builds or network.
Byte-copy/atomic verification reuses the transaction.py pattern by inspection;
maintenance.py is read as reference only, NEVER imported or invoked here.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

DEFAULT_WORK = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME = Path('C:/IALD/projetos_pyhton/IALD')
TARGETS = {
    'backend': ('iald_app_providers.py','iald_mimo_multimodal.py','private_media_routes.py','private_media_store.py'),
    'routing': ('iald_media_budget.py','iald_auto_router.py','iald_task_policy.py','iald_execution_guide.py','iald_routing_metrics.py'),
    'host': ('iald_app_spend.py','iald_web_server.py','new_private_media_host.py'),
    'client': ('app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js',
               'iald-app/android/app/src/main/assets/public/iald.js',
               'iald-app/ios/App/App.xcodeproj/project.pbxproj','iald-app/android/app/build.gradle'),
}
GROUP_DIRS={'backend':'backend_stage','routing':'routing_stage','host':'host_stage','client':'client_stage'}
ALLOWED_HASH_KEYS={'sha256','sourcehash','source_hash','source_sha256','staging_sha256','staged_sha256',
                   'final_sha256','client_sha256','server_sha256','spend_sha256'}


class Refusal(ValueError):pass


def digest(raw):return hashlib.sha256(raw).hexdigest()


def read_json(path):
    if path.stat().st_size>8*1024*1024:raise Refusal('Oversized metadata: '+path.name)
    return json.loads(path.read_bytes())


def within(path, root):
    path,root=Path(path).absolute(),Path(root).absolute()
    try:path.relative_to(root)
    except ValueError:raise Refusal('Path outside declared root') from None
    current=path
    while True:
        if current.is_symlink() or (hasattr(current,'is_junction') and current.is_junction()):
            raise Refusal('Symlink/junction path refused')
        if current==root:break
        current=current.parent
    try:path.resolve().relative_to(root.resolve())
    except ValueError:raise Refusal('Resolved path outside declared root') from None
    return path


def atomic_new(path,raw):
    if not raw:raise Refusal('Empty output')
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise Refusal('Frozen output already exists; no overwrite')
    temporary=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    if temporary.read_bytes()!=raw:raise Refusal('Temporary bytes differ')
    os.replace(temporary,path)
    if path.read_bytes()!=raw:raise Refusal('Staging bytes differ')


def hash_values(value):
    found=set()
    if type(value) is list:
        for child in value:found.update(hash_values(child))
    elif type(value) is dict:
        for key,child in value.items():
            if key=='files' and type(child) is dict:
                found.update(v for v in child.values() if type(v) is str and len(v)==64)
            if key in ALLOWED_HASH_KEYS and type(child) is str and len(child)==64:
                found.add(child)
            found.update(hash_values(child))
    return found


def field_value(value, dotted):
    for key in dotted.split('.'):
        if type(value) is not dict:return None
        value=value.get(key)
    return value


def current_science(work,runtime):
    path=within(work/'SCIENCE_BASELINE.json',work)
    source=read_json(path)
    if source.get('preserve_all') is not True or not source.get('files'):
        raise Refusal('Science baseline missing preserve-all evidence')
    rows=[]
    for item in source['files']:
        target=within(Path(item['path']),runtime)
        raw=target.read_bytes();actual=digest(raw)
        if actual!=item['sha256'] or len(raw)!=item['bytes']:
            raise Refusal('Science baseline changed: '+item['role'])
        rows.append(dict(role=item['role'],path=str(target),sha256=actual,bytes=len(raw),matches=True))
    return dict(status='MATCH_READ_ONLY_NO_SCIENCE_EXECUTION',release=source.get('release'),
                reference=str(path),reference_sha256=digest(path.read_bytes()),files=rows)


def inspect(config,work,runtime):
    if type(config) is not dict or set(config.get('groups',{}))!=set(TARGETS):
        raise Refusal('Exactly backend/routing/host/client groups required')
    pending=[];files=[];receipts=[]
    for group,targets in TARGETS.items():
        entry=config['groups'][group]
        if entry.get('final_for_packaging') is not True:
            pending.append(group);continue
        receipt=within(work/entry['receipt'],work/GROUP_DIRS[group])
        receipt_raw=receipt.read_bytes()
        if digest(receipt_raw)!=entry.get('receipt_sha256'):
            raise Refusal('Final receipt pin mismatch: '+group)
        receipt_data=read_json(receipt)
        if 'receipt_status' not in entry or receipt_data.get('status')!=entry['receipt_status']:
            raise Refusal('Final receipt status differs: '+group)
        if len(entry.get('files',[]))!=len(targets):raise Refusal('Wrong final file count: '+group)
        seen=set();receipt_hashes=hash_values(receipt_data)
        for extra in entry.get('supplemental_receipts',[]):
            if not extra.get('source_manifest_bound_by_primary_field'):continue
            manifest_path=within(work/extra['path'],work/GROUP_DIRS[group])
            manifest_raw=manifest_path.read_bytes()
            if digest(manifest_raw)!=extra['sha256'] or field_value(receipt_data,extra['source_manifest_bound_by_primary_field'])!=extra['sha256']:
                raise Refusal('Source manifest is not pinned by final primary receipt')
            receipt_hashes.update(hash_values(read_json(manifest_path)))
        for item in entry['files']:
            relative=item['target']
            if relative not in targets or relative in seen:raise Refusal('Unexpected or repeated target: '+group)
            seen.add(relative)
            source=within(work/item['source'],work/GROUP_DIRS[group])
            source_parts=source.relative_to(work/GROUP_DIRS[group]).parts
            if any(part.casefold() in ('tests','test','fixtures','node_modules','.git','__pycache__') for part in source_parts):
                raise Refusal('Test/dependency/hidden source path refused')
            # Exact targets plus exact suffix/name whitelist; no recursive copying.
            if source.name!=Path(relative).name:raise Refusal('Source/target filename differs')
            raw=source.read_bytes();source_hash=digest(raw)
            if not raw or source_hash!=item.get('sourcehash') or source_hash not in receipt_hashes:
                raise Refusal('Source not bound to final receipt: '+relative)
            target=within(runtime/relative,runtime)
            exists=target.exists()
            if exists and not target.is_file():raise Refusal('Non-file runtime target')
            baseline=digest(target.read_bytes()) if exists else None
            if 'baseline' not in item or baseline!=item['baseline']:
                raise Refusal('Runtime R baseline changed/unpinned: '+relative)
            files.append(dict(group=group,relative_target=relative,staged_original=str(source),
                target=str(target),destination=str(target),baseline=baseline,baseline_exists=exists,
                sourcehash=source_hash,sha256=source_hash,bytes=len(raw)))
        receipts.append(dict(group=group,path=str(receipt),sha256=digest(receipt_raw),status=entry['receipt_status']))
        for extra in entry.get('supplemental_receipts',[]):
            extra_path=within(work/extra['path'],work/GROUP_DIRS[group])
            extra_raw=extra_path.read_bytes()
            if digest(extra_raw)!=extra['sha256']:raise Refusal('Supplemental receipt pin mismatch: '+group)
            extra_data=read_json(extra_path)
            field=extra.get('binds_primary_sha256_field')
            if field is not None and field_value(extra_data,field)!=digest(receipt_raw):
                raise Refusal('Supplemental receipt refers to another primary receipt')
            if extra.get('covers_sources') is True and not {f['sourcehash'] for f in files if f['group']==group}<=hash_values(extra_data):
                raise Refusal('Supplemental manifest differs from packaged sources')
            receipts.append(dict(group=group,path=str(extra_path),sha256=digest(extra_raw),supplemental=True))
    if pending:return dict(status='WAITING_FINAL_RECEIPTS',pending_groups=pending,plan_frozen=False),None
    if len(files)!=18 or len({row['target'].casefold() for row in files})!=18:
        raise Refusal('Exactly 18 unique targets required')
    by_target={row['relative_target']:row['sourcehash'] for row in files}
    for target,expected in config.get('required_source_dependencies',{}).items():
        if by_target.get(target)!=expected:raise Refusal('Cross-front dependency pin differs: '+target)
    science=current_science(work,runtime)
    return dict(status='READY_FOR_STAGING_FREEZE',files=files,receipts=receipts,
                science=science,plan_frozen=False),science


def prepare(config,work=DEFAULT_WORK,runtime=DEFAULT_RUNTIME,*,freeze=False):
    work,runtime=Path(work).absolute(),Path(runtime).absolute()
    release=within(work/'release_stage',work)
    state,science=inspect(config,work,runtime)
    if state['status']=='WAITING_FINAL_RECEIPTS' or not freeze:return state
    release.mkdir(parents=True,exist_ok=True)
    lock=within(release/'.prepare.lock',release)
    with lock.open('xb') as owner:
        owner.write(str(os.getpid()).encode());owner.flush();os.fsync(owner.fileno())
    try:
        return freeze_tree(config,work,runtime,release)
    finally:
        lock.unlink()


def freeze_tree(config,work,runtime,release):
    state,science=inspect(config,work,runtime)
    if state['status']!='READY_FOR_STAGING_FREEZE':raise Refusal('Final receipts no longer ready')
    tree=within(release/'tree',release)
    if tree.exists() or (release/'install_plan.json').exists() or (release/'INSTALL_PLAN.json').exists() or (release/'SCIENCE_BASELINE.json').exists():
        raise Refusal('Tree/plan already exists; no stale merge or overwrite')
    for row in state['files']:
        source=Path(row['staged_original']);raw=source.read_bytes()
        if digest(raw)!=row['sourcehash']:raise Refusal('Source changed before copy')
        dest=within(tree/row['relative_target'],tree)
        atomic_new(dest,raw);row['source']=str(dest)
    # Recheck receipts, runtime R, scientific baseline and sources after copying.
    checked,_=inspect(config,work,runtime)
    if checked['status']!='READY_FOR_STAGING_FREEZE':raise Refusal('Receipt status changed during copy')
    if checked['files']!=[{k:v for k,v in row.items() if k!='source'} for row in state['files']]:
        raise Refusal('Release inputs changed during copy')
    if checked['science']!=science or checked['receipts']!=state['receipts']:
        raise Refusal('Science/receipts changed during copy')
    for row in state['files']:
        if digest(Path(row['source']).read_bytes())!=row['sourcehash']:raise Refusal('Copied tree changed')
    atomic_new(release/'SCIENCE_BASELINE.json',json.dumps(science,ensure_ascii=False,indent=2).encode('utf-8'))
    plan=dict(protocol='iald.staging-release/v1',status='FROZEN_STAGING_ONLY_NOT_INSTALLED',
        utc=datetime.now(timezone.utc).isoformat(),runtime_root=str(runtime),files=state['files'],
        receipts=state['receipts'],config_sha256=digest(json.dumps(config,sort_keys=True,allow_nan=False).encode()),
        science_comparison_sha256=digest((release/'SCIENCE_BASELINE.json').read_bytes()),
        runtime_writes=False,builds=False,push=False,secrets_included=False,
        deployment_requirement='Separate approved transaction/maintenance with fresh runtime CAS and independent review; this script never deploys')
    raw_plan=json.dumps(plan,ensure_ascii=False,indent=2).encode('utf-8')
    atomic_new(release/'install_plan.json',raw_plan)
    atomic_new(release/'INSTALL_PLAN_PIN.json',json.dumps(dict(path=str(release/'install_plan.json'),
        sha256=digest(raw_plan),legacy_case_alias='INSTALL_PLAN.json',
        windows_note='Case-insensitive alias of same file; no second independent plan',
        transaction_fields=['source','destination','sha256','baseline'],installed=False),indent=2).encode('utf-8'))
    return dict(status=plan['status'],plan_frozen=True,files=len(plan['files']),
                install_plan=str(release/'install_plan.json'),plan_sha256=digest(raw_plan),runtime_writes=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--runtime-root',type=Path,default=DEFAULT_RUNTIME)
    parser.add_argument('--freeze',action='store_true',help='Requires all four exact final pinned receipts')
    args=parser.parse_args()
    config_path=within(args.config,DEFAULT_WORK/'release_stage')
    try:
        result=prepare(read_json(config_path),runtime=args.runtime_root,freeze=args.freeze)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (Refusal,OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps(dict(status='REFUSED_NO_DEPLOYMENT',reason=str(exc)),ensure_ascii=False));return 2


if __name__=='__main__':sys.exit(main())
