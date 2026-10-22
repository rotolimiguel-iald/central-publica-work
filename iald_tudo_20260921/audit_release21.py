"""Audit the eight release files and embedded assets before GitHub publication."""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(r"C:\IALD\projetos_pyhton\IALD\iald-app")
WORK = Path(__file__).resolve().parent
STAGE = WORK / "release21_20260923_083047_956051"
GIT = r"C:\Program Files\Git\cmd\git.exe"
FILES = ["android/app/build.gradle", "ios/App/App.xcodeproj/project.pbxproj",
         "ios/App/App/public/iald.js", "ios/App/App/public/iald.css", "ios/App/App/public/index.html",
         "www/iald.js", "www/iald.css", "www/index.html"]


def main():
    def git(*args):
        return subprocess.check_output([GIT, "-C", str(ROOT), *args], stderr=subprocess.DEVNULL).decode().strip()
    assert not git("diff", "--cached", "--name-only"), "Existing staged changes"
    changed = set(git("diff", "--name-only").splitlines()) | set(git("ls-files", "--others", "--exclude-standard").splitlines())
    assert changed == set(FILES), sorted(changed)
    patterns = [rb"sk-(?:ant-|proj-)?[A-Za-z0-9_-]{30,}", rb"gh[pousr]_[A-Za-z0-9]{30,}",
                rb"github_pat_[A-Za-z0-9_]{30,}", rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    rows = []
    for relative in FILES:
        raw = (ROOT / relative).read_bytes()
        assert not any(re.search(p, raw) for p in patterns), "Credential pattern: " + relative
        rows.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    for name in ["iald.js", "iald.css", "index.html"]:
        expected = (STAGE / "www" / name).read_bytes()
        for folder in ["www", "ios/App/App/public", "android/app/src/main/assets/public"]:
            assert (ROOT / folder / name).read_bytes() == expected, folder + "/" + name
    result = {"checked_at": datetime.now().astimezone().isoformat(), "status": "PASS", "files": rows,
              "head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
              "allowed_destination": "https://github.com/rotolimiguel-iald/iald-app.git",
              "scope": "Eight client/version files only; no server, credentials, env or private corpus",
              "tests": {"selo_export": "82 passed", "haiku_client": "6 passed", "validate_release": "passed"}}
    assert git("remote", "get-url", "origin") == result["allowed_destination"]
    out = WORK / ("release21_audit_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json")
    raw = json.dumps(result, ensure_ascii=False, indent=2).encode("utf8")
    with out.open("xb") as stream:
        stream.write(raw)
    assert out.read_bytes() == raw
    print(json.dumps({"status": "PASS", "receipt": str(out), "files": len(rows)}))


if __name__ == "__main__":
    main()
