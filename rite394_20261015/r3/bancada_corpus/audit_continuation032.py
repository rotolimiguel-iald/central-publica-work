"""Exact-byte and Lean-output audit for spontaneous continuation 032.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'PhaseFrequencySeparation',
    'ModularEigenRecognition',
    'ModularDomainCommutation',
    'RelativeModularProduct',
]
MANIFEST = ROOT / 'CONTINUACAO032_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_032_ESPONTANEA_comutacao_modular_e_dominio.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

NARRATIVE = {
    "status": "REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending",
    "kind": "Spontaneous continuation 032 of order 007; modular domain commutation and equality of the relative operator with exp(L) Delta",
    "reuse": [
        "Total local eigenvector family of the actual reference Delta and modular flow, with weak graph recognition already verified in Chatgpt",
        "Summable profile family of 028 and bounded log-likelihood generator and exponential filter of 030",
        "Relative Tomita closure, maximal adjoint and positive self-adjoint congruence Delta_rel=R Delta R with explicit pullback domain from 031"
    ],
    "paid": [
        "Continuous real frequencies are separated by their phases at every real modular time when the scalar coefficient is nonzero; the proof differentiates at zero",
        "Finite matrix-unit tests recover all local weak Delta tests; a vector with flow frequency r belongs to the actual Delta graph with value exp(r) times that vector",
        "For a bounded self-adjoint operator B fixed by every reference modular automorphism, B preserves D(Delta) and Delta B x=B Delta x on that domain, using weak tests",
        "The concrete filter R=exp(L/2) and inverse V=exp(-L/2) commute with the reference flow, preserve D(Delta), and commute with Delta on that domain",
        "The inverse identities and preservation in both directions prove D(Delta_rel)=D(Delta), not merely one inclusion",
        "The relative operator from 031 equals the explicitly defined partial operator exp(L) Delta as a LinearPMap with its actual domain",
        "The product exp(L) Delta inherits positivity, self-adjointness and closure from the constructed relative operator",
        "The bounded generator L itself preserves D(Delta) and commutes with Delta there; the reference control at state parameter t=0 recovers the original Delta exactly"
    ],
    "inputs_and_unpaid": [
        "The concrete state family remains the specified summable commuting product perturbation, with reference weights (1/3,2/3), 0<=b_n<=1/12 and h(t)=t^2/(1+t^2). No arbitrary pair of faithful states is substituted.",
        "The generic domain theorem requires B bounded and self-adjoint. It does not assume B positive or invertible. Invertibility is used separately for the concrete equality of relative and reference Delta domains.",
        "Frequency separation uses equality for every real modular time. Equality at discrete times alone would retain periodic ambiguity and is not used as a substitute.",
        "The actual extension from local eigenvector tests to the full Delta domain uses weak tests and self-adjointness of B; it does not assume that B preserves a finite tower level.",
        "Commutation on the explicit unbounded domain and the equality Delta_rel=exp(L) Delta are proved. This stage does not formalize a generic joint spectral calculus or relative imaginary powers.",
        "The relative logarithm, a full Connes Radon-Nikodym identification and the identification with Araki entropy remain open obligations. The previously constructed cocycle is not relabeled as an established spectral relative power.",
        "This stage does not additionally prove equality of the relative and original Tomita domains or identify their polar conjugations.",
        "The angular observable, geometric screen area, length scale, region-algebra map, general H3 and physical graviton dynamics are not identified by this domain theorem.",
        "Final counts include auxiliary lemmas and controls; they do not measure completion of quantum gravity.",
        "Original canonical files, um.py, Atlas, memories, gates, seals and previous deliveries remain untouched. Independent managerial audit and incorporation remain pending."
    ],
    "criteria": [
        [
            "Derivação anterior ao código",
            "PAGO",
            "CONTINUACAO032_DERIVACAO_PREVIA.md; a rota formalizada para B autoadjunto usa testes fracos."
        ],
        [
            "Separação das frequências reais",
            "PAGO",
            "phase_frequency_separation, modular_phase_frequency_separation, modular_phase_frequency_iff."
        ],
        [
            "Reconhecimento do gráfico de Delta",
            "PAGO",
            "weak_delta_of_eigen_tests, delta_graph_of_eigen_tests, flow_eigen_implies_delta_graph."
        ],
        [
            "Invariância modular e fluxo",
            "PAGO",
            "modular_fixed_commutes_with_flow, flow_commuting_modular_fixed."
        ],
        [
            "Domínio e comutação para B autoadjunto",
            "PAGO SOB HIPÓTESES EXPLÍCITAS",
            "commuting_operator_delta_graph, commuting_operator_preserves_delta_domain, commuting_operator_delta_apply."
        ],
        [
            "Aplicação ao filtro e seu inverso",
            "PAGO",
            "filter_preserves_delta_domain, inverse_filter_preserves_delta_domain, filter_delta_commutes, inverse_filter_delta_commutes."
        ],
        [
            "Igualdade dos domínios de Delta",
            "PAGO",
            "filter_delta_domain_iff, relative_delta_original_domain."
        ],
        [
            "Igualdade dos operadores parciais",
            "PAGO",
            "relative_delta_product_value, relative_delta_eq_likelihood_product; igualdade de LinearPMap."
        ],
        [
            "Positividade, auto-adjunticidade e fecho",
            "PAGO",
            "likelihood_modular_product_positive, likelihood_modular_product_selfadjoint, likelihood_modular_product_closed."
        ],
        [
            "Gerador e controle de referência",
            "PAGO",
            "generator_preserves_delta_domain, generator_delta_commutes, relative_delta_reference_control."
        ],
        [
            "Cálculo funcional e potências relativas",
            "NÃO PAGO",
            "Comutação no domínio não é apresentada como uma formalização genérica de cálculo espectral."
        ],
        [
            "Identificação Connes/Araki",
            "NÃO PAGO",
            "A identificação relativa completa exige caracterização ou construção adicional."
        ],
        [
            "Área geométrica e reconstrução geral",
            "NÃO PAGO",
            "A prova não seleciona tela, escala ou dinâmica gravitacional."
        ]
    ],
    "dependency_limit": "Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved read-only by verify_stage.ps1. This is not a portable full bundle or independent recompilation."
}


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
    pattern = (
        r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]"
        r"|does not depend on any axioms)"
    )
    result = []
    for match in re.finditer(pattern, output):
        names = match.group(2) or ''
        result.append({
            'declaration': match.group(1),
            'axioms': [name.strip() for name in names.split(',') if name.strip()],
        })
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
    if namespace != 'ChatgptAudit.Commutation032':
        raise RuntimeError(f'Unexpected namespace: {module}')
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
                        'record_kind': 'bench_interruption_note' if out.startswith('BENCH INTERRUPTION RECORD') else 'lean_compiler_output',
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

    visit('RelativeModularProduct')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation032.py', 'revise_continuation032.py', 'verify_stage.ps1',
        'CONTINUACAO032_DERIVACAO_PREVIA.md', 'CONTINUACAO032_PARECER.md',
        'CONTINUACAO031_MANIFESTO.json',
        'audit_continuation031.py',
        'TUNEL/DO_CHATGPT/ENTREGA_031_ESPONTANEA_operador_modular_relativo.md',
        'CONTINUACAO030_MANIFESTO.json',
        'audit_continuation030.py',
        'TUNEL/DO_CHATGPT/ENTREGA_030_ESPONTANEA_cociclo_global_e_leitura_angular.md',
        'TUNEL/DO_CHATGPT/ENTREGA_030_ERRATA001_referencia_nominal.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO029_MANIFESTO.json', 'audit_continuation029.py', 'CONTINUACAO028_MANIFESTO.json', 'audit_continuation028.py', 'CONTINUACAO027_MANIFESTO.json', 'audit_continuation027.py', 'CONTINUACAO026_MANIFESTO.json', 'audit_continuation026.py', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/Cocycle.lean', 'fontes/tgl_kernel/TGLExt/Ergodicity.lean', 'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO032_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation032.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation032.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **NARRATIVE,
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'RelativeModularProduct',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = [
    "[REAL / INPUT / OPEN] ENTREGA 032 ESPONTÂNEA — comutação modular e domínio do operador relativo.",
    "",
    "06/09/2026. Continuação da ordem 007. A prova ampla permanece aberta; auditoria independente da gerência pendente.",
    "",
    "A igualdade de fases para todos os tempos modulares reais separa as frequências quando o coeficiente é não nulo. A derivada em zero paga essa separação, sem substituir o contínuo por uma amostra de tempos discretos.",
    "",
    "Usando a família local de autovetores da torre e os testes fracos já construídos, provou-se que U_s x=exp(i s r)x para todo s implica que (x,exp(r)x) pertence ao gráfico efetivo de Delta. O reconhecimento inclui o domínio do operador não limitado.",
    "",
    "Para B limitado e autoadjunto, fixo por todas as automorfias modulares da referência, B preserva D(Delta) e Delta B x=B Delta x nesse domínio. A extensão usa testes fracos e a auto-adjunticidade de B; não exige que B seja positivo, invertível ou preserve um andar finito.",
    "",
    "O resultado foi aplicado a R=exp(L/2), V=exp(-L/2) e ao gerador limitado L da família somável. A preservação pelos dois filtros inversos identifica D(Delta_rel)=D(Delta).",
    "",
    "O operador relativo construído na 031 satisfaz Delta_rel=exp(L) Delta como igualdade de LinearPMap, com o domínio incluído. O produto explícito herda positividade, auto-adjunticidade e fecho. No parâmetro de estado t=0, o operador relativo é exatamente o Delta de referência.",
    "",
    "Esta etapa demonstra comutação no domínio e a identidade do produto. Não constrói um cálculo funcional conjunto genérico, potências imaginárias relativas ou o logaritmo relativo; as identificações completas Connes/Araki permanecem abertas.",
    "",
    "A inscrição angular, a área geométrica e a reconstrução gravitacional geral continuam exigindo suas próprias ligações. A identidade entre operadores não seleciona superfície, escala ou dinâmica física.",
    "",
    "A custódia inclui manifesto, auditor e entrega 031, bem como a cadeia anterior e a errata nominal da 030. As etapas seladas foram preservadas."
]


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation032.py'}'", '\u0060\u0060\u0060',
             '', 'Comando somente leitura; recompilacao independente em copias, na ordem do manifesto:']
    rows.extend('- '+str(ROOT / (module+'.lean')) for module in MODULES)
    rows += ['', '## Axiomas', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration']+': ['+', '.join(item['axioms'])+']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos',
             '', f"Manifesto: {MANIFEST}; SHA256 dos bytes: {digest(MANIFEST)}.",
             f"Inventario: {len(data['files'])} caminhos, com tamanho e SHA256.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m+'.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO032_DERIVACAO_PREVIA.md','CONTINUACAO032_PARECER.md','audit_continuation032.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| {item['path']} | {item['sha256']} |")
    rows += ['', '## Tentativas rejeitadas preservadas', '']
    rejected = 0
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rejected += 1
                rows.append(f"- {run['rejected_copy']}: exit {run['exit_code']}; copia dos bytes do log.")
    rows += ['', f'{rejected} tentativas rejeitadas preservadas com logs e fontes em backups dos bytes.',
             '', '## Limites e dividas', '']
    rows.extend('- '+item for item in data['inputs_and_unpaid'])
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO032_PARECER.md'),
             '', 'Ordens encontradas:']
    rows.extend('- '+p for p in data['incoming_orders'])
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_032_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_032_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 032 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation032.py [--write]')



