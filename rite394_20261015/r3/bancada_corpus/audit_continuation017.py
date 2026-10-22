"""Exact-byte and Lean-output audit for spontaneous continuation 017.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'FlowGermUniqueness', 'FlowRegularityInduction', 'FlowSmoothGerm',
    'FlowTimePropagation', 'SmoothGeodesicFlow', 'SmoothFlowControls',
]
MANIFEST = ROOT / 'CONTINUACAO017_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_017_ESPONTANEA_suavidade_do_fluxo_no_dominio_local.md'
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
        label = ('failed_compile' if data['exit_code'] else
                 'rejected_warning')
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
    namespaces = re.findall(r'^namespace ([\w.]+)', code, re.M)
    if len(namespaces) != 1:
        raise RuntimeError(f'Unexpected namespace structure: {module}')
    namespace = namespaces[0]
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
    if sorted(row['declaration'] for row in axioms) != sorted(namespace + '.' + name for name in prints):
        raise RuntimeError(f'Qualified axiom names mismatch: {module}')
    paths = {source, source.with_suffix('.olean')}
    paths.update(ROOT.glob(module + '.lean.bak_*'))
    history = []
    source_versions = {digest(source)} | {digest(p) for p in ROOT.glob(module + '.lean.bak_*')}
    for m, d, l, out, archive in attempts:
        if d['proof_sha256'].lower() not in source_versions or not d['source_stable']:
            raise RuntimeError(f'Historical source missing or unstable: {m}')
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
    return {'module': module, 'namespace': namespace, 'theorems': len(theorems), 'printed_definitions': len(prints)-len(theorems),
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

    visit('SmoothFlowControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation017.py', 'revise_continuation017.py', 'verify_stage.ps1',
        'CONTINUACAO017_DERIVACAO_PREVIA.md', 'CONTINUACAO017_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO017_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation017.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation017.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 017; no managerial order 017 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['local ODE uniqueness and Picard existence from mathlib',
                  'actual joint flow derivative from 016',
                  'null conservation and flat affine solution from 015',
                  'conformal background and initial acceleration from 014-015'],
        'integrated_root': 'SmoothFlowControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['equality of local flow germs with matching initial values',
                 'induction of every finite regularity order using the variational field',
                 'all finite orders transferred to one fixed flow choice by uniqueness',
                 'smooth germ at every interior initial datum',
                 'nearby-time transition by restarting the ODE',
                 'open/closure propagation over the connected original time interval',
                 'joint C-infinity regularity on the original fixed data-time domain',
                 'smoothness of the same c1GeodesicFlow function constructed in 016',
                 'smooth local metric and Levi-Civita flows preserving initial nullity',
                 'zero-field, independent flat polynomial and curved smooth controls'],
        'inputs_and_unpaid': ['smooth field on an open set of a real Banach space',
                             'explicit properties of LipschitzLocalFlow, constructed in 016',
                             'smooth invertible solder and fixed Lorentzian dimension/signature',
                             'transverse initial hypersurface and local inverse of the position map',
                             'smooth spacetime null congruence and equilibrium first jet',
                             'surface immersion and integrated area',
                             'microscopic region-to-algebra and entropy-to-area identification',
                             'area unit and entropy density coefficient',
                             'state evolution and heat current', 'Clausius/H3',
                             'global chart gluing', 'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 017 ESPONTÂNEA — suavidade conjunta do fluxo no domínio local original.',
        '', '06/09/2026. Continuação de 016. Auditoria independente pendente. Nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO017_DERIVACAO_PREVIA.md, preservada em backup antes do adendo posterior. |',
        '| Unicidade entre escolhas | PAGO | flow_germ_eq_at_initial: igualdade perto do mesmo dado e do tempo zero, com centros e domínios possivelmente diferentes. |',
        '| Todas as ordens finitas | PAGO | exists_finite_regular_flow, por indução no campo variacional; o diferencial efetivo vem de 016. |',
        '| Uma única escolha de fluxo | PAGO | flow_finite_regular_at_initial e flow_smooth_at_initial; igualdade local transfere todas as ordens para a função recebida. |',
        '| Propagação temporal | PAGO | flow_finite_regular_nearby_transfer e conexão do intervalo; a transição usa a ODE recomeçada. |',
        '| C∞ no domínio fixo | PAGO | flow_smooth_on_domain: mesmo raio, mesma bola e mesmo intervalo do fluxo original. |',
        '| Aplicação geodésica | PAGO sob INPUT | c1_geodesic_flow_smooth fortalece a própria escolha de 016; local_smooth_levi_civita_null_geodesics reúne suavidade e nulidade preservada sob solda suave invertível. |',
        '| Controles | PAGO | Campo zero, fórmula plana polinomial independente e fluxo curvo suave com aceleração inicial não nula. |',
        '| Campo nulo suave no espaço-tempo | NÃO PAGO | Falta selecionar dados transversais e construir a inversa local do mapa de posição; o fluxo atual vive no espaço de fases. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | Primeiro jato de equilíbrio, horizonte, H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definição com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'A prova chega a ContDiffOn ℝ ∞ no aberto original. Não infere um raio positivo de uma interseção de raios decrescentes. A contagem é de declarações e inclui aplicações de resultados anteriores; não é uma contagem de descobertas novas.',
        'As compilações finais da fonte fixada não têm erros, avisos ou sorryAx. As dependências impressas ficam no trio propext, Classical.choice, Quot.sound.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation017.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando só lê e verifica custódia e evidências registradas. A recompilação independente da gerência deve preservar os artefatos entregues. Ordem dos módulos novos:',
    ]
    rows.extend('- ' + m + '.lean' for m in MODULES)
    rows += ['', 'SmoothFlowControls importa toda a árvore 017 e a entrega 016. A ordem local completa está no manifesto. O wrapper verify_stage.ps1 e seus metadados documentam Lean 4.31.0/mathlib; não se declara um pacote portátil integral.',
             '', '## Axiomas impressos', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
             f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
             f"Inventário: {len(data['files'])} caminhos absolutos com tamanho e hash dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO017_DERIVACAO_PREVIA.md',
                   'CONTINUACAO017_PARECER.md', 'audit_continuation017.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += ['', 'Os backups preservam os bytes das versões compiladas. As falhas intermediárias de coerção, vizinhanças e composição, além dos avisos de variáveis, foram corrigidas sem apagar os registros. Só as compilações finais limpas sustentam a entrega.',
             '', '## Próxima obrigação geométrica', '',
             'A regularidade C∞ do fluxo está paga. Ainda é preciso selecionar uma seção transversal de dados iniciais nulos, provar a invertibilidade do diferencial do mapa de posição e construir a inversa local suave. A velocidade transportada então poderá definir um campo SmoothVectorOn no espaço-tempo. O primeiro jato de equilíbrio continua uma obrigação própria.',
             'O operador variacional J desta cadeia é flowVariation de 016; não foi identificado com a conjugação modular. A solda invertível e a assinatura permanecem INPUT. A família completa no espaço de fases não é inteiramente nula: a conclusão recebe explicitamente a nulidade do dado inicial.',
             '', 'Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate não foram tocados pela bancada. A custódia 016 foi reconferida sem alterações. O objetivo amplo permanece ativo e OPEN; esta é uma prova local sob hipóteses nomeadas.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO017_PARECER.md') + '.',
             '', 'Ordens de entrada encontradas no inventário:']
    rows.extend('- ' + p for p in data['incoming_orders'])
    return '\n'.join(rows) + '\n'


def verify_custody():
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
        if re.findall(r'^namespace ([\w.]+)', code, re.M) != [module['namespace']]:
            raise RuntimeError('Namespace changed')
        if len(re.findall(r'^theorem\s+', code, re.M)) != module['theorems']:
            raise RuntimeError('Theorem count changed')
        prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
        if sorted(module['namespace'] + '.' + n for n in prints) != sorted(r['declaration'] for r in module['axioms']):
            raise RuntimeError('Axiom coverage changed')
    if delivery_text(data) != read(DELIVERY):
        raise RuntimeError('Delivery does not match the pinned inventory')
    print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
          f"{data['theorems']} declared theorems; {data['printed_definitions']} printed definitions; delivery verified")


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_017_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_017_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 017 already occupied; refusing publication')
        preserve_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        verify_custody()
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        verify_custody()
    else:
        raise SystemExit('Usage: audit_continuation017.py [--write]')


