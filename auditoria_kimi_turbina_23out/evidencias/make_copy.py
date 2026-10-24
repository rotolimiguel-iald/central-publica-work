"""Builds the isolated test copy C:\\t\\orq_copia_kimi (code only; NO state, NO secrets, NO production data).
Variants of canonical_memory.py / nos_packet.py / transport_cli.py are taken from the byte backups that sit next to the
production files. The only patch applied to the copy is the redirection of the ACOM state constant to a sandbox folder."""
import hashlib
import shutil
from pathlib import Path

SRC = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
DST = Path(r"C:\t\orq_copia_kimi")
assert str(DST) == r"C:\t\orq_copia_kimi"
if DST.exists():
    shutil.rmtree(DST)
(DST / "iald_orchestrator").mkdir(parents=True)
(DST / "_variants").mkdir()
(DST / "_sandbox" / "acom_state").mkdir(parents=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


n = 0
for p in (SRC / "iald_orchestrator").iterdir():
    if p.is_file() and ".bak" not in p.name and p.suffix in (".py", ".json"):
        shutil.copy2(p, DST / "iald_orchestrator" / p.name)
        n += 1
for p in SRC.iterdir():
    if p.is_file() and ".bak" not in p.name and p.suffix == ".py":
        shutil.copy2(p, DST / p.name)
        n += 1
for name in ("coordinator.json", "jev_body_policy.json", "jev_questions_v1.json", "pricing_mimo_verified.json", "transport.json"):
    shutil.copy2(SRC / name, DST / name)
# the real provenance.json hashes production patent sources; the copy gets an empty pin list instead
(DST / "provenance.json").write_text('{"scope": "COPY-LOCAL TEST FIXTURE (no source pins)", "sources": []}', encoding="utf-8")

IO = SRC / "iald_orchestrator"
V = DST / "_variants"
pairs = {
    "cm_prekimi.py": IO / "canonical_memory.py.bak_20261020_191500_dobra_envelope",
    "cm_kimi.py": IO / "canonical_memory.py.bak_20261021_133553_500586_b50dfd4dd6b34fe282f6257a852a7375",
    "cm_current.py": IO / "canonical_memory.py",
    "nos_old.py": IO / "nos_packet.py.bak_20261021_133553_500586_b50dfd4dd6b34fe282f6257a852a7375",
    "nos_new.py": IO / "nos_packet.py",
    "tcli_old.py": SRC / "transport_cli.py.bak_20261021_133553_500586_b50dfd4dd6b34fe282f6257a852a7375",
    "tcli_new.py": SRC / "transport_cli.py",
}
for k, p in pairs.items():
    shutil.copy2(p, V / k)
    print(k, sha(V / k)[:16], (V / k).stat().st_size)

# sandbox patch (raw strings: backslashes are literal)
target = DST / "iald_orchestrator" / "operational_memory.py"
lines = target.read_text(encoding="utf-8").split("\n")
changed = 0
for i, ln in enumerate(lines):
    if ln.startswith("COMMON_STATE = Path("):
        lines[i] = r"COMMON_STATE = Path(r'C:\t\orq_copia_kimi\_sandbox\acom_state')"
        changed += 1
assert changed == 1
target.write_text("\n".join(lines), encoding="utf-8")
print("copied files:", n, "| sandbox patch lines:", changed)
