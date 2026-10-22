"""Pin the main reader's completed batch, without changing source documents."""
import json
from pathlib import Path
from finalize_weyl_bridge import ROOT, WORK, NOW, pin, atomic


def main():
    inventory = json.loads((ROOT / 'JOINT_DEFINITION_INVENTORY.json').read_text(encoding='utf-8'))
    records = []
    for item in inventory['sources']:
        if item['review_group'] != 'PHYSICAL_QUANTUM_AND_RECENT':
            continue
        current = pin(Path(item['path']))
        assert current['sha256'] == item['sha256'], item['path']
        assert current['bytes'] == item['bytes'], item['path']
        records.append({**item, 'read_status': 'FULL_TEXT_REVIEWED',
                        'reviewer': 'main', 'source_role': 'delivery_or_tunnel_document'})
    assert len(records) == 47
    primary = [
        'REDUCAO_ON_SHELL_RG_070_20260909_232623_681687/REDUCAO_EFT_E_FLUXO_LOGARITMICO.md',
        'ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md',
        'POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md',
        'RENORMALIZACAO_SIGMA_EFT_20260909/FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md',
        'FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md',
        'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
        'REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md',
    ]
    result = {
        'timestamp': NOW, 'reviewer': 'main',
        'scope': '47_PHYSICAL_QUANTUM_AND_RECENT_DELIVERY_DOCUMENTS',
        'read_method': 'Full tool outputs in disjoint batches [0,10), [10,20), [20,32), [32,47); mathematical synthesis by main reader, not keyword-only or byte-only scan.',
        'records': records,
        'primary_notes_read_fully_this_stage': [dict(**pin(WORK / p), read_status='FULL_TEXT_REVIEWED') for p in primary],
        'partial_or_truncated_followup_reads_not_counted_as_full': [
            'Combined extra follow-up of REEXAME_SUFICIENCIA_069 and _070 was truncated; not counted here as full primary proof review. Their delivery documents were read fully in the 47-file batches.',
        ],
        'report': pin(ROOT / 'AUDITORIA_CONJUNTA_FISICA.md'),
        'new_lean_build': False, 'new_cas_run': False,
        'canonical_execution': False, 'gate_changed': False,
    }
    atomic(ROOT / 'AUDITORIA_CONJUNTA_FISICA.json', json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'files': len(records), 'bytes': sum(x['bytes'] for x in records), 'report': result['report']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
