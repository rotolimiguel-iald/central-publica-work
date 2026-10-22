"""Exact-byte and Lean-output audit for spontaneous continuation 014.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'Screen013NullFrame', 'Screen013Constructed', 'Screen013Controls',
    'ScreenImportIntegration', 'ScreenTransportODE', 'ScreenPairTransport',
    'ScreenFrameCompletion', 'TransportedScreenExistence', 'TransportedScreenControls',
]
MANIFEST = ROOT / 'CONTINUACAO014_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_014_ESPONTANEA_transporte_local_da_tela_e_controle_curvo.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
COPIES = {
    'NullFrameConstruction': 'Screen013NullFrame',
    'ConstructedScreenAtPoint': 'Screen013Constructed',
    'NullScreenConstructionControls': 'Screen013Controls',
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


def inspect_copies():
    records = []
    for original, copied in COPIES.items():
        source = ROOT / (original + '.lean')
        target = ROOT / (copied + '.lean')
        expected = source.read_bytes().decode('utf-8')
        expected = expected.replace('namespace ChatgptAudit\n', 'namespace ChatgptAudit.Screen013\n')
        expected = expected.replace('end ChatgptAudit\n', 'end ChatgptAudit.Screen013\n')
        for before, after in COPIES.items():
            expected = expected.replace('import ' + before + '\n', 'import ' + after + '\n')
        if target.read_bytes() != expected.encode('utf-8'):
            raise RuntimeError(f'Non-mechanical change in corrected copy: {target}')
        records.append({'original': str(source), 'copy': str(target),
                        'original_sha256': digest(source), 'copy_sha256': digest(target),
                        'changes': 'namespace/end namespace and local module import names only'})
    return records


def inventory():
    copies = inspect_copies()
    records, paths = [], set()
    paths.update(ROOT / (name + '.lean') for name in COPIES)
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

    visit('TransportedScreenControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation014.py', 'revise_continuation014.py', 'verify_stage.ps1',
        'CONTINUACAO014_DERIVACAO_PREVIA.md', 'CONTINUACAO014_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO014_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation014.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation014.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 014; no managerial order 014 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'mechanical_copies': copies,
        'copied_theorems': sum(row['theorems'] for row in records if row['module'] in COPIES.values()),
        'copied_printed_definitions': sum(row['printed_definitions'] for row in records if row['module'] in COPIES.values()),
        'integration_theorems': next(row['theorems'] for row in records if row['module']=='ScreenImportIntegration'),
        'new_geometric_theorems': sum(row['theorems'] for row in records if row['module'] not in COPIES.values() and row['module']!='ScreenImportIntegration'),
        'new_printed_definitions': sum(row['printed_definitions'] for row in records if row['module'] not in COPIES.values()),
        'integrated_root': 'TransportedScreenControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['mechanical namespace repair of the three copied 013 modules',
                 'joint import of corrected 013 construction and 012 controls',
                 'C1 coupled frame vector field and actual local ODE existence',
                 'preservation of the null-vector pairings along transported columns',
                 'open-neighborhood negative screen Gram with positive determinant',
                 'algebraic completion of the auxiliary null vector without changing the screen',
                 'local inhabitant of GeometricScreenAlong for a supplied smooth null geodesic field',
                 'actual area derivative near the past and at the initial parameter',
                 'constant flat screen recovered from zero generator',
                 'curved nonconstant screen with initial area 1 and derivative 2'],
        'inputs_and_unpaid': ['smooth invertible solder and fixed Lorentzian dimension/signature',
                             'existence of general smooth null geodesic congruences',
                             'surface immersion, transverse parameter dependence and integrated area',
                             'microscopic region-to-algebra and entropy-to-area identification',
                             'area unit and entropy density coefficient',
                             'state evolution and heat current', 'Clausius/H3',
                             'screen-only equilibrium in place of full zero covariant gradient',
                             'global chart gluing', 'modular-geometric bridge', 'broad quantum gravity objective'],
        'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. '
                            'External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or independent recompilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 014 ESPONTÂNEA — construção local da tela transportada e controle curvo.',
        '', '06/09/2026. Continuação de 013. Ordens gerenciais 001–007 presentes no túnel; auditoria independente pendente. Nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO014_DERIVACAO_PREVIA.md e adendo do controle curvo anterior à sua implementação. |',
        '| Integração 012/013 | PAGO nas cópias | Três cópias mecânicas com namespace Screen013; previous_and_constructed_frames_coexist e compilação conjunta do módulo final. |',
        '| Existência local de curva e matriz transportada | PAGO | localFrameFlow aplica a existência de ODE da mathlib ao campo (V,KF), após provar C¹. |',
        '| Preservação de g(V,W) e g(V,S) | PAGO | Derivadas efetivas e constância no intervalo aberto da solução. |',
        '| Certificado nulo com tela variável | PAGO | completedNullScreen corrige somente o vetor auxiliar; mantém S e prova o Gram e a inversa. |',
        '| Habitante de GeometricScreenAlong | PAGO sob INPUT | local_levi_civita_transported_screen constrói curva e tela a partir de solda e campo nulo geodésico suave. |',
        '| Lei de área | PAGO | A=sqrt(det(SᵀgS)); A′=θA perto de zero pelo lado passado; derivada efetiva também em zero. |',
        '| Controles | PAGO | Tela plana constante; controle curvo com A(0)=1, A′(0)=2, área não localmente constante e componente de curvatura igual a 1. |',
        '| Campo nulo geodésico e horizonte geral | NÃO PAGO | O campo é recebido; não se constrói horizonte imerso, família transversal ou equilíbrio geral. |',
        '| Entropia microscópica e gravitação quântica geral | NÃO PAGO | Vínculo entropia-área, coeficiente físico, calor, H3, ponte modular e globalização permanecem abertos. |',
        '',
        f"{len(data['modules'])} módulos; {data['theorems']} teoremas; {data['printed_definitions']} definições com axiomas separadamente impressos.",
        f"Separação da contagem: {data['copied_theorems']} teoremas e {data['copied_printed_definitions']} definições copiados de 013; "
        f"{data['integration_theorems']} teorema de integração; {data['new_geometric_theorems']} teoremas e {data['new_printed_definitions']} definições da nova construção e seus controles.",
        'As contagens vêm dos fontes. Dependências finais restritas a propext, Classical.choice e Quot.sound; sem erros, avisos ou sorryAx.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation014.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando acima só lê e confere a custódia. A gerência deve recompilar em sua cópia independente; os comandos abaixo recompilam os módulos novos no caminho local atual e escrevem os respectivos binários/logs:',
        '', '\u0060\u0060\u0060powershell',
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['\u0060\u0060\u0060', '',
             'O último módulo importa conjuntamente toda a árvore nova e os controles anteriores. A ordem completa das fontes locais está em bench_source_build_order no manifesto. As fontes/binários locais estão fixados; Lean 4.31.0/mathlib são dependências externas. A bancada não alega uma recompilação independente da cadeia nem um pacote portátil.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO014_DERIVACAO_PREVIA.md',
                   'CONTINUACAO014_PARECER.md', 'audit_continuation014.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Cópias corrigidas de 013', '', '| Original | Cópia | SHA256 original | SHA256 cópia |', '|---|---|---|---|']
    for item in data['mechanical_copies']:
        rows.append(f"| \u0060{item['original']}\u0060 | \u0060{item['copy']}\u0060 | \u0060{item['original_sha256']}\u0060 | \u0060{item['copy_sha256']}\u0060 |")
    rows += ['', 'O auditor verifica que somente namespace/end namespace e nomes de imports locais foram substituídos. A colisão de nomes flatNullFrame foi identificada pela leitura dos dois fontes originais; não foi rodada uma sonda conjunta desses originais. A compilação conjunta das cópias corrigidas foi executada e passou.',
             '', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; erro de elaboração ou aviso; cópia exata do log.")
    rows += ['', 'Revisões conservam backups dos bytes. Falhas de elaboração de ODE, filtros, diferenciação, expansão matricial, denominadores e avisos de táticas redundantes foram corrigidos sem apagar os registros. A custódia das entregas anteriores permanece imutável.',
             '', '## Limites e encaminhamento', '',
             'A construção recebe V suave, nulo e geodésico numa vizinhança, V(x)≠0, e uma solda suave invertível. Produz uma curva e uma tela ao longo dela, não uma superfície imersa ou um horizonte geral. O contrato GeometricScreenAlong é local no parâmetro passado de zero.',
             '', 'O controle curvo tem expansão inicial 2; portanto não satisfaz B(0)=0. Ele não é uma construção completa do horizonte de equilíbrio ou de Clausius. A(0)=1 é normalização da base, não uma unidade física deduzida.',
             '', 'Entropia-área microscópica, calor/H3, coeficiente físico, seleção de assinatura/dimensão, ponte modular e globalização permanecem OPEN. Não há prova ou confirmação de gravidade quântica geral.',
             '', 'Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. Parecer detalhado: ' + str(ROOT / 'CONTINUACAO014_PARECER.md') + '. A gerência audita independentemente antes de incorporar.']
    return '\n'.join(rows) + '\n'


def verify_custody():
    data = json.loads(read(MANIFEST))
    for item in data['files']:
        path = Path(item['path'])
        if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
            raise RuntimeError(f'Custody mismatch: {path}')
    if inspect_copies() != data['mechanical_copies']:
        raise RuntimeError('Mechanical copy inventory changed')
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
          f"{data['theorems']} theorems ({data['new_geometric_theorems']} new, "
          f"{data['copied_theorems']} copied, {data['integration_theorems']} integration); "
          f"{data['printed_definitions']} printed definitions; mechanical copies and delivery verified")


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_014_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_014_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 014 already occupied; refusing publication')
        preserve_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        verify_custody()
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'new_geometric_theorems': data['new_geometric_theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        verify_custody()
    else:
        raise SystemExit('Usage: audit_continuation014.py [--write]')
