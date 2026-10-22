from review_helpers import *
PARAGRAPHS=["[REAL — contrações incondicionais] O primeiro teorema recebe somente P. Constrói E_n=e_n q_n, com δ_n=1/(n+1)>0, média regular e_n e corte de domínio q_n antigos. Normas≤1 dão a contração; e_n∈nν e domainCut_finite do delta26 dão τ(E_n*E_n)<∞. bounded_application_tendsto combina q_n v→v e e_n v→v. Não exige tracialidade nem afirma que E_n seja positivo, projeção, crescente ou convergente em norma de operadores.","[REAL — hipótese explícita] O segundo teorema recebe htr : ∀a∈N, τ(a*a)=τ(aa*) e X : PositiveCoreInput P. Prova exatamente o campo de minorantes positivos finitos para o MESMO τ, condicionado a htr. Não fornece esse antecedente, não impõe tal propriedade ao peso dual não tracial ν e não constrói um habitante de RegularCoreTraceData.","[REAL — raiz e ordem] O auxiliar hilbert_core_square_source usa CFC.sqrt ambiental já existente, cfcₙ_mem e fechamento normado de N para obter a∈N com a*a=X. Não instala CompleteSpace no subtipo N nem cria outra raiz. Y_n=(E_n a)*(E_n a)≤X decorre de E_n*E_n≤I por conjugação positiva. Não comuta a com E_n ou com os reguladores; não usa ordem falsa dos conjugadores.","[REAL — usos de htr] Primeiro htr(E_n a) troca τ(Y_n) por τ((E_n a)(E_n a)*). A cota (E_n a)(E_n a)*≤‖a‖²E_n E_n* vem de a a*≤‖a‖²I. Monotonicidade e homogeneidade dão o bound; htr(E_n) troca τ(E_n E_n*) pelo valor finito τ(E_n*E_n). O escalar NNReal ‖a‖² é finito. Esses dois usos são explícitos, sem conversão de infinito para real ou finitude presumida de τ(X).","[REAL — passagem ao limite] E_n a→a fortemente. O bound sequencial de quadrados do delta27, com C o supremo de todos os minorantes finitos de X, dá τ(X)≤C porque cada Y_n participa dele. Não se exige que Y_n cresça, nem convergência dos adjuntos ou finitude de C. O sentido contrário é monotonicidade. A prova cobre τ(X)=∞.","[REAL — auxiliares e histórico] Quatro helpers privados genéricos: hilbert_square_norm_bound, hilbert_compressed_square_bound, hilbert_smul_one_le_one e hilbert_core_square_source. Auditados transitivamente pelos dois alvos. As 11 entradas da ficha e três do adendo foram conferidas por fonte/linha/pin; a ficha precede o código, o adendo declara posterioridade ao DEV e os adaptadores de instâncias. Quatro DEV rc1 por síntese de instâncias/coerções/rewrites foram preservados e excluídos. Pins históricos apontam os snapshots reais.","[REAL — controle próprio] BadFiniteMinorantsTraceRemoved foi copiado em bytes para V/ReviewControls e reproduzido após o Lake positivo. Retornou rc1 por Type mismatch ao omitir htr; imports funcionaram, sem erro de ambiente ou timeout. O controle autoral também foi relido e pinado. A recusa não demonstra impossibilidade de provar htr futuramente."]
def main():
 p=load(OUT/'SNAPSHOT_POINTER.json');ck(p['snapshot']);a=Path(p['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0
 assert load(a/'preservation.json')['all_unchanged']
 for q in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(q)
 for x in s['sources']:ck(x['original']);ck(x['copy'])
 target=next(x for x in s['sources'] if x['target']);names={x['name'] for x in s['targets']}
 code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
 assert len(names)==2 and len(re.findall(r'^theorem\s+',code,re.M))==2
 assert len(re.findall(r'^private theorem\s+',code,re.M))==4
 assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
 assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
 ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos));assert set(ax)==names
 assert all(set(v)<=ALLOWED for v in ax.values());types={}
 for n in names:
  q=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==n];assert len(q)==1;types[n]=q[0]
 save(a/'type_axiom_audit.json',dict(types=types,axioms=ax,trace=pin(ap),targets=s['targets'],private_helpers_audited_transitively=True))
 authorpath=R/'AUDITORIA_MINORANTES_FINITOS_A1B.json';author=load(authorpath);pins=[];validate_pin_tree(author,pins)
 assert {x['name'] for x in author['targets']}==names and author['modules'][0]['source']==target['original']
 assert (author['new_theorems'],author['new_definitions'],author['private_theorems'])==(2,0,4)
 assert author['finite_minorants_conditional_on_traciality'] and not author['full_trace_constructed']
 br=load(Path(author['positive_build']['path']));validate_pin_tree(br,pins);assert br['returncode']==0 and br['sources_unchanged_during_build']
 rows=[]
 for i,row in enumerate(author['commands']):
  txt=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
  if i==0:
   aa=parse_axioms(txt);assert row['returncode']==0 and set(aa)==names and all(set(v)<=ALLOWED for v in aa.values())
  else:
   assert row['returncode']==1 and 'type mismatch' in txt.lower()
   assert not any(w in txt.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
  rows.append(dict(**row,source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stream_text=txt))
 ownneg=load(OUT/'negative_control_own.json');validate_pin_tree(ownneg,pins)
 nt=Path(ownneg['stdout']['path']).read_text(encoding='utf8')
 assert ownneg['returncode']==1 and 'type mismatch' in nt.lower() and ownneg['own_execution']
 assert not any(w in nt.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
 assert ownneg['source']==rows[1]['source']
 negative=dict(status='OWN_AND_AUTHOR_REJECTED_TYPE_MISMATCH',own_execution=True,own=ownneg,author_audit=pin(authorpath),author_rows=rows,author_pins=pins)
 save(OUT/'negative_controls_read.json',negative)
 history=[]
 for q in sorted((R/'dev_finite_minorants').glob('*/run.json')):
  j=load(q);sp=pin(q.parent/'V351InverseLimitFiniteMinorants.lean')
  assert (sp['sha256'],sp['bytes'])==(j['source']['sha256'],j['source']['bytes'])
  ck(j['stdout']);ck(j['stderr'])
  history.append(dict(run=pin(q),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],used_as_own_build=False,diagnostic=Path(j['stdout']['path']).read_text(encoding='utf8')))
 assert [x['returncode'] for x in history]==[1,1,1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
 save(OUT/'history_read.json',dict(rows=history,failed_count=4,failures_excluded=True,historical_locations_not_active_pins=True))
 dp=[];checks=[]
 for doc in s['documents']:
  if not doc['path'].endswith('.json'):continue
  jd=load(Path(doc['path']));validate_pin_tree(jd,dp)
  for pr in jd.get('providers',[]):
   fp=Path(pr['source']['path']);ck(pr['source']);ls=fp.read_text(encoding='utf8').splitlines();stmt=pr.get('statement',pr.get('excerpt'))
   assert stmt
   actual='\n'.join(ls[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
   assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr['name']
   op=V/fp.relative_to(K);assert op.read_bytes()==fp.read_bytes()
   checks.append(dict(name=pr['name'],line=pr['line'],statement=stmt,source_excerpt='\n'.join(ls[pr['line']-1:pr['line']+15]),author=pin(fp),own=pin(op)))
 assert len(checks)==14
 cp=V/'TGLExt/V351RegularCoreTraceContract.lean';ls=cp.read_text(encoding='utf8').splitlines();ci=next(i for i,l in enumerate(ls) if l.startswith('  semifinite :'))
 save(OUT/'provider_checks.json',dict(checks=checks,consumer=dict(source=pin(cp),line=ci+1,statement='\n'.join(ls[ci:ci+3]))))
 base=load(OUT/'preservation_19_940.json');validate_pin_tree(base,[])
 assert base['all_matched'] and base['baseline_file_count']==940 and len(base['original_v351'])==19
 assert not [x for x in s['sources'] if not x['target'] and not x['source_preexisting']]
 inherited={x['path'] for x in s['protected'] if x['path'].endswith('.olean')};objects=[];tw=[];sw=[]
 for q in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
  mod=str(q.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
  tr,tj,mi=trace(mod);row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(q),trace=pin(tr),own_previously_compiled=str(q) in inherited)
  if mod in s['modules']:
   aq=K/'.lake/build/lib/lean'/q.relative_to(V/'.lake/build/lib/lean');row['author_cold']=pin(aq);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
  for msg in tj['log']:
   if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
  objects.append(row)
 assert not tw
 new=[x for x in objects if not x['own_previously_compiled']]
 assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
 stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
 assert set(built)==set(s['modules']+[s['auditor_module']])
 comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=4,private_definitions=0,total_source_theorems_including_private=6,
 all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
 all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; four failed author DEV attempts excluded.',
 all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,
 own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_cache_not_rebuilt=True,
 package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
 own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
 newly_recompiled_old_supplier_count=0,newly_recompiled_old_suppliers=[],objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
 type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,
 lake_stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8'),built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,
 baseline_preservation=pin(OUT/'preservation_19_940.json'),original_v351_count=19,baseline_files_count=940,baseline_lean_count=937,baseline_config_count=3,nineteen_subset_of_baseline=True,
 fiche_provider_pins=dp,provider_checks=pin(OUT/'provider_checks.json'),history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
 helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']],
 finite_contractions_constructed=True,finite_minorants_conditional_on_traciality=True,core_traciality_proved=False,full_trace_constructed=False)
 checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
 limits=['Aceite dos dois tipos, quatro helpers transitivos e zero defs. Contrações finitas incondicionais; minorantes finitos condicionados a htr.',
 'Nenhum contrato habitado, nenhuma prova tracial global ou no núcleo. A1(b) continua aberto.',
 '19 V351 são subconjunto das 940 entradas da base (937 Lean e três configurações), não 959 arquivos.',
 'Apenas novas saídas em V e nesta revisão. Fontes autorais, originais, V353, memórias, monólito, writers e pareceres anteriores preservados.']
 report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=4,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],
 type_axiom_audit=comp['type_axiom_audit'],semantic_review=PARAGRAPHS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],
 all_prior_pins_preserved=True,finite_contractions_constructed=True,finite_minorants_conditional_on_traciality=True,unconditional_finite_minorants_proved=False,core_traciality_proved=False,trace_constructed=False,gate_modified=False)
 validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
 obj=next(x for x in objects if x['module'] in s['modules'])
 md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Módulo e auditor próprios rc0; dois tipos completos com universos, axiomas do trio. Controle negativo próprio rc1 por Type mismatch.\n\n'+'\n\n'.join(PARAGRAPHS)
 md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios preservados; '+str(len(new))+' novos (alvo+auditor), total '+str(len(objects))+'. Nenhum fornecedor antigo recompilado, nenhum objeto K/DEV herdado. Run '+str(round(run['elapsed_seconds'],3))+' s; negativo '+str(round(ownneg['elapsed_seconds'],3))+' s. Zero avisos do alvo/auditor; '+str(len(sw))+' mensagens de fornecedores herdadas discriminadas. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui o negativo esperado. LEAN_PATH dos traces restrito a V/pacotes.\n\n'
 md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte K=snapshot=V | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral, só comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n'
 md+='[OPEN] '+' '.join(limits)+'\n\nTipos lidos:\n\n'
 for t in author['targets']:
  md+='~~~lean\n'+t['statement']+'\n~~~\n\nAxiomas próprios: '+', '.join(ax[t['name']])+'.\n\n'
 md+='Evidências:\n\n'
 for label,pin0 in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('negativo próprio',ownneg['run']),('preservação19/940',comp['baseline_preservation']),('histórico',comp['history'])]:
  md+='- ['+label+'](<'+pin0['path']+'>) — SHA256 '+pin0['sha256']+'.\n'
 fresh(OUT/(NAME+'.md'),md.encode())
 save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
 print(json.dumps(dict(status=STATUS,report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],P0=[],P1=[],P2=[],objects_before=len(inherited),objects_after=len(objects),binary_equal=obj['equal_author_cold'],negative_rc=ownneg['returncode']),ensure_ascii=False))
if __name__=='__main__':main()

