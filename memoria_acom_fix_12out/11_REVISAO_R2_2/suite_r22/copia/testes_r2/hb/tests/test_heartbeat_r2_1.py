# -*- coding: utf-8 -*-
"""Testes novos da R2.1 para o heartbeat (revisão R2 §3: `3 != 1`). Rodam sobre o trecho REAL do heartbeat da cópia
(hb_fixture), com psion SINTÉTICO. Um leitor concorrente (open 'rb' do Python: sem FILE_SHARE_DELETE) segura os
arquivos como faria um antivírus/indexador. Em copia_r2 devem FALHAR; em copia, PASSAR."""
import os
import tempfile
import threading
import time
import unittest
from pathlib import Path

import hb_fixture as fx
from hb_fixture import memory, FakeReq, load_heartbeat, seed_psion

HERE = Path(__file__).resolve().parent
ONE_PROMPT = [{'role': 'user', 'content': 'synthetic-benchmark /no_think'}]


class Segura:
    def __init__(self, path, s):
        self.f = open(path, 'rb')
        self.t = threading.Timer(s, self.f.close)
        self.t.start()

    def soltar(self):
        self.t.cancel()
        self.f.close()


class Varredor:
    """Abre (rb) por `hold` s cada arquivo do diretório, em laço — o «varredor» da revisão R2 (s3c), em thread."""

    def __init__(self, root, hold=0.03):
        self.root, self.hold, self.stop = str(root), hold, threading.Event()
        self.aberturas = 0
        self.th = threading.Thread(target=self.run, daemon=True)
        self.th.start()

    def run(self):
        while not self.stop.is_set():
            for dp, _, fs in os.walk(self.root):
                for f in fs:
                    try:
                        with open(os.path.join(dp, f), 'rb') as h:
                            h.read(64)
                            self.aberturas += 1
                            time.sleep(self.hold)
                    except OSError:
                        pass
            time.sleep(0.005)

    def parar(self):
        self.stop.set()
        self.th.join(5)


class HeartbeatR21(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir='\\\\?\\' + str(HERE / 'tmp'))
        self.root = Path(self.tmp.name)
        self.old_root = memory._SHARED_ROOT
        memory._SHARED_ROOT = self.root / 'shared'

    def tearDown(self):
        memory._SHARED_ROOT = self.old_root
        for _ in range(20):
            try:
                self.tmp.cleanup()
                break
            except OSError:
                time.sleep(0.1)

    def ns(self, req, **extra):
        base = dict(HEARTBEAT_PROMPTS=ONE_PROMPT, HEARTBEAT_RUNS_PER_PROMPT=2, _heartbeat_llama_ok=lambda: True)
        base.update(extra)
        return load_heartbeat(self.root, base, req_lib=req)

    def orfaos(self):
        return sorted(p.name for p in self.root.rglob('*.tmp_*'))

    def test_HB1_psion_replace_waits_for_reader(self):
        ns = self.ns(FakeReq(timings=True, predicted_n=64, predicted_ms=640.0))
        seed_psion(ns)
        h = Segura(ns['HEARTBEAT_STATE_FILE'], 0.4)
        try:
            ns['_save_psion_state'](ns['_load_psion_state']())
        finally:
            h.soltar()
        self.assertEqual(self.orfaos(), [])

    def test_HB2_health_replace_waits_for_reader(self):
        ns = self.ns(FakeReq())
        ns['_heartbeat_health_save']({'class': 'ok'})
        h = Segura(ns['HEARTBEAT_HEALTH_FILE'], 0.4)
        try:
            ns['_heartbeat_health_save']({'class': 'alerta'})
        finally:
            h.soltar()
        self.assertEqual(ns['_heartbeat_health_load']().get('class'), 'alerta')
        self.assertEqual(self.orfaos(), [])

    def test_HB3_failed_replace_leaves_no_orphan_temp(self):
        ns = self.ns(FakeReq(), HEARTBEAT_REPLACE_RETRY_S=0.3)
        seed_psion(ns)
        before = Path(ns['HEARTBEAT_STATE_FILE']).read_bytes()
        h = Segura(ns['HEARTBEAT_STATE_FILE'], 3.0)
        try:
            with self.assertRaises(PermissionError):
                ns['_save_psion_state'](ns['_load_psion_state']())
        finally:
            h.soltar()
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)
        self.assertEqual(self.orfaos(), [])

    def test_HB4_rotation_waits_for_reader(self):
        ns = self.ns(FakeReq(), HEARTBEAT_TELEMETRY_MAX_BYTES=200)
        ns['_heartbeat_telemetry_append']({'kind': 'beat', 'n': 1, 'pad': 'x' * 150})
        h = Segura(ns['HEARTBEAT_TELEMETRY_FILE'], 0.4)
        try:
            ns['_heartbeat_telemetry_append']({'kind': 'beat', 'n': 2, 'pad': 'x' * 150})   # rotação com o .jsonl preso
        finally:
            h.soltar()
        self.assertTrue(Path(ns['HEARTBEAT_TELEMETRY_FILE'] + '.1').exists())

    def test_HB5_sixty_beats_with_concurrent_sweeper_one_event(self):
        """O cenário s3c da revisão (varredor que segura cada arquivo 30 ms), em processo: 60 batidas ok, 1 evento."""
        req = FakeReq(timings=True, predicted_n=64, predicted_ms=640.0)
        ns = self.ns(req, HEARTBEAT_TELEMETRY_MAX_BYTES=16384)
        seed_psion(ns, baseline=100.0, total_beats=10)
        v = Varredor(self.root)
        try:
            status = [ns['heartbeat_cycle']() for _ in range(60)]
        finally:
            v.parar()
        self.assertGreater(v.aberturas, 0)
        self.assertEqual([s for s in status if s != 'ok'], [])
        self.assertEqual(fx.memory_events(), 1)
        self.assertEqual(self.orfaos(), [])


if __name__ == '__main__':
    unittest.main()
