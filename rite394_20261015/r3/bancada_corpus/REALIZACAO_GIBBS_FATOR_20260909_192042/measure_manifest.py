from pathlib import Path
import datetime
import hashlib
import json
import os
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)
INVENTORY = ROOT / 'REEXAME_GIBBS_DINAMICA_20260909/INVENTARIO_SEIS_FONTES.json'
inventory = json.loads(INVENTORY.read_text(encoding='utf-8'))

def measured(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

modules = []
for item in inventory['modules']:
    if item['module'] not in {'TransverseGibbsResponse', 'MixedQuadraticGibbsResponse'}:
        continue
    src = measured(item['source']['path'])
    receipt = measured(item['receipt']['path'])
    assert src == item['source']
    assert receipt == item['receipt']
    result = json.loads(Path(receipt['path']).read_text(encoding='utf-8'))
    assert result['status'] == 'PASS_COMPILED_SCOPE'
    assert all(run['exit_code'] == 0 for run in result['runs'])
    assert all(set(row['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for row in result['axiom_rows'])
    assert src in result['sources']
    logs = []
    for run in result['runs']:
        log = Path(receipt['path']).parent / (run['module'] + '.log')
        text = log.read_text(encoding='utf-8')
        assert not re.search(r'\b(?:warning|error):', text, re.I), log
        logs.append(measured(log))
    lines = Path(src['path']).read_text(encoding='utf-8').splitlines()
    anchors = [{'line': i, 'declaration': line.strip()}
               for i, line in enumerate(lines, 1)
               if re.match(r'^(?:def|theorem) (?:mixedWeights|mixedBase|quadraticWeights|mixedCurve|quadratic_tangent_zero|quadratic_fisher_zero|quadratic_relative_entropy_limit|quadratic_entropy_limit|quadratic_modular_increment_limit|susceptibility|transverseWeights|response_fisher|uniform_modular_increment_zero|response_entropy_quadratic_limit)\b', line)]
    modules.append({'module': item['module'], 'source': src, 'receipt': receipt,
                    'observed_status': result['status'], 'theorems': result['theorems'],
                    'definitions': result['definitions'], 'axiom_rows': len(result['axiom_rows']),
                    'run_exit_codes': [r['exit_code'] for r in result['runs']],
                    'logs_read': logs, 'scope_note': result['scope_note'], 'anchors': anchors})

CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
references = [
    INVENTORY,
    ROOT / 'REEXAME_GIBBS_DINAMICA_20260909/DEDUCAO_RESPOSTA_E_FRONTEIRA.md',
    ROOT / 'ESTADO_ARAKI_20260909/DEDUCAO_ESTADO_PERTURBADO_ARAKI.md',
    ROOT / 'ESTADO_ARAKI_20260909/Araki_1973_Relative_Hamiltonian.pdf',
    ROOT / 'MAPA_ARAKI_REFERENCIA_20260909_165524_615258/MAPA_DADOS_E_CONVENCOES_ARAKI.md',
    CANON / 'TowerDefinite.lean', CANON / 'TowerHilbert.lean',
    CANON / 'ModularFlowLevel.lean', CANON / 'FiniteEntropyAlgebra.lean',
]
manifest = {
    'status': 'WRITTEN_DERIVATION_AND_EXISTING_RECEIPTS_MEASURED',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'authorship': 'Analise propria da subtarefa finish_gibbs_realization; sem aprovacao atribuida a terceiros.',
    'new_note': measured(OUT / 'REALIZACAO_MATRICIAL_E_FATORIZACAO.md'),
    'measurement_script': measured(__file__),
    'existing_formal_results': modules,
    'references_measured': [measured(p) for p in references],
    'primary_reference': {'title': 'Relative Hamiltonian for Faithful Normal States of a von Neumann Algebra',
                          'author': 'Huzihiro Araki', 'year': 1973,
                          'url': 'https://ems.press/journals/prims/articles/2638',
                          'doi': '10.2977/PRIMS/1195192744',
                          'use': 'Construtor limitado; calculo finito e fatorizacao sao deducao explicita nesta nota.'},
    'new_lean_compilations': 0,
    'matrix_realization_formalized_here': False,
    'araki_finite_factorization_formalized_here': False,
    'quantum_entropy_formalized_here': False,
    'um_py_executed_or_imported': False,
    'originals_written': False,
    'scope': 'Leitura de folhas, recibos e logs existentes; derivacao matricial escrita e fatorizacao finita no GNS produto. Nenhuma alegacao de nova compilacao ou de prova gravitacional incondicional.'
}
dest = OUT / 'MANIFESTO_REALIZACAO.json'
temp = OUT / 'MANIFESTO_REALIZACAO.json.tmp'
assert not dest.exists() and not temp.exists()
payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
with temp.open('xb') as stream:
    stream.write(payload)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == payload
temp.rename(dest)
assert dest.read_bytes() == payload
print(json.dumps({'status': manifest['status'], 'note': manifest['new_note'],
                  'manifest': measured(dest),
                  'modules': [{'module': x['module'], 'theorems': x['theorems'],
                               'definitions': x['definitions'], 'axiom_rows': x['axiom_rows']}
                              for x in modules]}, ensure_ascii=False))
