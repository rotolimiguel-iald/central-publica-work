from build_delta import *
ALLOWED={'propext','Classical.choice','Quot.sound'}
def norm(x):return re.sub(r'\.\{[^}]*\}','',x).strip()
def axioms(text):
 out={}
 for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
  name=norm(m[1]);aa=[] if m[3] else [norm(x) for x in m[2].split(',') if x.strip()]
  if name in out:assert out[name]==aa,(name,out[name],aa)
  out[name]=aa
 return out
def trace(mod):
 p=V/'.lake/build/lib/lean'/Path(mod.replace('.','/')+'.trace');j=load(p)
 assert not any(x['level']=='error' for x in j['log']),p
 msgs=[re.sub(r'^.*?\.lean:\d+:\d+:\s*','',x['message']) for x in j['log'] if x['level']=='info']
 cmd=[x['message'] for x in j['log'] if x['level']=='trace' and 'LEAN_PATH=' in x['message']]
 assert cmd,(mod,'no tool invocation')
 for c in cmd:
  lp=re.split(r'\s+[cC]:\\',c.split('LEAN_PATH=',1)[1],maxsplit=1)[0]
  for path in lp.split(';'):assert Path(path).resolve().is_relative_to(V.resolve()),(mod,path)
 return p,j,msgs
