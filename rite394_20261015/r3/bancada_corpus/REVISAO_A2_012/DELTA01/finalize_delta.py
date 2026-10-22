from review_delta import *


def normalize(s):
    return re.sub(r'\.\{[^}]*\}', '', s.strip())


def parse_axioms(s):
    pairs = []
    for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", s, re.S):
        pairs.append((normalize(m[1]), [normalize(a) for a in m[2].split(',') if a.strip()]))
    for m in re.finditer(r"'([^']+)' does not depend on any axioms", s):
        pairs.append((normalize(m[1]), []))
    return pairs


def link(p, label=None):
    p = Path(p)
    return f'[{label or p.name}](<{p.as_posix()}>)'


def output(row):
    return ''.join(Path(row[k]['path']).read_text(encoding='utf-8') for k in ['stdout', 'stderr'])


def main():
    d = read(ROOT/'DELTA_COMPARISON.json')
    b = read(ROOT/'BUILD_DELTA01.json')
    tc = read(ROOT/'TOOLCHAIN.json')
    expected = d['remaining_names']
    snapshots = [dict(**r, source_current=current(r['source']), copy_current=current(r['copy'])) for r in d['snapshots']]
    history = read(PRIOR/'MANIFESTO_A2.json')
    history_rows = history['files'] + history['new_objects'] + read(PRIOR/'SELO_A2.json')['files']
    history_checks = [dict(file=r, unchanged=current(r)) for r in history_rows]
    cache_checks = [dict(**r, source_current=current(r['source']), borrowed_current=current(r['borrowed_from']),
        review_current=current(r['review']), same_file=os.path.samefile(r['borrowed_from']['path'], r['review']['path']))
        for r in d['cache_links']]
    sources_exact = []
    for row in d['changes']:
        old = Path(row['before']['path']).read_bytes()
        new = Path(row['after']['path']).read_bytes()
        expected_bytes = prune_expected(old, row['removed_name'])[0] if 'removed_name' in row else old
        sources_exact.append(dict(module=row['module'], before=row['before'], after=row['after'],
            bytes_exact=expected_bytes == new, before_current=current(row['before']), after_current=current(row['after'])))
    live_audit = SRC/'TGLExt'/'AuditA2RegularSupport.lean'
    old_audit = Path(d['author_audit_backup'][0]['path']).read_bytes()
    for name in QUALIFIED:
        needle = ('#print axioms '+name+'\n').encode()
        assert old_audit.count(needle) == 1
        old_audit = old_audit.replace(needle, b'', 1)
    audit_source_exact = old_audit == live_audit.read_bytes()
    current_source_names = []
    for row in d['changes']:
        current_source_names += ['TGLV350.Regular.'+n for n in re.findall(
            r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+(\w+)',
            Path(row['after']['path']).read_text(encoding='utf-8'), re.M)]
    source_name_set_ok = len(current_source_names) == 33 and len(set(current_source_names)) == 33 and set(current_source_names) == set(expected)
    audit_prints = re.findall(r'^#print axioms\s+(\S+)', live_audit.read_text(encoding='utf-8'), re.M)
    audit_names = read(ROOT/'inputs'/'AUDIT_NAMES_DELTA01.json')['names']
    expected_name_set_ok = set(expected) == set(d['old_names'])-set(QUALIFIED) and len(d['old_names']) == 35
    active_audits_ok = len(audit_prints) == len(audit_names) == 33 and set(audit_prints) == set(audit_names) == set(expected)
    audited = {}
    for name, row in b['audits'].items():
        pairs = parse_axioms(output(row))
        found = dict(pairs)
        missing = sorted(set(expected)-set(found))
        unexpected = sorted(set(found)-set(expected))
        foreign = {n: a for n, a in found.items() if not set(a) <= ALLOWED}
        audited[name] = dict(result=row, actual=found, missing=missing, unexpected=unexpected,
            foreign=foreign, count=len(pairs), passed=row['returncode'] == 0 and len(pairs) == 33
            and len(found) == 33 and not missing and not unexpected and not foreign)
    removed = b['removed_name_check']
    diagnostics = output(removed)
    absent = [n for n in QUALIFIED if re.search(r'Unknown (?:identifier|constant)[^\n]*'+re.escape(n), diagnostics, re.I)]
    removed_ok = removed['returncode'] != 0 and set(absent) == set(QUALIFIED) and not re.search(
        r'unknown module|object file .*does not exist|unexpected token', diagnostics, re.I)
    runs = list(b['modules'].values()) + list(b['audits'].values()) + [removed]
    records_current = all(current(r[k]) for r in runs for k in ['source', 'stdout', 'stderr'])
    objects_current = all(current(r['object']) for r in runs if r.get('object'))
    prior = read(PRIOR/'AUDITORIA_A2_INDEPENDENTE.json')
    gates = dict(
        exact_requested_removals=all(r['bytes_exact'] and r['before_current'] and r['after_current'] for r in sources_exact),
        remaining_33_preserved=source_name_set_ok and expected_name_set_ok,
        active_audit_exact_removals=audit_source_exact and active_audits_ok,
        eight_affected_modules_built=len(b['modules']) == 8 and set(b['modules']) == set(d['affected_modules'])
            and all(r['returncode'] == 0 and r['object'] and r['source_unchanged'] for r in b['modules'].values()),
        both_complete_axiom_audits=len(audited) == 2 and all(a['passed'] for a in audited.values()),
        removed_names_absent_in_fresh_environment=removed_ok,
        lean_431='version 4.31.0,' in tc['version'] and current(tc['lean']),
        author_and_review_snapshots_unchanged=all(r['source_current'] and r['copy_current'] for r in snapshots),
        cached_objects_readonly_unchanged=all(r['source_current'] and r['borrowed_current'] and r['review_current'] and r['same_file'] for r in cache_checks),
        prior_lot35_artifacts_preserved=all(r['unchanged'] for r in history_checks) and all(current(r) for r in d['prior_receipt_pins']),
        prior_semantic_review_passed=all(prior['gates'].values()) and prior['findings_counts']['P0'] == 0 and prior['findings_counts']['P1'] == 0,
        fresh_sources_logs_objects_current=records_current and objects_current)
    passed = all(gates.values())
    findings = [] if passed else [dict(priority='P1', gate=k, result='FALHOU') for k, v in gates.items() if not v]
    p2_status = 'QUITADO' if passed else 'NAO_QUITADO'
    decision = 'DELTA01_VERIFICADO__33_PRESERVADOS__P2_01_QUITADO' if passed else 'DELTA01_NAO_ACEITAVEL'
    identity = d['reviewer_identity']
    integrity = dict(snapshots=snapshots, exact_source_comparison=sources_exact,
        history_checks=history_checks, cached_objects=cache_checks, created_utc=stamp())
    record(ROOT/'INTEGRIDADE_DELTA01.json', integrity)
    author_result = AUTHOR/'delta01_build'/'RESULT.json'
    author_build_info = None
    if author_result.exists():
        write(ROOT/'inputs'/'AUTHOR_DELTA01_BUILD_RESULT.json', author_result.read_bytes())
        author_build_info = dict(source=info(author_result), copy=info(ROOT/'inputs'/'AUTHOR_DELTA01_BUILD_RESULT.json'),
            role='Registro autoral consultado somente como proveniencia; nao participa dos gates independentes')
    report = dict(decision=decision, created_utc=stamp(), reviewer_identity=identity, gates=gates,
        findings=findings, counts={p:sum(f['priority'] == p for f in findings) for p in ['P0', 'P1', 'P2']},
        P2_01=p2_status, prior_receipt_unchanged=d['prior_receipt_pins'], old_names=d['old_names'],
        removed_names=QUALIFIED, remaining_names=expected, current_count=len(expected), audits=audited,
        changed_modules=d['changed_modules'], freshly_built_modules=b['modules'],
        unchanged_CoreSupport_reused=d['reused_core_support'], cache_count=len(cache_checks),
        cache_is_not_source_build=True, removed_name_check=dict(result=removed, verified_absent=absent, passed=removed_ok),
        semantic_controls=dict(rerun=False, changed=False, reason='Exclusao estrita de duas especializacoes sem consumidor; demais provas byte-identicas.',
            evidence=info(PRIOR/'CONTROLS.json'), historical_receipt=info(PRIOR/'RECIBO_REVISAO_A2.md')),
        full_A2_or_adendo_accepted=False, ThreeLocksCoreData_constructed=False, FullWitness_constructed=False,
        legacy_total_trace_adapter='OPEN', SusyRelativeData_same_core=dict(status='OPEN_DECLARADO_PELA_PRINCIPAL',
            certified_by_this_delta=False, modelSusy_ENNReal_not_a_substitute=True),
        mathematical_scope='Preserva o representante minimo, suporte espectral de traco A1 um, gap relativo, afiliacao, CCW e parede do reader; sem ampliacao.',
        toolchain=tc, author_build_provenance_only=author_build_info)
    record(ROOT/'AUDITORIA_DELTA01.json', report)
    if not passed:
        print(json.dumps(gates, indent=2)); raise RuntimeError('No acceptance receipt: independent gate failed')
    text = [
        '# Recibo aditivo de revisão independente — A2 Delta01, lote 33',
        f'**[REAL — medido nesta revisão] {decision}. P0=0; P1=0; P2=0 neste delta. P2-01: {p2_status}.**',
        '**Carver — agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`**, convocado pelo agente principal no escopo autorizado; revisor independente, não autor. Identidade fornecida pela principal [INPUT], registrada também no JSON. Nenhum outro usuário é apresentado como aprovador.',
        f'O recibo de 35 nomes permanece intacto em {link(PRIOR/"RECIBO_REVISAO_A2.md")}, incluindo o P2 histórico. Este recibo acrescenta o resultado do delta de poda; não substitui nem reescreve a história. Escrita desta rodada exclusivamente em `{ROOT}`.',
        'Foram removidas exatamente as declarações `scalarTrace_finite_positive_seed` e `scalarTrace_finite_projection_exists`, seus dois `#print axioms` nos módulos e os dois nomes no Audit ativo. A comparação com as cópias seladas de 35 nomes confirmou igualdade byte a byte após somente essas exclusões. Os seis outros V354 não mudaram. Os backups autorais correspondem aos bytes anteriores.',
        'O conjunto público atual contém exatamente os 33 nomes anteriores menos os dois removidos. Os enunciados e corpos de prova restantes foram preservados, sem consumidor artificial. Os dois auxiliares gerais usados pela cadeia em e11 continuam presentes. Os módulos que os fornecem continuam necessários.',
        f'Diffs verificáveis: {link(ROOT/"diffs"/"V354FiniteTraceSupport.diff")}, {link(ROOT/"diffs"/"V354SpectralThreshold.diff")} e {link(ROOT/"diffs"/"AuditA2RegularSupport.diff")}. Comparação e grafo: {link(ROOT/"DELTA_COMPARISON.json")}.',
        f'Compilador medido: `{tc["version"]}`. Executável: `{tc["lean"]["path"]}`; {tc["lean"]["bytes"]} bytes; SHA-256 `{tc["lean"]["sha256"]}`.',
        'A remoção afeta transitivamente os oito V354. Todos os oito foram recompilados de fontes próprios com rc0, sem objetos V354 antigos no ambiente. Também compilaram com rc0 o Audit autoral copiado e o Audit independente que enumera todos os 33 nomes. São oito módulos matemáticos e dois auditores; não se conta o cache como compilação.',
        'Ambos os auditores imprimiram os 33 nomes, sem ausentes, duplicados ou axiomas fora de `{propext, Classical.choice, Quot.sound}`. A fonte própria `RemovedNamesAbsent.lean` teve as duas consultas recusadas por nome desconhecido no ambiente recém-compilado. Essas recusas comprovam ausência das declarações; não são provas matemáticas nem falhas de importação.',
        f'Evidência completa de execução: {link(ROOT/"BUILD_DELTA01.json")}; axiomas e gates: {link(ROOT/"AUDITORIA_DELTA01.json")}. Cada execução registra comando, raiz, fonte, objeto, rc, tempo e logs com SHA-256 e bytes.',
        f'CoreSupport não mudou: reutilizou-se o objeto compilado independentemente na revisão de 35 nomes, após conferir fonte e objeto. As dependências A1 aceitas e esse objeto totalizam {len(cache_checks)} hardlinks usados somente para leitura. Mathlib foi cache. Nenhum A1 ou CoreSupport foi recompilado nesta rodada, nenhum objeto emprestado foi sobrescrito. A integridade pós-build foi medida em {link(ROOT/"INTEGRIDADE_DELTA01.json")}.',
        'Os controles semânticos próprios da revisão de 35 nomes permanecem preservados e não foram alterados nem reexecutados. O delta não altera hipótese, enunciado ou prova restante; os testes desta rodada limitam-se à exclusão exata, recompilação dos dependentes, cobertura completa de axiomas e ausência efetiva dos nomes removidos.',
        'O alcance matemático do recibo anterior permanece: suporte não nulo, traço A1 igual a um, split igual e ortogonal, projeção do kernel de 1−PF igual a PF, gap um no complemento do kernel e afiliação do representante mínimo. CCW usa o reader que coincide com A1 em todos os positivos; sua extensão por zero fora do cone continua não cíclica e não fornece o traço total legado.',
        '**Não é aceite integral de A2/ORDEM011 nem do adendo.** O totalizador Core→ENNReal com as leis antigas permanece [OPEN]; ThreeLocksCoreData e FullWitness não estão certificados como construídos. W/D têm os fornecedores já documentados no recibo anterior. A principal informa [DECLARADO] que SusyRelativeData reticular ainda não foi instanciado no mesmo core; este delta não certifica essa realização e não a substitui por modelSusy ENNReal. Não houve integração canônica.',
        'Os metadados abaixo são dos arquivos autorais efetivamente lidos e copiados; os caminhos das cópias e seus hashes constam do manifesto e do JSON. A aprovação deste delta é calculada dos gates, sem usar o resultado autoral como prova.',
        '| Arquivo autoral lido | Bytes | SHA-256 |\n|---|---:|---|',
    ]
    for r in snapshots:
        s = r['source']
        text.append(f'| {link(s["path"])} | {s["bytes"]} | `{s["sha256"]}` |')
    text += ['\n| Módulo recompilado nesta revisão | rc | Segundos |\n|---|---:|---:|']
    for m, r in b['modules'].items():
        text.append(f'| {m} | {r["returncode"]} | {r["seconds"]:.2f} |')
    text += [f'\nRecibo e selo de 35 nomes preservados: {link(PRIOR/"RECIBO_REVISAO_A2.md")} e {link(PRIOR/"SELO_A2.json")}. '
        f'Recibo de 33 nomes, evidência nova e cópias são indexados por {link(ROOT/"MANIFESTO_DELTA01.json")} e {link(ROOT/"SELO_DELTA01.json")}.']
    rendered = re.sub(r'(?m)(^\|[^\n]*\|)\n\n(?=\|)', r'\1\n', '\n\n'.join(text)+'\n')
    write(ROOT/'RECIBO_REVISAO_A2_DELTA01_33.md', rendered)
    files = []
    fresh_objects = []
    cached_paths = {Path(r['review']['path']) for r in cache_checks}
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p in cached_paths or p.name in ['MANIFESTO_DELTA01.json', 'SELO_DELTA01.json'] or 'tmp' in p.relative_to(ROOT).parts:
            continue
        (fresh_objects if p.suffix == '.olean' else files).append(info(p))
    manifest = dict(created_utc=stamp(), root=str(ROOT), reviewer_identity=identity, files=files,
        new_objects=fresh_objects, source_snapshots=d['snapshots'], prior_receipt_pins=d['prior_receipt_pins'],
        borrowed_objects_index=info(ROOT/'INTEGRIDADE_DELTA01.json'), history_policy='Lote35 preservado; recibo33 aditivo')
    record(ROOT/'MANIFESTO_DELTA01.json', manifest)
    record(ROOT/'SELO_DELTA01.json', dict(created_utc=stamp(), decision=decision, P2_01=p2_status, reviewer_identity=identity,
        files=[info(ROOT/n) for n in ['RECIBO_REVISAO_A2_DELTA01_33.md', 'AUDITORIA_DELTA01.json', 'MANIFESTO_DELTA01.json']],
        prior_seal=info(PRIOR/'SELO_A2.json')))
    assert all(current(r) for r in files+fresh_objects+read(ROOT/'SELO_DELTA01.json')['files'])
    assert all(current(r) for r in d['prior_receipt_pins'])
    print(json.dumps(dict(decision=decision, gates=gates, files=len(files), fresh_objects=len(fresh_objects),
        receipt=info(ROOT/'RECIBO_REVISAO_A2_DELTA01_33.md'), seal=info(ROOT/'SELO_DELTA01.json')), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
