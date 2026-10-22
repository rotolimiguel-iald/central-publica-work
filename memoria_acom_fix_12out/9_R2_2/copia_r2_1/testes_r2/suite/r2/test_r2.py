# -*- coding: utf-8 -*-
"""Testes NOVOS da R2 (achados bloqueantes da revisão de 13/10). Rodam sobre as cópias do candidato_r2 em suite/.

  achado 2 — o filtro D4 (guard.scan_text) é linear: os casos E7/E7b da revisão A e os F da revisão B, mais uma
             bateria adversarial por regra (~1 MB cada); e a decisão é a MESMA do R1 em toda forma que o R1 conhecia
             (fuzz contra as regras do R1 extraídas do guard R1), só acrescentando c:escritorio e %5c/%2f.
  achado 4 — session_memory.py: write_reference e reference passam pelo guard ANTES de exists/read/create; um JSON
             com nome confidencial (sintético, criado aqui) nunca é aberto; chave estranha é recusada sem eco.
  revisão B (t3/E) — dois contextos que diferem só na caixa têm diários distintos e ambos verificam.
Os achados 1 e 3 (implantar/reverter/processos) são ensaiados em ensaio_implantacao_r2/rodar_ensaio_r2.py.
"""
from __future__ import annotations
import hashlib
import json
import os
import random
import re
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent          # suite/r2
SUITE = HERE.parent
TESTES = SUITE.parent
INT = TESTES.parent
EVID = Path(os.environ.get('INTEGRACAO_EVIDENCIAS', INT / 'evidencias_r2'))
sys.path[:0] = [str(SUITE / 'core'), str(SUITE / 'sessions'), str(HERE)]

from iald_memory import MemoryStore, ContextNotFound, guard  # noqa: E402
import session_memory as sm  # noqa: E402
from perf_inputs import inputs, listing  # noqa: E402

B = chr(92)
RESULTS = {}


def r1_rules():
    """As regras de conteúdo do guard R1, lidas do arquivo R1 (cópia byte a byte em suite/r2)."""
    text = (HERE / 'guard_r1_referencia.py').read_text(encoding='utf-8')
    block = text[text.index('_CONTENT_RULES = ('):text.index('def scan_text')]
    ns = {}
    exec('import re, json\n' + block, ns)
    return ns['_CONTENT_RULES'], ns['_ESCRITORIO_PATH']


R1_RULES, R1_ESC = r1_rules()
NEW_FORMS = re.compile(r'(?:%5c|%2f|\b[a-z]:)escritorio')


def scan_r1(text):
    rules = [n for n, p in R1_RULES if p.search(text)]
    if R1_ESC.search(guard.fold(text)):
        rules.append('escritorio_path')
    return rules


def timed(text):
    t0 = time.perf_counter()
    r = guard.scan_text(text)
    return time.perf_counter() - t0, r


