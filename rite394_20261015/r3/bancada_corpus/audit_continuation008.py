"""Verify continuation 008 using exact source bytes and preserved Lean output.

Default mode reads only. --write creates a new, immutable spontaneous delivery.
No canonical files, memories, um.py, network services or imported project scripts are touched.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'TensorNullCone', 'MetricCompatibleJet', 'CovariantScalarConservation',
    'MetricFieldConnection', 'LorentzMetricField', 'TensorFieldLinearity',
    'GeneralTensorReconstruction', 'TensorReconstructionControls',
]
MANIFEST = ROOT / 'CONTINUACAO008_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_008_ESPONTANEA_reconstrucao_tensorial_condicional.md'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig')


def write_new_bytes(path, raw):
    if not path.resolve().is_relative_to(ROOT):
        raise RuntimeError(f'Write outside the bench refused: {path}')
    if path.exists():
        raise RuntimeError(f'Overwrite refused: {path}')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw) or temp.read_bytes() != raw:
        raise RuntimeError(f'Incomplete output: {temp}')
    temp.rename(path)


def write_new(path, value):
    write_new_bytes(path, value.encode('utf-8'))


def attempts(module):
    values = []
    for meta in sorted(ROOT.glob(module + '.*.json')):
        data = json.loads(read(meta))
        log = ROOT / data['log']
        if not log.is_file():
            raise RuntimeError(f'Missing compiler output: {log}')
        output = read(log)
        rejected = data['exit_code'] != 0 or bool(re.search(r'\b(error|warning):', output))
        label = 'failed_compile' if data['exit_code'] != 0 else 'rejected_warning'
        archive = log.with_name(log.stem + '.' + label + '.log') if rejected else None
        values.append((meta, data, log, output, archive))
    return values


def preserve_rejected_attempts():
    for module in MODULES:
        for _, _, log, _, archive in attempts(module):
            if archive is not None:
                raw = log.read_bytes()
                if archive.exists():
                    if archive.read_bytes() != raw:
                        raise RuntimeError(f'Failed-attempt archive mismatch: {archive}')
                else:
                    write_new_bytes(archive, raw)


def inventory():
    records, paths = [], set()
    for module in MODULES:
        source = ROOT / (module + '.lean')
        code = read(source)
        if re.search(r'\b(sorry|admit|axiom)\b', code):
            raise RuntimeError(f'Forbidden final-source declaration: {source}')
        declarations = re.findall(r'^(theorem|def)\s+(\w+)', code, re.M)
        theorems = [name for kind, name in declarations if kind == 'theorem']
        prints = re.findall(r'^#print axioms (\w+)', code, re.M)
        if set(theorems) != set(prints) or len(prints) != len(set(prints)):
            raise RuntimeError(f'Theorem axiom coverage mismatch: {module}')
        runs = attempts(module)
        clean = [row for row in runs if row[1]['exit_code'] == 0 and row[1]['source_stable']
                 and row[1]['proof_sha256'].lower() == digest(source) and row[4] is None]
        if not clean:
            raise RuntimeError(f'No clean exact-source compilation: {module}')
        meta, data, log, output, _ = clean[-1]
        if 'sorryAx' in output:
            raise RuntimeError(f'Unproved dependency in final output: {log}')
        rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
        if sorted(name.split('.')[-1] for name, _ in rows) != sorted(prints):
            raise RuntimeError(f'Compiler print list mismatch: {module}')
        axiom_rows = []
        for name, value in rows:
            axioms = [item.strip() for item in value.split(',') if item.strip()]
            if not set(axioms) <= ALLOWED_AXIOMS:
                raise RuntimeError(f'Unexpected axioms: {name}: {axioms}')
            axiom_rows.append({'declaration': name, 'axioms': axioms})
        run_rows = []
        for m, d, l, out, archive in runs:
            paths.update([m, l])
            if archive is not None:
                if not archive.exists() or archive.read_bytes() != l.read_bytes():
                    raise RuntimeError(f'Rejected attempt not preserved byte for byte: {l}')
                paths.add(archive)
            issues = [line for line in out.splitlines() if re.search(r'\b(error|warning):', line)]
            run_rows.append({
                'metadata': str(m), 'log': str(l), 'exit_code': d['exit_code'],
                'source_sha256': d['proof_sha256'].lower(), 'issues': issues,
                'rejected_attempt_copy': str(archive) if archive is not None else None,
            })
        records.append({
            'module': module, 'theorems': len(theorems), 'axioms': axiom_rows,
            'helper_definitions_not_separately_printed': [n for k, n in declarations if k == 'def'],
            'final_log': str(log), 'final_metadata': str(meta), 'attempts': run_rows,
        })
        paths.update([source, ROOT / (module + '.olean')])
        paths.update(ROOT.glob(module + '.lean.bak_*'))
    visited, source_order = set(), []

    def visit(module):
        path = ROOT / (module.replace('.', '/') + '.lean')
        if module in visited or not path.exists():
            return
        visited.add(module)
        for imported in re.findall(r'^import\s+(\S+)', read(path), re.M):
            visit(imported)
        source_order.append(module)
        paths.add(path)
        binary = path.with_suffix('.olean')
        if binary.exists():
            paths.add(binary)

    for module in MODULES:
        visit(module)
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation008.py', 'verify_stage.ps1',
        'CONTINUACAO008_DERIVACAO_PREVIA.md', 'CONTINUACAO008_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'ORDEM006_MANIFESTO.json', 'ORDEM007_MANIFESTO.json',
        'fontes/tgl_kernel/TGLExt/EmergenceTriad.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean',
        'fontes/tgl_kernel/TGLExt/PoincareGroup.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO008_*.md.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact source bytes and Lean compiler evidence; independent audit pending',
        'kind': 'spontaneous continuation; no order 008 was issued at delivery time',
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'bench_source_build_order': source_order, 'files': files,
        'scope': 'Conditional tensor reconstruction on an open preconnected coordinate domain. '
                 'Lorentzian frame, null condition and conservation remain explicit inputs.',
        'unpaid': ['general curvature and geometric Einstein tensor', 'contracted Bianchi',
                   'physical null condition', 'global chart gluing',
                   'H3 from dynamics', 'four channels', 'derived signature', 'broad quantum gravity goal'],
        'dependency_limit': 'Bench source closure and copied TGL/TGLExt olean files are pinned. '
                            'External Lean 4.31.0/mathlib environment is resolved by verify_stage.ps1; '
                            'this is not a portable dependency bundle or an independent compilation.',
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 008 ESPONTÂNEA — reconstrução tensorial condicional: o cone nulo determina A=fg e a conservação torna f constante em um domínio coordenado aberto preconexo.',
        '', '05/09/2026. Continuação após a entrega 007, conforme o protocolo. Não responde a uma ordem 008 da gerência: essa ordem não estava no túnel ao publicar esta entrega. Pronta para auditoria independente; não altera gate ou conclusão física.',
        '', '## Resultado e critérios desta continuação', '',
        '| Critério | Estado | Evidência e limite |', '|---|---|---|',
        '| Derivação antes do código | PAGO | CONTINUACAO008_DERIVACAO_PREVIA.md. |',
        '| Rigidez para tensores gerais | PAGO | lorentz_tensor_null_rigidity: matriz simétrica geral e contrato LorentzByCongruence; reutiliza o GeneralNullCone anterior. |',
        '| Métrica e inversa do referencial | PAGO com referencial como INPUT | g=EᵀηE, g⁻¹=DηDᵀ; as duas identidades de inversão são teoremas. η não foi derivada. |',
        '| Conexão de Levi-Civita | PAGO na carta | Fórmula construída das derivadas de g, torção zero e compatibilidade provadas. |',
        '| Derivadas genuínas | PAGO | fderiv, regra do produto e igualdade local em aberto; hipóteses de diferenciabilidade explícitas. |',
        '| Coeficiente produzido | PAGO | f=(DᵀAD)₀₀, A=fg e diferenciabilidade de f provadas. |',
        '| Conservação ⇒ constante | PAGO | div(fg)=df; derivada zero e preconexão dão f constante. |',
        '| G+Λg=κT | PAGO como implicação | G,T simétricos diferenciáveis conservados; diferença anula o cone nulo. Λ é constante. G é um campo do enunciado, não o tensor de Einstein já construído. |',
        '| Controle sem conservação | PAGO | A(x)=x⁰η anula o cone, tem coeficiente não constante e divergência temporal 1. |',
        '| Curvatura/Bianchi gerais | NÃO PAGO | Construir Ric, R, G geométrico e provar conservação. |',
        '| Hipótese nula da dinâmica/horizontes | NÃO PAGO | Clausius/Raychaudhuri e H3 não foram produzidos. |',
        '| Globalização e origem do referencial | NÃO PAGO | Colagem de cartas, quatro canais e assinatura derivada permanecem abertos. |',
        '', f"São {len(data['modules'])} módulos novos e {data['theorems']} teoremas novos, contados nos fontes. Todos os teoremas têm #print axioms e compilação limpa para os hashes finais. As definições auxiliares não impressas individualmente são listadas no manifesto; as provas que as usam têm suas dependências axiomáticas verificadas.",
        '', '## Reprodução', '', '```powershell',
        f"& 'C:\\Python314\\python.exe' '{ROOT / 'audit_continuation008.py'}'",
    ]
    for module in MODULES:
        rows += [f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}",
                 'if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }']
    rows += ['```', '', 'Os comandos recompilam os módulos novos usando as dependências locais já presentes. O manifesto registra a ordem de compilação dos fontes da bancada e os oleans locais; o ambiente externo Lean/mathlib não é um pacote portátil. A auditoria de bytes não substitui a recompilação independente da gerência.',
             '', '## Axiomas impressos', '', '```text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    rows += ['```', '', '## Arquivos e hashes dos bytes', '',
             f"Manifesto: `{MANIFEST}` — SHA256 `{digest(MANIFEST)}`.",
             f"O manifesto contém {len(data['files'])} registros com caminho absoluto, tamanho e SHA256. Os valores desta tabela são lidos dos arquivos pelo script.",
             '', '| Artefato | SHA256 |', '|---|---|']
    primary = {str(ROOT / (module + '.lean')) for module in MODULES}
    primary.update(module['final_log'] for module in data['modules'])
    primary.update(str(ROOT / name) for name in [
        'CONTINUACAO008_DERIVACAO_PREVIA.md', 'CONTINUACAO008_PARECER.md', 'audit_continuation008.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| `{item['path']}` | `{item['sha256']}` |")
    rows += ['', '## Tentativas preservadas', '']
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_attempt_copy']:
                rows.append(f"- `{run['rejected_attempt_copy']}`: cópia de bytes do log, exit code {run['exit_code']}; metadados e fonte correspondente preservados. Os erros e avisos estão discriminados no manifesto.")
    rows += ['', '## O alcance que continua aberto', '',
             'O parecer detalha as hipóteses e os passos pagos. Assinatura, referencial e condição nula são entradas; G ainda não foi identificado com Ric−½Rg; conservação de G/T não foi obtida de Bianchi/dinâmica. O resultado cobre uma carta, não uma variedade global já colada. A gravitação quântica em sentido amplo permanece aberta.',
             '', 'Escritas somente em Chatgpt. Nenhum um.py executado/importado/editado; nenhum kernel canônico, Atlas, memória, selo ou gate alterado. As entregas 006 e 007 permanecem intactas. Nenhum dado observacional foi buscado.',
             '', 'A gerência audita antes de incorporar e atualiza as superfícies da casa quando houver incorporação. A confirmação física não é consequência desta entrega matemática.']
    return '\n'.join(rows) + '\n'


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_008_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_008_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 008 or manifest already occupied; refusing publication')
        preserve_rejected_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'files': len(data['files']), 'delivery': str(DELIVERY),
                          'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
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
                    'sorryAx' in output or re.search(r'\b(error|warning):', output)):
                raise RuntimeError(f'Invalid final compilation: {module["module"]}')
            rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
            actual = [{'declaration': name, 'axioms': [a.strip() for a in value.split(',') if a.strip()]}
                      for name, value in rows]
            if actual != module['axioms'] or any(not set(row['axioms']) <= ALLOWED_AXIOMS for row in actual):
                raise RuntimeError(f'Axiom record mismatch: {module["module"]}')
            count = len(re.findall(r'^theorem\s+', read(source), re.M))
            prints = re.findall(r'^#print axioms (\w+)', read(source), re.M)
            if count != module['theorems'] or sorted(prints) != sorted(row['declaration'].split('.')[-1] for row in actual):
                raise RuntimeError(f'Theorem coverage mismatch: {module["module"]}')
        if delivery_text(data) != read(DELIVERY):
            raise RuntimeError('Delivery content does not match the pinned inventory')
        print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
              f"{data['theorems']} theorems; all axiom logs checked; delivery verified")
    else:
        raise SystemExit('Usage: audit_continuation008.py [--write]')
