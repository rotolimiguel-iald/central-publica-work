from review_helpers import *

FINAL_STATUS=STATUS

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==15 and sum(t['kind']=='theorem' for t in s['targets'])==13 and sum(t['kind']=='def' for t in s['targets'])==2
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==13 and len(re.findall(r'^private theorem\s+',code,re.M))==0 and len(re.findall(r'^def\s+',code,re.M))==2
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=False))

    audit_path=R/'AUDITORIA_LEIS_PESO_LIMITE_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(13,2,0,0)
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
    for p in sorted((R/'dev_inverse_limit_weight').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351InverseLimitWeight.lean')
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
    # Read only the already proven interfaces actually used by this delta.
    excerpts=[]
    for relative,lo,hi in [
       ('TGLExt/V350DualFormNormality.lean',13,48),
       ('TGLExt/V350RegularNormality.lean',50,70),
       ('TGLExt/V350DualFixedWeightLaws.lean',116,123),
       ('.lake/packages/mathlib/Mathlib/Data/ENNReal/Operations.lean',686,689),
       ('.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean',803,809)]:
        p=V/relative;ls=p.read_text(encoding='utf-8').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=min(hi,len(ls)),text='\n'.join(ls[lo-1:hi])))
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
        exact_target_count=15,new_theorems=13,new_definitions=2,private_theorems=0,private_definitions=0,total_source_theorems_including_private=13,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This independent Lake invocation only; two author DEV rc1 excluded; final DEV rc0 read only; no author DEV object used',
        all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=False,own_previous_project_objects_reused=True,
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
    paragraphs=['[REAL — objetos e domínio] As duas definições usam o mesmo PositiveCoreInput P, hilbertPositiveSqrt(Bε), dualQuadraticIntegral e regularVacuum P. Wε(X)=ν(sε* X sε) e o candidato limite é sup_n W_(1/(n+1))(X). O domínio é o cone positivo limitado do core; não exige finitude do valor. A expressão é definida para todo ε real, mas a interpretação como corte inverso positivo e a ordem entre reguladores usam ε>0. Não se afirma que os cortes são fixos pela ação dual; PositiveCoreInput.conjugate, restrito ao core fixo, não é aplicado indevidamente.', '[REAL — leis dos cortes] Zero, aditividade, homogeneidade por r:NNReal e monotonia em X são transportadas das leis integrais existentes. A positividade de star b X b e a ordem sob conjugador FIXO vêm das leis de estrela. Não se deduz ordem de sanduíches a partir da ordem de conjugadores. Todos os valores são ENNReal; não se elimina infinito nem se divide por um valor de peso.', '[REAL — normalidade] Para qualquer universo do índice ι, com Preorder, IsDirectedOrder e Nonempty, A é uma rede crescente de positivos no core e S seu supremo INTERNO limitado. A cota ||A_i||≤||S|| é deduzida. vonNeumann_exists_positive_isLUB constrói um limite forte D no core; unicidade do supremo dá D=S. A continuidade do CLM star b produz o limite forte dos sanduíches em todos os vetores, que alimenta a normalidade integral antiga. Não se recebe continuidade forte como premissa nem se pressupõe que conjugação preserve supremos internos.', '[REAL — limite comum] A antitonia em ε é o alvo já entregue do módulo21. Para n≤m, 1/(m+1)≤1/(n+1), logo as avaliações crescem. ENNReal.iSup_add_iSup_of_monotone é usado nas DUAS famílias com o mesmo índice natural; não se aplica a igualdade falsa entre soma de supremos e supremo diagonal para famílias arbitrárias. Homogeneidade usa mul_iSup (inclusive zero e infinito), monotonia usa le_iSup no mesmo índice. A normalidade final troca os supremos n/i por iSup_comm, após a normalidade de cada corte. Não é argumento de convergência sequencial que restrinja a rede A a índices contáveis.', '[REAL — documentos e evidências] Ficha 22:30:29 e adendo 22:31:48 foram lidos integralmente antes da conclusão desta revisão; ambos precedem o primeiro DEV 22:33:31. Nove fornecedores mais cinco do adendo foram confrontados com suas fontes, linhas, tipos, hashes e cópias próprias. Módulo e auditor independentes passaram; os 15 tipos com universos e respectivos axiomas foram lidos e reparsados. Não há helpers privados, sorry, axioma novo, native_decide ou trustCompiler.', '[REAL — histórico e negativo] Duas tentativas autorais rc1 (22:33:31 e 22:35:54) ficam excluídas, mesmo que tenham prints parciais. Seus pins apontam a snapshots históricos reais, nunca à fonte viva. A final 22:36:37 está rc0. O negativo autoral substitui a soma por produto na conclusão de scalarInverseLimitWeight_add e é recusado por Type mismatch, com imports resolvidos. Fonte e streams desse controle foram relidos e pinados; nenhum controle autoral foi executado nesta revisão.']
    limits=['Aceite exclusivo de 15 declarações: 13 teoremas e duas definições, zero privados.', 'Normalidade provada para redes positivas crescentes, dirigidas e não vazias, com supremo interno no core; não afirma completude do cone de afiliados nem cobertura de todo predual.', 'Fidelidade, semifinitude, tracialidade e escala dual deste peso limite permanecem OPEN neste delta. A consulta anterior é proposta independente, não prova Lean desses campos.', 'Nenhum novo GNS, gap, minorantes positivos finitos de ν ou promoção de A1(b)/gate. O módulo23 é separado e não está aceito por este relatório.', 'Reuso apenas de objetos próprios anteriores e cache de pacotes pinado. Nenhum objeto autoral/DEV, monólito, recorder, writer ou memória executado/modificado.']
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=15,new_theorems=13,new_definitions=2,private_theorems=0,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),
        sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,
        all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — leis do peso limite\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Treze teoremas públicos + duas definições, zero privados. Módulo completo e auditor próprios rc0; quinze #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; somente módulo e auditor novos, total '+str(len(objects))+'. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor e '+str(len(sw))+' mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, apenas comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores da ficha',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects)),ensure_ascii=False))
if __name__=='__main__':main()

