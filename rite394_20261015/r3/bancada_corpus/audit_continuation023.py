"""Exact-byte and Lean-output audit for spontaneous continuation 023.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['DirectionalUnitaryFamily', 'CoherentScalarStress', 'CovectorStressCalculus', 'ScalarStressConservation', 'CoherentHeatMatching', 'CoherentEinsteinBridge', 'CoherentMatterControls']
MANIFEST = ROOT / 'CONTINUACAO023_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_023_ESPONTANEA_covetor_materia_conservacao.md'
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

    visit('CoherentMatterControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation023.py', 'revise_continuation023.py', 'verify_stage.ps1',
        'CONTINUACAO023_DERIVACAO_PREVIA.md', 'CONTINUACAO023_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO023_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation023.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation023.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'spontaneous continuation 023; no managerial order 023 issued at publication time', 'reuse': ['explicit finite unitary marginal from 022', 'actual geometric screen, area and temporal heat integral from 019-020', 'relative entropy and microscopic error definitions from 021', 'general covariant tensor reconstruction from 008-020'], 'paid': ['one common covector produces directional Hamiltonians and compatible unitary compositions at a fixed point', 'quadratic response is a symmetric rank-at-most-one covariant tensor with explicit change-of-basis identity', 'constructed scalar-type stress tensor and null contraction matched to the unitary response', 'actual covariant derivative of the outer product and inverse-metric squared norm', 'general stress divergence including antisymmetric covector derivative', 'closed covector reduces stress divergence to coupling times covector divergence times covector', 'pointwise conservation equivalent to wave condition away from zero coupling and zero covector', 'gradient covectors smooth and closed for smooth potentials', 'heat-modular error divided by t squared tends to zero for the constructed stress on actual null screens', 'area-error coefficient and equivalence of area matching to null Ricci balance', 'uniqueness of a symmetric conserved source with these null contractions up to a constant metric term on an open preconnected domain', 'Einstein implication with heat matching and stress conservation proved, area matching and covector wave equation assumed', 'flat constant nonzero conserved stress matches heat but fails area matching', 'flat gradient covector from x0 squared over two is directionally coherent but does not conserve stress'], 'inputs_and_unpaid': ['selection of fixed Hermitian axis, positive reference amplitudes and smooth covector field', 'normalization coupling equals minus unit-frequency response divided by pi is chosen to realize the heat identification', 'wave equation for the covector and closedness, or smooth scalar potential plus wave equation', 'entropy-area error o(t squared), proved equivalent to null Ricci balance but not derived microscopically', 'four dimensions, Lorentzian metric from a smooth invertible solder, common affine/unitary parameter and nonzero entropy density', 'this rank-at-most-one family is not general matter and is not identified with the canonical um.py dynamics', 'no space-time translation action or coherence among regions/tower floors is obtained from direction addition at one point', 'type-III limit, global gluing, physical units, temperature and Newton coefficient', 'finite periodic unitary evolution does not supply the hyperbolic face or evade the Borchers obstruction', 'the broad quantum gravity objective remains unresolved'], 'criteria': [['Derivação anterior ao código', 'PAGO', 'CONTINUACAO023_DERIVACAO_PREVIA.md, com antecedentes e controles registrados.'], ['Coerência em cada ponto', 'PAGO', 'directional_hamiltonian_add, directional_flow_add, directional_flow_unitary; um único covetor, eixo e referência.'], ['Resposta tensorial e mudança de base', 'PAGO', 'response_tensor_quad, response_tensor_symmetric, covector_read_change_basis e outer_tensor_change_basis.'], ['Tensor candidato e sinais', 'PAGO sob escolha explícita', 'covector_stress_null, response_equals_negative_null_stress; acoplamento positivo no controle de resposta negativa.'], ['Divergência efetivamente calculada', 'PAGO', 'covector_stress_divergence_point inclui a parte antissimétrica; covector_stress_divergence_closed a elimina sob fechamento e torção zero.'], ['Conservação e equação de onda', 'PAGO CONDICIONAL', 'covector_stress_conserved_on; equivalência pontual para coupling≠0 e w(x)≠0; a equação de onda segue INPUT.'], ['Caso de potencial', 'PAGO', 'potential_covector_smooth e potential_covector_closed; growing_potential_covector realiza o exemplo quadrático.'], ['Calor–modular efetivo', 'PAGO para o tensor normalizado escolhido', 'coherent_heat_matching e coherentScreenMatching: o erro do calor construído de 020 tende a zero após divisão por t².'], ['Entropia–área', 'EQUIVALÊNCIA PAGA; ORIGEM NÃO PAGA', 'coherent_area_matching_iff_ricci: erro pequeno equivale a η Ric(d,d)=2π T(d,d).'], ['Unicidade do tensor', 'PAGO CONDICIONAL', 'frame_covector_source_unique: mesma resposta nula e conservação implicam diferença constante vezes g.'], ['Reconstrução gravitacional', 'PAGO CONDICIONAL', 'einstein_from_coherent_area_matching: conservação calculada sob onda; hipótese de área permanece explícita.'], ['Controle plano conservado', 'PAGO', 'coherent_flat_matter_matrix e coherent_flat_matter_conserved; calor corresponde, mas coherent_flat_area_not_matching para toda η.'], ['Controle de falha da conservação', 'PAGO', 'w=d(x0²/2), div(w)=1, div(T)=κ x0 e0; growing_time_not_conserved em x=e0.'], ['Origem canônica e gravidade quântica', 'NÃO PAGO', 'Campo, onda, normalização física, área e conexão ao acervo permanecem INPUT/OPEN; gate intocado.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'CoherentMatterControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = ['[REAL / INPUT / OPEN] ENTREGA 023 ESPONTÂNEA — família unitária direcional, tensor candidato e conservação calculada.', '', '06/09/2026. Continuação da entrega 022 e do objetivo amplo associado à ordem 007. A ordem 006 já foi aprovada pela gerência, segundo a ordem 007. Esta entrega não é uma nova ordem gerencial.', '', '## Resultado e alcance', '', 'Com eixo M=[[a,b],[b,−a]] e referência u,v fixos, usar um único campo de covetores w: ell_x(d)=w_x(d), H_x(d)=ell_x(d)M. A composição U_x(d+e,t)=U_x(d,t)U_x(e,t) é provada no mesmo ponto. Direções no núcleo de w produzem fluxo trivial; isso não constrói translações do espaço-tempo.', '', 'A resposta da marginal efetiva de 022 é L_x(d)=L0 ell_x(d)². A matriz L0 w⊗w transforma-se por congruência quando o covetor muda de base. Escolhe-se κ=−L0/π e constrói-se T=κ[w⊗w−g q/2], q=gInv(w,w). Em direções nulas L=−πT(d,d), e o erro calor–modular/t² tende a zero para o calor temporal efetivo de 020. Essa escolha de normalização realiza a correspondência; não deriva as unidades ou a origem física de T.', '', 'Definindo W_ij=∇_i w_j, a prova calcula ∇^iT_ij=κ[(∇^i w_i)w_j+gInv^{ik}w_k(W_ij−W_ji)]. Sob covetor fechado e conexão sem torção, a segunda parcela desaparece. Com κ≠0 e w(x)≠0, conservação no ponto equivale a ∇^i w_i=0. Para w=dφ suave, o fechamento é demonstrado; a equação de onda continua uma hipótese dinâmica.', '', 'O tensor escalar e a dependência da conservação nas equações de movimento são [KNOWN] na literatura; o resultado desta bancada é sua verificação formal nas definições geométricas existentes e sua ligação à resposta escolhida. Referência primária: [Carroll, capítulo 1, equações (1.112)–(1.113)](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll1.html).', '', 'Qualquer tensor simétrico conservado com as mesmas contrações nulas difere do candidato por uma constante vezes a métrica, em domínio aberto preconexo, sob os antecedentes declarados. A conclusão depende da conservação de ambos.', '', 'O coeficiente do erro entropia–área é L_x(d)+η Ric_x(d,d)/2. Sua anulação equivale ao balanço nulo η Ric=2πT. Sob esse erro pequeno e a condição de onda, obtém-se G+Λg=(2π/η)T. A equivalência registra exatamente a dívida restante: a origem da relação de área não foi demonstrada pela renomeação do balanço de Einstein.', '', '## Controles', '', 'No plano, com w=e0 constante e o eixo de resposta negativa de 022, κ>0 e T=(κ/2)diag(1,1,1,1). O tensor é não nulo e conservado. A correspondência calor–modular é satisfeita, mas a correspondência entropia–área falha para toda η. Assim, conservação e correspondência de calor não implicam a hipótese restante.', '', 'No plano, w=x0 e0=d(x0²/2) é suave e fechado. A divergência do covetor vale 1, e ∇T=κ x0 e0, não nula em x=e0. A família unitária continua disponível para esse covetor: unitariedade e coerência direcional não forçam a condição de onda.', '', 'O caso w=0 dá tensor zero (covector_stress_zero) e frequência zero; directional_kernel_trivial_flow e a fórmula da resposta mantêm esse limite degenerado.', '', '## Critérios', '', '| Critério | Estado | Evidência |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += [
        '',
        f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definição com axiomas impressos separadamente. Contagens lidas dos fontes; incluem lemas auxiliares e controles.",
        'Compilações finais fixadas: exit 0, fonte estável, zero erros, avisos ou sorryAx. Axiomas: apenas propext, Classical.choice, Quot.sound. Auditoria independente da gerência pendente.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation023.py'}'",
        '\u0060\u0060\u0060', '',
        'Esse comando só lê: confere os bytes, metadados, logs e axiomas registrados. Recompilação independente deve ocorrer em cópia. Ordem dos novos módulos:',
    ]
    rows.extend('- '+str(ROOT / (module+'.lean')) for module in MODULES)
    rows += [
        '', 'O manifesto fixa a árvore de fontes local, sua ordem e os oleans copiados. Lean/mathlib externos são resolvidos pelo wrapper: não é um pacote integral portátil.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO023_DERIVACAO_PREVIA.md',
        'CONTINUACAO023_PARECER.md', 'audit_continuation023.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += [
        '', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups dos bytes. Somente as compilações finais limpas sustentam esta entrega.',
        '', '## Limites', '',
        'A seleção de w, do eixo e da referência é INPUT. O candidato tem resposta de posto no máximo um. Não cobre toda matéria; soma de campos, interações e extensões não comutantes não foram construídas.',
        'A equação de onda, normalização física, parâmetro comum afim/unitário e origem microscópica da relação entropia–área continuam INPUT/OPEN.',
        'A evolução periódica finita não substitui a face hiperbólica. Não há identificação com a dinâmica canônica do um.py, coerência entre regiões/andares, limite tipo III, origem modular da dimensão/solda/assinatura ou globalização.',
        'Nenhum um.py executado, importado ou editado. Escritas somente em Chatgpt. Originais, entregas anteriores, kernel canônico, Atlas, memórias, selos e gate intocados. Custódia 022 reconferida em leitura.',
        'O objetivo amplo permanece ativo e não alcançado. A gerência deve auditar antes de incorporar. Nenhum juízo de confirmação física foi produzido.',
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO023_PARECER.md')+'.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_023_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_023_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 023 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation023.py [--write]')




