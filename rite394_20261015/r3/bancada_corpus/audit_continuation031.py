"""Exact-byte and Lean-output audit for spontaneous continuation 031.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'RelativeFilterInverse',
    'BoundedPositiveCongruence',
    'RelativeTomitaClosure',
    'RelativeModularOperator',
]
MANIFEST = ROOT / 'CONTINUACAO031_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_031_ESPONTANEA_operador_modular_relativo.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

NARRATIVE = {
    "status": "REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending",
    "kind": "Spontaneous continuation 031 of order 007; relative Tomita closure and positive self-adjoint relative modular operator with exact domains",
    "reuse": [
        "Faithful global product states and modular transport of 026-027",
        "Summable profile family of 028",
        "Positive bounded invertible filter R=exp(L/2), exact preparation R Omega=Psi, and global cocycle of 030",
        "Closed reference Tomita operator, maximal antilinear adjoint, and positive self-adjoint reference Delta already verified in Chatgpt"
    ],
    "paid": [
        "Explicit inverse V=exp(-L/2), V and R in the factor, both inverse identities, and continuous linear equivalence defined by R",
        "Exact homeomorphism of the algebraic graphs and their closures: the relative rule A Omega -> A* Psi has closure S_rel=S_omega composed with R",
        "Single-valued closed relative Tomita graph and dense domain {x | R x belongs to D(S_omega)}",
        "Maximal antilinear adjoint S_rel^dagger=R composed with S_omega^dagger, with adjoint domain characterized by the pairing",
        "Generic bounded congruence e T e: exact graph, dense pullback domain, closure, formal adjoint, positive quadratic form and self-adjointness under the stated hypotheses",
        "Relative Delta=R Delta_omega R is closed, densely defined, positive and self-adjoint on {x | R x belongs to D(Delta_omega)}",
        "Exact domain criterion for S_rel^dagger S_rel, equality with relative Delta on that domain, and quadratic identity Re<x,Delta_rel x>=||S_rel x||^2"
    ],
    "inputs_and_unpaid": [
        "The concrete state family remains specified: reference weights (1/3,2/3), 0<=b_n<=1/12, summable b, and h(t)=t^2/(1+t^2). This is not a theorem about every pair of faithful states.",
        "The relative convention is S^0_{psi|omega}(A Omega)=A* Psi. Its closure is constructed by a homeomorphism of the actual algebraic graphs, not assigned by a name.",
        "The domains are pullbacks by the bounded invertible filter R. Equality with the original Tomita or Delta domains is not proved in this stage.",
        "This stage does not prove preservation of the original unbounded domains by R, strong commutation with Delta_omega, or the simplification Delta_rel=exp(L) Delta_omega.",
        "The imaginary powers and logarithm of the relative unbounded operator are not constructed here. No full identification of the previously built cocycle with the Connes Radon-Nikodym derivative or of its expectation with Araki entropy is claimed.",
        "The graph construction gives the relative operator for the actual vectors Psi and Omega. Identification with Connes may use relative spectral calculus or an equivalent characterization; formalizing the natural cone is one possible route, not a mandatory prerequisite. Identification of the relative polar conjugation with the existing J needs its own proof.",
        "Positive relative modular quadratic forms do not identify a geometric screen area. The angular reading, length scale, region-algebra map, general H3 and physical graviton dynamics remain open.",
        "Final counts include auxiliary lemmas and do not measure completion of quantum gravity.",
        "Original canonical files, um.py, Atlas, memories, gates, seals and previous deliveries remain untouched. Independent managerial audit and incorporation remain pending."
    ],
    "criteria": [
        [
            "Derivação anterior ao código",
            "PAGO",
            "CONTINUACAO031_DERIVACAO_PREVIA.md."
        ],
        [
            "Filtro inverso efetivo",
            "PAGO",
            "filter_mul_inverse, inverse_mul_filter, inverse_filter_selfadjoint, inverse_filter_mem_factor."
        ],
        [
            "Gráfico relativo e fecho",
            "PAGO",
            "relative_tomita_graph_image, relative_tomita_closed_graph_image, relative_tomita_closed_graph_eq."
        ],
        [
            "Domínio efetivo de S relativo",
            "PAGO",
            "relative_tomita_domain_iff, relative_tomita_domain_dense, relative_tomita_extends_star."
        ],
        [
            "Adjunto antilinear maximal",
            "PAGO",
            "relative_tomita_adjoint_pairing, relative_tomita_adjoint_maximal, relative_tomita_adjoint_domain_iff."
        ],
        [
            "Congruência genérica",
            "PAGO SOB HIPÓTESES EXPLÍCITAS",
            "bounded_congruence_graph_iff, bounded_congruence_closed, bounded_congruence_selfadjoint, bounded_congruence_positive."
        ],
        [
            "Operador modular relativo",
            "PAGO",
            "relative_delta_domain_iff, relative_delta_domain_dense, relative_delta_closed, relative_delta_selfadjoint, relative_delta_positive."
        ],
        [
            "Composição com domínio",
            "PAGO",
            "relative_composition_domain, relative_tomita_adjoint_comp_is_delta, relative_delta_quadratic_is_tomita_norm."
        ],
        [
            "Domínios originais e comutação",
            "NÃO PAGO",
            "Não se afirma D_rel=D_original nem Delta_rel=exp(L) Delta_omega."
        ],
        [
            "Potências e identificação Connes/Araki",
            "NÃO PAGO",
            "A identificação espectral do cociclo relativo e a entropia de Araki exigem demonstrações adicionais."
        ],
        [
            "Área geométrica e reconstrução geral",
            "NÃO PAGO",
            "A congruência positiva não seleciona tela, escala ou dinâmica; a lei geral de área continua aberta."
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
    if namespace != 'ChatgptAudit.Relative031':
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

    visit('RelativeModularOperator')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation031.py', 'revise_continuation031.py', 'verify_stage.ps1',
        'CONTINUACAO031_DERIVACAO_PREVIA.md', 'CONTINUACAO031_PARECER.md',
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
    paths.update(ROOT.glob('CONTINUACAO031_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation031.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation031.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **NARRATIVE,
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'RelativeModularOperator',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = [
    "[REAL / INPUT / OPEN] ENTREGA 031 ESPONTÂNEA — operador modular relativo com domínio e fecho.",
    "",
    "06/09/2026. Continuação da ordem 007. A prova ampla permanece aberta; auditoria independente da gerência pendente.",
    "",
    "Para a família somável da 028, reutiliza-se o filtro R=exp(L/2) da 030, limitado, positivo, invertível e pertencente ao fator, com R Omega=Psi. Foi construído seu inverso explícito V=exp(-L/2), também no fator, e a equivalência linear contínua definida por R.",
    "",
    "A regra relativa é S^0_{psi|omega}(A Omega)=A* Psi. O homeomorfismo (x,y)->(V x,y) leva exatamente o gráfico algébrico do Tomita de referência ao gráfico relativo e transporta os fechos. Assim S_rel=S_omega composto com R é o fecho efetivo, unívoco e densamente definido, em {x | R x pertence a D(S_omega)}.",
    "",
    "O adjunto antilinear S_rel^dagger=R composto com S_omega^dagger foi caracterizado pelo pareamento e pela maximalidade. A congruência Delta_rel=R Delta_omega R tem domínio {x | R x pertence a D(Delta_omega)}, é fechada, positiva, autoadjunta e densamente definida.",
    "",
    "A composição S_rel^dagger S_rel foi ligada a Delta_rel com o domínio exato, e Re<x,Delta_rel x>=||S_rel x||^2 foi demonstrada nesse domínio. A auto-adjunticidade não é premissa sobre o operador relativo: decorre do lema genérico de congruência e das propriedades do operador de referência e do filtro.",
    "",
    "Esta etapa não identifica os domínios relativos com os originais, não prova comutação de R com o operador não limitado nem constrói potências imaginárias relativas. A identificação completa Connes/Araki continua aberta. Nenhuma identidade com área geométrica ou reconstrução gravitacional geral é reivindicada.",
    "",
    "A custódia inclui o manifesto e o auditor 030, a entrega anterior e sua errata nominal preservada ao lado. Nenhum desses artefatos foi alterado."
]


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation031.py'}'", '\u0060\u0060\u0060',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO031_DERIVACAO_PREVIA.md','CONTINUACAO031_PARECER.md','audit_continuation031.py'])
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
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO031_PARECER.md'),
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_031_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_031_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 031 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation031.py [--write]')


