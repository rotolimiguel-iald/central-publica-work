"""Exact-byte and Lean-output audit for spontaneous continuation 011.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'FiniteEntropyAlgebra', 'TowerEntropyScaling', 'SchmidtCutPurification',
    'BoundaryEntropyBridge', 'EntropyGeometryControls',
]
MANIFEST = ROOT / 'CONTINUACAO011_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_011_ESPONTANEA_entropia_da_torre_e_purificacao.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def read(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_bytes(path, raw):
    if not path.resolve().is_relative_to(ROOT) or path.exists():
        raise RuntimeError(f'Output refused: {path}')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw) or temp.read_bytes() != raw:
        raise RuntimeError(f'Incomplete output: {temp}')
    temp.rename(path)


def write_new(path, value):
    write_bytes(path, value.encode('utf-8'))


def runs(module):
    records = []
    for meta in sorted(ROOT.glob(module + '.*.json')):
        data = json.loads(read(meta))
        log = ROOT / data['log']
        output = read(log)
        rejected = data['exit_code'] != 0 or bool(re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', output))
        label = 'failed_compile' if data['exit_code'] else 'rejected_warning'
        archive = log.with_name(log.stem + '.' + label + '.log') if rejected else None
        records.append((meta, data, log, output, archive))
    return records


def preserve_attempts():
    for module in MODULES:
        for _, _, log, _, archive in runs(module):
            if archive is not None:
                if archive.exists():
                    if archive.read_bytes() != log.read_bytes():
                        raise RuntimeError(f'Archive mismatch: {archive}')
                else:
                    write_bytes(archive, log.read_bytes())


def axiom_rows(output):
    rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
    result = [{'declaration': n, 'axioms': [a.strip() for a in v.split(',') if a.strip()]} for n, v in rows]
    if any(not set(row['axioms']) <= ALLOWED for row in result):
        raise RuntimeError('Unexpected axiom dependency')
    return result


def inspect_module(module):
    source = ROOT / (module + '.lean')
    code = read(source)
    if re.search(r'\b(sorry|admit|axiom)\b', code):
        raise RuntimeError(f'Forbidden declaration: {source}')
    declarations = re.findall(r'^(theorem|def)\s+([\w.]+)', code, re.M)
    theorems = [name for kind, name in declarations if kind == 'theorem']
    prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
    if not set(theorems) <= set(prints) or len(prints) != len(set(prints)):
        raise RuntimeError(f'Theorem print coverage mismatch: {module}')
    if not set(prints) <= {name for _, name in declarations}:
        raise RuntimeError(f'Unknown printed declaration: {module}')
    attempts = runs(module)
    candidates = [r for r in attempts if r[1]['exit_code'] == 0 and r[1]['source_stable']
                  and r[1]['proof_sha256'].lower() == digest(source) and r[4] is None]
    if not candidates:
        raise RuntimeError(f'No clean compilation for exact final source: {module}')
    meta, data, log, output, _ = candidates[-1]
    if 'sorryAx' in output:
        raise RuntimeError(f'Unproved final dependency: {module}')
    axioms = axiom_rows(output)
    if sorted(row['declaration'].removeprefix('ChatgptAudit.') for row in axioms) != sorted(prints):
        raise RuntimeError(f'Qualified axiom names mismatch: {module}')
    paths = {source, source.with_suffix('.olean')}
    paths.update(ROOT.glob(module + '.lean.bak_*'))
    history = []
    for m, d, l, out, archive in attempts:
        paths.update([m, l])
        if archive is not None:
            if not archive.exists() or archive.read_bytes() != l.read_bytes():
                raise RuntimeError(f'Failed attempt not preserved: {l}')
            paths.add(archive)
        history.append({'metadata': str(m), 'log': str(l), 'exit_code': d['exit_code'],
                        'source_sha256': d['proof_sha256'].lower(),
                        'rejected_copy': str(archive) if archive else None,
                        'issues': [line for line in out.splitlines()
                                   if re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', line)]})
    return {'module': module, 'theorems': len(theorems), 'printed_definitions': len(prints)-len(theorems),
            'helper_definitions_not_separately_printed': [n for k, n in declarations if k == 'def' and n not in prints],
            'final_metadata': str(meta), 'final_log': str(log), 'axioms': axioms, 'attempts': history}, paths


def inventory():
    records, paths = [], set()
    for module in MODULES:
        record, items = inspect_module(module)
        records.append(record)
        paths.update(items)
    visited, order = set(), []

    def visit(module):
        path = ROOT / (module.replace('.', '/') + '.lean')
        if module in visited or not path.exists():
            return
        visited.add(module)
        for imported in re.findall(r'^import\s+(\S+)', read(path), re.M):
            visit(imported)
        order.append(module)
        paths.add(path)
        if path.with_suffix('.olean').exists():
            paths.add(path.with_suffix('.olean'))

    for module in MODULES:
        visit(module)
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation011.py', 'revise_continuation011.py', 'verify_stage.ps1',
        'CONTINUACAO011_DERIVACAO_PREVIA.md', 'CONTINUACAO011_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO010_MANIFESTO.json',
        'CONTINUACAO009_MANIFESTO.json', 'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json',
        'audit_continuation010.py', 'fontes/tgl_kernel/TGLExt/TowerDefinite.lean',
        'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean', 'fontes/tgl_kernel/TGLExt/GNSTower.lean',
        'fontes/tgl_kernel/TGLExt/PowersLadder.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO011_*.md.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 011; no managerial order 011 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['finite diagonal entropy and product additivity',
                 'canonical tower entropy sum and uniform count scaling',
                 'conditional obstruction to sublinear area law',
                 'explicit positive normalized idempotent bipartite density',
                 'calculated partial traces and canonical left expectation',
                 'left restriction faithfulness and full algebra nonfaithfulness',
                 'half-weight correlation control and area calibration freedom'],
        'inputs_and_unpaid': ['geometric region and cut assignment',
                             'independent geometric area measure and area unit',
                             'arbitrary matrix logarithm and general von Neumann entropy library',
                             'infinite bipartite limit and its dynamics',
                             'screen area and heat current from the quantum state', 'H3',
                             'escape from the product Borchers obstruction',
                             'signature and dimension selection', 'global chart gluing',
                             'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 011 ESPONTÂNEA — entropia da torre, purificação de corte e liberdade da unidade de área.',
        '', 'Continuação de 010, 05/09/2026. Nenhuma ordem 011 da gerência estava no túnel ao publicar. Pronta para auditoria independente; não altera gate nem conclui gravitação quântica.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação antes do código | PAGO | CONTINUACAO011_DERIVACAO_PREVIA.md: sete passos e limites explicitados. |',
        '| Entropia dos pesos efetivos | PAGO | tower_entropy_sum e tower_entropy_uniform: S_N=Σ h(P.w_n); no perfil constante, S_N=(N+1)h(p). |',
        '| Ponte modular finita | PAGO | Entropia igual à expectativa de diag(−log p); primeira variação ligada a first_law_diagonal. |',
        '| Escala sublinear | PAGO como obstrução condicional | no_sublinear_area_entropy: A_N/(N+1)→0 exclui S_N=ηA_N para todo N no perfil constante admissível. |',
        '| Purificação explícita | PAGO | Ψ(i,j)=δ_ij√p_i; densidade positiva, traço 1, idempotente; ambas as marginais calculadas. |',
        '| Mesmo estado canônico | PAGO | tower_cut_expectation e tower_cut_prefix_coherence: expectativa esquerda igual a tState, coerente entre andares. |',
        '| Entropia reduzida da torre | PAGO | tower_cut_reduced_entropy e tower_cut_entropy_sum, para a marginal comprovadamente diagonal. |',
        '| Fidelidade | PAGO com domínios distintos | Restrição esquerda fiel; na álgebra completa existe a≠0 com Tr[ρ(a†a)]=0. |',
        '| Correlação e controle de pesos iguais | PAGO | Densidade pura diferente do produto das marginais; entropia reduzida log 2. Informação mútua zero somente no produto comparativo. |',
        '| Unidade de área | NEGATIVO DELIMITADO | two_area_calibrations: o mesmo estado admite A=(N+1) e A=2(N+1), com η recíproco; o coeficiente 2π/η escala. |',
        '| Área geométrica e dinâmica | NÃO PAGO | A atribuição a cortes, medida geométrica independente, calor, limite bipartido e H3 continuam INPUT/OPEN. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | As implicações anteriores permanecem condicionais; assinatura, dimensão, globalização e vínculo modular-geométrico não foram obtidos aqui. |',
        '', f"{len(data['modules'])} módulos novos; {data['theorems']} teoremas; {data['printed_definitions']} definições separadamente impressas. Contagens lidas dos fontes. Todos os teoremas têm #print axioms, com dependências contidas no trio permitido; nenhum sorryAx nos logs finais.",
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation011.py'}'",
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['\u0060\u0060\u0060', '', 'A ordem de fontes e as dependências locais estão no manifesto. O ambiente externo Lean/mathlib é local. A conferência de hashes não substitui recompilação independente.',
             '', '## Axiomas impressos', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
             f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
             f"Inventário completo: {len(data['files'])} caminhos absolutos, tamanhos e hashes dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO011_DERIVACAO_PREVIA.md',
                   'CONTINUACAO011_PARECER.md', 'audit_continuation011.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: cópia dos bytes do log; exit code {run['exit_code']}; problemas e metadados no manifesto.")
    rows += ['', 'Falhas de normalização, notação e inferência e todos os avisos foram rejeitados. Fontes intermediários e logs foram preservados. A revisão ambígua recusada e a recompilação da versão antiga estão descritas no parecer; não contam como progresso de prova.',
             '', '## Limites e integração', '',
             'S_N é entropia dos pesos normalizados. Na torre produto original ela é entropia de densidade mista, não emaranhamento entre sítios. Na purificação explícita, a mesma diagonal é a marginal calculada. reducedDiagonalEntropy não implementa entropia de von Neumann para matrizes arbitrárias.',
             '', 'A=N+1 vezes uma unidade escolhida é uma leitura por contagem. Nenhum corte geométrico ou unidade de área foi deduzido do estado. A obstrução sublinear é condicional ao perfil uniforme e à escala proposta; não exclui toda interpretação possível de área.',
             '', 'O gerador diagonal −log p não foi identificado com −log Δ de Tomita. A purificação conserva o estado esquerdo e não remove, por si, a obstrução de Borchers de 007. Não foi construído limite bipartido contínuo com dinâmica.',
             '', 'A fonte primária [Jacobson, 1995](https://arxiv.org/abs/gr-qc/9504004) recebe entropia proporcional à área e Clausius como premissas. A conexão física dessas premissas com o estado continua aberta.',
             '', 'Escritas somente em Chatgpt. Nenhum um.py executado, importado ou editado; nenhuma edição no kernel canônico, Atlas, memórias, selos ou gate. Nenhum dado observacional. A gerência recompila, audita e decide incorporação. O objetivo amplo permanece ativo e aberto.']
    return '\n'.join(rows) + '\n'


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_011_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_011_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 011 already occupied; refusing publication')
        preserve_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        data = json.loads(read(MANIFEST))
        for item in data['files']:
            path = Path(item['path'])
            if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
                raise RuntimeError(f'Custody mismatch: {path}')
        for module in data['modules']:
            source = ROOT / (module['module'] + '.lean')
            metadata = json.loads(read(Path(module['final_metadata'])))
            output = read(Path(module['final_log']))
            if (metadata['exit_code'] != 0 or not metadata['source_stable'] or
                    metadata['proof_sha256'].lower() != digest(source) or
                    'sorryAx' in output or re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', output)):
                raise RuntimeError(f'Invalid final compilation: {module["module"]}')
            if axiom_rows(output) != module['axioms']:
                raise RuntimeError('Axiom inventory changed')
            code = read(source)
            if len(re.findall(r'^theorem\s+', code, re.M)) != module['theorems']:
                raise RuntimeError('Theorem count changed')
            prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
            if sorted(prints) != sorted(r['declaration'].removeprefix('ChatgptAudit.') for r in module['axioms']):
                raise RuntimeError('Axiom coverage changed')
        if delivery_text(data) != read(DELIVERY):
            raise RuntimeError('Delivery does not match the pinned inventory')
        print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
              f"{data['theorems']} theorems; {data['printed_definitions']} printed definitions; delivery verified")
    else:
        raise SystemExit('Usage: audit_continuation011.py [--write]')


