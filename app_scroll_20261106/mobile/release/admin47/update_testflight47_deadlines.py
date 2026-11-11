"""Staged admin-only sidecar, adapted from build44. No work at import.
--prepare: only after valid distribution47 receipt; creates frozen ADMIN_PLAN.
--apply: parent only after independent ADMIN_REVIEW; exactly two admin objects.
"""
from pathlib import Path
import datetime,hashlib,json,os,sys,tempfile
D=Path(__file__).resolve().parent
MOBILE=D.parents[1]
AUTHOR='codex-app-builder'
TARGET=Path(r'C:\IALD\projetos_pyhton\IALD\iald_deadlines.json')
DISTRIBUTION=D.parent/'IOS47_DISTRIBUTION.json'
PLAN=D/'ADMIN_PLAN.json';REVIEW=D/'ADMIN_REVIEW.json'
RESULT=D/'TESTFLIGHT47_INTERNAL_DEADLINES.json'

def check_context(applying=False):
    import subprocess
    ref=D.parents[2]/"SESSION_REFERENCE.json"
    def call(payload, cli):
        run=subprocess.run([sys.executable,"-B","-X","utf8",str(Path(r"C:\IALD\MEMORIA_IALD")/cli)],input=json.dumps(payload).encode(),capture_output=True)
        result=strict_json(run.stdout)
        require(run.returncode==0 and result.get("ok") is True,"Own mission preflight refused")
        return result["result"]
    call(dict(operation="project",reference=str(ref)),"session_memory.py")
    if applying:
        p=call(dict(operation="project",reference=str(ref),max_chars=100000),"mission_cli.py")
        tasks=[t for t in p["projection"]["active"] if t["id"]=="mobile"]
        require(len(tasks)==1 and tasks[0].get("lease"),"Current mobile lease required")
        lease=tasks[0]["lease"]
        require(lease["owner"]=="codex-app-scroll-01a094df","Unexpected parent lease")
        result=call(dict(operation="check",reference=str(ref),task_id="mobile",lease_id=lease["id"],actor=dict(id=lease["owner"],kind="agent"),expected_revision=p["receipt"]["revision"],projection_sha256=p["projection_sha256"]),"mission_cli.py")
        return result

GROUPS=(('testflight_internal','IALD Equipe',1),('testflight_external','IALD Piloto',6))

def digest(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'Duplicate JSON member');result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs)
def validate_distribution(raw):
    r=strict_json(raw)
    require(r.get("status")=="BOTH_GROUPS_TESTING" and r.get("build")=="4.1 (47)" and r.get("notes_saved") is True,"Distribution47 not verified")
    groups=r.get("groups")
    require(isinstance(groups,list) and len(groups)==2,"Both groups required")
    for group,(_,name,count),scope in zip(groups,GROUPS,("internal","external")):
        require(group.get("name")==name and type(group.get("testers")) is int and group["testers"]==count and group.get("type")==scope,"Group mismatch")
        require(group.get("status")=="Em testes" and group.get("build")=="4.1 (47)","Group build not testing")
        require(group.get("expiry_label")=="Expira em 90 dias" and "exact_expiry" in group and group["exact_expiry"] is None,"Exact expiration must remain unknown")
    require(groups[0].get("operator_membership_verified") is True,"Owner membership unverified")
    observed=r.get("observed_utc")
    require(isinstance(observed,str) and datetime.datetime.fromisoformat(observed).utcoffset()==datetime.timedelta(0),"UTC observation required")
    return dict(r,observed_at=observed,expiry_label="Expira em 90 dias")

def member_span(text,start,wanted):
    decoder=json.JSONDecoder();i=start+1
    while True:
        while text[i].isspace() or text[i]==',':i+=1
        if text[i]=='}':raise KeyError(wanted)
        key,end=decoder.raw_decode(text,i);i=end
        while text[i].isspace():i+=1
        require(text[i]==':','Invalid JSON member');i+=1
        while text[i].isspace():i+=1
        value,end=decoder.raw_decode(text,i)
        if key==wanted:return i,end,value
        i=end

