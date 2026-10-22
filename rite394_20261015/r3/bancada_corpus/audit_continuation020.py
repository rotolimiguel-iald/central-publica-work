"""Exact-byte and Lean-output audit for spontaneous continuation 020.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['PastContinuousExtension', 'EquilibriumAreaExpansion', 'ConstructedHeatPrimitive', 'ScreenClausiusCoefficient', 'ConstructedHorizonPencil', 'ConstructedEinsteinReconstruction', 'ConstructedClausiusControls']
MANIFEST = ROOT / 'CONTINUACAO020_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_020_ESPONTANEA_area_calor_e_clausius_construidos.md'
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

    visit('ConstructedClausiusControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation020.py', 'revise_continuation020.py', 'verify_stage.ps1',
        'CONTINUACAO020_DERIVACAO_PREVIA.md', 'CONTINUACAO020_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO020_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation020.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation020.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 020; no managerial order 020 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['local equilibrium congruence and normalized screen from 019',
                  'geodesic flow, shooting, regularity, null frame and transport from 013-018',
                  'actual induced screen area from 012',
                  'quadratic primitive limit and conditional Clausius reconstruction from 010',
                  'general tensor, Levi-Civita, curvature and Bianchi results from 008-009'],
        'integrated_root': 'ConstructedClausiusControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['globally continuous extension of an eventually continuous past germ',
                 'actual interval-integral primitive with the prescribed local past derivative',
                 'area continuous at zero and initial value one for the constructed screen',
                 'actual temporal quadratic area limit equals minus Ricci(v,v)/2',
                 'matter contraction and stipulated heat flux continuous along the local curve',
                 'constructed heat primitive continuous with zero initial value and correct local rate',
                 'quadratic heat coefficient equals minus rate*T(v,v)/2',
                 'quadratic heat coefficient independent of the continuous extension',
                 'quadratic Clausius residual coefficient rate/2*(eta*Ricci(v,v)/(2*pi)-T(v,v))',
                 'Clausius vanishing equivalent to null Ricci balance for nonzero rate and eta',
                 'geometric pencil constructed from equilibrium screen and explicit Clausius hypothesis',
                 'conditional Einstein reconstruction with screen and heat constructed for each null direction',
                 'flat vacuum satisfies the constructed Clausius condition',
                 'flat symmetric conserved matter example has residual coefficient minus one half',
                 'symmetry and conservation alone do not force the constructed Clausius condition'],
        'inputs_and_unpaid': ['open subset of Coordinate4, smooth solder A and smooth inverse B',
                             'dimension four and prescribed Lorentzian signature',
                             'nonzero null tangent for each local construction',
                             'differentiable symmetric conserved tensor T on a connected open set',
                             'nonzero rate and entropy-density parameter eta',
                             'Clausius/H3 as an explicit independent physical input',
                             'stipulated energy-momentum heat flux versus actual physical or modular heat',
                             'null hypersurface immersion and integrated spatial horizon area',
                             'microscopic region-to-algebra and entropy-to-area identification',
                             'physical area unit, entropy density and thermodynamic temperature',
                             'modular origin of the solder and state-to-stress identification',
                             'global chart gluing', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 020 ESPONTÂNEA — área quadrática, integral de calor e reconstrução condicional de Einstein.',
        '', '06/09/2026. Continuação de 019. Auditoria independente da gerência pendente. Nenhuma alteração de gate.',
        '', '## Critérios', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO020_DERIVACAO_PREVIA.md. |',
        '| Área da tela em segunda ordem | PAGO | screen_area_quadratic_limit: (A(t)−1)/t² → −Ric(v,v)/2. |',
        '| Extensão contínua do germe | PAGO | pastContinuousExtension, com truncamento a um intervalo [a,0]. |',
        '| Integral efetiva do fluxo estipulado | PAGO | constructedHeat é uma integral intervalar; constructed_heat_rate prova sua derivada local. |',
        '| Coeficiente de calor | PAGO | constructed_heat_quadratic_limit: Q(t)/t² → −rate T(v,v)/2. |',
        '| Independência da extensão | PAGO | heat_extension_difference_quadratic_zero. |',
        '| Coeficiente do resíduo | PAGO | screen_clausius_coefficient: rate/2 × (η Ric(v,v)/(2π) − T(v,v)). |',
        '| Equivalência exata de Clausius | PAGO sob INPUT | constructed_clausius_at_iff; exige rate≠0 e η≠0. Clausius não foi deduzido da geometria. |',
        '| Construção de GeometricHorizonPencil | PAGO sob INPUT | horizonPencilFromScreen constrói os campos e a integral; recebe a condição de Clausius. |',
        '| Reconstrução geral em aberto conexo | PAGO CONDICIONAL | einstein_from_constructed_clausius: G+Λg=(2π/η)T, com todas as hipóteses expostas. |',
        '| Controle de vácuo plano | PAGO | flat_vacuum_clausius, com objetos efetivamente construídos. |',
        '| Controle negativo conservado | PAGO | conserved_matter_does_not_force_constructed_clausius: T=diag(1,0,0,0) é simétrico e conservado, mas o resíduo dividido por t² tende a −1/2. |',
        '| Justificação física de Clausius/H3 | NÃO PAGO | Condição explícita, equivalente à relação nula de Einstein nos dados considerados. |',
        '| Horizonte imerso, área espacial integrada e ponte microscópica | NÃO PAGO | A integral construída é temporal, e o nome do tipo não fornece uma hipersuperfície nula. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definições com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'As compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound. As contagens incluem lemas auxiliares, aplicações e controles.',
        '', '## Enunciado principal', '',
        'Dados U⊆R⁴ aberto e conexo, A,B suaves com AB=BA=I em U, T diferenciável, simétrico e covariantemente conservado, rate≠0 e η≠0, constrói-se para cada p∈U e v≠0 nulo uma congruência geodésica de equilíbrio, sua tela e a integral Q do fluxo estipulado −rate·t·T(V,V)·A(t).',
        'Se, para todos esses p e v, o resíduo Q(t)−rate·η/(2π)·(A(t)−1) dividido por t² tende a zero pela esquerda, existe uma constante Λ tal que G+Λg=(2π/η)T em U.',
        'O antecedente termodinâmico é ConstructedClausiusAt. O teorema constructed_clausius_at_iff mostra que ele equivale a Ric(v,v)=(2π/η)T(v,v). Ele não pode ser considerado demonstrado apenas porque Q foi integrado.',
        '', '## Controle que delimita o resultado', '',
        'Na solda identidade, Ric=0. Com T=diag(1,0,0,0), direção v=(1,1,0,0), rate=1 e η=2π, o tensor é simétrico e conservado, e T(v,v)=1. A área tem coeficiente quadrático zero; o calor e o resíduo têm coeficiente −1/2. Logo a condição de Clausius falha. Com T=0, o controle positivo satisfaz a condição.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation020.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando só lê e confere bytes, logs e axiomas registrados. A gerência deve recompilar em uma cópia para a auditoria independente. Ordem dos novos módulos:',
    ]
    rows.extend('- ' + m + '.lean' for m in MODULES)
    rows += ['', 'ConstructedClausiusControls importa a árvore inteira 020 e as dependências locais anteriores. O manifesto registra a ordem local completa. O wrapper documenta Lean 4.31.0/mathlib; não se declara um pacote portátil integral.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO020_DERIVACAO_PREVIA.md',
                   'CONTINUACAO020_PARECER.md', 'audit_continuation020.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += ['', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Somente as compilações finais limpas sustentam esta entrega; falhas intermediárias e avisos foram preservados.',
             '', '## Limites', '',
             'O avanço remove a primitiva e o lápis geométrico inteiro da lista de objetos recebidos como hipótese. Não remove Clausius: a nova equivalência e o controle negativo expõem precisamente esse limite.',
             'O fluxo de energia-momento é uma expressão matemática estipulada a partir de T. Sua identificação com calor físico ou energia modular, temperatura e coeficiente de entropia por área não foi demonstrada.',
             'A área é a área normalizada da tela transportada ao longo da curva. A integral é temporal. Não se construiu uma hipersuperfície nula imersa nem uma integral espacial de área sobre horizonte.',
             'Dimensão, assinatura e solda são INPUT. Região–álgebra, entropia–área microscópica, identificação do tensor T, Clausius/H3, origem modular da solda e globalização seguem OPEN.',
             'A constante Λ é obtida no aberto conexo considerado, por conservação e Bianchi já formalizados. Isso não equivale a construir uma variedade global ou demonstrar gravidade quântica.',
             '', 'Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. A custódia 019 foi reconferida em modo de leitura.',
             'O objetivo amplo permanece ativo e não alcançado. Incorporação pela gerência após auditoria; confirmação física reservada ao observador.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO020_PARECER.md') + '.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_020_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_020_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 020 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation020.py [--write]')




