from review_helpers import *

FINAL_STATUS=STATUS

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==4 and all(t['kind']=='theorem' for t in s['targets'])
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==4 and len(re.findall(r'^private theorem\s+',code,re.M))==1 and len(re.findall(r'^def\s+',code,re.M))==0
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_ESCALA_PESO_LIMITE_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(4,0,1,0)
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
    for p in sorted((R/'dev_inverse_limit_scaling').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351InverseLimitScaling.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,1,1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=3,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
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
    # Read only the already proven interfaces actually used by this delta.
    excerpts=[]
    for relative,lo,hi in [
       ('TGLExt/V351RegularCoreTraceContract.lean',15,19),
       ('TGLExt/V351RegularCoreTraceContract.lean',40,60),
       ('TGLExt/V350DualWeightForm.lean',87,97),
       ('TGLExt/V350RegularDualAction.lean',18,46),
       ('TGLExt/V351InverseGeneratorCutoff.lean',81,95),
       ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',283,297),
       ('.lake/packages/mathlib/Mathlib/Algebra/Order/Archimedean/Basic.lean',211,220),
       ('.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean',807,810)]:
        p=V/relative;ls=p.read_text(encoding='utf-8').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=min(hi,len(ls)),text='\n'.join(ls[lo-1:hi])))
    save(OUT/'semantic_supplier_excerpts.json',dict(timestamp=now(),records=excerpts))
    oldmods={x['module'] for x in s['sources'] if not x['target'] and not x['source_preexisting']}
    assert oldmods=={'TGLExt.V351RegularCoreTraceContract','TGLExt.V350CoreContractCounterexample'}
    old_author_run=R/'existing_contract_dependency_attempts/20260914_225600_779024/run.json'
    oldrun=load(old_author_run);assert oldrun['returncode']==0;validate_pin_tree(oldrun,[])
    old_audits=[]
    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')};objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod);row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            ao=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(ao);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
            assert not parse_axioms('\n'.join(tm))
        if mod in oldmods:
            cp=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(cp);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
            srcp=V/(mod.replace('.','/')+'.lean');st=uncomment(srcp.read_text(encoding='utf-8-sig'))
            ns=re.findall(r'^namespace\s+(\S+)',st,re.M);assert len(ns)==1
            oe={ns[0]+'.'+n for n in re.findall(r'^#print axioms\s+(\S+)',st,re.M)}
            oa=parse_axioms('\n'.join(tm));assert set(oa)==oe and all(set(a)<=ALLOWED for a in oa.values())
            old_audits.append(dict(module=mod,source=pin(srcp),own=pin(p),author_cold=pin(cp),trace=pin(tp),axioms=oa,not_new_results=True))
        for msg in tj['log']:
            if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])|oldmods
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout);assert set(built)==set(s['modules']+[s['auditor_module']])|oldmods
    comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=4,new_theorems=4,new_definitions=0,private_theorems=1,private_definitions=0,total_source_theorems_including_private=5,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This independent Lake invocation only; three author DEV rc1 excluded (one dependency absence, two elaboration); final clean rc0; no author DEV object used',
        all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,own_previous_project_objects_reused=True,
        external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,
        package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
        own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
        newly_recompiled_old_supplier_count=len(oldmods),newly_recompiled_old_suppliers=old_audits,old_supplier_author_run_read_only=pin(old_author_run),objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
        type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,
        package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,
        provider_checks=pin(OUT/'provider_checks.json'),semantic_supplier_excerpts=pin(OUT/'semantic_supplier_excerpts.json'),
        history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
        helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=['[REAL — identidade e contrato] Quatro teoremas públicos e um helper privado, zero definições. O peso é scalarInverseLimitWeight P; a ação sobre o MESMO PositiveCoreInput é TGLV351.positiveDual P, definida no contrato antigo por regularDualAction, cuja coerção é dualAmbient. O tipo final é ∀s X, value(positiveDual P s X)=ofReal(exp(-s))*value(X), exatamente o campo RegularCoreTraceData.dual_scaling ao especializar value:=scalarInverseLimitWeight P. Não foi construído um habitante do contrato, nem recebido outro peso/cone/ação como parâmetro.', '[REAL — raiz e positividade] O helper recebe uma StarAlgEquiv complexa f e f(A)=r•B, com A,B≥0 e r≥0. Mostra que f(sqrt A) e sqrt(r)•sqrt B são positivos e têm o mesmo quadrado; CFC.mul_self_eq_mul_self_iff identifica-os. A raiz é sempre o wrapper antigo hilbertPositiveSqrt=CFC.sqrt, sem definição nova ou inversa. Na aplicação concreta todas essas hipóteses são descarregadas por positividade dos cortes e regularInverseGeneratorCutoff_dual; r=exp(s)>0 e o novo regulador εexp(s)>0. O caso genérico r=0 é permitido pelo helper; não há hipótese de comutação adicional.', '[REAL — sinal da avaliação] scalarInverseCutoffWeight_dual transporta o sanduíche INTEIRO por dualAmbient(-s), usando a invariância da integral original. O input dualAmbient(s)X retorna a X por simetria da mesma StarAlgEquiv. Cada raiz recebe sqrt(exp(-s)); estrela conjuga esse escalar REAL sem trocar seu valor. As duas raízes produzem exp(-s), e a homogeneidade da mesma dualQuadraticIntegral fornece Wε(θ_sX)=ofReal(exp(-s))*W_(εexp(-s))(X). Não há substituição de invariância por tracialidade nem uso de domínio GNS/valor finito.', '[REAL — cofinalidade e supremos] Para r>0, o lema escalado prova as duas desigualdades. Para cada n escolhe m com 1/(m+1)<r/(n+1); no sentido inverso escolhe 1/(m+1)<[1/(n+1)]/r, obtendo r/(m+1)≤1/(n+1). A antitonia já entregue e le_iSup_of_le dão igualdade dos supremos; não se afirma uma bijeção dos índices ou comutação indevida de limites. O último teorema usa r=exp(-s), a identidade aritmética (1/(n+1))*r=r/(n+1), e ENNReal.mul_iSup. Valores infinitos permanecem cobertos, sem toReal/cancelamento de infinito.', '[REAL — fontes antigas e cronologia] V351RegularCoreTraceContract e V350CoreContractCounterexample foram copiados das fontes OLD/kernel após comparação byte a byte com K, e compilados por este Lake próprio; nenhum objeto foi herdado do autor. São dois fornecedores ANTIGOS, separados dos quatro alvos novos. O contrato antigo continua recusando o traço zero e ν como fornecedor direto; sua recompilação não declara traço novo. A ficha 22:53:53 antecede o primeiro DEV. O adendo 22:59:23 é POSTERIOR ao DEV final 22:58:45 e registra a reprodução antiga 22:56:00, não se apresenta como busca pré-código. Doze entradas de fornecedores foram confrontadas por nomes, linhas, enunciados e pins.', '[REAL — histórico e negativo] Três DEV rc1 foram relidos e excluídos: 22:55:10 falhou na carga de objeto ausente, 22:56:43 teve coerções/recursão de simp e 22:57:46 ainda recursão de simp. Nenhum print parcial dessas falhas autoriza a prova. O final 22:58:45 é rc0 sem avisos. Pins históricos usam os snapshots reais, mantendo o path antigo apenas como localização textual. O negativo autoral substitui exp(-s) por exp(s) e falha por Type mismatch, não por ambiente; foi relido/pinado, não reexecutado. O módulo completo e auditor4 próprios passaram; o helper é coberto pelos axiomas transitivos públicos, e os 14 prints dos dois fornecedores antigos também foram conferidos separadamente.']
    limits=['Aceite exclusivo de quatro teoremas públicos e um helper privado; duas fontes antigas reproduzidas não aumentam essa contagem.', 'ε>0 nos dois alvos de corte; r>0 na cofinalidade; o alvo final cobre todo s real e todo X:PositiveCoreInput P, inclusive peso infinito.', 'Paga a escala dual do mesmo candidato ao campo exato do contrato. Semifinitude e tracialidade permanecem OPEN; não há habitante final de RegularCoreTraceData nem promoção de A1(b)/gate.', 'Os 22/23 e todos os anteriores permaneceram intactos. Consultas de semifinitude não são provas adicionais deste delta.', 'Cache de pacotes e objetos próprios anteriores reutilizados; nenhum objeto de projeto autoral/DEV, monólito, writer, recorder ou memória executado/modificado.']
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=4,new_theorems=4,new_definitions=0,private_theorems=1,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),
        sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,
        all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — escala dual do peso limite\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Quatro teoremas públicos + um helper privado, zero definições. Módulo completo e auditor próprios rc0; quatro #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; construídos alvo, auditor e dois fornecedores antigos, total '+str(len(objects))+'. Dois fornecedores antigos reproduzidos de fonte; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor e '+str(len(sw))+' mensagens de fornecedores com origem separada no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, apenas comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores da ficha',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects)),ensure_ascii=False))
if __name__=='__main__':main()

