from review import *

def normalize(s): return re.sub(r'\.\{[^}]*\}','',s.strip())
def axioms(s):
    pairs=[]
    for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",s,re.S):
        pairs.append((normalize(m[1]),[normalize(a) for a in m[2].split(',') if a.strip()]))
    for m in re.finditer(r"'([^']+)' does not depend on any axioms",s): pairs.append((normalize(m[1]),[]))
    return pairs
def output(r): return ''.join(Path(r[k]['path']).read_text(encoding='utf-8') for k in ['stdout','stderr'])
def check_audit(row,names):
    pairs=axioms(output(row)); found=dict(pairs)
    missing=sorted(set(names)-set(found)); extra=sorted(set(found)-set(names))
    foreign={n:a for n,a in found.items() if not set(a)<=ALLOWED}
    return dict(result=row,expected=names,actual=found,missing=missing,extra=extra,foreign=foreign,
        passed=row['returncode']==0 and len(pairs)==len(names)==len(found) and not missing and not extra and not foreign)
def link(p,label=None):
    p=Path(p); return f'[{label or p.name}](<{p.as_posix()}>)'

def main():
    d=read(ROOT/'INPUTS.json'); a=read(ROOT/'ASSEMBLY_INPUTS.json')
    b=read(ROOT/'BUILD.json'); ab=read(ROOT/'ASSEMBLY_BUILD.json')
    fa=read(ROOT/'FINAL_AUDIT.json'); c=read(ROOT/'CONTROLS.json'); ac=read(ROOT/'ASSEMBLY_CONTROLS.json')
    tc=read(ROOT/'TOOLCHAIN.json')
    public=check_audit(fa['result'],fa['names'])
    first=check_audit(b['audit'],d['public_names'])
    own=[check_audit(c['audit'],c['names']),check_audit(ac['audit'],ac['names'])]
    all_own={n:v for row in own for n,v in row['actual'].items()}
    negatives=c['negative_controls']+ac['negative_controls']
    for row in negatives:
        text=output(row)
        row['rechecked_rejection']=row['returncode']!=0 and 'Type mismatch' in text and not re.search(
            r'unknown (identifier|constant|namespace|module)|unexpected token|object file .*does not exist',text,re.I)
        anchor=row.get('wall',row.get('positive_anchor'))
        row['anchor_verified']=anchor in all_own and set(all_own[anchor])<=ALLOWED
    snapshots=d['snapshots']+a['snapshots']
    source_integrity=[dict(**r,source_current=current(r['source']),copy_current=current(r['copy'])) for r in snapshots]
    cache=d['cache_links']+a['A2_reused_objects']
    cache_integrity=[dict(**r,source_current=current(r['source']),borrowed_current=current(r['borrowed']),
        review_current=current(r['review']),same_file=os.path.samefile(r['borrowed']['path'],r['review']['path'])) for r in cache]
    history=[d['prior_receipt'],d['prior_seal'],d['historical_math_review_seal'],a['prior_delta_seal']]
    old_seals=[read(PRIOR/'SELO_A2.json'),read(PRIOR/'DELTA01/SELO_DELTA01.json'),read(ROOT.parent/'SELO_DOCUMENTAL.json')]
    history_ok=all(current(r) for r in history) and all(current(r) for s in old_seals for r in s['files'])
    modules={**b['modules'],**ab['modules']}
    runs=list(modules.values())+[b['audit'],ab['discovery'],fa['result'],c['positive'],c['audit'],ac['positive'],ac['audit']]+negatives
    records_ok=all(current(r[k]) for r in runs for k in ['source','stdout','stderr'])
    objects_ok=all(current(r['object']) for r in runs if r.get('object'))
    code=(SRC/'TGLExt/V354PositiveShiftCompatibility.lean').read_text(encoding='utf-8')
    headers=[code.split('theorem '+name,1)[1].split(':=',1)[0] for name in ['positiveShift_trace_compatible','cyclicTraceCandidate_positive']]
    headers_no_compatible=not any(re.search(r'\bcompatible\b',h) for h in headers)
    all_code=[code_only(Path(r['copy']['path']).read_text(encoding='utf-8')) for r in snapshots]
    own_code=[code_only((SRC/n).read_text(encoding='utf-8')) for n in ['IndependentCompatibilityControls.lean','IndependentAssemblyControls.lean']]
    forbidden=[x for text in all_code+own_code for x in re.findall(
        r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',text,re.M)]
    shared=d['shared_polar']
    shared_ok=all(current(shared[k]) for k in ['original','author_copy','independent_copy']) and len({shared[k]['sha256'] for k in ['original','author_copy','independent_copy']})==1
    gates=dict(eleven_fresh_modules=len(modules)==11 and all(r['returncode']==0 and r.get('object') and r['source_unchanged'] for r in modules.values()),
        complete_export_coverage=public['passed'] and set(fa['explicit_names'])<=set(fa['names']),
        initial_35_audit=first['passed'],own_positive_anchors=c['positive']['returncode']==0 and ac['positive']['returncode']==0 and all(x['passed'] for x in own),
        six_motivated_negatives=len(negatives)==6 and all(r['rechecked_rejection'] and r['anchor_verified'] for r in negatives),
        no_compatible_premise_in_final_statements=headers_no_compatible,new_sources_clean=not forbidden,
        sources_frozen_unchanged=all(r['source_current'] and r['copy_current'] for r in source_integrity),
        shared_polar_exact=shared_ok,cache_readonly_unchanged=all(r['source_current'] and r['borrowed_current'] and r['review_current'] and r['same_file'] for r in cache_integrity),
        history_preserved=history_ok,source_log_object_integrity=records_ok and objects_ok,
        lean431='version 4.31.0,' in tc['version'] and current(tc['lean']))
    passed=all(gates.values())
    findings=[] if passed else [dict(priority='P1',gate=k,status='FAILED') for k,v in gates.items() if not v]
    decision='VERIFICADO_COMPATIBILIDADE_MONTAGEM_LEGADA_E_SUSY_MINIMO' if passed else 'NAO_ACEITAVEL_NESTA_RODADA'
    identity=dict(name='Carver',agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0',provenance='INPUT supplied by principal',role='independent reviewer, not author')
    scopes=dict(positive_compatibility='PROVED_NO_COMPATIBLE_PREMISE',positive_reader='EQUAL_TO_A1_ON_ALL_POSITIVES_INCLUDING_INFINITY',
        bounded_polar='CONSTRUCTED_INSIDE_SAME_VON_NEUMANN_ALGEBRA',ContinuousCoreData='EXACT_LEGACY_TYPE_TERM',
        ThreeLocksCoreData='EXACT_LEGACY_TYPE_VIA_threeLocksFromSupport',FullTGLWitness='DEPENDENT_SUM_TERM_NOT_ONLY_NONEMPTY',
        SusyRelativeData='CONCRETE_FULL_PROJECTION_LATTICE_SAME_CORE_AND_A1',
        H3Lt='1-PF_MINIMAL_BOUNDED_REPRESENTATIVE',PF='regularFiniteSupport_mixProfile',
        susy_D='regularMinimalLock',susy_D0='1',susy_diff='PF',susy_gapD='projker_Hmin',susy_gapD0='projker_1=0',
        standard_bounded_transform_identification='NOT_PROVED_NOT_REQUIRED_BY_RECORD_FIELDS',microscopic_identification='NOT_PROVED',
        U='TRIVIAL_LEGACY_REPRESENTATION',new_BW='NOT_PROVED',global_complex_linearity='NOT_ASSERTED',
        global_additivity='NOT_A_PROPERTY_OF_THIS_TOTAL_READER',physical_confirmation=False,canonical_integration=False,gate_changed=False,entire_adendo_accepted=False)
    failed_dev=read(ROOT/'controls_logs/positive/RESULT.json')
    record(ROOT/'INTEGRIDADE_FINAL.json',dict(source_integrity=source_integrity,cache_integrity=cache_integrity,history=history,history_ok=history_ok))
    # Sources of interfaces are read-only suppliers, not new builds or reaudited A1 proofs.
    provider_entries=[]
    providers=[(BASE/'TGLExt/V350PositiveRootIntertwining.lean',None),
        (BASE/'TGLExt/SusyRelativeGap.lean',None),(BASE/'TGLExt/LocalBreuerGap.lean',(1,140)),
        (PRIOR/'src/TGL/CoreSupport.lean',(67,127)),(BASE/'TGL/ModularRealization.lean',(40,137)),
        (BASE/'TGLExt/WedgeNet.lean',(354,363)),(BASE/'TGLExt/V350WedgeModularData.lean',(68,81)),
        (BASE/'TGLExt/WitnessV3.lean',(232,244))]
    for p,span in providers:
        raw=p.read_bytes(); piece=raw if span is None else b''.join(raw.splitlines(keepends=True)[span[0]-1:span[1]])
        q=ROOT/'inputs/interfaces'/(p.stem+('_full' if span is None else f'_{span[0]}_{span[1]}')+'.txt'); write(q,piece)
        provider_entries.append(dict(source=info(p),scope='full' if span is None else dict(first=span[0],last=span[1]),excerpt=info(q),rebuilt=False))
    report=dict(created_utc=stamp(),decision=decision,reviewer_identity=identity,gates=gates,
        findings=findings,counts={p:sum(f['priority']==p for f in findings) for p in ['P0','P1','P2']},
        sources_compiled=len(modules),modules=modules,public_axioms=public,explicit_name_count=len(fa['explicit_names']),
        additional_exports=fa['generated_names'],own_axioms=own,negative_controls=negatives,
        cache_counts=dict(A1=len(d['cache_links']),A2_CoreSupport=len(a['A2_reused_objects'])),
        mathematical_scope=scopes,interfaces=provider_entries,shared_polar=shared,
        final_statement_headers=headers,invalid_dev_attempt=dict(result=failed_dev,
            reason='Own ext tactic consumed the one-dimensional goal before binding x; corrected with ContinuousLinearMap.ext. Failed attempt is not proof.'),
        history=history,toolchain=tc)
    record(ROOT/'AUDITORIA_FINAL_INDEPENDENTE.json',report)
    if not passed: print(json.dumps(gates,indent=2)); raise RuntimeError('No acceptance receipt: gate failed')
    paragraphs=[
        '# Recibo independente — compatibilidade, montagem legada e SUSY concreto',
        f'**[REAL — compilação e auditoria independentes] {decision}. P0=0; P1=0; P2=0 no lote e alcance abaixo.**',
        '**Carver — agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`**, convocado pela principal no escopo autorizado, revisor independente e não autor. Identidade fornecida pela principal [INPUT] e registrada no JSON. Nenhum outro usuário é apresentado como aprovador.',
        f'Foram compilados de cópias próprias **11 módulos**: sete da compatibilidade (incluindo o polar compartilhado), a montagem final e três módulos SUSY. Todos rc0 com `{tc["version"]}`. O diretório {link(ROOT)} conserva o nome inicial COMPATIBILIDADE_7; a ampliação para onze está registrada em ASSEMBLY_INPUTS.json e neste recibo.',
        f'Foram auditados **{len(fa["explicit_names"])} nomes declarados explicitamente + {len(fa["generated_names"])} exportações adicionais = {len(fa["names"])} nomes**, todos com axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`. A união das listas autorais é 58: 40 da principal e 29 de SUSY com 11 do polar compartilhados. A descoberta no ambiente compilado acrescentou `TGLV354.instBoundedOrderCoreProjection` e `TGLV354.boundedPolar.congr_simp`, ambas também auditadas. O log final contém tipos, corpos e axiomas de todos os sessenta.',
        'A compatibilidade positiva foi efetivamente construída: `positiveShift_trace_compatible` recebe P, positivos p/q e ShiftRelated no mesmo core; não recebe compatible, traço cíclico total ou testemunha de polar. `cyclicTraceCandidate_positive` aplica essa prova e concorda com A1 em TODO positivo, inclusive valores infinitos. O auxiliar condicional anterior continua como lema consumido, com sua premissa agora fornecida; isso não é circularidade nem uma hipótese escondida no teorema final.',
        'O polar é definido pela extensão de |r|x↦rx ao fecho da imagem, seguida de projeção ortogonal; a igualdade de normas justifica a extensão. São provados produto com |r|, núcleo, ambos os suportes, comutação e pertença ao mesmo von Neumann algebra via bicomutante. Os lemas de potência requerem n>0 e auto-adjunção, sem dimensão finita ou imagem fechada. A passagem de entrelaçamento usa densidade e anulação no núcleo, sem cancelar |r|. As inclusões dos suportes são usadas corretamente; não se impõe igualdade indevida com os suportes dos endpoints.',
        'O transporte do traço constrói a=u√q no mesmo core. De p=uqu* e (u*u)q=q obtém a*a=q e aa*=p, consumindo uma vez a tracialidade quadrática A1. O private asCore apenas empacota o operador positivo com a pertença existente. Nenhuma escolha Classical inventa uma testemunha analítica sem prova.',
        '**A montagem habita os tipos antigos exatos.** `regularLegacyCore` fornece ContinuousCoreData com o core regular de mixProfile, embedding injetivo, ação dual existente e leitor cíclico. `regularLegacyThreeLocks` aplica threeLocksFromSupport aos PF e faces já pagos; as leituras são transportadas do leitor novo para A1 antes de usar normalização, aditividade do split e igualdade das faces. `regularModularRealization` fornece o pacote dependente com Hilbert infinito do fornecedor existente. `regularFullWitness` é o termo Σ de FullTGLWitness; não é somente Nonempty ou uma flag.',
        '`regularLegacyThreeLocks_concrete` identifica por rfl os campos PF e H3Lt com regularFiniteSupport e regularMinimalLock. A sonda própria confirmou H3Lt=1−PF e traço do PF montado igual a um. O grafo limitado afiliado e o gap relativo de norma vêm dos 33 já pagos, agora ligados ao campo concreto. A glosa antiga “transformada limitada” não acrescenta uma equação H3Lt=H/√(1+H²); tal identificação padrão e uma origem microscópica não foram demonstradas por esta montagem.',
        '**SUSY usa projeções reais do mesmo N e o peso A1.** CoreProjection abrange todos os subespaços fechados invariantes pelo comutante; operator_mem e ofOperator/operator_ofOperator dão o vínculo com todas as projeções de N. A ordem é a inclusão, o supremo é o fecho da soma e o ínfimo a interseção. O polar de (1−q)p fornece a comparação do join, com u*u≤p e uu*=p∨q−q; tracialidade, aditividade positiva e monotonicidade de A1 dão a subaditividade. Não se presume p e q comutantes.',
        '`regularSusyData` é um termo de SusyRelativeData sobre esse reticulado: ker=gapD=diff=PF e gapD0=⊥. Finitude e não nulidade vêm do suporte construído, e o consumidor susy_relative_gives_breuer é aplicado efetivamente. As identificações demonstram ker e gapD como projker(Hmin), gapD0 como projker(1), diff=1−Hmin=PF, gap relativo um e traço do kernel um. A inclusão reticular gap_relative é simples porque gapD=diff: é uma instanciação concreta usando fatos já pagos, não uma nova prova de perturbatividade microscópica ou de um teorema geral de Weyl. modelSusy em ENNReal não foi usado como substituto.',
        '**Limites do aceite:** W é theSpecificAQFTWitness existente, com U:=fun _=>1; a própria sonda verificou essa identidade. Os dados modulares usam o fluxo e a conjugação da torre existentes, sem nova prova BW ligando-os a uma representação geométrica não trivial. O leitor total é cíclico e coincide com A1 no cone; aditividade ou linearidade complexa globais não são campos preenchidos nem consequências. SusyRelativeData reticular não codifica por si só um operador microscópico. Não há confirmação física, mudança de gate, integração canônica ou aceite do adendo inteiro.',
        f'**Sondas novas:** {len(c["names"])+len(ac["names"])} nomes próprios de controle positivo/tipos foram compilados e auditados no trio; seis adulterações recusadas semanticamente. Três cobrem leitura unitária anulada, suporte polar incorreto e lag zero; três cobrem traço do PF montado adulterado para 2, gap SUSY zerado e modelSusy numérico passado ao tipo concreto. A última é separação de tipos; as demais têm paredes positivas não nulas/não iguais. Os controles dos 33 não foram refeitos. A primeira tentativa de um controle próprio falhou por elaboração de ext e está preservada, sem valor de prova.',
        f'**Reaproveitamento declarado:** {len(d["cache_links"])} objetos A1 e {len(a["A2_reused_objects"])} objetos da revisão aceita de A2/CoreSupport foram ligados apenas para leitura. Mathlib entrou como cache. Nenhum A1, dos oito V354 antigos ou CoreSupport foi recompilado ou sobrescrito nesta rodada. O polar compartilhado foi comparado byte a byte com a fonte Poincare e recompilado aqui uma única vez para os dois consumidores. Históricos dos lotes 35/33 e do parecer matemático permanecem intactos.',
        f'Comandos, logs, objetos, rc, hashes e bytes: {link(ROOT/"AUDITORIA_FINAL_INDEPENDENTE.json")}, {link(ROOT/"INTEGRIDADE_FINAL.json")} e {link(ROOT/"MANIFESTO_FINAL.json")}. Os hashes a seguir foram lidos dos fontes autorais efetivamente copiados; a auditoria usa as cópias e objetos próprios, sem converter rc autoral em prova independente.',
    ]
    table=['| Fonte autoral congelado | Bytes | SHA-256 |','|---|---:|---|']
    for r in snapshots:
        s=r['source']; table.append(f'| {link(s["path"])} | {s["bytes"]} | `{s["sha256"]}` |')
    paragraphs.append('\n'.join(table))
    paragraphs.append(f'Selo deste recibo: {link(ROOT/"SELO_FINAL.json")}. A aprovação é calculada dos gates em AUDITORIA_FINAL_INDEPENDENTE.json e limitada às hipóteses e tipos descritos acima.')
    write(ROOT/'RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md','\n\n'.join(paragraphs)+'\n')
    cache_paths={Path(r['review']['path']) for r in cache}; files=[]; fresh=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p in cache_paths or p.name in ['MANIFESTO_FINAL.json','SELO_FINAL.json'] or 'tmp' in p.relative_to(ROOT).parts: continue
        (fresh if p.suffix=='.olean' else files).append(info(p))
    record(ROOT/'MANIFESTO_FINAL.json',dict(created_utc=stamp(),files=files,new_objects=fresh,sources=snapshots,history=history,
        cache_index=info(ROOT/'INTEGRIDADE_FINAL.json'),interfaces=provider_entries))
    record(ROOT/'SELO_FINAL.json',dict(created_utc=stamp(),decision=decision,reviewer_identity=identity,
        files=[info(ROOT/n) for n in ['RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md','AUDITORIA_FINAL_INDEPENDENTE.json','MANIFESTO_FINAL.json']]))
    assert all(current(r) for r in files+fresh+read(ROOT/'SELO_FINAL.json')['files'])
    print(json.dumps(dict(decision=decision,gates=gates,public_names=len(fa['names']),fresh_modules=len(modules),
        controls=len(negatives),receipt=info(ROOT/'RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md')),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