class GuardLinearTests(unittest.TestCase):
    def test_review_A_E7b_listing_4000_paths_was_71s(self):
        text = listing(4000)
        dt, rules = timed(text)
        RESULTS['E7b_4000_paths'] = {'chars': len(text), 'seconds': round(dt, 4), 'rules': rules, 'r1_declarado_s': 71.237}
        self.assertEqual(rules, [])
        self.assertLess(dt, 1.0)

    def test_review_A_E7_drive_letters_32000_was_43s(self):
        text = 'a:/' * 32000
        dt, rules = timed(text)
        RESULTS['E7_a_colon_slash_32000'] = {'chars': len(text), 'seconds': round(dt, 4), 'r1_declarado_s': 43.33}
        self.assertLess(dt, 1.0)

    def test_key_pem_regex_was_also_quadratic_and_now_is_linear(self):
        text = 'a-' * 32000      # R1: 23 s medidos na integração R2 (64 KB)
        dt, rules = timed(text)
        RESULTS['key_pem_a_hyphen_32000'] = {'chars': len(text), 'seconds': round(dt, 4)}
        self.assertEqual(rules, [])
        self.assertLess(dt, 1.0)

    def test_adversarial_battery_one_megabyte_each(self):
        out = {}
        for label, text in inputs().items():
            dt, rules = timed(text)
            out[label] = {'chars': len(text), 'seconds': round(dt, 4), 'rules': rules}
            self.assertLess(dt, 5.0, label)
        RESULTS['bateria_1MB'] = out

    def test_growth_is_linear_not_quadratic(self):
        out = {}
        for label, make in {'listing': lambda k: listing(k), 'a_colon': lambda k: 'a:/' * (15 * k),
                            'a_hyphen': lambda k: 'a-' * (25 * k), 'deep_path': lambda k: 'c:' + (B + 'ab') * (16 * k)}.items():
            small, big = make(4000), make(16000)
            ts = min(timed(small)[0] for _ in range(3))
            tb = min(timed(big)[0] for _ in range(3))
            out[label] = {'chars_small': len(small), 'chars_big': len(big), 's_small': round(ts, 5), 's_big': round(tb, 5),
                          'razao': round(tb / max(ts, 1e-6), 2)}
            self.assertLess(tb / max(ts, 1e-4), 9.0, label)   # 4x o tamanho: linear ~4, quadrático ~16
        RESULTS['crescimento_4x'] = out

    def test_same_decision_as_r1_on_every_r1_form(self):
        rnd = random.Random(20261013)
        alpha_r1 = ['a', 'Z', '-', '.', 'key', 'pem', 'KEY', ' ', B, '/', 'escritorio', 'Escritório', '_', '"', ',', '.env',
                    'x9', 'sk-', 'AIza', 'ghp_', 'xoxb-', 'bearer ', 'iald_psion_state', 'iald_stack_v7', B + B, 'é']
        alpha_all = alpha_r1 + ['c:', 'C:', ':', '%5c', '%2F', 'file:///']
        n_same = n_extra = 0
        for alpha, n in ((alpha_r1, 30000), (alpha_all, 30000)):
            for _ in range(n):
                t = ''.join(rnd.choice(alpha) for _ in range(rnd.randint(1, 16)))
                a, b = scan_r1(t), guard.scan_text(t)
                if a == b:
                    n_same += 1
                    continue
                # a única diferença admitida: escritorio_path a mais, e só se o texto tem uma das formas novas
                self.assertTrue(set(a) <= set(b), (t, a, b))
                self.assertEqual(set(b) - set(a), {'escritorio_path'}, (t, a, b))
                self.assertTrue(NEW_FORMS.search(guard.fold(t)), (t, a, b))
                self.assertEqual([x for x in b if x != 'escritorio_path'], [x for x in a if x != 'escritorio_path'])
                n_extra += 1
                self.assertIs(alpha, alpha_all, 'sem as formas novas a decisão tem de ser idêntica')
        RESULTS['equivalencia_r1'] = {'casos': 60000, 'iguais': n_same, 'so_formas_novas': n_extra}

    def test_review_B_content_table(self):
        fake_sk = 'sk-proj-' + 'A1b2C3d4E5f6G7h8I9j0K1l2M3n4'
        expect = {
            'chave ' + fake_sk: ['openai_key'],
            'C:' + B + 'Escritorio' + B + 'processos': ['escritorio_path'],
            json.dumps({'p': 'C:' + B + 'Escritorio'}): ['escritorio_path'],
            'file:///C:/Escritorio/x': ['escritorio_path'],
            'C:Escritorio' + B + 'x': ['escritorio_path'],              # R1: [] (forma nova)
            'C%3A%5CEscritorio%5Cprocessos': ['escritorio_path'],       # R1: [] (forma nova)
            '\uff23\uff1a\uff3c\uff25\uff53\uff43\uff52\uff49\uff54\uff4f\uff52\uff49\uff4f': ['escritorio_path'],
            'a casa Escritorio fica separada': [],
            'nota:escritorio sem caminho': [],
            'Confidenciais nunca saem: iald_stack_v7.py, iald_psion_state.json, tokens, .env': ['psion_name', 'stack_name', 'dotenv_name'],
            'use record.key e self.pem para indexar': ['key_pem_name'],
            '--.key': [],
        }
        for text, rules in expect.items():
            self.assertEqual(guard.scan_text(text), rules, text)


