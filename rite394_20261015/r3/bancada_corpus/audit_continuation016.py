"""Exact-byte and Lean-output audit for spontaneous continuation 016.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'DifferentialFlowExistence', 'VariationalFlow', 'FlowLinearizationError',
    'FlowDifferentiability', 'GeodesicInitialRegularity', 'FlowDifferentiabilityControls',
]
MANIFEST = ROOT / 'CONTINUACAO016_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_016_ESPONTANEA_diferencial_do_fluxo_e_regularidade_c1.md'
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

    visit('FlowDifferentiabilityControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation016.py', 'revise_continuation016.py', 'verify_stage.ps1',
        'CONTINUACAO016_DERIVACAO_PREVIA.md', 'CONTINUACAO016_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO016_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation016.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation016.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 016; no managerial order 016 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['Banach generalization of the Picard/rectangle argument from 015',
                  'null conservation from the general LocalPhaseFlow lemmas of 015',
                  'flat flow formula from 015, differentiated independently and compared to J',
                  'conformal curved background and initial acceleration from 014-015'],
        'integrated_root': 'FlowDifferentiabilityControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['uniform Lipschitz local flow on a common data-time rectangle',
                 'construction of the joint solution and variational operator',
                 'actual differential equation for the linearization error',
                 'uniform Taylor estimate derived from smoothness using compact time',
                 'Gronwall estimate and little-o identification of the initial derivative',
                 'positive and negative times',
                 'strict joint derivative and joint C1 regularity',
                 'C1 local metric and Levi-Civita flows with initial nullity preserved',
                 'linear Taylor remainder zero and zero-field variation equal to identity',
                 'flat phase derivative block (hx + t hv, hv)',
                 'curved C1 null flow control'],
        'inputs_and_unpaid': ['smooth field on an open domain; Banach completeness for construction',
                             'smooth invertible solder and fixed Lorentzian dimension/signature',
                             'joint C-infinity regularity',
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
        '[REAL / INPUT / OPEN] ENTREGA 016 ESPONTÂNEA — diferencial efetivo do fluxo e regularidade conjunta C1.',
        '', '06/09/2026. Continuação de 015. Auditoria independente pendente. Nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO016_DERIVACAO_PREVIA.md; adendo posterior identificado, versão anterior preservada em backup de bytes. |',
        '| Existência com Lipschitz nos dados iniciais | PAGO | lipschitzLocalFlow; bola e intervalo comuns no aberto prescrito. |',
        '| Operador variacional | PAGO | variationalLocalFlow; J(0)=I e J′=Df(Φ)∘J por HasDerivAt. |',
        '| Equação do erro de linearização | PAGO | flow_remainder_derivative, com resto de Taylor explícito. |',
        '| Taylor uniforme deduzido | PAGO | flow_taylor_uniform usa suavidade e compacidade do intervalo temporal; não acrescenta uma hipótese de Taylor ao resultado final. |',
        '| Derivada efetiva nos dados | PAGO | flow_initial_hasFDerivAt em ambos os sinais do tempo; prova por Grönwall e little-o. |',
        '| Derivada conjunta e C1 | PAGO | flow_joint_hasStrictFDerivAt e flow_joint_c1; DΦ[h,τ]=Jh+τf(Φ). |',
        '| Fluxo geodésico C1 e nulidade | PAGO sob INPUT | local_c1_metric_null_geodesics e local_c1_levi_civita_null_geodesics; solda/conexão suave recebida, nulidade inicial explícita. |',
        '| Controles | PAGO | Campo linear com resto zero, campo nulo com J=I, bloco plano J(hx,hv)=(hx+t hv,hv), fluxo curvo C1 inicialmente nulo. |',
        '| C∞ nos dados e congruência espacial | NÃO PAGO | Regularidade superior, seção transversal, inversão local da posição e primeiro jato de equilíbrio ainda faltam. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definições com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'As declarações reutilizam resultados de Picard/mathlib e conservação de 015; a contagem não representa descobertas matemáticas novas. A contribuição formal está na identificação do diferencial do fluxo e sua continuidade conjunta.',
        'Os logs finais da fonte fixada não têm erros, avisos ou sorryAx. Axiomas impressos: apenas propext, Classical.choice e Quot.sound.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation016.py'}'",
        '\u0060\u0060\u0060', '',
        'Esse comando é somente leitura. Confere os bytes e as evidências do compilador; não substitui a recompilação independente da gerência. A ordem de compilação dos módulos novos é:',
    ]
    for module in MODULES:
        rows.append('- ' + module + '.lean')
    rows += ['', 'FlowDifferentiabilityControls importa toda a árvore 016 e os controles 015. O manifesto registra também a ordem completa dos fontes locais. Recompilar em cópia independente, mantendo imutáveis fontes, oleans e logs entregues. O wrapper verify_stage.ps1 e os metadados documentam a configuração Lean 4.31.0/mathlib usada.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO016_DERIVACAO_PREVIA.md',
                   'CONTINUACAO016_PARECER.md', 'audit_continuation016.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; erro de elaboração ou aviso; cópia exata do log.")
    rows += ['', 'Os backups preservam todas as versões efetivamente compiladas. Falhas intermediárias de tipos, composição e continuidade foram corrigidas; avisos de argumentos redundantes foram removidos. Só as compilações finais limpas sustentam a entrega.',
             '', '## Parede exata', '',
             'O fluxo é C1 conjunto. SmoothVectorOn de 014 requer C∞: a indução de regularidade superior ainda não foi formalizada. Também faltam a seleção transversal de dados e a inversa local da projeção para a posição. A família completa no espaço de fases não é uma congruência espacial e não é inteiramente nula; a preservação da nulidade recebe o dado inicial nulo.',
             'A construção usa uma nova escolha de Picard no sistema variacional. Não foi provada igualdade literal com a escolha existencial da entrega 015; seus teoremas gerais de conservação se aplicam ao novo LocalPhaseFlow.',
             '', 'A relação microscópica entropia-área e Clausius/H3 permanecem abertas. [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004) assume a proporcionalidade entropia-área e a relação de Clausius para sua dedução termodinâmica; citar essa dedução não paga as hipóteses.',
             '', 'Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. As custódias 014 e 015 foram reconferidas sem alteração. O objetivo amplo de gravidade quântica permanece ativo e OPEN.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO016_PARECER.md') + '.',
             '', 'Ordens de entrada encontradas no momento do inventário:']
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_016_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_016_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 016 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation016.py [--write]')

