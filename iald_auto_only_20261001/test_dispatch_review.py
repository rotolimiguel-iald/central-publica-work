import unittest,tempfile,threading,time,json,sys
from pathlib import Path
from unittest.mock import Mock,patch
from types import SimpleNamespace
import iald_app_providers as p
from test_evaluation import Response,chunk,USAGE
from test_auto_only import h,S

class Revocation(unittest.TestCase):
 def test_revoked_after_reserve_refunds_only_known_unsent_call(self):
  from test_public_budgets import PublicAccount
  import hashlib
  calls=[0];sent=Mock(side_effect=AssertionError('must not dispatch'))
  def authorize():
   calls[0]+=1
   if calls[0]==2:raise PermissionError('revoked after reserve')
  with tempfile.TemporaryDirectory() as tmp,patch.object(p,'adapter',return_value=SimpleNamespace(load_key=lambda:'synthetic')):
   ev=p.Evaluation(tmp);ev.save=Mock()
   account=PublicAccount(tmp,hashlib.sha256(b'guest').hexdigest(),1,2,3)
   with self.assertRaises(PermissionError):
    ev._api('deepseek',[{'role':'user','content':'test'}],[],lambda *a:None,lambda _:None,threading.Event(),[],{'calls':[]},time.monotonic(),sent,account,authorize)
   account.close()
   with account.guard._connect() as db:
    self.assertEqual(db.execute('SELECT SUM(actual) FROM calls').fetchone()[0],0)
   self.assertIsNone(account.pending)
  sent.assert_not_called()

 def test_external_refusal_discards_only_before_send(self):
  env={};h.extract(S/'iald_web_server.py',functions=('_check_reserved_dispatch',),env=env)
  account=SimpleNamespace(descartar_ultima_chamada=Mock())
  env['_check_reserved_dispatch'](lambda:None,account);account.descartar_ultima_chamada.assert_not_called()
  def denied():raise PermissionError('revoked')
  with self.assertRaises(PermissionError):env['_check_reserved_dispatch'](denied,account)
  account.descartar_ultima_chamada.assert_called_once()

 def test_mimo_revocation_after_tool_prevents_second_post(self):
  active=[True];sends=[]
  def authorize():
   if not active[0]:raise PermissionError('revoked')
  def execute(*a):active[0]=False;return 'public result'
  tc={'index':0,'id':'call_one','type':'function','function':{'name':'search_tgl','arguments':'{}'}}
  def post(*a,**kw):
   sends.append(1);return Response([chunk('mimo',{'tool_calls':[tc]}),chunk('mimo',finish='tool_calls'),chunk('mimo',usage=USAGE),'[DONE]'])
  with tempfile.TemporaryDirectory() as tmp,patch.object(p,'adapter',return_value=SimpleNamespace(load_mimo=lambda:'synthetic')):
   ev=p.Evaluation(tmp);ev.save=Mock()
   with self.assertRaises(PermissionError):
    ev._api('mimo',[{'role':'user','content':'test'}],[{'type':'function','function':{'name':'search_tgl','parameters':{'type':'object'}}}],execute,lambda _:None,threading.Event(),[],{'calls':[]},time.monotonic(),post,authorize=authorize)
  self.assertEqual(sends,[1])

 def test_kimi_revoked_before_generator_never_calls_cli(self):
  execute=Mock(side_effect=AssertionError('must not send'))
  def deny():raise PermissionError('revoked')
  with tempfile.TemporaryDirectory() as tmp,patch.object(p,'adapter',return_value=SimpleNamespace(execute=execute)):
   frames=list(p.Evaluation(tmp).stream('kimi',[{'role':'system','content':'public'},{'role':'user','content':'test'}],[],lambda *a:None,memory_sha256='synthetic',authorize=deny))
  execute.assert_not_called();self.assertTrue(any('falha_motor' in frame for frame in frames))

class Moderation(unittest.TestCase):
 def test_native_blocked_and_unavailable_never_reach_model(self):
  import iald_auto_router as router
  for decision,kind in [({'ok':True,'bloquear':True},'moderacao'),({'ok':False},'moderacao_indisponivel')]:
   mod=Mock(return_value=decision);prepare=Mock(side_effect=AssertionError('must not prepare model'))
   motors=SimpleNamespace(consentiu=lambda *a:True,extrair_do_cliente=lambda _:('profile',False),moderar_textos=mod,MENSAGEM_MODERACAO_BLOQUEIO='blocked')
   env=dict(app_router=router,app_providers=p,iald_motores=motors,MODERACAO_LIGADA=True,MODERACAO_FALHA='bloquear',
       _dispatch_guard=lambda *a:lambda:None,req_lib=SimpleNamespace(post=Mock()),MOTORES_CFG=SimpleNamespace(url_base='invalid',chave='synthetic'),
       _CACHE_MODERACAO=None,MSG_MODERACAO_INDISPONIVEL='unavailable',_prepare_native_payload=prepare,_sse_aviso=lambda text,kind:kind)
   h.extract(S/'iald_web_server.py',functions=('_chat_nativa_automatica',),env=env)
   result=env['_chat_nativa_automatica']({'messages':[{'role':'user','content':'synthetic'}]},'guest',{'admin':False})
   self.assertEqual(result,kind);mod.assert_called_once();prepare.assert_not_called()

 def test_native_guard_checks_after_response_before_generation(self):
  import iald_auto_router as router
  state={'admin':False};sends=[]
  def agent(messages,**kw):kw['verificar_payload']({'messages':messages});sends.append(1);yield 'generated'
  env=dict(app_router=router,app_providers=p,iald_motores=SimpleNamespace(consentiu=lambda *a:True,extrair_do_cliente=lambda _:('',False)),
      MODERACAO_LIGADA=False,load_users_estrito=lambda:{'guest':state},_prepare_native_payload=lambda body,_:(body,[],lambda _:None),
      _SEMAFORO_GRATUITO=threading.BoundedSemaphore(1),agent_loop=agent,Response=h.Response,
      _identificar_resposta=lambda r,_:r,_modelo_nativo_resposta=lambda:{},_sse_aviso=lambda *a:None,json=json)
  h.extract(S/'iald_web_server.py',functions=('_chat_nativa_automatica','_dispatch_guard'),env=env)
  response=env['_chat_nativa_automatica']({'messages':[{'role':'user','content':'test'}]},'guest',state)
  state['bloqueado']=True
  with self.assertRaises(PermissionError):list(response.response)
  response.close();self.assertEqual(sends,[])
