from review_helpers import *

def save(p,x):
    if p.exists():
        old=load(p)
        assert {k:v for k,v in old.items() if k!='timestamp'}=={k:v for k,v in x.items() if k!='timestamp'}, ('changed retry',str(p))
        return
    fresh(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())

def main():
    ptr=load(OUT/'SNAPSHOT_POINTER.json');ck(ptr['snapshot'])
    a=Path(ptr['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target'])
    expected={x['name'] for x in s['targets']}
    assert len(expected)==4 and all(t['kind']=='theorem' for t in s['targets'])
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==4
    assert len(re.findall(r'^private theorem\s+',code,re.M))==2
    assert not re.findall(r'^(?:private |noncomputable )*def\s+',code,re.M)
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code)
    tp,tj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values())
    types={}
    for n in expected:
        z=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==n]
        assert len(z)==1,(n,z);types[n]=z[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(tp),
         all_axioms_allowed=True,private_helpers_audited_transitively=True,universes_normalized_for_axiom_comparison_only=True))

    audit_path=R/'AUDITORIA_EXTENSAO_TRACIAL_A1B.json';author=load(audit_path);authorpins=[]
    validate_pin_tree(author,authorpins)
    assert {t['name'] for t in author['targets']}==expected
    assert author['modules'][0]['source']==target['original']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(4,0,2,0)
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert not author['core_traciality_proved'] and not author['full_trace_constructed']
    br=load(Path(author['positive_build']['path']));validate_pin_tree(br,authorpins)
    assert br['returncode']==0 and br['sources_unchanged_during_build']
    rows=[]
    for i,row in enumerate(author['commands']):
        txt=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
        if i==0:
            aa=parse_axioms(txt);assert row['returncode']==0 and set(aa)==expected
            assert all(set(v)<=ALLOWED for v in aa.values())
        else:
            assert row['returncode']==1 and 'type mismatch' in txt.lower()
            assert not any(q in txt.lower() for q in ['unknown identifier','unknown module','object file','timeout','unexpected token','unterminated'])
        rows.append(dict(label=row['label'],returncode=row['returncode'],source=row['source'],
             source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),
             stdout=row['stdout'],stderr=row['stderr'],stream_excerpt=txt))
    assert len(rows)==2 and rows[1]['label']=='BadTracialCorePremiseRemoved'
    negative=dict(status='AUTHOR_NEGATIVE_READ_HASH_VERIFIED__TYPE_MISMATCH',own_execution=False,
        author_execution=True,author_audit=pin(audit_path),rows=rows,pins=authorpins,
        meaning='Deleting the core hypothesis is rejected; this is not a proof of core traciality or of its impossibility.')
    save(OUT/'negative_controls_read.json',negative)

    history=[]
    for p in sorted((R/'dev_tracial_extension').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351InverseLimitTracialExtension.lean')
        assert (sp['bytes'],sp['sha256'])==(j['source']['bytes'],j['source']['sha256'])
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],
            stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],
            used_as_own_build_evidence=False,dev_object_imported=False,
            diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,0]
    assert history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=1,
         excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))

    docs=[];checks=[];consumer=None
    for d in s['documents']:
        if not d['path'].endswith('.json'):continue
        jd=load(Path(d['path']));validate_pin_tree(jd,docs)
        for pr in jd.get('providers',[]):
            fp=Path(pr['source']['path']);ck(pr['source']);lines=fp.read_text(encoding='utf-8-sig').splitlines()
            stmt=pr.get('statement',pr.get('excerpt'));assert stmt
            actual='\n'.join(lines[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
            assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr['name']
            own=V/fp.relative_to(K);assert own.read_bytes()==fp.read_bytes()
            # Include surrounding complete source, avoiding pretending a prefix is a complete type.
            extra='\n'.join(lines[pr['line']-1:pr['line']+15])
            checks.append(dict(name=pr['name'],line=pr['line'],documented_prefix=stmt,
              source_excerpt=extra,author=pin(fp),own=pin(own),prefix_matches=True))
        if isinstance(jd.get('consumer'),dict) and 'source' in jd['consumer']:
            c=jd['consumer'];ck(c['source'])
            actual=Path(c['source']['path']).read_text(encoding='utf-8-sig').splitlines()[c['line']-1]
            assert actual==c['statement'];consumer=c
    assert len(checks)==11 and consumer is not None
    save(OUT/'provider_checks.json',dict(timestamp=now(),checks=checks,consumer=consumer,
        chronology='Fiche before code; addendum explicitly after first DEV, before acceptance. Original line59 corrected to line58 in addendum.',
        incomplete_documentary_prefix='The mathlib norm_le_one_iff_of_nonneg excerpt was truncated at an optional binder. Full local statement including := by cfc_tac read; no mathematical mismatch.'))
    oldmods={x['module'] for x in s['sources'] if not x['target'] and not x['source_preexisting']}
    assert not oldmods

    excerpts=[]
    for rel,lo,hi in [
        ('TGLExt/V350DualCutNormality.lean',49,59),
        ('TGLExt/V350DualWeightForm.lean',14,22),
        ('TGLExt/V350DualWeightForm.lean',40,67),
        ('TGLExt/V350ScalarRightAverage.lean',70,79),
        ('TGLExt/V351InverseLimitWeight.lean',87,115),
        ('TGLExt/V350FiniteDualStarCore.lean',16,25),
        ('TGLExt/V350FiniteDualStarCore.lean',47,75),
        ('TGLExt/V350FiniteDualStarCore.lean',94,122),
        ('TGLExt/V351RegularCoreTraceContract.lean',43,60),
        ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean',245,248)]:
        p=V/rel;lines=p.read_text(encoding='utf-8-sig').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=hi,text='\n'.join(lines[lo-1:hi])))
    save(OUT/'semantic_supplier_excerpts.json',dict(timestamp=now(),records=excerpts))

    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
    objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tr,j,mi=trace(mod)
        row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tr),
             own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            cp=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(cp);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
        for msg in j['log']:
            if msg['level']=='warning':
                (tw if mod in s['modules']+[s['auditor_module']] else sw).append(
                    dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8')
    stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
    assert set(built)==set(s['modules']+[s['auditor_module']])
    authorhelpers=[pin(R/n) for n in ['run_tracial_extension_replay.py','audit_tracial_extension.py','validate_tracial_extension.py']]
    save(OUT/'author_helpers_read.json',dict(timestamp=now(),sourcepins=authorhelpers,executed_by_reviewer=False,
       observations=['Replay reads existing source pins, clears LEAN_PATH and builds in K; not invoked here.',
       'Audit matches the four public targets, excludes forbidden proof terms and requires a genuine Type mismatch from the negative.',
       'Validator sequences author builds and audit; not a supplier of the mathematical premise.']))
    comp=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,
       P0=[],P1=[],P2=[],findings=[],exact_target_count=4,new_theorems=4,new_definitions=0,
       private_theorems=2,private_definitions=0,total_source_theorems_including_private=6,
       all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,
       all_attempts_scope='This independent Lake invocation only. One author DEV rc1 rejected; final DEV and standalone rc0. No author/DEV objects used.',
       all_axioms_allowed=True,all_target_typechecks_present=True,private_helpers_audited_transitively=True,
       own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,
       package_cache_inherited=True,package_cache_not_rebuilt=True,
       package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),
       base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),
       own_project_object_count_after=len(objects),new_project_object_count=len(new),
       newly_recompiled_old_supplier_count=0,newly_recompiled_old_suppliers=[],newly_recompiled_old_print_count=0,
       objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
       type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,
       supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,built_log_entries=built,
       protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,
       provider_checks=pin(OUT/'provider_checks.json'),semantic_supplier_excerpts=pin(OUT/'semantic_supplier_excerpts.json'),
       history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
       author_helpers_static=pin(OUT/'author_helpers_read.json'),
       helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py','finish_review_v2.py','finalizer_schema_correction.json']],
       traciality_reduced_to_existing_core=True,core_traciality_proved=False,full_trace_constructed=False)
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)

    paragraphs=[
    '[REAL — tipos] Quatro teoremas públicos, dois helpers privados transitivos, nenhuma definição nova. Todos usam o MESMO scalarInverseLimitWeight e positiveSquare. A primeira conclusão é fechamento de subnível para SEQUÊNCIAS fortemente convergentes A_n, com C : ℝ≥0∞ arbitrário; não se exige C<∞, uniformidade de norma ou convergência dos adjuntos. Não foi promovida a uma afirmação topológica sobre redes arbitrárias ou a uma caracterização completa de LSC além do enunciado compilado.',
    '[REAL — Fatou e Haar] dualSquare_le_of_strong passa A_n→S para θ_s(A_n)v pela conjugação limitada já existente, e daí para os quadrados das normas. Isso evita inferir forte convergência de A_n* ou de A_n*A_n. O integrando incorpora ENNReal.ofReal dualHaarFactor, finito; measurabilidade, continuidade ofReal e multiplicação pelo fator finito dão o limite ponto a ponto. Fatou fornece a desigualdade sem DCT ou finitude de C. Em cada regulador k, usa-se A_n b_k→S b_k, com b_k a raiz ORIGINAL do corte. A identidade de quadrados vem de star_mul/associatividade; o limite τ é obtido por iSup_le. Mesmo vetor, Haar e corte, sem toReal de infinito.',
    '[REAL — média direita] scalarInverseLimitWeight_right_average_le vale para TODO A∈N e todo δ real, incluindo 0, conforme o fornecedor antigo. Para ε=1/(k+1)>0, a raiz b_k pertence a N pelo lema regularInverseGeneratorCutoff_sqrt_right; basta a primeira componente da conclusão, já paga. A comutação usada é b_k eδ=eδ b_k: (A eδ)b_k=(A b_k)eδ. Não se comuta A com b_k ou com eδ. scalarWeight_right_average_le recebe A b_k sem hipótese de quadrado finito. O mesmo índice k é comparado antes dos supremos.',
    '[REAL — sanduíche e ordem] regularSandwich A δ=eδ* A eδ. O helper genérico hilbert_contraction_left_square usa ‖c‖≤1 para c*c≤I e então a*(c*c)a≤a*a. Aplicado a c=eδ* e a=Aeδ, dá a ordem dos QUADRADOS dos dois operadores, seguida da monotonicidade do peso e do bound de média direita. Não usa eδ=eδ*, nenhuma ordem no conjugador de sanduíches e nenhuma tracialidade para permutar fatores.',
    '[REAL — equivalência exata e não circularidade] O sentido global→núcleo é restrição. No outro, o limite forte dos sanduíches com δ_n=1/(n+1)>0 e a primeira conclusão dão τ(A*A)≤τ(AA*) usando hcore em cada sanduíche, regularSandwich_star e o bound para A*. Repetir com A* dá igualdade em ENNReal, inclusive infinito. A hipótese hcore é consumida explicitamente; não se prova esse antecedente nem se declara finiteDualStarCore analítico ou finito-matricial. O tipo global coincide com a forma do campo RegularCoreTraceData.tracial (linha58) quando value é τ, mas não constrói um habitante do contrato.',
    '[REAL — ficha/histórico/controle] Nove fornecedores da ficha e dois do adendo foram conferidos por bytes, linhas e prefixos; tipos completos relevantes relidos. A ficha precede o código. O adendo é explicitamente posterior ao primeiro DEV, corrige linha59 para58 e localiza o fornecedor de pertença real da raiz; não foi reclassificado como anterior a toda implementação. O prefixo de norm_le_one_iff_of_nonneg é documentalmente truncado no binder opcional; o enunciado completo foi lido e é adequado. O primeiro DEV rc1 preservado tem Unknown identifier regularInverseCutoffSqrt_mem e not a positivity goal; foi excluído. O final e standalone estão rc0. O negativo BadTracialCorePremiseRemoved falha por Type mismatch ao tentar usar a equivalência como prova incondicional de tracialidade. Esse controle foi relido/pinado, não reexecutado; não é evidência de impossibilidade do antecedente.'
    ]
    limits=[
       'Aceite27 restrito à redução formal: quatro alvos, dois auxiliares transitivos; nenhum novo peso, GNS, cone ou contrato.',
       'A propriedade de subníveis provada é sequencial/forte; o teorema não tem parâmetro de rede arbitrária nem demanda uma cota de norma.',
       'Tracialidade no finiteDualStarCore continua OPEN, assim como a conclusão tracial completa A1(b) e os minorantes positivos finitos exigidos pelo contrato final.',
       'Normalidade, fidelidade, escala dual e semifinitude usual já entregues são herdadas; não foram reabertas como novas obrigações.',
       'K, OLD, memória, writers e monólito não foram escritos/executados pelo revisor. Só V recebeu o alvo/auditor novos; todos os pins próprios anteriores protegidos permaneceram iguais.'
    ]
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,
       P0=[],P1=[],P2=[],findings=[],exact_target_count=4,new_theorems=4,new_definitions=0,private_theorems=2,private_definitions=0,
       run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],
       type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,
       negative_controls=negative,all_prior_pins_preserved=True,core_traciality_proved=False,
       traciality_reduced_to_existing_core=True,trace_constructed=False,finite_positive_minorants_proved=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md=now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Módulo completo e auditor próprios rc0; quatro #check com universos e quatro #print axioms no trio permitido. Dois helpers privados incluídos transitivamente.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos anteriores de V preservados; '+str(len(new))+' objetos novos (alvo e auditor), total '+str(len(objects))+'. Nenhum fornecedor antigo reconstruído e nenhum objeto de K/DEV importado. Run próprio '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor; '+str(len(sw))+' mensagens de fornecedores herdadas discriminadas no JSON. Traces confirmam LEAN_PATH dentro de V/pacotes. Jobs totais Lake não são recompilações novas.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte K = snapshot = V | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, somente comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária do alvo medida: '+str(obj['equal_author_cold'])+'.\n\n'
    md+='[OPEN — limites] '+' '.join(limits)+'\n\nEvidências:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos e axiomas completos',comp['type_axiom_audit']),('histórico DEV',comp['history']),('fornecedores e consumidor',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),
       report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(status=STATUS,report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),
       compilation=report['compilation'],P0=[],P1=[],P2=[],own_objects_before=len(inherited),own_objects_after=len(objects),
       binary_equal=obj['equal_author_cold'],old_supplier_rebuilds=0),ensure_ascii=False))

if __name__=='__main__':main()

