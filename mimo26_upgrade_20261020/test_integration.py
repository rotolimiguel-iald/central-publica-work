"""Offline integration boundaries; production server is never imported."""
from pathlib import Path
import ast, base64, hashlib, json, sys, tempfile, unittest
from types import SimpleNamespace
from unittest.mock import Mock

W=Path(__file__).parent
S=W/'final_stage'
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(S),str(R)]
(W/'test_temp').mkdir(exist_ok=True)
tempfile.tempdir=str(W/'test_temp')
import iald_mimo_multimodal as media
import iald_routing_metrics as metrics
import iald_router_media_view as router_media_view

def functions(path,names,namespace):
    tree=ast.parse(path.read_bytes())
    nodes=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in names]
    assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    return namespace

provider=functions(S/'iald_app_providers.py',{'request_media','image_parts','wire_messages'},
    dict(base64=base64,binascii=__import__('binascii'),router_media_view=router_media_view,app_memory=SimpleNamespace(project_messages=lambda m:m)))

def part(name,kind,field,mime):
    raw=(W/'test_assets'/name).read_bytes()
    return {'type':kind,kind:{field:'data:'+mime+';base64,'+base64.b64encode(raw).decode()}}

IMAGE=part('two_colors.png','image_url','url','image/png')
AUDIO=part('tone.wav','input_audio','data','audio/wav')
VIDEO=part('red_clip.mp4','video_url','url','video/mp4')

