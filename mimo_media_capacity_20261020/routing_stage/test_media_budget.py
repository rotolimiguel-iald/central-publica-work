import ast
import copy
import json
import math
import re
import threading
import base64
import io
import wave
import importlib.util
from pathlib import Path
import unittest
import iald_media_budget as budget
import iald_routing_metrics as metrics

RATES={'input':'.435','cache_read':'.0036','output':'.87'}


def item(kind='audio', seconds=60, size=12000):
    value=dict(id='a'*32,kind=kind,sha256='b'*64,decoded_bytes=size,
               encoded_bytes=4*((size+2)//3),duration_seconds=seconds)
    if kind=='video':value.update(width=1920,height=1080,has_audio=True)
    return value


def body(items, text='full scientific text'):
    return dict(model='mimo-v2.6-pro',max_completion_tokens=131072,
        messages=[dict(role='system',content=text),dict(role='user',content=[
            dict(type='iald_media',media_ref=row['id'],kind=row['kind']) for row in items])])


class BudgetTests(unittest.TestCase):
    def plan(self, items=None, payload=None, **kwargs):
        items=[item()] if items is None else items
        return budget.plan_request(body(items) if payload is None else payload,items,rates=RATES,**kwargs)

    def test_audio_formula_and_margin(self):
        plan=self.plan()
        self.assertEqual(plan['media_tokens_estimate'],375)
        self.assertEqual(plan['media_slack_tokens'],256)
        self.assertEqual(plan['output_reserved_tokens'],131072)

    def test_legacy_text_bound_unchanged(self):
        payload=dict(messages=[dict(role='user',content='texto íntegro')])
        self.assertEqual(budget.text_bound(payload),len(json.dumps(payload,ensure_ascii=False).encode('utf-8')))

    def test_legacy_image_bound_unchanged(self):
        payload=dict(messages=[dict(role='user',content=[dict(type='image_url',image_url=dict(url='data:image/png;base64,'+'A'*4000))])])
        self.assertEqual(budget.text_bound(payload),len(json.dumps(payload,ensure_ascii=False).encode('utf-8')))
        self.assertEqual(self.plan([],payload)['media_tokens_estimate'],0)

    def test_base64_not_text_tokens_for_audio_video(self):
        for kind,key in [('input_audio','data'),('video_url','url')]:
            a={'messages':[{'role':'user','content':[{'type':kind,kind:{key:'data:video/mp4;base64,'+'A'*1000}}]}]}
            b=copy.deepcopy(a);b['messages'][0]['content'][0][kind][key]+='A'*100000
            self.assertEqual(budget.text_bound(a),budget.text_bound(b))

    def test_all_history_occurrences_count(self):
        one=item();payload=body([one,one]);before=copy.deepcopy(payload)
        plan=self.plan([one,one],payload)
        self.assertEqual(plan['media_tokens_estimate'],750)
        self.assertEqual(payload,before)
        with self.assertRaises(budget.BudgetRefusal):self.plan([one],payload)

    def test_fifty_mb_encoded_boundary(self):
        self.plan([item(size=37500000)])
        with self.assertRaises(budget.BudgetRefusal):self.plan([item(size=37500001)])

    def test_encoding_metadata_forgery_refused(self):
        bad=item();bad['encoded_bytes']-=4
        with self.assertRaises(budget.BudgetRefusal):self.plan([bad])

    def test_no_arbitrary_duration_cap(self):
        self.plan([item(seconds=36000,size=1000)])

    def test_long_compressed_audio_context_refusal(self):
        with self.assertRaises(budget.BudgetRefusal):self.plan([item(seconds=1000000,size=1000)])

    def test_dynamic_output_floor_and_full_core(self):
        payload=body([item()],text='x'*950000)
        before=copy.deepcopy(payload);plan=self.plan(payload=payload)
        self.assertTrue(plan['output_reduced_technically'])
        self.assertGreaterEqual(plan['output_reserved_tokens'],16384)
        self.assertEqual(payload,before)
        with self.assertRaises(budget.BudgetRefusal):self.plan(payload=body([item()],text='x'*1040000))

    def test_video_known_reference_numbers(self):
        # Independently calculated from documented 32px spatial/2frame grid rules.
        estimate=budget.estimate_video(item('video'),dict(fps=2,media_resolution='default'))
        self.assertEqual(estimate['sampled_frames'],120)
        self.assertEqual(estimate['visual_tokens'],16862)
        self.assertEqual(budget.video_audio_tokens(60),378)
        self.assertEqual(self.plan([item('video')])['media_tokens_estimate'],17240)

    def test_300_is_tokens_not_frames(self):
        estimate=budget.estimate_video(item('video',seconds=300),dict(fps=2,media_resolution='default'))
        self.assertEqual(estimate['sampled_frames'],600)
        self.assertEqual(estimate['per_frame_token_budget_default'],300)

    def test_vendor_frame_cap_refuses_instead_of_silently_capping(self):
        with self.assertRaises(budget.BudgetRefusal):self.plan([item('video',seconds=3000)])
        with self.assertRaises(budget.BudgetRefusal):
            budget.estimate_video(item('video',seconds=3000),dict(fps=2,media_resolution='default'))
        with self.assertRaises(budget.BudgetRefusal):
            self.plan([item('video',seconds=3000)],visual_estimator=lambda *_:dict(visual_tokens=1,sampled_frames=2))
        plan=self.plan([item('video',seconds=3000)],policy=dict(fps=.5,media_resolution='default'))
        self.assertEqual(plan['items'][0]['sampled_frames'],1500)
        self.assertFalse(plan['items'][0]['vendor_frame_cap_applied'])
        boundary=self.plan([item('video',seconds=20480)],policy=dict(fps=.1,media_resolution='default'))
        self.assertEqual(boundary['items'][0]['sampled_frames'],2048)
        with self.assertRaises(budget.BudgetRefusal):
            self.plan([item('video',seconds=20481)],policy=dict(fps=.1,media_resolution='default'))

    def test_intent_motion_and_ocr(self):
        with self.assertRaises(budget.BudgetRefusal):self.plan([item('video')],intent_limits={'require_max_resolution':True})
        plan=self.plan([item('video')],policy=dict(fps=5,media_resolution='max'),intent_limits={'require_max_resolution':True,'min_fps':5})
        self.assertEqual(plan['policy']['media_resolution'],'max')
        with self.assertRaises(budget.BudgetRefusal):self.plan([item('video',seconds=3000)],intent_limits={'min_fps':2})

    def test_policy_boundaries(self):
        for fps in [.1,10]:budget.validate_policy(dict(fps=fps,media_resolution='default'))
        for fps in [True,float('nan'),float('inf'),0,11]:
            with self.subTest(fps=fps),self.assertRaises(budget.BudgetRefusal):budget.validate_policy(dict(fps=fps,media_resolution='default'))
        with self.assertRaises(budget.BudgetRefusal):budget.validate_policy(dict(fps=2,media_resolution='low'))

    def test_unknown_duration_dimensions_audio_stream(self):
        for field,value in [('duration_seconds',None),('duration_seconds',True),('width',0),('has_audio',None)]:
            bad=item('video');bad[field]=value
            with self.subTest(field=field),self.assertRaises(budget.BudgetRefusal):self.plan([bad])

    def test_no_automatic_muting(self):
        row=item('video');audible=self.plan([row]);row['has_audio']=False;muted=self.plan([row])
        self.assertEqual(audible['media_tokens_estimate']-muted['media_tokens_estimate'],378)

    def test_no_cache_hit_assumed(self):
        plan=self.plan();lower=dict(RATES,cache_read='0')
        self.assertEqual(plan['reservation_nanousd'],budget.plan_request(body([item()]),[item()],rates=lower)['reservation_nanousd'])

    def test_actual_wire_limit(self):
        budget.validate_final_wire_bytes(64000000)
        with self.assertRaises(budget.BudgetRefusal):budget.validate_final_wire_bytes(64000001)

    def test_final_video_policy_matches_explicit_plan(self):
        payload={'messages':[{'role':'user','content':[{'type':'video_url','video_url':{'url':'data:video/mp4;base64,AAAA'},'fps':5,'media_resolution':'max'}]}]}
        policy=dict(fps=5,media_resolution='max')
        self.assertTrue(budget.validate_video_wire_policy(payload,policy))
        payload['messages'][0]['content'][0]['fps']=2
        with self.assertRaises(budget.BudgetRefusal):budget.validate_video_wire_policy(payload,policy)

    def test_aggregate_byte_budget(self):
        with self.assertRaises(budget.BudgetRefusal):self.plan([item(size=30000000),item(size=30000000)])

    def test_unknown_data_uri_location(self):
        with self.assertRaises(budget.BudgetRefusal):budget.text_bound({'hidden':'data:video/mp4;base64,AAAA'})

    def test_cost_proportional(self):
        small=self.plan();large=self.plan([item(seconds=6000)])
        self.assertGreater(large['reservation_nanousd'],small['reservation_nanousd'])

    def test_existing_spending_contract(self):
        payload=body([item()]);plan=self.plan(payload=payload)
        payload['max_completion_tokens']=plan['output_reserved_tokens']
        self.assertEqual(budget.spending_bound(payload,plan),plan['input_tokens_bound'])
        payload['messages'][0]['content']+='CHANGED'
        with self.assertRaises(budget.BudgetRefusal):budget.spending_bound(payload,plan)

    def test_one_existing_guard_reservation_no_retry(self):
        payload=body([item()]);plan=self.plan(payload=payload)
        payload['max_completion_tokens']=plan['output_reserved_tokens']
        calls=[]
        class Existing:
            def before(self,*args,**kwargs):
                calls.append((args,kwargs))
                self.remaining=-1  # An already-admitted task may finish below zero.
                return 'existing-reservation-id'
        guard=Existing()
        self.assertEqual(budget.reserve_existing(guard,payload,plan),'existing-reservation-id')
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][0][2],plan['input_tokens_bound'])
        class Refusing:
            def before(self,*args,**kwargs):calls.append(1);raise RuntimeError('global provider limit')
        with self.assertRaises(RuntimeError):budget.reserve_existing(Refusing(),payload,plan)
        self.assertEqual(len(calls),2)

    def test_exact_spending_diff_preserves_existing_guard(self):
        original=Path('C:/IALD/projetos_pyhton/IALD/iald_app_spend.py').read_text(encoding='utf-8').splitlines(True)
        patch=Path(__file__).with_name('SPENDING_INTEGRATION.diff').read_text(encoding='utf-8').splitlines(True)
        output=[];cursor=0;index=2
        while index<len(patch):
            match=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',patch[index])
            self.assertIsNotNone(match)
            start=int(match[1])-1;output.extend(original[cursor:start]);cursor=start;index+=1
            while index<len(patch) and not patch[index].startswith('@@'):
                line=patch[index];kind=line[0];value=line[1:]
                if kind in (' ','-'):
                    self.assertEqual(original[cursor],value);cursor+=1
                if kind in (' ','+'):output.append(value)
                index+=1
        output.extend(original[cursor:])
        tree=ast.parse(''.join(output));fn=next(node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='before')
        class GuardError(ValueError):pass
        def positive(value):
            if value<=0:raise GuardError('invalid positive')
            return value
        ns=dict(BudgetError=GuardError,json=json,_positive=positive,
                MODELS={'mimo':dict(model='mimo-v2.6-pro',output=131072,rates=(.435,.0036,.87))})
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<staged-spending-integration>','exec'),ns)
        calls=[]
        class ExistingGuard:
            def reserve(self,*args,**kwargs):calls.append((args,kwargs));return 'original-ledger-id'
        class Cursor:pass
        cursor=Cursor();cursor._lock=threading.RLock();cursor.closed=False;cursor.pending=None
        cursor.account_key_hash='a'*64;cursor.daily=1.;cursor.group=5.;cursor.total=15.;cursor.guard=ExistingGuard()
        payload=body([item()],text='x'*950000);plan=self.plan(payload=payload)
        payload['max_completion_tokens']=plan['output_reserved_tokens']
        ns['before'](cursor,'mimo',payload,plan['input_tokens_bound'],media_plan=plan)
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][1]['group'],'mimo_public')
        self.assertEqual(calls[0][1]['group_limit'],5.)
        expected=(plan['input_tokens_bound']*.435+plan['output_reserved_tokens']*.87)/1000000
        self.assertGreaterEqual(calls[0][0][2],expected)
        self.assertAlmostEqual(calls[0][0][2],plan['reservation_usd'],places=8)
        self.assertEqual(cursor.pending['key'],'original-ledger-id')

    def test_group_notice_does_not_admit_or_interrupt(self):
        plan=self.plan()
        self.assertEqual(budget.group_notice(plan,group_remaining_usd=0)[0]['status'],'ESTIMATED_RESERVATION_EXCEEDS_REMAINING')
        self.assertEqual(budget.group_notice(plan)[1]['status'],'UNKNOWN_REMAINING')

    def test_named_jev_options_no_refs(self):
        plans=budget.options(body([item('video')]),[item('video')],
            {'standard':dict(fps=2,media_resolution='default'),'detail':dict(fps=5,media_resolution='max')},rates=RATES)
        view=budget.routing_options(plans);raw=json.dumps(view)
        self.assertNotIn('sha256',raw);self.assertNotIn('media_ref',raw);self.assertNotIn('data:',raw)
        answer=dict(type='choice',choice='detail',probabilities={'standard':.1,'detail':.9},confidence=.9)
        self.assertEqual(budget.resolve_policy(answer,plans),'detail')
        answer['confidence']=.3
        with self.assertRaises(budget.BudgetRefusal):budget.resolve_policy(answer,plans)

    def test_stamp_typed_refs_and_full_cost_profile(self):
        messages=body([item('video')])['messages']+[dict(role='user',content='continue')]
        record={};plan=self.plan([item('video')]);metrics.stamp(record,messages,media_plan=plan)
        self.assertEqual(record['task'],'video_analysis')
        self.assertIn('history_media',record['media_cost_profile'])

    def test_syntax_all_staged_modules(self):
        for path in Path(__file__).parent.glob('*.py'):ast.parse(path.read_text(encoding='utf-8'))

    def test_router_legacy_image_and_audio_budget_gate(self):
        import iald_task_policy as policy
        tree=ast.parse(Path(__file__).with_name('iald_auto_router.py').read_text(encoding='utf-8'))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='choose')
        stop=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='mod' for t in n.targets))
        fn.body=fn.body[:stop]+[ast.Return(value=ast.Name(id='candidates',ctx=ast.Load()))]
        ast.fix_missing_locations(fn)
        ns=dict(ROOT=Path('.'),task_policy=policy,routing_metrics=metrics,copy=copy,json=json,
                DESCRIPTIONS=dict.fromkeys(['kimi','mimo']),media_budget_policy=budget)
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<real-router-prefix>','exec'),ns)
        self.assertEqual(ns['choose']('image',['kimi','mimo'],multimodal=True),['mimo'])
        summary=dict(kinds=['audio'],counts=dict(image=0,audio=1,video=0))
        with self.assertRaises(budget.BudgetRefusal):ns['choose']('audio',['kimi','mimo'],media=summary)
        self.assertEqual(ns['choose']('audio',['kimi','mimo'],media=summary,media_budget_options={'default':self.plan()}),['mimo'])

    def test_route_instruction_exposes_selected_cost_policy(self):
        import types
        tree=ast.parse(Path(__file__).with_name('iald_auto_router.py').read_text(encoding='utf-8'))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='route_instruction')
        ns=dict(jev_control=types.SimpleNamespace(manager_instruction=lambda c:'control'),
                execution_guide=types.SimpleNamespace(manager_instruction=lambda c:'strategy'),
                task_policy=types.SimpleNamespace(delivery_steps=lambda c:['answer']))
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<route-instruction>','exec'),ns)
        text=ns['route_instruction'](dict(status='selected',control={},collaboration={},media_budget=self.plan()))
        self.assertIn('fps=2.0',text);self.assertIn('custo estimado',text);self.assertIn('131072',text)

    def test_unknown_identity_in_resolved_metadata_refuses(self):
        row=item();payload=body([row]);payload['messages'][1]['content'][0]['media_ref']='c'*32
        with self.assertRaises(budget.BudgetRefusal):self.plan([row],payload)

    def test_private_media_never_sent_to_text_providers(self):
        for provider in ('kimi','openai','deepseek','nativa','jev','worker'):
            with self.subTest(provider=provider),self.assertRaises(budget.BudgetRefusal):
                budget.assert_private_media_destination(body([item()]),provider)
        self.assertTrue(budget.assert_private_media_destination(body([item()]),'mimo'))

    def test_inline_old_client_options_and_mixed_refs(self):
        import SERVER_GLUE_EXAMPLE as glue
        raw=b'fake audio for trusted decoder fixture'
        part={'type':'input_audio','input_audio':{'data':'data:audio/wav;base64,'+base64.b64encode(raw).decode()}}
        payload=body([]);payload['tools']=[{'type':'function','function':{'name':'source_read'}}]
        payload['messages'][1]['content']=[part]
        def local_probe(raw,mime):
            self.assertEqual(mime,'audio/wav')
            return dict(kind='audio',duration_seconds=60)
        items,plans=glue.build_options(full_body=payload,resolved_facts=[],validate_upload=local_probe,rates=RATES)
        self.assertEqual(set(plans),{'standard','detail'})
        self.assertEqual(items[0]['kind'],'audio')
        self.assertEqual(plans['standard']['media_tokens_estimate'],375)
        row=item();payload['messages'][1]['content'].append(dict(type='iald_media',media_ref=row['id'],kind='audio'))
        facts=[dict(type='iald_media',media_ref=row['id'],kind='audio',bytes=row['decoded_bytes'],duration_seconds=60,sha256=row['sha256'],encoded_bytes_upper=row['encoded_bytes']+128)]
        items,plans=glue.build_options(full_body=payload,resolved_facts=facts,validate_upload=local_probe,rates=RATES)
        self.assertEqual(len(items),2);self.assertEqual(plans['standard']['media_tokens_estimate'],750)

    def test_inline_bridge_with_real_cicero_wav_validator(self):
        path=Path(__file__).parents[1]/'backend_stage/iald_mimo_multimodal.py'
        spec=importlib.util.spec_from_file_location('isolated_cicero_validator',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        buffer=io.BytesIO()
        with wave.open(buffer,'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000);wav.writeframes(b'\0'*16000)
        uri='data:audio/wav;base64,'+base64.b64encode(buffer.getvalue()).decode()
        messages=[dict(role='user',content=[dict(type='input_audio',input_audio=dict(data=uri))])]
        rows=budget.legacy_inline_metadata(messages,validate_upload=module.validate_upload)
        self.assertEqual(rows[0]['duration_seconds'],1)
        self.assertEqual(rows[0]['encoded_bytes'],4*((len(buffer.getvalue())+2)//3))


if __name__=='__main__':unittest.main(verbosity=2)
