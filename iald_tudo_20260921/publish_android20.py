"""Verify the signed Android20 artifacts and publish only its APK download."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import zipfile

WORK = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")
MOBILE = ROOT / "iald-app"
spec = importlib.util.spec_from_file_location("signing_check", WORK / "verify_android17.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def main():
    apk = MOBILE / "android/app/build/outputs/apk/release/app-release.apk"
    aab = MOBILE / "android/app/build/outputs/bundle/release/app-release.aab"
    metadata = json.loads((apk.parent / "output-metadata.json").read_text())
    assert metadata["applicationId"] == "br.ia.IALD"
    assert metadata["elements"][0]["versionCode"] == 20
    assert metadata["elements"][0]["versionName"] == "4.1"
    signer = helper.certificate(apk)
    assert signer == helper.certificate(ROOT / "downloads/IALD-4.1-19.apk")
    for package, prefix in [(apk, "assets/public/"), (aab, "base/assets/public/")]:
        with zipfile.ZipFile(package) as archive:
            public = [n for n in archive.namelist() if n.startswith(prefix)]
            assert public and not any(any(s in n for s in [".bak_", ".env", ".jks", ".staged"]) for n in public)
            for name in ["iald.js", "iald.css", "index.html"]:
                assert archive.read(prefix + name) == (MOBILE / "www" / name).read_bytes()
            assert b"/api/alertas" not in archive.read(prefix + "iald.js")
    verify = subprocess.run([r"C:\Program Files\Android\Android Studio1\jbr\bin\jarsigner.exe", "-verify", str(aab)],
                            capture_output=True, text=True)
    assert verify.returncode == 0 and "jar verified" in verify.stdout.lower(), "AAB signature check failed"
    target = ROOT / "downloads/IALD-4.1-20.apk"
    raw = apk.read_bytes()
    if target.exists():
        assert target.read_bytes() == raw, "Different APK already published"
    else:
        temp = target.with_name(target.name + ".tmp_release")
        with temp.open("xb") as stream:
            stream.write(raw)
        assert temp.read_bytes() == raw
        temp.replace(target)
    assert target.read_bytes() == raw
    result = {"checked_at": datetime.now().astimezone().isoformat(), "android": "4.1 (20)",
              "certificate_sha256": signer, "same_signer_as_19": True, "aab_signature_verified": True,
              "embedded_assets_match": True, "operational_alerts_absent": True,
              "artifacts": [{"path": str(p), "bytes": p.stat().st_size,
                             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in [apk, aab, target]],
              "google_play": "NOT_UPLOADED_DUNS_PENDING", "physical_test": "PENDING",
              "download_url": "https://demo.iald.ia.br/downloads/IALD-4.1-20.apk",
              "download_access": "Authenticated route; browser download not checked in this script"}
    out = WORK / ("android20_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json")
    with out.open("x", encoding="utf8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({"receipt": str(out), "apk": str(target), "bytes": len(raw)}))


if __name__ == "__main__":
    main()
