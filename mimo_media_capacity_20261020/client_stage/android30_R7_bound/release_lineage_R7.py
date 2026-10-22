"""Validate original18 + hotfix4 evidence; an effective manifest is never installed."""
from pathlib import Path
import hashlib,json
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pinned(item,work):
    if not isinstance(item,dict) or not item.get('path') or not item.get('sha256'):
        raise RuntimeError('Pending pinned release evidence')
    p=Path(item['path']).resolve(strict=True)
    if not p.is_relative_to(Path(work).resolve()):raise RuntimeError('Release evidence outside mission')
    for q in [p,*p.parents]:
        if q.exists() and q.lstat().st_file_attributes & 0x400:raise RuntimeError('Reparse evidence refused')
    if digest(p)!=item['sha256']:raise RuntimeError('Release evidence pin changed')
    return json.loads(p.read_bytes())
def verify_effective(plan,work):
    chain=plan['installation_chain']
    original=pinned(chain['original18_plan'],work);hotfix=pinned(chain['hotfix4_plan'],work)
    effective=pinned(plan['main_plan_current_pin'],work)
    if effective.get('status')!='NOT_INSTALLABLE_EFFECTIVE_STATE' or effective.get('installable') is not False:
        raise RuntimeError('Effective manifest must be explicitly NOT_INSTALLABLE')
    def rows(d):return {x['destination']:x['sha256'] for x in d['files']}
    old,new,actual=rows(original),rows(hotfix),rows(effective)
    if len(old)!=18 or len(new)!=4 or not set(new)<=set(old) or actual!={**old,**new}:
        raise RuntimeError('Effective state is not exact original18 plus hotfix4')
    if any('baseline' in x for x in effective['files']):raise RuntimeError('Effective state must not carry installation baselines')
    return chain
def verify_release_admission(receipt,plan,work):
    chain=verify_effective(plan,work)
    for field in ('review_receipts','installation_receipts'):
        entries=receipt.get(field)
        if not isinstance(entries,list) or len(entries)!=2:
            raise RuntimeError('Two distinct original18/hotfix4 '+field+' required')
        roles={x.get('role'):x for x in entries}
        if set(roles)!={'original18','hotfix4'}:raise RuntimeError('Release chain roles missing')
        for role in ('original18','hotfix4'):
            data=pinned(roles[role],work);expected=chain[role+'_plan']['sha256']
            if data.get('status')!='PASS' or data.get('plan_sha256')!=expected:
                raise RuntimeError('Successful evidence for actual installation plan required')
    ui=pinned(receipt.get('ui_verification'),work)
    if ui.get('status')!='PASS' or ui.get('client_sha256')!=plan['accepted_js_sha256']:
        raise RuntimeError('Real UI verification of installed R7 client required')
    return True
