"""Preserve the map-schema refusal and prepare an additive correction."""
from pathlib import Path
import datetime as dt,hashlib,json,os,sys
R=Path(r'C:\IALD\Central de Patentes');O=R/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE';W=R/'work/rede_quantica_20261013'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(p,v):
 if p.exists():raise FileExistsError(p)
 b=(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode();t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.rename(t,p)
if sys.argv[1]=='prepare':
 receipt=json.loads((O/'MAP_REGISTER_ENTREGA_R1.json').read_text(encoding='utf-8'))
 assert receipt['exit_code']==2 and json.loads(receipt['stdout'])['ok'] is False
 entry=json.loads((O/'MAP_ENTRY_ENTREGA_R1.json').read_text(encoding='utf-8'))
 entry['status']='EXAMINADA';entry['nota']+=' O status EXAMINADA é do mapa; ENTREGUE pertence ao quadro. Recusa anterior de esquema não registrou a rota.'
 new(O/'MAP_ENTRY_ENTREGA_R1A.json',entry)
 code=(W/'register_delivery_r1.py').read_text(encoding='utf-8').replace('MAP_ENTRY_ENTREGA_R1.json','MAP_ENTRY_ENTREGA_R1A.json').replace('MAP_REGISTER_ENTREGA_R1.json','MAP_REGISTER_ENTREGA_R1A.json')
 new(W/'register_delivery_r1a.py',code)
 new(O/'NOTA_REGISTRO_R1.json',{'author':'codex-gerente-tgl','old':pin(O/'MAP_REGISTER_ENTREGA_R1.json'),'correction':pin(O/'MAP_ENTRY_ENTREGA_R1A.json'),'text':'A primeira submissão usou o status ENTREGUE do quadro, não aceito pelo mapa. O mapa recusou antes da gravação. A evidência científica não mudou; nova entrada usa EXAMINADA. A memória executou depois dessa recusa por falha de sequenciamento do wrapper; a remissão ao recibo será corrigida ao lado sob a mesma reivindicação.'})
 print('Prepared additive registration correction; no original overwritten.')
elif sys.argv[1]=='memory':
 import subprocess
 u=json.loads(subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver','F1.REDE'],capture_output=True,text=True,encoding='utf-8',check=True).stdout)
 assert u['reivindicacao']['quem']=='codex-gerente-tgl'
 assert dt.datetime.fromisoformat(u['reivindicacao']['vence_em'])>dt.datetime.now(dt.timezone.utc)
 receipt=json.loads((O/'MAP_REGISTER_ENTREGA_R1A.json').read_text(encoding='utf-8'))
 assert receipt['exit_code']==0
 new(O/'MEMORY_CORRECTION_INTENT_R1.json',{'claim':u['reivindicacao'],'map_receipt':pin(O/'MAP_REGISTER_ENTREGA_R1A.json')})
 text='\n\n### Correção ao lado — F1.REDE, 13/10/2026, em nome de codex-gerente-tgl\n<!-- f1_rede_map_receipt_correction_20261013 -->\nA remissão acima ao MAP_REGISTER_ENTREGA_R1.json aponta a primeira tentativa, recusada pelo esquema do mapa antes de registrar. O recibo válido é MAP_REGISTER_ENTREGA_R1A.json; a rota está EXAMINADA no mapa e a entrega será ENTREGUE no quadro, estatutos diferentes. A correção não altera resultado científico. NOTA_REGISTRO_R1.json conserva a falha de sequenciamento do wrapper.\n'
 entries=[];stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
 for p in [R/'memory/TGL_ATLAS.md',R/'memory/TGL_INDICE_VIVO.md',R/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
  old=p.read_bytes();assert b'f1_rede_map_receipt_correction_20261013' not in old
  bak=p.with_name(p.name+'.bak_'+stamp+'_F1_REDE_MAP');tmp=p.with_name(p.name+'.tmp_'+stamp)
  with bak.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
  assert bak.read_bytes()==old
  raw=old+text.encode()
  with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  assert tmp.read_bytes()==raw and p.read_bytes()==old
  os.replace(tmp,p);assert p.read_bytes()==raw
  entries.append({'surface':pin(p),'backup':pin(bak),'append_only':True})
 new(O/'MEMORY_CORRECTION_R1.json',{'author':'codex-gerente-tgl','claim':u['reivindicacao'],'surfaces':entries,'valid_map_receipt':pin(O/'MAP_REGISTER_ENTREGA_R1A.json')})
 print('Corrected receipt reference additively with byte backups.')
else:raise ValueError(sys.argv[1])
