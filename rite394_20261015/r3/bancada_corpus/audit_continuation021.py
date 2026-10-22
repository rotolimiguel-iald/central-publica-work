"""Exact-byte and Lean-output audit for spontaneous continuation 021.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['DiagonalRelativeEntropy', 'DiagonalStateCurve', 'RelativeEntropyFisherLimit', 'QuadraticStateResponse', 'MicroscopicClausiusBridge', 'MicroscopicEinsteinBridge', 'RelativeEntropyGravityControls']
MANIFEST = ROOT / 'CONTINUACAO021_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_021_ESPONTANEA_entropia_relativa_e_ponte_de_segunda_ordem.md'
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

    visit('RelativeEntropyGravityControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation021.py', 'revise_continuation021.py', 'verify_stage.ps1',
        'CONTINUACAO021_DERIVACAO_PREVIA.md', 'CONTINUACAO021_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO021_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation021.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation021.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 021; no managerial order 021 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['constructed screen, temporal heat integral and Clausius coefficient from 020',
                  'conditional general Einstein reconstruction from 008-020',
                  'finite diagonal entropy and explicit Schmidt cut purification from 011',
                  'canonical first_law_diagonal and canonical towerW positivity and normalization'],
        'integrated_root': 'RelativeEntropyGravityControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['exact diagonal relative entropy equals modular increment minus entropy increment',
                 'modular increment equals the trace against the existing diagonal modular generator',
                 'positive definite diagonal Fisher quadratic form for a strictly positive reference',
                 'trace-preserving state curves with actual local derivatives',
                 'strict positivity of weights near the initial reference state',
                 'zero trace of the tangent derived from normalization',
                 'actual relative entropy derivative and first-order cancellation',
                 'quadratic relative entropy coefficient equals Fisher(initial tangent)/2',
                 'quadratic defect vanishes exactly when the initial state tangent vanishes',
                 'explicit affine and quadratic normalized state responses',
                 'quadratic entropy and modular response coefficients agree',
                 'exact decomposition of the Clausius residual into two matching errors and relative entropy',
                 'conditional local compatibility eta*Ricci(v,v)=2*pi*T(v,v)+Fisher',
                 'conditional Einstein reconstruction from quadratic response and two explicit matching errors',
                 'first-order entropy equilibrium does not imply quadratic relative entropy cancellation',
                 'nontracial quadratic entropy and modular coefficients equal log(2)>0',
                 'nearby normalized pure bipartite states with the prescribed diagonal marginals',
                 'finite canonical tower instantiation for each floor and trace-zero response',
                 'actual flat-vacuum matching with a nonconstant quadratic state curve',
                 'no quadratic matching for the incompatible flat conserved-matter control'],
        'inputs_and_unpaid': ['finite commuting density description and strictly positive reference weights',
                             'normalized differentiable state curve with initial continuous tangent',
                             'a physical relation between state perturbation and geometric affine parameter',
                             'quadratic response as a mathematical family rather than a derived microscopic dynamics',
                             'entropy-area and heat-modular matching errors are still explicit assumptions',
                             'physical region-to-algebra and state-to-stress identification',
                             'noncommuting quantum relative entropy and the infinite/type-III limit',
                             'coherence of responses between tower floors',
                             'null hypersurface immersion and integrated spatial horizon area',
                             'physical area unit, temperature, entropy density and Newton coefficient',
                             'dimension, Lorentzian signature, smooth solder and inverse',
                             'symmetric conserved matter for the Einstein implication',
                             'modular origin of geometry, global gluing and broad quantum gravity objective'],
        'references': [
            {'title': 'Jacobson, Thermodynamics of Spacetime (1995)',
             'url': 'https://arxiv.org/abs/gr-qc/9504004',
             'scope': 'Entropy-area and Clausius premises; not imported as a proof of the missing matches'},
            {'title': 'Jacobson, Entanglement Equilibrium and the Einstein Equation (2016)',
             'url': 'https://arxiv.org/abs/1505.04753',
             'scope': 'First-order vacuum variations with geometric and matter hypotheses'},
            {'title': 'Lashkari and Van Raamsdonk, Canonical Energy is Quantum Fisher Information (2016)',
             'url': 'https://arxiv.org/html/1508.00897v2',
             'scope': 'Relative entropy, first versus second order; holographic identification not transferred to this tower'},
        ],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / KNOWN / OPEN] ENTREGA 021 ESPONTÂNEA — entropia relativa e a ordem necessária à ponte gravitacional.',
        '', '06/09/2026. Continuação de 020. Auditoria independente da gerência pendente. Nenhuma alteração de gate.',
        '', '## Critérios', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO021_DERIVACAO_PREVIA.md. |',
        '| Identidade modular exata | PAGO | relative_entropy_identity: D=ΔK−ΔS, na face diagonal finita. |',
        '| Ponte com o gerador existente | PAGO | modular_increment_is_generator_trace: ΔK é o traço contra diagonalModularGenerator. |',
        '| Positividade do coeficiente | PAGO | diagonal_fisher_nonneg e diagonal_fisher_zero_iff. |',
        '| Curva de estados admissível perto da origem | PAGO sob INPUT | DiagonalStateCurve, state_curve_positive_near e state_curve_tangent_trace. |',
        '| Limite quadrático de entropia relativa | PAGO | relative_entropy_curve_quadratic_limit: D/t²→F_p(q)/2. |',
        '| Critério exato de anulação | PAGO | relative_entropy_quadratic_zero_iff: D/t²→0 se e somente se q(0)=0. |',
        '| Resposta quadrática efetiva | PAGO | quadraticStateCurve: p+t²q; limites de ΔS e ΔK calculados. |',
        '| Decomposição do resíduo geométrico | PAGO | residual_entropy_decomposition: B=E_heat+cD+cE_area. |',
        '| Compatibilidade local | PAGO CONDICIONAL | geometric_microscopic_compatibility: η Ric(v,v)=2π T(v,v)+F_p(q). |',
        '| Reconstrução tensorial | PAGO CONDICIONAL | einstein_from_quadratic_microscopic_matching, com os dois erros de identificação no antecedente. |',
        '| Contraexemplo à passagem automática de ordem | PAGO | first_order_does_not_imply_second_order: S′(0)=0 e D/t→0, mas D/t²→2. |',
        '| Resposta não tracial não nula | PAGO | nontracial_quadratic_response: coeficientes de ΔS e ΔK iguais a log 2>0, D/t²→0. |',
        '| Purificação da família local | PAGO | state_curve_purification_near: positividade, traço um, idempotência e marginal diagonal. |',
        '| Instância nos pesos canônicos | PAGO | tower_quadratic_relative_zero, em cada andar finito e para resposta de traço zero. |',
        '| Habitante do novo contrato | PAGO em controle plano | flatVacuumMatching usa área e calor de 020 e uma curva de estados não constante. |',
        '| Recusa do controle incompatível | PAGO | flat_nonzero_matter_has_no_quadratic_matching. |',
        '| Identificações microscópicas gerais | NÃO PAGO | Os dois erros de identificação ainda precisam ser demonstrados a partir do modelo. |',
        '| Dinâmica física, limite não comutativo e gravidade quântica | NÃO PAGO | Não se promove a resposta quadrática escolhida a lei física. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definições com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'As compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound. As contagens incluem lemas auxiliares, aplicações e controles.',
        '', '## Resultado que muda o próximo passo', '',
        'A primeira lei de entropia é uma igualdade de primeira variação do estado. Ela não torna automaticamente desprezível o resíduo de ordem t² exigido pelo balanço geométrico de 020. Para uma curva diagonal normalizada, com referência estritamente positiva, D/t²→(1/2)Σ_i q_i(0)²/p_i. A anulação exige q(0)=0.',
        'A resposta p(t)=p+t²q fornece esse jato zero e permite variação real do estado. Sua normalização é exata, e a positividade foi provada perto de zero. Identificar essa resposta com uma dinâmica física no parâmetro afim da curva continua sendo conteúdo a demonstrar.',
        'O resíduo de Clausius separa-se em erro calor–modular, entropia relativa e erro entropia–área. Se os dois erros divididos por t² tendem a zero, a resposta quadrática permite deduzir Clausius e aplicar a reconstrução tensorial. O novo contrato QuadraticScreenMatching contém precisamente os dados finitos e esses dois limites; não recebe Clausius como campo.',
        'Para uma resposta geral, a compatibilidade local exige η Ric(v,v)=2π T(v,v)+F_p(q). É uma implicação sob identificações assumidas. Não foi demonstrado que F define um tensor conservado, uma energia gravitacional ou uma correção física de Einstein.',
        '', '## Controles', '',
        'p=(1/2,1/2), q=(1,−1): a resposta afim tem primeira variação de entropia zero, mas D/t²→2. A resposta quadrática tem D/t²→0 e varia o estado para t≠0.',
        'p=(1/3,2/3), q=(1,−1): na resposta quadrática, ΔS/t² e ΔK/t² tendem a log 2>0. Logo o resultado positivo não se restringe a uma resposta modular nula.',
        'Na geometria plana de 020 com T=0, foi construído flatVacuumMatching, com área, calor e curva de estados efetivos. O exemplo plano com T=diag(1,0,0,0), simétrico e conservado, não admite esse contrato.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation021.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando só lê e confere bytes, logs e axiomas registrados. A gerência deve recompilar em uma cópia para a auditoria independente. Ordem dos novos módulos:',
    ]
    rows.extend('- ' + m + '.lean' for m in MODULES)
    rows += ['', 'RelativeEntropyGravityControls importa toda a árvore 021 e as dependências locais anteriores. O manifesto registra a ordem local completa. O wrapper documenta Lean 4.31.0/mathlib; não se declara pacote portátil integral.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO021_DERIVACAO_PREVIA.md',
                   'CONTINUACAO021_PARECER.md', 'audit_continuation021.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += ['', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Somente as compilações finais limpas sustentam esta entrega; falhas intermediárias e avisos foram preservados.',
             '', '## Referências e alcance', '',
             '[KNOWN] Jacobson deriva a equação de estado gravitacional com entropia–área e Clausius como premissas: [Jacobson 1995](https://arxiv.org/abs/gr-qc/9504004). A discussão de equilíbrio de entrelaçamento envolve primeira variação do vácuo e hipóteses próprias: [Jacobson 2016](https://arxiv.org/abs/1505.04753).',
             '[KNOWN] A distinção entre primeira lei e termo quadrático de entropia relativa é explícita em [Lashkari–Van Raamsdonk, seção 2.1](https://arxiv.org/html/1508.00897v2). Sua identificação com energia canônica depende do contexto holográfico. Não se transporta esse resultado para a torre apenas pela palavra modular.',
             '', '## Limites', '',
             'A fórmula de Fisher provada é a da face diagonal finita. Não se afirma um teorema de entropia relativa para operadores não comutantes ou para o limite tipo III.',
             'A normalização da curva é global como função matemática; a positividade e a interpretação de estado são locais. Não se atribui interpretação física a pesos eventualmente negativos longe da origem.',
             'A purificação foi calculada ponto a ponto. Não fornece por si uma evolução física, coerência entre andares, rede de regiões ou identificação de energia modular com fluxo geométrico.',
             'A hipótese temporal p(t)=p+t²q não é uma mudança livre do parâmetro afim geométrico. O modelo microscópico precisa justificar a relação entre esses parâmetros e os dois erros de identificação.',
             'Região–álgebra, entropia–área física, calor–energia modular, identificação do tensor T, unidade e coeficiente, horizonte imerso, área espacial integrada, origem modular da solda e globalização permanecem OPEN.',
             '', 'Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. A custódia 020 foi reconferida em modo de leitura.',
             'O objetivo amplo permanece ativo e não alcançado. Incorporação pela gerência após auditoria; confirmação física reservada ao observador.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO021_PARECER.md') + '.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_021_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_021_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 021 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation021.py [--write]')




