import time, os, tempfile, sys
from pathlib import Path
def bench(d, label):
    d = Path(d); d.mkdir(parents=True, exist_ok=True)
    f = d / 'x.bin'; f.write_bytes(b'0' * 600_000)
    def t(fn, n=50):
        t0 = time.perf_counter()
        for _ in range(n): fn()
        return round((time.perf_counter() - t0) * 1000 / n, 3)
    def rplus():
        with f.open('r+b') as h: h.seek(0, 2); h.write(b'x'); h.flush(); os.fsync(h.fileno())
    def rplus_nofsync():
        with f.open('r+b') as h: h.seek(0, 2); h.write(b'x')
    def ab():
        with f.open('ab') as h: h.write(b'x')
    def rb():
        with f.open('rb') as h: h.read(1024)
    def tmpw():
        p = d / 'p.tmp'
        with p.open('wb') as h: h.write(b'{}'); h.flush(); os.fsync(h.fileno())
        os.replace(p, d / 'p.json')
    print(label, 'rb', t(rb), 'ab', t(ab), 'r+b-nofsync', t(rplus_nofsync), 'r+b+fsync', t(rplus), 'tmp+fsync+replace', t(tmpw))
bench(Path(__file__).resolve().parent / 'bench_here', 'NUCLEO/tmp  ')
bench(Path(os.environ.get('LOCALAPPDATA')) / 'Temp' / 'iald_bench', 'LOCALAPPDATA')
