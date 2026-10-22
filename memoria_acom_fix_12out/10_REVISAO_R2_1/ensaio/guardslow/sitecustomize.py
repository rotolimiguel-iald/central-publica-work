import os, sys, time
exec(compile(open('C:/IALD/Central de Patentes/work/memoria_acom_fix_12out/10_REVISAO_R2_1/suite_r21/copia/guard/sitecustomize.py', encoding="utf-8").read(), 'C:/IALD/Central de Patentes/work/memoria_acom_fix_12out/10_REVISAO_R2_1/suite_r21/copia/guard/sitecustomize.py', "exec"))
_SLOW = float(os.environ.get("SLOW_RENAME_S", "0") or 0)
_MARK = os.environ.get("SLOW_RENAME_MARK", "")
_SRC = os.environ.get("SLOW_RENAME_SRC", ".tmp_")
def _slowhook(ev, args):
    if ev == "os.rename" and _SLOW and _MARK:
        try:
            s, d = os.fsdecode(args[0]), os.fsdecode(args[1])
        except Exception:
            return
        if _MARK.lower() in d.lower() and _SRC in s:
            time.sleep(_SLOW)
sys.addaudithook(_slowhook)
