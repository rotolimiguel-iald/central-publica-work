import ast
import copy
import json
import math
from pathlib import Path
import sqlite3
import statistics
import sys
import tempfile
import types
import unittest
import uuid
sys.path.insert(0,str(Path(__file__).parent))
sys.modules['iald_execution_guide']=types.SimpleNamespace(public_catalog=lambda:{})
import iald_task_policy as policy
import iald_adaptive_routing as routing
import iald_routing_metrics as metrics

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.ids=policy.model_identities(['kimi','mimo'])
        self.obs={'providers':{k:dict(model_id=v,task='code',paired_samples=3,median_cost_usd=1.,median_seconds=2.) for k,v in self.ids.items()}}
    def select(self,obs=None,pool=None):
        return routing.select(pool or ['kimi','mimo'],self.ids,'code',self.obs if obs is None else obs,policy.AUTOMATIC_ORDER)[0]
    def test_unmeasured_nativa_does_not_block(self):
        self.obs['providers']['mimo'].update(median_cost_usd=.5,median_seconds=1.)
        result,receipt=routing.select(['kimi','mimo','nativa'],dict(self.ids,nativa=None),'code',self.obs,policy.AUTOMATIC_ORDER)
        self.assertEqual(result,'mimo');self.assertIn('nativa',receipt['unmeasured_or_unqualified'])
    def test_unmeasured_nonbaseline_ignored(self):
        self.obs['providers']['mimo'].update(median_cost_usd=.5,median_seconds=1.)
        result,_=routing.select(['kimi','mimo','openai'],dict(self.ids,openai='exact-openai'),'code',self.obs,policy.AUTOMATIC_ORDER)
        self.assertEqual(result,'mimo')
    def test_unmeasured_baseline_preserved(self):
        self.obs['providers'].pop('kimi')
        self.assertEqual(self.select(),'kimi')
    def test_ledger_stamp(self):
        import iald_routing_metrics as metrics
        for content,task in [('implemente codigo','code'),('pesquise fontes','research'),([{'type':'text','text':'explique'},{'type':'image_url','image_url':{'url':'https://invalid.example/image'}}],'image_analysis')]:
            with self.subTest(task=task):
                record={};messages=[{'role':'user','content':'planilha antiga'},{'role':'assistant','content':'site'},{'role':'user','content':content}]
                before=copy.deepcopy(messages);metrics.stamp(record,messages)
                self.assertEqual(record['task'],task);self.assertEqual(messages,before)
                self.assertNotIn('content',record)
        for messages in [[],[{'role':'user','content':None}],[{'role':'user','content':[{'type':'audio'}]}]]:
            record={};metrics.stamp(record,messages);self.assertIsNone(record['task'])
    def test_multimodal_filter_before_jev_and_api(self):
        source=Path(__file__).with_name('iald_auto_router.py').read_text(encoding='utf-8')
        tree=ast.parse(source)
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='choose')
        # Execute the real pre-JEV admission prefix without loading production modules.
        fn.body=fn.body[:next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='mod' for t in n.targets))]+[ast.Return(value=ast.Name(id='candidates',ctx=ast.Load()))]
        ast.fix_missing_locations(fn)
        ns=dict(ROOT=Path('.'),task_policy=policy,DESCRIPTIONS=dict.fromkeys(['kimi','mimo','nativa','claude-haiku']),json=json,routing_metrics=metrics)
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<admission-prefix>','exec'),ns)
        self.assertEqual(ns['choose']('explique',['kimi','mimo'],multimodal=True),['mimo'])
        for kind in ('audio','video'):
            counts=dict(image=0,audio=0,video=0);counts[kind]=1
            self.assertEqual(ns['choose']('continue',['kimi','mimo'],media={'kinds':[kind],'counts':counts}),['mimo'])
        self.assertEqual(ns['choose']('explique',['kimi','mimo']),['kimi','mimo'])
        for kwargs in [dict(multimodal='true'),dict(multimodal=True,worker=True)]:
            with self.assertRaises(ValueError):ns['choose']('explique',['kimi','mimo'],**kwargs)
        with self.assertRaises(ValueError):ns['choose']('explique',['kimi'],multimodal=True)
        limits=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='limits')
        exec(compile(ast.Module(body=[limits],type_ignores=[]),'<limits>','exec'),ns)
        self.assertTrue(ns['limits']()['imagens'])
    def test_history_media_partitions(self):
        mapping={'image_url':('image','url'),'input_audio':('audio','data'),'video_url':('video','url')}
        for part_type,(kind,field) in mapping.items():
            messages=[{'role':'user','content':[{'type':part_type,part_type:{field:'data:private'}}]},
                      {'role':'assistant','content':'recebido'}, {'role':'user','content':'continue'}]
            record={};metrics.stamp(record,messages)
            self.assertEqual(record['task'],kind+'_analysis')
            self.assertEqual(record['modality_class'],kind)
            self.assertEqual(record['modality_counts'][kind],1)
            self.assertNotIn('private',json.dumps(record))
            messages.insert(0,copy.deepcopy(messages[0]))
            second={};metrics.stamp(second,messages)
            self.assertEqual(second['modality_counts'][kind],2)
    def test_mixed_media(self):
        messages=[{'role':'user','content':[{'type':'image_url','image_url':{'url':'data:x'}},
            {'type':'input_audio','input_audio':{'data':'data:y'}},
            {'type':'video_url','video_url':{'url':'data:z'}}]}]
        record={};metrics.stamp(record,messages)
        self.assertEqual(record['task'],'video_analysis')
        self.assertEqual(record['modality_class'],'image+audio+video')
        self.assertEqual(record['modality_counts'],dict(image=1,audio=1,video=1))
    def test_host_media_summary(self):
        for kind in ('image','audio','video'):
            counts=dict.fromkeys(('image','audio','video'),0);counts[kind]=1
            summary={'kinds':[kind],'counts':counts,'encoded_bytes':123,'prompt':'continue'}
            self.assertEqual(metrics.partition(summary),counts)
            self.assertEqual(metrics.category('continue',counts),kind+'_analysis')
        for bad in [{'counts':{}},{'counts':dict(image=True,audio=0,video=0),'kinds':['image']},
                    {'counts':dict(image=0,audio=0,video=0),'kinds':['image']}]:
            with self.assertRaises(ValueError):metrics.partition(bad)
    def test_media_catalog_gate(self):
        self.assertEqual(policy.capability_catalog(['mimo'],media_integrated=True)['mimo']['input_modalities'],['text','image','audio','video'])
        self.assertEqual(policy.capability_catalog(['mimo'],media_integrated=True,worker=True)['mimo']['input_modalities'],['text'])
    def test_partition_matches_transport_helper(self):
        helper=Path(__file__).parents[2]/'multimodal_stage/image_transport.py'
        tree=ast.parse(helper.read_text(encoding='utf-8'))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='request_media')
        ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<transport-media>','exec'),ns)
        messages=[{'role':'user','content':[{'type':'image_url','image_url':{'url':'data:x'}}]},
                  {'role':'user','content':[{'type':'text','text':'continue'}, {'type':'input_audio','input_audio':{'data':'data:y'}}]}]
        summary=ns['request_media'](messages)
        text,counts=metrics.summarize(messages)
        self.assertEqual(summary['prompt'],text)
        self.assertEqual(metrics.partition(summary),counts)
    def test_cold_start(self):self.assertEqual(self.select({}),'kimi')
    def test_tool_cold_start(self):self.assertEqual(self.select({},['mimo']),'mimo')
    def test_pareto(self):
        self.obs['providers']['mimo'].update(median_cost_usd=.5,median_seconds=1.)
        self.assertEqual(self.select(),'mimo')
    def test_tie(self):self.assertEqual(self.select(),'kimi')
    def test_tradeoff(self):
        self.obs['providers']['mimo'].update(median_cost_usd=.5,median_seconds=3.)
        self.assertEqual(self.select(),'kimi')
    def test_missing_or_invalid(self):
        for field,value in [('task','research'),('model_id','old-model'),('paired_samples',2),('paired_samples',True),('paired_samples','3'),('median_cost_usd',None),('median_cost_usd',float('nan')),('median_cost_usd',float('inf')),('median_cost_usd',-1),('median_seconds',True)]:
            with self.subTest(field=field,value=value):
                obs=copy.deepcopy(self.obs);obs['providers']['kimi'][field]=value
                self.assertEqual(self.select(obs),'kimi')
    def test_malformed(self):
        for obs in [None,[],{'providers':[]},{'providers':{'kimi':None}}]:
            with self.subTest(obs=obs):self.assertEqual(self.select(obs),'kimi')
    def test_no_candidate_grant(self):
        self.obs['providers']['mimo'].update(median_cost_usd=0,median_seconds=0)
        self.assertEqual(self.select(pool=['kimi']),'kimi')
    def test_claude_excluded(self):
        self.assertEqual(policy.automatic_candidates(['claude-haiku','mimo','claude-sonnet']),['mimo'])
        with self.assertRaises(ValueError):routing.select(['claude-haiku'],{},'code',{},policy.AUTOMATIC_ORDER)
    def test_unknown_rejected(self):
        with self.assertRaises(ValueError):policy.automatic_candidates(['unknown'])
    def test_tool_filter(self):
        self.assertEqual(policy.eligible_managers(['kimi','mimo'],'spreadsheet'),['mimo'])
    def test_catalog(self):
        c=policy.capability_catalog(['mimo'])['mimo']
        self.assertEqual(c['input_modalities'],['text'])
        self.assertEqual(c['provider_limits'],{'context_tokens':1048576,'max_output_tokens':131072})
        self.assertEqual(c['transport'],'sse')
        self.assertFalse(policy.capability_catalog(['mimo'],worker=True)['mimo']['task_manager'])
    def test_observations_exact_and_paired(self):
        source=Path(__file__).with_name('iald_auto_router.py').read_text(encoding='utf-8')
        tree=ast.parse(source); fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='observations')
        ns=dict(ROOT=Path('.'),task_policy=policy,sqlite3=sqlite3,json=json,math=math,statistics=statistics,routing_metrics=metrics)
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<observations>','exec'),ns)
        if True:
            tmp=Path(__file__).parent/('fixture_'+uuid.uuid4().hex)
            root=Path(tmp); path=root/'.iald_runtime/app_evaluation/metrics.sqlite3';path.parent.mkdir(parents=True)
            db=sqlite3.connect(path);db.execute('create table turns(data text)')
            base=dict(status='completed',provider='mimo',model='mimo-v2.6-pro',task='code',task_source=metrics.VERSION,modality_counts={'image':0,'audio':0,'video':0},elapsed_seconds=2,calls=[{'cost_estimate_usd':.1}])
            rows=[base,dict(base,task='research'),dict(base,model='old'),dict(base,status='failed'),dict(base,calls=[]),dict(base,modality_counts={'image':1,'audio':0,'video':0}),dict(base,modality_counts=None),dict(base,task_source='legacy_untrusted')]
            for row in rows:db.execute('insert into turns values(?)',(json.dumps(row),))
            db.commit();db.close()
            result=ns['observations'](['mimo'],root,task='code',modality_counts={'image':0,'audio':0,'video':0})['providers']['mimo']
            self.assertEqual(result['samples'],2);self.assertEqual(result['paired_samples'],1)
            self.assertAlmostEqual(result['median_cost_usd'],.1)
    def test_syntax_and_preserved_error_path(self):
        for name in ['iald_auto_router.py','iald_task_policy.py','iald_adaptive_routing.py']:
            ast.parse(Path(__file__).with_name(name).read_text(encoding='utf-8'))
        source=Path(__file__).with_name('iald_auto_router.py').read_text(encoding='utf-8')
        self.assertIn('FAILED_OR_UNCERTAIN_NO_RETRY',source)
        self.assertIn('wallet_runtime.routing_end(wallet_event,billing_usage)',source)

if __name__=='__main__':unittest.main(verbosity=2)
