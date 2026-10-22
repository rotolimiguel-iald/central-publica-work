"""Exact-byte and Lean-output audit for spontaneous continuation 019.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'NullJetAlgebra', 'PrescribedCovariantJet', 'NullSeedWithJet',
    'ShootingJetTransfer', 'EquilibriumNullCongruence',
    'EquilibriumScreenIntegration', 'EquilibriumCongruenceControls',
]
MANIFEST = ROOT / 'CONTINUACAO019_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_019_ESPONTANEA_primeiro_jato_de_equilibrio_construido.md'
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

    visit('EquilibriumCongruenceControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation019.py', 'revise_continuation019.py', 'verify_stage.ps1',
        'CONTINUACAO019_DERIVACAO_PREVIA.md', 'CONTINUACAO019_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO019_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation019.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation019.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 019; no managerial order 019 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['smooth geodesic shooting and inverse chart constructed in 018',
                  'actual joint flow derivative from 016 and joint C-infinity flow from 017',
                  'normalized null frame from 013 and transported screen from 014',
                  'metric derivative and focusing identities from earlier geometry modules',
                  'explicit expanding field and nonzero curvature control from 014'],
        'integrated_root': 'EquilibriumCongruenceControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['null correction by a companion null direction',
                 'preservation of value and derivative when the nullity error has zero first jet',
                 'affine seed with actual covariant gradient zero at a prescribed point',
                 'zero derivative of the affine seed nullity error by metric compatibility',
                 'companion null vector from the normalized frame and smooth transport by the solder',
                 'open neighborhood with nonzero correction denominator',
                 'smooth exactly null seed with prescribed zero covariant first jet',
                 'actual shooting velocity derivative and identity derivative of inverse position at base',
                 'zero covariant first jet transferred to the constructed geodesic congruence',
                 'local equilibrium congruence from smooth invertible solder and nonzero null tangent',
                 'constructed geometric screen data with zero expansion and optical form at base',
                 'area value one in the normalized screen and local area rate identity',
                 'expansion focusing derivative equals minus Ricci on the initial null tangent',
                 'flat and nonzero-curvature equilibrium construction controls',
                 'curved equilibrium field differs from the explicit expanding field'],
        'inputs_and_unpaid': ['open subset of Coordinate4, smooth solder A and smooth inverse B',
                             'fixed dimension four and prescribed Lorentzian signature',
                             'prescribed nonzero initial tangent null for the soldered metric',
                             'null hypersurface immersion and integrability beyond the point',
                             'integrated area over a horizon',
                             'microscopic region-to-algebra and entropy-to-area identification',
                             'physical area unit and entropy density coefficient',
                             'state evolution and heat current', 'Clausius/H3',
                             'global chart gluing', 'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 019 ESPONTÂNEA — primeiro jato de equilíbrio construído na congruência nula local.',
        '', '06/09/2026. Continuação de 018. Auditoria independente da gerência pendente. Nenhuma alteração de gate.',
        '', '## Critérios', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO019_DERIVACAO_PREVIA.md. |',
        '| Campo afim com jato prescrito | PAGO | affine_seed_derivative e affine_seed_gradient_zero. |',
        '| Erro de nulidade com derivada zero | PAGO | affine_seed_energy_derivative_zero, por compatibilidade métrica. |',
        '| Correção nula sem alterar o jato | PAGO | null_correction_null e null_correction_preserves_derivative. |',
        '| Dados iniciais inteiramente construídos | PAGO sob INPUT | local_null_seed_with_zero_covariant_jet constrói companheiro, aberto e campo nulo. |',
        '| Transferência para a congruência | PAGO | shooting_velocity_derivative_zero, shooting_inverse_derivative_base e congruence_prescribed_gradient_zero. |',
        '| Existência com equilíbrio | PAGO sob INPUT | local_levi_civita_equilibrium_congruence acrescenta ∇V(p)=0 à construção de 018, sem receber esse equilíbrio como hipótese. |',
        '| Tela e focalização | PAGO sob INPUT | localEquilibriumScreen e local_equilibrium_screen_with_focusing: θ(p)=0, A(0)=1 e θ′(0)=−Ric(v,v). |',
        '| Forma óptica inicial | PAGO | equilibrium_screen_optical_form_zero: Sᵀg(∇V)S=0 no ponto. |',
        '| Controles | PAGO | Campo de equilíbrio construído em fundo plano e em fundo com curvatura não zero; o segundo difere do campo expansivo de 014. |',
        '| Horizonte nulo imerso e área integrada | NÃO PAGO | A carta do fluxo e o jato no ponto não fornecem por si uma hipersuperfície nula integrada. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | Ponte microscópica, coeficiente físico, calor, Clausius/H3, ponte modular e globalização permanecem OPEN. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definição com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'As compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound. As contagens incluem aplicações, lemas auxiliares e controles que reutilizam resultados anteriores.',
        '', '## Enunciado principal', '',
        'Dados U aberto, A e B suaves com AB=BA=I em U, p∈U e uma tangente v≠0 nula para g(p)=A(p)ᵀηA(p), existem p∈N⊆U aberto e V suave em N com V(p)=v, V≠0, g(V,V)=0, ∇_V V=0 em N e ∇V(p)=0.',
        'A nova condição é pontual. Não se afirma que V seja paralelo num aberto. A construção não exige curvatura zero; o controle curvo verifica isso.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation019.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando só lê e confere bytes, logs e axiomas registrados. A gerência deve recompilar em uma cópia para a auditoria independente. Ordem dos novos módulos:',
    ]
    rows.extend('- ' + m + '.lean' for m in MODULES)
    rows += ['', 'EquilibriumCongruenceControls importa toda a árvore 019 e as dependências locais anteriores. O manifesto contém a ordem local completa. O wrapper documenta Lean 4.31.0/mathlib; não se declara um pacote portátil integral.',
             '', '## Axiomas impressos', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
             f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
             f"Inventário: {len(data['files'])} caminhos absolutos, com tamanho e hash dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO019_DERIVACAO_PREVIA.md',
                   'CONTINUACAO019_PARECER.md', 'audit_continuation019.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += ['', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Somente as compilações finais limpas sustentam a entrega; as falhas intermediárias e os avisos não foram apagados.',
             '', '## Limites', '',
             'O equilíbrio inicial é pago como gradiente covariante zero. A forma óptica projetada também zera; não foi introduzida uma definição independente de cisalhamento para rebatizar uma hipótese.',
             'EquilibriumScreenData contém somente os dados geométricos construídos. Não se disfarçam calor ou Clausius como geometria: GeometricHorizonPencil ainda os exige e não foi declarado habitado por esta entrega.',
             'A área inicial um é a normalização da base da tela. Não fixa unidade física nem coeficiente microscópico de entropia por área.',
             'A hipersuperfície nula, a integrabilidade além do ponto, a área integrada, as identificações microscópicas, o calor/H3 e a ponte modular seguem OPEN. Dimensão, assinatura e solda continuam INPUT.',
             '', 'Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. A custódia 018 foi reconferida em modo de leitura.',
             'O objetivo amplo permanece ativo e não alcançado. Incorporação pela gerência após auditoria; confirmação física reservada ao observador.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO019_PARECER.md') + '.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_019_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_019_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 019 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation019.py [--write]')




