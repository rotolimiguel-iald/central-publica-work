# -*- coding: utf-8 -*-
"""Testes NOVOS da integração (conserto ACOM 12/10). Rodam sobre as cópias do candidato em `suite/`, com bancos
sintéticos em TEMP (dentro de 4_INTEGRACAO, sob a guarda da auditoria). Nunca o banco de produção.

  1. ponta a ponta: init (CLI de sessões) -> 300 transitions (295 pela lib v2 + 5 pelo CLI) -> project (CLI) -> verify
     (CLI e lib, deep) — mede bytes do banco, do diário, dos instantâneos (locais e «D:») e o tempo por transição;
  2. ensaio de migração: banco v1 sintético com 3 contextos (código v1 congelado, sha256 do store.py instalado),
     dry-run sem mudar bytes, --apply com recibo, cabeças iguais, linhas de `events` byte-iguais, verify deep, transição v2;
  3. o CLI de sessões recusa um banco v1 (fail-closed visível) até a migração;
  4. os merges: __init__.py exporta a união das duas frentes; record_measurement (HEARTBEAT) passa pelo guard (FILTROS)
     ANTES de criar contexto — recusa visível, nada gravado, log sem o trecho.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent              # suite/integracao
SUITE = HERE.parent                                   # suite
TESTES = SUITE.parent                                 # testes
INT = TESTES.parent                                   # 4_INTEGRACAO
CORE = SUITE / 'core'
CLI = SUITE / 'sessions' / 'session_memory.py'
SCRIPTS = TESTES / 'nucleo' / 'copia' / 'MEMORIA_IALD'   # migrar_para_delta.py / mover_backups_antigos.py do candidato
EVID = Path(os.environ.get('INTEGRACAO_EVIDENCIAS', INT / 'evidencias'))
PY = sys.executable
SCOPE = {'house': 'IALD', 'principal': 'operator'}
AGENT = {'id': 'integrador-teste', 'kind': 'agent'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
TEXT = ('heartbeat sample response text ' * 40)[:1200]   # ~1,3 KB canônicos, como na auditoria

sys.path[:0] = [str(CORE), str(HERE)]
import iald_memory  # noqa: E402
from iald_memory import MemoryStore, ContextNotFound  # noqa: E402
import store_v1_frozen  # noqa: E402


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def dir_bytes(p):
    p = Path(p)
    return sum(f.stat().st_size for f in p.rglob('*') if f.is_file()) if p.exists() else 0


def candidate(name, text=TEXT):
    return {'id': name, 'text': text, 'statute': 'DECLARADO', 'source': {'kind': 'executor', 'ref': 'job:' + name}}


def cli(request, store, ok=True, timeout=120):
    proc = subprocess.run([PY, '-X', 'utf8', str(CLI), '--core-root', str(CORE), '--store', str(store)],
                          input=json.dumps(request, ensure_ascii=False).encode('utf-8'), capture_output=True, timeout=timeout)
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    try:
        payload = json.loads(out) if out.strip() else {}
    except ValueError:
        payload = {'raw': out}
    if ok and proc.returncode != 0:
        raise AssertionError('CLI falhou: rc=%d stdout=%s stderr=%s' % (proc.returncode, out[-800:], err[-800:]))
    return proc.returncode, payload, out + err


class IntegracaoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.archive = self.base / 'arquivo_D'
        EVID.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ 1. ponta a ponta
    def test_e2e_init_300_transitions_project_verify(self):
        state = self.base / 'state'
        source = self.base / 'objetivo.txt'
        original = 'Integração 12/10: preservar a inscrição original.\r\nMedir 300 transições.\r\n'.encode('utf-8')
        source.write_bytes(original)
        ref = self.base / 'ref.json'
        rc, init, _ = cli({'operation': 'init', 'objective_file': str(source),
                           'objective_sha256': hashlib.sha256(original).hexdigest(), 'scope': SCOPE, 'actor': AGENT,
                           'request_id': str(uuid.uuid4()), 'write_reference': str(ref),
                           'constraints': {'no_remote_calls': True, 'preserve_original': True}}, state)
        snapshot = init['result']['snapshot']
        context_id = snapshot['context_id']
        self.assertEqual(snapshot['revision'], 0)
        store = MemoryStore(state, snapshot_archive_dir=self.archive)
        times, cli_times = [], []
        n_cli = 5
        for i in range(1, 301):
            changes = {'candidates': [candidate('c%03d' % i)],
                       'flow': {'phase': 'fase_%03d' % i, 'next_action': 'seguir para %d' % (i + 1)}}
            if i % 60 == 0:  # 5 das 300 passam pelo CLI de sessões (processo novo)
                t0 = time.perf_counter()
                cli({'operation': 'transition', 'reference': str(ref), 'expected_revision': i - 1,
                     'event_id': 'ev-%03d' % i, 'actor': AGENT, 'changes': changes}, state)
                cli_times.append(time.perf_counter() - t0)
            else:
                t0 = time.perf_counter()
                store.transition(context_id, SCOPE, expected_revision=i - 1, event_id='ev-%03d' % i, actor=AGENT, changes=changes)
                times.append(time.perf_counter() - t0)
        rc, proj, _ = cli({'operation': 'project', 'reference': str(ref), 'max_chars': 24000}, state)
        projection = proj['result']
        self.assertIn('preservar a inscrição original', projection['text'])
        rc, ver, _ = cli({'operation': 'verify', 'reference': str(ref)}, state)
        verify_cli = ver['result']
        self.assertTrue(verify_cli['ok'])
        self.assertEqual(verify_cli['event_count'], 301)
        t0 = time.perf_counter()
        deep = store.verify(context_id, SCOPE, deep=True)
        t_deep = time.perf_counter() - t0
        self.assertTrue(deep['ok'] and deep['journal_ok'])
        self.assertEqual((deep['legacy_events'], deep['delta_events']), (0, 300))
        self.assertEqual(deep['replay_from_revision'], 0)            # deep=True replaya desde a âncora, por desenho
        self.assertGreaterEqual(verify_cli['replay_from_revision'], 256)   # leitura normal parte do último instantâneo
        got = store.get(context_id, SCOPE)
        self.assertEqual(got['revision'], 300)
        self.assertEqual(got['p']['phase'], 'fase_300')
        self.assertEqual(sum(r['kind'] == 'candidate' for r in got['q']['records']), 300)   # candidatos entram como registros kind='candidate'
        conn = sqlite3.connect(str(state / 'memory.sqlite3'))
        try:
            legacy_state = conn.execute("SELECT count(*) FROM events WHERE revision>0 AND state_json<>''").fetchone()[0]
        finally:
            conn.close()
        baks = sorted(p.name for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
        self.assertEqual(legacy_state, 0)      # D1: nenhum evento carrega estado inteiro
        self.assertEqual(baks, [])             # D2: nenhum backup por mutação
        snaps_local = sorted(p.name for p in (state / 'snapshots').glob('memory.sqlite3.snap_*') if not p.name.endswith('.sha256'))
        snaps_arch = sorted(p.name for p in self.archive.rglob('memory.sqlite3.snap_*') if not p.name.endswith('.sha256')) if self.archive.exists() else []
        self.assertLessEqual(len(snaps_local), 3)
        self.assertEqual(len(snaps_local) + len(snaps_arch), 300 // 50)   # 50 mutações por instantâneo
        per_cent = [statistics.median(times[a:b]) * 1000 for a, b in ((0, 98), (98, 197), (197, 295))]
        numbers = {
            'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'n_transitions': 300, 'n_lib': len(times), 'n_cli': len(cli_times),
            'db_bytes': (state / 'memory.sqlite3').stat().st_size,
            'journal_bytes': dir_bytes(state / 'journal'), 'journal_files': len(list((state / 'journal').glob('*'))),
            'snapshots_local_bytes': dir_bytes(state / 'snapshots'), 'snapshots_local_n': len(snaps_local),
            'snapshots_archive_bytes': dir_bytes(self.archive), 'snapshots_archive_n': len(snaps_arch),
            'transition_ms_median': round(statistics.median(times) * 1000, 2),
            'transition_ms_p90': round(sorted(times)[int(len(times) * 0.9)] * 1000, 2),
            'transition_ms_max': round(max(times) * 1000, 2),
            'transition_ms_median_por_centena': [round(x, 2) for x in per_cent],
            'cli_transition_s_median': round(statistics.median(cli_times), 3),
            'project_chars': projection['actual_chars'], 'project_sha256': projection['projection_sha256'],
            'verify_cli': {k: verify_cli[k] for k in ('ok', 'event_count', 'journal_ok', 'journal_lines', 'replay_from_revision')},
            'verify_deep_seconds': round(t_deep, 3), 'verify_deep': {k: deep[k] for k in ('ok', 'legacy_events', 'delta_events', 'snapshot_rows', 'journal_ok')},
            'sqlite': sqlite3.sqlite_version, 'python': sys.version.split()[0],
        }
        (EVID / 'e2e_n300.json').write_text(json.dumps(numbers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        self.assertLess(numbers['transition_ms_median'], 100)
        self.assertLess(numbers['db_bytes'], 8 * 1024 * 1024)

    # ------------------------------------------------------------------ 2. ensaio de migração
    def build_v1(self, root, sizes=(150, 25, 0)):
        store = store_v1_frozen.MemoryStore(root)
        ids = []
        for k, n in enumerate(sizes):
            cid = 'ctx_%d' % k if k != 1 else 'ctx:1'   # um id com ':' (como os do app)
            store.ensure_context(cid, objective='Objetivo original %d\r\ncom CRLF' % k, scope=SCOPE, actor=OPERATOR,
                                 constraints={'no_remote_calls': True, 'k': k})
            for i in range(1, n + 1):
                changes = {'candidates': [candidate('c%d_%03d' % (k, i))], 'flow': {'phase': 'f%d' % i, 'next_action': 'n'}}
                if i % 7 == 0:
                    changes['records'] = [{'id': 'r%d_%03d' % (k, i), 'kind': 'fact', 'statute': 'REAL',
                                           'text': 'fato %d' % i, 'sources': [{'kind': 'measurement', 'ref': 'm:%d' % i}]}]
                store.transition(cid, SCOPE, expected_revision=i - 1, event_id='e%d_%03d' % (k, i), actor=AGENT, changes=changes)
            ids.append(cid)
        heads = {cid: store.get(cid, SCOPE)['receipt'] for cid in ids}
        return ids, heads

    @staticmethod
    def events_rows(db):
        conn = sqlite3.connect(str(db))
        try:
            return conn.execute('SELECT context_id, revision, event_id, actor_json, changes_json, state_json, state_sha256, '
                                'previous_hash, event_hash, created_at FROM events ORDER BY context_id, revision').fetchall()
        finally:
            conn.close()

    def test_migration_rehearsal_three_contexts(self):
        root = self.base / 'state_v1'
        ids, heads_v1 = self.build_v1(root)
        db = root / 'memory.sqlite3'
        before_bytes, before_sha = db.stat().st_size, sha256_file(db)
        rows_before = self.events_rows(db)
        baks_v1 = sorted(p.name for p in root.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
        self.assertGreater(len(baks_v1), 100)   # a v1 fez um backup integral por mutação
        env = dict(os.environ, PYTHONUTF8='1')
        # dry-run: nada muda
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'migrar_para_delta.py'), '--state', str(root),
                               '--snapshot-archive-dir', str(self.archive)], capture_output=True, env=env, timeout=300)
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        dry = json.loads(proc.stdout.decode('utf-8'))
        self.assertTrue(dry['dry_run'] and not dry['already_migrated'])
        self.assertEqual(sha256_file(db), before_sha)
        self.assertFalse((root / 'journal').exists())
        # apply
        receipt_path = self.base / 'MIGRACAO_RECIBO.json'
        second = self.base / 'pre_v2_D'
        t0 = time.perf_counter()
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'migrar_para_delta.py'), '--state', str(root), '--apply',
                               '--receipt', str(receipt_path), '--second-copy-dir', str(second),
                               '--snapshot-archive-dir', str(self.archive)], capture_output=True, env=env, timeout=600)
        t_apply = time.perf_counter() - t0
        self.assertEqual(proc.returncode, 0, proc.stderr[-1500:])
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        self.assertTrue(receipt['ok'])
        self.assertEqual(receipt['head_mismatches'], [])
        for cid in ids:
            self.assertEqual(receipt['contexts'][cid]['head_state_sha256'], heads_v1[cid]['state_sha256'])
            self.assertEqual(receipt['contexts'][cid]['head_event_hash'], heads_v1[cid]['event_hash'])
            self.assertEqual(receipt['verify_after'][cid]['receipt']['revision'], heads_v1[cid]['revision'])
            self.assertTrue(receipt['verify_after'][cid]['ok'])
        # backup integral antes da migração: bytes e sidecar iguais ao banco original
        bk = Path(receipt['backup']['path'])
        self.assertTrue(bk.exists() and bk.name.startswith('memory.sqlite3.pre_v2_'))
        self.assertEqual(sha256_file(bk), before_sha)
        self.assertEqual(receipt['backup']['sha256'], before_sha)
        self.assertEqual(Path(bk.name + '.sha256', ).name, bk.name + '.sha256')
        self.assertEqual(sha256_file(Path(receipt['backup']['second_copy']['path'])), before_sha)
        # eventos legados byte-iguais; só acrescentou
        self.assertEqual(self.events_rows(db), rows_before)
        # verify-only --deep pelo CLI
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'migrar_para_delta.py'), '--state', str(root), '--verify-only',
                               '--deep', '--snapshot-archive-dir', str(self.archive)], capture_output=True, env=env, timeout=300)
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        ver = json.loads(proc.stdout.decode('utf-8'))
        self.assertTrue(ver['ok'])
        # idempotente
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'migrar_para_delta.py'), '--state', str(root), '--apply',
                               '--snapshot-archive-dir', str(self.archive)], capture_output=True, env=env, timeout=300)
        again = json.loads(proc.stdout.decode('utf-8'))
        self.assertTrue(again['already_migrated'])
        # transição v2 em cada contexto, recibos e get iguais à v1 antes dela
        store = MemoryStore(root, snapshot_archive_dir=self.archive)
        for cid in ids:
            got = store.get(cid, SCOPE)
            self.assertEqual(got['receipt']['state_sha256'], heads_v1[cid]['state_sha256'])
            r = store.transition(cid, SCOPE, expected_revision=got['revision'], event_id='v2_' + cid.replace(':', '_'),
                                 actor=AGENT, changes={'flow': {'phase': 'pos_migracao', 'next_action': 'ok'}})
            self.assertEqual(r['revision'], got['revision'] + 1)
            v = store.verify(cid, SCOPE, deep=True)
            self.assertTrue(v['ok'] and v['journal_ok'])
            self.assertEqual((v['legacy_events'], v['delta_events']), (heads_v1[cid]['revision'], 1))
        # o código v1 congelado recusa o banco migrado (fail-closed)
        with self.assertRaises(ValueError):
            store_v1_frozen.MemoryStore(root)
        # o arquivador dos backups legados: dry-run não move; keep 3 move o resto com manifesto
        dest = self.base / 'backups_D'
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'mover_backups_antigos.py'), '--state', str(root), '--dest', str(dest),
                               '--keep', '3', '--dry-run'], capture_output=True, env=env, timeout=300)
        plan = json.loads(proc.stdout.decode('utf-8'))
        self.assertEqual(plan['to_move'], len(baks_v1) - 3)
        self.assertFalse(dest.exists())
        proc = subprocess.run([PY, '-X', 'utf8', str(SCRIPTS / 'mover_backups_antigos.py'), '--state', str(root), '--dest', str(dest),
                               '--keep', '3'], capture_output=True, env=env, timeout=600)
        moved = json.loads(proc.stdout.decode('utf-8'))
        self.assertTrue(moved['ok'])
        self.assertEqual(moved['moved'], len(baks_v1) - 3)
        left = sorted(p.name for p in root.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
        self.assertEqual(left, baks_v1[-3:])
        manifest = json.loads((dest / 'MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['moved'], moved['moved'])
        numbers = {
            'contexts': {cid: {'events_v1': heads_v1[cid]['revision']} for cid in ids},
            'db_bytes_before': before_bytes, 'db_bytes_after_migration': receipt['after']['db_bytes'] if 'db_bytes' in receipt.get('after', {}) else db.stat().st_size,
            'db_bytes_now': db.stat().st_size, 'journal_bytes': dir_bytes(root / 'journal'),
            'journal_lines_written': receipt['journal_lines_written'], 'migration_seconds_cli': round(t_apply, 3),
            'migration_seconds_internal': receipt['seconds'], 'legacy_backups_found': len(baks_v1), 'legacy_backups_moved': moved['moved'],
            'legacy_backups_bytes_moved': moved['moved_bytes'], 'backup_pre_v2': receipt['backup']['path'],
            'verify_after': {cid: receipt['verify_after'][cid]['ok'] for cid in ids},
        }
        (EVID / 'migracao_ensaio_3ctx.json').write_text(json.dumps(numbers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    # ------------------------------------------------------------------ 3. CLI recusa v1
    def test_sessions_cli_refuses_v1_database_until_migrated(self):
        root = self.base / 'state_v1b'
        ids, _ = self.build_v1(root, sizes=(2, 0, 0))
        rc, payload, text = cli({'operation': 'get', 'context_id': ids[0], 'scope': SCOPE}, root, ok=False)
        self.assertNotEqual(rc, 0)
        self.assertIn('migra', text.lower())
        before = sha256_file(root / 'memory.sqlite3')
        rc, payload, text = cli({'operation': 'transition', 'context_id': ids[0], 'scope': SCOPE, 'expected_revision': 2,
                                 'event_id': 'x', 'actor': AGENT, 'changes': {'flow': {'phase': 'p', 'next_action': 'n'}}}, root, ok=False)
        self.assertNotEqual(rc, 0)
        self.assertEqual(sha256_file(root / 'memory.sqlite3'), before)

    # ------------------------------------------------------------------ 4. merges
    def test_merged_init_exports_union_of_both_fronts(self):
        v1 = {'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound', 'ScopeViolation', 'AnchorConflict',
              'RevisionConflict', 'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow', 'InvariantViolation'}
        self.assertTrue(v1 <= set(iald_memory.__all__))
        self.assertTrue({'SchemaMigrationRequired', 'ConfidentialContent', 'guard'} <= set(iald_memory.__all__))
        self.assertTrue(issubclass(iald_memory.SchemaMigrationRequired, iald_memory.IntegrityError))
        self.assertTrue(issubclass(iald_memory.ConfidentialContent, iald_memory.MemoryError))
        for name in iald_memory.__all__:
            self.assertTrue(hasattr(iald_memory, name), name)
        self.assertTrue(callable(iald_memory.guard.assert_clean_text))

    def test_record_measurement_passes_through_guard_before_any_write(self):
        sys.path[:0] = [str(SUITE / 'app')]
        import iald_app_memory as memory
        from iald_memory import ConfidentialContent
        old = memory._SHARED_ROOT
        memory._SHARED_ROOT = self.base / 'shared'
        try:
            secret = 'sk-' + 'A' * 40
            with self.assertRaises(ConfidentialContent) as ctx:
                memory.record_measurement('native-heartbeat', 'Medir tok/s', 'avg 12.3 ' + secret, 'heartbeat_telemetry:abc',
                                          lineage='health')
            self.assertNotIn(secret, str(ctx.exception))
            self.assertFalse((self.base / 'shared' / 'memory.sqlite3').exists())   # nada criado: o guard roda antes do banco
            log = (self.base / 'shared' / 'guard_refusals.jsonl')
            self.assertTrue(log.exists())
            self.assertNotIn(secret, log.read_text(encoding='utf-8'))
            self.assertIn('app.record_measurement:native-heartbeat', log.read_text(encoding='utf-8'))
            # caminho do Escritório como texto também é recusado; texto limpo entra como fact/REAL
            with self.assertRaises(ConfidentialContent):
                memory.record_measurement('native-heartbeat', 'Medir tok/s', r'lido de C:\Escritorio\x.txt', 'heartbeat_telemetry:abd', lineage='health')
            receipt = memory.record_measurement('native-heartbeat', 'Medir tok/s', '{"class":"ok","avg_tok_s":90.1}',
                                                'heartbeat_telemetry:abe', lineage='health', flow={'phase': 'heartbeat_ok', 'next_action': 'n'})
            self.assertEqual(receipt['revision'], 1)
            store = MemoryStore(self.base / 'shared', snapshot_archive_dir=self.archive)
            got = store.get(receipt['context_id'], {'house': 'IALD_APP_SERVICES', 'principal': 'service.native-heartbeat'})
            self.assertEqual(got['q']['records'][0]['statute'], 'REAL')
            self.assertEqual(got['p']['phase'], 'heartbeat_ok')
            with self.assertRaises(ContextNotFound):
                store.get('app_service_' + memory.digest('native-heartbeat'), {'house': 'IALD_APP_SERVICES', 'principal': 'service.native-heartbeat'})
        finally:
            memory._SHARED_ROOT = old


if __name__ == '__main__':
    unittest.main()
