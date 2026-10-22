from review_helpers import *
PARAGRAPHS=['[REAL — tipos] Um teorema público, zero privados e zero definições. scalarTomitaImaginaryPower_eq_regular_implementation recebe somente P:SiteProfile, t:ℝ e x:ScalarGNSHilbert P. Conclui a igualdade do U original com π(λ_t) regularRightGNS(-t), em TODO vetor. Não recebe igualdade de grupos, totalidade, vetor cíclico, tracialidade ou identidade de produtos ilimitados como hipótese. As estruturas anteriores do mesmo P permanecem as mesmas.', '[REAL — família fixa] d_n=1/(n+1)>0 e e_n=regularAverage(P,d_n). choose Z hZ hU aplica o fornecedor regularAverage_square_modular_fixed a n apenas: Z_n e sua igualdade ambiente exata e_n*e_n são escolhidos antes da especialização hU n t; uma única família serve a todos os tempos. Z_n é auto-adjunto e pertence a scalarPolarRightAlgebra por star/mul dos elementos e_n já pagos. Não declara e_n auto-adjunto.', '[REAL — sinal e W] StrongIntegral.operatorIntegral_commutes e a lei abeliana de λ provam comutação de λ_s com eδ. Estrelar a igualdade em -t dá comutação com eδ*, daí com Z_n. W é apenas let local do operador limitado π(λ_t)R_-t. As identidades direita/esquerda originais dão WΛZ_n=Λ(λ_t Z_n λ_-t)=ΛZ_n. O sinal negativo vem da inversa efetiva λ_-t=λ_t*, não de troca de J linear por antilinear.', '[REAL — concordância] A covariância all-core anterior e hU n t calculam U_tπ(a)ΛZ_n. Para W, regularRightGNS_commutes_left vale para TODO a do core, e a unitariedade de πλ_t junto de WΛZ_n=ΛZ_n fornece a mesma expressão π(λ_t a λ_t*)ΛZ_n. Não se infere unicidade do implementador apenas de covariância; a concordância é demonstrada nesta família específica.', '[REAL — totalidade demonstrada] A cota ||Z_n||≤1 vem das contrações e_n. bounded_application_tendsto usa simultaneamente e_n v→v e e_n* v→v, para obter Z_n v→v; não assume continuidade forte geral da estrela. A continuidade forte limitada da MESMA π transporta Z_n→I ao H_I. Conjugação pelo J original contínuo, com Z_n*=Z_n, dá ρ(Z_n)→I fortemente. Para cada a∈nν, a identidade direita de E e o entrelaçamento esquerdo produzem π(a)ΛZ_n=ρ(Z_n)Λa→Λa. A densidade do Λ original e continuidade dos dois operadores completam a igualdade em TODO H_I. Não se pressupõe que qualquer ΛZ_n isolado seja cíclico.', '[REAL — fornecedores e ficha] Doze entradas da ficha e a assinatura integral corrigida do adendo foram confrontadas por linhas/bytes com fontes e cópias V. A ficha histórica truncou operatorIntegral_commutes dentro de (H := H); o adendo posterior ao DEV e anterior ao aceite registra o tipo completo. A anterioridade da leitura integral é declarada pelo autor; nesta revisão a leitura integral foi refeita diretamente e o tipo compila. A correção documental não cria uma hipótese ou novo fornecedor matemático. O replay antigo V350ScalarRegularPolarCommutation foi necessário também no V: um módulo com quatro declarações antigas, contado separadamente do novo alvo.', '[REAL — história e controle] Quatro DEV preservados: três rc1 excluídos (objeto antigo ausente, erros de composição/coerção, timeout de reescritas) e o final011125 rc0 sem avisos. maxHeartbeats2200000 e synthInstance200000 permanecem; o stdout DEV final vazio não foi tratado como auditoria de axiomas. Os auditores completos próprio/autoral fornecem o trio. BadModularImplementationRightSignChanged troca R_-t por R_t: as execuções própria e autoral recusam a aplicação por Type mismatch com imports válidos. Isso não é prova de impossibilidade por qualquer outro argumento.', '[REAL — independência e limites] Somente fontes do alvo e do fornecedor antigo ausente foram copiadas; o Lake próprio usa objetos anteriores produzidos no V e caches de pacotes pinados. Nenhum objeto K/DEV foi herdado. A ressalva histórica de autoria dos dois módulos antiunitários continua a dos40, inspecionados pelo principal; não é reclassificada aqui. Esta igualdade de implementadores está paga no escopo formal. Q, compatibilidade de meias potências/domínios, tracialidade do scalarInverseLimitWeight e contrato de traço continuam OPEN; nenhum gate, memória, monólito ou recibo foi alterado.']

