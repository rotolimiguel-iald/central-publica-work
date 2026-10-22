from review_helpers import *

FINAL_STATUS='A1_CUTOFF_AVERAGE_COMMUTATION_MATH_REVIEW_PASSED__DOCUMENTARY_P2_OPEN'

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==3 and all(t['kind']=='theorem' for t in s['targets'])
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==3 and len(re.findall(r'^private theorem\s+',code,re.M))==1
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(3,0,1,0)
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
    for p in sorted((R/'dev_cutoff_average_commutation').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351CutoffAverageCommutation.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=1,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
    docs=[]
    for p in s['documents']:
        if p['path'].endswith('.json'):validate_pin_tree(load(Path(p['path'])),docs)

    # Documentary mismatch is recorded, never silently normalized or treated as a Lean failure.
    adp=R/'ADENDO_FICHA_COMUTACAO_CFC.json';ad=load(adp);provided=ad['providers'][0]
    mp=V/'.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean'
    mt=mp.read_text(encoding='utf8');actual=re.search(r'^protected theorem IsSelfAdjoint\.commute_cfc \{a b : A\}[\s\S]*? :=',mt,re.M);assert actual
    actual_line=mt[:actual.start()].count('\n')+1
    assert provided['name']=='IsSelfAdjoint.commute_cfc' and provided['line']==67 and 'commute_cfcHom' in provided['statement'] and actual_line==87
    assert pin(mp)['sha256']==ad['source']['sha256']
    mdp=R/'ADENDO_FICHA_COMUTACAO_CFC.md';adt=mdp.read_text(encoding='utf8');mdline=adt[:adt.index('protected theorem IsSelfAdjoint.commute_cfcHom')].count('\n')+1
    finding=dict(id='P2-CFC-PROVIDER-LOCATOR',severity='P2',category='documentation',title='Adendo mistura commute_cfc com commute_cfcHom',file=str(adp),json_pointer='$.providers[0]',markdown_file=str(mdp),markdown_line=mdline,observed=provided,actual=dict(name='IsSelfAdjoint.commute_cfc',line=actual_line,statement=actual[0][:-3].rstrip(),source=pin(mp)),mathematical_result_affected=False,blocks_unqualified_delivery=True,correction='Com backup de bytes, corrigir no MD/JSON o locador e enunciado de IsSelfAdjoint.commute_cfc para a linha 87; manter commute_cfcHom linha 67 apenas se descrito separadamente. Não alterar Lean nem recompilar o delta por esta correção documental.')
    save(OUT/'documentary_finding.json',dict(timestamp=now(),finding=finding,documents=[pin(adp),pin(mdp)]))

    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')};objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod);row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            ao=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean');row['author_cold']=pin(ao);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256'];assert not parse_axioms('\n'.join(tm))
        for msg in tj['log']:
            if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']];assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf8');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf8');built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout);assert set(built)==set(s['modules']+[s['auditor_module']])
    comp=dict(timestamp=now(),status=FINAL_STATUS,requested_acceptance_status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=False,P0=[],P1=[],P2=[finding],exact_target_count=3,new_theorems=3,new_definitions=0,private_theorems=1,private_definitions=0,total_source_theorems_including_private=4,all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='Only this independent Lake invocation; one historical author DEV rc1 excluded',all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=0,objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,documentary_finding=pin(OUT/'documentary_finding.json'),helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — realização e sinal] O primeiro alvo usa exatamente regularSpectralCoordinates P, o multiplicador por sigmoid e o caráter de parâmetro +2πt. A comutação com todos os caracteres é descarregada pela lei aditiva existente. character_commutation_realScalarMultiplier fornece M C=C M, e o transporte pela equivalência estrela de V entrega o MESMO R e regularUnitary P t, sem hipótese residual nem nova transformação espectral.',
      '[REAL — CFC e raiz] R≥0 fornece IsSelfAdjoint para commute_cfc; a igualdade já provada Bε=cfc(fε)(R), sob ε>0, identifica o corte original. O helper hilbertPositiveSqrt_commutes é genérico em Hilbert complexa completa e consome Commute.cfcₙ_nnreal NNReal.sqrt com as instâncias do wrapper antigo. Nenhuma raiz nova é definida. O helper foi relido e compilado; seus axiomas entram transitivamente nos prints dos alvos públicos, sem alegar #print privado separado.',
      '[REAL — integral e domínio] A última identidade vale para TODO δ real, inclusive zero e negativo; somente ε>0 é exigido. regularAverage_apply mantém δ⁻¹ e o integral orientado de 0 a δ. O CLM B comuta com o escalar e atravessa o integral por intervalIntegral_comp_comm, usado na orientação inversa. A integrabilidade é descarregada pela continuidade forte de λ_t em cada vetor. Integral_congr usa a comutação pontual já provada; nenhuma continuidade em norma do grupo, separabilidade ou seleção de eventos a.e. sobre conjunto não enumerável foi pressuposta.',
      '[REAL — histórico e negativo] A tentativa DEV 220259_446252 rc1 permanece excluída: a reescrita procurava o lado errado do lema de integral. A final 220350_353915 rc0 coincide com a fonte reproduzida, sem avisos; maxHeartbeats 1600000 está explícito. A auditoria autoral standalone e os streams foram relidos com pins. O negativo insere sinal menos na conclusão e é recusado por Type mismatch, com imports resolvidos; não foi reexecutado nesta revisão. A recusa não exclui coincidências especiais, como δ=0.'
    ]
    limits=['As três conclusões formais passaram, mas o P2 documental de locador/enunciado deve ser corrigido antes de entrega sem ressalvas.','Não se afirma que qualquer b∈E comuta com as médias; o resultado é para as raízes dos cortes originais.','Extensão da ordem dos pesos a todos os positivos e tracialidade permanecem abertas; nenhum gate é promovido.','Nenhuma consulta adicional, edição de fontes autorais/memórias ou execução de monólito/recorder.']
    report=dict(timestamp=now(),status=FINAL_STATUS,requested_acceptance_status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=False,P0=[],P1=[],P2=[finding],findings=[finding],exact_target_count=3,new_theorems=3,new_definitions=0,private_theorems=1,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report);obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — comutação de cortes e médias\n\n'+now()+'\n\n**'+FINAL_STATUS+'**\n\n[REAL] **Sem P0/P1; um P2 documental.** Três teoremas públicos + um helper privado, zero definições. Leitura completa e Lake/auditor próprios rc0: #check com universos e axiomas apenas propext, Classical.choice, Quot.sound. O resultado matemático passou; não se emite aceite documental sem ressalvas.\n\n'
    md+='**P2 — referência CFC trocada no adendo.** [ADENDO_FICHA_COMUTACAO_CFC.md](<'+str(mdp)+':'+str(mdline)+'>) e JSON `$.providers[0]` nomeiam `IsSelfAdjoint.commute_cfc`, mas a linha 67 e o texto são de `commute_cfcHom`. O lema efetivamente usado existe na [linha 87 do mesmo arquivo pinado](<'+str(mp)+':87>). Corrigir locador e enunciado no MD/JSON, preservando bytes anteriores; não é necessário alterar/recompilar Lean.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; adicionados apenas módulo e auditor (total '+str(len(objects))+'). Nenhum fornecedor antigo recompilado ou objeto autoral/DEV importado. Pacotes externos são cache pinado herdado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor, '+str(len(sw))+' mensagens históricas de fornecedores registradas no JSON. LEAN_PATH dos traces só contém V e seus pacotes.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final | `'+obj['source']['sha256']+'` |\n| .olean próprio | `'+obj['own']['sha256']+'` |\n| .olean cold autoral, só comparação | `'+obj['author_cold']['sha256']+'` |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos próprios:\n\n'
    for label,p in [('compilation',report['compilation']),('run',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('P2 documental',comp['documentary_finding'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
    fresh(OUT/(NAME+'.md'),md.encode());save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=FINAL_STATUS,P2_count=1,objects_equal=obj['equal_author_cold']),ensure_ascii=False))

if __name__=='__main__':main()