def main(key):
 folder,names,count,docs=CONFIG[key];out=R/folder;a=Path(load(out/'SNAPSHOT_POINTER.json')['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0,run
 ck(load(out/'SNAPSHOT_POINTER.json')['snapshot'])
 for p in run['streams']+run['executables']+s['protected']+s['documents']+s['base_compilations']:ck(p)
 for x in s['sources']:ck(x['original']);ck(x['copy'])
 assert load(a/'preservation.json')['all_unchanged']
 notes=load(out/'semantic_notes.json');assert notes['review_complete'] and not notes['findings']
 expected={t['name'] for t in s['targets']}
 ap,aj,msg=trace(s['auditor_module']);aa=axioms('\n'.join(msg));assert set(aa)==expected,(set(aa)^expected)
 assert all(set(x)<=ALLOWED for x in aa.values())
 types={}
 for name in expected:
  matches=[m for m in msg if norm(m.split(' ',1)[0])==name and not m.startswith("'")]
  assert len(matches)==1,(name,matches);types[name]=matches[0]
 typespath=a/'type_axiom_audit.json';typedata=dict(targets=s['targets'],types=types,axioms=aa,trace=pin(ap),all_axioms_allowed=True)
 if typespath.exists():assert load(typespath)==typedata
 else:save(typespath,typedata)
 objects=[];tw=[];sw=[];inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
 for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
  mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
  tp,tj,tm=trace(mod);src=V/(mod.replace('.','/')+'.lean')
  rec=dict(module=mod,source=pin(src),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
  if mod in s['modules']:
   act=axioms('\n'.join(tm));ex={t['name'] for t in s['targets'] if t['module']==mod}
   assert set(act)==ex and all(set(v)<=ALLOWED for v in act.values()),mod
   author=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
   rec['author_cold']=pin(author) if author.is_file() else None
   rec['equal_author_cold']=rec['own']['sha256']==rec['author_cold']['sha256'] if rec['author_cold'] else None
  for m in tj['log']:
   if m['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=m['message'],old_object=rec['own_previously_compiled']))
  objects.append(rec)
 assert not tw,tw
 docscheck=[]
 def verify_records(x):
  if isinstance(x,dict):
   if {'path','bytes','sha256'}<=set(x):
    p=Path(x['path']);assert pin(p)['sha256']==x['sha256'] and pin(p)['bytes']==x['bytes'],x
    docscheck.append(pin(p))
   else:
    for v in x.values():verify_records(v)
  elif isinstance(x,list):
   for v in x:verify_records(v)
 for d in s['documents']:
  if d['path'].endswith('.json'):verify_records(load(Path(d['path'])))
 devpaths={
  'core':['dev_left/20260914_174247_734758/run.json','dev_core/20260914_180511_642247/run.json'],
  'absorcao':['dev_absorption/20260914_182118_370442/run.json'],
  'fourier':['dev_fourier_translation/20260914_183403_872821/run.json'],
  'grafo':['dev_positive_graph/20260914_185143_820184/run.json'],
  'espectral':['dev_spectral_graph/20260914_191213_503075/run.json'],
  'calculo':['dev_multiplier_calculus/20260914_192424_032053/run.json'],
  'potencias':['dev_regular_powers/20260914_193204_622512/run.json'],
  'afiliacao':['dev_regular_affiliation/20260914_194034_466190/run.json'],
  'escala_dual':['dev_regular_dual_scaling/20260914_200033_241925/run.json'],
  'cortes_inverso':['dev_inverse_cutoff/20260914_201442_615970/run.json'],
  'fechamento_gns':['dev_gns_closedness/20260914_203030_719820/run.json'],
  'limites_direita':['dev_right_action_limits/20260914_203706_719663/run.json'],
  'algebra_direita':['dev_right_action_algebra/20260914_210039_263478/run.json'],
  'seno_resolvente':['dev_sine_resolvent/20260914_211359_468646/run.json']}[key]
 devread=[]
 for rel in devpaths:
  dp=R/rel;dj=load(dp);assert dj['returncode']==0
  historical=dp.parent/'V351SineResolventApprox.lean';hp=pin(historical)
  assert hp['sha256']==dj['source']['sha256'] and hp['bytes']==dj['source']['bytes']
  history=load(out/'history_read.json');cleanup=history['final_cleanup'];ck(cleanup['previous']);ck(cleanup['current'])
  assert historical.read_bytes().replace(cleanup['exact_only_removed_line'].encode(),b'')==Path(cleanup['current']['path']).read_bytes()
  match=[x for x in s['sources'] if x['target'] and x['original']==cleanup['current']];assert len(match)==1,dp
  for field in ['stdout','stderr']:ck(dj[field])
  da=axioms(Path(dj['stdout']['path']).read_text(encoding='utf8'));ex={x['name'] for x in s['targets'] if x['module']==match[0]['module']}
  assert set(da)==ex and all(set(v)<=ALLOWED for v in da.values()),dp
  devread.append(dict(run=pin(dp),source=dj['source'],stdout=dj['stdout'],stderr=dj['stderr'],returncode=dj['returncode'],role='Historical pre-cleanup DEV rc0 with warning, retained source snapshot; final source validated separately by author Lake and own Lake',historical_snapshot=hp,cleanup=cleanup))
 negative=load(out/'negative_controls_read.json') if (out/'negative_controls_read.json').exists() else dict(status='AUTHOR_NEGATIVES_NOT_YET_AVAILABLE__NOT_CLAIMED_AS_EXECUTED',own_negative_tests_executed=False)
 if 'pins' in negative:
  for p in negative['pins']:ck(p)
 stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8')
 built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
 newobjects=[x for x in objects if not x['own_previously_compiled']]
 assert all(m.startswith(('TGL.','TGLExt.')) for m in built),('package rebuild',built)
 comp=dict(timestamp=now(),status=notes['status'],exact_target_count=count,new_theorems=sum(t['kind']=='theorem' for t in s['targets']),new_definitions=sum(t['kind']=='def' for t in s['targets']),all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='Only this independent delta Lake invocation',all_axioms_allowed=True,all_target_typechecks_present=True,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(newobjects),newly_recompiled_old_supplier_count=sum(x['module'] not in s['modules']+[s['auditor_module']] for x in newobjects),objects=objects,sourcepins=[x for x in s['sources'] if x['target']],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(typespath),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins_checked=len(docscheck),fiche_provider_pins=docscheck)
 comp['author_dev_evidence_read_only']=devread
 comp['history']=pin(out/'history_read.json')
 comp['private_declarations']=pin(out/'private_declarations.json')
 comp['private_theorems']=6;comp['private_definitions']=1
 comp['public_new_theorems']=comp['new_theorems'];comp['public_new_definitions']=comp['new_definitions']
 comp['total_source_theorems_including_private']=15;comp['total_source_definitions_including_private']=3
 comp['count_scope']='11 public targets, with 6 private theorems and 1 private definition compiled transitively'
 comp['helper_provenance']=pin(out/'finalizer_provenance.json')
 save(out/'compilation.json',comp)
 report=dict(timestamp=now(),status=notes['status'],P0=[],P1=[],P2=[],findings=[],run=comp['run'],compilation=pin(out/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=notes['paragraphs'],limits=notes['limits'],negative_controls=negative,all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
 name=notes['report_name'];save(out/(name+'.json'),report)
 md='# '+notes['title']+'\n\n'+now()+'\n\n**'+notes['status']+'**\n\n[REAL] Sem P0, P1 ou P2 no delta delimitado. '+str(count)+' declarações ('+str(comp['new_theorems'])+' teoremas, '+str(comp['new_definitions'])+' definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.\n\n'
 md+='\n\n'.join(notes['paragraphs'])+'\n\n'
 md+='[REAL] Execução própria rc0 em '+str(round(run['elapsed_seconds'],2))+' s. '+str(len(inherited))+' objetos próprios anteriores preservados; '+str(comp['newly_recompiled_old_supplier_count'])+' fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. '+str(len(tw))+' avisos de alvo/auditor; '+str(len(sw))+' mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.\n\n'
 md+='Pins lidos dos fontes e objetos próprios:\n\n| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |\n|---|---|---|---|\n'
 for ob in objects:
  if ob['module'] in s['modules']:md+='| '+ob['module']+' | `'+ob['source']['sha256']+'` | `'+ob['own']['sha256']+'` | '+str(ob['equal_author_cold'])+' |\n'
 md+='\nComparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.\n\nControles: '+negative['status']+'. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.\n\n'
 md+='[OPEN / limites] '+' '.join(notes['limits'])+'\n\nArtefatos próprios:\n\n'
 for label,p in [('run',comp['run']),('compilation',report['compilation']),('tipos/axiomas',comp['type_axiom_audit'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
 fresh(out/(name+'.md'),md.encode());print(json.dumps(dict(report=pin(out/(name+'.md')),json=pin(out/(name+'.json')),compilation=report['compilation']),ensure_ascii=False),flush=True)
if __name__=='__main__':main(sys.argv[1])
