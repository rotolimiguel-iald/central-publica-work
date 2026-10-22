"""Real Binding/SQLite, real choose + fit functions, mocked outbound transport."""
import ast
import base64
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock
import uuid

HERE = Path(__file__).resolve().parent
WORK = HERE.parent.parent
APP = Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0] = [str(HERE), str(HERE.parent / 'lib'), str(APP), str(WORK / 'final_stage')]
import iald_app_memory as memory
from iald_memory import MemoryStore
import iald_router_media_view as view


def proposal():
    return (HERE.parent / 'ROUTER_MEDIA_INTEGRATION_PROPOSAL.py').read_text(encoding='utf-8')


class Captured(RuntimeError):
    pass


class MediaView(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = MemoryStore(self.root / 'state', snapshot_archive_dir=self.root / 'archive')
        self.scope = dict(house='IALD_APP', principal='synthetic_public_fixture')
        self.parts = []
        self.payloads = []
        for kind, typ, field, mime in [('image', 'image_url', 'url', 'image/png'),
                                     ('audio', 'input_audio', 'data', 'audio/wav'),
                                     ('video', 'video_url', 'url', 'video/mp4')]:
            payload = base64.b64encode(('SYNTHETIC_' + kind.upper() + '_MEDIA_BYTES_937').encode()).decode()
            self.payloads.append(payload)
            self.parts.append(dict(type=typ, **{typ: {field: 'data:' + mime + ';base64,' + payload}}))
        self.pdf_block = '[ARQUIVO: synthetic.pdf]\nSYNTHETIC_PDF_PRIVATE_TEXT_729\n[FIM]'
        self.messages = [dict(role='user', content=[dict(type='text', text='KEEP_TEXT_AND_CRITERION\n' + self.pdf_block), *self.parts])]
        self.objective = json.dumps(self.messages, ensure_ascii=False)
        self.store.ensure_context('synthetic_media', objective=self.objective, scope=self.scope,
                                  actor=dict(id='fixture', kind='agent'), constraints={'keep': 'MANDATORY_CONSTRAINT'})
        self.binding = memory.Binding(self.store, 'synthetic_media', self.scope, 'fixture_request')
        snapshot = self.binding.snapshot()
        self.store.transition(self.binding.context_id, self.scope, expected_revision=snapshot['revision'],
                              event_id='fixture-history', actor=dict(id='fixture', kind='agent'), changes={
            'records': [dict(id='legacy_history', kind='decision', statute='DECLARADO',
                             text=json.dumps(dict(history=self.messages, nested=json.dumps(json.dumps(self.messages)),
                                                  raw_audio={'type': 'input_audio', 'data': self.payloads[1]},
                                                  decision='KEEP_DECISION'), ensure_ascii=False),
                             sources=[dict(kind='document', ref='fixture:history')])],
            'flow': dict(phase='KEEP_PHASE', next_action='KEEP_NEXT_ACTION', handles=[])})
        self.before = self.binding.snapshot()

    def raw_common(self):
        with memory.bound(self.binding):
            return memory.routing_state()

    def derived(self):
        with memory.bound(self.binding):
            return view.routing_state(memory)

    def assert_clean(self, value):
        wire = json.dumps(value)
        self.assertNotIn('data:image/', wire)
        self.assertNotIn('data:audio/', wire)
        self.assertNotIn('data:video/', wire)
        self.assertNotIn('SYNTHETIC_PDF_PRIVATE_TEXT_729', wire)
        self.assertNotIn('[ARQUIVO:', wire)
        for payload in self.payloads:
            self.assertNotIn(payload, wire)

    def test_real_binding_provenance_and_recovery(self):
        raw = self.raw_common()
        derived = self.derived()
        self.assert_clean(derived)
        for text in ('KEEP_TEXT_AND_CRITERION', 'MANDATORY_CONSTRAINT', 'KEEP_DECISION', 'KEEP_PHASE', 'KEEP_NEXT_ACTION'):
            self.assertIn(text, derived['projection'])
        self.assertEqual(raw['projection_receipt'], derived['projection_receipt'])
        self.assertEqual(view.sha(raw['projection']), derived['router_media_view']['original_projection_sha256'])
        self.assertEqual(view.sha(derived['projection']), derived['coverage']['projection_sha256'])
        self.assertEqual(len(derived['projection']), derived['coverage']['actual_chars'])
        self.assertEqual(self.before, self.binding.snapshot())
        self.assertEqual(self.objective, self.binding.snapshot()['objective'])

    def test_body_prompt_nested_json_and_same_scope_custody(self):
        body = dict(state=dict(common_memory=self.derived(), request='literal ' + self.parts[0]['image_url']['url'],
                               legacy=json.dumps(json.dumps(self.messages)), scientific='ω(I)=1; KEEP_SCIENCE'), questions={})
        result = view.prepare_body(body, self.binding)
        self.assert_clean(result)
        self.assertEqual(result['state']['scientific'], body['state']['scientific'])
        self.assertIn('data:image/', json.dumps(body))
        self.assertEqual(self.before, self.binding.snapshot())

    def test_system_only_user_parts_exact(self):
        common = self.raw_common()
        messages = [dict(role='system', content='KEEP_SCIENCE\n<IALD_COMMON_MEMORY_V1>\n' + common['projection'] + '\n</IALD_COMMON_MEMORY_V1>'),
                    dict(role='developer', content=view.ACOM_START + json.dumps(json.dumps(self.messages)) + view.ACOM_END), *self.messages]
        result = view.project_system_messages(messages, common, binding=self.binding)
        self.assertEqual(result[2], messages[2])
        self.assertEqual(json.dumps(result[2]), json.dumps(messages[2]))
        self.assert_clean(result[:2])
        self.assertTrue(result[0]['content'].startswith('KEEP_SCIENCE\n'))
        self.assertEqual(result[-1]['role'], 'user')
        self.assertEqual(result, view.project_system_messages(result, common, binding=self.binding))
        self.assertEqual(self.before, self.binding.snapshot())

    def test_real_executor_projection_prefix_idempotence_user_and_tool_last(self):
        scientific_prefix = 'KEEP_EXACT_SCIENCE\n{"a": 1, "b": 2}\nω(I)=1\n'
        for last in (self.messages[0], dict(role='tool', tool_call_id='fixture', content='tool result')):
            messages = [dict(role='system', content=scientific_prefix), *self.messages, last]
            with memory.bound(self.binding):
                projected = memory.project_messages(messages)
                once = view.project_system_messages(projected)
                twice = view.project_system_messages(once)
                projected_again = memory.project_messages(once)
                next_round = view.project_system_messages(projected_again)
            self.assertEqual(once, twice)
            self.assertEqual(once, next_round)
            self.assertEqual(once[-1], last)
            self.assertTrue(once[0]['content'].startswith(scientific_prefix))
            self.assertEqual(once[0]['content'].count(view.PROV_START), 1)
            self.assert_clean(once[0])
            self.assertEqual(once[1], messages[1])
        inserted = view.project_system_messages(self.messages, binding=self.binding)
        self.assertEqual(inserted[0]['role'], 'system')
        self.assertEqual(inserted[-1], self.messages[-1])

    def test_unbound_legacy_text_only_compatibility(self):
        body = dict(state=dict(request='text only', canonical_memory='KEEP_SCIENCE'), questions={})
        self.assertEqual(view.prepare_body(body, None), body)
        self.assertTrue(view.assert_public_body(body, None))
        for bad in (dict(state=dict(request=self.parts[0]['image_url']['url'])),
                    dict(state=dict(common_memory=self.raw_common()))):
            with self.assertRaises(view.MediaViewError):
                view.prepare_body(bad, None)

    def short_binding(self, token):
        literal = 'data:image/png;base64,' + token
        objective = json.dumps(dict(literal=literal, ordinary=token, protocol_key_Lean_IALD='Lean IALD',
                                    raw_audio=dict(type='input_audio', data=token)))
        context = 'short_' + token
        self.store.ensure_context(context, objective=objective, scope=self.scope,
                                  actor=dict(id='fixture', kind='agent'), constraints={'keep': 'Lean IALD unchanged'})
        binding = memory.Binding(self.store, context, self.scope, 'short_fixture')
        return binding, literal

    def test_short_tokens_preserve_science_protocol_and_untyped_text(self):
        for token in ('para', 'Lean', 'IALD', 'role', '1234', 'true'):
            binding, literal = self.short_binding(token)
            before = binding.snapshot()
            science = 'Lean: immutable scientific kernel TGL. IALD TGL ' + token
            with memory.bound(binding):
                raw = memory.routing_state()
                common = view.routing_state(memory)
                body = dict(state=dict(common_memory=common, canonical_memory=science, request='Inspect ' + literal,
                                       ordinary=token, embedded_word='prefix' + token + 'suffix',
                                       raw_audio=dict(type='input_audio', data=token)),
                            questions={'protocol_key_Lean_IALD': token})
                clean = view.prepare_body(body, binding)
                self.assertEqual(clean['state']['canonical_memory'], science)
                self.assertEqual(clean['state']['ordinary'], token)
                self.assertEqual(clean['state']['embedded_word'], 'prefix' + token + 'suffix')
                self.assertEqual(clean['questions'], body['questions'])
                self.assertNotEqual(clean['state']['raw_audio']['data'], token)
                self.assertNotIn(literal, json.dumps(clean))
                self.assertTrue(view.assert_public_body(clean, binding))
                self.assertEqual(common['projection_receipt'], raw['projection_receipt'])
                self.assertEqual(common['router_media_view']['original_projection_sha256'], view.sha(raw['projection']))
                user = dict(role='user', content=[dict(type='text', text='Inspect ' + literal)])
                projected = memory.project_messages([dict(role='system', content=science), user])
                system = view.project_system_messages(projected)
                prefix = system[0]['content'].split(memory._START)[0]
                self.assertEqual(prefix, science)
                self.assertNotIn(literal, system[0]['content'])
                self.assertEqual(system[-1], user)
                self.assertEqual(system, view.project_system_messages(system))
            self.assertEqual(before, binding.snapshot())

    def test_protected_science_with_explicit_uri_refuses_instead_of_mutating(self):
        binding, literal = self.short_binding('Lean')
        with memory.bound(binding):
            common = view.routing_state(memory)
            with self.assertRaises(view.MediaViewError):
                view.prepare_body(dict(state=dict(common_memory=common, canonical_memory='Lean ' + literal)), binding)
            projected = memory.project_messages([dict(role='system', content='Lean ' + literal), *self.messages])
            with self.assertRaises(view.MediaViewError):
                view.project_system_messages(projected)

    def test_unknown_uri_extending_known_token_is_not_substring_replaced(self):
        binding, literal = self.short_binding('Lean')
        with self.assertRaises(view.MediaViewError):
            view.prepare_body(dict(state=dict(request=literal + 'AAAA')), binding)

    def test_actual_choose_short_lean_keeps_canonical_kernel(self):
        self.binding, literal = self.short_binding('Lean')
        self.before = self.binding.snapshot()
        self.parts[0] = dict(type='image_url', image_url=dict(url=literal))
        self.science = 'Lean: immutable scientific kernel TGL. IALD TGL unchanged.'
        self.capture_choose()

    def test_actual_choose_para_keeps_verified_canonical8000(self):
        tree = ast.parse((WORK / 'final_stage/iald_auto_router.py').read_bytes())
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'memory_slice')
        namespace = dict(ROOT=APP, json=json, Path=Path, hashlib=hashlib)
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual_memory_slice', 'exec'), namespace)
        self.science, source = namespace['memory_slice'](APP)
        self.assertEqual(len(self.science), 8000)
        self.assertIn('para', self.science)
        self.binding, literal = self.short_binding('para')
        self.before = self.binding.snapshot()
        self.parts[0] = dict(type='image_url', image_url=dict(url=literal))
        self.capture_choose()

    def test_wrong_revision_hash_scope_and_unbound_media_refuse(self):
        common = self.raw_common()
        for key, value in [('revision', 999), ('scope', dict(house='IALD_APP', principal='other'))]:
            wrong = copy.deepcopy(common)
            wrong['projection_receipt'][key] = value
            with self.assertRaises(view.MediaViewError):
                view._common(wrong, view._View(self.binding))
        wrong = copy.deepcopy(common)
        wrong['coverage']['projection_sha256'] = '0' * 64
        with self.assertRaises(view.MediaViewError):
            view._common(wrong, view._View(self.binding))
        with self.assertRaises(view.MediaViewError):
            view.prepare_body(dict(state=dict(request='data:image/png;base64,VU5CT1VORA==')), self.binding)
        old = self.derived()
        snap = self.binding.snapshot()
        self.store.transition(self.binding.context_id, self.scope, expected_revision=snap['revision'],
                              event_id='new-revision', actor=dict(id='fixture', kind='agent'), changes={'flow': {'phase': 'new'}})
        with self.assertRaises(view.MediaViewError):
            view.prepare_body(dict(state=dict(common_memory=old)), self.binding)

    def test_final_egress_guard_and_rehashed_tamper_refuse(self):
        raw = dict(state=dict(common_memory=self.derived(), request=self.parts[0]['image_url']['url']))
        with self.assertRaises(view.MediaViewError):
            view.assert_public_body(raw, self.binding)
        clean = view.prepare_body(raw, self.binding)
        tampered = copy.deepcopy(clean)
        common = tampered['state']['common_memory']
        common['projection'] = common['projection'].replace('KEEP_DECISION', 'CHANGED_DECISION')
        common['coverage']['projection_sha256'] = view.sha(common['projection'])
        common['coverage']['actual_chars'] = len(common['projection'])
        with self.assertRaises(view.MediaViewError):
            view.assert_public_body(tampered, self.binding)
        self.assertTrue(view.assert_public_body(clean, self.binding))

    def test_incomplete_file_block_and_escaped_unknown_media_refuse(self):
        for literal in ('[ARQUIVO: incomplete.pdf] content without terminator',
                        'quoted fragment data:image\\/png;base64,VU5CT1VORA=='):
            with self.assertRaises(view.MediaViewError):
                view.prepare_body(dict(state=dict(request=literal)), self.binding)

    def capture_choose(self, force_reprojection=False):
        if force_reprojection:
            snap = self.binding.snapshot()
            self.store.transition(self.binding.context_id, self.scope, expected_revision=snap['revision'],
                                  event_id='optional-candidate', actor=dict(id='fixture', kind='agent'), changes={
                'records': [dict(id='optional_long', kind='candidate', statute='DECLARADO', text='optional retrieval ' * 250,
                                 sources=[dict(kind='document', ref='fixture:optional')])]})
            self.before = self.binding.snapshot()
        control = NS(ControlError=ValueError, MAX_STATE_BYTES=1_000_000, MAX_REQUEST_BYTES=2_000_000,
                     load_contract=lambda root: {}, contract_state=lambda c: dict(release='fixture', source_sha256='f' * 64),
                     questions=lambda **kw: {'work_path': {'type': 'choice', 'instructions': 'keep'}},
                     check_payload=lambda body, **kw: dict(transport_headers={}),
                     new_receipt=lambda *args, **kw: dict(state='new'),
                     transition=lambda receipt, state, **kw: dict(state=state))
        policy = NS(model_identities=lambda c, ids: dict.fromkeys(c, 'fixture-model'),
                    automatic_candidates=lambda c: c, eligible_managers=lambda c, task: c,
                    capability_catalog=lambda *a, **kw: {}, executor_criteria=lambda *a: {}, tool_managers=lambda c: c)
        metrics = NS(partition=lambda *a, **kw: dict(image=1, audio=1, video=1), category=lambda *a: 'video_analysis')
        wallet = NS(enabled=lambda: False, routing_begin=lambda *a: None, routing_end=lambda *a: None)
        guide = NS(strategy_question=lambda worker: {}, routing_guide=lambda *a, **kw: {}, VERSION='fixture')
        backend = NS(availability=lambda: dict(status='ready'), validate_prompt=lambda p: None,
                     ENDPOINT='https://invalid.example/fixture', _key=lambda: 'SYNTHETIC_NOT_CREDENTIAL')
        ns = dict(ROOT=self.root, app_memory=memory, router_media_view=view, task_policy=policy, routing_metrics=metrics,
                  jev_control=control, wallet_runtime=wallet, execution_guide=guide,
                  bootstrap_intent=NS(classify=lambda p: None), DESCRIPTIONS=dict(mimo='fixture'),
                  backend=lambda: backend, available=lambda: True,
                  memory_slice=lambda *a: (getattr(self, 'science', 'KEEP_SCIENCE'), dict(release='fixture', release_source_sha256='f' * 64, packet_sha256='e' * 64)),
                  observations=lambda *a, **kw: {}, json=json, hashlib=hashlib, Path=Path, uuid=uuid,
                  datetime=datetime, timezone=timezone, time=time)
        names = {'choose', '_fit_routing_payload', '_auditable_projection', 'RoutingContextOverflow'}
        nodes = [n for n in ast.parse(proposal()).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'proposed_router_choose.py', 'exec'), ns)
        if force_reprojection:
            control.MAX_STATE_BYTES = 3500
        source_calls = []
        real_view = view.routing_state
        def checked_view(*args, **kwargs):
            value = real_view(*args, **kwargs)
            self.assert_clean(value)
            source_calls.append(kwargs.get('max_chars'))
            return value
        captured = []
        def capture(*args, **kw):
            captured.append(copy.deepcopy(kw['json']))
            raise Captured('synthetic post stops after actual outbound capture')
        post = Mock(side_effect=capture)
        # HTTP operation wrapper has independent lifecycle duties; this test
        # executes real choose/fit but replaces only that wrapper and transport.
        from unittest.mock import patch
        with memory.bound(self.binding), patch.object(view, 'routing_state', side_effect=checked_view), patch.object(memory, 'http_call', side_effect=lambda label, fn, *a, **kw: fn(*a, **kw)):
            with self.assertRaises(Captured):
                ns['choose']('literal ' + self.parts[0]['image_url']['url'], ['mimo'], root=self.root,
                             post=post, validation_probe=True, multimodal=True, media_integrated=True)
        post.assert_called_once()
        self.assertEqual(len(captured), 1)
        self.assert_clean(captured[0])
        self.assertEqual(captured[0]['state']['canonical_memory'], getattr(self, 'science', 'KEEP_SCIENCE'))
        self.assertEqual(captured[0]['state']['modality_counts'], dict(image=1, audio=1, video=1))
        ns['_auditable_projection'](captured[0]['state']['common_memory'])
        self.assertEqual(captured[0]['state']['holographic_projection']['estatuto'], 'DERIVED')
        self.assertEqual(captured[0]['state']['holographic_projection']['custody_pointer']['scope'], self.scope)
        self.assertEqual(self.before, self.binding.snapshot())
        if force_reprojection:
            self.assertTrue(any(budget is not None for budget in source_calls))
            budgets = [budget for budget in source_calls if budget is not None]
            self.assertEqual(budgets, sorted(budgets, reverse=True))
            self.assertLess(len(source_calls), 10)
        self.assertTrue(view.assert_public_body(captured[0], self.binding))

    def test_actual_choose_outgoing_with_real_bound_acom(self):
        self.capture_choose()

    def test_actual_choose_forces_reprojection_and_terminates(self):
        self.capture_choose(force_reprojection=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
