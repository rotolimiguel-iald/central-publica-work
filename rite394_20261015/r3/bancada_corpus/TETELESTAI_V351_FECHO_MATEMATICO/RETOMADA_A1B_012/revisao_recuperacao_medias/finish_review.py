from review_helpers import *
import difflib

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
    assert not re.findall(r'^\s*(?:private\s+|noncomputable\s+)?def\s+|^\s*private\s+theorem\s+|\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code,re.M)
    ap,aj,infos=trace(s['auditor_module']);ax=parse_axioms('\n'.join(infos))
    assert set(ax)==expected and all(set(v)<=ALLOWED for v in ax.values())
    name=next(iter(expected));types=[v for v in infos if not v.startswith("'") and norm(v.split(' ',1)[0])==name]
    assert len(types)==1
    save(a/'type_axiom_audit.json',dict(targets=s['targets'],types={name:types[0]},axioms=ax,trace=pin(ap),all_axioms_allowed=True))

    p=R/'AUDITORIA_RECUPERACAO_MEDIAS_A1B.json';author=load(p);pins=[];validate_pin_tree(author,pins)
    assert {x['name'] for x in author['targets']}==expected and author['modules'][0]['source']==target['original']
    assert author['all_axioms_allowed'] and author['negative_controls_rejected']
    assert (author['new_theorems'],author['new_definitions'],author['private_theorems'],author['private_definitions'])==(1,0,0,0)
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
    for p in sorted((R/'dev_weight_average_recovery').glob('*/run.json')):
        j=load(p);sp=pin(p.parent/'V351WeightAverageRecovery.lean')
        assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
        for f in ['stdout','stderr']:ck(j[f])
        history.append(dict(run=pin(p),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],accepted_as_final_build_evidence=False,role='Historical DEV snapshot; no object imported',diagnostic=Path(j['stdout']['path']).read_text(encoding='utf-8-sig')))
    assert [h['returncode'] for h in history]==[1,1,0]
    before=Path(history[-1]['source']['path']).read_bytes();after=Path(target['copy']['path']).read_bytes()
    removed=[line for line in before.splitlines(keepends=True) if line.decode('utf8').strip()=='change d n ∈ ({0} : Set ℝ)ᶜ']
    assert len(removed)==1 and before.replace(removed[0],b'',1)==after
    delta=dict(historical_source=history[-1]['source'],final_source=target['copy'],removed_line=removed[0].decode('utf8'),bytes_removed=len(removed[0]),exact_byte_removal_verified=True,diff=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True))))
    save(OUT/'history_read.json',dict(timestamp=now(),rows=history,failed_attempt_count=2,excluded_failed_attempts=True,historical_locations_are_not_active_pins=True,final_linter_cleanup=delta))
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
            assert not parse_axioms('\n'.join(tm)) # #check/axioms are in the independent auditor
        for msg in tj['log']:
            if msg['level']=='warning':(tw if mod in s['modules']+[s['auditor_module']] else sw).append(dict(module=mod,message=msg['message'],old_object=row['own_previously_compiled']))
        objects.append(row)
    assert not tw
    new=[x for x in objects if not x['own_previously_compiled']]
    assert {x['module'] for x in new}==set(s['modules']+[s['auditor_module']])
    stdout=Path(run['streams'][0]['path']).read_text(encoding='utf-8-sig');stderr=Path(run['streams'][1]['path']).read_text(encoding='utf-8-sig')
    built=re.findall(r'\bBuilt\s+([^\s(]+)',stdout)
    assert set(built)==set(s['modules']+[s['auditor_module']])
    comp=dict(timestamp=now(),status=STATUS,exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=0,private_definitions=0,count_scope='One public theorem; no private declarations',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='Only this independent Lake invocation; two author historical DEV rc1 excluded, DEV rc0 with warning not final source',all_axioms_allowed=True,all_target_typechecks_present=True,own_previous_project_objects_reused=True,external_project_objects_inherited=False,dev_objects_used=False,package_cache_inherited=True,package_provenance=pin(R/'revisao/independent_20260914_173529_454447/cache_provenance.json'),base_compilations=s['base_compilations'],own_previous_project_object_count=len(inherited),own_project_object_count_after=len(objects),new_project_object_count=len(new),newly_recompiled_old_supplier_count=0,objects=objects,sourcepins=[target],run=pin(a/'run.json'),snapshot=pin(a/'snapshot.json'),type_axiom_audit=pin(a/'type_axiom_audit.json'),negative_controls=negative,supplierwarnings=sw,targetwarnings=tw,lake_stderr=stderr,package_cache_not_rebuilt=True,built_log_entries=built,protected_pins=s['protected'],all_prior_pins_preserved=True,fiche_provider_pins=docs,history=pin(OUT/'history_read.json'),author_dev_evidence_read_only=history,final_linter_cleanup=delta,helper_provenance=[pin(OUT/n) for n in ['build_delta.py','review_helpers.py','helper_provenance.json','finish_review.py']])
    checked=[];validate_pin_tree(comp,checked);save(OUT/'compilation.json',comp)
    paragraphs=[
      '[REAL — tipo e domínio] scalarWeight_square_eq_iSup_averages recebe somente P e A no core N. Não recebe HasFiniteScalarSquare, MemLp, finitude da integral, monotonicidade das amostras ou hipótese sobre seus minorantes. O resultado é uma igualdade em ENNReal para o mesmo dualQuadraticIntegral, regularVacuum, dualAmbient e regularAverage P (1/(n+1)), incluindo ν(A*A)=∞.',
      '[REAL — limite e Haar] A sequência d_n=1/(n+1) converge a zero na vizinhança perfurada, com d_n≠0 provado. A convergência pontual da órbita existente passa a norma-quadrado e ofReal. O fator fixo ofReal dualHaarFactor permanece dentro de f_n e g; continuous_const_mul usa explicitamente ofReal_ne_top. Isso exige finitude da CONSTANTE, não finitude da integral. dualQuadraticIntegrand_star_mul liga exatamente as avaliações quadráticas às normas. Measurabilidade e lintegral_const_mul recuperam a normalização original.',
      '[REAL — duas desigualdades] Fatou para a sequência atTop dá integral(g)≤liminf integral(f_n); a cota por iSup de todos os termos fecha esse sentido. No sentido oposto, iSup_le aplica scalarWeight_right_average_le a cada d_n, cujo fornecedor vale para todo A∈N. Não há DCT com integrabilidade escondida, rede arbitrária exigida por Fatou, ordenação das amostras, ou comparação (Ae_n)*(Ae_n)≤A*A em ordem de operadores.',
      '[REAL — ficha, história e negativo] A ficha anterior ao código foi relida, com nove fornecedores pinados; a consulta é identificada como roteiro, não prova. Os dois DEV rc1 efetivamente encontrados são 215633_172434 e 215716_269572, ambos excluídos. O DEV 215753_855426 rc0 tem um aviso de change inútil; a remoção exata de uma linha (40 bytes) foi medida entre seu snapshot histórico e a fonte final reproduzida. Pins antigos apontam aos snapshots reais, nunca ao caminho vivo com hash antigo. A auditoria autoral final rc0 foi conferida; substituir o supremo por um único corte produz Type mismatch com imports resolvidos. Esse negativo não foi reexecutado e não demonstra que igualdade num corte seja impossível em casos especiais.'
    ]
    limits=['Há recuperação dos valores quadráticos para todo A∈N, inclusive ∞.','A finitude dos quadrados regularizados é fornecedor anterior, não premissa desta prova nem novo alvo.','Comutação dos cortes com as mesmas médias e a extensão correspondente da ordem dos pesos dos cortes ainda são obrigações posteriores.','Tracialidade/A1(b) permanecem abertos; não se usa a propriedade falsa de minorantes positivos finitos de ν.','Sem novas consultas, testes extra, monólito, recorder, escrita autoral ou alteração de memória/gate.']
    report=dict(timestamp=now(),status=STATUS,P0=[],P1=[],P2=[],findings=[],exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=0,private_definitions=0,run=comp['run'],compilation=pin(OUT/'compilation.json'),sourcepins=comp['sourcepins'],type_axiom_audit=comp['type_axiom_audit'],semantic_review=paragraphs,limits=limits,negative_controls=negative,all_prior_pins_preserved=True,trace_constructed=False,gate_modified=False)
    validate_pin_tree(report,[]);save(OUT/(NAME+'.json'),report)
    obj=next(x for x in objects if x['module'] in s['modules'])
    md='# Revisão independente — recuperação do peso pelas médias\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] Sem P0, P1 ou P2: **1 teorema público, 0 definições/helpers privados**. Fonte inteiro relido, módulo e auditor próprios rc0; #check completo com universos e #print axioms: somente propext, Classical.choice e Quot.sound.\n\n'+'\n\n'.join(paragraphs)
    md+='\n\n[REAL — proveniência] '+str(len(inherited))+' objetos anteriores do Lake próprio preservados; acrescentados apenas módulo e auditor (total '+str(len(objects))+'). Nenhum fornecedor antigo recompilado, nenhum objeto autoral/DEV herdado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em '+str(round(run['elapsed_seconds'],3))+' s; zero avisos do alvo/auditor. '+str(len(sw))+' mensagens históricas de fornecedores constam no JSON. LEAN_PATH dos traces contém apenas V e seus pacotes.\n\n'
    md+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final | `'+obj['source']['sha256']+'` |\n| .olean próprio | `'+obj['own']['sha256']+'` |\n| .olean cold autoral (comparação somente) | `'+obj['author_cold']['sha256']+'` |\n| Snapshot DEV anterior ao ajuste do linter | `'+history[-1]['source']['sha256']+'` |\n\nIgualdade binária do alvo final medida: '+str(obj['equal_author_cold'])+'.\n\n'
    md+='[OPEN — limites] '+' '.join(limits)+'\n\nArtefatos próprios:\n\n'
    for label,p in [('compilation',report['compilation']),('run',comp['run']),('tipos e axiomas',comp['type_axiom_audit']),('histórico/diff',comp['history'])]:md+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
    fresh(OUT/(NAME+'.md'),md.encode())
    save(OUT/'pin_verification.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),report=pin(OUT/(NAME+'.md')),report_json=pin(OUT/(NAME+'.json')),compilation=report['compilation']))
    print(json.dumps(dict(report=pin(OUT/(NAME+'.md')),json=pin(OUT/(NAME+'.json')),compilation=report['compilation'],status=STATUS,objects_equal=obj['equal_author_cold']),ensure_ascii=False))

if __name__=='__main__':main()
