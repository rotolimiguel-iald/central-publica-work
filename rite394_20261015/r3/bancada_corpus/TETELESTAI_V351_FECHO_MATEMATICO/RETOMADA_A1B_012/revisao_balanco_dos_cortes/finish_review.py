from review_helpers import *

SEMANTICS = [
 '[REAL — tipo e objetos] Um teorema público, nove auxiliares privados e zero definições. O público recebe somente P:SiteProfile, epsilon/eta reais e suas positividades. Conclui Commute T C_epsilon, Commute T D_eta e (1-T) C_epsilon q_eta = T p_epsilon D_eta no MESMO ScalarGNSHilbert P. T é scalarTomitaResolvent P; A=pi(regularSpectralResolvent P) e B=J A J^-1 são distintos. Não recebe balanço, comutação, tracialidade ou igualdade h=Delta_nu como premissas.',
 '[REAL — fases concretas e sinal] regularPositiveGenerator_imaginaryPower e resolventImaginaryPower_damping dão a fase amortecida do resolvente regular; closed_representation_cfc transporta essa igualdade pela pi original. antiunitaryConjugate_complex_cfc e resolventPhaseFunction_star produzem a fase de B em -t, em conformidade com scalarTomitaPolar_regular_generator. A igualdade efetiva dos implementadores32 é consumida, junto da comutação da ação direita com pi: não se infere igualdade de grupos apenas de covariância.',
 '[REAL — comutações] T comuta com as translações representadas pelo fornecedor direito antigo e pelo flip J T J^-1=1-T. As janelas seno, CFC e convergência forte uniformemente limitada transportam isso a A. O mesmo flip dá TB=BT; AB=BA vem de scalarTomitaPolar_core_commutes, válido para todo core. As duas novas conclusões públicas usam o CFC do MESMO corte e hTA já obtido, seguido da conjugação por J. Nenhuma nova hipótese de CompleteSpace da VNA: fechamento normado é deduzido do bicomutante e fornece a instância do subtipo.',
 '[REAL — extremos e cancelamento] No cálculo escalar, o produto dos amortecimentos nulo é tratado primeiro. Somente no caso não nulo se deduz interioridade e positividade dos argumentos de log/divisões e se aplica modular_phase_frequency_separation. A subálgebra comutativa fechada dos três resolventes usa Gelfand e map_cfc existentes; positividade ambiente é refletida explicitamente por raiz no subtipo, sem pressupor identificação de ordens. O produto amortecedor é cancelado como composição de aplicações vetoriais injetivas. Não se exige gap, inversa limitada, sobrejetividade ou densidade dos caracteres interiores.',
 '[REAL — injetividade representada e cortes] A injetividade de a.val passa por dualAmbient, pelas duas igualdades a.e. de operatorFieldLift para cada par de vetores e pela restrição original a H_I. Não se confunde fidelidade de pi com injetividade de pi(a) como operador. Os complementos são tratados do mesmo modo. B_1=R e regularDomainCut_inverse_product dão A p=(1-A) C; a conjugação dá B q=(1-B) D. O lema puramente de anel explicita a ordem dos fatores e as comutações usadas. A igualdade multiplicada à esquerda por AB é cancelada por hiA.comp hiB, sem declarar que toda álgebra de operadores não tem divisores de zero.',
 '[REAL — metadados e história] A auditoria inicial truncou o resultado no primeiro let :=. A versão TIPO_COMPLETO modifica somente esse enunciado nos metadados; o tipo completo já estava no stdout Lean e a auditoria anterior permanece pinada. O tipo extraído desta revisão termina no := by que inicia a prova e coincide com o tipo completo corrigido; o auditor próprio imprime ambas as comutações e a identidade, com universos. As tentativas DEV e sucessos apenas parciais são inventariados separadamente, com pins dos snapshots reais e a localização histórica apenas textual. Nenhum print de rc1 nem sucesso parcial foi contado como aceite33.',
 '[REAL — independência] Lake no V, com LEAN_PATH/LEAN_SRC_PATH externos removidos, reutiliza os objetos próprios anteriores e o cache de pacotes já pinado. Fontes dos fornecedores antigos ausentes foram copiadas da base preservada e comparadas com K; nenhum olean K/DEV foi copiado. Os traces registram somente V e seus pacotes nos caminhos Lean. A ressalva de autoria histórica dos dois módulos antiunitários e a inspeção independente pelo principal permanecem as dos40; esta revisão não as reclassifica.',
 '[OPEN — alcance] Balanço limitado e suas duas comutações estão pagos neste delta. O transporte para a igualdade quadrática Q, tracialidade de scalarInverseLimitWeight e contrato completo do traço ainda não estão provados por esta entrega. Não identifica h com Delta_nu, não atribui domínio a produto ilimitado e não move gate. Nenhum monólito, writer, memória, recibo ou fonte autoral foi executado/modificado.'
]

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot']);a=Path(pointer['attempt'])
    s=load(a/'snapshot.json');run=load(a/'run.json');assert run['returncode']==0
    assert load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for row in s['sources']:ck(row['original']);ck(row['copy'])
    target=next(x for x in s['sources'] if x['target']);names={t['name'] for t in s['targets']}
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(names)==1 and len(re.findall(r'^theorem\s+',code,re.M))==1
    assert len(re.findall(r'^private theorem\s+',code,re.M))==9
    assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
    audit_trace,_,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==names and all(set(v)<=ALLOWED for v in ax.values())
    types={}
    for name in names:
        found=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name]
        assert len(found)==1
        assert found[0].count('Commute.')==2 and 'regularDomainCut P ε' in found[0] and 'regularDomainCut P η' in found[0]
        types[name]=found[0]
    target_trace,_,target_infos=trace(target['module']);all_target_ax=parse_axioms('\n'.join(target_infos))
    assert len(all_target_ax)==10 and all(set(v)<=ALLOWED for v in all_target_ax.values())
    private_ax={n:v for n,v in all_target_ax.items() if n not in names};assert len(private_ax)==9
    assert next(v for n,v in private_ax.items() if n.endswith('.cut_balance_after_multiplication'))==['propext']
    source_types={}
    for m in re.finditer(r'^(?:private )?theorem\s+(\S+)',code,re.M):
        end=code.index(':= by',m.end());source_types[m[1]]=code[m.start():end].rstrip()
    author_read=load(OUT/'author_evidence_read.json');author=author_read['metadata'];validate_pin_tree(author_read,[])
    assert source_types['scalarTomitaResolvent_double_cut_balance']==author['targets'][0]['statement']
    assert author['modules'][0]['source']==target['original']
    assert author['double_cut_balance_constructed'] and author['cut_commutation_constructed']
    assert not author['core_traciality_proved'] and not author['full_trace_constructed']
    save(a/'type_axiom_audit.json',dict(types=types,source_types=source_types,axioms=ax,private_axioms=private_ax,all_axioms=all_target_ax,trace=pin(audit_trace),target_trace=pin(target_trace),exact_target_count=1,private_helpers_audited_transitively=True))
    ownneg=load(OUT/'negative_control_own.json');validate_pin_tree(ownneg,[])
    negtext=Path(ownneg['stdout']['path']).read_text(encoding='utf-8-sig')
    negerr=Path(ownneg['stderr']['path']).read_text(encoding='utf-8-sig')
    assert ownneg['returncode']==1 and 'type mismatch' in negtext.lower() and ownneg['own_execution']
    assert not any(w in negtext.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
    assert ownneg['source']==author_read['commands'][1]['source']
    negative=dict(status='OWN_AND_AUTHOR_REJECTED_TYPE_MISMATCH',own_execution=True,own=ownneg,own_stdout_text=negtext,own_stderr_text=negerr,author_audit=author_read['audit'],author_rows=author_read['commands'])
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
            oa=parse_axioms('\n'.join(mi));assert oa and all(set(v)<=ALLOWED for v in oa.values())
            old.append(dict(module=mod,source=row['source'],trace=pin(tr),axioms=oa,new_theorems_counted=False))
        for msg in tj['log']:
            if msg['level']=='warning':
                (tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    assert {x['module'] for x in old}=={'TGLExt.PhaseFrequencySeparation','TGLExt.V350CorePolarInclusion'}
    new=[x for x in objects if not x['own_previously_compiled']]
    expected_new=set(s['modules']+[s['auditor_module']]+[x['module'] for x in old])
    assert {x['module'] for x in new}==expected_new
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf-8-sig')
    stderr=Path(run['streams'][1]['path']).read_text(encoding='utf-8-sig')
    assert not re.search(r'^error:',stdout,re.M)
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout);assert set(built)==expected_new
    printed=parse_axioms(re.sub(r'^info: [^\n]*?\.lean:\d+:\d+:\s*','',stdout,flags=re.M))
    assert printed and all(set(v)<=ALLOWED for v in printed.values())
    save(OUT/'old_supplier_replay_read.json',dict(own=old,newly_built_old_count=len(old),old_printed_declarations=sum(len(x['axioms']) for x in old),source_only_copy=True))
    for p in s['protected']:ck(p)
    comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
      exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=9,private_definitions=0,total_source_theorems_including_private=10,
      all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,all_expected_exit_codes_observed=True,
      all_attempts_scope='Own positive Lake rc0 and intentional negative rc1; author DEV failures and partial rc0 snapshots excluded from final acceptance.',
      all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,all_printed_build_axioms_allowed=True,printed_build_axiom_count=len(printed),
      own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_cache_not_rebuilt=True,
      package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
      own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=len(old),newly_recompiled_old_suppliers=old,old_supplier_replay=pin(OUT/'old_supplier_replay_read.json'),
      objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,
      supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,
      baseline_preservation=pin(OUT/'preservation_19_940.json'),original_v351_count=19,baseline_files_count=940,baseline_lean_count=937,baseline_config_count=3,nineteen_subset_of_baseline=True,
      fiche_provider_pins=providers['pins'],provider_checks=pin(OUT/'provider_checks.json'),history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history['rows'],author_audit=author_read['audit'],metadata_correction_verified=True,
      helper_provenance=[pin(OUT/n) for n in ['setup_review.py','build_delta.py','review_helpers.py','helper_provenance.json','inspect_evidence.py','finish_review.py','negative_control.py']],
      modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=True,double_cut_balance_constructed=True,cut_commutation_constructed=True,
      core_traciality_proved=False,full_trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False,gate_changed=False)
    checked=[];validate_pin_tree(comp,checked)
    limits=['Aceite33 restrito a um público de balanço e duas comutações, nove privados, zero defs; dois fornecedores antigos reconstruídos e discriminados separadamente.',
      'Q, tracialidade de scalarInverseLimitWeight e contrato completo do traço permanecem OPEN; h não foi identificado com Delta_nu.',
      '19 V351 são subconjunto das940 entradas de base, não959; fontes e predecessores relidos por bytes.',
      'A execução de publicação/entrega e atualização de memória cabe ao principal após ler este parecer. Nenhum writer, monólito ou memória foi executado/modificado.']
    save(OUT/'compilation.json',comp)
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=9,private_definitions=0,
      run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=SEMANTICS,limits=limits,negative_controls=negative,baseline_preservation=comp['baseline_preservation'],
      all_prior_pins_preserved=True,all_axioms_allowed=True,all_target_typechecks_present=True,all_accepted_builds_exit_zero=True,all_attempts_exit_zero=False,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,
      modular_fixed_vectors_constructed=True,fixed_tomita_vectors_constructed=True,implementator_equality_proved=True,double_cut_balance_constructed=True,cut_commutation_constructed=True,core_traciality_proved=False,full_trace_constructed=False,trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module']==target['module'])
    md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Fonte final e auditor próprios rc0; controle negativo próprio rc1 por Type mismatch com imports válidos. Aceite independente33, limitado ao balanço e suas duas comutações.\n\n'+'\n\n'.join(SEMANTICS)
    md+='\n\n[REAL — execução] '+str(len(inherited))+' objetos próprios preservados; '+str(len(new))+' novos (alvo, auditor, PhaseFrequencySeparation e V350CorePolarInclusion), total '+str(len(objects))+'. Os dois fornecedores antigos imprimem '+str(sum(len(x['axioms']) for x in old))+' declarações já existentes, não contadas como novidade. '+str(round(run['elapsed_seconds'],3))+' s no Lake; '+str(round(ownneg['elapsed_seconds'],3))+' s no negativo. Zero avisos do alvo/auditor; '+str(len(sw))+' mensagens herdadas/de fornecedores discriminadas em supplierwarnings. O aviso aesop de alterações locais pertence ao cache de pacotes herdado e está preservado no stderr. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui a recusa esperada.\n\n'
    md+='[REAL — histórico] '+str(len(history['rows']))+' DEV preservados: '+str(history['failed_count'])+' rc1 recusados, '+str(history['partial_success_count'])+' rc0 de snapshots parciais/superados, e um final rc0. Os limites locais de elaboração do fonte final são '+', '.join(history['rows'][-1]['heartbeat_limits'])+' heartbeats; não se declara orçamento uniforme de200k. Nenhuma recompilação independente inalterada foi repetida.\n\n'
    md+='| Artefato | Bytes | SHA256 lido |\n|---|---:|---|\n'
    for label,p in [('Fonte K=snapshot=V',obj['source']),('.olean próprio',obj['own']),('.olean autoral, só comparação',obj['author_cold'])]:md+='| '+label+' | '+str(p['bytes'])+' | '+p['sha256']+' |\n'
    md+='\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\nTipo público completo, confrontado com #check próprio com universos:\n\n~~~lean\n'+author['targets'][0]['statement']+'\n~~~\n\nAxiomas públicos próprios: '+', '.join(ax[next(iter(names))])+'. Os nove privados foram impressos no build próprio; cut_balance_after_multiplication usa apenas propext, os outros permanecem no trio. Tipos-fonte completos dos privados e respectivos axiomas estão no type_axiom_audit.json.\n\n'
    md+='[OPEN] '+' '.join(limits)+'\n\nEvidências:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos e axiomas',comp['type_axiom_audit']),('negativo próprio',ownneg['run']),('preservação19/940',comp['baseline_preservation']),('fichas e fornecedores',comp['provider_checks']),('histórico',comp['history'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode('utf-8'))
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(status=STATUS,report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],P0=[],P1=[],P2=[],objects_before=len(inherited),objects_after=len(objects),binary_equal=obj['equal_author_cold'],negative_rc=ownneg['returncode'],old_suppliers=len(old)),ensure_ascii=False))

if __name__=='__main__':main()
