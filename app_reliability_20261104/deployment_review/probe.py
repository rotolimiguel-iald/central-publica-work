"""Isolated installer AST probes. No production imports/processes or network."""
import ast
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
INSTALL=WORK/'install_release.py'
PREPARE=WORK/'prepare_release.py'
sources={p.name:p.read_bytes() for p in (INSTALL,PREPARE)}
sha=lambda data:hashlib.sha256(data).hexdigest()
tree=ast.parse(sources[INSTALL.name].decode())
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'main','record'}]


def simulate(mode, optimize=0):
    events=[]
    with tempfile.TemporaryDirectory(dir=HERE,prefix='synthetic-') as tmp:
        base=Path(tmp);root=base/'runtime';root.mkdir();work=base/'work';work.mkdir();(work/'review').mkdir()
        outputs={'first.py':b'new_first=True\n','second.py':b'new_second=True\n'}
        (root/'first.py').write_bytes(b'old_first=True\n')
        (root/'second.py').write_bytes(b'old_second=True\n')
        before={name:(root/name).read_bytes() for name in outputs}
        files=[dict(path=str(root/name),before=sha(before[name]),after=sha(raw)) for name,raw in outputs.items()]
        plan={'files':files,'sources':[]}
        (work/'INSTALL_PLAN.json').write_text(json.dumps(plan))
        review={'status':'REJECTED' if mode=='optimized_rejected_review' else 'PASS',
            'plan_sha256':sha((work/'INSTALL_PLAN.json').read_bytes()),'installer_sha256':sha(sources[INSTALL.name])}
        (work/'review'/'RELEASE_REVIEW.json').write_text(json.dumps(review))
        if mode=='stale_receipt':(work/'MAINTENANCE.json').write_text('{}')
        @contextmanager
        def stopped_web(quiet):
            events.append('web_stopped')
            try:yield {'old_web_pid':1}
            finally:events.append('supervisor_resumed')
        def check():
            events.append('quiesced')
            if mode=='interrupt_second' and events.count('quiesced')==2:raise KeyboardInterrupt('synthetic')
        def protected(path,raw):
            if mode=='write_failure' and '.tmp_' in path.name and path.name.startswith('second'):
                raise OSError('synthetic failure')
            path.write_bytes(raw)
        def replace(a,b):
            os.replace(a,b)
            if mode=='rollback_conflict' and b.name=='first.py' and '.tmp_' in a.name:
                b.write_bytes(b'concurrent_change=True\n')
        def restart(*a,**kw):
            events.append('restart_checked')
            if mode=='restart_failure':raise RuntimeError('synthetic no health')
            return {'status':'PASS'}
        env=dict(W=work,ROOT=root,Path=Path,datetime=datetime,timezone=timezone,json=json,
            os=NS(replace=replace),task=NS(check=lambda name:events.append('preflight') or {'ready':True}),
            sha=sha,staged_bytes=lambda:outputs,quiet=lambda:None,stopped_web=stopped_web,
            assert_quiesced=check,await_restart=restart,protected=protected,
            __file__=str(INSTALL),print=lambda *a,**kw:None)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'<isolated installer>', 'exec', optimize=optimize),env)
        error=None
        try:env['main']()
        except BaseException as exc:error=type(exc).__name__
        return dict(case=mode,optimize=optimize,error=error,events=events,
            files={name:'original' if (root/name).read_bytes()==before[name] else
                'installed' if (root/name).read_bytes()==outputs[name] else 'other'
                for name in outputs},receipts=sorted(p.name for p in work.glob('*.json')))


def main():
    cases=[simulate(mode,optimize) for mode,optimize in [('success',0),('write_failure',0),
        ('rollback_conflict',0),('interrupt_second',0),('stale_receipt',0),
        ('optimized_rejected_review',1),('restart_failure',0)]]
    manifest=WORK/'recovery'/'MANIFEST.json';m=json.loads(manifest.read_text(encoding='utf-8'))
    mismatches=[Path(e['path']).name for e in m['artifacts'] if sha(Path(e['path']).read_bytes())!=e['sha256']]
    report=dict(status='CHANGES_REQUESTED_BEFORE_INSTALL',role='INDEPENDENT_DEPLOYMENT_SCRIPT_REVIEW',
        utc=datetime.now(timezone.utc).isoformat(),sources=[{'path':str(WORK/name),'sha256':sha(raw)} for name,raw in sources.items()],
        current_sources_unchanged=all((WORK/name).read_bytes()==raw for name,raw in sources.items()),
        r2={'manifest_sha256':sha(manifest.read_bytes()),'candidate':m['candidate'],
            'artifacts_checked':len(m['artifacts']),'mismatches':mismatches,
            'author_tests':m['tests']['tests'],'author_replay_of_review_probes':m['reviewer_probes_author_replay']['tests'],
            'independent_r2_acceptance':'NOT_PERFORMED_BY_THIS_REVIEW'},
        no_production_execution=True,no_credentials_read=True,scripts_modified=False,
        probes=cases,
        findings=[
            dict(id='D1',severity='HIGH',file='install_release.py',lines=[68,72,83],
                finding='Interrupted installation or rollback conflict resumes supervisor with a partial release.',
                evidence='interrupt_second leaves first installed/second original; rollback_conflict resumes with first other/second original; both invoke restart.',
                proposal='Durable intent and explicit release state; handle cancellation before resuming; complete verified rollback, otherwise keep admissions stopped with actionable recovery receipt. Do not unconditionally resume partial/conflicted runtime.'),
            dict(id='D2',severity='MEDIUM',file='install_release.py',lines=[38,41,42],
                finding='Safety and approval checks use assert and disappear under Python optimization.',
                evidence='Optimized AST accepted REJECTED review and installed both fixture files, without executing task preflight.',
                proposal='Use explicit if/raise; at minimum reject sys.flags.optimize before any mutating path and document invocation.'),
            dict(id='D3',severity='MEDIUM',file='install_release.py',lines=[52,86],
                finding='Existing evidence filenames are not preflighted before stopping web.',
                evidence='Existing MAINTENANCE.json causes FileExistsError only after web_stopped; supervisor then resumes and restart runs.',
                proposal='Check all receipt destinations before maintenance or use immutable attempt directories and a resumable intent; protect receipts with temp/verify/atomic publication.'),
            dict(id='D4',severity='MEDIUM',file='install_release.py',lines=[85,86],
                finding='Restart health failure leaves installed files and only restart_pending, without a durable failure/recovery receipt.',
                evidence='restart_failure leaves both new files and DEPLOYMENT/MAINTENANCE, no RESTART or recovery record.',
                proposal='Record restart failure with installed pins/process state and defined recovery path; never report successful availability from INSTALLED alone.')],
        positives=['Current prepare checks deadlines before/after hashes',
            'Current source list pins maintenance.py and transaction.py',
            'Reviewed plan/installer hashes checked before maintenance in normal interpreter',
            'Normal fixture write failure restores original bytes',
            'Protected temp/backup ACL-before-write design and server preamble not persisted in staging'],
        limits=['AST installer functions with injected maintenance, storage ACL and process boundaries',
            'No actual plan generation, production import, service stop, runtime write, key read, HTTP or API call',
            'R2 integrity confirmation does not replace Socrates final semantic review'])
    if not report['current_sources_unchanged']:report['status']='STALE_SCRIPTS_CHANGED_DURING_REVIEW'
    (HERE/'REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'r2':report['r2'],'probes':len(cases),'findings':len(report['findings'])}))


if __name__=='__main__':main()
