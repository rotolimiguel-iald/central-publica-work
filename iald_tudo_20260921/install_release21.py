"""Install only reviewed mobile assets and version numbers; preserve web source."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")
MOBILE = ROOT / "iald-app"
WORK = Path(__file__).resolve().parent
STAGE = WORK / "release21_20260923_083047_956051"
GIT = r"C:\Program Files\Git\cmd\git.exe"


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    assert path.read_bytes() == raw


def main():
    assert not subprocess.check_output([GIT, "-C", str(MOBILE), "status", "--porcelain"]).strip()
    receipt = json.loads((STAGE / "receipt.json").read_text(encoding="utf8"))
    for relative, digest in receipt["sources"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    changed = {"www/" + name: (STAGE / "www" / name).read_bytes() for name in ["iald.js", "index.html", "iald.css"]}
    versions = {"ios/App/App.xcodeproj/project.pbxproj": (b"CURRENT_PROJECT_VERSION = 20;", b"CURRENT_PROJECT_VERSION = 21;", 2),
                "android/app/build.gradle": (b"versionCode 19", b"versionCode 20", 1)}
    for relative, (old, new, count) in versions.items():
        raw = (MOBILE / relative).read_bytes()
        assert raw.count(old) == count, relative
        changed[relative] = raw.replace(old, new)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = MOBILE / ("_backups_release21_" + stamp)
    tracked = subprocess.check_output([GIT, "-C", str(MOBILE), "ls-files"], text=True).splitlines()
    originals = {}
    for relative in tracked:
        if relative.startswith(("www/", "ios/", "android/")):
            originals[relative] = (MOBILE / relative).read_bytes()
            create(backup / relative, originals[relative])
    rows = []
    for relative, raw in changed.items():
        target = MOBILE / relative
        assert target.read_bytes() == originals[relative], relative
        temp = target.with_name(target.name + ".tmp_" + stamp)
        create(temp, raw)
        temp.replace(target)
        assert target.read_bytes() == raw
        rows.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest()})
    out = WORK / ("release21_installed_" + stamp + ".json")
    create(out, json.dumps({"created_at": datetime.now().astimezone().isoformat(),
                           "backup": str(backup), "files": rows, "sync_pending": True,
                           "ios": "4.1 (21)", "android": "4.1 (20)",
                           "web_source_changed": False, "paid_calls": 0}, ensure_ascii=False, indent=2).encode("utf8"))
    print(json.dumps({"receipt": str(out), "files": len(rows), "backup": str(backup)}))


if __name__ == "__main__":
    main()
