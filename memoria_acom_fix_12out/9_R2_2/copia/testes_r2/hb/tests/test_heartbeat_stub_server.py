# -*- coding: utf-8 -*-
"""Servidor de modelo FALSO (stub local, sem llama) + banco sintetico: 60 batidas (D3, 12/10/2026).

O stub e um adaptador de transporte do `requests` (hb_fixture.StubLlama): o heartbeat chama req_lib.post/get
de verdade, o `requests` monta o pedido HTTP, o stub le os BYTES do corpo e responde no formato do llama.cpp.
Nenhum socket e aberto; a guarda da auditoria roda byte a byte.
"""
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import hb_fixture as fx
from hb_fixture import memory, StubLlama, load_heartbeat, r60_payload, seed_psion, seed_health, telemetry_lines

HERE = Path(__file__).resolve().parent


class StubServerTests(unittest.TestCase):
    def setUp(self):
        # prefixo \\?\: os nomes do outbox do app (~190 caracteres) estouram MAX_PATH a partir desta pasta (LongPathsEnabled=0)
        self.tmp = tempfile.TemporaryDirectory(dir='\\\\?\\' + str(HERE / 'tmp'))
        self.root = Path(self.tmp.name)
        self.old_root = memory._SHARED_ROOT
        memory._SHARED_ROOT = self.root / 'shared'

    def tearDown(self):
        memory._SHARED_ROOT = self.old_root
        self.tmp.cleanup()

    def ns(self, stub, **extra):
        """Namespace real do heartbeat: _heartbeat_llama_ok e _heartbeat_is_idle REAIS, req_lib = sessão do stub."""
        return load_heartbeat(self.root, extra, llama_url=stub.url, req_lib=stub.session())

    def test_sixty_beats_stub_server_zero_or_one_memory_event(self):
        stub = StubLlama(timings=True, predicted_n=64, predicted_ms=640.0)     # 100,0 tok/s por timings
        ns = self.ns(stub, HEARTBEAT_TELEMETRY_MAX_BYTES=32768)
        seed_psion(ns, baseline=100.0, total_beats=10)
        counter = []
        with mock.patch.object(memory, 'project_messages', side_effect=lambda m, **k: counter.append(1) or m), \
             mock.patch.object(memory, 'tool_result', side_effect=lambda *a, **k: counter.append(1)), \
             mock.patch.object(memory, 'run_autonomous', side_effect=lambda *a, **k: counter.append(1)):
            statuses = [ns['heartbeat_cycle']() for _ in range(60)]
        self.assertEqual(statuses, ['ok'] * 60)
        self.assertEqual(counter, [])                                           # memória nunca dentro da batida
        self.assertEqual(fx.memory_events(), 1)                                 # 60 batidas → 1 evento (classe estabelecida)
        posts = [r for r in stub.requests if r['method'] == 'POST']
        healths = [r for r in stub.requests if r['method'] == 'GET']
        self.assertEqual(len(posts), 60 * len(ns['HEARTBEAT_PROMPTS']) * ns['HEARTBEAT_RUNS_PER_PROMPT'])
        self.assertEqual(len(healths), 60)
        for post in posts:                                                      # bytes do corpo == payload r60
            index = [p['content'] for p in ns['HEARTBEAT_PROMPTS']].index(post['body']['messages'][1]['content'])
            self.assertEqual(post['body'], r60_payload(ns, ns['HEARTBEAT_PROMPTS'][index]))
            self.assertEqual(post['content_type'], 'application/json')
            self.assertEqual(post['timeout'], 60)
            self.assertNotIn('IALD_COMMON_MEMORY', json.dumps(post['body']))
        all_lines = sum((telemetry_lines(ns, s) for s in ['.5', '.4', '.3', '.2', '.1', '']), [])
        beats = [l for l in all_lines if l['kind'] == 'beat']
        self.assertEqual(len(beats), 60)
        for beat in beats:                                                      # tok/s medido só da geração (timings)
            self.assertEqual(beat['regime'], 'generation_only')
            self.assertEqual(beat['formula'], 'timings.predicted_n/predicted_ms')
            self.assertEqual(beat['avg_tok_s'], 100.0)
            self.assertEqual(beat['psion'], 'updated')
            self.assertEqual(beat['class'], 'ok')
            self.assertTrue(all(s['tok_s'] == 100.0 and s['formula'] == 'timings.predicted_n/predicted_ms' for s in beat['samples']))
        psion = json.loads(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes())
        self.assertEqual((psion['heartbeat']['total_beats'], psion['generation']), (70, 60))
        self.assertEqual(psion['heartbeat']['baseline_tok_s'], 100.0)
        self.assertEqual(psion['heartbeat']['alerts'], [])
        self.assertTrue(Path(ns['HEARTBEAT_TELEMETRY_FILE'] + '.1').exists())    # rotação aconteceu com o teto de 32 KiB
        events = [l for l in all_lines if l['kind'] == 'memory_event']
        self.assertEqual(len(events), 1)
        ledger = fx.health_ledger()
        self.assertEqual(ledger['revision'], 1)
        self.assertEqual(ledger['p']['phase'], 'heartbeat_ok')
        self.assertEqual(ledger['q']['records'][0]['id'], events[0]['event_id'])
        # variante com estado de saúde prévio (classe ok, evento recente): 60 batidas → 0 eventos novos
        ns2 = self.ns(StubLlama(timings=True, predicted_n=64, predicted_ms=640.0), HEARTBEAT_LOG_DIR=str(self.root / 'logs2'),
                      HEARTBEAT_TELEMETRY_FILE=str(self.root / 'logs2' / 't.jsonl'), HEARTBEAT_HEALTH_FILE=str(self.root / 'logs2' / 'h.json'),
                      HEARTBEAT_STATE_FILE=str(self.root / 'psion_synthetic_state_2.json'))
        seed_psion(ns2, baseline=100.0, total_beats=10)
        seed_health(ns2, 'ok')
        before = fx.memory_events()
        self.assertEqual([ns2['heartbeat_cycle']() for _ in range(60)], ['ok'] * 60)
        self.assertEqual(fx.memory_events(), before)

    def test_stub_without_timings_measures_only_the_generation_window(self):
        stub = StubLlama(delay=0.2, timings=False, predicted_n=64, completion_tokens=64)
        ns = self.ns(stub, HEARTBEAT_PROMPTS=[{'role': 'user', 'content': 'stub-benchmark /no_think'}], HEARTBEAT_RUNS_PER_PROMPT=2)
        seed_psion(ns, baseline=250.0, total_beats=10)
        slow = []

        def slow_projection(messages, max_chars=None):
            slow.append(1)
            time.sleep(1.0)
            return messages
        with mock.patch.object(memory, 'project_messages', side_effect=slow_projection):
            self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        self.assertEqual(slow, [])
        beat = [l for l in telemetry_lines(ns) if l['kind'] == 'beat'][0]
        self.assertEqual(beat['formula'], 'completion_tokens/elapsed')
        for sample in beat['samples']:
            self.assertTrue(0.2 <= sample['elapsed_s'] <= 0.3)                 # a janela é só o post ao stub
            self.assertTrue(210 <= sample['tok_s'] <= 330)
        self.assertEqual(beat['class'], 'ok')

    def test_stub_http_500_then_offline_then_recovers_without_blocking(self):
        stub = StubLlama(status=500)
        ns = self.ns(stub, HEARTBEAT_PROMPTS=[{'role': 'user', 'content': 'stub-benchmark /no_think'}], HEARTBEAT_RUNS_PER_PROMPT=1)
        before = seed_psion(ns, baseline=100.0, total_beats=10)
        self.assertEqual(ns['heartbeat_cycle'](), 'no_results')
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)   # falha nunca toca o psion
        self.assertEqual(fx.memory_events(), 1)
        self.assertEqual(fx.health_ledger()['p']['phase'], 'heartbeat_falha')
        stub.health_status = 503
        self.assertEqual(ns['heartbeat_cycle'](), 'skipped_offline')            # /health real do stub
        self.assertEqual(fx.memory_events(), 1)                                 # mesma classe (falha), < 1 h
        stub.health_status, stub.status = 200, 200
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')                         # recupera sem conciliação
        self.assertEqual(fx.memory_events(), 2)
        self.assertEqual(fx.health_ledger()['p']['phase'], 'heartbeat_ok')
        beats = [l['status'] for l in telemetry_lines(ns) if l['kind'] == 'beat']
        self.assertEqual(beats, ['no_results', 'skipped_offline', 'ok'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
