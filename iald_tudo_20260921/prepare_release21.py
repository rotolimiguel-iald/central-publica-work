"""Prepare the completed Selo/Haiku mobile release without changing production."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")
MOBILE = ROOT / "iald-app"
WORK = Path(__file__).resolve().parent
NODE = r"C:\Program Files\nodejs\node.exe"
GIT = r"C:\Program Files\Git\cmd\git.exe"


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    assert path.read_bytes() == raw


def main():
    handoff = (ROOT / "CLAUDE.md").read_text(encoding="utf8")
    conclusion = handoff.rsplit("Claude: CONCLUSÃO — Selo IALD", 1)
    assert len(conclusion) == 2, "Selo completion missing"
    conclusion = conclusion[1]
    source_hashes = {}
    for relative in ["iald_web_server.py", "iald_selo.py", "app/iald.js", "app/index.html", "app/iald.css"]:
        expected = re.search(r"`" + re.escape(relative) + r"` ([0-9a-f]{16})", conclusion)
        assert expected, relative
        digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert digest.startswith(expected[1]), "Source changed since handoff: " + relative
        source_hashes[relative] = digest
    clean = subprocess.check_output([GIT, "-C", str(MOBILE), "status", "--porcelain"], text=True)
    assert not clean.strip(), "Mobile has uncommitted changes"
    stage = WORK / ("release21_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    stage.mkdir()
    tracked = subprocess.check_output([GIT, "-C", str(MOBILE), "ls-files", "www"], text=True).splitlines()
    for relative in tracked:
        create(stage / relative, (MOBILE / relative).read_bytes())
    replacements = {
        "index.html": "index.html", "iald.js": "iald.js", "iald.css": "iald.css",
        "kernel_prompt.js": "kernel_prompt_bundle.js", "kernel_prompt_loja.js": "kernel_prompt_loja.js",
    }
    for name, origin in replacements.items():
        raw = (ROOT / "app" / origin).read_bytes()
        target = stage / "www" / name
        temp = target.with_suffix(target.suffix + ".staged")
        create(temp, raw)
        temp.replace(target)
    for relative in ["capacitor.config.json", "scripts/validate-release.mjs"]:
        create(stage / relative, (MOBILE / relative).read_bytes())
    js = (stage / "www/iald.js").read_text(encoding="utf8")
    for prohibited in ["/api/alertas", "renderDeadlines", "verificarAlertas", "operational_deadlines.js"]:
        assert prohibited not in js, prohibited
    for feature in ["anthropic-native-v1", "motor_selecao", "/api/exportar", "iald_selo_prev", "iald_selo"]:
        assert feature in js, feature
    test = (WORK / "test_haiku_client_context.cjs").read_text(encoding="utf8")
    old = "path.join(__dirname,\n  'claude_routes_stage_20260922_154903_859968', 'iald.js')"
    assert test.count(old) == 1
    create(stage / "test_haiku_client_context.cjs", test.replace(old, "path.join(__dirname, 'www', 'iald.js')").encode("utf8"))
    results = []
    for args in [[NODE, "--check", str(stage / "www/iald.js")],
                 [NODE, str(stage / "scripts/validate-release.mjs")],
                 [NODE, str(stage / "test_haiku_client_context.cjs")]]:
        run = subprocess.run(args, capture_output=True, text=True, encoding="utf8")
        results.append({"command": args[1:], "code": run.returncode, "output": run.stdout.strip()})
        assert run.returncode == 0, run.stdout + run.stderr
    for relative, digest in source_hashes.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    receipt = {"created_at": datetime.now().astimezone().isoformat(), "status": "PREPARED_NOT_PUBLISHED",
               "sources": source_hashes, "ios_build": 21, "android_build": 20,
               "checks": results, "production_modified": False,
               "limitations": ["Native device exports require operator test", "Paid model tests pending"]}
    create(stage / "receipt.json", json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf8"))
    print(json.dumps({"stage": str(stage), "checks": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