def main():
 p=load(OUT/'SNAPSHOT_POINTER.json');ck(p['snapshot']);a=Path(p['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0
 assert load(a/'preservation.json')['all_unchanged']
 for q in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(q)
 for x in s['sources']:ck(x['original']);ck(x['copy'])
 target=next(x for x in s['sources'] if x['target']);names={x['name'] for x in s['targets']}
 code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
 assert len(names)==1 and len(re.findall(r'^theorem\s+',code,re.M))==1
 assert len(re.findall(r'^private theorem\s+',code,re.M))==0
 assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
 assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
 ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos));assert set(ax)==names
 assert all(set(v)<=ALLOWED for v in ax.values());types={}
 for n in names:
  q=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==n];assert len(q)==1;types[n]=q[0]
 save(a/'type_axiom_audit.json',dict(types=types,axioms=ax,trace=pin(ap),targets=s['targets'],private_helpers_audited_transitively=True))
 authorpath=R/'AUDITORIA_IMPLEMENTADOR_MODULAR_A1B.json';author=load(authorpath);pins=[];validate_pin_tree(author,pins)
 assert {x['name'] for x in author['targets']}==names and author['modules'][0]['source']==target['original']
 assert (author['new_theorems'],author['new_definitions'],author['private_theorems'])==(1,0,0)
 assert author['implementator_equality_proved'] and not author['full_trace_constructed']
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
 for q in sorted((R/'dev_modular_implementation').glob('*/run.json')):
  j=load(q);sp=pin(q.parent/'V351ModularImplementation.lean')
  assert (sp['sha256'],sp['bytes'])==(j['source']['sha256'],j['source']['bytes'])
  ck(j['stdout']);ck(j['stderr'])
  hist_code=uncomment((q.parent/'V351ModularImplementation.lean').read_text(encoding='utf8'))
  assert re.findall(r'set_option maxHeartbeats (\d+)',hist_code)==['2200000']
  assert re.findall(r'set_option synthInstance.maxHeartbeats (\d+)',hist_code)==['200000']
  history.append(dict(run=pin(q),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],used_as_own_build=False,diagnostic=Path(j['stdout']['path']).read_text(encoding='utf8')))
 assert [x['returncode'] for x in history]==[1,1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
 save(OUT/'history_read.json',dict(rows=history,failed_count=3,failures_excluded=True,historical_locations_not_active_pins=True))
 dp=[];checks=[]
 for doc in s['documents']:
  if not doc['path'].endswith('.json'):continue
  jd=load(Path(doc['path']));validate_pin_tree(jd,dp)
  for pr in jd.get('providers',[])+([jd['corrected_provider']] if 'corrected_provider' in jd else []):
   fp=Path(pr['source']['path']);ck(pr['source']);ls=fp.read_text(encoding='utf8').splitlines();stmt=pr.get('statement',pr.get('excerpt'))
   assert stmt
   actual='\n'.join(ls[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
   assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr.get('name',pr['statement'].split(' :',1)[0])
   op=V/fp.relative_to(K);assert op.read_bytes()==fp.read_bytes()
   checks.append(dict(name=pr.get('name',pr['statement'].split(' :',1)[0]),line=pr['line'],statement=stmt,source_excerpt='\n'.join(ls[pr['line']-1:pr['line']+15]),author=pin(fp),own=pin(op)))
 assert len(checks)==13
 cj=load(R/'REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR.json')['consumer'];cl=Path(cj['source']['path']).read_text(encoding='utf8').splitlines()
 assert '\n'.join(cl[cj['line']-1:]).startswith(cj['statement'])
 save(OUT/'provider_checks.json',dict(checks=checks,consumer=dict(**cj,source_excerpt='\n'.join(cl[cj['line']-1:cj['line']+12])),consumer_status='IMPLEMENTATOR_EQUALITY_PROVED__QUADRATIC_TRACE_OPEN'))
 base=load(OUT/'preservation_19_940.json');validate_pin_tree(base,[])
 assert base['all_matched'] and base['baseline_file_count']==940 and len(base['original_v351'])==19
 oldnew=[x for x in s['sources'] if not x['target'] and not x['source_preexisting']]
 assert {x['module'] for x in oldnew}=={'TGLExt.V350ScalarRegularPolarCommutation'}
 old_audits=[]
 for x in oldnew:
  tr,tj,mi=trace(x['module']);oa=parse_axioms('\n'.join(mi))
  assert len(oa)==4 and all(set(v)<=ALLOWED for v in oa.values())
  old_audits.append(dict(module=x['module'],source=x,trace=pin(tr),axioms=oa,new_theorems_counted=False))
 pr=load(R/'ADENDO_FICHA_IMPLEMENTADOR_MODULAR.json')['provider_replay']
 ck(pr);pj=load(Path(pr['path']));validate_pin_tree(pj,[])
 assert pj['returncode']==0 and pj['source_bytes_unchanged'] and len(pj['new_or_changed_objects'])==1
 save(OUT/'old_supplier_replay_read.json',dict(author=pr,author_metadata=pj,own=old_audits))
 expected_new=set(s['modules']+[s['auditor_module']]+[x['module'] for x in oldnew])
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
 assert {x['module'] for x in new}==expected_new
 stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
 assert set(built)==expected_new
 comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=0,private_definitions=0,total_source_theorems_including_private=1,
 all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
 all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; three failed author DEV attempts excluded; only final whole-file rc0 accepted.',
 all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,
 own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_cache_not_rebuilt=True,
 package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
 own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
 newly_recompiled_old_supplier_count=len(oldnew),newly_recompiled_old_suppliers=old_audits,old_supplier_replay=pin(OUT/'old_supplier_replay_read.json'),objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
 type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,
 lake_stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8'),built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,
 baseline_preservation=pin(OUT/'preservation_19_940.json'),original_v351_count=19,baseline_files_count=940,baseline_lean_count=937,baseline_config_count=3,nineteen_subset_of_baseline=True,
 fiche_provider_pins=dp,provider_checks=pin(OUT/'provider_checks.json'),history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
 helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py','negative_control.py','auxiliary_helpers_provenance.json']],
 modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=True,core_traciality_proved=False,full_trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False)
 checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
 limits=['Aceite32: um teorema público, zero privados/defs; um fornecedor antigo de quatro declarações reconstruído separadamente, além do auditor próprio.', 'U_t=π(λ_t)R_-t em TODO H_I original está demonstrado. Q, meias potências/domínios, tracialidade e contrato de traço continuam abertos; não há h=Delta_nu.', '19 V351 são subconjunto das 940 entradas da base, não959. Preservação relida em bytes.', 'Somente esta pasta e novas saídas em V foram escritas; K/OLD/V353, memórias, monólito, writers e predecessores preservados.']
 report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
 exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=0,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],
 type_axiom_audit=comp['type_axiom_audit'],semantic_review=PARAGRAPHS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],
 all_prior_pins_preserved=True,modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=True,average_selfadjoint_claimed=False,core_traciality_proved=False,trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False)
 validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
 obj=next(x for x in objects if x['module'] in s['modules'])
 md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Módulo e auditor próprios rc0; um tipo completo com universos, axiomas do trio. Controle negativo próprio rc1 por Type mismatch.\n\n'+'\n\n'.join(PARAGRAPHS)
 md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios preservados; '+str(len(new))+' novos (alvo+auditor+um fornecedor antigo), total '+str(len(objects))+'. Um fornecedor antigo reconstruído de fonte, nenhum objeto K/DEV herdado. Run '+str(round(run['elapsed_seconds'],3))+' s; negativo '+str(round(ownneg['elapsed_seconds'],3))+' s. Zero avisos do alvo/auditor; '+str(len(sw))+' mensagens de fornecedores discriminadas em supplierwarnings (old_object indica herança). all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui o negativo esperado. LEAN_PATH dos traces restrito a V/pacotes.\n\n'
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

