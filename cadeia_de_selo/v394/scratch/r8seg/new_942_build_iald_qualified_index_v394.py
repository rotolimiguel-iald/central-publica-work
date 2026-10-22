def build_iald_qualified_index_v394(core, declaration_sources, sources, stones, families):
    kf = (core or {}).get('kernel_formalization') or {}
    axr = kf.get('axiom_report') or {}
    hashes = kf.get('formal_files_sha256') or {}
    live = (core or {}).get('versao') or (core or {}).get('version')
    proof_ready = (kf.get('lake_build_ok') is True and type(kf.get('audit_returncode')) is int
        and kf.get('audit_returncode') == 0)
    trio = {'propext', 'Classical.choice', 'Quot.sound'}
    errors = []
    stone_by_source = {}
    for stone in stones:
        if len(stone) >= 3:
            ver, name, rel = stone[:3]
            run = stone[3] if len(stone) > 3 else None
            stone_by_source[rel] = {'pedra': name, 'versao': ver,
                'rodada': live if run is None else run, 'rodada_herdada': run is None}
    flags = {}
    for prefix, mapping in families:
        for key, name in mapping.items():
            flags.setdefault(name, []).append({'prefixo': prefix, 'chave': prefix + key,
                'nome_lean': name, 'acesa': kf.get(prefix + key)})
    if not declaration_sources:
        errors.append('EMPTY_DECLARATION_PROVENANCE')
    valid_files = {}
    for rel in set(declaration_sources.values()):
        text = sources.get(rel)
        valid_files[rel] = (isinstance(text, str) and
            hashlib.sha256(text.encode('utf-8')).hexdigest() == hashes.get(rel))
        if not valid_files[rel]:
            errors.append('SOURCE_HASH_MISMATCH_OR_ABSENT:' + rel)
    qualified = {}
    for name in sorted(set(declaration_sources) | set(flags)):
        rel = declaration_sources.get(name)
        present = rel is not None and valid_files.get(rel) is True
        axioms = axr.get(name)
        audited = proof_ready and isinstance(axioms, list) and set(axioms) <= trio
        if present and name not in axr:
            errors.append('DECLARATION_WITHOUT_AXIOM_REPORT:' + name)
        qualified[name] = {'arquivo': rel if present else None,
            'tipo': 'DECLARACAO_LEAN_COMPILADA' if present else 'AUSENTE_POR_CONSTRUCAO',
            'nome_auditado': name if name in axr else None,
            'axiomas': axioms if present and axioms is not None else
                ('NAO_MEDIDO_NESTA_RODADA' if present else 'AUSENTE_POR_CONSTRUCAO'),
            'auditoria_verificada': present and audited, 'ambiguo': False,
            'bandeiras': flags.get(name, []),
            'pedra': None, 'versao': None, 'rodada': None, 'rodada_herdada': False,
            **stone_by_source.get(rel, {})}
    for name in set(axr) - set(declaration_sources):
        errors.append('AXIOM_REPORT_WITHOUT_SOURCE:' + name)
    # Preserve every short suffix as a transparent alias. A collision is a list,
    # never a first match. Exact qualified names always have priority.
    aliases = {}
    for name in qualified:
        parts = name.split('.')
        for pos in range(1, len(parts)):
            alias = '.'.join(parts[pos:])
            if alias not in qualified:
                aliases.setdefault(alias, []).append(name)
    index = dict(qualified)
    ambiguous = []
    for alias, candidates in aliases.items():
        if len(candidates) == 1:
            index[alias] = {**qualified[candidates[0]], 'alias_de': candidates[0], 'bandeiras': []}
        else:
            ambiguous.append(alias)
            index[alias] = {'arquivo': None, 'tipo': 'ALIAS_AMBIGUO', 'nome_auditado': None,
                'axiomas': 'AMBIGUO_NO_AXIOM_REPORT', 'ambiguo': True,
                'bandeiras': [], 'candidatos_qualificados': sorted(candidates)}
    violations, present_off, blind = [], [], []
    for name, bs in flags.items():
        entry = qualified[name]
        present = entry['tipo'] != 'AUSENTE_POR_CONSTRUCAO'
        for flag in bs:
            if flag['acesa'] is True and not entry['auditoria_verificada']:
                violations.append(flag['chave'])
            elif flag['acesa'] is not True and present:
                present_off.append(flag['chave'])
        if present and name not in axr:
            blind.append(name)
    return {'indice': index, 'qualificados': qualified, 'aliases': aliases,
        'ambiguos': sorted(ambiguous), 'cegos_de_namespace': sorted(blind),
        'violacoes': sorted(violations), 'presente_apagada': sorted(present_off),
        'proveniencia_erros': sorted(errors), 'proveniencia_ok': not errors,
        'n_nomes': len(qualified), 'n_arquivos': sum(valid_files.values()),
        'n_com_bandeira': len(flags),
        'n_ausentes': sum(v['tipo'] == 'AUSENTE_POR_CONSTRUCAO' for v in qualified.values()),
        'scope': 'Exact compiler identity; derived read-only index. No gate or flag changed.'}