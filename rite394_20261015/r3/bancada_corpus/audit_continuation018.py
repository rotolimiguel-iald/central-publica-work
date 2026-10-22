"""Exact-byte and Lean-output audit for spontaneous continuation 018.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'TransverseInitialData', 'GeodesicShooting', 'ShootingLocalInverse',
    'NullCongruenceField', 'ConstructedNullCongruence',
    'CongruenceScreenIntegration', 'NullCongruenceControls',
]
MANIFEST = ROOT / 'CONTINUACAO018_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_018_ESPONTANEA_congruencia_nula_local_construida.md'
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

    visit('NullCongruenceControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation018.py', 'revise_continuation018.py', 'verify_stage.ps1',
        'CONTINUACAO018_DERIVACAO_PREVIA.md', 'CONTINUACAO018_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO018_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation018.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation018.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending',
        'kind': 'spontaneous continuation 018; no managerial order 018 issued at publication time',
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'reuse': ['inverse function theorem and smooth inverse from mathlib',
                  'actual joint flow derivative from 016 and joint C-infinity flow from 017',
                  'null conservation in 015 and transported screen existence in 014',
                  'curved background, explicit expanding congruence and curvature control in 014'],
        'integrated_root': 'NullCongruenceControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
        'paid': ['normalized covector and transverse projection constructed from a nonzero tangent',
                 'smooth transported null seed from the inverse solder',
                 'open shooting domain containing zero with smooth position and velocity',
                 'actual shooting position derivative at zero equals the identity',
                 'inverse chart with C-infinity inverse on its entire open target',
                 'spacetime vector field obtained by velocity composed with inverse position',
                 'nullity, nonvanishing and prescribed base value of the constructed field',
                 'vanishing actual covariant acceleration by uniqueness of curve derivatives',
                 'local smooth null geodesic congruence from a smooth invertible solder',
                 'transported screen and area derivative identity for the constructed congruence',
                 'flat and nonzero-curvature construction controls',
                 'explicit geodesic null field with nonzero expansion separates equilibrium from geodesicity'],
        'inputs_and_unpaid': ['open subset of Coordinate4, smooth solder A and smooth inverse B',
                             'fixed dimension four and prescribed Lorentzian signature',
                             'prescribed nonzero initial tangent null for the soldered metric',
                             'first jet of equilibrium including expansion and shear conditions',
                             'null hypersurface immersion, hypersurface orthogonality and integrated area',
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
        '[REAL / INPUT / OPEN] ENTREGA 018 ESPONTÂNEA — congruência nula local construída por seção transversal e inversão suave.',
        '', '06/09/2026. Continuação de 017. Auditoria independente da gerência pendente. Nenhuma alteração de gate.',
        '', '## Critérios e alcance', '', '| Critério | Estado | Evidência |', '|---|---|---|',
        '| Derivação anterior ao código | PAGO | CONTINUACAO018_DERIVACAO_PREVIA.md; seis passos anteriores às provas Lean. |',
        '| Dados transversais | PAGO | exists_normalized_covector, initial_position_in_section, initial_position_shift e transported_seed_null. |',
        '| Domínio aberto e suavidade | PAGO | shooting_domain_zero e shooting_phase_smooth; argumentos mantidos no domínio fixo do fluxo de 017. |',
        '| Diferencial invertível | PAGO | shooting_position_derivative_zero: DX(0)=I, usando o diferencial efetivo do fluxo de 016. |',
        '| Inversa suave no aberto | PAGO | smoothLocalChart produz OpenPartialHomeomorph com fonte contida no domínio e inversa ContDiffOn ℝ ∞ em todo o alvo. |',
        '| Campo espacial construído | PAGO | shootingCongruence=Y∘X⁻¹; congruence_smooth, congruence_nonzero, congruence_null e congruence_base_value. |',
        '| Equação geodésica | PAGO | congruence_geodesic: vectorAcceleration Γ V=0; a prova usa derivadas reais das curvas X(z+sv) e Y(z+sv). |',
        '| Existência a partir da solda | PAGO sob INPUT | local_levi_civita_null_congruence recebe apenas aberto, solda/inversa suaves e tangente nula não nula; constrói N e V. |',
        '| Tela e variação de área | PAGO sob INPUT | constructed_congruence_transported_screen aplica 014 ao campo construído e prova A′=θA localmente, no lado t<0. |',
        '| Controles | PAGO | Congruência construída com solda identidade; construção em fundo de curvatura não zero; campo explícito geodésico nulo com θ(0)=2. |',
        '| Primeiro jato de equilíbrio | NÃO PAGO | Nulidade e geodesicidade não impõem θ=0 nem cisalhamento nulo. O controle separa essas obrigações. |',
        '| Reconstrução gravitacional geral | NÃO PAGO | Horizonte nulo imerso, área integrada, H3, ponte microscópica, coeficiente físico, calor, ponte modular e globalização seguem OPEN. |',
        '', f"{len(data['modules'])} módulos; {data['theorems']} teoremas declarados; {data['printed_definitions']} definição com axiomas impressos separadamente. Contagens lidas dos fontes.",
        'Todas as compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound.',
        'As contagens incluem lemas auxiliares, aplicações e controles que reutilizam resultados anteriores. Não são contagens de descobertas científicas.',
        '', '## Enunciado principal', '',
        'Se U é aberto, A e B são campos matriciais suaves com AB=BA=I em U, p∈U, v≠0 e (A(p)ᵀηA(p))(v,v)=0, existem N aberto com p∈N⊆U e V suave em N tais que V(p)=v, V não se anula, g(V,V)=0 e ∇_V V=0 em N.',
        'A solda, a dimensão e a assinatura são INPUT. A existência de V deixou de ser INPUT nesta etapa. A conclusão é local; não constrói por si uma hipersuperfície nula ou um horizonte.',
        '', '## Reprodução', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation018.py'}'",
        '\u0060\u0060\u0060', '',
        'O comando é somente leitura e confere os bytes, logs, enunciados contados e dependências de axiomas registrados. A gerência deve recompilar numa cópia para a auditoria independente, preservando os artefatos entregues. Ordem dos módulos novos:',
    ]
    rows.extend('- ' + m + '.lean' for m in MODULES)
    rows += ['', 'NullCongruenceControls importa toda a árvore 018 e as entregas anteriores usadas. A ordem local completa consta do manifesto. verify_stage.ps1 documenta a compilação Lean 4.31.0; as dependências externas não constituem um pacote portátil integral.',
             '', '## Axiomas impressos', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
             f"Manifesto: \u0060{MANIFEST}\u0060 — SHA256 \u0060{digest(MANIFEST)}\u0060.",
             f"Inventário: {len(data['files'])} caminhos absolutos, cada um com tamanho e hash dos bytes.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO018_DERIVACAO_PREVIA.md',
                   'CONTINUACAO018_PARECER.md', 'audit_continuation018.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit code {run['exit_code']}; cópia exata do log rejeitado.")
    rows += ['', 'Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Falhas intermediárias não são evidência de prova: somente as compilações finais limpas sustentam a entrega. O helper de revisão teve uma quebra de linha ausente na criação; falhou antes de escrever documentos e sua versão defeituosa também foi preservada.',
             '', '## Limites e próximo elo', '',
             'A seção transversal inicial usa ℓ(v)=1 e Π=I−v⊗ℓ. Isso garante uma carta do fluxo; não garante que o campo resultante seja normal a uma hipersuperfície nula. Primeiro jato de equilíbrio e integrabilidade do horizonte são obrigações próprias.',
             'O controle com θ(0)=2 reutiliza o campo explícito expandingNullVelocity de 014; não afirma que toda escolha de campo construída tenha essa expansão. Seu papel é refutar a implicação geodesicidade + nulidade ⇒ expansão zero.',
             'A identidade de área é a da tela transportada de 014, válida eventualmente para t<0 perto de zero. Não é ainda uma integração sobre um horizonte.',
             'Não se identifica flowVariation com a conjugação modular. Nenhuma ponte região–álgebra, entropia–área, H3 ou coeficiente físico foi assumida paga pelo novo teorema.',
             '', 'Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. As custódias 016 e 017 foram reconferidas por seus auditores de leitura.',
             'O objetivo amplo permanece ativo e OPEN. A incorporação é da gerência após auditoria; a confirmação física é ato do observador. Esta entrega transporta o enunciado condicional exato.',
             '', 'Parecer: ' + str(ROOT / 'CONTINUACAO018_PARECER.md') + '.',
             '', 'Ordens de entrada encontradas no inventário:']
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_018_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_018_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 018 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation018.py [--write]')



