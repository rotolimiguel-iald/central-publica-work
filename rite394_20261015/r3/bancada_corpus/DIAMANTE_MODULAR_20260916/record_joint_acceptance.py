"""Consolidate reader declarations against the exact delivery inventory."""
import json
from pathlib import Path
from finalize_weyl_bridge import ROOT, NOW, atomic, pin


def main():
    inventory = json.loads((ROOT / 'JOINT_DEFINITION_INVENTORY.json').read_text(encoding='utf-8'))
    core = json.loads((ROOT / 'AUDITORIA_CONJUNTA_CORE.json').read_text(encoding='utf-8'))
    geometry = json.loads((ROOT / 'AUDITORIA_CONJUNTA_GEOMETRIA.json').read_text(encoding='utf-8'))
    physical = json.loads((ROOT / 'AUDITORIA_CONJUNTA_FISICA.json').read_text(encoding='utf-8'))
    expected = {str(Path(x['path']).resolve()): x for x in inventory['sources']}
    seen = {}

    def accept(path, digest, size, group):
        path = str(Path(path).resolve())
        assert path not in seen, ('DUPLICATE', path)
        item = expected[path]
        assert item['review_group'] == group
        assert item['sha256'] == digest and item['bytes'] == size
        current = pin(Path(path))
        assert current['sha256'] == digest and current['bytes'] == size
        seen[path] = group

    for row in core['fontes']:
        assert row['leitura'] == 'integral'
        assert row['cobertura']['conteudo_inspecionado'] is True
        assert row['cobertura']['truncamento_pendente'] is False
        accept(row['fonte'], row['pin_sha256_lido'], row['bytes'], 'CORE_AND_FRIEDMANN')
    for row in geometry['sources']:
        assert row['reading']['status'] == 'integral'
        assert row['reading']['unresolved_truncation'] is False
        accept(row['path'], row['pin']['read_from_bytes'], row['bytes'], 'GEOMETRY_AND_MODULAR_EARLY')
    for row in physical['records']:
        assert row['read_status'] == 'FULL_TEXT_REVIEWED'
        accept(row['path'], row['sha256'], row['bytes'], 'PHYSICAL_QUANTUM_AND_RECENT')
    assert set(seen) == set(expected)
    groups = {
        group: {'full_delivery_read_count': list(seen.values()).count(group),
                'reviewer': reviewer,
                'reading_evidence': 'Reader full-content declaration and per-file coverage, validated against current byte pins; not inferred from hashing alone.'}
        for group, reviewer in (
            ('CORE_AND_FRIEDMANN', 'McClintock'),
            ('GEOMETRY_AND_MODULAR_EARLY', 'Russell'),
            ('PHYSICAL_QUANTUM_AND_RECENT', 'main'),
        )
    }
    result = {
        'timestamp': NOW,
        'all_three_reports_read_by_main': True,
        'main_report_reading': 'Core MD read in [1,130] and [131,223]; geometry MD initial output truncated in middle, repaired by full [89,178] ranges; physical report written and reviewed by main. JSON ledgers parsed in full, coverage and pins checked programmatically. No claim that main personally reread all 156 deliveries.',
        'complete_delivery_coverage': True,
        'groups': groups,
        'coverage_count': len(seen),
        'coverage_bytes': sum(x['bytes'] for x in expected.values()),
        'independent_synthesis_review': {
            'reviewer': 'Russell',
            'scope': 'Consistency with deliveries <=059 only; no re-audit of later physical providers.',
            'verdict_received': 'No explicit reopening of paid obligations or promotion of hypotheses found in the two synthesis documents read.',
            'later_editorial_changes': 'Main added explicit accounts of reviewed geometry/core findings and domain/representative clarifications. Not presented as a new independent full mathematical review.',
        },
        'documentary_attribution_note': 'The geometry report phrase that physical reading was reported by the operator refers to coordination by the main assistant, not a new direct user statement. Direct user instruction is the verbatim tunnel receipt.',
        'limits': [
            'Not every recursively linked proof/source/build has been reviewed.',
            'Historical Lean/CAS/runtime success is not a new execution.',
            'Composition and limited adversarial source review do not establish an interacting UV-complete regional modular identification.',
        ],
    }
    atomic(ROOT / 'JOINT_READING_ACCEPTANCE.json', json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'status': 'COVERAGE_PASS', 'documents': len(seen), 'bytes': result['coverage_bytes']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