def render(raw,receipt_raw):
    r=validate_distribution(receipt_raw);old=strict_json(raw);text=raw.decode('utf-8')
    require(isinstance(old.get('items'),dict),'Administrative items object required')
    items_start,_,_=member_span(text,0,'items');edits=[]
    reference={'path':str(DISTRIBUTION),'sha256':digest(receipt_raw),'bytes':len(receipt_raw)}
    for key,label,count in GROUPS:
        start,end,value=member_span(text,items_start,key)
        require(isinstance(value,dict),'Administrative TestFlight object required')
        require(value.get('build')=='4.1 (46)' and value.get('testers')==count and value.get('label')=='IALD 4.1 (46) — '+label,'Expected build 46 baseline')
        require(value.get('expires_on') is None and value.get('expires_never') is not True,'Competing deadline evidence')
        value.update(expires_at=None,expiry_label=r['expiry_label'],label='IALD 4.1 (47) — '+label,build='4.1 (47)',status='Em testes',testers=count,
            source='Observação direta no App Store Connect: compilação 47 Em testes neste grupo. Expira em 90 dias. Data exata desconhecida.',
            observed_utc=r['observed_at'],source_reference=reference,
            expiry_read_status='EXACT_EXPIRY_UNKNOWN_UI_NOT_EXPOSED',expiry_read_error='Data/hora exatas não informadas; 90 dias relativos não convertidos em prazo.')
        edits.append((start,end,json.dumps(value,ensure_ascii=False,indent=2)))
    after=text
    for start,end,value in sorted(edits,reverse=True):after=after[:start]+value+after[end:]
    parsed=strict_json(after)
    for key,_,_ in GROUPS:old['items'][key]=parsed['items'][key]
    require(old==parsed,'Unexpected administrative semantic change')
    # Verify byte identity outside the two allowed value spans, including CRLF.
    def masked(value):
        start,_,_=member_span(value,0,'items');spans=[member_span(value,start,key)[:2] for key,_,_ in GROUPS]
        for a,b in sorted(spans,reverse=True):value=value[:a]+'<TESTFLIGHT_VALUE>'+value[b:]
        return value.encode('utf-8')
    require(masked(text)==masked(after),'Unrelated administrative bytes changed')
    return after.encode('utf-8')

def new(path,value):
    require(not path.exists(),'Existing receipt/plan; reconcile without overwrite')
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode('utf8')
    temp=path.with_name(path.name+'.tmp_'+str(os.getpid()))
    with temp.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
    require(temp.read_bytes()==raw and not path.exists(),'Staging receipt CAS failed')
    os.rename(temp,path)
    require(path.read_bytes()==raw,'Staging receipt verification failed')

def prepare():
    require(not sys.flags.optimize,'Optimized guards refused')
    receipt_raw=DISTRIBUTION.read_bytes();validate_distribution(receipt_raw)
    check_context()
    raw=TARGET.read_bytes();after=render(raw,receipt_raw)
    require(TARGET.read_bytes()==raw and DISTRIBUTION.read_bytes()==receipt_raw,'Preparation input changed')
    staged=strict_json(after)["items"]
    new(D/"STAGED_OBJECTS.json",{key:staged[key] for key,_,_ in GROUPS})
    new(PLAN,{'status':'READY_AFTER_PARENT_DISTRIBUTION_VERIFICATION','target':str(TARGET),'baseline_sha256':digest(raw),
        'distribution_receipt':str(DISTRIBUTION),'distribution_sha256':digest(receipt_raw),'distribution_bytes':len(receipt_raw),
        'script_sha256':digest(Path(__file__).read_bytes()),'after_sha256':digest(after),'after_bytes':len(after),
        'only_keys':[x[0] for x in GROUPS],'exact_expiry_unknown':True,'not_applied':True,'staged_objects_sha256':digest((D/'STAGED_OBJECTS.json').read_bytes()),'other_bytes_preserved':True})

