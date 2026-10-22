from review_helpers import *

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==1 and s['targets'][0]['kind']=='theorem'
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==1
    assert len(re.findall(r'^private theorem\s+',code,re.M))==1
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values())
    name=next(iter(expected));types=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name]
    assert len(types)==1
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types={name:types[0]},axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    supplier='TGLExt.V350ScalarGNSNormality';old=next(x for x in s['sources'] if x['module']==supplier)
    assert not old['source_preexisting']
    assert Path(old['original']['path']).read_bytes()==(K/'TGLExt/V350ScalarGNSNormality.lean').read_bytes()
    tp,tj,oldinfos=trace(supplier);oldax=parse_axioms('\n'.join(oldinfos))
    assert len(oldax)==6 and all(set(v)<=ALLOWED for v in oldax.values())
    save(OUT/'old_supplier_reproduction.json',dict(source=old,author_source_read_only=pin(K/'TGLExt/V350ScalarGNSNormality.lean'),trace=pin(tp),axioms=oldax,old_theorems_not_new=6,all_axioms_allowed=True,author_object_used=False))

    p=R/'AUDITORIA_ORDEM_PESO_PERTURBADO_A1B.json';author=load(p);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(1,0,1,0)
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
    negative=dict(status='AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT',author_execution=True,own_execution=False,author_audit=pin(p),rows=rows,pins=pins)
    save(OUT/'negative_controls_read.json',negative)

    history=[]
    for p in sorted((R/'dev_perturbed_weight_order').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351PerturbedWeightOrder.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_build_evidence=False,role='Historical DEV only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,1,1,1,0]
    assert history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=4,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
    docs=[]
    for p in s['documents']:
        if p['path'].endswith('.json'):validate_pin_tree(load(Path(p['path'])),docs)

    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
    objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod);row=dict(module=mod,source=pin(V/(mod.replace('.','/')+'.lean')),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            author_obj=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(author_obj);row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
            assert not parse_axioms('\n'.join(tm)) # public and private source has no #print; independent auditor supplies it
        for msg in tj['log']:
            if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module'],supplier])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf-8-sig');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf-8-sig')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
    assert set(built)==set(s['modules']+[s['auditor_module'],supplier])
    comp=dict(timestamp=now(),status=STATUS,exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=1,private_definitions=0,total_source_theorems_including_private=2,count_scope='One new public theorem plus one private helper; six OLD supplier theorems excluded from novelty',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='Only this independent Lake invocation; four author historical DEV rc1 excluded',all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=1,old_supplier_reproduction=pin(OUT/'old_supplier_reproduction.json'),objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,helper_provenance=[pin(OUT/n) for n in ['build_delta.py','build_helper_origin.json','review_helpers.py','finish_helper_origin.json','finish_review.py']])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — hipótese e orientação] O alvo público recebe P, b,c no mesmo core, hb/hc na álgebra de ação direita e A no ideal escalar completo nν. A hipótese é bb*≤cc*. Não se assume b*b≤c*c, nem comutação entre b,c ou auto-adjunção. As duas identidades de norma anteriores mantêm π(b*)/π(c*) e o mesmo J⁻¹ΛA.',
      '[REAL — helper privado] star_apply_norm_sq_mono é genérico em uma Hilbert complexa completa. A positividade de CC*−BB* dá a desigualdade das partes reais dos produtos internos em v. apply_norm_sq_eq_inner_adjoint_left aplicado a star D fornece ‖D*v‖²=Re⟨DD*v,v⟩. RCLike.re_eq_complex_re explicita a ponte das projeções reais. O helper foi relido e compilado no módulo; seus axiomas entram transitivamente no alvo público, sem alegação de #print privado separado.',
      '[REAL — aplicação concreta] scalarGNSRepresentation_monotone P transporta a hipótese bb*≤cc*. map_mul e map_star entregam a ordem no tipo CLM concreto exigida pelo helper. ENNReal.ofReal_le_ofReal conclui a ordem dos valores, preservando o peso, Haar, vácuo e inscrição. O adendo da ficha corrige a seleção do fornecedor genérico OrderHomClass para o lema especializado já existente, sem re-provar a monotonicidade de π.',
      '[REAL — histórico e controle] Quatro DEV rc1 preservados/excluídos: instâncias/coerções, ausência do .olean antigo, síntese especializada e RCLike.re/Complex.re. O último usa helper genérico e re_eq_complex_re, com maxHeartbeats 1000000. A auditoria autoral standalone rc0 e seu negativo foram relidos por bytes/streams. Inverter a conclusão no mesmo contexto produz Type mismatch, não erro de imports ou ambiente. Isso recusa aquela prova adulterada, não demonstra desigualdade estrita universal. Nenhum teste autoral foi reexecutado.'
    ]
    limits=['Somente quadrados de A∈nν: extensão a TODOS os positivos, inclusive valores infinitos, não foi provada neste delta.','Nenhuma ordem dos sanduíches como operadores é inferida de bb*≤cc*.','Aplicação a ε requer a comparação concreta dos coeficientes; este teorema é genérico em b,c.','Limite e tracialidade continuam abertos. Nenhuma propriedade falsa de minorantes finitos de ν é usada.','Não foram alterados fontes autorais, memórias, relatórios anteriores ou gate; nenhum monólito ou recorder executado.']
    report=dict(timestamp=now(),status=STATUS,P0=[],P1=[],P2=[],findings=[],exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=1,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],old_supplier_reproduction=comp['old_supplier_reproduction'],semantic_review=paragraphs,limits=limits,negative_controls=negative,all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — ordem do peso perturbado\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] Sem P0, P1 ou P2: **1 teorema público + 1 helper privado, 0 definições**. Fonte inteiro relido; módulo e auditor próprio rc0. #check completo com universos e #print axioms do alvo público: apenas propext, Classical.choice e Quot.sound, incluindo dependência transitiva do helper.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos anteriores do Lake próprio preservados; acrescentados **um fornecedor antigo, módulo novo e auditor** (total '+str(len(objects))+'). Os seis teoremas de V350ScalarGNSNormality foram reproduzidos com prints no trio, mas não integram a novidade. Fonte antiga comparada OLD/kernel ↔ K ↔ V; nenhum objeto autoral/DEV herdado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor. '+str(len(sw))+' mensagens de fornecedores, inclusive histórico, constam no JSON. LEAN_PATH dos traces contém apenas V e seus pacotes.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final | `'+obj['source']['sha256']+'` |\n| .olean próprio | `'+obj['own']['sha256']+'` |\n| .olean cold autoral (comparação somente) | `'+obj['author_cold']['sha256']+'` |\n| Fonte do fornecedor antigo | `'+old['copy']['sha256']+'` |\n\nIgualdade binária do alvo medida: '+str(obj['equal_author_cold'])+'.\n\n'
    md+='[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos próprios:\n\n'
    for label,p in [('compilation',report['compilation']),('run',comp['run']),('tipos e axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedor antigo',comp['old_supplier_reproduction'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,objects_equal=obj['equal_author_cold']),ensure_ascii=False))

if __name__=='__main__':main()
