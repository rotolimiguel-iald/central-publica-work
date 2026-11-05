"""Seven comparable D1-D4 probes; real AST functions, synthetic files/processes."""
import ast
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
sources={n:(WORK/n).read_bytes() for n in ('install_release.py','maintenance_safe.py','prepare_release.py','INSTALL_PLAN.json')}

def functions(name,exclude=()):
    tree=ast.parse(sources[name])
    return ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name not in exclude],type_ignores=[])

def simulate(mode,optimize=0):
    events=[]
    with tempfile.TemporaryDirectory(dir=HERE,prefix='r2-synthetic-') as tmp:
        base=Path(tmp);root=base/'runtime';root.mkdir();work=base/'work';work.mkdir();(work/'review').mkdir()
        outputs={'first.py':b'new_first=True\n','second.py':b'new_second=True\n'}
        before={name:('old_'+name+'\n').encode() for name in outputs}
        for name,raw in before.items():(root/name).write_bytes(raw)
        rows=[dict(path=str(root/name),before=sha(before[name]),after=sha(raw)) for name,raw in outputs.items()]
        (work/'INSTALL_PLAN.json').write_text(json.dumps({'files':rows,'sources':[]}))
        review={'status':'REJECTED' if optimize else 'PASS','plan_sha256':sha((work/'INSTALL_PLAN.json').read_bytes()),'installer_sha256':sha(sources['install_release.py'])}
        (work/'review/RELEASE_REVIEW.json').write_text(json.dumps(review))
        if mode=='stale_receipt':(work/'MAINTENANCE.json').write_text('{}')
        class Process:
            def __init__(self,pid,script):self.pid=pid;self.script=script;self.stopped=False;self.alive=True
            def cmdline(self):return ['python.exe',str(root/self.script)]
            def create_time(self):return 42
            def status(self):return 'stopped' if self.stopped else 'running'
            def parent(self):return parent
            def suspend(self):self.stopped=True;events.append('suspend_'+str(self.pid))
            def resume(self):self.stopped=False;events.append('resume_'+str(self.pid))
            def terminate(self):self.alive=False;events.append('web_stopped')
            def wait(self,timeout):return 0
        parent=Process(1,'start_iald_web.ps1');child=Process(2,'iald_web_server.py')
        maintenance=dict(ROOT=root,Path=Path,contextmanager=contextmanager,_active=None,
            psutil=NS(STATUS_STOPPED='stopped',NoSuchProcess=ProcessLookupError))
        exec(compile(functions('maintenance_safe.py',('_web_processes','_listeners','await_restart')),'<maintenance AST>','exec'),maintenance)
        maintenance['_web_processes']=lambda:[child] if child.alive else []
        maintenance['_listeners']=lambda:[NS(pid=child.pid)] if child.alive else []
        def protected(path,raw):
            if mode=='write_failure' and '.tmp_reliability_' in path.name and path.name.startswith('second'):
                raise OSError('synthetic write failure')
            path.write_bytes(raw)
            if '.bak_' in path.name:events.append('backup_'+path.name.split('.bak_')[0])
        def replace(a,b):
            if '.tmp_reliability_' in a.name:
                assert all('backup_'+n in events for n in outputs),'all backups must precede mutation'
            os.replace(a,b)
            if b.name=='first.py' and '.tmp_reliability_' in a.name:
                if mode=='interrupt_second':raise KeyboardInterrupt('after replace, before bookkeeping')
                if mode=='rollback_conflict':b.write_bytes(b'concurrent_change=True\n')
        def restart(*a,**kw):
            events.append('restart_checked')
            if mode=='restart_failure':raise RuntimeError('synthetic no health')
            return {'status':'PASS'}
        env=dict(W=work,ROOT=root,Path=Path,datetime=datetime,timezone=timezone,json=json,
            os=NS(replace=replace,link=os.link,fsync=os.fsync),sys=NS(flags=NS(optimize=optimize)),
            task=NS(check=lambda name:events.append('preflight') or {'ready':True}),sha=sha,
            staged_bytes=lambda:outputs,quiet=lambda:None,stopped_web=maintenance['stopped_web'],
            assert_quiesced=maintenance['assert_quiesced'],await_restart=restart,protected=protected,
            __file__=str(WORK/'install_release.py'),print=lambda *a,**kw:None)
        exec(compile(functions('install_release.py',('protected',)),'<installer AST>','exec',optimize=optimize),env)
        error=None
        try:env['main']()
        except BaseException as exc:error=type(exc).__name__
        states={n:'original' if (root/n).read_bytes()==before[n] else 'installed' if (root/n).read_bytes()==outputs[n] else 'other' for n in outputs}
        receipts={p.name:json.loads(p.read_bytes()).get('status') for p in work.glob('*.json') if p.name!='INSTALL_PLAN.json'}
        if mode=='success':passed=error is None and set(states.values())=={'installed'} and receipts.get('RESTART.json')=='PASS'
        elif mode in ('write_failure','interrupt_second'):passed=bool(error) and set(states.values())=={'original'} and receipts.get('RECOVERY.json')=='ROLLED_BACK' and receipts.get('RESTART.json')=='PASS'
        elif mode=='rollback_conflict':passed=bool(error) and states=={'first.py':'other','second.py':'original'} and parent.stopped and 'restart_checked' not in events and receipts.get('RECOVERY.json')=='HOLD_FOR_RECOVERY'
        elif mode in ('stale_receipt','optimized_rejected_review'):passed=bool(error) and set(states.values())=={'original'} and 'suspend_1' not in events
        else:passed=bool(error) and set(states.values())=={'installed'} and receipts.get('RESTART.json')=='FAILED'
        return dict(case=mode,passed=passed,optimize=optimize,error=error,events=events,files=states,receipts=receipts,supervisor_suspended=parent.stopped)

