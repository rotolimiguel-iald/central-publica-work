import ast,json,unittest
from pathlib import Path
p=Path(r'C:\IALD\Central de Patentes\work\iald_v410_20261111\app\R4\runtime\iald_web_server.py')
nodes=ast.parse(p.read_bytes()).body
selected=[n for n in nodes if isinstance(n,ast.FunctionDef) and n.name in ('_science_tool','_prepare_native_payload')]
class Snap:
 def __init__(self,version): self.version=version;self.identity={'release':version};self.prefix='core '+version;self.calls=[]
 def check(self):return {'release':self.version}
 def pre_retrieve(self,m):self.calls.append(m);return {'prompt':' source '+self.version}
 def execute_tool(self,name,args):return {'release':self.version,'text':'immutable'}
class Native:
 configured_window=staticmethod(lambda _:100000)
 prepare_activity_payload=staticmethod(lambda payload,**kw:(payload,{}))
 attach_context=staticmethod(lambda m,p:[{'role':'system','content':p}]+m)
 check_text_window=staticmethod(lambda payload,window,base_url:len(str(payload)))
class Source:
 tool_definitions=staticmethod(lambda:[])
ns=dict(json=json,SCIENCE_TOOLS={'search_tgl'},SERVE_DIR='fixture',MEMORIA_EXTERNA=type('Memory',(),{'nucleus_manifest':'fixture'})(),
 native_memory=Native,iald_kernel=Source,iald_core_indexado=Source,_ferramentas_para=lambda _:[],ACTIVE_MODEL_ID='model',LLAMA_URL='fixture',MODELS={'model':{}},
 app_memory=type('App',(),{'current':staticmethod(lambda:None),'project_messages':staticmethod(lambda x:x)})())
exec(compile(ast.Module(body=selected,type_ignores=[]),str(p),'exec'),ns)
class Tests(unittest.TestCase):
 def test_tool_uses_captured(self):
  old=Snap('v410');ns['_capture_science']=lambda:Snap('v411')
  result=json.loads(ns['_science_tool'](old,lambda *a,**k: self.fail('legacy reader'), 'search_tgl',{}));self.assertEqual(result['release'],'v410')
 def test_atlas_explicit_refusal(self):
  r=json.loads(ns['_science_tool'](Snap('v410'),lambda *a,**k:self.fail('private reader'),'iald_atlas_read',{}));self.assertEqual(r['status'],'UNAVAILABLE_USE_VERSIONED_SEARCH_TGL')
 def test_unrelated_tool_preserves_authority(self):
  seen=[];ns['_science_tool'](Snap('v410'),lambda *a,**kw:seen.append(kw),'get_current_datetime',{},operator_authorized=False);self.assertFalse(seen[0]['operator_authorized'])
 def test_live_catalog_refused(self):
  for name in ('iald_public_read','iald_public_search'):
   r=json.loads(ns['_science_tool'](Snap('v410'),lambda *a,**k:self.fail('live catalog'),name,{}));self.assertEqual(r['status'],'UNAVAILABLE_USE_VERSIONED_SEARCH_TGL')
 def test_external_source_labeled(self):
  r=json.loads(ns['_science_tool'](Snap('v410'),lambda *a,**k:'external','fetch_url',{}));self.assertEqual(r['scope'],'EXTERNAL_SOURCE_NOT_PINNED_SCIENTIFIC_RELEASE')
 def test_native_survives_active_change(self):
  old=Snap('v410');ns['_capture_science']=lambda:old
  body,defs,check=ns['_prepare_native_payload']({'messages':[{'role':'user','content':'query'}]},'app')
  ns['_capture_science']=lambda:Snap('v411');self.assertIs(check.science_snapshot,old);self.assertIn('v410',body['messages'][0]['content']);check(body)
 def test_native_model_change_refuses(self):
  ns['_capture_science']=lambda:Snap('v410');body,_,check=ns['_prepare_native_payload']({'messages':[{'role':'user','content':'q'}]},'app')
  ns['ACTIVE_MODEL_ID']='changed'
  try:
   with self.assertRaises(ValueError):check(body)
  finally:ns['ACTIVE_MODEL_ID']='model'
if __name__=='__main__':unittest.main()


