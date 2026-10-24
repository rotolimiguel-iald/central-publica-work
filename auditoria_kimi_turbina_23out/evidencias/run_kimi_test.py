"""Runs Kimi's own teste_dobra_envelope.py UNMODIFIED in logic against the COPY (BASE redirected; output redirected to scratchpad)
for the pre-Kimi, Kimi and current variants."""
import json, os, re, shutil, subprocess, sys
from pathlib import Path
COPY = Path(r"C:\t\orq_copia_kimi")
SP = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg\ferramentas\teste_dobra_envelope.py")
txt = SRC.read_text(encoding="utf-8")
old_base = 'BASE = Path(r"C:\\IALD\\Central de Patentes\\Chatgpt\\IALD_ORQUESTRACAO_20260923")'
assert old_base in txt, "BASE line not found"
txt = txt.replace(old_base, 'BASE = Path(r"C:\\t\\orq_copia_kimi")')
old_out = 'alvo = Path(__file__).resolve().parents[1] / "teste_dobra_envelope_resultado.json"'
assert old_out in txt, "out line not found"
txt = txt.replace(old_out, 'alvo = Path(r"%s") / "kimi_test_out.json"' % (str(SP / "saidas")).replace("\\", "\\\\"))
patched = SP / "saidas" / "kimi_test_patched.py"
patched.write_text(txt, encoding="utf-8")
env = dict(os.environ)
env["PATH"] = r"C:\Python314;C:\Windows\System32;C:\Windows"
env["PYTHONDONTWRITEBYTECODE"] = "1"
for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
    env[k] = "http://127.0.0.1:9"
for name, f in (("prekimi", "cm_prekimi.py"), ("kimi", "cm_kimi.py"), ("producao_atual", "cm_current.py")):
    shutil.copy2(COPY / "_variants" / f, COPY / "iald_orchestrator" / "canonical_memory.py")
    p = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", str(patched)], cwd=str(COPY), env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    try:
        d = json.loads(p.stdout)
        res = [(t["prova"], t["passou"], {k: v for k, v in t.items() if k not in ("prova", "passou")}) for t in d["testes"]]
    except Exception:
        res = p.stdout[-600:] + p.stderr[-600:]
    print("==", name, "rc", p.returncode)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:1500])
