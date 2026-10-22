from review import *

def read(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))

def parse_axioms(text):
    found={}
    normalize=lambda n: re.sub(r'\.\{[^}]*\}', '', n.strip())
    for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text,re.S):
        found[normalize(m[1])]=[normalize(a) for a in m[2].split(',') if a.strip()]
    for m in re.finditer(r"'([^']+)' does not depend on any axioms",text):
        found[normalize(m[1])]=[]
    return found

def validate_axioms(found,expected):
    missing=sorted(set(expected)-found.keys())
    bad={n:[a for a in found.get(n,[]) if a not in ALLOWED] for n in expected}
    bad={n:v for n,v in bad.items() if v}
    return dict(missing=missing,unexpected=bad,ok=bool(expected) and not missing and not bad)

def line(path,needle):
    hits=[i for i,s in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1) if needle in s]
    assert hits, (path,needle)
    return hits[0]

def link(path,label=None,at=None):
    path=Path(path)
    suffix=f':{at}' if at else ''
    return f'[{label or path.name}](<{path.as_posix()}{suffix}>)'

def main():
    build=read('BUILD.json'); inputs=read('INPUTS.json'); scan=read('SOURCE_SCAN.json')
    baseline=read('BASELINE_COMPARISON.json'); author=read('AUTHOR_CONTROLS_RERUN.json')
    own=read('INDEPENDENT_CONTROLS.json'); semantics=read('SEMANTICA_REVISOR.json')
    cache=read('CACHE_EVIDENCE.json'); toolchain=read('TOOLCHAIN.json')
    audit_source=K/'TGLExt'/'AuditSameBetaFourFaces.lean'
    expected=re.findall(r'^#print axioms (\S+)',audit_source.read_text(encoding='utf-8'),re.M)
    stdout=Path(build['modules']['TGLExt.AuditSameBetaFourFaces']['stdout']['path'])
    log=stdout.read_text(encoding='utf-8')
    found=parse_axioms(log); ax=validate_axioms(found,expected)
    own_source=K/'IndependentSubstitution.lean'
    own_expected=re.findall(r'^#print axioms (\S+)',own_source.read_text(encoding='utf-8'),re.M)
    own_stdout=Path(own['positive']['stdout']['path'])
    own_found=parse_axioms(own_stdout.read_text(encoding='utf-8')); own_ax=validate_axioms(own_found,own_expected)
    all_found=found|own_found
    own_scan=[]
    for p in sorted(K.glob('Independent*.lean')):
        code=lean_code(p.read_text(encoding='utf-8'))
        own_scan.append(dict(source=info(p),forbidden_tokens=re.findall(
            r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',code,re.M)))
    origin_checks=[]
    for row in inputs['snapshots']:
        before=row['source']; p=Path(before['path'])
        try:
            now=info(p); same=now==before
        except OSError as e: now=dict(error=str(e)); same=False
        origin_checks.append(dict(before=before,after=now,unchanged=same))
    record(ROOT/'INTEGRIDADE_ORIGENS_REVISOR.json',dict(files=origin_checks,
        all_unchanged=all(r['unchanged'] for r in origin_checks),
        scope='Somente arquivos efetivamente copiados/lidos do autor e contrato; não atesta outras sessões ou casas inacessíveis'))
    for row in author['controls']:
        row['semantic_basis']=semantics['control_semantics'][row['name']]
        row['wall_axioms']=all_found.get(row['semantic_basis']['wall'])
        row['wall_verified']=row['semantic_basis']['wall'] in all_found and set(row['wall_axioms'])<=ALLOWED
    selftests={
        'missing_name_rejected':not validate_axioms({},['required'])['ok'],
        'foreign_axiom_rejected':not validate_axioms({'required':['foreign.test']},['required'])['ok'],
        'empty_requirement_rejected':not validate_axioms({},[])['ok'],
        'universe_suffix_normalized':parse_axioms("'Foo.{u}' depends on axioms: [Quot.sound.{u}]")=={'Foo':['Quot.sound']}
    }
    main_source=K/'TGLExt'/'TheSameBetaReadsFourFaces.lean'
    body=main_source.read_text(encoding='utf-8').split('theorem the_same_beta_reads_four_faces',1)[1]
    main_print=log.split('theorem TGLExt.the_same_beta_reads_four_faces',1)[-1]
    source_current=all(info(Path(r['source']['path']))==r['source'] for r in build['modules'].values())
    log_current=all(info(Path(r[k]['path']))==r[k] for r in build['modules'].values() for k in ['stdout','stderr','object'])
    checks={
        'lean_4_31_0': 'version 4.31.0,' in toolchain['version'],
        'fresh_local_source_build': build['count']==len(inputs['graph']) and all(r['returncode']==0 and r['object'] and r['source_unchanged'] for r in build['modules'].values()),
        'build_sources_unchanged':source_current,
        'build_logs_and_objects_unchanged':log_current,
        'author_axioms':ax['ok'], 'independent_axioms':own_ax['ok'],
        'source_scan':scan['all_clean'] and all(not r['forbidden_tokens'] for r in own_scan),
        'baseline_sources_identical':baseline['all_equal'] and baseline['count']==len(inputs['graph'])-len(NEW),
        'direct_B1_application':'exact ⟨the_same_beta_reads_three_faces c ρr ρm ρΛ, hEOM⟩' in body and 'the_same_beta_reads_three_faces' in main_print and 'hEOM' in main_print,
        'nine_author_controls':len(author['controls'])==9 and all(r['returncode']!=0 and r['semantic_type_rejection'] and r['wall_verified'] for r in author['controls']),
        'independent_substitution_controls':own['positive']['returncode']==0 and len(own['negatives'])==2 and all(r['semantic_type_rejection'] for r in own['negatives']),
        'semantic_contract':semantics['semantic_contract_satisfied'],
        'origins_unchanged':all(r['unchanged'] for r in origin_checks),
        'cache_revisions':cache['all_revisions_match'],
        'fail_closed_selftests':all(selftests.values())
    }
    counts={p:sum(f['priority']==p for f in semantics['findings']) for p in ['P0','P1','P2']}
    if all(checks.values()) and not counts['P0'] and not counts['P1']:
        decision='ACEITAVEL_NO_ESCOPO_CONDICIONAL_DO_ADENDO_012_PARAGRAFO_4'
    else: decision='NAO_ACEITAVEL_NESTA_REVISAO'
    audit=dict(created_utc=stamp(),decision=decision,checks=checks,findings_counts=counts,
        findings=semantics['findings'],observations=semantics['observations'],
        reviewer=semantics['reviewer'],scope=semantics['scope'],
        toolchain=toolchain,source_build_count=build['count'],
        author_axioms=dict(expected=expected,found={n:found.get(n) for n in expected},**ax),
        independent_axioms=dict(expected=own_expected,found={n:own_found.get(n) for n in own_expected},**own_ax),
        author_controls=author,independent_controls=own,own_source_scans=own_scan,
        fail_closed_selftests=selftests,
        integration='Somente proposta; não instalado por esta revisão; EOM é hipótese, não experimento',
        article_A=read('PRIMARY_ACCESS.json'),
        limits='Caches de terceiros lidos, não recompilados; revisão não equivale a reconstruir Lean/Mathlib nem à validação empírica da EOM')
    record(ROOT/'AUDITORIA_INDEPENDENTE.json',audit)
    if not all(checks.values()):
        print(json.dumps(dict(decision=decision,checks=checks),ensure_ascii=False,indent=2))
        raise RuntimeError('At least one gate failed; no acceptance report issued')
    evidence=[main_source,K/'TGLExt'/'ActionCouplingControls.lean',audit_source,
        K/'TGLExt'/'TheSameBetaReadsThreeFaces.lean',own_source,K/'IndependentBadBeta.lean',K/'IndependentBadXi.lean',
        ROOT/'inputs'/'ENTREGA_B1_PRIME.md',ROOT/'inputs'/'AUDITORIA_B1_PRIME.json',
        ROOT/'inputs'/'REAPROVEITAMENTO_B1_PRIME.md',ROOT/'inputs'/'PROPOSTA_CONSUMIDOR.json',
        stdout,own_stdout,ROOT/'BUILD.json',ROOT/'AUTHOR_CONTROLS_RERUN.json',ROOT/'INDEPENDENT_CONTROLS.json',
        ROOT/'AUDITORIA_INDEPENDENTE.json',ROOT/'INTEGRIDADE_ORIGENS_REVISOR.json',ROOT/'CACHE_EVIDENCE.json']
    origin=AUTHOR/'kernel'/'TGLExt'/'TheSameBetaReadsFourFaces.lean'
    sections=[
        '# Revisão adversarial independente — B1′ / ORDEM 012',
        f'**Decisão: {decision}.** P0: {counts["P0"]}; P1: {counts["P1"]}; P2: {counts["P2"]}.',
        '[REAL — revisão desta sessão] Nenhum defeito encontrado no escopo condicional contratado. '
        'A aceitabilidade diz respeito à tipagem e à prova condicional. A equação de movimento é [INPUT], não experimento, '
        'nem resultado variacional. A integração continua fora desta revisão.',
        f'Revisor: {semantics["reviewer"]}. Escrita exclusiva em `{ROOT}`. '
        'Nenhum script autoral foi executado; os nove arquivos de controle foram copiados por bytes e executados pelo roteiro do revisor. '
        'A2, D1, canônico, um.py, Atlas, memórias e túnel não receberam escrita desta revisão.',
        '## Enunciado, hipóteses e circularidade',
        f'Fonte autoral: {link(origin,at=line(main_source,"theorem the_same_beta_reads_four_faces"))}; '
        f'cópia compilada: {link(main_source)}. `sources/` e `kernel/TGLExt/` do autor têm os mesmos bytes nos três arquivos novos.',
        'O tipo recebe `c : TGLCoupling` (0 < beta < 1), `D : ActionCouplingData X`, uma seção complexa `psi`, '
        '`hEOM : D.EOM c psi` e três densidades reais livres. Não exige solução não nula, curvatura não nula ou fonte não nula. '
        'A ausência dessas restrições é compatível com a formulação condicional pedida; impede interpretar o teorema como certificado de realização não trivial.',
        'A conclusão preserva literalmente as seis cláusulas internas de B1 e acrescenta '
        '`boxOperator psi − mass² • psi − xi • (R • psi) = c.beta • K_boundary psi`. '
        'A prova impressa é a aplicação direta `⟨the_same_beta_reads_three_faces c ρr ρm ρΛ, hEOM⟩`.',
        f'`modularSource` ({link(main_source,at=line(main_source,"def modularSource"))}) já define o termo modular com `c.beta`; '
        f'`EOM` ({link(main_source,at=line(main_source,"def EOM"))}) assume a igualdade correspondente. '
        '**A quarta face é, portanto, a reexposição definicional de hEOM.** Com B1 disponível, a conjunção tem o conteúdo lógico adicional exato da hipótese EOM. '
        'Não há ciclo de imports ou uso de B1′ para provar B1. Haveria circularidade se essa conclusão fosse usada para alegar que beta foi derivado/selecionado pela ação. '
        'A entrega e LIMITES já declaram corretamente essa fronteira.',
        '## ξ, gerador importado e fornecedores',
        '`xi` é campo real próprio; não é definido por beta e também não se exige desigualdade numérica. '
        '`K_boundary` é uma aplicação real linear total em todas as funções X → ℂ, sem prova de autoadjunção, domínio diferencial, afiliação ou relação com uma dinâmica modular. '
        '`boxOperator` também é dado; `scalarCurvature` é função real fornecida. Esses tipos não constroem um d’Alembertiano nem uma ação.',
        f'Fornecedores lidos: {link(K/"TGLExt"/"TheVerbalCoupling.lean")}, {link(K/"TGLExt"/"NoFullWitness.lean")}, '
        f'{link(K/"TGLExt"/"RhoPlusPClosure.lean")}, {link(ROOT/"inputs"/"suppliers"/"TheDammingByExpansion.lean")}, '
        f'{link(ROOT/"inputs"/"suppliers"/"TheImportedEquilibrium.lean")} e {link(ROOT/"inputs"/"suppliers"/"TowerModular.lean")}; '
        'B1 e as cópias disponíveis de B3/B4 foram confrontados. `EquilibriumInput.flow : A → A` e a conjugação matricial `towerFlow` '
        'não fornecem diretamente um gerador temporal nas seções da EOM. A ficha os marca como examinados, sem alegar consumo formal. '
        'B1 é o fornecedor formal efetivamente aplicado.',
        'B1 continua parametrizado por beta simbólico; alpha é beta/exp(1/2), não CODATA derivado. '
        'As cláusulas de fundo são álgebra; a perda exponencial exige tempo e gap positivos; a unicidade herdada identifica a taxa do semigrupo. '
        'Nada aqui escolhe uma rota cosmológica ou move gate.',
        '## Evidência de execução independente',
        f'- Lean medido: `{toolchain["version"]}`. Executável, SHA256 e ambiente: {link(ROOT/"TOOLCHAIN.json")}.',
        f'- {build["count"]}/{len(inputs["graph"])} fontes locais TGL/TGLExt recompilados de bytes em raiz nova, incluindo B1, B1′ e os teoremas dos controles. '
        f'{baseline["count"]} dependências coincidem com a bancada histórica B1. Nenhum .olean local autoral foi utilizado. '
        f'Comandos, rc, fontes, objetos e logs por módulo: {link(ROOT/"BUILD.json")}.',
        f'- {len(expected)} nomes autorais e {len(own_expected)} nomes novos do revisor com `#print axioms` efetivo: '
        '`propext`, `Classical.choice`, `Quot.sound` ou subconjunto. Ausência de nome reprova; nome fora do trio reprova. '
        f'Logs: {link(stdout)} e {link(own_stdout)}.',
        f'- {len(author["controls"])} controles autorais reexecutados; recusas semânticas por incompatibilidade de tipo e respectivas paredes recompiladas. '
        f'O quadro abaixo declara as condições exatas. Evidência: {link(ROOT/"AUTHOR_CONTROLS_RERUN.json")}.',
        f'- Controles próprios para beta e xi: casos positivos, caracterizações “se e somente se” e duas mutações negativas rejeitadas. '
        f'Fonte: {link(own_source)}; evidência: {link(ROOT/"INDEPENDENT_CONTROLS.json")}.',
        '- Verificação de comandos proibidos em todos os 47 fontes locais e nos controles próprios; comentários e strings não contam como comandos. '
        'Nenhum numeral beta foi introduzido. Os três módulos novos não alteram maxHeartbeats; opções herdadas estão em SOURCE_SCAN.json.',
        'A Mathlib e os pacotes auxiliares são **cache de terceiros lido**, não build dos fontes nesta revisão. '
        'Os nove HEADs de pacotes coincidem com lake-manifest; isso não comprova recompilação nem autentica todos os objetos transitivos. '
        'O cache Cli não tem diretório de build e não foi incluído no LEAN_PATH. As dependências efetivamente exigidas resolveram sem ele.',
        '## Os nove controles, relidos semanticamente',
        '| Controle | Teorema de impossibilidade / limite | Condições |\n|---|---|---|',
    ]
    for row in author['controls']:
        basis=row['semantic_basis']
        sections.append(f'| {row["name"]} | `{basis["wall"]}` | {basis["conditions"]} |')
    sections += [
        'As sondas genéricas não declaram que qualquer troca seja falsa em todo dado degenerado. '
        'As paredes fornecem as hipóteses sob as quais ela é falsa. A recusa isolada de `exact hEOM` apenas rejeita aquele termo; '
        'a prova da parede, com modelo não nulo disponível, é o suporte semântico usado neste parecer.',
        '## Controles do revisor',
        '`fixedData c xi` fixa `box=(xi+beta)•id`, massa zero, curvatura unitária e K=id, com seção unitária não nula. '
        '`beta_change_iff` prova que trocar apenas o coeficiente modular preserva a igualdade exatamente quando b=beta. '
        '`xi_change_iff` prova que trocar apenas xi, conservando box/K/curvatura/massa, preserva EOM exatamente quando eta=xi. '
        'Os casos iguais compilam; as tentativas de reutilizar a prova para valores distintos são rejeitadas e têm paredes independentes.',
        '`zero_field_eom` demonstra a possibilidade de vacuidade do campo zero; `equal_roles_admitted` mostra que papéis independentes permitem xi=beta acidentalmente. '
        '`fourth_projection` extrai precisamente EOM do teorema principal. São controles algébricos; nenhum é experimento ou solução física.',
        '## P0 / P1 / P2 e limites do aceite',
        f'P0={counts["P0"]}, P1={counts["P1"]}, P2={counts["P2"]}. Nenhuma correção obrigatória ao autor no contrato delimitado. '
        'O1–O4 em SEMANTICA_REVISOR.json são limites explícitos já declarados, não defeitos artificialmente contados. '
        'O parecer permite tratar o candidato como teorema condicional para posterior incorporação. '
        '`ext_pb_same_beta_four_faces_kernel_proved` continua proposta; a checagem futura deve preservar “EOM assumida; K importado; xi livre”. '
        'A revisão não instalou bandeira nem aprovou realização da EOM pela natureza.',
        '**[DECLARADO_do_adendo] Artigo A:** a consulta a `C:\\IALD\\Artigo\\Haja_Luz` foi negada pelo filesystem. '
        'Não foi lido nem hasheado o artigo original. A atribuição da EOM e de xi=1/6 ao artigo é somente a do §4 do adendo, '
        f'efetivamente lido e preservado. Registro: {link(ROOT/"PRIMARY_ACCESS.json")}.',
        '## Tentativas e integridade',
        'Uma falha inicial de preparação detectou o diretório ausente do cache Cli antes de compilar qualquer fonte; '
        'foi corrigida retirando somente caminhos inexistentes da busca, com registro DEV_SETUP_FAILURE.json. '
        'Uma tentativa de edição de script via shell foi rejeitada pelo parser do PowerShell, sem escrita; a edição foi aplicada depois com backup de bytes. '
        'Logs e snapshots de qualquer tentativa própria que falhou ficam preservados sob independent_logs e não entram nos gates de aprovação. '
        'Os logs de desenvolvimento do autor não foram usados como prova.',
        f'Todos os {len(origin_checks)} registros de origem copiados foram rechecados em bytes: '
        f'{link(ROOT/"INTEGRIDADE_ORIGENS_REVISOR.json")}. A comparação não afirma o estado de casas inacessíveis nem de trabalho concorrente.',
        'A decisão foi calculada por finalize_review.py a partir dos gates medidos e da avaliação semântica nomeada do revisor, '
        'sem aproveitar literais autorais como `all_semantic` ou `all_axioms_subset_of_trio` como aprovação. '
        'Os testes do finalizador rejeitam nome ausente, axioma estranho e lista vazia de requisitos; normalizam os sufixos de universo.',
        '## Arquivos de evidência — SHA256 e bytes lidos',
        'Os caminhos abaixo são absolutos. INPUTS.json contém os caminhos de origem e cópia; MANIFESTO_REVISAO.json inventaria por arquivo '
        'os fontes, relatórios, logs, controles e objetos locais finais. SELO_REVISAO.json sela o manifesto sem hash autocircular.',
        '| Arquivo | Bytes | SHA256 |\n|---|---:|---|'
    ]
    for p in evidence:
        item=info(p)
        sections.append(f'| {link(p)} | {item["bytes"]} | `{item["sha256"]}` |')
    rendered=re.sub(r'(\|)\n\n(?=\|)',r'\1\n','\n\n'.join(sections))
    write(ROOT/'REVISAO_B1_PRIME.md',rendered+'\n')
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name not in ['MANIFESTO_REVISAO.json','SELO_REVISAO.json']:
            files.append(info(p))
    record(ROOT/'MANIFESTO_REVISAO.json',dict(created_utc=stamp(),root=str(ROOT),files=files,count=len(files),
        excludes=['MANIFESTO_REVISAO.json','SELO_REVISAO.json']))
    record(ROOT/'SELO_REVISAO.json',dict(created_utc=stamp(),decision=decision,
        files=[info(ROOT/n) for n in ['MANIFESTO_REVISAO.json','REVISAO_B1_PRIME.md','AUDITORIA_INDEPENDENTE.json']]))
    print(json.dumps(dict(decision=decision,checks=checks,findings=counts,author_names=len(expected),
        independent_names=len(own_expected),report=info(ROOT/'REVISAO_B1_PRIME.md')),ensure_ascii=False,indent=2))
    if not all(checks.values()): sys.exit(1)

if __name__=='__main__': main()
