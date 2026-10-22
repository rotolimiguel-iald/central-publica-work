from review_helpers import *

FINAL_STATUS=STATUS

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==2 and all(t['kind']=='theorem' for t in s['targets'])
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==2 and len(re.findall(r'^private theorem\s+',code,re.M))==1
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(2,0,1,0)
    br=load(Path(author['positive_build']['path']));assert br['returncode']==0;validate_pin_tree(br,pins)
    assert len(author['commands'])==2;rows=[]
    for i,row in enumerate(author['commands']):
        txt=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
        if i==0:
            aa=parse_axioms(txt);assert row['returncode']==0 and set(aa)==expected and all(set(v)<=ALLOWED for v in aa.values())
        else:
            assert row['returncode']==1 and 'type mismatch' in txt.lower()
            assert not any(v in txt.lower() for v in ['unknown identifier','unknown module','object file','timeout','unexpected token','unterminated'])
        rows.append(dict(label=row['label'],returncode=row['returncode'],source=row['source'],stdout=row['stdout'],stderr=row['stderr'],source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stream_excerpt=txt))
    negative=dict(status='AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT',author_execution=True,own_execution=False,author_audit=pin(audit_path),rows=rows,pins=pins)
    save(OUT/'negative_controls_read.json',negative)
    history=[]
    for p in sorted((R/'dev_all_positive_weight_order').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351AllPositiveWeightOrder.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=2,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
    docs=[]
    for p in s['documents']:
        if p['path'].endswith('.json'):validate_pin_tree(load(Path(p['path'])),docs)


    # Read every provider statement/line against the pinned source and own copy.
    provider_checks=[]
    for document in s['documents']:
        if not document['path'].endswith('.json'):continue
        jd=load(Path(document['path']))
        for pr in jd.get('providers',[]):
            fp=Path(pr['source']['path']);ck(pr['source'])
            lines=fp.read_text(encoding='utf-8-sig').splitlines()
            stmt=pr['statement'];actual='\n'.join(lines[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
            assert re.sub(r'\s+',' ',actual).startswith(re.sub(r'\s+',' ',stmt)),(pr['name'],pr['line'])
            relative=fp.relative_to(K);own=V/relative
            assert fp.read_bytes()==own.read_bytes(),pr['name']
            provider_checks.append(dict(name=pr['name'],line=pr['line'],statement=stmt,author=pin(fp),own=pin(own),statement_matches=True))
    save(OUT/'provider_checks.json',dict(timestamp=now(),checks=provider_checks))
    # Exact types of the domain and weight, read without reconstructing any old provider.
    domainp=V/'TGLExt/V350DualFixedWeightLaws.lean';domain=domainp.read_text(encoding='utf-8')
    assert 'abbrev PositiveCoreInput' in domain
    excerpts=[]
    for name,lo,hi in [('V350DualFixedWeightLaws.lean',12,18),('V350ScalarDualWeight.lean',13,16),('V350ScalarWeightDomain.lean',43,48),('V350LevelExpectationUniformBound.lean',57,84)]:
        p=V/'TGLExt'/name;ls=p.read_text(encoding='utf-8').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=hi,text='\n'.join(ls[lo-1:hi])))
    save(OUT/'semantic_supplier_excerpts.json',dict(timestamp=now(),records=excerpts))
    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')};objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod);row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            ao=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(ao);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
            assert not parse_axioms('\n'.join(tm))
        for msg in tj['log']:
            if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout);assert set(built)==set(s['modules']+[s['auditor_module']])
    comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=1,private_definitions=0,total_source_theorems_including_private=3,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This independent Lake invocation only; two author DEV rc1 preserved and excluded',
        all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,own_previous_project_objects_reused=True,
        external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,
        package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
        own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
        newly_recompiled_old_supplier_count=0,objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
        type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,
        package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,
        provider_checks=pin(OUT/'provider_checks.json'),semantic_supplier_excerpts=pin(OUT/'semantic_supplier_excerpts.json'),
        history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
        helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — alvo e hipóteses] scalarWeight_right_perturbed_mono_all_squares recebe TODO A do mesmo regularCoreAlgebra P, sem A∈nν. Recebe explicitamente b,c∈scalarPolarRightAlgebra P, b b*≤c c* e comutação de b,c com regularAverage P δ para TODO δ real. A conclusão compara valores em ENNReal do MESMO dualQuadraticIntegral no MESMO regularVacuum P; a definição antiga scalarDualWeight é exatamente essa avaliação. Não há troca para outro peso, ideal uniforme ou GNS.',
      '[REAL — extensão por valores] d_n=1/(n+1)>0 torna T_n=A e_n membro do ideal scalarWeightLeftIdeal pela finitude e pertença fornecidas por scalarDualWeight_square_finite_strong_density. A igualdade (A b)e_n=(A e_n)b usa somente a comutação explícita b e_n=e_n b; idem c. A comparação finita anterior é aplicada a T_n. iSup_le seguido de le_iSup_of_le no MESMO índice transporta a comparação aos supremos, e a recuperação já provada é usada para A b e A c. Não se postula monotonicidade dos quadrados, minorantes positivos finitos de ν, nem valor finito dos supremos. O ramo de convergência forte do fornecedor não é usado como substituto da recuperação de valores.',
      '[REAL — cone inteiro e raiz efetiva] PositiveCoreInput P é o subtipo de operadores do core positivos, sem campo de finitude escalar. O helper privado hilbertPositiveSqrt_core_square trabalha numa Hilbert complexa completa abstrata. vonNeumann_norm_closed fornece fechamento do mesmo subobjeto; cfcₙ_mem com s=N.toStarSubalgebra e 𝕜′=ℂ mantém a raiz no core. hilbertPositiveSqrt continua o wrapper existente de CFC.sqrt; sqrt_eq_real_sqrt, sqrt_nonneg e sqrt_mul_sqrt_self provam exatamente star(sqrt X)*sqrt X=X. Aplicar o primeiro teorema a essa raiz produz o segundo para TODO X≥0, inclusive ν(X)=∞. Não há instalação de uma ordem alternativa nem suposição de CompleteSpace do subtipo N.',
      '[REAL — axiomas, histórico e controle] O auditor próprio imprime os DOIS tipos completos com pp.universes e os axiomas transitivos. O helper privado é compilado e está coberto transitivamente, sem alegar print privado independente. Axiomas permitidos: propext, Classical.choice, Quot.sound, com universos normalizados apenas no parser; os streams brutos permanecem pinados. Duas tentativas DEV rc1 foram relidas e excluídas: SMulMemClass/iSup_le_iSup e coerções, depois StarSubalgebra.coe_mul e aviso de binder. A fonte final usa o subobjeto explícito, iSup_le/le_iSup_of_le e change, maxHeartbeats 1400000. O negativo autoral inverte a conclusão mantendo as hipóteses; o stream acusa Type mismatch com imports resolvidos. Trata-se de controle de aplicação do teorema, não demonstração de falsidade para toda instância especial.',
      '[REAL — fichas] Ficha e adendo de raiz foram lidos por inteiro; os sete e cinco fornecedores tiveram bytes, linha e enunciado confrontados com os arquivos e com as cópias próprias. Registros datados 22:14:00 e 22:15:22 antecedem a primeira tentativa DEV 22:16:43. Reaproveitamento da finitude das médias, ordem finita e recuperação está efetivamente consumido. A aplicação às raízes dos cortes usa fornecedores anteriores para pertença em E e comutação; sua ordem em ε permanece obrigação separada, não antecedente silencioso quitado neste delta.'
    ]
    limits=[
       'Aceite restrito a dois teoremas públicos e um helper privado; nenhuma definição nova.',
       'As hipóteses b,c∈E, b b*≤c c* e comutação com médias permanecem explícitas; não se afirma comparação para b,c arbitrários.',
       'Todos os positivos significa o cone de operadores limitados do mesmo core; valores do peso podem ser infinitos. Não se estende aqui a todos os operadores positivos afiliados não limitados.',
       'Ordem dos reguladores em ε, peso limite perturbado e tracialidade permanecem abertos neste delta; A1(b) não concluído.',
       'Nenhuma execução de monólito, recorder, writer ou memória; controle negativo autoral apenas relido. Nenhum objeto de projeto autoral/DEV utilizado.'
    ]
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=1,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),
        sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,
        all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — ordem do peso em todos os positivos\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Dois teoremas públicos + um helper privado, zero definições. Módulo completo e auditor próprios rc0; dois #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; somente módulo e auditor novos, total '+str(len(objects))+'. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor e '+str(len(sw))+' mensagens históricas de fornecedores separadas no JSON. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, apenas comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores da ficha',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects)),ensure_ascii=False))
if __name__=='__main__':main()

