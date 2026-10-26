import hashlib,json,pathlib,subprocess,uuid
BASE=pathlib.Path(__file__).resolve().parent
PY=r'C:\Python314\python.exe'
SOURCE=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_os_dois_filmes_v7.md')
ACTOR={'id':'codex-video-v7','kind':'agent'}
REF=BASE/'SESSION_REFERENCE.json'
def save(name,obj):
 p=BASE/name
 data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():
  if p.read_bytes()==data:return
  raise RuntimeError('Existing receipt differs: '+str(p))
 p.write_bytes(data)
def cli(script,payload):
 r=subprocess.run([PY,'-B','-X','utf8',script],input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
 if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
 return json.loads(r.stdout)
if __name__=='__main__':
 source_sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 u={'id':'F0.FILMES_V7_20261024','frente':'F0','titulo':'Construir os dois filmes V7 da TGL — ORDEM 022','dono':ACTOR['id'],'status':'PRONTA','fonte':str(SOURCE),'criterio_de_fechado':'Partes A–E da ORDEM 022 entregues com evidências; revisão e publicação pela gerência.','escopo':'Somente video_um e recibos próprios/túnel; preservar Nós, Atlas, espelho e site.','levantamento':'Consulta QUADRO/PROGRAMA e mapa de rotas em 24/10: apenas encaminhamento F0.ORDEM022_ENCAMINHAMENTO; reutilizar cinema_v7 e entrega V6 preservados.'}
 save('UNIDADE.json',[u])
 for args in [['nova','--json',str(BASE/'UNIDADE.json'),'--quem',ACTOR['id']],['reivindicar',u['id'],'--quem',ACTOR['id'],'--nota','Construção autorizada ORDEM 022, fontes canônicas somente leitura.']]:
  r=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True,text=True,encoding='utf-8')
  if r.returncode:raise RuntimeError(r.stdout+r.stderr)
  save('BOARD_'+args[0]+'.json',json.loads(r.stdout));print(r.stdout)
 payload={'operation':'init','objective_file':str(SOURCE),'objective_sha256':source_sha,'request_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'codex-video-v7-01a08ff4-20261024-ordem022')),'scope':{'house':'TGL','principal':'operador-iald'},'actor':ACTOR,'write_reference':str(REF)}
 out=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',payload);save('INIT.json',out)
 print('INIT',str(REF),out.keys())
