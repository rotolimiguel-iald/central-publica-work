from finish_delta import *
FILES={'core':'AUDITORIA_ACAO_CORE_A1B.json','absorcao':'AUDITORIA_ABSORCAO_A1B.json','fourier':'AUDITORIA_FOURIER_TRANSLACAO_A1B.json','grafo':'AUDITORIA_GRAFO_POSITIVO_A1B.json','espectral':'AUDITORIA_GRAFO_ESPECTRAL_A1B.json','calculo':'AUDITORIA_CALCULO_MULTIPLICADOR_A1B.json','potencias':'AUDITORIA_POTENCIAS_REGULARES_A1B.json','afiliacao':'AUDITORIA_AFILIACAO_REGULAR_A1B.json','escala_dual':'AUDITORIA_ESCALA_DUAL_REGULAR_A1B.json','cortes_inverso':'AUDITORIA_CORTES_INVERSO_A1B.json','fechamento_gns':'AUDITORIA_FECHAMENTO_GNS_A1B.json'}
def main(key):
 out=R/CONFIG[key][0];p=R/FILES[key];j=load(p);pins=[pin(p)]
 snapshot=load(Path(load(out/'SNAPSHOT_POINTER.json')['attempt'])/'snapshot.json')
 expected={t['name'] for t in snapshot['targets']}
 assert {t['name'] for t in j['targets']}==expected
 for m in j['modules']:
  for name in ['source','object']:ck(m[name]);pins.append(m[name])
  assert any(x['target'] and x['original']==m['source'] for x in snapshot['sources'])
 ck(j['positive_build']);pins.append(j['positive_build'])
 run=load(Path(j['positive_build']['path']));assert run['returncode']==0
 for k in ['stdout','stderr']:
  if k in run:ck(run[k]);pins.append(run[k])
 rows=[]
 for i,row in enumerate(j['commands']):
  for n in ['source','stdout','stderr']:ck(row[n]);pins.append(row[n])
  text=Path(row['stdout']['path']).read_text(encoding='utf8');low=text.lower()
  if i==0:
   assert row['returncode']==0
   a=axioms(text);assert set(a)==expected and all(set(v)<=ALLOWED for v in a.values())
  else:
   assert row['returncode']!=0 and 'type mismatch' in low
   assert not any(t in low for t in ['unknown identifier','unknown module','object file','timeout','unexpected token','unterminated'])
  rows.append(dict(label=row['label'],returncode=row['returncode'],stream_excerpt=text,source_text=Path(row['source']['path']).read_text(encoding='utf8'),source=row['source'],stdout=row['stdout'],stderr=row['stderr']))
 save(out/'negative_controls_read.json',dict(timestamp=now(),status='AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT',author_execution=True,own_execution=False,author_audit=pin(p),rows=rows,pins=pins))
 print(json.dumps(dict(status='VERIFIED',count=len(rows)-1,rows=[dict(label=r['label'],returncode=r['returncode'],text=r['stream_excerpt']) for r in rows[1:]]),ensure_ascii=False))
if __name__=='__main__':main(sys.argv[1])
