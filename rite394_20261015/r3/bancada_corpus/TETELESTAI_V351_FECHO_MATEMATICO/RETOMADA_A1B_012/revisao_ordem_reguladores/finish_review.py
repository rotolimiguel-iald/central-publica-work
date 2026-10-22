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
    assert len(re.findall(r'^theorem\s+',code,re.M))==4 and len(re.findall(r'^private theorem\s+',code,re.M))==2
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_ORDEM_REGULADORES_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(4,0,2,0)
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
    for p in sorted((R/'dev_regulator_weight_order').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351RegulatorWeightOrder.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[0] and history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=0,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
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
       ('TGLExt/V351InverseGeneratorCutoff.lean',50,80),
       ('TGLExt/V351InverseGeneratorCutoff.lean',99,135),
       ('TGLExt/V351AllPositiveWeightOrder.lean',73,93),
       ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',346,355)]:
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
        exact_target_count=4,new_theorems=4,new_definitions=0,private_theorems=2,private_definitions=0,total_source_theorems_including_private=6,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This independent Lake invocation only; author DEV first attempt rc0 read only; no author DEV object used',
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
       '[REAL — objetos e comutação] Quatro teoremas públicos e dois helpers privados, zero definições. A identificação já paga Bε=cfc(Fε)(R), com ε>0, é usada para os DOIS cortes do MESMO regularSpectralResolvent P. cfc_commute_cfc fornece comutação de funções desse único operador. Não há outro h, inverso, raiz, realização espectral ou hipótese de comutação recebida pelo novo teorema.',
       '[REAL — identidade e domínio] Para todo vetor x do Hilbert regular, graph coloca (Bεx,x−εBεx) no grafo do mesmo regularPositiveGenerator P. graph_iff com η implica Bη(x−εBεx+ηBεx)=Bεx. Linearidade, extensionalidade e abel dão exatamente Bε−Bη=(η−ε)•(BηBε). Não se divide por η−ε, logo ε=η está incluído; não se aplica h a vetor fora de seu domínio nem se pressupõe h limitado/inversível com gap.',
       '[REAL — antitonia] O helper hilbert_commuting_positive_product é genérico numa Hilbert complexa completa e consome Commute.mul_nonneg. Bη,Bε são positivos e sua comutação vem do primeiro alvo. A diferença é positiva porque η−ε≥0: a passagem pela positividade dos CLM e IsPositive.smul_of_nonneg conserva o coeficiente REAL embutido em ℂ, com exact_mod_cast. Assim 0<ε≤η implica Bη≤Bε. Não se usa produto positivo de operadores não comutantes nem uma hipótese de ordem disfarçada como conclusão.',
       '[REAL — peso em todo positivo] O último alvo usa b=sqrt(Bη), c=sqrt(Bε), sempre o wrapper antigo hilbertPositiveSqrt. O segundo helper prova b b*=Bη e c c*=Bε por positividade/auto-adjunção da raiz e sqrt_mul_sqrt_self. A pertença dessas raízes em E e no core, e a comutação com TODAS as médias, são descarregadas pelos fornecedores já provados. scalarWeight_right_perturbed_mono_all_positive recebe então a ordem b b*≤c c* e entrega νη(X)≤νε(X) para TODO X:PositiveCoreInput P, inclusive valores infinitos. Não resta hipótese A∈nν, comutação ou pertença em E no tipo público final. Isso compara avaliações do peso, não afirma sη X sη≤sε X sε.',
       '[REAL — proveniência documental e autoria] Ficha 22:22:49 e adendo 22:23:56 foram lidos integralmente e antecedem o primeiro DEV 22:25:47. Oito fornecedores da ficha e três do adendo foram confrontados por bytes, nomes, linhas e enunciados com K e V. A identidade pelo grafo é escolha e construção do agente principal, registrada com consumidor para produtos dos cortes; a consulta independente comparou alternativas e não é alegada como origem da prova. A rota CFC real alternativa não foi recodificada.',
       '[REAL — axiomas e controle] Módulo completo e auditor próprios passaram. Quatro tipos com universos e prints transitivos contêm somente propext, Classical.choice e Quot.sound; universos são normalizados no parser, sem alterar streams. Os dois helpers foram lidos e compilados, cobertos transitivamente pelos alvos públicos, sem print privado separado. O único DEV localizado é rc0 sem avisos; não se importou seu objeto. O negativo autoral mantém 0<ε≤η e tenta usar o teorema na ordem inversa; falha por Type mismatch com imports resolvidos. Controle relido, não reexecutado; não é prova de desigualdade estrita, e a igualdade ε=η permanece possível.'
    ]
    limits=[
       'Aceite restrito a quatro teoremas públicos mais dois helpers privados, sem nova definição.',
       'ε>0 e η>0 são hipóteses explícitas; ε≤η é necessária para as duas conclusões de ordem. Não se cobre ε=0.',
       'X pertence ao cone positivo LIMITADO do mesmo core, sem restrição de finitude do peso; não se amplia aqui o domínio para todos os afiliados não limitados.',
       'Não foi definido peso limite nem provadas suas leis/semifinitude/tracialidade. A1(b) e gate permanecem sem promoção.',
       'Nenhum objeto autoral/DEV utilizado, nenhum monólito/recorder/writer ou memória executado/modificado; controle negativo autoral somente relido.'
    ]
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=4,new_theorems=4,new_definitions=0,private_theorems=2,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),
        sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,
        all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — ordem dos reguladores e dos pesos\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Quatro teoremas públicos + dois helpers privados, zero definições. Módulo completo e auditor próprios rc0; quatro #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; somente módulo e auditor novos, total '+str(len(objects))+'. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor e '+str(len(sw))+' mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, apenas comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores da ficha',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects)),ensure_ascii=False))
if __name__=='__main__':main()

