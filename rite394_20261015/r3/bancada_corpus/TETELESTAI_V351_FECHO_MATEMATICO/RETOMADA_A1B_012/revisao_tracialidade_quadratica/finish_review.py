from review_helpers import *
sys.stdout.reconfigure(encoding='utf-8')

SEMANTICS=[
 '[REAL — delta34] Um teorema público, scalarInverseLimitWeight_tracial, seis teoremas privados e uma definição consumidora, scalarInverseLimitTraceData.{u}. Não há outras definições nem teoremas públicos. O público recebe somente P:SiteProfile e a no core original: nenhuma hipótese de Q, tracialidade ou equivalência h=Delta_nu. A definição é polimórfica no universo u das redes do campo normal.',
 '[REAL — formas e domínio] root_quadratic_commutation usa autoadjunção da raiz, positive_sqrt_intertwines e sqrt_mul_sqrt_self. bounded_root_form_balance aplica o balanço limitado (1-T)U=TV ao grafo já existente resolventSquareRoot T hT hi. O parâmetro u pertence ao Hilbert genérico; x=sqrt(T)u e a raiz original aplicada a x é sqrt(1-T)u. A mudança de localização da aplicação ao grafo não adiciona hipótese, raiz, GNS ou camada pública. Não se atribui domínio a produto ilimitado.',
 '[REAL — retirada dos dois cortes] double_cut_form_supremum compara os produtos C_n q_m e p_n D_m com C_n e D_m mediante positividade, contrações e comutações explícitas. Passa ao limite em um índice por vez com continuidade e le_of_tendsto em ENNReal. Não pressupõe finitude dos supremos, monotonicidade de C/D ou cota uniforme de C/D. As hipóteses inferiores 0<=p e 0<=q são mais fortes do que as usadas nesse privado, sem afetar validade.',
 '[REAL — famílias concretas] scalar_root_cut_supremum usa pi e J originais, C_n=pi(B_delta_n), D_n=J C_n J^-1, p_n=pi(q_delta_n) e q_n=J p_n J^-1, delta_n=1/(n+1). Positividade/ordem passam pela representação; a convergência forte uniformemente limitada dos cortes passa por scalarGNSRepresentation_tendsto_of_uniformly_bounded. A conjugação por J transporta o segundo limite. CorePolarInclusion fornece as comutações cruzadas; o público33 fornece TC=CT, TD=DT e o balanço. As comutações restantes são descarregadas por p=1-delta C e pelo flip original. Não se usa h=Delta_nu nem se deduz igualdade de grupos apenas de covariância.',
 '[REAL — peso e forma] represented_positive_root_norm é somente o cálculo de Gram de pi(star b), para b a raiz original de B_epsilon. map_star/map_mul e b*star b=B_epsilon fornecem a forma Re<x,pi(B_epsilon)x>. scalar_inverse_cutoff_weight_form consome scalarWeight_inverseCutoff_perturbed_norm: sua pertinência da raiz é obtida do fornecedor existente. Mantém ENNReal.ofReal(Re inner), J.symm e o MESMO scalarWeightGNSEmbedding. Não introduz nova normalidade, nova representação ou identidade entre pi(sqrt B) e uma raiz redefinida.',
 '[REAL — tracialidade sem premissa residual] Para a em finiteDualStarCore, o embedding uniforme é incluído no ideal de peso completo pelo fornecedor antigo, e scalarWeightGNSEmbedding_uniform identifica o vetor. scalarStarCore_mem_closedTomitaDomain e scalarClosedTomita_extends_star dão o domínio e S Lambda(a)=Lambda(a*). A fatorização original dá J.symm Lambda(a*)=root Lambda(a). O balanço de supremos e antiunitary_inner_conj, após tomar Re, dão tau(a*a)=tau(aa*). scalarInverseLimitWeight_tracial_iff_core é aplicado com ESSA prova e estende a igualdade a todo elemento limitado do core. O núcleo algébrico não é declarado analítico.',
 '[REAL — contrato concreto] scalarInverseLimitTraceData.value é literalmente scalarInverseLimitWeight P. Os nove campos de leis são ligados aos fornecedores existentes. Em especial, semifinite recebe scalarInverseLimitWeight_finite_minorants P (scalarInverseLimitWeight_tracial P): a premissa htr do fornecedor28 é agora descarregada, não recebida como campo aberto. normal cobre redes dirigidas arbitrárias no universo u; dual_scaling usa exp(-s). Fidelidade e positiveUnit_ne_zero no contrato excluem o traço zero. Não se renomeia scalarDualWeight: o valor é o supremo da sua perturbação já construído, sem mudar normalização.',
 '[REAL — execução e preservação] Lake foi executado em V com objetos próprios anteriores e cache de pacotes herdado pinado. Nenhum objeto K/DEV foi copiado e LEAN_PATH/LEAN_SRC_PATH externos foram removidos. Os caminhos dos comandos Lean nos traces foram conferidos. Fontes, objetos e relatórios predecessores permanecem byte a byte. Os 19 V351 originais são subconjunto das940 entradas de base. A ressalva de autoria histórica dos dois módulos antiunitários e a inspeção pelo principal permanecem as registradas na revisão dos40; não são reclassificadas aqui.',
 '[REAL — história e parser] Os sete snapshots DEV foram preservados: cinco rc1, um rc0 parcial e o final rc0. Prints dos rc1, inclusive os timeouts de6m/18m, não são evidência de aceite. Os pins históricos apontam para os snapshots reais, com a localização antiga apenas textual. O parser próprio normaliza sufixos de universos dos axiomas e aceita a forma does not depend on any axioms; o stdout bruto fica intacto. A consulta de console teve somente erro de codificação cp1252 ao exibir um tipo; a exibição foi refeita em UTF-8 sobre os MESMOS traces, sem nova compilação.',
 '[LIMITE] Aceite do contrato RegularCoreTraceData no core concreto de A1: tracialidade, normalidade, fidelidade, semifinitude por minorantes e escala dual do MESMO peso. Não identifica h com Delta_nu; não paga A2/PF, quadro de quatro frames, H3, testemunha completa, física ou gate. Nenhum writer, monólito, memória, recibo ou fonte K foi executado/modificado. A entrega/custódia posterior cabe ao principal.'
]

