import time, os, tempfile
from pathlib import Path
d = Path(tempfile.mkdtemp(dir=str(Path(__file__).resolve().parents[2] / "tmp")))
f = d / 'j.jsonl'; f.write_bytes(b'x' * 600_000)
def cycle(read_tail):
    t_open = t_read = 0.0
    for _ in range(40):
        with f.open('ab') as h:
            h.write(b'{"line":1}\n'); h.flush(); os.fsync(h.fileno())
        if read_tail:
            t0 = time.perf_counter()
            h = f.open('rb')
            t1 = time.perf_counter()
            h.seek(-4096, 2); h.read(); h.close()
            t2 = time.perf_counter()
            t_open += t1 - t0; t_read += t2 - t1
    return round(t_open * 1000 / 40, 3), round(t_read * 1000 / 40, 3)
print('after append: open rb ms, read 4KB ms =', cycle(True))
t0 = time.perf_counter()
for _ in range(40): os.stat(f)
print('stat ms', round((time.perf_counter() - t0) * 1000 / 40, 3))
t0 = time.perf_counter()
for _ in range(40):
    with f.open('ab') as h: h.write(b'{"line":1}\n'); h.flush(); os.fsync(h.fileno())
print('append+fsync only ms', round((time.perf_counter() - t0) * 1000 / 40, 3))
