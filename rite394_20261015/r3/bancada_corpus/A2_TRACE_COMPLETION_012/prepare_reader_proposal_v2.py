from pathlib import Path
import datetime, difflib, hashlib, json, os
root=Path(__file__).resolve().parent
def put(name,b):
    p=root/name;assert not p.exists()
    if isinstance(b,str):b=b.encode('utf8')
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
old=(root/'PROPOSTA_LEITORES_EXISTENTES.py').read_text(encoding='utf8')
needle='and kf.get("audit_returncode") == 0'
assert old.count(needle)==1
new=old.replace(needle,'and type(kf.get("audit_returncode")) is int\n                and kf.get("audit_returncode") == 0')
candidate=put('PROPOSTA_LEITORES_EXISTENTES_V2.py',new)
baseline=(root/'CANONICAL_READERS_SNAPSHOT.py').read_text(encoding='utf8')
diff=put('PROPOSTA_LEITORES_EXISTENTES_V2.diff',''.join(difflib.unified_diff(baseline.splitlines(True),new.splitlines(True),fromfile='CANONICAL_READERS_SNAPSHOT.py',tofile='PROPOSTA_LEITORES_EXISTENTES_V2.py')))
data=json.loads((root/'PROPOSTA_MAPA_CONSUMIDORES.json').read_bytes())
data['timestamp']=datetime.datetime.now().astimezone().isoformat()
data['candidate']=candidate;data['diff']=diff
data['P2_READERS_01']={'status':'FIXED_IN_V2_FOR_REVIEW','cause':'Inherited equality accepted bool False as rc0.','delta':'Require exact int type before comparing returncode with zero.','v1_preserved':True}
put('PROPOSTA_MAPA_CONSUMIDORES_V2.json',json.dumps(data,ensure_ascii=False,indent=2))
test=(root/'test_reader_proposal.py').read_text(encoding='utf8')
for a,b in [('PROPOSTA_LEITORES_EXISTENTES.py','PROPOSTA_LEITORES_EXISTENTES_V2.py'),('PROPOSTA_MAPA_CONSUMIDORES.json','PROPOSTA_MAPA_CONSUMIDORES_V2.json'),('TESTES_LEITORES_COPIADOS.json','TESTES_LEITORES_COPIADOS_V2.json')]:test=test.replace(a,b)
anchor="m=copy.deepcopy(base);m['lake_build_ok']=False;m.update"
assert test.count(anchor)==1
insertion="""for malformed in [False, True, '0', 0.0, None]:
    m=copy.deepcopy(base);m['audit_returncode']=malformed
    check('P2_READERS_01_exact_returncode_type:'+repr(malformed),not any(ns['verify_v350_modular_provenance'](m)[f] for f in new_flags))
"""
test=test.replace(anchor,insertion+anchor)
put('test_reader_proposal_v2.py',test)
print(json.dumps({'candidate':candidate,'P2_READERS_01':'fixed in source, awaiting tests/review'}))
