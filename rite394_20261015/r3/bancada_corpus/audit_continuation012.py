"""Exact-byte and Lean-output audit for spontaneous continuation 012.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'ScreenAreaCalculus', 'NullScreenAlgebra', 'GeometricScreenTransport',
    'GeometricAreaHorizon', 'ScreenEntropyObstruction', 'GeometricScreenControls',
]
MANIFEST = ROOT / 'CONTINUACAO012_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_012_ESPONTANEA_area_geometrica_e_dinamica_da_entropia.md'
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


def signature_rejected_hashes(module):
    if module != 'GeometricAreaHorizon':
        return set()
    return {digest(path) for path in ROOT.glob(module + '.lean.bak_*')
            if 'first_screen_positive' in read(path)}


def runs(module):
    records = []
    bad_signature = signature_rejected_hashes(module)
    for meta in sorted(ROOT.glob(module + '.*.json')):
        data = json.loads(read(meta))
        log = ROOT / data['log']
        output = read(log)
        signature_issue = data['proof_sha256'].lower() in bad_signature
        rejected = data['exit_code'] != 0 or signature_issue or bool(re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', output))
        label = ('failed_compile' if data['exit_code'] else
                 'rejected_signature_condition' if signature_issue else 'rejected_warning')
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
    if sorted(row['declaration'].removeprefix('ChatgptAudit.') for row in axioms) != sorted(prints):
        raise RuntimeError(f'Qualified axiom names mismatch: {module}')
    paths = {source, source.with_suffix('.olean')}
    paths.update(ROOT.glob(module + '.lean.bak_*'))
    history = []
    for m, d, l, out, archive in attempts:
        paths.update([m, l])
        if archive is not None:
            if not archive.exists() or archive.read_bytes() != l.read_bytes():
                raise RuntimeError(f'Failed attempt not preserved: {l}')
            paths.add(archive)
        history.append({'metadata': str(m), 'log': str(l), 'exit_code': d['exit_code'],
                        'source_sha256': d['proof_sha256'].lower(),
                        'rejected_copy': str(archive) if archive else None,
                        'semantic_issue': ('positive screen incompatible with canonical +--- convention'
                                           if d['proof_sha256'].lower() in signature_rejected_hashes(module) else None),
                        'issues': [line for line in out.splitlines()
                                   if re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', line)]})
    return {'module': module, 'theorems': len(theorems), 'printed_definitions': len(prints)-len(theorems),
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

    for module in MODULES:
        visit(module)
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation012.py', 'revise_continuation012.py', 'verify_stage.ps1',
        'CONTINUACAO012_DERIVACAO_PREVIA.md', 'CONTINUACAO012_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO012_*.md.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 012; no managerial order 012 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['induced screen determinant and area derivative',
                 'equality of transverse and ambient expansion under explicit null-frame conditions',
                 'metric compatibility and Lie transport cancellation along a curve',
                 'geometric area adapter without an assumed area-rate field',
                 'conditional reconstruction using actual geometric Einstein tensor',
                 'one-sided entropy-area derivative constraint and frozen-state obstruction',
                 'nonzero flat geometric horizon inhabitant',
                 'signature correction validated against canonical eta4 and variable-area control'],
        'inputs_and_unpaid': ['existence of general screens and geodesic congruences',
                             'deduction of the supplied null-gradient pairing condition',
                             'surface immersion and integrated total area',
                             'microscopic region-to-algebra and entropy-to-area identification',
                             'area unit and entropy density coefficient',
                             'state evolution and heat current', 'H3',
                             'screen-only equilibrium in place of full zero covariant gradient',
                             'signature and dimension selection', 'global chart gluing',
                             'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 012 ESPONTÂNEA — densidade de área geométrica e restrição dinâmica da entropia.',
        '', 'Continuação de 011, 05/09/2026. Nenhuma ordem 012 da gerência estava no túnel ao publicar. Pronta para auditoria independente; não altera gate nem conclui gravitação quântica.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação antes do código | PAGO | Derivação inicial e adendo anterior à correção de assinatura. |',
        '| Área independente da entropia | PAGO como densidade local | A=√det(SᵀgS), definida da métrica e de duas direções transversais. |',
        '| Lei de variação geométrica | PAGO sob dados explícitos | coordinate_screen_area_derivative: A′=tr(∇V)A, via determinante, compatibilidade métrica e transporte. |',
        '| Igualdade das duas expansões | PAGO | ambient_expansion_is_screen_trace, com referencial nulo, Bk=0 e g(k,Bn)=0. |',
        '| Reconstrução com área calculada | PAGO como implicação | GeometricHorizonPencil não recebe area/area_rate; geometricHorizonToLocal os calcula e a reconstrução usa o tensor de Einstein efetivo. |',
        '| Direções não nulas | PAGO | Testemunhos exigidos apenas para v≠0; a forma quadrática na direção zero é tratada diretamente. |',
        '| Contrato habitado | PAGO no caso plano | flatGeometricHorizon, direção (1,1,0,0), tela constante e A=1 calculada; três definições de testemunhos com axiomas impressos. |',
        '| Correção de assinatura | PAGO | eta4 tem convenção +---; tela espacial h₀₀<0, det h>0. screen_area_signature_flip; controle plano final passou. |',
        '| Entropia fixa e área variável | PAGO como obstrução local | Igualdade no ponto e no ramo passado, η≠0 e A≠0 forçam θ=0 para entropia congelada. |',
        '| Variação dos pesos | PAGO como condição necessária | Σq_i(−log p_i)=ηθA(0), se a lei entropia-área vale para a perturbação normalizada. |',
        '| Existência geral e vínculo quântico | NÃO PAGO | Telas/congruências gerais, imersão e área integrada, preserves_null_pairing, região/fator, estado dinâmico, calor e H3 seguem INPUT/OPEN. |',
        '| Gravitação quântica geral | NÃO PAGO | Reconstrução condicional; assinatura, dimensão, escala e globalização permanecem abertas. |',
        '', f"{len(data['modules'])} módulos novos; {data['theorems']} teoremas; {data['printed_definitions']} definições com axiomas separadamente impressos. Contagens lidas dos fontes. As dependências finais estão contidas no trio permitido; sem sorryAx, erros ou avisos.",
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation012.py'}'",
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['\u0060\u0060\u0060', '', 'O manifesto fixa fontes, cópias binárias locais e logs. O ambiente externo Lean/mathlib é local. Conferência de hashes não substitui recompilação independente.',
             '', '## Axiomas impressos', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
             f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
             f"Inventário completo: {len(data['files'])} caminhos absolutos, tamanhos e hashes dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO012_DERIVACAO_PREVIA.md',
                   'CONTINUACAO012_PARECER.md', 'audit_continuation012.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                why = run.get('semantic_issue') or 'erro de elaboração ou aviso'
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; {why}; cópia exata do log.")
    rows += ['', 'A versão inicial que exigia Gram espacial positivo era incompatível com +---. Mesmo as compilações limpas dessa versão não são aceitas como evidência geométrica final. O auditor reconhece seus hashes a partir dos backups e arquiva os logs com o motivo de assinatura. A correção e o controle plano estão no parecer.',
             '', '## Limites e integração', '',
             'A é densidade de área associada às direções fornecidas. A imersão de uma superfície geral e a integral de área não foram construídas. O transporte e a condição preserves_null_pairing são dados explícitos; a geodesicidade produz Bk=0. O equilíbrio B=0 continua mais forte que equilíbrio apenas da tela.',
             '', 'A igualdade S=ηA, a escolha de η, o calor e o limite de Clausius não foram deduzidos do estado. Para perfil e andar fixos, a entropia é constante: a nova obstrução exige mudança do estado, corte, álgebra ou número efetivo de fatores para acompanhar expansão não nula.',
             '', 'O controle stretchedScreen tem A=(1+t)² e A′(0)=2; é uma família de paralelogramos parametrizados, não um segundo horizonte dinâmico completo. O habitante completo provado é o plano de área constante.',
             '', 'Fonte primária de referência: [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004), equações (3)–(6). A distinção entre identidade geométrica e premissa termodinâmica foi preservada.',
             '', 'Escritas somente em Chatgpt. Nenhum um.py executado, importado ou editado; nenhuma edição no kernel canônico, Atlas, memórias, selos ou gate. Nenhum dado observacional. A gerência recompila, audita e decide incorporação. O objetivo amplo permanece ativo e aberto.']
    return '\n'.join(rows) + '\n'


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_012_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_012_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 012 already occupied; refusing publication')
        preserve_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
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
            if len(re.findall(r'^theorem\s+', code, re.M)) != module['theorems']:
                raise RuntimeError('Theorem count changed')
            prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
            if sorted(prints) != sorted(r['declaration'].removeprefix('ChatgptAudit.') for r in module['axioms']):
                raise RuntimeError('Axiom coverage changed')
        if delivery_text(data) != read(DELIVERY):
            raise RuntimeError('Delivery does not match the pinned inventory')
        print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
              f"{data['theorems']} theorems; {data['printed_definitions']} printed definitions; delivery verified")
    else:
        raise SystemExit('Usage: audit_continuation012.py [--write]')



