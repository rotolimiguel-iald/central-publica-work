# -*- coding: utf-8 -*-
"""E7: cost of the D4 content scan on large/adversarial texts (scan_text runs before writes and before projections)."""
import json, time
from common import RUNS, dump
from iald_memory import guard
cases = {}
def t(label, text):
    t0 = time.perf_counter(); rules = guard.scan_text(text); dt = time.perf_counter() - t0
    cases[label] = {'chars': len(text), 'seconds': round(dt, 4), 'rules': rules}
    print(label, cases[label], flush=True)
t('plain_1MB', 'texto comum da memoria ' * 45000)
for n in (2000, 8000, 32000):
    t('drive_letters_%d' % n, 'a:/' * n)
    t('drive_path_deep_%d' % n, 'c:/' + 'pasta/' * n + 'x')
    t('words_colon_%d' % n, 'ab:/cd ' * n)
t('json_like_1MB', json.dumps([{'k': 'v' * 50, 'path': 'C:/IALD/x/y/z/arquivo.txt'}] * 15000))
dump(RUNS / 'e7_guard_perf.json', cases)