def apply():
    require(not sys.flags.optimize and os.name=='nt','Windows non-optimized parent execution required')
    plan_raw=PLAN.read_bytes();review_raw=REVIEW.read_bytes();plan=strict_json(plan_raw);review=strict_json(review_raw)
    require(review.get('status')=='PASS' and review.get('reviewer') not in (None,'',AUTHOR),'Independent admin review required')
    require(review.get('plan_sha256')==digest(plan_raw) and review.get('script_sha256')==digest(Path(__file__).read_bytes()),'Admin review pins changed')
    require(plan.get('status')=='READY_AFTER_PARENT_DISTRIBUTION_VERIFICATION','Distribution verification pending')
    require(plan.get('target')==str(TARGET) and plan.get('distribution_receipt')==str(DISTRIBUTION),'Unexpected administrative scope')
    require(plan.get('script_sha256')==digest(Path(__file__).read_bytes()),'Plan script pin changed')
    require(not RESULT.exists(),'Existing application receipt; reconcile, never replay')
    receipt_raw=DISTRIBUTION.read_bytes();validate_distribution(receipt_raw)
    require(digest(receipt_raw)==plan.get('distribution_sha256'),'Distribution receipt changed')
    check_context(applying=True)
    raw=TARGET.read_bytes();require(digest(raw)==plan.get('baseline_sha256'),'Administrative target changed')
    after=render(raw,receipt_raw)
    require(digest((D/'STAGED_OBJECTS.json').read_bytes())==plan['staged_objects_sha256'],'Staged objects changed')
    require(digest(after)==plan.get('after_sha256') and len(after)==plan.get('after_bytes'),'Planned administrative output changed')
    backup=TARGET.with_name(TARGET.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with backup.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
    require(backup.read_bytes()==raw and TARGET.read_bytes()==raw,'Backup/CAS mismatch')
    fd,name=tempfile.mkstemp(dir=TARGET.parent,prefix=TARGET.name+'.tmp_')
    try:
        with os.fdopen(fd,'wb') as out:out.write(after);out.flush();os.fsync(out.fileno())
        require(Path(name).read_bytes()==after and TARGET.read_bytes()==raw,'Administrative CAS mismatch')
        def validate_inputs():
            require(DISTRIBUTION.read_bytes()==receipt_raw and PLAN.read_bytes()==plan_raw and REVIEW.read_bytes()==review_raw,'Reviewed inputs changed')
            require(digest(Path(__file__).read_bytes())==plan['script_sha256'] and backup.read_bytes()==raw,'Writer/backup drift')
        result={'status':'PASS','only_two_testflight_objects_changed':True,'other_text_bytes_preserved':True,'backup_verified':True,
        'backup':str(backup),'baseline_sha256':digest(raw),'after_sha256':digest(after),'plan_sha256':digest(plan_raw),
        'distribution_sha256':digest(receipt_raw),'exact_expiry_unknown':True,'chat_or_public_ui_changed':False}
        result.update(atomic_target_and_receipt=True,protocol='NTFS transaction',review_sha256=digest(review_raw))
        commit_pair(name,raw,after,result,validate_inputs)
    finally:
        if Path(name).exists():Path(name).unlink()

import ctypes
import msvcrt
from ctypes import wintypes

def commit_pair(temp_path, raw, after, result, validate_inputs):
    """Protect the target comparison and commit the new target and receipt together."""
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    ktm=ctypes.WinDLL('ktmw32',use_last_error=True)
    handle=wintypes.HANDLE; dword=wintypes.DWORD; ptr=ctypes.c_void_p
    def bind(dll,name,returns,*args):
        fn=getattr(dll,name);fn.restype=returns;fn.argtypes=args;return fn
    start=bind(ktm,'CreateTransaction',handle,ptr,ptr,dword,dword,dword,dword,wintypes.LPWSTR)
    open_file=bind(kernel,'CreateFileTransactedW',handle,wintypes.LPCWSTR,dword,dword,ptr,dword,dword,handle,handle,ptr,ptr)
    commit=bind(ktm,'CommitTransaction',wintypes.BOOL,handle)
    rollback=bind(ktm,'RollbackTransaction',wintypes.BOOL,handle)
    close=bind(kernel,'CloseHandle',wintypes.BOOL,handle)
    def valid(h):
        if h==handle(-1).value:raise ctypes.WinError(ctypes.get_last_error())
        return h
    tx=valid(start(None,None,0,0,0,30000,None))
    def stream(path,creation):
        # GENERIC_READ|GENERIC_WRITE, FILE_SHARE_READ; no competing write or rename.
        h=valid(open_file(str(path),0xC0000000,1,None,creation,0x80,None,tx,None,None))
        try:fd=msvcrt.open_osfhandle(h,os.O_BINARY|os.O_RDWR)
        except BaseException:close(h);raise
        return os.fdopen(fd,'r+b',buffering=0)
    committed=False
    try:
        with stream(TARGET,3) as target:  # OPEN_EXISTING
            require(target.read()==raw,'Transactional CAS: administrative baseline changed')
            data=Path(temp_path).read_bytes();require(data==after,'Temporary bytes changed')
            target.seek(0);require(target.write(data)==len(data),'Incomplete transaction write')
            target.truncate();os.fsync(target.fileno())
            target.seek(0);require(target.read()==after,'Transaction target mismatch')
        # The NTFS write conflict remains until commit, including after handle close.
        receipt=json.dumps(result,ensure_ascii=False,indent=2).encode('utf8')
        with stream(RESULT,1) as out:  # CREATE_NEW
            require(out.write(receipt)==len(receipt),'Incomplete receipt')
            os.fsync(out.fileno());out.seek(0);require(out.read()==receipt,'Transaction receipt mismatch')
        validate_inputs()
        if not commit(tx):raise ctypes.WinError(ctypes.get_last_error())
        committed=True
    finally:
        if not committed:rollback(tx)
        close(tx)
    require(RESULT.read_bytes()==receipt and TARGET.read_bytes()==after,'Post-commit verification failed')

def main():
    if sys.argv[1:]==['--prepare']:prepare()
    elif sys.argv[1:]==['--apply']:apply()
    else:raise RuntimeError('Staging only. Explicit --prepare after distribution; --apply only after independent ADMIN_REVIEW.')
if __name__=='__main__':main()
