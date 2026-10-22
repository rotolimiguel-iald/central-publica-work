from review_helpers import *
PARAGRAPHS=['[REAL — tipos] Dois teoremas públicos, um helper privado phase_at_half, zero definições. scalarTomitaImaginaryPower_fixed_of_fixed_pair recebe x no MESMO H_I, pertinência aos domínios originais D(S)/D(F) e as duas igualdades Sx=x/Fx=x. Conclui U_t x=x para qualquer t, usando scalarTomitaImaginaryPower já existente. regularAverage_square_modular_fixed consome delta30 e constrói UM A com valor exato star(eδ)*eδ e invariância para TODO t, δ>0. Não troca o vetor quando t varia.', '[REAL — domínio e resolvente] scalarTomitaSquare_domain_iff exige x∈D(S) e Sx∈D(F). A segunda pertença é transportada de hF usando Sx=x. A aplicação da composição FS é identificada por Subtype.ext entre o argumento Sx e x em D(F), logo Delta_nu x=x. Só então scalarTomitaResolvent_inverse fornece T_nu(x+x)=x; linearidade e escala complexa dão T_nu x=(1/2)x. Não se trata domínio total de Delta nem igualdade de operadores não limitados sem domínio.', '[REAL — adaptador privado e zero] phase_at_half é genérico em Hilbert completo, T auto-adjunto e Tx=(1/2)x; não recebe a conclusão C_t x=(1/4)x. Primeiro separa x=0, resolvido por linearidade. Para x≠0 usa L=InnerProductSpace.rankOne ℂ x x e Q=algebraMap ℂ B(H) (1/2). A igualdade TL=LQ usa Tx=(1/2)x, a linearidade do produto interno na segunda variável e comutatividade dos escalares; não requer normalizar x nem tornar L uma projeção.', '[REAL — fase e cancelamento] Q é auto-adjunto por algebraMap_star_comm. cfc_algebraMap avalia exatamente g_t(1/2)=(1/4)exp(i t log1)=1/4, para TODO t, nas definições já existentes. resolventPhaseOperator_intertwines transporta TL=LQ para C_t(T)L=L C_t(Q). Após avaliar em x, cancela somente inner(x,x)≠0, provado de x≠0 por inner_self_ne_zero. Não cancela um vetor arbitrário nem pressupõe cota espectral inferior de T.', '[REAL — mesmo U] O cálculo direto de T(1−T)x dá (1/4)x. A identidade scalarTomitaImaginaryPower_damping produz U_t((1/4)x)=(1/4)x. O cancelamento final usa apenas o escalar complexo 1/4≠0. U é a potência imaginária do resolvente original, não grupo de Q redefinido como identidade, não implementação esquerda regular e não conjugação gaussiana. Não foi criado CFC, grupo, gerador, GNS ou peso.', '[REAL — concretização e limites] O segundo alvo obtém de regularAverage_square_fixed_pair o A∈scalarWeightStarCore, sua igualdade com eδ*eδ e ambos os valores/domínios S/F. Descarrega todas as hipóteses do primeiro. Não afirma eδ auto-adjunto, norma unitária do vetor, vetor individual cíclico, família totalizante, U=πλR_-t, compatibilidade Q ou tracialidade. O consumidor indicado na ficha é etapa posterior, não hipótese silenciosa.', '[REAL — ficha, errata e história] Oito fornecedores da ficha e dois do adendo relidos por linhas/pins; cópias Mathlib de K e V conferidas em bytes. A consulta anterior deste revisor indicou incorretamente ContinuousLinearMap.rankOne: a fonte define InnerProductSpace.rankOne/rankOne_apply. O adendo corrige AO LADO, depois do DEV e antes do aceite; também registra algebraMap_star_comm, nome efetivamente usado. Quatro DEV medidos: três rc1 por nomes/reescritas e final010047 rc0 limpo. maxHeartbeats1600000 não aumentado. Stdout DEV final vazio; trio lido dos auditores.', '[REAL — controle e independência] BadModularFixedAdjointEqualityRemoved elimina a igualdade Fx=x e tenta usar o teorema ainda parcialmente aplicado. Controle próprio e autoral: rc1 por Type mismatch, imports válidos. Isso recusa a aplicação adulterada, não prova impossibilidade universal com outros argumentos. Herda somente objetos de projeto previamente construídos pelo nosso Lake e pacotes pinados; nenhum objeto K/DEV. A ressalva de autoria histórica dos auxiliares antiunitários permanece a dos40, já inspecionados pelo principal.']
def main():
 p=load(OUT/'SNAPSHOT_POINTER.json');ck(p['snapshot']);a=Path(p['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0
 assert load(a/'preservation.json')['all_unchanged']
 for q in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(q)
 for x in s['sources']:ck(x['original']);ck(x['copy'])
 target=next(x for x in s['sources'] if x['target']);names={x['name'] for x in s['targets']}
 code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
 assert len(names)==2 and len(re.findall(r'^theorem\s+',code,re.M))==2
 assert len(re.findall(r'^private theorem\s+',code,re.M))==1
 assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
 assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
 ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos));assert set(ax)==names
 assert all(set(v)<=ALLOWED for v in ax.values());types={}
 for n in names:
  q=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==n];assert len(q)==1;types[n]=q[0]
 save(a/'type_axiom_audit.json',dict(types=types,axioms=ax,trace=pin(ap),targets=s['targets'],private_helpers_audited_transitively=True))
 authorpath=R/'AUDITORIA_VETORES_FIXOS_MODULARES_A1B.json';author=load(authorpath);pins=[];validate_pin_tree(author,pins)
 assert {x['name'] for x in author['targets']}==names and author['modules'][0]['source']==target['original']
 assert (author['new_theorems'],author['new_definitions'],author['private_theorems'])==(2,0,1)
 assert author['modular_fixed_vectors_constructed'] and not author['full_trace_constructed']
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
 for q in sorted((R/'dev_modular_fixed_vectors').glob('*/run.json')):
  j=load(q);sp=pin(q.parent/'V351ModularFixedVectors.lean')
  assert (sp['sha256'],sp['bytes'])==(j['source']['sha256'],j['source']['bytes'])
  ck(j['stdout']);ck(j['stderr'])
  history.append(dict(run=pin(q),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],used_as_own_build=False,diagnostic=Path(j['stdout']['path']).read_text(encoding='utf8')))
 assert [x['returncode'] for x in history]==[1,1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
 save(OUT/'history_read.json',dict(rows=history,failed_count=3,failures_excluded=True,historical_locations_not_active_pins=True))
 dp=[];checks=[]
 for doc in s['documents']:
  if not doc['path'].endswith('.json'):continue
  jd=load(Path(doc['path']));validate_pin_tree(jd,dp)
  for pr in jd.get('providers',[])+jd.get('extra_providers',[]):
   fp=Path(pr['source']['path']);ck(pr['source']);ls=fp.read_text(encoding='utf8').splitlines();stmt=pr.get('statement',pr.get('excerpt'))
   assert stmt
   actual='\n'.join(ls[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
   assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr.get('name',pr['statement'].split(' :',1)[0])
   op=V/fp.relative_to(K);assert op.read_bytes()==fp.read_bytes()
   checks.append(dict(name=pr.get('name',pr['statement'].split(' :',1)[0]),line=pr['line'],statement=stmt,source_excerpt='\n'.join(ls[pr['line']-1:pr['line']+15]),author=pin(fp),own=pin(op)))
 assert len(checks)==10
 cj=load(R/'REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES.json')['consumer'];cl=Path(cj['source']['path']).read_text(encoding='utf8').splitlines()
 assert '\n'.join(cl[cj['line']-1:]).startswith(cj['statement'])
 save(OUT/'provider_checks.json',dict(checks=checks,consumer=dict(**cj,source_excerpt='\n'.join(cl[cj['line']-1:cj['line']+12])),consumer_status='IMPLEMENTATOR_EQUALITY_STILL_OPEN'))
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
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=1,private_definitions=0,total_source_theorems_including_private=3,
 all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
 all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; three failed author DEV attempts excluded; only final whole-file rc0 accepted.',
 all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,
 own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_cache_not_rebuilt=True,
 package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
 own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
 newly_recompiled_old_supplier_count=0,newly_recompiled_old_suppliers=[],objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
 type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,
 lake_stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8'),built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,
 baseline_preservation=pin(OUT/'preservation_19_940.json'),original_v351_count=19,baseline_files_count=940,baseline_lean_count=937,baseline_config_count=3,nineteen_subset_of_baseline=True,
 fiche_provider_pins=dp,provider_checks=pin(OUT/'provider_checks.json'),history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
 helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py','negative_control.py','auxiliary_helpers_provenance.json']],
 modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=False,core_traciality_proved=False,full_trace_constructed=False)
 checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
 limits=['Aceite31: dois teoremas públicos e um helper privado auditado transitivamente; zero definições. Nenhum fornecedor antigo recompilado nesta rodada.', 'Mesmo U fixa as inscrições dos quadrados eδ*eδ, δ>0. Totalidade/ciclicidade, U=πλR_-t, Q e tracialidade não são afirmadas.', '19 V351 são subconjunto das 940 entradas da base, não959. Preservação relida em bytes.', 'Somente esta pasta e novas saídas em V foram escritas; K/OLD/V353, memórias, monólito, writers e predecessores preservados.']
 report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=1,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],
 type_axiom_audit=comp['type_axiom_audit'],semantic_review=PARAGRAPHS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],
 all_prior_pins_preserved=True,modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=False,average_selfadjoint_claimed=False,core_traciality_proved=False,trace_constructed=False,gate_modified=False)
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

