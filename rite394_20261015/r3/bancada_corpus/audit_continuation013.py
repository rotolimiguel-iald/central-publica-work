"""Exact-byte and Lean-output audit for spontaneous continuation 013.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'CovariantNullPreservation', 'SpatialScreenConstruction', 'NullFrameConstruction',
    'ConstructedScreenAtPoint', 'NullScreenConstructionControls',
]
MANIFEST = ROOT / 'CONTINUACAO013_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_013_ESPONTANEA_nulidade_e_tela_construida_no_ponto.md'
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
        'audit_continuation013.py', 'revise_continuation013.py', 'verify_stage.ps1',
        'CONTINUACAO013_DERIVACAO_PREVIA.md', 'CONTINUACAO013_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO013_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation013.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation013.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 013; no managerial order 013 issued at publication time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['actual derivative of the null field norm',
                 'null-gradient frame pairing deduced from metric compatibility',
                 'spatial screen constructed by orthogonal reflection for every unit direction',
                 'normalized null frame and inverse for every nonzero Minkowski null vector',
                 'explicit inverse-solder transport of the frame and its Gram',
                 'pointwise inhabitant of the existing NullScreenAt contract for Levi-Civita',
                 'normalized area and non-axis null control',
                 'zero-direction impossibility and normalized-family expansion obstruction'],
        'inputs_and_unpaid': ['existence and regularity of Lie-transported screens',
                             'existence of general null geodesic congruences',
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
        '[REAL / INPUT / OPEN] ENTREGA 013 ESPONTÂNEA — preservação da nulidade e construção pontual da tela.',
        '', 'Continuação de 012, 05/09/2026. Nenhuma ordem 013 da gerência estava no túnel ao publicar. Auditoria independente pendente; nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO nos alvos iniciais | CONTINUACAO013_DERIVACAO_PREVIA.md; o controle suplementar de famílias normalizadas é documentado posteriormente no parecer. |',
        '| Preservação de g(V,V)=0 | PAGO | Derivadas efetivas: d[g(V,V)](w)=2g(V,∇wV); nulidade numa vizinhança implica g(V,∇wV)=0. |',
        '| Condição da tela anteriormente recebida | PAGO | null_field_preserves_frame_pairing produz preserves_null_pairing da primeira coluna V; nenhuma hipótese geodésica necessária aqui. |',
        '| Base transversal para todo eixo unitário | PAGO | reflectedSpatialScreen usa uma reflexão ortogonal em R³. |',
        '| Referencial nulo para toda direção não nula | PAGO | flatNullFrame: Gram G0=nullScreenGram(-I), inversa construída e primeira coluna v. |',
        '| Transporte para métrica soldada | PAGO | solderedNullFrame: g=EᵀηE, F=D F0; produtos inversos e Gram provados. Assinatura e dimensão permanecem INPUT. |',
        '| Habitante do contrato da entrega 012 | PAGO no ponto | leviCivitaScreenAtPoint e levi_civita_null_screen_exists; não recebem tela nem preserves_null_pairing. |',
        '| Densidade inicial | PAGO como normalização | Gram transversal -I implica A=1 na base escolhida. Não fixa área física. |',
        '| Controles contra vacuidade e promoção indevida | PAGO | Vetor (5,3,4,0), direção zero impossível, família normalizada com lei A′=θA exige θ=0. |',
        '| Família transportada e horizontes gerais | NÃO PAGO | Não construída uma tela suave que satisfaça transporte de Lie, nem congruência/superfície geral. |',
        '| Gravitação quântica geral | NÃO PAGO | Entropia-área microscópica, calor, H3, ponte modular, escala e globalização permanecem abertos. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas; {data['printed_definitions']} definições com axiomas separadamente impressos. Contagens lidas dos fontes. Apenas propext, Classical.choice e Quot.sound nas dependências finais; sem erros, avisos ou sorryAx.",
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation013.py'}'",
        '\u0060\u0060\u0060',
        '', 'O comando acima só lê e confere a custódia. Comandos de recompilação dos módulos novos, na ordem abaixo (a gerência deve usar sua cópia independente):',
        '', '\u0060\u0060\u0060powershell',
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['\u0060\u0060\u0060', '', 'O manifesto fixa a árvore local de fontes, cópias binárias e logs. Lean 4.31.0/mathlib são dependências externas locais; isto não é um pacote portátil nem uma recompilação independente.',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO013_DERIVACAO_PREVIA.md',
                   'CONTINUACAO013_PARECER.md', 'audit_continuation013.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; erro de elaboração ou aviso; cópia exata do log.")
    rows += ['', 'As revisões têm backups dos bytes. Erros de sintaxe, diferenciação de somas e redução das entradas matriciais foram corrigidos; seus logs continuam no inventário. O histórico da correção de assinatura da entrega 012 permanece fixado por seu manifesto, sem alterar os arquivos anteriores.',
             '', '## Limites e integração', '',
             'O enunciado principal assume um campo V suave e nulo numa vizinhança, V(x)≠0 e uma solda suave invertível em quatro dimensões. A construção é pontual. A existência desse campo para todos os dados de horizonte, sua geodesicidade e o transporte dos vetores de tela ainda têm de ser construídos.',
             '', 'Normalizar independentemente cada tela produz Gram -I e área 1 em cada parâmetro; isso não é o transporte que mede uma área em expansão. O controle normalized_family_expansion_obstruction formaliza precisamente essa restrição.',
             '', 'Fonte primária de contexto: [Dey e Majhi, 2020](https://arxiv.org/abs/2009.08221), sobre superfície nula, projeção transversal e vetor nulo auxiliar. As provas aqui usam as definições e operações formais locais; a referência não fornece uma hipótese física ao kernel.',
             '', 'Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. A gerência recompila e audita antes de incorporar. Objetivo amplo ativo e OPEN.']
    return '\n'.join(rows) + '\n'

if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_013_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_013_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 013 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation013.py [--write]')