class SessionReferenceTests(unittest.TestCase):
    """Achado 4: o arquivo do write_reference/reference é decidido pelo guard ANTES de exists/read/create."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='r2_ref_', dir=os.environ.get('TEMP')))
        self.store_root = (self.tmp / 'state').resolve()
        self.store_root.mkdir()
        self.obj = self.tmp / 'objetivo.txt'
        self.obj.write_bytes('Objetivo sintetico limpo da R2.\n'.encode('utf-8'))
        self.sha = hashlib.sha256(self.obj.read_bytes()).hexdigest()
        self.rid = str(uuid.uuid4())
        self.scope = {'house': 'IALD', 'principal': 'r2'}
        self.ctx = str(uuid.uuid5(uuid.NAMESPACE_URL, 'iald-memory-session:' + json.dumps([self.scope, self.rid], sort_keys=True, separators=(',', ':'))))
        self.opened = []
        tmp_s = str(self.tmp)

        def hook(event, args):
            if event == 'open' and args and isinstance(args[0], str) and args[0].startswith(tmp_s):
                self.opened.append(args[0])
        sys.addaudithook(hook)   # não removível: filtra só este diretório temporário

    def req(self, write_reference):
        return {'operation': 'init', 'objective_file': str(self.obj), 'objective_sha256': self.sha, 'scope': self.scope,
                'request_id': self.rid, 'actor': {'id': 'r2', 'kind': 'agent'}, 'write_reference': str(write_reference)}

    def identity(self, **extra):
        d = {'protocol': sm.PROTOCOL, 'store': str(self.store_root), 'context_id': self.ctx, 'scope': self.scope,
             'objective_sha256': self.sha, 'request_id': self.rid}
        d.update(extra)
        return d

    def test_confidential_named_reference_is_never_opened(self):
        conf = self.tmp / 'iald_psion_state_32B.json'      # SINTÉTICO, criado aqui; o teste nunca o lê
        conf.write_text(json.dumps(self.identity(CANARY_SECRET='FAKE_SYNTHETIC_CANARY')), encoding='utf-8')
        self.opened.clear()
        with self.assertRaises(sm.ProtocolError) as cm:
            sm.dispatch(self.req(conf), self.store_root, MemoryStore)
        self.assertEqual(str(cm.exception), 'source_path_not_allowed:psion_name')
        self.assertNotIn('CANARY', str(cm.exception))
        self.assertFalse([o for o in self.opened if o.endswith('iald_psion_state_32B.json')], self.opened)
        with self.assertRaises(ContextNotFound):        # recusado antes de qualquer gravação
            MemoryStore(self.store_root).get(self.ctx, self.scope)
        log = (self.store_root / sm.GUARD_LOG_NAME).read_text(encoding='utf-8')
        self.assertIn('psion_name', log)
        self.assertNotIn('CANARY', log)
        RESULTS['t3_C_write_reference'] = {'resultado': str(cm.exception), 'aberto': False, 'contexto_criado': False}

    def test_backup_suffix_and_case_variants_refused(self):
        # '.env' e 'iald_psion_state.json' exatos: a guarda da auditoria nem deixa CRIAR o arquivo (bloqueio da guarda, não do código)
        for name in ('IALD_PSION_STATE_32B.JSON', 'iald_psion_state_32B.json.bak_20261010_092000', 'x.pem', 'chave.key.bak_1'):
            path = self.tmp / name
            path.write_text('{}', encoding='utf-8')
            self.opened.clear()
            with self.assertRaises(sm.ProtocolError) as cm:
                sm.dispatch(self.req(path), self.store_root, MemoryStore)
            self.assertTrue(str(cm.exception).startswith('source_path_not_allowed:'), (name, str(cm.exception)))
            self.assertFalse([o for o in self.opened if o.endswith(name)], name)

    def test_extra_key_refused_without_echo(self):
        ref = self.tmp / 'ref_com_canario.json'
        ref.write_text(json.dumps(self.identity(CANARY_SECRET='FAKE_SYNTHETIC_CANARY')), encoding='utf-8')
        with self.assertRaises(sm.ProtocolError) as cm:
            sm.dispatch(self.req(ref), self.store_root, MemoryStore)
        self.assertEqual(str(cm.exception), 'reference_unexpected_keys:1')
        self.assertNotIn('CANARY', str(cm.exception))

    def test_hardlinked_reference_refused(self):
        real = self.tmp / 'ref_real.json'
        real.write_text(json.dumps(self.identity()), encoding='utf-8')
        link = self.tmp / 'ref_link.json'
        os.link(real, link)
        with self.assertRaises(sm.ProtocolError) as cm:
            sm.dispatch(self.req(link), self.store_root, MemoryStore)
        self.assertEqual(str(cm.exception), 'source_path_not_allowed:hardlink')

    def test_normal_flow_and_reuse_return_only_protocol_keys(self):
        ref = self.tmp / 'sessions' / 'r2.json'
        first = sm.dispatch(self.req(ref), self.store_root, MemoryStore)
        second = sm.dispatch(self.req(ref), self.store_root, MemoryStore)
        self.assertEqual(first['reference'], second['reference'])
        self.assertTrue(set(second['reference']) <= sm.REFERENCE_KEYS)
        got = sm.dispatch({'operation': 'get', 'reference': str(ref)}, self.store_root, MemoryStore)
        self.assertEqual(got['context_id'], self.ctx)

    def test_reference_operand_is_guarded_too(self):
        conf = self.tmp / 'iald_psion_state_32B.json.bak_x'
        conf.write_text('{}', encoding='utf-8')
        sm.dispatch(self.req(self.tmp / 'ok.json'), self.store_root, MemoryStore)
        self.opened.clear()
        with self.assertRaises(sm.ProtocolError) as cm:
            sm.dispatch({'operation': 'get', 'reference': str(conf)}, self.store_root, MemoryStore)
        self.assertEqual(str(cm.exception), 'source_path_not_allowed:psion_name')
        self.assertFalse([o for o in self.opened if o.endswith('iald_psion_state_32B.json.bak_x')])

    def test_production_reference_format_accepted(self):
        # as 4 referências de produção (lidas em 13/10, só as chaves) têm exatamente estas 8 chaves e source{path,sha256,bytes}
        ref = self.tmp / 'formato_producao.json'
        ref.write_text(json.dumps(self.identity(source={'path': str(self.obj), 'sha256': self.sha, 'bytes': 31},
                                                authority='local_os_access_only_not_external_identity_authentication')),
                       encoding='utf-8')
        out = sm.dispatch(self.req(ref), self.store_root, MemoryStore)
        self.assertEqual(sorted(out['reference']), sorted(sm.REFERENCE_KEYS))


class JournalCaseTests(unittest.TestCase):
    def test_contexts_differing_only_in_case_have_distinct_journals(self):
        root = Path(tempfile.mkdtemp(prefix='r2_case_', dir=os.environ.get('TEMP')))
        st = MemoryStore(root / 'state')
        scope = {'house': 'IALD', 'principal': 'r2'}
        actor = {'id': 'r2', 'kind': 'agent'}
        st.ensure_context('CtxCase', objective='objetivo A', scope=scope, actor=actor)
        st.ensure_context('ctxcase', objective='objetivo B', scope=scope, actor=actor)
        st.transition('CtxCase', scope, 0, 'ev-a1', actor, {'flow': {'phase': 'a1', 'next_action': 'x'}})
        st.transition('ctxcase', scope, 0, 'ev-b1', actor, {'flow': {'phase': 'b1', 'next_action': 'y'}})
        files = sorted(os.listdir(root / 'state' / 'journal'))
        self.assertEqual(len(files), 2, files)
        for cid in ('CtxCase', 'ctxcase'):
            v = st.verify(cid, scope)
            self.assertTrue(v['ok'] and v['journal_ok'], (cid, v))
        RESULTS['t3_E_journal_case'] = {'journal_files': files, 'verify_ok': True}


def tearDownModule():
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / 'r2_testes_novos.json').write_text(json.dumps(RESULTS, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
