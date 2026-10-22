"""Exact-byte and Lean-output audit for spontaneous continuation 022.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['HermitianTwoLevelFlow', 'TwoLevelSchrodinger', 'CorrelatedUnitaryState', 'UnitaryMarginalDynamics', 'UnitaryEntropyResponse', 'UnitaryClausiusBridge', 'UnitaryResponseControls']
MANIFEST = ROOT / 'CONTINUACAO022_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_022_ESPONTANEA_resposta_quadratica_por_dinamica_unitaria.md'
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

    visit('UnitaryResponseControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation022.py', 'revise_continuation022.py', 'verify_stage.ps1',
        'CONTINUACAO022_DERIVACAO_PREVIA.md', 'CONTINUACAO022_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO022_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation022.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation022.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'spontaneous continuation 022; no managerial order 022 issued at publication time', 'reuse': ['finite diagonal entropy and partial trace from 011', 'geometric screen and temporal heat primitive from 019-020', 'general diagonal state curve and relative entropy limit from 021', 'conditional general Einstein reconstruction from 008-021'], 'paid': ['Hermitian two-level Hamiltonian with involutive axis', 'one-parameter unitary group, actual Schrodinger derivative and Hamiltonian conservation', 'explicit amplitudes and unitary extension to the two-qubit correlated sector', 'positive normalized idempotent bipartite density with computed partial trace', 'globally nonnegative normalized marginal weights from amplitude squares', 'actual reduced-state derivative with zero initial tangent', 'relative entropy divided by t squared tends to zero on the actual marginal curve', 'entropy and modular quadratic coefficients equal frequency squared times transfer coefficient times log weight ratio', 'modular increment equals trace against the existing generator of the actual reduced density', 'conditional Clausius and Einstein implication for explicit unitary marginal matching', 'heat-modular matching forces null matter contraction equal to minus response divided by pi', 'positive response rules out matching with nonnegative null matter contraction', 'exact positive, negative, stationary and tracial response controls', 'actual flat-vacuum unitary matching with stationary marginal', 'no unitary matching for the incompatible flat conserved-matter control'], 'inputs_and_unpaid': ['axis, frequency and positive real initial amplitudes are selected inputs', 'this finite candidate dynamics is not selected by or identified with the canonical um.py dynamics', 'using the same parameter in unitary and geometric formulas is an explicit physical identification', 'heat-modular and entropy-area matching errors remain assumptions of order o(t squared)', 'dimension, Lorentzian signature, smooth solder and inverse, domain and matter regularity', 'symmetric conserved matter and connectedness in the Einstein implication', 'physical region-to-algebra and state-to-stress identification', 'noncommuting relative entropy, infinite or type-III limits and coherence between tower floors', 'physical area, temperature, entropy density, units and Newton coefficient', 'null horizon immersion and spatially integrated area', 'modular origin of geometry, global gluing and the broad quantum gravity objective'], 'criteria': [['Derivação antes do código', 'PAGO', 'CONTINUACAO022_DERIVACAO_PREVIA.md.'], ['Hamiltoniano e grupo unitário', 'PAGO', 'axis_hermitian, axis_square, pair_flow_group, pair_flow_adjoint_mul, pair_flow_mul_adjoint.'], ['Equação diferencial e energia total', 'PAGO', 'pair_flow_schrodinger e pair_energy_conserved.'], ['Estado bipartido produzido pelo fluxo', 'PAGO', 'correlated_flow_unitary, correlated_state_is_evolved e evolved_state_valid.'], ['Marginal e admissibilidade', 'PAGO', 'pair_amplitude_weights, pair_weights_nonnegative, pair_weights_normalized; positividade estrita perto da referência.'], ['Resposta inicialmente quadrática', 'PAGO', 'pair_weights_derivative, pair_tangent_at_zero e unitary_first_weight_response.'], ['Entropia relativa da trajetória efetiva', 'PAGO', 'unitary_relative_entropy_quadratic_zero: D/t²→0.'], ['Coeficientes de entropia e energia modular', 'PAGO', 'unitary_entropy_quadratic_limit, unitary_modular_quadratic_limit e unitary_marginal_modular_trace.'], ['Clausius e reconstrução de Einstein', 'PAGO CONDICIONAL', 'unitary_matching_gives_clausius e einstein_from_unitary_microscopic_matching.'], ['Restrição de sinal da matéria', 'PAGO CONDICIONAL / NEGATIVO', 'unitary_heat_matching_requires_matter e positive_response_blocks_nonnegative_heat_matching.'], ['Controles exatos', 'PAGO', 'Hamiltonianos admissíveis com respostas (7/25)log(16/9)>0 e (−176/625)log(16/9)<0; controles estacionário e tracial.'], ['Habitante do novo contrato', 'PAGO em controle plano', 'flatUnitaryVacuumMatching: eixo diagonal, marginal estacionária, calor e área de 020.'], ['Recusa do controle incompatível', 'PAGO', 'flat_incompatible_matter_has_no_unitary_matching.'], ['Identificações físicas gerais', 'NÃO PAGO', 'Os dois erros pequenos e a relação entre parâmetros permanecem INPUT/OPEN.'], ['Dinâmica canônica e gravidade quântica', 'NÃO PAGO', 'Modelo finito candidato; nenhum novo veredito de gate.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation.'},

        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'UnitaryResponseControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 022 ESPONTÂNEA — resposta quadrática de uma evolução unitária explícita.',
        '', '06/09/2026. Continuação de 021. Auditoria independente da gerência pendente. Nenhuma alteração de gate.',
        '', '## Critérios', '', '| Critério | Estado | Evidência |', '|---|---|---|',
    ]
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += [
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definições com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'Todas as compilações finais fixadas: exit 0, fonte estável, sem erros, avisos ou sorryAx. Axiomas permitidos: propext, Classical.choice, Quot.sound. A contagem inclui lemas auxiliares e controles.',
        '', '## Resultado e alcance', '',
        'O eixo M=[[a,b],[b,−a]], com a²+b²=1, define H=ωM e U(t)=cos(ωt)I−i sin(ωt)M. O código verifica o grupo unitário, U′=−iHU e U†HU=H. A energia total conservada não é identificada com o gerador modular da marginal.',
        'A partir de Ψ(0)=u|00>+v|11>, u,v>0, u²+v²=1, a evolução dá amplitudes complexas explícitas. A extensão do fluxo ao espaço bipartido é unitária; sua ação coincide com o estado construído. A densidade é positiva, tem traço um e é idempotente.',
        'O traço parcial efetivo é diagonal: r0(t)=u²+C sin²(ωt), r1(t)=v²−C sin²(ωt), C=(au+bv)²−u². A não negatividade global vem dos módulos quadrados; a referência estritamente positiva garante fidelidade local.',
        'A tangente inicial da marginal zera. Portanto D(r(t)||r(0))/t²→0. As variações ΔS/t² e ΔK/t² convergem a L=ω²C log(v²/u²). A fórmula é da marginal diagonal; não se aplica a mesma entropia relativa ao estado bipartido puro.',
        'UnitaryScreenMatching contém os parâmetros unitários, a referência normalizada e os dois erros de identificação E_heat/t²→0 e E_area/t²→0. Sob essas hipóteses, a identidade B=E_heat+cD+cE_area de 021 fornece Clausius e a reconstrução condicional G+Λg=(2π/η)T. O contrato não recebe Einstein como campo, mas ainda exige as identificações físicas.',
        'A tangente nula foi demonstrada para esta família e suas amplitudes iniciais reais selecionadas. Não foi demonstrada para toda evolução unitária ou para estados iniciais arbitrários.',
        'O uso do mesmo t nos estados e na curva geométrica é INPUT. Não há uma mudança livre de parâmetro afim nem uma demonstração de que esse Hamiltoniano é a dinâmica canônica do um.py.',
        '', '## Controles e restrição de sinal', '',
        'Para u=3/5, v=4/5 e ω=1: a=0,b=1 dá C=7/25; a=−3/5,b=4/5 dá C=−176/625. Os dois eixos satisfazem a²+b²=1. Como log(16/9)>0, o sinal da resposta muda com o Hamiltoniano. Os limites da entropia foram instanciados nos dois casos.',
        'A correspondência calor–modular, combinada com o calor integrado de 020 e rate≠0, exige T_x(direction,direction)=−L/π. Assim, L>0 é incompatível com contração nula não negativa da matéria. L<0 retira essa obstrução de sinal; não demonstra a correspondência completa.',
        'O eixo diagonal a=1,b=0 mantém os pesos fixos. Uma referência tracial tem resposta modular quadrática zero. Esses controles preservam os casos degenerados.',
        'flatUnitaryVacuumMatching realiza os dois erros pequenos no controle plano de vácuo com eixo diagonal e marginal estacionária. É uma realização explícita do contrato; não fornece resposta gravitacional não nula. O controle plano conservado incompatível não admite UnitaryScreenMatching.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation022.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando só lê e confere bytes, logs e axiomas registrados. Recompilação independente é feita pela gerência em cópia. Ordem dos novos módulos:',
    ]
    rows.extend('- '+module+'.lean' for module in MODULES)
    rows += [
        '', 'O manifesto fixa a árvore local e registra sua ordem. Lean/mathlib externos são resolvidos pelo wrapper; não é um pacote portátil integral.',
        '', '## Axiomas impressos', '', '\u0060\u0060\u0060text',
    ]
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration']+': ['+', '.join(item['axioms'])+']')
    rows += [
        '\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
        f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
        f"Inventário: {len(data['files'])} caminhos absolutos, com tamanho e hash dos bytes.",
        '', '| Artefato principal | SHA256 |', '|---|---|',
    ]
    primary = {str(ROOT / (m+'.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO022_DERIVACAO_PREVIA.md',
        'CONTINUACAO022_PARECER.md', 'audit_continuation022.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += [
        '', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Apenas as compilações finais limpas sustentam a entrega.',
        '', '## Limites', '',
        'O modelo é finito, com marginais comutantes. A evolução unitária finita aqui construída não substitui o regime hiperbólico da face e não contorna a obstrução de Borchers da torre-produto.',
        'Não foram demonstradas seleção canônica do Hamiltoniano, coerência entre andares ou regiões, limite tipo III, origem modular da solda, dimensão/assinatura sem entrada, identificação do tensor T, unidades físicas ou globalização.',
        'Os dados de cada tela no contrato podem ser escolhidos separadamente. Coerência entre essas escolhas não foi postulada como conclusão nem provada.',
        'Calor–modular e entropia–área de ordem o(t²), parâmetro físico, horizonte imerso e área espacial integrada continuam OPEN.',
        '', 'Nenhum um.py executado, importado ou editado. Escritas somente em Chatgpt. Originais, entregas anteriores, kernel canônico, Atlas, memórias, selos e gate intocados. A custódia 021 foi reconferida em leitura.',
        'O objetivo amplo permanece ativo e não alcançado. Incorporação depende da auditoria independente da gerência; confirmação física é ato do observador.',
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO022_PARECER.md')+'.',
        '', 'Ordens de entrada encontradas no inventário:',
    ]
    rows.extend('- '+path for path in data['incoming_orders'])
    return '\n'.join(rows)+'\n'


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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_022_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_022_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 022 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation022.py [--write]')




