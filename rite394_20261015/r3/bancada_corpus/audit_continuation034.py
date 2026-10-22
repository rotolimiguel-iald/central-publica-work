"""Exact-byte and Lean-output audit for spontaneous continuation 034.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['CentralizerPhaseOrbit', 'SitePhaseCovariance', 'AngularScreenMetric', 'AngularAreaObservability']
MANIFEST = ROOT / 'CONTINUACAO034_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_034_ESPONTANEA_area_angular_e_observabilidade.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

NARRATIVE = {'status': 'REAL: exact-byte custody and clean Lean evidence; independent managerial audit pending', 'kind': 'Spontaneous continuation 034 of order 007; two-site angular area in the actual tower and the operational pullback obstruction', 'reuse': ['Site projections and norm-closed state centralizer proved in 030–033', 'Actual tower product state, tail conditional expectation and faithful representation', 'Existing real two-dimensional screenArea=sqrt(det), reused without asserting a gravitational screen'], 'paid': ['State-product factorization for arbitrary distinct sites and exact centered-vector covariance', 'Differentiable two-phase unitary orbit inside the state centralizer, with actual coordinate derivatives and preservation of the reference state on M', 'Horizontal projection of actual derivatives at the origin equals the centered phase vectors used by the real Gram matrix', 'Two distinct sites have positive Gram determinant and angular area; repeated site has zero determinant and area', 'For the reference profile, distinct sites 0,1 give angular area density 2/9 while repeated site 0,0 gives zero', 'The vector state of the two-phase orbit restricted to M is identically the original reference state', 'Every finite family of fixed observables in M has constant real expectation values and zero coordinate derivatives on this orbit', 'The actual real reading Jacobian J is zero; every finite matrix pullback J^T G J and its area are zero', 'No such observable pullback agrees at the origin with the positive angular Gram or its area for distinct sites', 'The phase evolution preserves Hilbert distances; this is an exact control relevant to claims of attracting stabilization'], 'inputs_and_unpaid': ['The construction uses the actual tower and site projections for any admissible SiteProfile. It does not substitute an unrelated finite-dimensional toy.', 'The angular Gram is proved to represent horizontal tangents of the differentiable orbit at the origin. Global transport of this metric over the entire orbit is not a new theorem here.', 'screenArea is the previously defined sqrt determinant on real 2x2 matrices. Reusing that function does not construct a Lorentzian screen, spacetime surface or identification with its area.', 'The value 2/9 is an area density in the specified angular coordinates. It is not a physical area with length units, an integrated surface area or an intrinsic comparison under arbitrary coordinate rescaling.', 'The operational obstruction concerns any finite family of fixed observables in M and their real expectation derivatives along this particular centralizing orbit. Full complex restricted-state constancy is separately proved.', 'G is an arbitrary finite real matrix at the evaluation point; symmetry, positivity and constancy in the parameters are unnecessary for the zero result.', 'The result does not exclude parameter-dependent observables such as omega(F_s), observables outside M, interferometric reference systems or geometries of purifications.', 'No claim of impossibility of quantum geometry or absence of physical area is made. The obstruction identifies why centralizing phase directions alone cannot generate a nonzero metric through these state readings.', 'Microscopic noncentralizing deformations with two observable independent directions, a region-algebra map, length scale, Lorentzian signature, area matching and gravitational dynamics remain obligations.', 'The proposed two-site Pauli-X/Pauli-Y follow-up is an analytic candidate in the report, not an executed or compiled claim of this stage.', 'Originals, canonical kernel, um.py, Atlas, memories, previous seals, gates and deliveries remain unchanged. Managerial recompilation and incorporation remain pending.'], 'criteria': [['Derivação anterior ao código', 'PAGO', 'CONTINUACAO034_DERIVACAO_PREVIA.md; refinement of operational Jacobian precedes integration module.'], ['Covariância real da torre', 'PAGO', 'site_zero_product_state; centered_site_inner_self/distinct; centered_site_variance_pos.'], ['Órbita e derivadas efetivas', 'PAGO', 'two_phase_vector_differentiable; two_phase_first_derivative/second_derivative; first_horizontal_tangent/second_horizontal_tangent.'], ['Área angular não degenerada', 'PAGO', 'angular_screen_determinant_positive e angular_screen_area_positive.'], ['Controle de sítio repetido', 'PAGO', 'angular_screen_determinant_repeated e angular_screen_area_repeated.'], ['Controle exato da referência', 'PAGO', 'reference_phase_area_split; área angular 2/9 e área repetida/observável zero.'], ['Estado restrito aos observáveis', 'PAGO', 'phase_vector_state_form e phase_restricted_state_eq no subtipo M.'], ['Derivadas das leituras e jacobiano', 'PAGO', 'phase_reading_first_derivative/second_derivative; observable_phase_jacobian_zero.'], ['Obstrução ao pullback dessas leituras', 'PAGO NO ESCOPO', 'observable_phase_gram_zero, observable_phase_area_zero, observable_phase_gram_not_angular, observable_phase_area_not_angular.'], ['Lei de estabilização', 'NÃO PAGO', 'two_phase_distance_preserved é controle; nenhuma atração dinâmica foi construída.'], ['Área gravitacional geral', 'NÃO PAGO', 'Não há identificação de superfície física, escala, região-algebra ou dinâmica a partir dessas fases.']], 'dependency_limit': 'The local source closure and copied TGL/TGLExt oleans are pinned; external Lean 4.31.0/mathlib is resolved read-only by verify_stage.ps1. This is not a portable full bundle or managerial recompilation.'}


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
    if namespace != 'ChatgptAudit.Angular034':
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

    visit('AngularAreaObservability')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation034.py', 'revise_continuation034.py', 'verify_stage.ps1',
        'CONTINUACAO034_DERIVACAO_PREVIA.md', 'CONTINUACAO034_PARECER.md',
        'CONTINUACAO033_MANIFESTO.json', 'audit_continuation033.py',
        'TUNEL/DO_CHATGPT/ENTREGA_033_ESPONTANEA_densidade_logaritmo_e_cociclo.md',
        'CONTINUACAO032_MANIFESTO.json', 'audit_continuation032.py',
        'TUNEL/DO_CHATGPT/ENTREGA_032_ESPONTANEA_comutacao_modular_e_dominio.md',
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
    paths.update(ROOT.glob('CONTINUACAO034_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation034.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation034.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **NARRATIVE,
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'AngularAreaObservability',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = ['[REAL / DERIVED / INPUT / OPEN] ENTREGA 034 ESPONTÂNEA — área angular de dois sítios e teste operacional.', '', '06/09/2026. Continuação da ordem007 e da hipótese angular do operador. Auditoria e incorporação da gerência pendentes.', '', 'Foram construídas duas direções angulares na própria torre, com U(s,t)=exp(is e_n)exp(it e_m). A família é diferenciável, unitária e preserva o estado de referência em M. As derivadas horizontais efetivas na origem foram identificadas com i(e_n-p_n I)Omega e i(e_m-p_m I)Omega.', '', 'Para sítios distintos, o Gram real é diag(p_n(1-p_n),p_m(1-p_m)), com determinante e densidade de área positivos. Para sítio repetido, a área é zero. No perfil1/3, os controles são 2/9 e zero.', '', 'O vetor da órbita define o mesmo estado quando restrito a M. Toda coleção finita de observáveis fixos em M tem leituras constantes e jacobiano real J=0. Logo qualquer métrica induzida J^T G J é zero e não iguala o Gram angular positivo na origem.', '', 'Esse resultado localiza a diferença entre geometria de purificações e geometria obtida dessas leituras do estado. Não exclui observáveis que também variem, referências interferométricas ou observáveis fora de M. A densidade 2/9 não é uma área física dimensional.', '', 'A próxima obrigação é construir deformações que alterem observáveis com duas direções independentes, e ligar sua geometria a uma superfície/região e escala. O parecer inclui uma candidata Pauli-X/Pauli-Y com estatuto analítico, ainda não formalizada nesta etapa.', '', 'Originais e entregas anteriores preservados. Esta entrega não move o gate nem encerra a reconstrução gravitacional geral.']


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation034.py'}'", '\u0060\u0060\u0060',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO034_DERIVACAO_PREVIA.md','CONTINUACAO034_PARECER.md','audit_continuation034.py'])
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
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO034_PARECER.md'),
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_034_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_034_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 034 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation034.py [--write]')



