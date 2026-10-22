from review_helpers import *

FINAL_STATUS=STATUS
def save(p,x):
    if p.exists():
        old=load(p)
        assert {k:v for k,v in old.items() if k!='timestamp'}=={k:v for k,v in x.items() if k!='timestamp'}, ('refuse nonidentical retry output',str(p))
        return
    fresh(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())


def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0 and load(a/'preservation.json')['all_unchanged']
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for x in s['sources']:ck(x['original']);ck(x['copy'])
    target=next(x for x in s['sources'] if x['target']);expected={x['name'] for x in s['targets']}
    assert len(expected)==7 and sum(t['kind']=='theorem' for t in s['targets'])==6 and sum(t['kind']=='def' for t in s['targets'])==1
    code=uncomment(Path(target['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==6 and len(re.findall(r'^private theorem\s+',code,re.M))==4 and len(re.findall(r'^def\s+',code,re.M))==1
    assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values());types={}
    for name in expected:
        ts=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name];assert len(ts)==1;types[name]=ts[0]
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types=types,axioms=ax,trace=pin(ap),all_axioms_allowed=True,private_helper_audited_transitively=True))

    audit_path=R/'AUDITORIA_CORTE_DOMINIO_A1B.json';author=load(audit_path);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(6,1,4,0)
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
    for p in sorted((R/'dev_domain_cut').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351RegularDomainCut.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot only; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,0] and history[-1]['source']['sha256']==target['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=1,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
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
            stmt=pr.get('statement',pr.get('excerpt')); assert stmt; actual='\n'.join(lines[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
            assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),(pr.get('name','excerpt'),pr['line'])
            relative=fp.relative_to(K);own=V/relative
            if own.exists():
                assert fp.read_bytes()==own.read_bytes(),pr.get('name','excerpt')
                ownpin=pin(own); availability='Source equal in own project'
            else:
                assert pr.get('name')=='scalarWeight_square_finite_wot_closure'
                assert not any(v['module']=='TGLExt.V351ScalarWeightSemifiniteness' for v in s['sources'])
                ownpin=None; availability='Future consumer only; NOT in this dependency closure, NOT independently rebuilt in delta25'
            provider_checks.append(dict(name=pr.get('name','excerpt'),line=pr['line'],statement=stmt,author=pin(fp),own=ownpin,own_availability=availability,statement_matches=True))
    save(OUT/'provider_checks.json',dict(timestamp=now(),checks=provider_checks))
    # Read only the already proven interfaces actually used by this delta.
    excerpts=[]
    for relative,lo,hi in [
       ('TGLExt/BoundedGraphOperator.lean',10,40),
       ('TGLExt/BoundedGraphOperator.lean',117,130),
       ('TGLExt/V351RegulatorWeightOrder.lean',22,49),
       ('TGLExt/V351RegularPositiveGraph.lean',90,113),
       ('.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Equicontinuity.lean',977,986),
       ('.lake/packages/mathlib/Mathlib/Topology/MetricSpace/UniformConvergence.lean',94,102),
       ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean',283,298),
       ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean',444,456)]:
        p=V/relative;ls=p.read_text(encoding='utf-8').splitlines()
        excerpts.append(dict(source=pin(p),start=lo,end=min(hi,len(ls)),text='\n'.join(ls[lo-1:hi])))
    save(OUT/'semantic_supplier_excerpts.json',dict(timestamp=now(),records=excerpts))
    oldmods={x['module'] for x in s['sources'] if not x['target'] and not x['source_preexisting']}
    assert oldmods==set()
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
        exact_target_count=7,new_theorems=6,new_definitions=1,private_theorems=4,private_definitions=0,total_source_theorems_including_private=10,
        all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='This independent Lake invocation only; one author DEV rc1 excluded (elaboration/coercions, names, instance and unsolved goal); final clean rc0; no author DEV object used',
        all_axioms_allowed=True,all_target_typechecks_present=True,private_helper_audited_transitively=True,own_previous_project_objects_reused=True,
        external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,
        package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],
        own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),
        newly_recompiled_old_supplier_count=len(oldmods),newly_recompiled_old_suppliers=old_audits,objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),
        type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,
        package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,
        provider_checks=pin(OUT/'provider_checks.json'),semantic_supplier_excerpts=pin(OUT/'semantic_supplier_excerpts.json'),
        history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,
        helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']]+[pin(p) for p in sorted(OUT.glob('finish_review.py.bak_*'))])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=['[REAL — objeto e hipóteses] Sete declarações públicas: regularDomainCut é uma definição no MESMO (regularCoreAlgebra P).toStarSubalgebra; seguem seis teoremas. qδ=1−δBδ usa exatamente regularInverseGeneratorCutoff P δ. A definição é total em δ, mas pertença à álgebra de ação direita, positividade e cotas exigem δ>0; identidades que envolvem Bε exigem também ε>0. Não se introduziu outra realização de h, raiz ou GNS.', '[REAL — produto e ordem] A positividade de qδ vem de Bδ≤δ⁻¹I e multiplicação pelo escalar REAL positivo δ; qδ≤I vem de Bδ≥0. A comutação com Bε é deduzida da comutação dos cortes existentes. A identidade Bεqδ=Bδ−εBδBε usa a identidade resolvente antiga, sem divisão por δ−ε e portanto também vale quando os reguladores coincidem. O helper genérico prova Bq²≤Bq por positividade de (Bq)(1−q), demonstrando a comutação necessária. Depois Bεqδ≤Bδ≤δ⁻¹I. Não há multiplicação de desigualdade por operadores não comutantes; a constante depende somente de δ, uniforme em todo ε>0.', '[REAL — convergência forte] No mesmo RegularHilbert(TowerHilbert P), R é regularSpectralResolvent P, S=1−R e Dn=δnBδn, δn=1/(n+1). O código prova Dn S=δn R qδn e ||Dn(Sy)||≤δn||y||. A imagem de S é densa pelo fornecedor antigo bounded_graph_domain_dense, cujo domínio é definicionalmente Ran(S), usando S auto-adjunto e a injetividade de 1−R já entregue. As contrações Dn são uniformemente 1-Lipschitz; Equicontinuous.isClosed_setOf_tendsto estende o limite zero da imagem densa a TODO vetor. Finalmente qδn v=v−Dn v→v. Não se troca ponto a ponto por norma de operadores, nem se assume inversa limitada de S ou gap.', '[REAL — auxiliares e reuso] Os quatro helpers privados são hilbert_positive_smul, hilbert_contract_norm, hilbert_positive_product e hilbert_commuting_contract_product, todos em Hilbert complexo genérico completo. Suas premissas de positividade/comutação são explicitamente satisfeitas na especialização; o auditor público cobre seus axiomas transitivos. A norma usa CStarAlgebra.norm_le_norm_of_nonneg_of_le e ContinuousLinearMap.norm_id_le, que não exigem que o espaço seja não trivial. As 14 entradas da ficha e os três recortes do adendo foram confrontados com fontes/linhas/pins; as interfaces futuras de finitude/WOT são somente consumidoras previstas, não resultados deste módulo. Em particular V351ScalarWeightSemifiniteness foi lido/pinado em K para a ficha, mas não está na dependência fechada deste delta nem em V; não foi reproduzido nesta revisão.', '[REAL — cronologia e evidência] Ficha 23:03:13 e adendo 23:03:55 antecedem a primeira tentativa 23:05:46. Essa tentativa rc1 foi preservada e excluída: o stream mostra norm_one_le ausente, reescrita de produtos, instância CFC concreta, coerção do subtipo e meta final não resolvida. O DEV final 23:07:09 é rc0 sem avisos. Pins históricos apontam para snapshots reais dos respectivos DEV; o caminho vivo antigo fica apenas como localização textual. O autor standalone e o auditor7 passaram; a sonda BadDomainCutProductReversed inverte ≤ e falha por Type mismatch, com imports válidos. O negativo foi relido/pinado, não reexecutado.']
    limits=['Delta25 somente: seis teoremas públicos, uma definição, quatro helpers privados transitivos; nenhum fornecedor antigo novo precisou ser construído neste delta.', 'ε>0 e δ>0 nas afirmações de produto; a convergência cobre todo vetor do MESMO Hilbert e a sequência δn=1/(n+1). A cota δ⁻¹ é uniforme em ε, não em δ.', 'Não demonstra norma-operador qδn→I, gap, finitude de (a qδ)*a qδ no peso limite, densidade WOT desse ideal, semifinitude usual ou tracialidade. Esses consumidores permanecem OPEN.', 'O peso/contrato anteriores não são redefinidos, e nenhuma condição do gate ou memória é alterada. O campo autoral sobre ação da raiz é herança do delta CFC aceito, não teorema novo deste arquivo.', 'Objetos próprios anteriores e cache de pacotes reutilizados com pins; nenhum objeto de projeto autoral/DEV usado, nenhum monólito/writer/recorder executado; parecer24 e todos os anteriores intactos.']
    report=dict(timestamp=now(),status=STATUS,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],
        exact_target_count=7,new_theorems=6,new_definitions=1,private_theorems=4,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),
        sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,
        all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — corte de domínio regular\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem achados P0/P1/P2.** Seis teoremas públicos + uma definição, quatro helpers privados. Módulo completo e auditor próprios rc0; sete #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos próprios anteriores preservados; construídos somente alvo e auditor, total '+str(len(objects))+'. Nenhum fornecedor antigo recompilado neste delta; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor e '+str(len(sw))+' mensagens de fornecedores com origem separada no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final (K=cópia própria) | '+obj['source']['sha256']+' |\n| .olean próprio | '+obj['own']['sha256']+' |\n| .olean autoral standalone, apenas comparação | '+obj['author_cold']['sha256']+' |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos de evidência:\n\n'
    for label,p in [('compilation',report['compilation']),('run próprio',comp['run']),('tipos/axiomas',comp['type_axiom_audit']),('histórico',comp['history']),('fornecedores da ficha',comp['provider_checks'])]:
        md+='- ['+label+'](<'+p['path']+'>) — SHA256 '+p['sha256']+'.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[],objects_equal=obj['equal_author_cold'],object_count=len(objects)),ensure_ascii=False))
if __name__=='__main__':main()

