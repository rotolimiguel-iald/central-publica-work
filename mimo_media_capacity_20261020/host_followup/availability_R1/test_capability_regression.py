"""Actual whole chooser + captured POST; synthetic policy/control collaborators."""
import ast,copy,hashlib,importlib.util,json,math,sys,tempfile,time,unittest,uuid
from datetime import datetime,timezone
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock
HERE=Path(__file__).resolve().parent;LIVE=Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0]=[str(HERE),str(LIVE),str(HERE.parent)]
import iald_media_budget as budget
import new_private_media_host as host
from claude_memory_package import load_package
PACKAGE=load_package(LIVE/'.iald_runtime/haiku',canonical_manifest=LIVE/'iald_nucleo_fixo.json')
METADATA=json.loads((HERE.parent/'SCOPED_JOB_METADATA.json').read_text())['media'][0]['metadata']
ACTUAL=json.loads(json.loads(Path('C:/IALD/MEMORIA_IALD/state/activity_artifacts/532f6902924d86e0f05a798a334bee442cc0a3d416788d17c3f7a3fc2cefe973.json').read_text())['payload']['wire_utf8'])
ITEM=budget.adapt_resolved_metadata([dict(METADATA,encoded_bytes_upper=4*((METADATA['bytes']+2)//3)+128)])[0]

def plans(items,proposals):
    parts=[dict(type='iald_media',media_ref=i['id'],kind=i['kind']) for i in items]
    body=dict(model='mimo-v2.6-pro',messages=[dict(role='system',content=PACKAGE.prefix),dict(role='user',content=parts)])
    return budget.options(body,items,proposals,rates=dict(input=.435,cache_read=.0036,output=.87))

class Capability(unittest.TestCase):
    def chooser(self,counts):
        temp=tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        control=NS(load_contract=lambda root:{},contract_state=lambda c:dict(release='fixture',source_sha256='f'*64),
            questions=lambda **kw:{k:{'instructions':'fixture'} for k in ('scientific_mode','work_path','memory_action')},
            new_receipt=lambda *a,**kw:dict(state='new'),transition=lambda r,state,**kw:dict(state=state),
            resolve=lambda *a,**kw:dict(work_path='answer'))
        policy=NS(model_identities=lambda c,ids:dict.fromkeys(c,'mimo-v2.6-pro'),tool_managers=lambda c:c,
            automatic_candidates=lambda c:c,eligible_managers=lambda c,t:c,capability_catalog=lambda *a,**kw:{},
            executor_criteria=lambda *a:{},delivery_steps=lambda c:['answer'],AUTOMATIC_ORDER=('mimo',))
        memory=NS(current=lambda:None,http_call=lambda label,fn,*a,**kw:fn(*a,**kw),routing_result=Mock())
        wallet=NS(enabled=lambda:False,routing_begin=Mock(return_value='synthetic-event'),routing_end=Mock())
        guide=NS(strategy_question=lambda worker:{},routing_guide=lambda *a,**kw:{},VERSION='fixture',resolve_strategy=lambda *a:{})
        backend=NS(availability=lambda:dict(status='ready'),validate_prompt=lambda p:None,ENDPOINT='https://invalid.local/no-network',_key=lambda:'SYNTHETIC')
        ns=dict(ROOT=Path(temp.name),copy=copy,math=math,json=json,hashlib=hashlib,Path=Path,uuid=uuid,datetime=datetime,timezone=timezone,time=time,
            task_policy=policy,jev_control=control,app_memory=memory,wallet_runtime=wallet,execution_guide=guide,
            routing_metrics=NS(partition=lambda *a,**kw:counts,category=lambda *a:'audio_analysis'),
            media_budget_policy=budget,backend=lambda:backend,available=lambda:True,DESCRIPTIONS={'mimo':'MiMo'},
            bootstrap_intent=NS(classify=lambda p:None),observations=lambda *a,**kw:{},
            router_media_view=NS(routing_state=lambda *a:None,prepare_body=lambda b,*a:b,assert_public_body=lambda *a:None),
            _fit_routing_payload=lambda b:dict(transport_headers={}),
            memory_slice=lambda *a:(PACKAGE.prefix,dict(release='fixture',release_source_sha256='f'*64)),
            adaptive_routing=NS(select=lambda *a,**kw:('mimo',{})))
        nodes=[n for n in ast.parse((HERE/'iald_auto_router.py').read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name in ('choose','parse_answer')]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'entire staged chooser AST','exec'),ns)
        return ns,wallet
    def run_choice(self,choices,counts,extra_answer=False):
        ns,wallet=self.chooser(counts);captured=[]
        def capture(*a,**kw):
            captured.append(copy.deepcopy(kw['json']))
            data=copy.deepcopy(ACTUAL)
            data['answers']={k:v for k,v in data['answers'].items() if k in kw['json']['questions']}
            if 'media_policy' in data['answers']:
                ids=list(budget.routing_options(choices));first=ids[0]
                data['answers']['media_policy']=dict(type='choice',choice=first,confidence=.68,
                    probabilities={name:(.84 if name==first else .16/(len(ids)-1)) for name in ids})
            if extra_answer:data['answers']['media_policy']=ACTUAL['answers']['media_policy']
            return NS(status_code=200,json=lambda:data)
        post=Mock(side_effect=capture)
        return ns,wallet,captured,post
    def test_audio_only_single_plan_real_answer_no_extra_request_same_budget(self):
        choices=plans([ITEM],host.video_proposals([ITEM]))
        self.assertEqual(set(choices),{'audio_full'})
        duplicated=plans([ITEM],{'standard':{'fps':2.,'media_resolution':'default'},'detail':{'fps':2.,'media_resolution':'max'}})
        for key in ('context_total','input_tokens_bound','output_reserved_tokens','reservation_nanousd','media_tokens_estimate'):
            self.assertEqual(choices['audio_full'][key],duplicated['standard'][key])
        ns,wallet,captured,post=self.run_choice(choices,dict(image=0,audio=1,video=0))
        chosen,receipt=ns['choose']('audio synthetic',['mimo'],post=post,validation_probe=True,multimodal=True,media_integrated=True,media_budget_options=choices)
        self.assertEqual(chosen,'mimo');post.assert_called_once();wallet.routing_begin.assert_called_once();wallet.routing_end.assert_called_once()
        self.assertNotIn('media_policy',captured[0]['questions']);self.assertEqual(captured[0]['state']['canonical_memory'],PACKAGE.prefix)
        self.assertEqual(receipt['media_policy_id'],'audio_full');self.assertEqual(receipt['media_budget'],choices['audio_full'])
        self.assertEqual(receipt['media_policy_resolution'],'host_single_audio_no_quality_alternatives')
        self.assertEqual(wallet.routing_end.call_args.args[1],ACTUAL['usage'])
    def test_multiple_audio_options_068_still_refuses(self):
        choices=plans([ITEM],{'standard':{'fps':2.,'media_resolution':'default'},'detail':{'fps':2.,'media_resolution':'max'}})
        ns,w,captured,post=self.run_choice(choices,dict(image=0,audio=1,video=0))
        with self.assertRaisesRegex(budget.BudgetRefusal,'Uncertain media policy'):
            ns['choose']('audio',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=choices)
        self.assertIn('media_policy',captured[0]['questions']);post.assert_called_once()
    def test_video_full_history_multiple_068_still_refuses(self):
        video=dict(ITEM,id='a'*32,kind='video',duration_seconds=10.,width=320,height=240,has_audio=True)
        for items,counts in (([video],dict(image=0,audio=0,video=1)),([ITEM,video],dict(image=0,audio=1,video=1))):
            choices=plans(items,host.video_proposals(items));self.assertGreater(len(choices),1)
            ns,w,captured,post=self.run_choice(choices,counts)
            with self.assertRaisesRegex(budget.BudgetRefusal,'Uncertain media policy'):
                ns['choose']('video',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=choices)
            self.assertIn('media_policy',captured[0]['questions']);post.assert_called_once()
    def test_single_video_is_not_audio_and_extra_answer_refused(self):
        video=dict(ITEM,id='a'*32,kind='video',duration_seconds=10.,width=320,height=240,has_audio=True)
        choices=plans([video],{'only_video':{'fps':2.,'media_resolution':'default'}})
        ns,w,captured,post=self.run_choice(choices,dict(image=0,audio=0,video=1))
        with self.assertRaises(budget.BudgetRefusal):ns['choose']('video',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=choices)
        self.assertIn('media_policy',captured[0]['questions'])
        choices=plans([ITEM],host.video_proposals([ITEM]));ns,w,captured,post=self.run_choice(choices,dict(image=0,audio=1,video=0),True)
        with self.assertRaisesRegex(ValueError,'Invalid decision envelope'):ns['choose']('audio',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=choices)
    def test_full_history_two_audio_and_unverified_plan_fail_closed(self):
        items=[ITEM,dict(ITEM,id='b'*32)];choices=plans(items,host.video_proposals(items))
        ns,w,captured,post=self.run_choice(choices,dict(image=0,audio=2,video=0))
        chosen,r=ns['choose']('two audio',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=choices)
        self.assertEqual(r['media_policy_id'],'audio_full');self.assertNotIn('media_policy',captured[0]['questions'])
        invalid=copy.deepcopy(choices);invalid['audio_full']['status']='REFUSED'
        ns,w,captured,post=self.run_choice(invalid,dict(image=0,audio=2,video=0))
        with self.assertRaises(budget.BudgetRefusal):ns['choose']('audio',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=invalid)
        post.assert_not_called()

if __name__=='__main__':unittest.main(verbosity=2)
