# -*- coding: utf-8 -*-
"""Revisor R2, item 3: mecanismo da intermitencia 'test_sixty_beats_in_process_zero_or_one_memory_event' (3 != 1).

Roda o MESMO cenario do teste (60 batidas sem estado previo + 60 com estado) sobre o trecho real do heartbeat da
copia (hb_fixture, candidato R2), com UMA falha transitoria injetada na segunda serie, em cada ponto de E/S do ciclo:
  F1  os.replace do psion falha uma vez (PermissionError, como sob um leitor concorrente/antivirus no Windows)
  F2  _heartbeat_health_load devolve {} uma vez (leitura transitoria falha)
  F3  os.replace do health falha uma vez (depois do evento gravado)
  F4  leitor concorrente REAL: uma thread mantem o arquivo do psion aberto (open() do CPython: sem FILE_SHARE_DELETE)
      durante uma batida -- sem mock
Conta os eventos na memoria comum (fx.memory_events()). Sem rede, sem provedor; tudo em TEMP da copia.
"""
import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from unittest import mock

HB_TESTS = Path(__file__).resolve().parents[1] / 'copia' / 'testes_r2' / 'hb' / 'tests'
sys.path.insert(0, str(HB_TESTS))
import hb_fixture as fx  # noqa: E402
from hb_fixture import memory, FakeReq, load_heartbeat, seed_psion  # noqa: E402

ONE_PROMPT = [{'role': 'user', 'content': 'synthetic-benchmark /no_think'}]
REAL_REPLACE = os.replace


def cenario(inject=None, beat_to_inject=30):
    tmpd = tempfile.TemporaryDirectory(dir='\\\\?\\' + str(HB_TESTS / 'tmp'))
    root = Path(tmpd.name)
    old = memory._SHARED_ROOT
    memory._SHARED_ROOT = root / 'shared'
    try:
        req = FakeReq(timings=True, predicted_n=64, predicted_ms=640.0)
        ns = load_heartbeat(root, dict(HEARTBEAT_PROMPTS=ONE_PROMPT, HEARTBEAT_RUNS_PER_PROMPT=2,
                                       _heartbeat_llama_ok=lambda: True, HEARTBEAT_TELEMETRY_MAX_BYTES=16384), req_lib=req)
        seed_psion(ns, baseline=100.0, total_beats=10)
        statuses1 = [ns['heartbeat_cycle']() for _ in range(60)]
        ev1 = fx.memory_events()
        statuses2, errors = [], []
        for i in range(60):
            ctx = None
            if i == beat_to_inject and inject:
                ctx = inject(ns)
            try:
                if ctx is not None:
                    with ctx:
                        statuses2.append(ns['heartbeat_cycle']())
                else:
                    statuses2.append(ns['heartbeat_cycle']())
            except Exception as exc:  # noqa: BLE001
                statuses2.append('EXC:' + type(exc).__name__)
                errors.append(repr(exc)[:200])
        ev2 = fx.memory_events()
        non_ok = [(i, s) for i, s in enumerate(statuses2) if s != 'ok']
        return {'eventos_serie1': ev1, 'eventos_apos_serie2': ev2, 'novos_na_serie2': ev2 - ev1,
                'nao_ok_serie2': non_ok, 'excecoes': errors, 'printed_tail': ns['printed'][-4:],
                'teste_original_passaria': ev1 == 1 and ev2 == 1 and all(s == 'ok' for s in statuses1)}
    finally:
        memory._SHARED_ROOT = old
        tmpd.cleanup()


def once_replace(match):
    state = {'done': False}

    def fake(src, dst, *a, **kw):
        if not state['done'] and str(dst).endswith(match):
            state['done'] = True
            try:
                os.remove(src)
            except OSError:
                pass
            raise PermissionError(13, 'injected: sharing violation (reader holds the file)', str(dst))
        return REAL_REPLACE(src, dst, *a, **kw)
    return mock.patch('os.replace', side_effect=fake)


class _HealthOnce:
    def __init__(self, ns):
        self.ns = ns
        self.orig = ns['_heartbeat_health_load']

    def __enter__(self):
        calls = {'n': 0}
        orig = self.orig

        def flaky():
            calls['n'] += 1
            return {} if calls['n'] == 1 else orig()
        self.ns['_heartbeat_health_load'] = flaky

    def __exit__(self, *exc):
        self.ns['_heartbeat_health_load'] = self.orig
        return False


class _RealReader:
    """A concurrent reader that keeps the psion file open while one beat runs (no mock)."""
    def __init__(self, ns):
        self.path = ns['HEARTBEAT_STATE_FILE']
        self.stop = threading.Event()
        self.t = None

    def _run(self):
        while not self.stop.is_set():
            try:
                with open(self.path, 'rb') as f:
                    f.read(16)
                    time.sleep(0.05)
            except OSError:
                time.sleep(0.001)

    def __enter__(self):
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t.start()
        time.sleep(0.02)

    def __exit__(self, *exc):
        self.stop.set()
        self.t.join(2)
        return False


def main():
    out = {}
    out['controle_sem_injecao'] = cenario(None)
    out['F1_replace_psion_falha_1x'] = cenario(lambda ns: once_replace('psion_synthetic_state.json'))
    out['F2_health_load_vazio_1x'] = cenario(lambda ns: _HealthOnce(ns))
    out['F3_replace_health_falha_1x'] = cenario(lambda ns: once_replace('iald_heartbeat_health.json'))
    out['F4_leitor_real_concorrente_no_psion'] = cenario(lambda ns: _RealReader(ns))
    dst = Path(__file__).resolve().parents[1] / 'runs' / 's3_heartbeat_injecao.json'
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: {kk: v[kk] for kk in ('novos_na_serie2', 'nao_ok_serie2', 'excecoes', 'teste_original_passaria')}
                      for k, v in out.items()}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
