# -*- coding: utf-8 -*-
"""Common helpers for the adversarial review A (robustness and growth). Writes only under 5_REVISAO_A."""
from __future__ import annotations
import hashlib
import json
import os
import sys
import time
from pathlib import Path

EXP = Path(__file__).resolve().parent
REV = EXP.parent
LIB = REV / 'int' / 'candidato' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib'
MEM_CAND = REV / 'int' / 'candidato' / 'C' / 'IALD' / 'MEMORIA_IALD'
V1 = REV / 'int' / 'testes' / 'suite' / 'integracao'
RUNS = EXP / 'runs'
sys.path.insert(0, str(LIB))

SCOPE = {'house': 'IALD', 'principal': 'revisao_a'}
AGENT = {'id': 'revisor.a', 'kind': 'agent'}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def dir_bytes(p):
    p = Path(p)
    if not p.exists():
        return 0, 0
    n = s = 0
    for x in p.rglob('*'):
        if x.is_file():
            n += 1
            s += x.stat().st_size
    return n, s


def record(i, size=300, kind='fact'):
    text = ('registro %d da revisao A; ' % i) + ('x' * max(0, size - 30))
    r = {'id': 'r%05d' % i, 'kind': kind, 'text': text,
         'statute': 'DECLARADO' if kind == 'candidate' else 'REAL',
         'sources': [{'kind': 'artifact', 'ref': 'exp/%d' % i}]}
    return r


def pct(values, q):
    v = sorted(values)
    if not v:
        return None
    k = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
    return v[k]


def dump(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(path) + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    os.replace(tmp, path)
