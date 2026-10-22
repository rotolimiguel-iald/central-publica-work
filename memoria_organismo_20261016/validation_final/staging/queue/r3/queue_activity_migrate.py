"""Local OS-authenticated migration CLI; intentionally NOT registered as MCP."""
import json,sys
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.legacy_activity_migration import invoke
from iald_orchestrator import operational_memory as om

def main():
    try:
        result=invoke(Runtime(recover=False),json.load(sys.stdin))
        reply={'ok':True,'result':result}
        om.core().guard.assert_clean_text(om.encode(reply),'queue.migration.cli')
        print(json.dumps(reply,ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'ok':False,'error':type(exc).__name__,'message':str(exc)},ensure_ascii=False))
        return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
