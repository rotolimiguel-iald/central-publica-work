"""Apply an independently requested domain clarification with an immediate byte backup."""
from pathlib import Path
from datetime import datetime
import os

folder = Path(__file__).resolve().parent
target = folder / "REEXAME_ATUALIZADO.md"
before = target.read_bytes()
old = "Com a = `recordCharacter(t,R)` e t ≠ 0, essa leitura".encode()
new = "Para U não vazio, com a = `recordCharacter(t,R)` e t ≠ 0, essa leitura".encode()
assert before.count(old) == 1
after = before.replace(old, new)
assert len(after) > len(before)
backup = target.with_name(target.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as stream:
    stream.write(before); stream.flush(); os.fsync(stream.fileno())
assert backup.read_bytes() == before
temp = target.with_name(target.name + ".tmp_domain")
with temp.open("xb") as stream:
    stream.write(after); stream.flush(); os.fsync(stream.fileno())
assert temp.read_bytes() == after and target.read_bytes() == before
os.replace(temp, target)
assert target.read_bytes() == after and backup.read_bytes() == before
print("Domain clarification applied; immediate byte backup preserved.")
