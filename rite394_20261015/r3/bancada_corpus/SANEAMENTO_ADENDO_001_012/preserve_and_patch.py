from support import *
import re,difflib
f=json.loads((ROOT/'FICHA_SANEAMENTO.json').read_text(encoding='utf-8'))
p=json.loads((ROOT/'PROVENIENCIA_COPIA.json').read_text(encoding='utf-8'))
expected={}
for r in p['files']:
 if r['path'].endswith('.lean') and not r['path'].startswith('.lake'):
  expected[r['source']]=r['sha256']
for r in f['sources']+f['orders']+f['modules44']:expected[r['path']]=r['sha256']
for r in f['preliminary_g']:
 for root in r['roots']:
  for x in root:
   if x['exists']:expected[x['path']]=x['sha256']
for r in json.loads((ROOT/'heartbeat/ENTREGAS_LIDAS.json').read_text(encoding='utf-8')):expected[r['path']]=r['sha256']
rows=[]
for name,h in sorted(expected.items()):
 q=Path(name);now=digest(q) if q.exists() else None
 rows.append(dict(path=name,initial_sha256=h,final_sha256=now,unchanged=h==now))
record(ROOT/'PRESERVACAO_FONTES.json',dict(files=len(rows),all_unchanged=all(x['unchanged'] for x in rows),rows=rows,scope='Fontes locais copiadas fora dos pacotes, fontes/ordens da ficha, entregas lidas e seis objetos B6 com traces. Pacotes e todos os objetos originais nao foram rehashados integralmente ao final; pins iniciais da copia estao em PROVENIENCIA_COPIA.json.'))
print('PRESERVATION',len(rows),'CHANGED',sum(not x['unchanged'] for x in rows))
proposals=json.loads((ROOT/'PROPOSTAS_INICIAIS.json').read_text(encoding='utf-8'))
patch=[];deltas=[]
for row in proposals:
 old=Path(row['source']);new=ROOT/'kernel/TGLExt'/Path(row['proposal']).name
 assert digest(old)==row['before']
 a=old.read_bytes();b=new.read_bytes();rel='TGLExt/'+new.name
 patch+=difflib.unified_diff(a.decode('utf-8').splitlines(True),b.decode('utf-8').splitlines(True),fromfile='a/'+rel,tofile='b/'+rel)
 deltas.append(dict(item=row['item'],source=str(old),source_sha256=digest(old),proposal=str(new),proposal_sha256=digest(new),bytes_before=len(a),bytes_after=len(b),crlf_before=a.count(b'\r\n'),crlf_after=b.count(b'\r\n')))
for name in ['SectorFriedmannAdditive','AuditSanitation']:
 q=ROOT/'kernel/TGLExt'/(name+'.lean');b=q.read_bytes();rel='TGLExt/'+q.name
 patch+=difflib.unified_diff([],b.decode('utf-8').splitlines(True),fromfile='/dev/null',tofile='b/'+rel)
 deltas.append(dict(item='f' if name=='SectorFriedmannAdditive' else 'auditoria',source=None,proposal=str(q),proposal_sha256=digest(q),bytes_after=len(b)))
atomic(ROOT/'PROPOSTA.patch',''.join(patch));record(ROOT/'DELTA_FONTES.json',deltas)
checks=[]
for q in [Path(r['proposal']) for r in deltas]+list((ROOT/'probes').glob('*.lean')):
 hits=[dict(line=n,text=l) for n,l in enumerate(q.read_text(encoding='utf-8').splitlines(),1) if re.search(r'\b(?:axiom|sorry|admit|sorryAx|native_decide|trustCompiler)\b',l)]
 checks.append(dict(path=str(q),sha256=digest(q),hits=hits))
record(ROOT/'SCAN_CODIGO.json',dict(all_clean=all(not x['hits'] for x in checks),files=checks,scope='Scan lexical dos fontes finais da proposta e sondas; nao substitui os prints transitivos de axiomas.'))
assert all(not x['hits'] for x in checks)