FIELDS={
 'value':'scalarInverseLimitWeight P',
 'zero':'scalarInverseLimitWeight_zero P',
 'additive':'scalarInverseLimitWeight_add P',
 'homogeneous':'scalarInverseLimitWeight_scale P',
 'monotone':'scalarInverseLimitWeight_mono P',
 'faithful':'scalarInverseLimitWeight_faithful P',
 'normal':'scalarInverseLimitWeight_normal P',
 'semifinite':'scalarInverseLimitWeight_finite_minorants P (scalarInverseLimitWeight_tracial P)',
 'tracial':'scalarInverseLimitWeight_tracial P',
 'dual_scaling':'scalarInverseLimitWeight_dual P'
}

def main():
 pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot']);a=Path(pointer['attempt'])
 s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
 for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
 for row in s['sources']:ck(row['original']);ck(row['copy'])
 targetrows=[r for r in s['sources'] if r['target']];names={x['name'] for x in s['targets']}
 assert len(targetrows)==2 and len(names)==2
 codes={r['module']:uncomment(Path(r['copy']['path']).read_text(encoding='utf-8-sig')) for r in targetrows}
 combined='\n'.join(codes.values())
 assert len(re.findall(r'^theorem\s+',combined,re.M))==1
 assert len(re.findall(r'^private theorem\s+',combined,re.M))==6
 assert len(re.findall(r'^def\s+',combined,re.M))==1
 assert not re.findall(r'^private def\s+',combined,re.M)
 assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',combined)
 atr,_,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
 assert set(ax)==names and all(set(v)<=ALLOWED for v in ax.values())
 types={}
 for name in names:
  found=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(found)==1;types[name]=found[0]
 assert 'positiveSquare P (star.{0} A)' in types['TGLV350.Regular.scalarInverseLimitWeight_tracial']
 assert 'scalarInverseLimitTraceData.{u}' in types['TGLV350.Regular.scalarInverseLimitTraceData']
 assert 'RegularCoreTraceData.{u} P' in types['TGLV350.Regular.scalarInverseLimitTraceData']
 allax={};target_traces=[];source_types={}
 for module,code in codes.items():
  tr,_,mi=trace(module);target_traces.append(pin(tr));parsed=parse_axioms('\n'.join(mi));assert all(set(v)<=ALLOWED for v in parsed.values());allax.update(parsed)
  for m in re.finditer(r'^(?:private )?(theorem|def)\s+(\S+)',code,re.M):
   end=code.index(':= by' if m[1]=='theorem' else ' where',m.end());source_types[m[2]]=code[m.start():end].rstrip()
 assert len(allax)==8 and names<=set(allax)
 private_ax={n:v for n,v in allax.items() if n not in names};assert len(private_ax)==6
 author_read=load(OUT/'author_evidence_read.json');validate_pin_tree(author_read,[]);author=author_read['metadata']
 for t in author['targets']:
  assert source_types[t['name'].split('.')[-1]]==t['statement']
  assert t['source']==next(r['original'] for r in targetrows if r['module'].endswith(t['module']))
 package_code=codes['TGLExt.V351RegularCoreTraceConstruction']
 actual_fields=dict(re.findall(r'^  (\w+) := (.+)$',package_code,re.M));assert actual_fields==FIELDS
 contract=V/'TGLExt/V351RegularCoreTraceContract.lean';ct=contract.read_text(encoding='utf-8-sig')
 block=ct.split('structure RegularCoreTraceData (P : SiteProfile) where',1)[1].split('\ntheorem ',1)[0]
 contract_fields=re.findall(r'^  (\w+) :',block,re.M);assert contract_fields==list(FIELDS)
 assert 'semifinite : ∀ A, value A =' in block and '{ι : Type u}' in block
 assert 'ENNReal.ofReal (Real.exp (-s)) * value A' in block
 assert 'RegularCoreTraceData.not_zero' in ct and 'positiveUnit_ne_zero' in ct
 save(a/'type_axiom_audit.json',dict(types=types,source_types=source_types,axioms=ax,private_axioms=private_ax,all_axioms=allax,trace=pin(atr),target_traces=target_traces,exact_target_count=2,private_helpers_audited_transitively=True,universe_annotations_normalized_only_for_parser=True))
 contract_mapping=dict(contract_source=pin(contract),construction_source=next(r['copy'] for r in targetrows if r['module'].endswith('V351RegularCoreTraceConstruction')),fields=FIELDS,law_field_count=9,value_is_literal_existing_weight=True,traciality_premise_discharged=True,normal_universe='arbitrary u',zero_trace_excluded_by_existing_faithfulness=True,h_not_identified_with_Delta=True)
 save(OUT/'contract_mapping.json',contract_mapping)
 ownneg=load(OUT/'negative_control_own.json');validate_pin_tree(ownneg,[])
 ns=Path(ownneg['stdout']['path']).read_text(encoding='utf-8-sig');ne=Path(ownneg['stderr']['path']).read_text(encoding='utf-8-sig')
 assert ownneg['returncode']==1 and 'type mismatch' in ns.lower() and ownneg['own_execution']
 assert not any(w in ns.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
 assert ownneg['source']==author_read['commands'][1]['source']
 negative=dict(status='OWN_AND_AUTHOR_REJECTED_TYPE_MISMATCH',own_execution=True,own=ownneg,own_stdout_text=ns,own_stderr_text=ne,author_audit=author_read['audit'],author_rows=author_read['commands'],scope='Replace tau(aa*) with zero in the exact theorem; does not claim generic impossibility of proving altered propositions.')
 save(OUT/'negative_controls_read.json',negative)
 inspected=load(OUT/'inspection_summary.json');validate_pin_tree(inspected,[]);assert inspected['all_checks_passed']
 history=load(OUT/'history_read.json');validate_pin_tree(history,[])
 base=load(OUT/'preservation_19_940.json');validate_pin_tree(base,[]);assert base['all_matched']
 providers=load(OUT/'provider_checks.json');validate_pin_tree(providers,[])
 inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
 objects=[];tw=[];sw=[];old=[]
 for q in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
  mod=str(q.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
  tr,tj,mi=trace(mod)
  row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(q),trace=pin(tr),own_previously_compiled=str(q) in inherited)
  if mod in s['modules']:
   row['author_cold']=pin(K/'.lake/build/lib/lean'/q.relative_to(V/'.lake/build/lib/lean'))
   row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
  if not row['own_previously_compiled'] and mod not in s['modules']+[s['auditor_module']]:
   oa=parse_axioms('\n'.join(mi));assert all(set(v)<=ALLOWED for v in oa.values())
   old.append(dict(module=mod,source=row['source'],trace=pin(tr),axioms=oa,new_theorems_counted=False))
  for msg in tj['log']:
   if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
  objects.append(row)
 assert not tw and not old
 new=[x for x in objects if not x['own_previously_compiled']];expected_new=set(s['modules']+[s['auditor_module']])
 assert {x['module'] for x in new}==expected_new
 stdout=Path(run['streams'][0]['path']).read_text(encoding='utf-8-sig');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf-8-sig')
 assert not re.search(r'^error:',stdout,re.M)
 built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout);assert set(built)==expected_new
 printed=parse_axioms(re.sub(r'^info: [^\n]*?\.lean:\d+:\d+:\s*','',stdout,flags=re.M));assert printed and all(set(v)<=ALLOWED for v in printed.values())
 save(OUT/'old_supplier_replay_read.json',dict(own=old,newly_built_old_count=0,old_printed_declarations=0,source_only_copy=True))
 for p in s['protected']:ck(p)
 flags=dict(modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=True,double_cut_balance_constructed=True,cut_commutation_constructed=True,core_traciality_proved=True,full_trace_constructed=True,trace_constructed=True,quadratic_trace_compatibility_proved=True,gate_modified=False,gate_changed=False)
 comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
  exact_target_count=2,new_theorems=1,new_definitions=1,private_theorems=6,private_definitions=0,total_source_theorems_including_private=7,
  all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
  all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; five author DEV failures and one partial rc0 excluded from acceptance. Console-only cp1252 display failure is not a Lean run.',
  all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,all_printed_build_axioms_allowed=True,printed_build_axiom_count=len(printed),
  own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_cache_not_rebuilt=True,
  package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
  own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=0,newly_recompiled_old_suppliers=old,old_supplier_replay=pin(OUT/'old_supplier_replay_read.json'),
  objects=objects,sourcepins=targetrows,run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,
  supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,
  baseline_preservation=pin(OUT/'preservation_19_940.json'),original_v351_count=19,baseline_files_count=940,baseline_lean_count=937,baseline_config_count=3,nineteen_subset_of_baseline=True,
  fiche_provider_pins=providers['pins'],provider_checks=pin(OUT/'provider_checks.json'),history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history['rows'],author_audit=author_read['audit'],
  helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','inspect_evidence.py','finish_review.py','negative_control.py']],
  contract_mapping=pin(OUT/'contract_mapping.json'),trace_scope='RegularCoreTraceData.{u} P with literal scalarInverseLimitWeight P; no A2/PF, H3, four-frame, full witness or gate promotion.',
  **flags)
 checked=[];validate_pin_tree(comp,checked)
 limits=['Aceite34: um público de tracialidade, seis privados e uma definição consumidora de RegularCoreTraceData.{u}; valor é o mesmo scalarInverseLimitWeight.',
  'full_trace_constructed significa contrato concreto de A1 preenchido. Não significa A2/PF, quatro frames/H3, testemunha completa, confirmação física ou gate.',
  'h não foi identificado com Delta_nu; não foi construída outra medida, estado, GNS ou gerador.',
  'Os19 V351 estão dentro das940 entradas de base; não são959. Fontes, objetos e relatórios predecessores foram relidos por bytes.',
  'Entrega/custódia e memória posteriores são atos do principal após ler o parecer. Nenhum writer/monólito/memória/K foi executado ou modificado.']
 save(OUT/'compilation.json',comp)
 report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],exact_target_count=2,new_theorems=1,new_definitions=1,private_theorems=6,private_definitions=0,
  run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=targetrows,type_axiom_audit=comp['type_axiom_audit'],semantic_review=SEMANTICS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],contract_mapping=comp['contract_mapping'],
  all_prior_pins_preserved=True,all_axioms_allowed=True,all_target_typechecks_present=True,all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,**flags)
 validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
 md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Os dois módulos e o auditor próprios passaram rc0; o negativo próprio foi recusado rc1 por Type mismatch com imports válidos. Aceite independente34: tracialidade do mesmo peso e preenchimento do contrato RegularCoreTraceData.\n\n'+'\n\n'.join(SEMANTICS)
 md+='\n\n[REAL — campos do contrato] O campo value não é uma lei nova. As nove leis são:\n\n| Campo | Fornecedor aplicado |\n|---|---|\n'
 for name,value in FIELDS.items():md+='| `'+name+'` | `'+value+'` |\n'
 md+='\n[REAL — execução] '+str(len(inherited))+' objetos próprios preservados; '+str(len(new))+' novos (dois módulos e auditor), total '+str(len(objects))+'. Zero fornecedores antigos adicionais reconstruídos. '+str(round(run['elapsed_seconds'],3))+' s no Lake; '+str(round(ownneg['elapsed_seconds'],3))+' s no negativo. Zero avisos de alvo/auditor; '+str(len(sw))+' mensagens herdadas discriminadas em supplierwarnings. O aviso aesop de alterações locais do cache está preservado no stderr. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui a recusa esperada.\n\n'
 md+='[REAL — histórico] '+str(len(history['rows']))+' snapshots DEV: '+str(history['failed_count'])+' rc1 recusados, '+str(history['partial_success_count'])+' rc0 parcial, '+str(history['final_success_count'])+' final rc0. O final usa maxHeartbeats global2400000 e local6000000; não se declara orçamento200k. As tentativas de6m/18m permanecem preservadas. Nenhuma execução matemática verde foi repetida para corrigir parser ou console.\n\n'
 md+='| Artefato | Bytes | SHA256 lido |\n|---|---:|---|\n'
 for obj in objects:
  if obj['module'] not in s['modules']:continue
  for label,p in [(obj['module']+' fonte K=snapshot=V',obj['source']),(obj['module']+' olean próprio',obj['own']),(obj['module']+' olean autoral só comparação',obj['author_cold'])]:md+='| '+label+' | '+str(p['bytes'])+' | '+p['sha256']+' |\n'
  md+='\nIgualdade binária medida para '+obj['module']+': '+str(obj['equal_author_cold'])+'.\n\n'
 md+='Tipos públicos completos extraídos e confrontados com #check próprio:\n\n'
 for t in author['targets']:md+='~~~lean\n'+t['statement']+'\n~~~\n\n'
 md+='Axiomas próprios dos dois alvos e dos seis privados: `propext`, `Classical.choice`, `Quot.sound`. Universos são normalizados somente no parser; tipos/streams brutos preservados. Os tipos completos de todas as privadas constam no type_axiom_audit.json.\n\n[REAL — negativo próprio]\n\n~~~text\n'+ns.strip()+'\n~~~\n\n'
 md+='[LIMITE] '+' '.join(limits)+'\n\nEvidências:\n\n'
 for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos e axiomas',comp['type_axiom_audit']),('negativo próprio',ownneg['run']),('campos do contrato',comp['contract_mapping']),('preservação19/940',comp['baseline_preservation']),('fichas e fornecedores',comp['provider_checks']),('histórico',comp['history'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
 fresh(OUT/(NAME+'.md'),md.encode('utf-8'))
 save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
 print(json.dumps(dict(status=STATUS,report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],P0=[],P1=[],P2=[],objects_before=len(inherited),objects_after=len(objects),binary_equal=[x['equal_author_cold'] for x in objects if x['module'] in s['modules']],negative_rc=ownneg['returncode'],old_suppliers=0,supplierwarnings=len(sw),targetwarnings=len(tw)),ensure_ascii=False))

if __name__=='__main__':main()
