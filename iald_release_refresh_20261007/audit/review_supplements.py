"""Independent checks of new foundation, retained numerical fields and native receipt."""
from pathlib import Path
from datetime import datetime,timezone
import json, ast
import review_memory as r
from audit_helpers import save
W=r.WORK;S=r.STAGE;OLD=W.parent/'iald_release_refresh_20261006'
m=r.load(S/'manifest_staged.json');source=r.load(m['published_evidence']['result']['path'])
previous=r.load(OLD/'audit/critical_numeric_review.json');numeric=previous['minimum_source_fields']
base='/core/fundacao_v390'
foundation=[base+'/'+k for k in ['verdict','all_verified','does_not_gate_core','kernel_flags_ok','kernel_flags_total','leitura','recusa','passagem','estatuto_do_fecho','not_claimed','status']]+[base+'/borchers/leitura']
foundation += [base+'/clausulas/'+str(i)+'/'+k for i in range(len(source['core']['fundacao_v390']['clausulas'])) for k in ['n','em_palavras','teorema']]
allfields={x['pointer'] for x in numeric}|set(foundation)
surfaces={};numeric_surfaces={}
for file,marker in [(Path(m['active_cluster']['path']),'DICIONÁRIO DO CLUSTER'),(S/'haiku_prefix.md','DICIONÁRIO DE LITERAIS')]:
 text=r.read(file).decode('utf8');dic=r.loads(text.split(marker+'\n',1)[1].split('\n',1)[0]);expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
 if 'DICIONÁRIO DE INDICADORES LITERAIS\n' in text:r.BOOLEAN_DICTIONARY.update(r.loads(text.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0]))
 ts=r.topics(text,source['core']);seen={};roundtrips={}
 for name in {p.split('/')[2] for p in allfields}:
  p='/core/'+name
  for line in ts[name].splitlines():
   if line.startswith('{'):
    node=r.decode(r.loads(line),dic,expo,source,name)
    restored=r.reconstruct(node,source,p,p,seen)
    roundtrips[name]=r.same(restored,source['core'][name])
 checks=[{'pointer':p,'inline_exact':r.covered(p,r.resolve(source,p),seen),'value':r.resolve(source,p)} for p in foundation]
 surfaces[file.name]={'sha256':r.sha(text.encode()),'source_roundtrip_exact':roundtrips['fundacao_v390'],'checks':checks}
 nc=[{'pointer':x['pointer'],'value':r.resolve(source,x['pointer']),'passed':r.same(x['value'],r.resolve(source,x['pointer'])) and r.covered(x['pointer'],r.resolve(source,x['pointer']),seen)} for x in numeric]
 numeric_surfaces[file.name]={'sha256':r.sha(text.encode()),'checks':nc,'passed':all(x['passed'] for x in nc)}
stable=all(r.sha(Path(p).read_bytes())==pin['sha256'] for p,pin in r.inputs.items())
common={'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'prefix_sha256':r.sha(r.read(S/'haiku_prefix.md')),'input_pins':dict(r.inputs),'inputs_stable':stable}
fok=stable and all(s['source_roundtrip_exact'] and all(c['inline_exact'] for c in s['checks']) for s in surfaces.values())
save('foundation_projection_review.json',dict(common,status='PASS' if fok else 'FAIL',source_sha256=r.sha(r.read(m['published_evidence']['result']['path'])),surfaces=surfaces,scope='Nine numbered clauses, their Portuguese concept and theorem, scopes and not_claimed all resident and exact; source proofs not executed.'))
nok=stable and all(s['passed'] for s in numeric_surfaces.values())
save('critical_numeric_review.json',dict(common,status='PASS' if nok else 'FAIL',minimum_source_fields=numeric,surfaces=numeric_surfaces,scope='Ten essential numeric and negative-qualifier fields retained from v389, not every historical parent inline.'))
# Native receipt and staged runtime only; do not call a model or execute runtime.
checks=[]
def check(n,ok,e=None):checks.append({'name':n,'passed':bool(ok),'evidence':e})
package=r.load(S/'haiku_runtime/manifest.json');receipt=r.load(package['measurement_receipt']);budget=receipt['budget'];prefix=r.read(S/'haiku_prefix.md');prep=r.load(S/'prepared.json')
check('prefix_runtime_and_native_receipt_same_bytes',prefix==r.read(S/'haiku_runtime/prefix.md') and r.sha(prefix)==package['prefix_sha256']==receipt['draft_sha256'])
check('receipt_pin_and_budget',r.sha(r.read(package['measurement_receipt']))==package['measurement_receipt_sha256'] and r.same(budget,package['budget']))
check('scientific_source_and_identity_pins',package['deployment']==prep['deployment_identity'] and receipt['source_sha256']==prep['source_sha256'] and receipt['cluster_sha256']==prep['deployment_identity']['cluster_sha256'])
check('native_180k_target_10k_reserve',budget['permanent_tokens']>=180000 and budget['remaining_tokens']>=10000 and budget['reserved_output_tokens']==4096 and budget['margin_tokens']==1024 and budget['request_input_tokens']+budget['reserved_output_tokens']+budget['margin_tokens']+budget['remaining_tokens']==200000 and budget['ready'] and budget['fits'],budget)
check('native_tools_and_model_pins',package['tools_sha256']==receipt['native_tools_sha256'] and package['model']==receipt['model']==budget['model'])
check('generation_not_used_in_count',receipt['generation_requests']==0 and receipt['count_requests']==2)
runtime=r.read(r.APP/'claude_memory_package.py').decode('utf8')
check('runtime_10k_policy_intact',"checked['remaining_tokens']<10000" in runtime and "b.get('reserved_output_tokens')!=4096" in runtime and "b.get('margin_tokens')!=1024" in runtime)
check('public_340k_limit_kept',prep['public_tokens']<=340000,prep['public_tokens'])
check('input_pins_stable',all(r.sha(Path(p).read_bytes())==pin['sha256'] for p,pin in r.inputs.items()))
aok=all(c['passed'] for c in checks)
save('memory_admission_review.json',dict(common,status='PASS' if aok else 'FAIL',checks=checks,input_pins=dict(r.inputs),scope='Offline audit of native count receipt and unchanged runtime reserve; no provider calls. Count is the measured base request, not a guarantee for arbitrary history.'))
print(json.dumps({'foundation':'PASS' if fok else 'FAIL','numeric':'PASS' if nok else 'FAIL','admission':'PASS' if aok else 'FAIL','missing_foundation':[c['pointer'] for s in surfaces.values() for c in s['checks'] if not c['inline_exact']],'failed_admission':[c['name'] for c in checks if not c['passed']]}))
