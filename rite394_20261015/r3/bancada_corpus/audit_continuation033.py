"""Exact-byte and Lean-output audit for spontaneous continuation 033.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['CentralizerDensity', 'LikelihoodDensityLog', 'DensityStateUniqueness']
MANIFEST = ROOT / 'CONTINUACAO033_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_033_ESPONTANEA_densidade_logaritmo_e_cociclo.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

NARRATIVE = {'status': 'REAL: exact-byte custody and clean Lean evidence; KNOWN/DERIVED: Pedersen-Takesaki specialization in the report; independent managerial audit pending', 'kind': 'Spontaneous continuation 033 of order 007; bounded centralizing Radon-Nikodym density, logarithm, uniqueness and angular interpretation', 'reuse': ['Actual summable likelihood family from 028–030, with L self-adjoint, R=exp(L/2), normalized faithful prepared vector state', 'Relative Tomita closure, adjoint and modular operator from 031, and exact-domain identity Delta_rel=exp(L)Delta from 032', 'Existing norm closure of the state centralizer and local likelihood term membership, plus mathlib continuous functional calculus'], 'paid': ['The trace-identity centralizer is a norm-closed complex subalgebra; local terms, prefixes, L, R, exp(L) and u_s belong to it', 'H=exp(L)=R^2 is a positive self-adjoint invertible factor element with omega(H)=1', 'The genuine continuous-functional-calculus logarithms satisfy log(H)=L and log(R)=L/2; L is the unique self-adjoint logarithm of H', 'The bounded expression exp(is log(H)) equals the constructed likelihood cocycle and is unitary', 'The prepared state is omega(H A)=omega(A H) for every A in the factor; the left density is unique among all factor elements', 'The cocycle conjugation preserves the reference state on the entire factor', 'The angular quadratic observable is even under reversal of modular time'], 'inputs_and_unpaid': ['The concrete family is the specified summable commuting product perturbation with reference weights (1/3,2/3), amplitudes 0<=b_n<=1/12 and h(t)=t^2/(1+t^2).', 'The generic density uniqueness theorem applies to the actual tower factor and its faithful vector state, with H,K in the factor; it does not assume positivity of competing densities.', 'The Connes identification is established analytically by explicitly applying Hiai Theorem 9.4(2) to the proved bounded centralizing density. This is KNOWN/DERIVED, not a newly compiled general Pedersen-Takesaki theorem.', 'Full normality of vector states and the standard identification of the trace-identity centralizer with the modular centralizer are literature bridges. Local sequential WOT continuity is not relabeled as full normality.', 'boundedDensityPower is the bounded expression exp(is CFC.log(H)). Generic unbounded relative imaginary powers, their joint spectral calculus and full Araki entropy are not formalized here.', 'Only reference-state invariance is compiled in this stage; prepared-state invariance is discussed as an analytic consequence using commutation with R.', 'F_s is a positive quadratic variation of phase, even under time reversal. The pure phase has constant squared modulus; root modulus, squared modulus and projective variance are distinct readings.', 'Physical area requires an independently specified surface/region, two independent geometric directions, scale and a proved identification. A single fixed generator can induce only rank-one projective geometry. These tests are analytic, not new Lean theorems.', 'Periodic return alone supplies no attracting dynamics. Identification of L with a physical well/tail and of its angular reading with light bending or a graviton remains open.', 'Originals, canonical kernel, um.py, Atlas, memories, prior seals, gates and deliveries are unchanged by this work. Managerial recompilation and incorporation remain pending.'], 'criteria': [['Centralizador sem definir o fluxo', 'PAGO', 'omegaCentralizerAlgebra e lemas de fechamento, soma, produto e exponencial.'], ['Inclusões globais L/R/H/u', 'PAGO', 'likelihood_generator_mem_centralizer, likelihood_filter_mem_centralizer, likelihood_density_mem_centralizer, likelihood_cocycle_mem_centralizer.'], ['Densidade positiva e normalizada', 'PAGO', 'likelihood_density_positive, selfadjoint, invertible, mem_factor e normalized.'], ['Logaritmo genuíno e unicidade', 'PAGO', 'likelihood_density_log, likelihood_filter_log, likelihood_density_log_unique; CFC.log_exp.'], ['Potência imaginária limitada', 'PAGO', 'bounded_density_power_eq_cocycle e bounded_density_power_unitary.'], ['Estado e unicidade da densidade', 'PAGO', 'likelihood_density_state_left/right, factor_density_state_unique, likelihood_density_state_unique.'], ['Controle da leitura angular', 'PAGO NO ESCOPO', 'phase_quadratic_time_even; reference_state_cocycle_invariant. Raiz, projeção e área discutidas analiticamente.'], ['Cociclo canônico da família', 'PAGO [KNOWN/DERIVED]', 'Especialização explícita de Hiai 9.4(2), com pontes externas identificadas no parecer.'], ['Pedersen–Takesaki geral no Lean', 'NÃO PAGO', 'Literatura não é apresentada como novo teorema do kernel.'], ['Área, retorno estabilizante e gravidade geral', 'NÃO PAGO', 'Faltam mapa geométrico/escala, direções independentes e dinâmica física demonstrada.']], 'dependency_limit': 'The local source closure and copied TGL/TGLExt oleans are pinned; external Lean 4.31.0/mathlib is read-only via verify_stage.ps1. This is not a portable full bundle or independent recompilation.'}


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
    if namespace != 'ChatgptAudit.Density033':
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

    visit('DensityStateUniqueness')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation033.py', 'revise_continuation033.py', 'verify_stage.ps1',
        'CONTINUACAO033_DERIVACAO_PREVIA.md', 'CONTINUACAO033_PARECER.md',
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
    paths.update(ROOT.glob('CONTINUACAO033_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation033.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation033.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **NARRATIVE,
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'DensityStateUniqueness',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = ['[REAL / KNOWN / DERIVED / INPUT / OPEN] ENTREGA 033 ESPONTÂNEA — densidade centralizante, logaritmo e leitura angular.', '', '06/09/2026. Continuação da ordem 007 e da pergunta do operador sobre a inscrição angular quadrática.', '', 'Foi construída a subálgebra norm-fechada definida por omega(AB)=omega(BA). O gerador L e as exponenciais R, H e u_s pertencem a ela por lemas efetivos.', '', 'H=exp(L)=R² é positivo, autoadjunto, invertível e normalizado. O cálculo funcional contínuo demonstra log(H)=L, com unicidade entre logaritmos autoadjuntos. A potência imaginária limitada exp(is log(H)) coincide com u_s.', '', 'Para todo A no fator, psi(A)=omega(H A)=omega(A H); nenhuma outra densidade do fator representa esse mesmo funcional pela multiplicação à esquerda.', '', '[KNOWN/DERIVED] As hipóteses da especialização de Pedersen–Takesaki estão identificadas: [Dpsi:Domega]_s=u_s. O parecer explicita as pontes de literatura; o teorema geral não foi formalizado no kernel.', '', 'A resposta quadrática F_s é par no tempo modular. A conjugação por u_s preserva o estado de referência na álgebra M. Assim, movimento de vetor/purificação, variação de fase e mudança de estado observável precisam ser distinguidos na ponte geométrica.', '', 'A interpretação de L como poço/cauda e da resposta angular como área física/retorno estabilizante permanece uma hipótese a desenvolver. A análise construtiva e seus testes estão no parecer. Nenhuma escolha entre módulo raiz e quadrado é assumida.', '', 'Auditoria e incorporação da gerência pendentes; esta entrega não move o gate.']


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation033.py'}'", '\u0060\u0060\u0060',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO033_DERIVACAO_PREVIA.md','CONTINUACAO033_PARECER.md','audit_continuation033.py'])
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
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO033_PARECER.md'),
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_033_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_033_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 033 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation033.py [--write]')



