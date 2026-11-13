"""Close order012 only after own mission has all requirements satisfied."""
from pathlib import Path
import json,hashlib,datetime,os
import task
A=Path(__file__).resolve().parent
P=Path(r'C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\012_RESULTADO.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(Path(p).read_bytes())}
projection=task.project();assert not projection['projection']['active'], 'Mission still has active requirements'
delivery=json.loads((A/'TECHNICAL_DELIVERY_R4.json').read_bytes());assert delivery['identity']['release']=='v410'
old=P.read_bytes();d=json.loads(old);assert d['ordem']=='ORDEM_012';d.setdefault('historico_app',[]).append(d['app'])
d.update(estado='cumprida',autor=task.OWNER,hora=datetime.datetime.now().astimezone().isoformat(),resumo='App e JEV v410 instalados e conferidos; fila v410 reutilizada; acervo público integral versionado com recuperação por chamada e atualizador local aguardando revisão independente para versões futuras.')
d['app']={'release_instalada':'v410','status':'INSTALLED_VERIFIED_INDEPENDENTLY_ACCEPTED','runtime_alterado':True,'restart':True,'arquivos_verificados':delivery['files_verified'],'identity':delivery['identity'],'updater_phase':delivery['updater']['phase'],'automatic_review_consumer':False,'generation_calls':0,'remote_count_calls':4}
d['o_que_falta']=[];d['limites']=delivery['limitations'];assert str(A/'SESSION_REFERENCE.json') in d['referencias']
for name in ('TECHNICAL_DELIVERY_R4.json','INSTALLED_VERIFICATION.json','LIVE_BACKEND.json','UPDATER_RUNNING_VERIFIED.json','TORRE_RESULT.json','MEMORY_DEPOSIT_RECEIPT_R4.json','validation/review_final.json','validation/review_deploy.json','validation/review_verify.json'):
 d['arquivos'].append(pin(A/name))
raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode();stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');bak=P.with_name(P.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old and P.read_bytes()==old
tmp=P.with_name(P.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and P.read_bytes()==old;os.replace(tmp,P);assert P.read_bytes()==raw
result={'status':'ORDER_012_COMPLETED','receipt':pin(P),'backup':str(bak),'mission_revision':projection['receipt']['revision']}
with (A/'ORDER_012_FINAL_WRITTEN_R4.json').open('xb') as f:f.write(json.dumps(result,indent=2).encode())
print(json.dumps(result))