class Integration(unittest.TestCase):
    def test_decoder_ready(self):
        caps=media.media_capabilities()
        self.assertTrue(caps['video']);self.assertIn('wav',caps['audio_formats'])
    def test_real_audio(self):
        self.assertEqual(media.media_part(AUDIO,media_authorized=True),AUDIO)
    def test_real_video(self):
        self.assertEqual(media.media_part(VIDEO,media_authorized=True),VIDEO)
    def test_no_media_consent(self):
        with self.assertRaises(ValueError):media.media_part(AUDIO)
    def test_remote_media_refused(self):
        with self.assertRaises(ValueError):media.media_part({'type':'video_url','video_url':{'url':'https://example.com/a.mp4'}},media_authorized=True)
    def test_video_wrong_stream(self):
        bad={'type':'video_url','video_url':{'url':AUDIO['input_audio']['data']}}
        with self.assertRaises(ValueError):media.media_part(bad,media_authorized=True)
    def test_wire_preserves_science_and_history(self):
        messages=[{'role':'user','content':[{'type':'text','text':'Confira as cores'},IMAGE]}, {'role':'assistant','content':'Recebido'}, {'role':'user','content':'Continue'}]
        wire=provider['wire_messages'](messages,'TGL_UNCHANGED','PROFILE',provider='mimo',images_authorized=True,media_authorized=True)
        self.assertTrue(wire[0]['content'].startswith('TGL_UNCHANGED'))
        self.assertEqual(wire[1]['content'][1],IMAGE);self.assertEqual(wire[-1]['content'],'Continue')
    def test_text_executor_cannot_take_media(self):
        with self.assertRaises(ValueError):provider['wire_messages']([{'role':'user','content':[IMAGE]}],'TGL',provider='kimi',images_authorized=True)
    def test_metadata_has_no_bytes(self):
        summary=provider['request_media']([{'role':'user','content':[{'type':'text','text':'Haja luz'},IMAGE]}])
        self.assertEqual(summary['prompt'],'Haja luz');self.assertNotIn('base64',json.dumps(summary))
        record={};metrics.stamp(record,[{'role':'user','content':[IMAGE]},{'role':'user','content':'Continue'}])
        self.assertEqual(record['task'],'image_analysis');self.assertNotIn('base64',json.dumps(record))
    def test_consent_version_scoped(self):
        ns=functions(S/'iald_motores.py',{'versao_do_consentimento'},dict(OPENAI='openai',CLAUDE='claude',AUTO='automatico',VERSAO_CONSENTIMENTO=1,VERSAO_CONSENTIMENTO_ANTHROPIC=1,_motor_do_provedor=lambda p:p))
        fn=ns['versao_do_consentimento'];self.assertEqual(fn('mimo'),2);self.assertEqual(fn('automatico'),3);self.assertEqual(fn('openai'),1);self.assertEqual(fn('claude'),1)
    def auto_ns(self,consented=True):
        router=SimpleNamespace(AUTO='automatico',DESCRIPTIONS={'mimo':'m','kimi':'k'},allowed=lambda *a:True,
            choose=Mock(return_value=('mimo',{})),route_instruction=lambda r:'route',bind_scope=lambda *a:None)
        motors=SimpleNamespace(consentiu=lambda record,key:consented if key=='mimo' else True)
        providers=SimpleNamespace(MODELS={'mimo':{}},allowed=lambda *a:True,**provider)
        rows=[dict(id='mimo',disponivel=True,modelo='mimo-v2.6-pro'),dict(id='kimi',disponivel=True,modelo='kimi-code/k3')]
        ns=dict(app_router=router,app_providers=providers,iald_motores=motors,
            _consentimento_automatico=lambda *a:dict(dado=True),
            _consentimento_do_motor=lambda *a:dict(dado=consented,versao=2,provedor='Xiaomi MiMo',texto='MEDIA_NOTICE'),
            _sse_aviso=lambda message,code,*args:dict(code=code),_opcoes_de_motor=lambda *a:rows,
            _automatic_budget_available=lambda *a:True,MODERACAO_LIGADA=False,
            operator_bench=SimpleNamespace(is_operator=lambda *a:False),
            load_users_estrito=lambda:{'luiz':{}},_new_app_task_scope=lambda *a,**kw:None,
            _dispatch_guard=lambda *a:lambda:None,
            _chat_avaliacao=Mock(return_value=SimpleNamespace(status='prepared')))
        router.RoutingContextOverflow=type('RoutingContextOverflow',(ValueError,),{})
        functions(S/'iald_web_server.py',{'_chat_automatico_autorizado'},ns)
        return ns
    def test_auto_requires_current_consent_before_jev(self):
        ns=self.auto_ns(False)
        out=ns['_chat_automatico_autorizado']({'messages':[{'role':'user','content':[IMAGE]}]},'luiz',{},True,0)
        self.assertEqual(out['code'],'consentimento_ia');ns['app_router'].choose.assert_not_called()
    def test_auto_routes_metadata_but_keeps_attachment(self):
        ns=self.auto_ns(True);req={'messages':[{'role':'user','content':[{'type':'text','text':'Descreva'},IMAGE]}]}
        out=ns['_chat_automatico_autorizado'](req,'luiz',{},True,0)
        self.assertEqual(out.status,'prepared')
        args,kw=ns['app_router'].choose.call_args
        self.assertEqual(args[0],'Descreva');self.assertTrue(kw['multimodal']);self.assertNotIn('base64',json.dumps(kw))
        self.assertIs(ns['_chat_avaliacao'].call_args.args[0],req)
    def test_bad_media_before_jev(self):
        ns=self.auto_ns(True);bad={'type':'image_url','image_url':{'url':'https://example.com/a.png'}}
        ns['_chat_automatico_autorizado']({'messages':[{'role':'user','content':[bad]}]},'luiz',{},True,0)
        ns['app_router'].choose.assert_not_called()
    def test_science_pins_preserved(self):
        baseline=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
        for entry in baseline['files']:
            self.assertEqual(hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest(),entry['sha256'])

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Integration))
    (W/'INTEGRATION_TESTS.json').write_bytes(json.dumps(dict(passed=result.wasSuccessful(),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),provider_calls=0),indent=2).encode())
    raise SystemExit(not result.wasSuccessful())
