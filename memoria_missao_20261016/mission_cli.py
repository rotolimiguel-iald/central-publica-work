"""Local mission synchronization; same ACOM store, JSON stdin, no providers."""
from pathlib import Path
import argparse, importlib.util, json, sys


def main():
    base=Path(__file__).resolve().parent
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--core-root',type=Path,default=base/'lib')
    p.add_argument('--store',type=Path,default=base/'state')
    p.add_argument('--session-adapter',type=Path,default=base/'session_memory.py')
    args=p.parse_args()
    sys.path.insert(0,str(args.core_root.resolve()))
    try:
        from iald_memory import MemoryStore,guard
        from iald_memory.mission import MissionController,MissionError
        spec=importlib.util.spec_from_file_location('session_adapter',args.session_adapter)
        adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
        raw=sys.stdin.buffer.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise MissionError('request_too_large')
        request=json.loads(raw.decode('utf-8'))
        guard.assert_clean_text(json.dumps(request,ensure_ascii=False),'mission_cli.request')
        root=args.store.resolve()
        if not (root/'memory.sqlite3').is_file():raise MissionError('memory_store_missing')
        ref=adapter.reference_for(request,root)
        store=MemoryStore(root)
        snap=store.get(ref['context_id'],ref['scope'])
        if ref.get('objective_sha256')!=snap['objective_sha256']:raise MissionError('reference_anchor_mismatch')
        ctl=MissionController(store,ref['context_id'],ref['scope'])
        op=request.get('operation')
        if op=='project':result=ctl.project(request.get('max_chars',24000))
        elif op=='poll':result=ctl.poll(request['after_revision'],request.get('wait_ms',0),request.get('max_chars',24000))
        elif op=='check':result=ctl.check(request)
        elif op=='handoff':result=ctl.handoff(request)
        elif op=='get':result=store.get(ref['context_id'],ref['scope'])
        else:result=ctl.action(request)
        guard.assert_clean_text(json.dumps(result,ensure_ascii=False,allow_nan=False),'mission_cli.result')
        print(json.dumps({'ok':True,'protocol':'iald-mission/v1','result':result},ensure_ascii=False,allow_nan=False))
        return 0
    except Exception as exc:
        print(json.dumps({'ok':False,'error':type(exc).__name__,'message':str(exc)},ensure_ascii=False))
        return 2


if __name__=='__main__':raise SystemExit(main())
