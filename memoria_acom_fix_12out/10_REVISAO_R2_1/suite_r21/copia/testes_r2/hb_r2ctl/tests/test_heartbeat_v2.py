# -*- coding: utf-8 -*-
"""Suite nova da frente HEARTBEAT (D3, 12/10/2026): req_lib falso em processo, psion sintetico, banco sintetico.

Cada caso roda sobre o trecho REAL do heartbeat da copia modificada (hb_fixture.load_heartbeat). Nenhum provedor,
nenhuma rede, nenhum confidencial: a guarda da auditoria (sitecustomize.py, copia byte a byte) vigia o processo.
"""
import ast
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import hb_fixture as fx
from hb_fixture import memory, MemoryStore, FakeReq, load_heartbeat, r60_payload, seed_psion, seed_health, telemetry_lines

HERE = Path(__file__).resolve().parent
ONE_PROMPT = [{'role': 'user', 'content': 'synthetic-benchmark /no_think'}]


class HeartbeatD3Tests(unittest.TestCase):
    def setUp(self):
        # prefixo \\?\: os nomes do outbox do app (~190 caracteres) estouram MAX_PATH a partir desta pasta (LongPathsEnabled=0)
        self.tmp = tempfile.TemporaryDirectory(dir='\\\\?\\' + str(HERE / 'tmp'))
        self.root = Path(self.tmp.name)
        self.old_root = memory._SHARED_ROOT
        memory._SHARED_ROOT = self.root / 'shared'

    def tearDown(self):
        memory._SHARED_ROOT = self.old_root
        self.tmp.cleanup()

    def ns(self, req, **extra):
        base = dict(HEARTBEAT_PROMPTS=ONE_PROMPT, HEARTBEAT_RUNS_PER_PROMPT=2, _heartbeat_llama_ok=lambda: True)
        base.update(extra)
        return load_heartbeat(self.root, base, req_lib=req)

    # ── D3(a): a medida é só de geração ──────────────────────────────────────────────
    def test_heartbeat_measures_generation_only(self):
        req = FakeReq(delay=0.2, timings=False, completion_tokens=64)
        ns = self.ns(req)
        seed_psion(ns)
        counter = []

        def slow_projection(messages, max_chars=None):
            counter.append(1)
            time.sleep(1.0)
            return messages
        ns['_operational_native_payload'] = lambda payload: (counter.append(1), time.sleep(1.0), payload)[2]
        with mock.patch.object(memory, 'project_messages', side_effect=slow_projection):
            t0 = time.perf_counter()
            measurement = ns['_heartbeat_measure']()
            wall = time.perf_counter() - t0
        self.assertEqual(counter, [])                                   # nenhuma projeção dentro da medida
        self.assertEqual(measurement['status'], 'ok')
        self.assertEqual(len(req.sent), 2)
        for sent in req.sent:
            self.assertEqual(sent, r60_payload(ns, ONE_PROMPT[0]))      # payload idêntico ao regime r60
            self.assertEqual(sent['messages'], [ns['HEARTBEAT_SYSTEM_MESSAGE'], ONE_PROMPT[0]])
            self.assertNotIn('IALD_COMMON_MEMORY', json.dumps(sent))
        for sample in measurement['samples']:
            self.assertTrue(0.2 <= sample['elapsed_s'] <= 0.3)         # só a latência do post
            self.assertEqual(sample['formula'], 'completion_tokens/elapsed')
            self.assertTrue(200 <= sample['tok_s'] <= 330)              # 64 tokens / ~0,2 s
        self.assertLess(wall, 0.9)                                      # as duas amostras somam ~0,4 s; sem o sleep da projeção
        self.assertNotIn('response body', json.dumps(measurement))      # corpos de resposta nunca entram na medida

    def test_heartbeat_tok_s_prefers_server_timings(self):
        ns = self.ns(FakeReq())
        with_timings = fx.llama_body(64, predicted_n=100, predicted_ms=500.0, timings=True)
        self.assertEqual(ns['_heartbeat_tok_s'](with_timings, 9.0), (200.0, 'timings.predicted_n/predicted_ms'))
        without = fx.llama_body(50, 0, 0, timings=False)
        tok, formula = ns['_heartbeat_tok_s'](without, 0.5)
        self.assertEqual((round(tok, 6), formula), (100.0, 'completion_tokens/elapsed'))
        broken = fx.llama_body(50, predicted_n=0, predicted_ms=0, timings=True)   # timings inválidos → cai na fórmula do elapsed
        self.assertEqual(ns['_heartbeat_tok_s'](broken, 0.5)[1], 'completion_tokens/elapsed')
        self.assertEqual(ns['_heartbeat_tok_s'](fx.llama_body(0, 0, 0, timings=False), 0.5), (None, None))
        self.assertEqual(ns['_heartbeat_tok_s']('not a dict', 0.5), (None, None))
        req = FakeReq(delay=0.3, timings=True, predicted_n=128, predicted_ms=400.0)
        ns = self.ns(req, HEARTBEAT_RUNS_PER_PROMPT=1)
        measurement = ns['_heartbeat_measure']()
        self.assertEqual(measurement['samples'][0]['tok_s'], 320.0)      # 128/400 ms, independente da latência de 0,3 s
        self.assertEqual(measurement['formulas'], ['timings.predicted_n/predicted_ms'])

    # ── D3(b): memória comum só por mudança de classe ou 1/hora ───────────────────────
    def test_heartbeat_memory_event_only_on_class_change_or_hourly(self):
        clock = [1_800_000_000.0]
        req = FakeReq(timings=True, predicted_n=100, predicted_ms=1000.0)   # 100 tok/s
        ns = self.ns(req, _heartbeat_clock=lambda: clock[0])
        seed_psion(ns, baseline=100.0, total_beats=10)
        seed_health(ns, 'ok', at=clock[0])
        for _ in range(3):
            clock[0] += 60
            self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        self.assertEqual(fx.memory_events(), 0)                         # 3 batidas ok → 0 eventos
        req.predicted_ms = 2000.0                                       # 50 tok/s → alerta (< 0,8 × baseline)
        clock[0] += 60
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        self.assertEqual(fx.memory_events(), 1)                         # mudança de classe → 1 evento
        clock[0] += 60
        ns['heartbeat_cycle']()
        self.assertEqual(fx.memory_events(), 1)                         # mesma classe, < 1 h → nada
        clock[0] += 61 * 60
        ns['heartbeat_cycle']()
        self.assertEqual(fx.memory_events(), 2)                         # ≥ 1 h → 1 evento
        ledger = fx.health_ledger()
        self.assertEqual(ledger['p']['phase'], 'heartbeat_alerta')
        for record in ledger['q']['records']:
            self.assertEqual((record['kind'], record['statute']), ('fact', 'REAL'))
            self.assertEqual(record['sources'][0]['kind'], 'measurement')
            self.assertTrue(record['sources'][0]['ref'].startswith('heartbeat_telemetry:'))
            self.assertTrue(record['id'].startswith('hb.'))
            self.assertNotIn('response', record['text'])
            self.assertNotIn('choices', record['text'])
            body = json.loads(record['text'])
            self.assertEqual(body['regime'], 'generation_only')
            self.assertEqual(body['class'], 'alerta')
        beats = [l for l in telemetry_lines(ns) if l['kind'] == 'beat']
        self.assertEqual(len(beats), 6)
        events = [l for l in telemetry_lines(ns) if l['kind'] == 'memory_event']
        self.assertEqual([e['event_id'] for e in events], [r['id'] for r in ledger['q']['records']])
        health = ns['_heartbeat_health_load']()
        self.assertEqual((health['class'], health['last_revision']), ('alerta', 2))

    def test_sixty_beats_in_process_zero_or_one_memory_event(self):
        req = FakeReq(timings=True, predicted_n=64, predicted_ms=640.0)   # 100 tok/s
        ns = self.ns(req, HEARTBEAT_TELEMETRY_MAX_BYTES=16384)
        before = seed_psion(ns, baseline=100.0, total_beats=10)
        for i in range(60):
            status = ns['heartbeat_cycle']()
            self.assertEqual(status, 'ok', msg=f'batida {i}: {ns["printed"][-3:]} :: {telemetry_lines(ns)[-1] if telemetry_lines(ns) else None}')
        self.assertEqual(fx.memory_events(), 1)                         # sem estado prévio: 1 evento (classe estabelecida)
        psion = json.loads(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes())
        self.assertEqual(psion['heartbeat']['total_beats'], 70)
        self.assertEqual(psion['generation'], 60)
        self.assertNotEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)
        current = telemetry_lines(ns)
        self.assertTrue(current)
        rotated = [Path(ns['HEARTBEAT_TELEMETRY_FILE'] + f'.{i}') for i in range(1, 6)]
        self.assertTrue(all(p.exists() for p in rotated[:2]))           # 61 linhas de ~700 B com teto de 16 KiB → rotação
        total = sum(len(telemetry_lines(ns, f'.{i}')) for i in range(1, 6) if rotated[i - 1].exists()) + len(current)
        self.assertEqual(total, 61)                                     # 60 beats + 1 memory_event
        # com estado de saúde prévio (classe ok, evento recente) → 0 eventos novos em outras 60 batidas
        for _ in range(60):
            ns['heartbeat_cycle']()
        self.assertEqual(fx.memory_events(), 1)

    def test_heartbeat_failure_does_not_block_next_cycle(self):
        req = FakeReq(status=500)
        ns = self.ns(req)
        seed_psion(ns)
        self.assertEqual(ns['heartbeat_cycle'](), 'no_results')          # HTTP 500 → continue → sem amostra
        self.assertEqual(fx.memory_events(), 1)                         # classe falha estabelecida → 1 evento
        self.assertEqual(fx.health_ledger()['p']['phase'], 'heartbeat_falha')
        req.status = 200
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')                  # o ciclo seguinte roda
        self.assertEqual(fx.memory_events(), 2)                         # falha → ok: mudança de classe
        req.raise_exc = OSError('synthetic timeout')
        self.assertEqual(ns['heartbeat_cycle'](), 'no_results')          # exceção de rede não propaga
        req.raise_exc = None
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        # memória comum indisponível: a batida completa, a telemetria registra, o ciclo seguinte roda
        with mock.patch.object(memory, 'record_measurement', side_effect=OSError('synthetic store failure')):
            req.predicted_ms = 100000.0                                   # alerta → evento devido → falha de gravação
            self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        failed = [l for l in telemetry_lines(ns) if l['kind'] == 'memory_event_failed']
        self.assertEqual(len(failed), 1)
        self.assertEqual(ns['_heartbeat_health_load']()['class'], 'ok')   # classe não avança sem evento gravado
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')                  # tenta de novo: alerta gravado agora
        self.assertEqual(fx.health_ledger()['p']['phase'], 'heartbeat_alerta')

    def test_skipped_busy_and_aborted_user_write_telemetry_only(self):
        ns = self.ns(FakeReq(), _heartbeat_is_idle=lambda: False)
        self.assertEqual(ns['heartbeat_cycle'](), 'skipped_busy')
        ns = self.ns(FakeReq(), _heartbeat_llama_ok=lambda: False)
        self.assertEqual(ns['heartbeat_cycle'](), 'skipped_offline')
        lines = telemetry_lines(ns)
        self.assertEqual([l['status'] for l in lines if l['kind'] == 'beat'], ['skipped_busy', 'skipped_offline'])
        self.assertEqual(fx.memory_events(), 1)                         # só o offline é sinal de saúde (classe falha)
        self.assertIsNone(lines[0]['class'])
        self.assertFalse(Path(ns['HEARTBEAT_STATE_FILE']).exists())     # o psion não foi criado nem tocado

    # ── telemetria rotativa ──────────────────────────────────────────────────────────
    def test_heartbeat_telemetry_rotation(self):
        ns = self.ns(FakeReq(), HEARTBEAT_TELEMETRY_MAX_BYTES=4096)
        for i in range(120):
            ns['_heartbeat_telemetry_append']({'kind': 'beat', 'i': i, 'pad': 'x' * 300})
        path = Path(ns['HEARTBEAT_TELEMETRY_FILE'])
        for i in range(1, 6):
            self.assertTrue(Path(str(path) + f'.{i}').exists())
            self.assertLessEqual(Path(str(path) + f'.{i}').stat().st_size, 4096)
        self.assertFalse(Path(str(path) + '.6').exists())
        self.assertLessEqual(path.stat().st_size, 4096)
        current = telemetry_lines(ns)                                   # cada linha íntegra, sha conferido
        self.assertEqual(current[-1]['i'], 119)
        kept = sorted(l['i'] for s in ['', '.1', '.2', '.3', '.4', '.5'] for l in telemetry_lines(ns, s))
        self.assertEqual(kept, list(range(kept[0], 120)))               # sequência contígua até a linha corrente

    # ── D3(c): psion ────────────────────────────────────────────────────────────────
    def test_psion_save_atomic_and_daily_bak(self):
        ns = self.ns(FakeReq())
        state = Path(ns['HEARTBEAT_STATE_FILE'])
        first = {'beta_tgl': ns['_BETA_TGL'], 'generation': 1, 'heartbeat': {'baseline_tok_s': 90.0}}
        ns['_save_psion_state'](first)
        original = state.read_bytes()
        self.assertEqual(json.loads(original), first)
        self.assertIn(b'\r\n', original)                                # os mesmos bytes do gravador em modo texto (Windows)
        day = time.strftime('%Y%m%d')
        self.assertFalse(Path(str(state) + '.bak_' + day).exists())     # primeira gravação do dia sem arquivo anterior
        ns['_save_psion_state'](dict(first, generation=2))
        ns['_save_psion_state'](dict(first, generation=3))
        baks = sorted(p.name for p in state.parent.glob(state.name + '.bak_*'))
        self.assertEqual(baks, [state.name + '.bak_' + day])            # 1 cópia por dia
        self.assertEqual(Path(str(state) + '.bak_' + day).read_bytes(), original)
        self.assertEqual(json.loads(state.read_bytes())['generation'], 3)
        self.assertEqual(list(state.parent.glob('*.tmp_*')), [])        # nenhum tempário sobrando
        ns['HEARTBEAT_PSION_DAILY_BAK'] = False
        ns['_save_psion_state'](dict(first, generation=4))
        self.assertEqual(len(list(state.parent.glob(state.name + '.bak_*'))), 1)

    def test_degraded_measurement_never_reaches_psion(self):
        ns = self.ns(FakeReq())
        before = seed_psion(ns, baseline=100.0, total_beats=10)
        good = FakeReq(timings=True, predicted_n=50, predicted_ms=1000.0)
        ns['req_lib'] = good
        base = ns['_heartbeat_measure']()
        self.assertEqual(ns['_heartbeat_psion_admissible'](base), (True, 'ok'))
        degraded = json.loads(json.dumps(base))
        degraded['regime'] = 'operational_memory_included'              # o regime de 10/10
        ns['_heartbeat_measure'] = lambda: degraded
        self.assertEqual(ns['heartbeat_cycle'](), 'inadmissible')
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)   # bytes do psion intactos
        foreign = json.loads(json.dumps(base))
        foreign['samples'][0]['payload_sha256'] = '0' * 64              # payload que não é o r60
        ns['_heartbeat_measure'] = lambda: foreign
        self.assertEqual(ns['heartbeat_cycle'](), 'inadmissible')
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)
        noform = json.loads(json.dumps(base))
        noform['samples'][0]['formula'] = None
        ns['_heartbeat_measure'] = lambda: noform
        self.assertEqual(ns['heartbeat_cycle'](), 'inadmissible')
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)
        lines = [l for l in telemetry_lines(ns) if l['kind'] == 'beat']
        self.assertEqual([l['psion'] for l in lines], ['refused_status_or_regime', 'refused_foreign_payload_or_formula',
                                                       'refused_foreign_payload_or_formula'])
        self.assertEqual({l['class'] for l in lines}, {'falha'})
        ns['_heartbeat_measure'] = lambda: base
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')                 # a medida admissível entra
        self.assertNotEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), before)
        self.assertEqual(json.loads(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes())['heartbeat']['total_beats'], 11)
        # ancoragem violada: o psion não é salvo
        broken = ns['_load_psion_state']()
        broken['beta_tgl'] = 0.5
        ns['_save_psion_state'](broken)
        snapshot = Path(ns['HEARTBEAT_STATE_FILE']).read_bytes()
        self.assertEqual(ns['heartbeat_cycle'](), 'anchoring_error')
        self.assertEqual(Path(ns['HEARTBEAT_STATE_FILE']).read_bytes(), snapshot)

    # ── record_measurement e o contexto legado ───────────────────────────────────────
    def test_memory_event_is_fact_real_without_bodies_and_legacy_context_untouched(self):
        req = FakeReq(timings=True, predicted_n=64, predicted_ms=640.0)
        ns = self.ns(req)
        seed_psion(ns)
        store = MemoryStore(memory._SHARED_ROOT)
        legacy_anchor = memory.run_autonomous('native-heartbeat', 'legacy mission of 10/10', lambda: 'legacy-ok')
        legacy_before = store.get(fx.LEGACY_IDENT, fx.SCOPE)
        self.assertEqual(ns['heartbeat_cycle'](), 'ok')
        self.assertEqual(store.get(fx.LEGACY_IDENT, fx.SCOPE)['receipt'], legacy_before['receipt'])   # legado intocado
        ledger = fx.health_ledger()
        self.assertEqual(ledger['scope'], fx.SCOPE)
        self.assertEqual(ledger['constraints']['no_response_bodies'], True)
        self.assertEqual(ledger['constraints']['gate_authority'], False)
        self.assertEqual(ledger['anchor_actor'], {'id': 'service.native-heartbeat', 'kind': 'system'})
        record = ledger['q']['records'][0]
        self.assertEqual((record['kind'], record['statute']), ('fact', 'REAL'))
        self.assertEqual(record['sources'], [{'kind': 'measurement', 'ref': 'heartbeat_telemetry:' + record['id'][3:]}])
        for forbidden in ('synthetic response body', 'choices', 'IALD_COMMON_MEMORY', 'sk-', 'psion_state'):
            self.assertNotIn(forbidden, record['text'])
        self.assertLess(len(record['text']), 600)
        projection = store.project(fx.HEALTH_IDENT, fx.SCOPE)
        self.assertNotIn('response body', projection['text'])

    def test_record_measurement_idempotent_scoped_and_validated(self):
        first = memory.record_measurement('fixture-service', 'fixture objective', '{"x":1}', 'telemetry:abc',
                                          flow={'phase': 'fixture_ok'}, event_id='hb.' + 'a' * 64)
        again = memory.record_measurement('fixture-service', 'fixture objective', '{"x":1}', 'telemetry:abc',
                                          flow={'phase': 'fixture_ok'}, event_id='hb.' + 'a' * 64)
        self.assertEqual((first['revision'], again['revision'], again['replayed']), (1, 1, True))
        other = memory.record_measurement('fixture-service', 'other objective', '{"x":2}', 'telemetry:def', lineage='other')
        self.assertNotEqual(other['context_id'], first['context_id'])
        with self.assertRaises(ValueError):
            memory.record_measurement('fixture-service', 'changed objective', '{"x":3}', 'telemetry:ghi')   # âncora imutável
        with self.assertRaises(ValueError):
            memory.record_measurement('fixture-service', 'fixture objective', '', 'telemetry:x')
        with self.assertRaises(ValueError):
            memory.record_measurement('bad id/with slash', 'fixture objective', 'x', 'telemetry:x')
        with self.assertRaises(ValueError):
            memory.record_measurement('fixture-service', 'fixture objective', 'x', 'telemetry:x',
                                      event_id='hb.' + 'b' * 64, flow={'phase': 'p', 'illegal': 1})
        store = MemoryStore(memory._SHARED_ROOT)
        ledger = store.get(first['context_id'], {'house': 'IALD_APP_SERVICES', 'principal': 'service.fixture-service'})
        self.assertEqual(ledger['q']['records'][0]['statute'], 'REAL')
        with self.assertRaises(ValueError):
            store.get(first['context_id'], {'house': 'IALD_APP', 'principal': 'service.fixture-service'})   # partição

    # ── estática: o heartbeat não tem mais a amarração de 10/10 ──────────────────────
    def test_heartbeat_source_has_no_memory_inside_the_measurement(self):
        source = fx.HEARTBEAT_SOURCE.read_text(encoding='utf-8')
        tree = ast.parse(source)
        funcs = {n.name: ast.get_source_segment(source, n) for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name in ('heartbeat_cycle', '_heartbeat_measure', '_heartbeat_record_memory_if_due'):
            code = ast.unparse(ast.parse(funcs[name]))                  # código sem comentários; docstrings não são chamadas
            for forbidden in ('run_autonomous(', 'tool_result(', '_operational_native_payload(', 'project_messages(',
                              'check_text_window(', '.projection(', 'routing_state('):
                self.assertNotIn(forbidden, code, f'{forbidden} em {name}')
        self.assertNotIn('_heartbeat_cycle_with_memory', funcs)
        self.assertIn('record_measurement', funcs['_heartbeat_record_memory_if_due'])
        self.assertIn('app_memory.project_messages', funcs['_operational_native_payload'])    # mantida para chat/admin
        self.assertIn('app_memory.project_messages', funcs['_prepare_native_payload'])
        self.assertIn('os.replace', funcs['_save_psion_state'])
        self.assertNotIn('open(HEARTBEAT_STATE_FILE, "w")', funcs['_save_psion_state'])
        trigger = funcs['admin_heartbeat_trigger']
        self.assertIn('heartbeat_cycle()', trigger)


if __name__ == '__main__':
    unittest.main(verbosity=2)
