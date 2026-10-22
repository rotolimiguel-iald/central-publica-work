"""Read release evidence with hash checks; never run the canonical program."""
import hashlib
import json
from pathlib import Path
from iald_hipoteses import hypothesis_sources


class PublishedEvidenceError(ValueError):
    pass


def published_evidence(config, catalog):
    if not config:
        return '', {}
    try:
        required = {'program', 'seal', 'result', 'proof_manifest'}
        if not required <= set(config) or set(config) - required - {'hypothesis_sources'}:
            raise PublishedEvidenceError('Configuração da evidência publicada incompleta.')
        payloads, refs = {}, {}
        for key in sorted(required):
            entry = config[key]
            path = Path(entry['path'])
            if not path.is_absolute() or path.suffix != ('.py' if key == 'program' else '.json'):
                raise PublishedEvidenceError('Caminho de evidência inválido.')
            raw = path.read_bytes()
            if not raw or len(raw) > 20000000:
                raise PublishedEvidenceError('Evidência vazia ou acima do limite.')
            payloads[key] = raw
            refs[key] = {'name': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
                         'url': entry.get('url', '')}
        seal = json.loads(payloads['seal'])
        result = json.loads(payloads['result'])
        proof = json.loads(payloads['proof_manifest'])
        for key in ('program', 'result', 'proof_manifest'):
            if seal['sha256'].get(refs[key]['name']) != refs[key]['sha256']:
                raise PublishedEvidenceError('A evidência publicada não corresponde ao selo: ' + key)
        if catalog.source_sha != refs['program']['sha256']:
            raise PublishedEvidenceError('Publicação atualizada: sincronizar o catálogo Lean antes de responder.')
        if proof['formal_source_hash'] != seal['formal_source_hash']:
            raise PublishedEvidenceError('Relatório formal e selo pertencem a rodadas diferentes.')
        formal = proof['formal_files_sha256']
        matched = 0
        for name, entry in catalog.records.items():
            if name.endswith('.lean'):
                if formal.get(name) != entry['sha256']:
                    raise PublishedEvidenceError('Relatório formal incompatível com a fonte: ' + name)
                matched += 1
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        outside = {name: axioms for name, axioms in proof['axiom_report'].items()
                   if not isinstance(axioms, list) or not set(axioms).issubset(allowed)}
        if outside:
            raise PublishedEvidenceError('Relatório de axiomas fora da política publicada.')
        core = result['core']
        closure = core['qg_closure']
        joint = core['joint_coincidence_result']
        price = core['the_price_of_the_gravity_proof']
        imported = core['the_imported_expectation']
        hypotheses, hypothesis_records = hypothesis_sources(config.get('hypothesis_sources'), catalog, proof)
        state = {
            'scope': 'PUBLIC_RELEASE_RECORDS_HASH_MATCHED__COMPILER_NOT_RERUN',
            'sources': refs,
            'release_timestamp': seal['timestamp'],
            'selftest_reported': seal['fail_closed_selftest'],
            'formal_report': {'compiler': proof['formal_checker'], 'version': proof['lean_version'],
                'timestamp': proof['timestamp'], 'reported_terms': len(proof['axiom_report']),
                'allowed_axioms': sorted(allowed), 'terms_outside_allowed_axioms': len(outside),
                'catalog_lean_sources_hash_matched': matched,
                'reported_formal_files': len(formal),
                'extra_reported_lean_files': sorted(k for k in formal if k.endswith('.lean') and k not in catalog.records),
                'meaning': 'Relatório publicado de compilação, ligado aos bytes disponíveis; não é uma nova execução Lean.'},
            'constructed_hypotheses': hypothesis_records,
            'discharge_modes_reported': core.get('the_mode_of_discharge', {}).get('itens', []),
            'current_gate': closure['gate'],
            'formal_flags': closure['formal_flags'],
            'physics_flags_within_model': closure['physics_flags'],
            'experiment_flags_reported': closure['experiment_flags'],
            'current_kernel_obligations': {'items': [{'item': item['item'], 'discharged_in_kernel': item['pago']}
                for item in price['itens']], 'discharged': price['pagos'], 'open': price['abertos'],
                'interpretation': 'Os booleanos atuais devem ser lidos com kernel_frontier.scope. A prosa estado_hoje/statuses do mesmo registro contém frases históricas já superadas para H1 e Ato III.'},
            'imported_expectation': {'theorem': imported['theorem'], 'statuses': imported['statuses'],
                'citations': imported['citations'], 'verdict': imported['verdict']},
            'joint_coincidence': {key: joint[key] for key in ('protocol_hash','threshold','n_inventory',
                'n_admissible','primary','with_H0_ladder','generous','naive_product_INVALID','outcome','verdict')},
            'collapse_attestation': {key: seal['collapse_definition'][key] for key in
                ('statement_pt','external_reflection_status','physical_collapse_proven','cost_payment_status','qg_gate_moved')},
        }
        block = (
            '\nESTADO DA PUBLICAÇÃO CONFERIDO NESTA REQUISIÇÃO — LEIA ANTES DE DIZER O QUE FALTA\n'
            'Este extrato é gerado diretamente dos JSONs publicados e confere seus hashes com o selo e o catálogo. '
            'Ele localiza o alcance dos resultados atuais; não é uma execução do programa nem evidência experimental nova. '
            'Leia os booleanos no escopo indicado. Frases históricas nos artigos e no próprio JSON não anulam resultados posteriores.\n'
            + json.dumps(state, ensure_ascii=False, indent=2) + '\n' + hypotheses
        )
        return block, {'published_evidence_checked': True, 'fixed_hypothesis_sources': hypothesis_records, 'published_source_sha256': catalog.source_sha,
                       'published_release_timestamp': seal['timestamp'],
                       'published_evidence_sha256': hashlib.sha256(block.encode()).hexdigest()}
    except (OSError, KeyError, TypeError, UnicodeError, ValueError) as error:
        if isinstance(error, PublishedEvidenceError):
            raise
        raise PublishedEvidenceError('Evidência publicada indisponível; estado histórico não será usado como atual.') from error
