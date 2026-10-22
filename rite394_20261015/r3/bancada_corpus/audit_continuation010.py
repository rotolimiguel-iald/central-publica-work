"""Exact-byte and Lean-output audit for spontaneous continuation 010.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'CovariantVectorCalculus', 'VectorCurvatureCommutator', 'CoordinateRaychaudhuri',
    'LocalHorizonBalance', 'HorizonEinsteinReconstruction', 'HorizonBalanceControls',
]
MANIFEST = ROOT / 'CONTINUACAO010_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_010_ESPONTANEA_focalizacao_e_clausius_local.md'
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
        'audit_continuation010.py', 'revise_continuation010.py', 'verify_stage.ps1',
        'CONTINUACAO010_DERIVACAO_PREVIA.md', 'CONTINUACAO010_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO009_MANIFESTO.json', 'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json',
        'audit_continuation009.py', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
        'fontes/tgl_kernel/TGLExt/TriadMaster.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/EmergenceTriad.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/PoincareGroup.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO010_*.md.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 010; no managerial order 010 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['covariant vector calculus from actual derivatives', 'curvature commutator',
                 'general coordinate Raychaudhuri identity', 'equilibrium Ricci focusing',
                 'one-sided Clausius residual and quadratic primitive limit',
                 'conditional Einstein reconstruction from local horizon data',
                 'flat nonzero-direction inhabitant and curved incompatible-data control'],
        'inputs_and_unpaid': ['smooth Lorentzian frame and dimension four', 'matter conservation',
                             'existence of local horizon pencils in general curved geometry',
                             'geometric screen area and entropy-area identification',
                             'heat current and equilibrium from quantum dynamics', 'H3',
                             'global chart gluing', 'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 010 ESPONTÂNEA — Raychaudhuri e balanço local de Clausius ligados à reconstrução com o tensor de Einstein geométrico.',
        '', 'Continuação de 009, 05/09/2026. Nenhuma ordem 010 da gerência estava no túnel ao publicar. Pronta para auditoria independente; não altera gate nem conclui gravitação quântica.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação antes do código | PAGO | Derivação geral e adendo prévio ao habitante plano; controle curvo reutiliza o cálculo prévio de 009. |',
        '| Derivadas vetoriais e curvatura | PAGO | Derivadas de Fréchet; comutador covariante igual à curvatura efetiva. |',
        '| Identidade de Raychaudhuri | PAGO | D_Vθ = div a − tr(B²) − Ric(V,V), para campos suaves e conexão sem torção na carta. |',
        '| Focalização de equilíbrio | PAGO como implicação | Campo geodésico em vizinhança e B=0 no ponto; derivada transportada para curva tangente. |',
        '| Balanço analítico local | PAGO como implicação | Resíduo integrado F/λ²→0 no ramo passado, leis de área e calor, continuidade e fatores não nulos forçam o balanço nulo de Ricci. |',
        '| Reconstrução geométrica | PAGO como implicação | horizon_einstein_reconstruction: testemunhos para todas as direções nulas e T conservado dão G_geom+Λg=(2π/η)T, Λ constante. |',
        '| Contrato não vazio | PAGO no controle plano | flatHorizonPencil e flat_nonzero_pencil_exists: direção nula (1,1,0,0), não zero, Γ=0, T=0, A=1, Q=0. |',
        '| Controle curvo incompatível | PAGO | Ric(v,v)=2 em x=0; com T=0 e η≠0 não existe o testemunho exigido. |',
        '| KMS e vinculação física | NEGATIVO DELIMITADO | KMS canônico coexiste com o par independente incompatível; não implica o balanço para geometria e matéria arbitrárias. |',
        '| Testemunhos físicos gerais e área de tela | NÃO PAGO | Existência geral, interpretação geométrica de A, entropia-área e calor oriundos do estado continuam INPUT/OPEN. |',
        '| H3 dinâmico, assinatura, quatro dimensões e globalização | NÃO PAGO | Permanecem obrigações do objetivo amplo. |',
        '', f"{len(data['modules'])} módulos novos; {data['theorems']} teoremas e {data['printed_definitions']} definição com axiomas impressos. Contagens lidas dos fontes. Logs finais limpos, sem sorryAx; somente o trio permitido.",
        '', '## Reprodução', '', '```powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation010.py'}'",
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['```', '', 'A ordem de fontes e as dependências locais estão no manifesto. O ambiente externo Lean/mathlib é local. A conferência de hashes não substitui recompilação independente.',
             '', '## Axiomas impressos', '', '```text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['```', '', '## Artefatos e hashes', '',
             f"Manifesto: `{MANIFEST}` — SHA256 `{digest(MANIFEST)}`.",
             f"Inventário completo: {len(data['files'])} caminhos absolutos, tamanhos e hashes dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO010_DERIVACAO_PREVIA.md',
                   'CONTINUACAO010_PARECER.md', 'audit_continuation010.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| `{item['path']}` | `{item['sha256']}` |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- `{run['rejected_copy']}`: cópia dos bytes do log; exit code {run['exit_code']}; problemas e metadados no manifesto.")
    rows += ['', 'Tentativas com erros de representação funcional, inferência ou avisos não contam como compilação final. Fontes intermediários e os bytes dos logs foram preservados.',
             '', '## Limites e integração', '',
             'O equilíbrio B=0 usado no ponto é mais forte que expansão e cisalhamento de tela nulos. A curva é especificada pelo ponto e pela tangente necessários ao limite; não se construiu o fluxo geodésico completo. A lei A\'=θA é entrada, e a identificação de A com área de tela ainda não está provada. O contrato não contém a igualdade de Ricci e matéria como campo: essa igualdade é deduzida. Sua existência física geral continua aberta.',
             '', 'A fonte primária de referência foi [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004); as hipóteses termodinâmicas da referência não foram promovidas a consequência de KMS.',
             '', 'Escritas somente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Nenhum dado observacional. A gerência recompila, audita e decide incorporação. O objetivo amplo permanece ativo e aberto.']
    return '\n'.join(rows) + '\n'


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_010_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_010_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 010 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation010.py [--write]')

