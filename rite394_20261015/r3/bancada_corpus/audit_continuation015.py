"""Exact-byte and Lean-output audit for spontaneous continuation 015.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'GeodesicSpray', 'LocalGeodesicFlow', 'NullGeodesicConservation',
    'GeodesicFlowRegularity', 'GeodesicFlowControls',
]
MANIFEST = ROOT / 'CONTINUACAO015_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_015_ESPONTANEA_fluxo_geodesico_e_preservacao_nula.md'
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

    visit('GeodesicFlowControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation015.py', 'revise_continuation015.py', 'verify_stage.ps1',
        'CONTINUACAO015_DERIVACAO_PREVIA.md', 'CONTINUACAO015_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO015_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation015.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation015.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 015; no managerial order 015 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reused_corollaries': ['ChatgptAudit.Screen015.curved_flow_background_nonzero'],
        'integrated_root': 'GeodesicFlowControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['smooth geodesic spray on the phase-space domain',
                 'jointly continuous local flow on a common initial-data/time rectangle',
                 'position and velocity derivatives equal to the actual geodesic ODE',
                 'uniform preservation of the open coordinate domain and nonzero velocity',
                 'actual derivative and conservation of metric energy',
                 'null preservation for every initially null datum in the local family',
                 'Levi-Civita flow constructed from a supplied smooth invertible solder',
                 'smoothness in time of each phase curve, position and velocity',
                 'flat affine control and curved null flow with nonzero initial acceleration',
                 'full phase-flow initial velocities cannot be a single spacetime vector field'],
        'inputs_and_unpaid': ['smooth invertible solder and fixed Lorentzian dimension/signature',
                             'smooth dependence on initial data',
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
        '[REAL / INPUT / OPEN] ENTREGA 015 ESPONTÂNEA — fluxo geodésico local e preservação da nulidade.',
        '', '06/09/2026. Continuação de 014. Ordens gerenciais 001–007 presentes no túnel; auditoria independente pendente. Nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação antes do código | PAGO | CONTINUACAO015_DERIVACAO_PREVIA.md. |',
        '| Campo geodésico no espaço de fases | PAGO | geodesic_spray_smooth e geodesic_spray_c1; campo (v,−Γ(v,v)). |',
        '| Existência para dados iniciais próximos | PAGO | localPhaseFlow e localGeodesicFlow; intervalo e bola comuns; continuidade conjunta. |',
        '| Equação geodésica efetiva | PAGO | x′=v e v′=−Γ(v,v), expressas com HasDerivAt. |',
        '| Preservação da nulidade | PAGO | geodesic_energy_derivative e geodesic_flow_energy_conserved; energia nula inicial continua nula. |',
        '| Habitante sob solda geral | PAGO sob INPUT | local_levi_civita_null_geodesics recebe solda suave invertível e velocidade não nula; não recebe um campo V. |',
        '| Suavidade no tempo | PAGO | geodesic_flow_smooth_time, posição e velocidade C∞ em todo o intervalo aberto. |',
        '| Controles | PAGO | Caso plano afim; caso curvo nulo com aceleração inicial −2(1,1,0,0) e curvatura não nula. |',
        '| Fluxo de fase versus campo espacial | PAGO, negativo preciso | phase_flow_cannot_assign_one_field: a família completa contém velocidades distintas na mesma posição. |',
        '| Congruência suave no espaço-tempo | NÃO PAGO | Suavidade nos dados iniciais, escolha transversal, inversão local e primeiro jato de equilíbrio ainda faltam. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados e {data['printed_definitions']} definições com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'O teorema curved_flow_background_nonzero reutiliza a componente de curvatura já provada em 014; não é contado como uma nova descoberta de curvatura. As demais declarações e os detalhes estão no manifesto.',
        'Todos os módulos finais têm compilação limpa da fonte fixada; os axiomas impressos ficam no trio propext, Classical.choice, Quot.sound, sem sorryAx.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation015.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando acima só lê. A gerência deve recompilar em sua cópia independente; os comandos a seguir indicam a ordem dos módulos novos e escrevem binários/logs no caminho especificado:',
        '', '\u0060\u0060\u0060powershell',
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['\u0060\u0060\u0060', '',
             'GeodesicFlowControls importa toda a árvore nova e TransportedScreenControls da entrega 014. A ordem completa de fontes locais está no manifesto. Lean 4.31.0/mathlib são dependências externas; não se declara um pacote portátil ou uma recompilação independente da cadeia.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO015_DERIVACAO_PREVIA.md',
                   'CONTINUACAO015_PARECER.md', 'audit_continuation015.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; erro de elaboração ou aviso; cópia exata do log.")
    rows += ['', 'Revisões conservam backups dos bytes. Falhas de elaboração das somas matriciais, intervalos, tipos de derivação e avisos de argumentos redundantes foram corrigidos sem apagar os registros. A custódia anterior permanece imutável.',
             '', '## Parede exata e encaminhamento', '',
             'O resultado constrói geodésicas no espaço de fases e prova suavidade no tempo e continuidade conjunta. Não prova suavidade nos dados iniciais nem produz um campo suave V em uma região do espaço-tempo. O negativo sobre a família completa não proíbe congruências: mostra que é necessário selecionar os dados iniciais apropriados.',
             '', 'Para usar diretamente o construtor de tela de 014, ainda se precisa de uma seção transversal de dados iniciais, da regularidade conjunta suficiente e da inversa local da projeção para a posição; o equilíbrio demanda controle do primeiro jato. A construção de GeometricHorizonPencil, Clausius/H3 e a ligação microscópica entropia-área continuam abertas.',
             '', 'Fonte primária de contexto: [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004). O artigo usa horizontes locais de equilíbrio e assume a relação entropia-área e Clausius; não é uma prova das hipóteses microscópicas.',
             '', 'Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. Parecer: ' + str(ROOT / 'CONTINUACAO015_PARECER.md') + '. Auditoria independente pendente; o objetivo amplo continua ativo e OPEN.']
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_015_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_015_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 015 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation015.py [--write]')
