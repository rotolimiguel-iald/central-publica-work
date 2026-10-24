import json, os, re, shutil, subprocess, sys
from pathlib import Path
COPY = Path(r"C:\t\orq_copia_kimi")
SP = Path(__file__).resolve().parent
OUT = SP / "saidas" / "fold"
OUT.mkdir(parents=True, exist_ok=True)
V = COPY / "_variants"
env = dict(os.environ)
env["PATH"] = r"C:\Python314;C:\Windows\System32;C:\Windows"
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PYTHONUTF8"] = "1"
for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    env[k] = "http://127.0.0.1:9"
env["NO_PROXY"] = ""
for k in list(env):
    if re.search(r"(KEY|TOKEN|SECRET|PASSWORD|ANTHROPIC|OPENAI|MIMO|KIMI|DEEPSEEK)", k, re.I):
        env.pop(k, None)
sys.path.insert(0, str(SP))
import synth  # noqa: E402
# ensure a synthetic release exists (run_tests.py already built one); rebuild if missing
if not (COPY / "state" / "canonical_memory" / "ACTIVE.json").exists():
    synth.make_active(COPY)
res = {}
for name, f in (("prekimi", "cm_prekimi.py"), ("kimi", "cm_kimi.py"), ("producao_atual", "cm_current.py")):
    shutil.copy2(V / f, COPY / "iald_orchestrator" / "canonical_memory.py")
    p = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", str(SP / "fold_cases.py")], cwd=str(COPY), env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    (OUT / (name + ".stderr.txt")).write_text(p.stderr, encoding="utf-8")
    if p.returncode:
        print(name, "RC", p.returncode, p.stderr[-800:])
        continue
    d = json.loads(p.stdout)
    (OUT / (name + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    res[name] = d
# compact comparison table
labels = [c["case"] for c in res["kimi"]["cases"]] if "kimi" in res else []
for i, lab in enumerate(labels):
    print("\n==", lab)
    for name in ("prekimi", "kimi", "producao_atual"):
        if name not in res:
            continue
        c = res[name]["cases"][i]
        if c["result"] == "REFUSED":
            print("  %-15s REFUSED  %s" % (name, c["message"][:110]))
        else:
            print("  %-15s ACCEPTED folded=%s scope=%s src=%s tot_chars=%s(cap %s over=%s) tot_bytes=%s(lim %s over=%s) notice=%s" % (
                name, c["folded"], c.get("retrieval_scope"), c["n_sources"], c["total_chars_with_reserve"], c.get("char_cap"),
                c.get("exceeds_char_cap_with_reserve"), c["total_bytes_with_reserve"], c["byte_limit"], c["exceeds_byte_limit_with_reserve"], c["has_notice_in_prompt"]))
