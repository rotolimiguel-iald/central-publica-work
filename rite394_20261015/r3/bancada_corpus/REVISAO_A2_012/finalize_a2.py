from review_a2 import *

def read(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))
def normalize(n): return re.sub(r'\.\{[^}]*\}','',n.strip())
def axioms(log):
    result={}
    for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S):
        result[normalize(m[1])]=[normalize(a) for a in m[2].split(',') if a.strip()]
    for m in re.finditer(r"'([^']+)' does not depend on any axioms",log): result[normalize(m[1])]=[]
    return result
def validate(found,expected):
    missing=sorted(set(expected)-found.keys())
    foreign={n:[x for x in found.get(n,[]) if x not in ALLOWED] for n in expected}
    foreign={n:v for n,v in foreign.items() if v}
    return dict(missing=missing,foreign=foreign,passed=bool(expected) and not missing and not foreign)
def link(p,label=None,line=None):
    p=Path(p); return f'[{label or p.name}](<{p.as_posix()}{":"+str(line) if line else ""}>)'
def lineof(p,needle): return next(i for i,l in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1) if needle in l)
def current(row):
    try: return info(Path(row['path']))==row
    except OSError: return False

def main():
    data=read('INPUTS.json'); build=read('BUILD.json'); controls=read('CONTROLS.json')
    semantics=read('SEMANTICA_A2.json'); scan=read('SOURCE_SCAN.json'); consumers=read('CONSUMER_PROOF_AUDIT.json')
    frozen=[]; documents=[]
    for row in data['snapshots']:
        item=dict(before=row['source'],copy=row['copy'],source_unchanged=current(row['source']),copy_unchanged=current(row['copy']))
        (frozen if 'module' in row else documents).append(item)
    dependency_sources=[dict(source=v['source'],unchanged=current(v['source'])) for v in data['accepted_dependencies'].values()]
    borrowed=[]
    for row in read('READONLY_NAMESPACE_LINKS.json')['links']:
        src=Path(row['source']['path']); dst=Path(row['compiled_namespace_link']['path'])
        borrowed.append(dict(source=row['source'],review_path=str(dst),source_unchanged=current(row['source']),
            same_file=dst.exists() and os.path.samefile(src,dst)))
    integrity=dict(frozen_sources=frozen,documents_snapshot_only=documents,
        accepted_dependency_sources=dependency_sources,borrowed_objects=borrowed,
        all_frozen_unchanged=all(r['source_unchanged'] and r['copy_unchanged'] for r in frozen),
        all_accepted_unchanged=all(r['unchanged'] for r in dependency_sources) and all(r['source_unchanged'] and r['same_file'] for r in borrowed),
        documents_note='Author documentation may evolve during review; the frozen source snapshot is the acceptance target')
    record(ROOT/'INTEGRIDADE_A2.json',integrity)
    public_log=Path(build['audit']['stdout']['path'])
    found=axioms(public_log.read_text(encoding='utf-8'))
    checked=validate(found,data['expected_public_names'])
    own_log=Path(controls['audit']['stdout']['path'])
    own_found=axioms(own_log.read_text(encoding='utf-8')); own_checked=validate(own_found,controls['names'])
    for r in controls['negative_controls']:
        output=Path(r['stdout']['path']).read_text(encoding='utf-8')+Path(r['stderr']['path']).read_text(encoding='utf-8')
        r['rechecked_rejection']=r['returncode']!=0 and 'Type mismatch' in output and not re.search(
            r'unexpected token|unknown (identifier|constant|namespace|module)|object file .* does not exist|failed to',output,re.I)
        r['wall_verified']=r['wall'] in own_found and set(own_found[r['wall']])<=ALLOWED
        r['interpretation']=semantics['controls_interpretation'][r['name']]
    own_code=code_only((SRC/'IndependentA2Controls.lean').read_text(encoding='utf-8'))
    own_forbidden=re.findall(r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',own_code,re.M)
    toolchain=read('TOOLCHAIN.json')
    run_rows=list(build['modules'].values())+[build['audit'],controls['positive'],controls['audit'],consumers['result']]+controls['negative_controls']
    check_records=all(current(r[k]) for r in run_rows for k in ['source','stdout','stderr'])
    check_objects=all(current(r['object']) for r in run_rows if r.get('object'))
    selftests=dict(missing_rejected=not validate({},['required'])['passed'],
        foreign_rejected=not validate({'required':['alien.axiom']},['required'])['passed'],
        empty_list_rejected=not validate({},[])['passed'])
    gates={
        'lean431': 'version 4.31.0,' in toolchain['version'],
        'nine_source_modules':len(build['modules'])==len(MODULES)==9 and all(r['returncode']==0 for r in build['modules'].values()),
        'all_public_names':checked['passed'] and build['audit']['returncode']==0,
        'own_positive_and_axioms':controls['positive']['returncode']==0 and controls['audit']['returncode']==0 and own_checked['passed'],
        'nine_negative_controls':len(controls['negative_controls'])==9 and all(r['rechecked_rejection'] and r['wall_verified'] for r in controls['negative_controls']),
        'new_sources_clean':scan['all_clean'] and not own_forbidden,
        'frozen_sources_unchanged':integrity['all_frozen_unchanged'],
        'accepted_A1_unchanged':integrity['all_accepted_unchanged'],
        'source_logs_objects_current':check_records and check_objects,
        'prunable_confirmed_by_printed_terms':consumers['no_remaining_term_mentions_prunable'],
        'semantics':semantics['mathematical_scope_satisfied'],
        'fail_closed_selftests':all(selftests.values())
    }
    counts={p:sum(f['priority']==p for f in semantics['findings']) for p in ['P0','P1','P2']}
    passed=all(gates.values()) and counts['P0']==0 and counts['P1']==0
    decision=('VERIFICADO_NO_ESCOPO_DO_REPRESENTANTE_MINIMO_CCW_E_PAREDE__DELTA_P2_PENDENTE'
              if passed else 'NAO_ACEITAVEL_NESTA_RODADA')
    report=dict(decision=decision,created_utc=stamp(),reviewer_identity=semantics['reviewer_identity'],
        scope=semantics['scope'],gates=gates,findings_counts=counts,findings=semantics['findings'],
        full_A2_or_adendo_accepted=False,ThreeLocksCoreData_constructed=False,FullWitness_constructed=False,
        legacy_trace_adapter='OPEN',existing_WD_suppliers=semantics.get('existing_WD_suppliers'),sources_compiled=build['count'],public_name_count=len(data['expected_public_names']),
        public_axioms=dict(expected=data['expected_public_names'],actual={n:found.get(n) for n in data['expected_public_names']},**checked),
        own_axioms=dict(expected=controls['names'],actual={n:own_found.get(n) for n in controls['names']},**own_checked),
        controls=controls,toolchain=toolchain,accepted_cache_modules=len(data['accepted_dependencies']),accepted_cache_objects=len(borrowed),
        cache_not_rebuilt=True,selftests=selftests,own_forbidden_tokens=own_forbidden,
        identity_B1_previously_closed='B1 receipt sealed before A2; later cadastral amendment recorded Carver identity without changing technical findings')
    record(ROOT/'AUDITORIA_A2_INDEPENDENTE.json',report)
    if not passed:
        print(json.dumps(gates,indent=2)); raise RuntimeError('Failed gate; no acceptance receipt')
    names_by_module={}
    for row in scan['files']: names_by_module[Path(row['source']['path']).name]=len(row['public_names'])
    text=[
        '# Recibo de revisão adversarial independente — A2, lote congelado V354',
        f'**[REAL — medido nesta revisão] {decision}.** P0={counts["P0"]}; P1={counts["P1"]}; P2={counts["P2"]}.',
        '**Carver — agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`**, convocado pelo agente principal no escopo autorizado; '
        'não autor de A2. A identidade foi fornecida pelo agente principal [INPUT] e consta também do JSON. '
        'Nenhum outro usuário é apresentado como auditor/aprovador.',
        'Os oito V354 e CoreSupport foram verificados no alcance do suporte construído, representante mínimo, leitura no cone, '
        'ContinuousCornerWitness e parede de não ciclicidade. **Não é aceite integral de A2 da ORDEM 011 nem do adendo.** '
        'ThreeLocksCoreData e FullWitness não foram construídos; o adapter de traço total legado permanece [OPEN]. '
        'Uma pendência P2 de remoção de dois corolários sem consumidor antecede a incorporação enxuta.',
        f'Escrita exclusiva da revisão A2 em `{ROOT}`. Fontes autorais congelados preservados; nenhum fonte A1 recompilado, nenhum objeto emprestado sobrescrito. '
        'O recibo B1′ foi fechado antes de A2; recebeu depois apenas a correção cadastral solicitada de identidade, com backup e novo selo.',
        '## Resultado por obrigação',
        '| Obrigação delimitada | Resultado e evidência |\n|---|---|',
        '| Mesmo core e traço A1 | `regularCoreAlgebra P`, em `RegularHilbert (TowerHilbert P)`, e `scalarInverseLimitWeight P` são mantidos em toda a cadeia. A1 entra por cache aceito e fornecedores explícitos. |',
        '| Projeção não nula, traço um | `regularFiniteSupport_projection`, `_trace` e `_ne_zero`; nenhuma hipótese de suporte ou de finitude do projetor no resultado final. |',
        '| Faces iguais e ortogonais | `a=vq`, q=a*a, r=aa*, qr=0. A igualdade de traços consome `scalarInverseLimitWeight_tracial P a`. A revisão também confirmou rq=0. |',
        '| Calibração | Ação dual efetiva com s=log(tau(q+r).toReal), após provar traço positivo e finito. Transporta ambas as faces; não redefine o peso A1. |',
        '| Projeção espectral | `regularMinimalLock_spectral_zero`: projker(1−PF)=PF como igualdade de operadores, obtida de ker=range(PF). |',
        '| Gap | `regularMinimalLock_relative_gap`: norma preservada no complemento ortogonal do kernel. Controle próprio refuta a leitura global em todo H. |',
        '| Domínio e afiliação | Grafo do operador limitado 1−PF com domínio top, auto-adjunto e fechado; invariância sob todo B limitado do comutante. Não identifica um operador microscópico distinto. |',
        '| Leitura positiva / CCW | `positiveTraceReader_positive` vale para TODO positivo; `regularContinuousCorner` é termo no mesmo N, com leituras normalizadas 1, 1/2, 1/2. |',
        '| Canto de Breuer delimitado | `regularMinimalLock_breuer_kernel`: p=projker(Hmin), tau_A1(p)=1, 0<tau_A1(p)<top, sem testemunha hipotética na assinatura. |',
        '| Parede do reader | `positiveTraceReader_not_cyclic` refuta a ciclicidade global da extensão por zero. Não prova impossibilidade de qualquer outra extensão total. |',
        '## Leitura adversarial dos enunciados e das escolhas',
        '`regularTrace_finite_positive_below` exige um positivo não zero e usa semifinitude/fidelidade do contrato. '
        'Na cadeia concreta, o contrato é `scalarInverseLimitTraceData`. `positive_operator_has_threshold_projection` produz epsilon=norm(X)/2 '
        'e q=projker((X−epsilon I)^−); a positividade não nula dá q!=0 e epsilon q<=X. Finitude vem da ordem e homogeneidade do mesmo traço A1.',
        'O auxiliar `scalarTrace_finite_subprojection_exists` recebe e projetor não zero, **sem exigir traço finito de e**. '
        'O consumidor principal fornece o canto matricial e e v construídos em `regularCore_matrix_corner`, '
        'obtendo q finito sob e. Não há hipótese de projeção finita oculta no resultado principal. '
        '`SiteProfile` contém w:N→R e 0<w(n)<1; a representação regular é L²(R,TowerHilbert P). '
        '`Fin 2` no sítio matricial não é hipótese de dimensão finita desse Hilbert.',
        '`scalarTrace_finite_equal_split` usa efetivamente a tracialidade quadrática de A1 para a=vq. '
        'A revisão exibiu um contraexemplo em R×R: projeções ortogonais que somam a unidade, com peso cíclico e leituras 1 e 2. '
        'Assim, ortogonalidade ou soma sozinhas não pagam igualdade de faces; o fornecedor tracial e a equivalência via vq importam.',
        '`regularNormalizedFaces` aplica Classical.choose/choose_spec ao existencial previamente provado por `scalarTrace_normalized_split_exists`. '
        'Não há testemunha introduzida sem prova. O `classical` do reader decide positividade em um if dependente. '
        'Todos os nomes públicos foram auditados, inclusive essas definições e os lemas não impressos individualmente no fonte.',
        'CoreSupport é cópia byte-idêntica do fornecedor aceito. Seus lemas algébricos de aniquilação, auto-adjunção e maximalidade '
        'são os consumidores usados para Hmin. Auditar os construtores condicionais `threeLocksFromSupport` e `realizationFromSupport` '
        'não os instancia. A ocorrência de `¬FiniteDimensional` no segundo construtor legado não é uma premissa escondida dos V354.',
        '## Alcance exato de ContinuousCornerWitness e da parede',
        f'A interface lida em {link(ROOT/"inputs"/"accepted_sources"/"TGL"/"ContinuousCornerAbstract.lean")} '
        'pede uma função total Core→ENNReal e leis apenas nas projeções e no split; não pede ciclicidade global, fidelidade global ou normalidade. '
        'O reader satisfaz esse contrato com a convenção zero fora do cone e coincide com A1 em todos os positivos. '
        'Portanto o termo CCW é válido, mas seu campo chamado `trace` não passa a ser um traço global genuíno por ocupar esse campo.',
        'A parede constrói X=e+v* e Y=e: XY=e é positivo não zero, enquanto YX=e+v* não é positivo. '
        'O primeiro valor do reader é tau_A1(e)!=0 por fidelidade; o segundo é zero pela convenção. '
        'Logo este reader não pode preencher `ContinuousCoreData.trace_tracial`. A parede não resolve nem fecha a questão de outro adapter possível.',
        'A prova de Breuer delimitada utiliza diretamente A1 na projeção do kernel do representante mínimo. '
        'Ela não depende de interpretar o reader fora do cone, nem de supor ContinuousCornerWitness como hipótese, '
        'nem promove o resultado a ThreeLocksCoreData/FullWitness.',
        'W/D já têm fornecedores: `TGLExt.theSpecificAQFTWitness` em WedgeNet e '
        '`TGLExt.V350Continuous.towerWedgeData : WedgeModularData theSpecificAQFTWitness` em V350WedgeModularData, para mixProfile. '
        'Os fontes foram lidos e preservados em inputs/WD, com hashes em SEMANTICA_A2.json. '
        'Não se registra ausência genérica de W/D como pendência. O totalizador de traço Core→ENNReal com as leis legadas continua aberto; '
        'o reader construído é explicitamente excluído desse papel por sua própria parede.',
        '## P2-01 — dois casos da unidade removíveis',
        f'1. {link(SRC/"TGLExt"/"V354FiniteTraceSupport.lean", "scalarTrace_finite_positive_seed",lineof(SRC/"TGLExt"/"V354FiniteTraceSupport.lean","theorem scalarTrace_finite_positive_seed"))}: '
        'apenas declaração e impressão de axiomas, sem consumidor matemático no lote.',
        f'2. {link(SRC/"TGLExt"/"V354SpectralThreshold.lean", "scalarTrace_finite_projection_exists",lineof(SRC/"TGLExt"/"V354SpectralThreshold.lean","theorem scalarTrace_finite_projection_exists"))}: '
        'mesma situação. A cadeia usa diretamente os lemas gerais sobre o canto e11 construído.',
        f'Conferência em fonte: {link(ROOT/"UNUSED_COROLLARIES.json")}; conferência em termos impressos: '
        f'{link(ROOT/"CONSUMER_PROOF_AUDIT.json")}. Os demais termos impressos têm zero menções a ambos. '
        'O escopo é o lote congelado; não é alegação de inexistência de toda referência futura ou externa.',
        '**Delta mínimo recomendado ao autor:** remover as duas declarações e seus dois `#print axioms`; atualizar Audit geral e contagens. '
        'Manter os dois módulos e seus fornecedores gerais. Não criar flags nem `have` sem uso para simular consumo. '
        'Nenhum desses fontes foi alterado nesta revisão. A pendência não invalida os teoremas compilados, mas impede chamar o lote atual de incorporação mínima sem sobras.',
        '## Compilação, axiomas e controles',
        f'Lean medido: `{toolchain["version"]}`. {build["count"]}/9 fontes próprios compilados, além dos auditores e controles da revisão. '
        f'{len(data["expected_public_names"])}/{len(data["expected_public_names"])} nomes públicos do lote/fornecedor e '
        f'{len(controls["names"])} nomes dos controles próprios com axiomas efetivamente lidos e contidos em propext/Classical.choice/Quot.sound. '
        f'Evidência integral: {link(ROOT/"AUDITORIA_A2_INDEPENDENTE.json")}; log geral: {link(public_log)}; log próprio: {link(own_log)}.',
        '| Controle negativo próprio | Parede/contraparte positiva compilada | Resultado |\n|---|---|---|'
    ]
    for r in controls['negative_controls']:
        text.append(f'| {r["name"]} | `{r["wall"]}`; {r["interpretation"]} | rc={r["returncode"]}, incompatibilidade semântica de tipo |')
    text += [
        'Cada recusa usa um fonte sintaticamente válido, em ambiente já compilado. O erro isolado rejeita o termo oferecido; '
        'o suporte semântico vem das paredes/contramodelos comprovados. Casos corretos compilam no módulo IndependentA2Controls. '
        'Nome ausente ou axioma fora do trio reprova o finalizador; não há literal autoral usado como aprovação.',
        f'Cache declarado: {len(data["accepted_dependencies"])} módulos TGL/TGLExt aceitos, com {len(borrowed)} arquivos de objetos/companheiros emprestados '
        'por hardlinks somente de leitura; Mathlib e pacotes de terceiros também são cache. '
        'Não houve reconstrução de A1, Mathlib ou toolchain. Objetos novos foram gravados apenas em caminhos inicialmente inexistentes. '
        f'Integridade antes/depois de todos os objetos emprestados e fontes congelados: {link(ROOT/"INTEGRIDADE_A2.json")}.',
        'O limiar espectral usa maxHeartbeats 600000 local, com motivo declarado no fonte (elaboração CFC/projeção). '
        'Nenhum comando novo axiom/sorry/native_decide/trustCompiler foi encontrado nos oito V354, CoreSupport ou controles próprios. '
        'Os axiomas Lean aceitos permanecem o trio; comentários históricos não são declarações axiomáticas.',
        '## Tentativas preservadas e limitações de evidência',
        'A primeira tentativa independente de compilação esbarrou na resolução de namespaces do Lean: dependências aceitas estavam em um segundo diretório de busca. '
        'Foram feitos hardlinks imutáveis também junto aos novos outputs, sem sobrescrever objetos, e os nove fontes foram então recompilados com sucesso. '
        'Os logs da falha inicial estão em failed_setup e não contam como prova.',
        'O primeiro controle próprio de vetor no kernel usou uma extensionalidade excessiva e falhou; foi corrigido para ContinuousLinearMap.ext. '
        'Em seguida, os controles positivos e seu auditor compilaram. Uma execução das sondas foi interrompida por validação de caminho antes da criação de três fontes; '
        'todos os caminhos foram medidos dentro da raiz, os diretórios foram preparados sequencialmente e as nove sondas foram reexecutadas. '
        'Logs, snapshots e backups das tentativas anteriores foram preservados. Nenhum deles substitui o rc0 e os logs finais selecionados no JSON.',
        'A revisão é de código e prova sobre os caches aceitos, sem execução de um.py, experimentos ou mudança de gate. '
        'O aceite do escopo matemático delimitado não elimina a pendência P2 nem autoriza afirmar encerramento do adendo, '
        'ThreeLocksCoreData, FullWitness, natureza realizando o modelo ou um traço global do reader.',
        '## Arquivos congelados — origem, bytes, SHA256 e cobertura',
        '| Fonte autoral / cópia compilada | Bytes | SHA256 | Nomes públicos auditados |\n|---|---:|---|---:|'
    ]
    for row in data['snapshots']:
        if 'module' not in row: continue
        p=Path(row['copy']['path']); i=info(p)
        text.append(f'| {link(Path(row["source"]["path"]),row["module"])} / {link(p,"cópia")} | {i["bytes"]} | `{i["sha256"]}` | {names_by_module[p.name]} |')
    text += [
        '## Entrega e reprodução',
        f'{link(ROOT/"AUDITORIA_A2_INDEPENDENTE.json")} contém os nomes completos, axiomas, gates calculados, identidade do revisor e controles. '
        f'{link(ROOT/"BUILD.json")} contém cada comando efetivo, fonte, objeto, stdout/stderr e retorno. '
        'INPUTS.json contém os 683 fornecedores consultados e todos os caminhos/bytes/SHA de origem, cópia e hardlinks. '
        'MANIFESTO_A2.json inventaria artefatos próprios; SELO_A2.json sela o manifesto, o recibo e a auditoria sem hash autocircular.',
        'Os scripts recusam sobrescrever objetos de build ou emprestados. Uma reprodução limpa precisa de outra raiz vazia autorizada, '
        'preservando a separação entre fontes novos e caches aceitos. Não se executou o roteiro autoral para emitir este parecer.'
    ]
    rendered=re.sub(r'(\|)\n\n(?=\|)',r'\1\n','\n\n'.join(text))
    write(ROOT/'RECIBO_REVISAO_A2.md',rendered+'\n')
    files=[info(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name not in ['MANIFESTO_A2.json','SELO_A2.json'] and not p.is_relative_to(CACHE) and not p.is_relative_to(OUT)]
    new_objects=[r['object'] for r in run_rows if r.get('object')]
    record(ROOT/'MANIFESTO_A2.json',dict(created_utc=stamp(),root=str(ROOT),files=files,new_objects=new_objects,
        accepted_object_manifest=info(ROOT/'READONLY_NAMESPACE_LINKS.json'),
        excludes=['MANIFESTO_A2.json','SELO_A2.json','borrowed caches inventoried separately']))
    record(ROOT/'SELO_A2.json',dict(created_utc=stamp(),decision=decision,reviewer_identity=semantics['reviewer_identity'],
        files=[info(ROOT/n) for n in ['MANIFESTO_A2.json','RECIBO_REVISAO_A2.md','AUDITORIA_A2_INDEPENDENTE.json']]))
    print(json.dumps(dict(decision=decision,gates=gates,counts=counts,public_names=len(data['expected_public_names']),
        own_names=len(controls['names']),receipt=info(ROOT/'RECIBO_REVISAO_A2.md')),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
