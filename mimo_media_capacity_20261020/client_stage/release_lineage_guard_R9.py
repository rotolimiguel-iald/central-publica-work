"""Read-only final19, ordered deployment lineage and science admission guards."""
from pathlib import Path
import hashlib,json
R=Path('C:/IALD/projetos_pyhton/IALD')
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def safe(path,root):
    p=Path(path).resolve(strict=True)
    if not p.is_relative_to(Path(root).resolve()):raise RuntimeError('Path outside release scope')
    for q in [p,*p.parents]:
        if q.exists() and q.lstat().st_file_attributes & 0x400:raise RuntimeError('Reparse path refused')
    return p
def pinned(item,work):
    if not isinstance(item,dict) or not item.get('path') or not item.get('sha256'):raise RuntimeError('Pending pinned evidence')
    p=safe(item['path'],work)
    if digest(p)!=item['sha256']:raise RuntimeError('Evidence pin changed')
    return json.loads(p.read_bytes())
def file_map(data):
    rows=data.get('files')
    if not isinstance(rows,list):raise RuntimeError('Explicit files list required')
    out={}
    for row in rows:
        p=str(Path(row.get('destination') or row.get('path') or ''))
        sha=row.get('sha256')
        if p in out or not isinstance(sha,str) or len(sha)!=64 or any(c not in '0123456789abcdef' for c in sha):
            raise RuntimeError('Duplicate or invalid runtime pin')
        out[p]=sha
    return out
def check_science(config,work):
    science=pinned(config['science_baseline'],work)
    if science.get('preserve_all') is not True:raise RuntimeError('Science preservation baseline required')
    for item in science['files']:
        p=safe(item['path'],R)
        if digest(p)!=item['sha256'] or p.stat().st_size!=item['bytes']:raise RuntimeError('Current science baseline changed')
    return science
def check_chain(config,work,installed=True):
    allowed=set(config['allowed_runtime_destinations']);state={}
    if len(allowed)!=19:raise RuntimeError('Exactly19 known destinations required')
    for layer in config['layers']:
        plan=pinned(layer['plan'],work);rows=plan['files'];actual=file_map(plan)
        if len(rows)!=layer['count'] or set(actual)!=set(layer['destinations']) or not set(actual)<=allowed:
            raise RuntimeError('Layer target allowlist changed')
        for item in rows:
            # Validate all historical staged bytes, but only latest runtime bytes.
            source=safe(item['source'],work)
            if source.name!=Path(item['destination']).name or digest(source)!=item['sha256']:
                raise RuntimeError('Layer staged source pin changed')
            if layer['role']!='original18' and item['baseline']!=state.get(item['destination']):
                raise RuntimeError('Overlay baseline does not match preceding state')
        review=pinned(layer['review'],work)
        if review.get('status')!='PASS' or review.get('plan_sha256')!=layer['plan']['sha256']:
            raise RuntimeError('Distinct reviewed actual plan required')
        if installed:
            dep=pinned(layer['deployment'],work);restart=pinned(layer['restart'],work)
            if dep.get('status') not in ('INSTALLED_RESTART_REQUIRED','PASS','INSTALLED') or dep.get('plan_sha256')!=layer['plan']['sha256']:
                raise RuntimeError('Actual deployment receipt required for each layer')
            if dep.get('files')!=actual:raise RuntimeError('Installed historical file pins differ from reviewed layer')
            if restart.get('status')!='PASS' or restart.get('http_status')!=200:
                raise RuntimeError('Actual restart PASS required for each layer')
        state.update(actual)
    if set(state)!=allowed or len(state)!=19:raise RuntimeError('Final ordered overlay union differs from19 allowlist')
    return state
def check_final(config,manifest,work,installed=True,runtime=True):
    expected=check_chain(config,work,installed=installed)
    final=pinned(manifest,work)
    if final.get('status') not in ('PASS','PASS_EFFECTIVE_RUNTIME_NOT_INSTALLABLE') or file_map(final)!=expected:raise RuntimeError('Parent final19 PASS pins do not match ordered overlays')
    # Enforce allowlist before opening any claimed runtime file.
    if runtime:
        for name,sha in expected.items():
            if digest(safe(name,R))!=sha:raise RuntimeError('Latest runtime baseline does not match final19')
    for name,sha in config['mobile6'].items():
        if expected.get(name)!=sha:raise RuntimeError('R7 JS or native35/30 pin changed')
    check_science(config,work)
    return expected
def verify_final_state(plan,work):
    config=pinned(plan['release_binding'],work)
    return check_final(config,plan['main_plan_current_pin'],work)
def verify_release_admission(receipt,plan,work):
    verify_final_state(plan,work)
    config=pinned(plan['release_binding'],work)
    phase=pinned(config['engineering_phase_review'],work)
    if (phase.get('status')!='PASS_BUILD_PUSH_TECHNICAL_SCOPE'
        or set(phase.get('repository_allowlist',[]))!=set(config['private_mobile_allowlist'])
        or phase.get('repository_branch')!='codex/mobile-release'
        or phase.get('baseline_head')!=config['repository_baseline_head']):
        raise RuntimeError('Actual scoped engineering phase review required')
    addendum=pinned(receipt.get('phase_binding_addendum'),work)
    if (addendum.get('status')!='PASS' or not addendum.get('actor')
        or addendum.get('actor')=='codex-app-01a094df'
        or addendum.get('phase_review_sha256')!=config['engineering_phase_review']['sha256']
        or addendum.get('final_manifest_sha256')!=plan['main_plan_current_pin']['sha256']
        or addendum.get('execution_plan_sha256',{}).get(receipt.get('operation'))!=receipt.get('plan_sha256')):
        raise RuntimeError('Distinct effective-pin and execution-binding addendum PASS required')
    if receipt.get('execution_authorized_now') is not True:
        raise RuntimeError('Concrete parent engineering execution release pending')
    # This engineering/distribution phase does not assert successful perception,
    # authorize any extra provider test, or promote final mission acceptance.
    return True
