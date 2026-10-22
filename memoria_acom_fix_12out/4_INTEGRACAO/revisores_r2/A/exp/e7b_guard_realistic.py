# -*- coding: utf-8 -*-
"""E7b: realistic input: compact (canonical) JSON of a Windows directory listing, as the app scans canonical(...)."""
import json, time
from common import RUNS, dump
from iald_memory import guard
out = {}
for n in (500, 1000, 2000, 4000):
    B = chr(92); paths = [B.join(['C:', 'IALD', 'projetos_pyhton', 'IALD', 'files', 'arquivo_%05d.txt' % i]) for i in range(n)]
    text = json.dumps({'tool': 'listdir', 'result': paths}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    t0 = time.perf_counter(); r = guard.scan_text(text); dt = time.perf_counter() - t0
    out[n] = {'chars': len(text), 'seconds': round(dt, 3), 'rules': r}
    print(n, out[n], flush=True)
dump(RUNS / 'e7b_guard_realistic.json', out)
