from pathlib import Path
from datetime import datetime
import os

p = Path(__file__).resolve().parent / "CharacterPrefixStability.lean"
raw = p.read_bytes()
backup = p.with_name(p.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as f:
    f.write(raw); f.flush(); os.fsync(f.fileno())
assert backup.read_bytes() == raw
s = raw.decode("utf-8")
replacements = [
    ("    convert h using 1 <;> ring", "    convert h using 1\n    ring"),
    ("  simp only [digitTerm, hu, hv, Bool.false_eq_true, if_false, if_true]\n  unfold siteGap",
     "  have du : digitTerm (geometricContrast t) u n = 0 := by simp [digitTerm, hu]\n"
     "  have dv : digitTerm (geometricContrast t) v n = geometricContrast t n := by simp [digitTerm, hv]\n"
     "  rw [du, dv]\n  unfold siteGap"),
    ("      le_abs_self (binaryCode (geometricContrast t) v - binaryCode (geometricContrast t) u))",
     "      (le_abs_self (binaryCode (geometricContrast t) v - binaryCode (geometricContrast t) u)))"),
    ("    simpa only [SamePrefix, not_forall, not_implies] using hnot",
     "    unfold SamePrefix at hnot\n    push_neg at hnot\n    exact hnot")
]
for old, new in replacements:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
out = s.encode("utf-8")
temp = p.with_name(p.name + ".tmp_fix")
with temp.open("xb") as f:
    f.write(out); f.flush(); os.fsync(f.fileno())
assert temp.read_bytes() == out and len(out) > len(raw)
os.replace(temp, p)
assert p.read_bytes() == out
print(backup.as_posix())
