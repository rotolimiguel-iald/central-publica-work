from build_delta import *

OUT=R/'revisao_peso_perturbado_norma'
STATUS='A1_PERTURBED_WEIGHT_NORM_REVIEW_ACCEPTED__ALL_POSITIVE_EXTENSION_TRACE_OPEN'
NAME='REVIEW_A1_PERTURBED_WEIGHT_NORM_FINAL'
ALLOWED={'propext','Classical.choice','Quot.sound'}

def norm(s):return re.sub(r'\.\{[^}]*\}','',s).strip()

def parse_axioms(text):
    result={}
    pattern=r"^'([^\r\n]+)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))"
    for m in re.finditer(pattern,text,re.M|re.S):
        name=norm(m[1]); ax=[] if m[3] else [norm(v) for v in m[2].split(',') if v.strip()]
        if name in result:assert result[name]==ax
        result[name]=ax
    return result

def trace(mod):
    p=V/'.lake/build/lib/lean'/Path(mod.replace('.','/')+'.trace');j=load(p)
    assert not any(v['level']=='error' for v in j['log']),mod
    commands=[v['message'] for v in j['log'] if v['level']=='trace' and 'LEAN_PATH=' in v['message']]
    assert commands,mod
    for cmd in commands:
        lp=re.split(r'\s+[cC]:\\',cmd.split('LEAN_PATH=',1)[1],maxsplit=1)[0]
        assert all(Path(x).resolve().is_relative_to(V.resolve()) for x in lp.split(';')),lp
    infos=[re.sub(r'^.*?\.lean:\d+:\d+:\s*','',v['message']) for v in j['log'] if v['level']=='info']
    return p,j,infos

def validate_pin_tree(x,records):
    if isinstance(x,dict):
        if {'path','bytes','sha256'}<=x.keys():
            actual=pin(Path(x['path']))
            assert all(actual[k]==x[k] for k in ['path','bytes','sha256']),x
            records.append(actual)
        else:
            for value in x.values():validate_pin_tree(value,records)
    elif isinstance(x,list):
        for value in x:validate_pin_tree(value,records)

