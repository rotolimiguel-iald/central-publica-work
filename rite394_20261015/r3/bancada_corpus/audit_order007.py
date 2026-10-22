"""Audit order 007 from bytes and compiler logs. Default mode is read-only."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = [
    'StationaryModularPeriod', 'PeriodAverageOperator', 'PeriodAveragePrefix',
    'PeriodicCentralizerExpectation', 'TailNotCyclic', 'CyclicExpectationObstruction',
    'PeriodicBorchersObstruction', 'ProductBorchersObstruction',
    'ModularSignatureObstruction', 'Order007Bridges',
]
MANIFEST = ROOT / 'ORDEM007_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_007_habitante_global_nao_ciclicidade_e_assinatura.md'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig')

def write_new(path, value):
    if path.exists():
        raise RuntimeError(f'Refusing overwrite: {path}')
    raw = value.encode('utf-8')
    if any(c < 32 and c not in (9, 10, 13) for c in raw):
        raise RuntimeError('Invalid control character')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw) or temp.read_bytes() != raw:
        raise RuntimeError(f'Incomplete output: {temp}')
    temp.rename(path)

def inventory():
    records, paths = [], set()
    for module in MODULES:
        source = ROOT / (module + '.lean')
        code = read(source)
        if re.search(r'\b(sorry|admit|axiom)\b', code):
            raise RuntimeError(f'Forbidden declaration in final source: {source}')
        declarations = re.findall(r'^(theorem|def)\s+(\w+)', code, re.M)
        theorems = [name for kind, name in declarations if kind == 'theorem']
        prints = re.findall(r'^#print axioms (\w+)', code, re.M)
        if not set(theorems) <= set(prints) or len(prints) != len(set(prints)):
            raise RuntimeError(f'Incomplete theorem axiom coverage: {module}')
        if not set(prints) <= {name for _, name in declarations}:
            raise RuntimeError(f'Unknown declaration in print list: {module}')
        attempts = []
        for meta in sorted(ROOT.glob(module + '.*.json')):
            data = json.loads(read(meta))
            log = ROOT / data['log']
            if not log.exists():
                raise RuntimeError(f'Missing log: {log}')
            paths.update([meta, log])
            attempts.append((meta, data, log))
        candidates = [(meta, data, log) for meta, data, log in attempts
                      if data['exit_code'] == 0 and data['source_stable']
                      and data['proof_sha256'].lower() == digest(source)]
        if not candidates:
            raise RuntimeError(f'No successful exact-source compilation: {module}')
        meta, data, log = candidates[-1]
        output = read(log)
        if 'sorryAx' in output or re.search(r'\b(error|warning):', output):
            raise RuntimeError(f'Final compiler log is not clean: {log}')
        rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
        if sorted(n.split('.')[-1] for n, _ in rows) != sorted(prints):
            raise RuntimeError(f'Compiler print coverage mismatch: {module}')
        axiom_rows = []
        for name, value in rows:
            axioms = [x.strip() for x in value.split(',') if x.strip()]
            if not set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}:
                raise RuntimeError(f'Unexpected axioms: {name}: {axioms}')
            axiom_rows.append({'declaration': name, 'axioms': axioms})
        records.append({
            'module': module, 'theorems': len(theorems),
            'printed_definitions': len(prints) - len(theorems),
            'helper_definitions_not_separately_printed': [n for k, n in declarations if k == 'def' and n not in prints],
            'final_log': str(log), 'final_metadata': str(meta), 'axioms': axiom_rows,
            'attempts': [{'metadata': str(m), 'log': str(l), 'exit_code': d['exit_code'],
                          'source_sha256': d['proof_sha256']} for m, d, l in attempts],
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
    for name in ['audit_order007.py', 'verify_stage.ps1', 'ORDEM007_DERIVACAO_PREVIA.md',
                 'ORDEM007_PARECER_FINAL.md', 'ORDEM007_NOTAS_DE_EXECUCAO.md',
                 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md']:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('ORDEM007_DERIVACAO_PREVIA.md.bak_*'))
    for name in ['ConcreteFourFrame', 'Solder4D', 'BisognanoWichmann', 'TheOathOnTheTower']:
        paths.add(ROOT / f'fontes/tgl_kernel/TGLExt/{name}.lean')
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        'status': 'REAL: exact bytes and Lean compiler evidence; independent managerial audit pending',
        'modules': records, 'theorems': sum(x['theorems'] for x in records),
        'printed_definitions': sum(x['printed_definitions'] for x in records),
        'bench_source_build_order': source_order, 'files': files,
        'dependency_limit': 'Bench source closure and copied TGL/TGLExt olean files pinned. '
          'External Lean/mathlib environment is resolved by verify_stage.ps1; not a portable bundle.',
    }

def delivery(data):
    rows = [
        '[REAL / DERIVED / KNOWN / OPEN] ENTREGA 007 — habitante global periódico construído; cauda não cíclica; obstruções de Borchers e da identificação finita da assinatura provadas com escopo explícito.',
        '', 'Pronta para auditoria independente da gerência. Escritas restritas a Chatgpt; nenhum um.py, gate, kernel canônico, Atlas ou memória foi alterado.',
        '', '## Critérios de aceitação', '',
        '| Critério | Estatuto | Evidência e alcance |', '|---|---|---|',
        '| A — derivação antes do código | PAGO | ORDEM007_DERIVACAO_PREVIA.md; adendo anterior à generalização de Borchers preservado em backup. |',
        '| A.1 stationary_modular_period | PAGO | Igualdade em H; generalização à rede inteira de log-razões dos sítios. |',
        '| A.2 period_average_operator | PAGO | Integral forte de vetores, continuidade, linearidade e norma ≤ ‖x‖. |',
        '| A.3 period_average_mem_factor | PAGO | Comutação com o comutante atravessa a integral; entrada efetiva no bicomutante M. |',
        '| A.4 period_average_prefix | PAGO | Projeção limitada em H atravessa a integral; cálculo de todas as entradas, sem hipótese fictícia de continuidade σ-fraca. |',
        '| A — habitante | PAGO | periodicExpectationInput e stationaryExpectationInput habitam TGLExt.ExpectationInput P; campos por prova. |',
        '| A — unicidade e restrição | PAGO | periodic_expectation_unique e periodic_expectation_local. |',
        '| A — controle ½ | PAGO | periodic_half_agrees em M; o wrapper não tracial exclui ½ por tipo, a construção periódica comum inclui. |',
        '| B.1 tail_not_cyclic | PAGO | Testemunha v, norma²=p(1−p)>0, ortogonalidade e fecho próprio. |',
        '| B.2 consequência abstrata | PAGO | SubalgebraExpectationInput é HIPÓTESE; ciclicidade força N=M. |',
        '| B.3 Borchers | PAGO como negativo condicionado; PAREDE NOMEADA para formalização do teorema clássico | product_borchers_trivial vale para TODO perfil produto sob continuidade, norma preservada, V(0)=I e relação de Borchers. Energia positiva/compressão ⇒ relação permanece KNOWN, não axioma Lean. |',
        '| C.1 invariância e não invariância | PAGO | Métrica lorentziana soldada preservada; euclidiana não preservada por boost não trivial, para frame invertível. |',
        '| C.1 identificação Δ^{it}↔boost finito | NEGATIVO PAGO no tipo testado | Entrelaçamento injetivo de ℝ⁴ com isometria positiva força parâmetro do boost zero; aplica-se ao fluxo real da torre. |',
        '| C.1 escolha única de assinatura | NÃO PAGO; INFERÊNCIA REFUTADA | Um único boost preserva (1,3) e (2,2). A comparação com (4,0) não seleciona sozinha Lorentz. |',
        '| C.2 pontes matriciais | PAGO | B₄ usa K₁ canônico; bloco coincide com TGLExt.boost; nada por homonímia. |',
        '| C — ponte geométrica geral | PAREDE NOMEADA | Requer outra representação/objetos e domínio explícito; não foi construída. |',
        '| A/B/C — frase final | PAGO | Matemática sem escolha delegada ao operador; incorporação pela gerência após auditoria. |',
        '', '## Verificação e reprodução', '',
        f"{len(data['modules'])} módulos; {data['theorems']} teoremas; {data['printed_definitions']} definições com axiomas impressos; todos os logs finais limpos e dependências axiomáticas contidas no trio. Definições auxiliares sem impressão individual são identificadas no manifesto e estão cobertas pelas provas que as usam.",
        '', 'Executar com o ambiente local de Lean 4.31.0 e dependências resolvidas pelo verificador:', '',
        '```powershell', f"python '{ROOT / 'audit_order007.py'}'",
    ]
    for module in MODULES:
        rows.append(f"& '{ROOT / 'verify_stage.ps1'}' -Module {module}")
        rows.append('if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }')
    rows += ['```', '', 'O manifesto inclui a ordem de compilação das dependências da bancada. Os comandos acima recompilam os dez módulos novos usando essas dependências já presentes. O auditor de bytes não é uma recompilação independente.',
             '', '## Axiomas efetivamente impressos', '', '```text']
    for module in data['modules']:
        for entry in module['axioms']:
            rows.append(entry['declaration'] + ': [' + ', '.join(entry['axioms']) + ']')
    rows += ['```', '', '## Arquivos e SHA256', '',
             f'Manifesto completo: `{MANIFEST}` — SHA256 `{digest(MANIFEST)}`.',
             f"São {len(data['files'])} arquivos por caminho absoluto, tamanho e hash dos bytes, incluindo todas as tentativas registradas, backups e dependências locais compiladas.", '',
             '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / name) for name in ['ORDEM007_DERIVACAO_PREVIA.md', 'ORDEM007_PARECER_FINAL.md',
                                                'ORDEM007_NOTAS_DE_EXECUCAO.md', 'audit_order007.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| `{item['path']}` | `{item['sha256']}` |")
    rows += ['', 'O parecer detalha enunciados, topologias, hipóteses, limites e os negativos. A entrega não é a reconstrução gravitacional geral e não altera qualquer conclusão física. O objetivo amplo permanece aberto.', '',
             'Nada nas conclusões matemáticas é decisão do operador. A gerência audita e decide incorporação; v98, errata e contorno continuam reservados ao operador.']
    return '\n'.join(rows) + '\n'

if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        if MANIFEST.exists() or DELIVERY.exists():
            raise RuntimeError('Order already delivered; refusing overwrite')
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery(data))
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        data = json.loads(read(MANIFEST))
        for item in data['files']:
            path = Path(item['path'])
            if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
                raise RuntimeError(f'Custody mismatch: {path}')
        fresh = inventory()
        if (fresh['theorems'], fresh['printed_definitions']) != (data['theorems'], data['printed_definitions']):
            raise RuntimeError('Declaration inventory changed')
        print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
              f"{data['theorems']} theorems; {data['printed_definitions']} printed definitions; all axiom logs checked")
    else:
        raise SystemExit('Usage: audit_order007.py [--write]')
