from review_helpers import *
PARAGRAPHS=["[REAL — tipos e objetos] regularAverage_polar_approximants recebe o mesmo P e δ>0, constrói b_n na álgebra direita existente E, norma≤1 e limites fortes b_n→eδ e b_n*→eδ*. regularAverage_mem_scalarPolarRightAlgebra conclui a pertença de eδ a E. A definição de E inclui as identidades direitas para b e b* em TODO o ideal escalar nν, com o J/GNS originais. A família aproximante exigida no fornecedor de fechamento é construída, não recebida como campo.", "[REAL — partição exata] O helper average_partition traduz cada integral em [0,h] por k h usando a lei de grupo e integral_comp_add_right. sum_integral_adjacent_intervals, com μ=volume explicitado, soma os intervalos adjacentes e fornece b_N e_h=e_(N h), com normalização N⁻¹h⁻¹=(Nh)⁻¹. É uma identidade finita da integral vetorial existente, não uma afirmação assintótica de Riemann. O helper admite N=0 ou h=0 pela convenção de inverso zero; o consumidor usa N=n+1>0 e h=d_n>0.", "[REAL — construção e convergência forte] b_n é a combinação finita (n+1)⁻¹Σ_{k<n+1}λ_(k d_n), d_n=δ/(n+1). Pertence a E por soma e escala dos geradores já existentes. A cota≤1 vem das normas das λ e da cardinalidade da soma. d_n tende a zero no filtro perfurado, pois δ>0. A identidade b_n e_(d_n)=eδ e a cota dão ‖b_n v−eδ v‖≤‖v−e_(d_n)v‖→0. O bound_limit local é um argumento de contração no corpo da prova, não uma quarta declaração privada/global.", "[REAL — adjunto, ponto crítico] average_commutes_regular demonstra comutação da média com cada λ por transporte da integral vetorial e abelianidade da lei regular. Da soma resulta b_n e_(d_n)=e_(d_n)b_n. A prova estrelará e_(d_n)b_n=eδ, e não somente a identidade na ordem anterior: assim obtém b_n* e_(d_n)*=eδ*. Reaplica bound_limit usando ‖b_n*‖≤1 e regularAverage_star_tendsto_identity, já provado para contrações. Não usa continuidade geral de star para SOT e não afirma eδ=eδ*.", "[REAL — fechamento e domínio] O primeiro uso de scalarRightAction_closed_of_bounded_strongStar recebe b_n, as duas convergências e a primeira componente da pertença b_n∈E. O segundo recebe b_n*, com o limite adjunto e star_star, além da segunda componente dessa pertença. Produz a ação para eδ e eδ* em todos A∈nν. A passagem da inscrição GNS é responsabilidade do fornecedor já aceito; não se presume continuidade forte irrestrita de Λ nem se constrói outro GNS.", "[REAL — auxiliares, ficha e histórico] Três helpers privados globais: average_commutes_regular, average_partition e finite_regular_average_norm, auditados transitivamente pelos dois alvos. Nove fornecedores da ficha relidos por linha e pin. O excerto operatorIntegral_commutes está truncado no binder; o tipo completo foi relido, e o adendo explica o adaptador concreto via integral vetorial. A ficha antecede o código; o adendo declara posterioridade ao DEV. Dois DEV rc1 preservados e excluídos: timeouts/coerções/ext/rewrite e depois medida/filtro/metavariáveis. As três versões usam os mesmos limites 2200000/200000; o final rc0 está limpo.", "[REAL — controle] BadAverageMembershipIsSelfAdjoint foi reproduzido em V/ReviewControls com cópia de bytes e objetos próprios. A tentativa de usar pertença em E como prova de eδ*=eδ retorna rc1 por Type mismatch, com imports funcionais. O controle autoral também foi relido/pinado. Essa recusa prova apenas a inadequação do termo adulterado, não uma classificação de todas as médias por auto-adjunção."]
def main():
 p=load(OUT/'SNAPSHOT_POINTER.json');ck(p['snapshot']);a=Path(p['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0
 assert load(a/'preservation.json')['all_unchanged']
 for q in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(q)
 for x in s['sources']:ck(x['original']);ck(x['copy'])
 target=next(x for x in s['sources'] if x['target']);names={x['name'] for x in s['targets']}
 code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
 assert len(names)==2 and len(re.findall(r'^theorem\s+',code,re.M))==2
 assert len(re.findall(r'^private theorem\s+',code,re.M))==3
 assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
 assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
 ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos));assert set(ax)==names
 assert all(set(v)<=ALLOWED for v in ax.values());types={}
 for n in names:
  q=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==n];assert len(q)==1;types[n]=q[0]
 save(a/'type_axiom_audit.json',dict(types=types,axioms=ax,trace=pin(ap),targets=s['targets'],private_helpers_audited_transitively=True))
 authorpath=R/'AUDITORIA_MEDIA_ACAO_DIREITA_A1B.json';author=load(authorpath);pins=[];validate_pin_tree(author,pins)
 assert {x['name'] for x in author['targets']}==names and author['modules'][0]['source']==target['original']
 assert (author['new_theorems'],author['new_definitions'],author['private_theorems'])==(2,0,3)
 assert author['average_polar_right_constructed'] and not author['full_trace_constructed']
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
 for q in sorted((R/'dev_average_polar_right').glob('*/run.json')):
  j=load(q);sp=pin(q.parent/'V351AveragePolarRight.lean')
  assert (sp['sha256'],sp['bytes'])==(j['source']['sha256'],j['source']['bytes'])
  ck(j['stdout']);ck(j['stderr'])
  history.append(dict(run=pin(q),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],used_as_own_build=False,diagnostic=Path(j['stdout']['path']).read_text(encoding='utf8')))
 assert [x['returncode'] for x in history]==[1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
 save(OUT/'history_read.json',dict(rows=history,failed_count=2,failures_excluded=True,historical_locations_not_active_pins=True))
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
 assert len(checks)==9
 ep=V/'TGLExt/V351ScalarRightActionAlgebra.lean';el=ep.read_text(encoding='utf-8-sig').splitlines()
 save(OUT/'provider_checks.json',dict(checks=checks,consumer=dict(source=pin(ep),property_line=14,property_text='\n'.join(el[13:19]),algebra_line=94,algebra_text='\n'.join(el[93:116])),note='operatorIntegral_commutes documentary prefix truncated; full provider read.'))
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
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=3,private_definitions=0,total_source_theorems_including_private=5,
 all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
 all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; two failed author DEV attempts excluded.',
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
 average_polar_right_constructed=True,fixed_tomita_vectors_constructed=False,core_traciality_proved=False,full_trace_constructed=False)
 checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
 limits=['Aceite29: dois teoremas públicos, três helpers privados globais e zero defs; bound_limit é prova local incluída transitivamente.', 'Pertença da média e da sua estrela na álgebra direita original. Não declara auto-adjunção da média, vetor fixo S/F, igualdade dos implementadores, Q ou tracialidade.', '19 V351 são subconjunto das 940 entradas da base (937 Lean e três configurações), não 959 arquivos; pins relidos.', 'Somente esta pasta e novas saídas em V. Fontes K/OLD/V353, memórias, monólito, writers e pareceres anteriores preservados.']
 report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=3,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],
 type_axiom_audit=comp['type_axiom_audit'],semantic_review=PARAGRAPHS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],
 all_prior_pins_preserved=True,average_polar_right_constructed=True,fixed_tomita_vectors_constructed=False,average_selfadjoint_claimed=False,core_traciality_proved=False,trace_constructed=False,gate_modified=False)
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