def main():
    pointer=load(OUT/'SNAPSHOT_POINTER.json');ck(pointer['snapshot'])
    a=Path(pointer['attempt']);s=load(a/'snapshot.json');run=load(a/'run.json')
    assert run['returncode']==0
    for p in s['protected']+s['base_compilations']+s['documents']+run['streams']+run['executables']:ck(p)
    for source in s['sources']:ck(source['original']);ck(source['copy'])
    assert load(a/'preservation.json')['all_unchanged']
    targets=s['targets'];expected={t['name'] for t in targets}
    assert len(targets)==2 and all(t['kind']=='theorem' for t in targets)
    target_source=next(x for x in s['sources'] if x['target'])
    code=uncomment(Path(target_source['copy']['path']).read_text(encoding='utf-8-sig'))
    assert len(re.findall(r'^theorem\s+',code,re.M))==2
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|^\s*private\s+theorem\s+',code,re.M)
    assert not re.findall(r'\b(?:axiom|sorry|admit|native_decide|trustCompiler|unsafe)\b',code)
    ap,aj,infos=trace(s['auditor_module']);axioms=parse_axioms('\n'.join(infos))
    assert set(axioms)==expected and all(set(v)<=ALLOWED for v in axioms.values())
    types={}
    for name in expected:
        matches=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name]
        assert len(matches)==1,(name,matches)
        types[name]=matches[0]
    typedata=dict(targets=targets,types=types,axioms=axioms,trace=pin(ap),all_axioms_allowed=True)
    save(a/'type_axiom_audit.json',typedata)

    # Current author standalone evidence is read, not executed or inherited.
    audit_path=R/'AUDITORIA_NORMA_PESO_PERTURBADO_A1B.json';author=load(audit_path)
    author_pins=[];validate_pin_tree(author,author_pins)
    assert {x['name'] for x in author['targets']}==expected
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert author['modules'][0]['source']==target_source['original']
    assert author['new_theorems']==2 and author['new_definitions']==0
    assert author['private_theorems']==0 and author['private_definitions']==0
    br=load(Path(author['positive_build']['path']));assert br['returncode']==0
    validate_pin_tree(br,author_pins)
    assert len(author['commands'])==2
    controls=[]
    for i,row in enumerate(author['commands']):
        txt=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
        if i==0:
            assert row['returncode']==0
            aa=parse_axioms(txt);assert set(aa)==expected and all(set(v)<=ALLOWED for v in aa.values())
        else:
            assert row['returncode']==1 and 'type mismatch' in txt.lower()
            assert not any(v in txt.lower() for v in ['unknown identifier','unknown module','object file','timeout','unexpected token','unterminated'])
        controls.append(dict(label=row['label'],returncode=row['returncode'],source=row['source'],stdout=row['stdout'],stderr=row['stderr'],source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stream_excerpt=txt))
    negative=dict(status='AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT',author_execution=True,own_execution=False,author_audit=pin(audit_path),rows=controls,pins=author_pins)
    save(OUT/'negative_controls_read.json',negative)

    # Historical source pins MUST resolve to retained snapshots, never live K paths.
    history=[]
    for p in sorted((R/'dev_perturbed_weight_norm').glob('*/run.json')):
        h=load(p);historical_location=h['source']['path'];snap=p.parent/'V351PerturbedWeightNorm.lean'
        actual=pin(snap);assert actual['bytes']==h['source']['bytes'] and actual['sha256']==h['source']['sha256']
        for field in ['stdout','stderr']:ck(h[field])
        text=Path(h['stdout']['path']).read_text(encoding='utf-8-sig')
        history.append(dict(run=pin(p),source=actual,historical_location=historical_location,stdout=h['stdout'],stderr=h['stderr'],returncode=h['returncode'],accepted_as_build_evidence=False,role='Author DEV history only; no object inherited',diagnostic=text))
    assert [h['returncode'] for h in history]==[1,1,0]
    assert history[-1]['source']['sha256']==target_source['copy']['sha256']
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=2,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True))
    docs=[]
    for p in s['documents']:
        if p['path'].endswith('.json'):validate_pin_tree(load(Path(p['path'])),docs)

    inherited={p['path'] for p in s['protected'] if p['path'].endswith('.olean')}
    objects=[];tw=[];sw=[]
    for p in sorted((V/'.lake/build/lib/lean').rglob('*.olean')):
        mod=str(p.relative_to(V/'.lake/build/lib/lean').with_suffix('')).replace('\\','.').replace('/','.')
        tp,tj,tm=trace(mod);src=V/(mod.replace('.','/')+'.lean')
        row=dict(module=mod,source=pin(src),own=pin(p),trace=pin(tp),own_previously_compiled=str(p) in inherited)
        if mod in s['modules']:
            author_obj=K/'.lake/build/lib/lean'/p.relative_to(V/'.lake/build/lib/lean')
            row['author_cold']=pin(author_obj)
            row['equal_author_cold']=row['own']['sha256']==row['author_cold']['sha256']
            assert not parse_axioms('\n'.join(tm))  # target source intentionally has no #print; independent auditor supplies both
        for entry in tj['log']:
            if entry['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=entry['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf-8-sig');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf-8-sig')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
    assert set(built)==set(s['modules']+[s['auditor_module']]),built
    comp=dict(timestamp=now(),status=STATUS,exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=0,private_definitions=0,all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='Only the independent Lake invocation of this delta; author historical rc1 explicitly excluded',all_axioms_allowed=True,all_target_typechecks_present=True,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=0,objects=objects,sourcepins=[target_source],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,helper_provenance=[pin(OUT/'build_delta.py'),pin(OUT/'build_helper_origin.json'),pin(Path(__file__))])
    checked=[];validate_pin_tree(comp,checked)
    save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — leitura e reprodução] O primeiro teorema recebe P, b pertencente à álgebra de ação direita já construída e A no ideal escalar completo nν. hb.1 fornece Ab∈nν e sua inscrição. A norma-quadrado existente identifica o mesmo dualQuadraticIntegral, com regularVacuum e Haar herdados; star_mul e associatividade dão (Ab)*(Ab)=b*(A*A)b. congrArg transporta a igualdade vetorial; a isometria do mesmo scalarTomitaPolarFactor elimina apenas o J externo. O J inverso interno e π(b*) permanecem no resultado.',
      '[REAL — aplicação concreta] O segundo teorema exige ε>0 e A∈nν. regularInverseGeneratorCutoff_sqrt_right fornece a pertinência ao core e a propriedade de ação direita da raiz positiva ORIGINAL do MESMO Bε. O testemunho existencial hb é apenas a prova de pertinência necessária à coerção; não pressupõe a conclusão de norma. Nenhuma hipótese residual de ação direita fica na aplicação concreta. Não se usa PositiveCoreInput.conjugate, cujo argumento pertence ao dualFixedCore, para tratar cortes por homonímia.',
      '[REAL — ficha e histórico] A ficha anterior ao código descreve exatamente esta ponte para valores de quadrados no domínio finito, sem extensão automática a todos os positivos. Seus fornecedores e pins foram relidos. Duas tentativas DEV rc1 (21:37 e 21:38) permanecem excluídas; seus diagnósticos de elaboração foram preservados. A versão final usa congrArg explícito, com maxHeartbeats 1000000 no fonte. Não se atribui aos rc1 prova parcial aceita. Pins históricos apontam às respectivas cópias DEV retidas, com o caminho vivo anterior separado como historical_location.',
      '[REAL — negativo relido] A auditoria autoral standalone rc0 foi conferida por bytes e streams. Remover J⁻¹ no controle BadPerturbedWeightWithoutJ produz rc1 Type mismatch, com imports resolvidos. Esta é evidência de recusa daquela prova adulterada, não demonstração universal da falsidade de toda fórmula sem J em casos especiais. O controle não foi reexecutado aqui.'
    ]
    limits=['A∈nν continua explícito; não há inscrição GNS declarada para A com ν(A*A)=∞.','Não há novas definições, helpers privados, axiomas postulados, sorry, native_decide ou trustCompiler no candidato.','Extensão e ordem dos pesos em TODOS os positivos, limite, semifinitude do limite e tracialidade permanecem obrigações posteriores. A propriedade falsa de minorantes positivos finitos de ν não é usada.','A1(b) permanece aberto; esta revisão não modifica gate, memórias, programa ou fontes autorais.']
    report=dict(timestamp=now(),status=STATUS,P0=[],P1=[],P2=[],findings=[],exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=0,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[])
    save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — norma do peso perturbado\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] Sem P0, P1 ou P2 no delta delimitado: **2 teoremas públicos, 0 definições, 0 helpers privados**. Fonte inteiro relido, Lake próprio rc0 e auditor independente com #check completo, pp.universes e #print axioms: somente propext, Classical.choice e Quot.sound.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos anteriores do Lake próprio preservados; adicionados apenas módulo e auditor (total '+str(len(objects))+'). Nenhum fornecedor antigo recompilado, nenhum objeto autoral/DEV importado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral da biblioteca. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor. '+str(len(sw))+' mensagens históricas de fornecedores constam no JSON; o stderr e avisos de cache, se presentes, foram preservados. LEAN_PATH dos traces contém somente V e seus pacotes.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final | `'+obj['source']['sha256']+'` |\n| .olean próprio | `'+obj['own']['sha256']+'` |\n| .olean cold autoral (comparação somente) | `'+obj['author_cold']['sha256']+'` |\n\nIgualdade binária medida: '+str(obj['equal_author_cold'])+'.\n\n'
    md+='[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos próprios:\n\n'
    for label,p in [('compilation',report['compilation']),('run',comp['run']),('tipos e axiomas',comp['type_axiom_audit']),('histórico',comp['history'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,objects_equal=obj['equal_author_cold']),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