def main():
    probes=[simulate(m,o) for m,o in [('success',0),('write_failure',0),('rollback_conflict',0),('interrupt_second',0),('stale_receipt',0),('optimized_rejected_review',1),('restart_failure',0)]]
    plan=json.loads(sources['INSTALL_PLAN.json'])
    mismatches=[Path(r['path']).name for r in plan['sources'] if sha(Path(r['path']).read_bytes())!=r['sha256']]
    stable=all((WORK/n).read_bytes()==b for n,b in sources.items())
    passed=all(p['passed'] for p in probes) and not mismatches and stable
    result=dict(status='PASS' if passed else 'CHANGES_REQUESTED',scope='D1-D4 and success only; isolated independent fault injection',
        utc=datetime.now(timezone.utc).isoformat(),tests=len(probes),passed=sum(p['passed'] for p in probes),probes=probes,
        plan_sha256=sha(sources['INSTALL_PLAN.json']),installer_sha256=sha(sources['install_release.py']),
        sources=[dict(path=str(WORK/n),sha256=sha(b)) for n,b in sources.items()],
        pinned_plan_sources=len(plan['sources']),pin_mismatches=mismatches,current_sources_unchanged=stable,
        resolved=['D1: BaseException rollback checks every target, including replace-before-bookkeeping; unknown bytes preserved and supervisor held',
                  'D2: explicit optimized execution refusal before mission check or mutation',
                  'D3: all five receipt and temp paths preflighted; fsynced temporary receipt published no-clobber by hardlink; intent before maintenance',
                  'D4: restart exception recorded durably as RESTART.json status FAILED, never availability PASS'],
        limits=['Actual installer and maintenance function ASTs executed with synthetic filesystem and process objects; no production imports, writes, process control, key reads, network or API',
                'ACL command execution and actual supervisor/HTTP startup not exercised; protected bytes writer substituted',
                'Uncatchable process kill/power failure and hostile privileged concurrent writers remain outside these seven comparable probes; durable intent supports manual recovery',
                'This scoped review does not replace final release approval or a real post-install verification'],
        scripts_modified=False)
    dest=HERE/'REVIEW_R2.json'
    with dest.open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':result['status'],'tests':len(probes),'passed':result['passed'],'pin_mismatches':mismatches,'stable':stable}))
    for p in probes:print(json.dumps(p))

if __name__=='__main__':main()
