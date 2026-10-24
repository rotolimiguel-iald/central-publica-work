"""Runs the four orchestrator test modules inside the COPY (C:\\t\\orq_copia_kimi) for several
canonical_memory variants. Isolation: copy-local code, sandboxed ACOM state, no provider CLIs on
PATH, dead proxy for any network call. Never touches production code or state for writing."""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

COPY = Path(r"C:\t\orq_copia_kimi")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
PY = r"C:\Python314\python.exe"
MODULES = ["test_canonical_memory", "test_request_controls", "test_coordination", "test_transport"]

CONFIGS = {
    "B0_hoje_prekimi": ("cm_prekimi.py", "nos_new.py", "tcli_new.py"),
    "B1_hoje_kimi": ("cm_kimi.py", "nos_new.py", "tcli_new.py"),
    "B2_hoje_producao": ("cm_current.py", "nos_new.py", "tcli_new.py"),
    "A0_20out_prekimi": ("cm_prekimi.py", "nos_old.py", "tcli_old.py"),
    "A1_20out_kimi": ("cm_kimi.py", "nos_old.py", "tcli_old.py"),
}
only = sys.argv[2:] or list(CONFIGS)


def install(cm, nos, tcli):
    V = COPY / "_variants"
    shutil.copy2(V / cm, COPY / "iald_orchestrator" / "canonical_memory.py")
    shutil.copy2(V / nos, COPY / "iald_orchestrator" / "nos_packet.py")
    shutil.copy2(V / tcli, COPY / "transport_cli.py")
    for pyc in COPY.rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)


env = dict(os.environ)
env["PATH"] = r"C:\Python314;C:\Python314\Scripts;C:\Windows\System32;C:\Windows"
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PYTHONUTF8"] = "1"
for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    env[k] = "http://127.0.0.1:9"
env["NO_PROXY"] = ""
env["no_proxy"] = ""
for k in list(env):
    if re.search(r"(KEY|TOKEN|SECRET|PASSWORD|ANTHROPIC|OPENAI|MIMO|KIMI|DEEPSEEK)", k, re.I):
        env.pop(k, None)

# sandbox fixtures: synthetic sealed memory (no production data) + empty provenance (no production hashes)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import synth  # noqa: E402
if (COPY / "state").exists():
    shutil.rmtree(COPY / "state")
release, manifest = synth.make_active(COPY)
(COPY / "provenance.json").write_text(json.dumps({"scope": "COPY-LOCAL TEST FIXTURE (no source pins)", "sources": []}), encoding="utf-8")
print("synthetic active release:", release.name)

summary = {}
for name in only:
    cm, nos, tcli = CONFIGS[name]
    install(cm, nos, tcli)
    res = {}
    for mod in MODULES:
        t0 = time.time()
        try:
            p = subprocess.run([PY, "-B", "-X", "utf8", "-m", "unittest", mod, "-v"], cwd=str(COPY), env=env,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
            out = p.stdout + "\n--STDERR--\n" + p.stderr
            rc = p.returncode
        except subprocess.TimeoutExpired as e:
            out = "TIMEOUT\n" + str(e.stdout)[-3000:]
            rc = -9
        (OUT / f"{name}__{mod}.txt").write_text(out, encoding="utf-8")
        m = re.search(r"Ran (\d+) tests? in ([\d.]+)s", out)
        ok = "\nOK" in out
        f = re.search(r"FAILED \((.*?)\)", out)
        res[mod] = {"rc": rc, "ran": int(m.group(1)) if m else None, "ok": ok,
                    "failed": f.group(1) if f else None, "secs": round(time.time() - t0, 1)}
        print(name, mod, res[mod], flush=True)
    summary[name] = res
(OUT / ("summary_" + "_".join(only)[:60] + ".json")).write_text(json.dumps(summary, indent=1), encoding="utf-8")
print(json.dumps(summary, indent=1))
