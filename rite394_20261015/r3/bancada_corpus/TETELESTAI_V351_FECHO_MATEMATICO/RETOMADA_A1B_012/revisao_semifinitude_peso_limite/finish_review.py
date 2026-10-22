from review_helpers import *

def save(p,x):
    if p.exists():
        old=load(p)
        assert {k:v for k,v in old.items() if k!='timestamp'}=={k:v for k,v in x.items() if k!='timestamp'}, ('refuse changed retry',str(p))
        return
    fresh(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())

OLD_MODS={'TGLExt.V350FixedBaseEquivalence','TGLExt.V351ExtendedBaseDualWeight',
          'TGLExt.V351ScalarWeightSemifiniteness'}

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==3 and all(t['kind']=='theorem' for t in s['targets'])
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==3
    assert len(re.findall(r'^private theorem\s+',code,re.M))==1
    assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name]
        assert len(ts)==1;(types.update({name:ts[0]}))
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),
        all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B.json';author=load(audit_path);pins=[]
    validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected
    assert author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(3,0,1,0)
    br=load(Path(author['positive_build']['path']));assert br['returncode']==0;validate_pin_tree(br,pins)
    assert len(author['commands'])==2;rows=[]
    for i,row in enumerate(author['commands']):
        txt=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
        if i==0:
            aa=parse_axioms(txt)
            assert row['returncode']==0 and set(aa)==expected and all(set(v)<=ALLOWED for v in aa.values())
        else:
            assert row['returncode']==1 and 'type mismatch' in txt.lower()
            assert not any(v in txt.lower() for v in ['unknown identifier','unknown module','object file','timeout','unexpected token','unterminated'])
        rows.append(dict(label=row['label'],returncode=row['returncode'],source=row['source'],
            stdout=row['stdout'],stderr=row['stderr'],source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stream_excerpt=txt))
    negative=dict(status='AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT',
        author_execution=True,own_execution=False,author_audit=pin(audit_path),rows=rows,pins=pins)
    save(OUT/'negative_controls_read.json',negative)

    history=[]
    for p in sorted((R/'dev_inverse_limit_semifinite').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351InverseLimitSemifiniteness.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],
            stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],
            accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',
            diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,1,1,1,0]
    assert history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=4,
        excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))

    docs=[];provider_checks=[]
    for document in s['documents']:
        if not document['path'].endswith('.json'):continue
        jd=load(Path(document['path']));validate_pin_tree(jd,docs)
        for pr in jd.get('providers',[]):
            fp=Path(pr['source']['path']);ck(pr['source'])
            lines=fp.read_text(encoding='utf-8-sig').splitlines();stmt=pr.get('statement',pr.get('excerpt'))
            assert stmt
            actual='\n'.join(lines[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
            assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr['name']
            own=V/fp.relative_to(K);assert fp.read_bytes()==own.read_bytes(),pr['name']
            provider_checks.append(dict(name=pr['name'],line=pr['line'],statement=stmt,
                author=pin(fp),own=pin(own),statement_matches=True))
    assert len(provider_checks)==7
    save(OUT/'provider_checks.json',dict(timestamp=now(),checks=provider_checks))
    oldmods={x['module'] for x in s['sources'] if not x['target'] and not x['source_preexisting']}
    assert oldmods==OLD_MODS
    old_source_origins=[]
    for x in s['sources']:
        if x['module'] not in oldmods:continue
        rel=Path(x['module'].replace('.','/')+'.lean');op=OLD/rel;kp=K/rel;vp=V/rel
        assert op.read_bytes()==kp.read_bytes()==vp.read_bytes()
        old_source_origins.append(dict(module=x['module'],old_source=pin(op),author_source=pin(kp),own_source=pin(vp),all_three_equal=True))
    erp=R/'existing_semifinite_dependency_attempts/20260914_231037_491709/run.json'
    er=load(erp);assert er['returncode']==0;ep=[];validate_pin_tree(er,ep)
    etxt=Path(er['stdout']['path']).read_text(encoding='utf8')
    assert set(re.findall(r'\bBuilt\s+([^\s(]+)',etxt))==OLD_MODS
    eaxioms=parse_axioms(re.sub(r'^info:.*?\.lean:\d+:\d+:\s*', '', etxt, flags=re.M))
    save(OUT/'old_suppliers_read_v2.json',dict(timestamp=now(),origins=old_source_origins,
        author_run=pin(erp),author_stream_pins=[er['stdout'],er['stderr']],author_active_pins=ep,
        author_built_modules=sorted(OLD_MODS),author_printed_axioms=eaxioms,
        scope='Three existing providers, OLD source equal to K and V. Independent objects below, not author objects.'))

    excerpts=[]
    for relative,lo,hi in [
        ('TGLExt/V351PerturbedWeightOrder.lean',10,51),
        ('TGLExt/V351InverseLimitWeight.lean',16,20),
        ('TGLExt/V351InverseLimitWeight.lean',87,98),
        ('TGLExt/V351RegularDomainCut.lean',62,105),
        ('TGLExt/V351RegularDomainCut.lean',110,165),
        ('TGLExt/V351ScalarWeightSemifiniteness.lean',12,32),
        ('TGLExt/V351RegularCoreTraceContract.lean',17,58),
        ('TGLExt/V350ScalarWeightDomain.lean',12,105)]:
        p=V/relative;ls=p.read_text(encoding='utf-8-sig').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=min(hi,len(ls)),text='\n'.join(ls[lo-1:hi])))
    save(OUT/'semantic_supplier_excerpts.json',dict(timestamp=now(),records=excerpts))

    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
    objects=[];old_audits=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod)
        row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in set(s['modules'])|oldmods:
            cp=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(cp);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
        if mod in s['modules']:assert not parse_axioms('\n'.join(tm))
        if mod in oldmods:
            st=uncomment(Path(row['source']['path']).read_text(encoding='utf-8-sig'))
            ns=re.findall(r'^namespace\s+(\S+)',st,re.M);assert len(ns)==1
            oe={ns[0]+'.'+n for n in re.findall(r'^#print axioms\s+(\S+)',st,re.M)}
            oa=parse_axioms('\n'.join(tm))
            assert set(oa)==oe and all(set(v)<=ALLOWED for v in oa.values())
            assert all(eaxioms[n]==v for n,v in oa.items())
            old_audits.append(dict(module=mod,source=row['source'],own=pin(p),author_cold=row['author_cold'],
                equal_author_cold=row['equal_author_cold'],trace=pin(tp),axioms=oa,not_new_results=True))
        for msg in tj['log']:
            if msg['level']=='warning':
                (tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])|oldmods
    assert sum(len(x['axioms']) for x in old_audits)==21
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
    assert set(built)==set(s['modules']+[s['auditor_module']])|oldmods
    comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,
        P0=[],P1=[],P2=[],findings=[],exact_target_count=3,new_theorems=3,new_definitions=0,
        private_theorems=1,private_definitions=0,total_source_theorems_including_private=4,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,
        all_attempts_scope='This independent Lake invocation only; four author DEV rc1 attempts excluded; final author DEV and standalone rc0; no author/DEV objects used',
        all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,
        own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,
        package_cache_inherited=True,package_cache_not_rebuilt=True,
        package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),
        base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),
        own_project_object_count_after=len(objects),new_project_object_count=len(new),
        newly_recompiled_old_supplier_count=len(oldmods),newly_recompiled_old_suppliers=old_audits,
        newly_recompiled_old_print_count=sum(len(x['axioms']) for x in old_audits),
        old_supplier_source_origins=old_source_origins,old_suppliers_evidence=pin(OUT/'old_suppliers_read_v2.json'),
        objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
        type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,
        supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,built_log_entries=built,
        protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,
        provider_checks=pin(OUT/'provider_checks.json'),semantic_supplier_excerpts=pin(OUT/'semantic_supplier_excerpts.json'),
        history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
        helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']]+[pin(p) for p in sorted(OUT.glob('finish_review.py.bak_*'))],
        preparation_correction=pin(OUT/'finalizer_parser_correction.json'))
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — tipos e objeto] Três teoremas públicos, nenhum def novo. O domínio inicial é a : scalarWeightLeftIdeal P do MESMO ν; δ>0 é explícito. A primeira conclusão avalia scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) e fornece a cota ENNReal.ofReal(δ⁻¹)·ν(a*a), uniforme no regulador ε da definição do limite. A segunda conclui <⊤. A terceira identifica o fecho WOT do conjunto de operadores de N com quadrado finito para esse MESMO peso limite com N inteiro, sem antecedente extra sobre P.',
      '[REAL — ordem correta] Para cada ε=1/(n+1), s é a raiz ORIGINAL hilbertPositiveSqrt(Bε), q=qδ e b=q s. A pertença b∈E usa as pertenças já provadas de q e s, e c=√(δ⁻¹)I também pertence a E. O cálculo é bb*=q(ss*)q=q Bε q=Bε q²≤δ⁻¹I=cc*. Usa apenas q auto-adjunto e sua comutação com Bε; não comuta a com q ou s, não supõe comutação de a com Bε e nem necessita provar q s=s q neste argumento. scalarWeight_right_perturbed_mono recebe precisamente bb*≤cc* e a∈nν. A desigualdade de pesos não é inferida por ordem falsa dos sanduíches.',
      '[REAL — supremum, finitude e Haar] A igualdade entre o corte do quadrado de aq e ν(b* a*a b) é associatividade/estrela no CLM, transportada por congrArg explícito de dualQuadraticIntegral. Para c, homogeneidade existente e δ>0 dão o fator real δ⁻¹; ←Complex.ofReal_inv resolve a coerção, sem trocar ℝ por uma ordem complexa indevida. A cota é independente de n, logo iSup_le a passa ao limite. ENNReal.mul_lt_top consome ofReal finito e a.property; não converte valor infinito com toReal. Mesmo dualQuadraticIntegral, regularVacuum e normalização Haar herdados, sem redefinição ou fator novo.',
      '[REAL — densidade WOT e não circularidade] Para cada a∈nν, aq_(1/(n+1)) pertence ao conjunto square-finite de τ pela segunda conclusão e converge fortemente a a pelo teorema de q_n já entregue; a multiplicação à esquerda usa apenas continuidade do CLM fixo a. strong_tendsto_wot e mem_closure_of_tendsto colocam todo nν no fecho WOT desse conjunto. closure_mono, o ANTIGO scalarWeight_square_finite_wot_closure de ν e closure_closure dão N⊆fecho. O sentido contrário usa somente a WOT-fechadura de N. Não se pressupõe semifinitude de τ, não se identifica nτ com nν e não se postula uma família de minorantes positivos finitos de ν.',
      '[REAL — auxiliar e fornecedores antigos] O único helper privado hilbert_sqrt_mul_star é genérico em Hilbert complexo completo e consome CFC.sqrt_nonneg/sqrt_mul_sqrt_self para ss*=B. Seus axiomas são auditados transitivamente pelas três conclusões. V350FixedBaseEquivalence, V351ExtendedBaseDualWeight e V351ScalarWeightSemifiniteness foram copiados de OLD/kernel após igualdade de bytes OLD=K; construídos do fonte em V, com 5+14+2 prints antigos, todos permitidos. São três fornecedores adicionais, não novos resultados. Não se instalou objeto autoral ou DEV nem se refez o GNS.',
      '[REAL — ficha e histórico] Ficha 23:10:26 antecede a primeira tentativa e reutiliza a busca de seis modalidades da ficha25, cujo consumidor já era a densidade do domínio de τ. As sete entradas de fornecedores foram verificadas por linha, enunciado e hash. O adendo 23:14:09 documenta a reprodução antiga já feita e é posterior ao primeiro DEV; não foi apresentado aqui como anterior a todo código. Quatro DEV rc1 foram preservados/excluídos: congr1/timeout, tentativa instrumentada, homogeneidade/isDefEq e cast de inverso complexo; o final 23:20:29 passou limpo. Os pins históricos apontam a snapshots reais, com localização viva apenas como texto. A auditoria autoral standalone rc0 e a recusa Type mismatch do negativo BadLimitSemifiniteInfiniteCut foram relidas/pinadas, sem reexecutar o negativo.'
    ]
    limits=[
      'Aceite26: três teoremas públicos, um helper privado transitivo, zero definições; os três fornecedores antigos e seus 21 prints são contados separadamente.',
      'P é o mesmo SiteProfile; δ>0 e a∈nν são hipóteses da estimativa/finitude, descarregadas na sequência usada para a densidade. A cota depende de δ, não de ε; não se afirma finitude de τ(a*a) para todo a∈nν.',
      'Com as leis de peso/normalidade anteriormente aceitas, o fecho WOT aqui provado é o critério usual de semifinitude do MESMO scalarInverseLimitWeight. Não é prova de tracialidade nem do campo finite-positive-minorants de RegularCoreTraceData; não é entrega do traço completo A1(b).',
      'Nenhuma afirmação de convergência em norma de operadores, gap, novo GNS, igualdade de domínios algébricos ou núcleo analítico inteiro. Não foram examinadas novas rotas de tracialidade nesta revisão.',
      'Somente V e esta pasta de revisão receberam novas saídas. K, OLD, pareceres/pins anteriores, memórias, writers e monólito preservados; pacote Mathlib e objetos próprios anteriores herdados com limites explícitos.'
    ]
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,
        P0=[],P1=[],P2=[],findings=[],exact_target_count=3,new_theorems=3,new_definitions=0,private_theorems=1,private_definitions=0,
        run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],
        semantic_review=paragraphs,limits=limits,negative_controls=negative,all_prior_pins_preserved=True,
        usual_semifiniteness_same_limit_weight=True,trace_constructed=False,finite_positive_minorants_proved=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Três teoremas públicos + um helper privado; módulo completo e auditor próprios rc0. Três #check com universos e axiomas exclusivamente do trio permitido. Aceite limitado aos tipos efetivamente verificados.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; '+str(len(new))+' novos objetos construídos (três fornecedores antigos + alvo + auditor), total '+str(len(objects))+'. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor, '+str(len(sw))+' mensagens de fornecedores com origem separada no JSON. Traces de compilação restringem LEAN_PATH a V e seus pacotes. Cache de pacotes pinado/herdado; quantidade total de jobs do Lake não é quantidade de recompilações. Stderr completo preservado, inclusive aviso herdado do pacote aesop, se presente.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone (só comparação) | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida do alvo: '+str(obj['equal_author_cold'])+'.\n\n'
    md+='| Fornecedor antigo | Igualdade fonte OLD=K=V | .olean próprio = autoral |\n|---|---|---|\n'
    for x in old_audits:md+='| '+x['module']+' | True | '+str(x['equal_author_cold'])+' |\n'
    md+='\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores',comp['old_suppliers_evidence'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,
        checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,
        P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects),old_suppliers=len(oldmods)),ensure_ascii=False))

if __name__=='__main__':main()
