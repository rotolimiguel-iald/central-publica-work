"""Read-only audit by default; --write creates a new immutable order delivery."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['CentralizerLocal', 'LocalCentralizerExpectation',
           'TracialCentralizerExpectation', 'SiteModularInvariance',
           'CentralizerContractBridge']
MANIFEST = ROOT / 'ORDEM006_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_text(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig')

def put_new(path, content):
    if path.exists():
        raise RuntimeError(f'Refusing overwrite: {path}')
    raw = content.encode('utf-8')
    if any(byte < 32 and byte not in (9, 10, 13) for byte in raw):
        raise RuntimeError('Unexpected control character in generated artifact')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw) or temp.read_bytes() != raw:
        raise RuntimeError(f'Incomplete write: {temp}')
    temp.rename(path)

def inventory():
    records, paths = [], set()
    for module in MODULES:
        source = ROOT / (module + '.lean')
        code = read_text(source)
        if re.search(r'\b(sorry|admit|axiom)\b', code):
            raise RuntimeError(f'Untrusted declaration: {source}')
        declarations = re.findall(r'^(theorem|def)\s+(\w+)', code, re.M)
        prints = re.findall(r'^#print axioms (\w+)', code, re.M)
        if sorted(prints) != sorted(name for _, name in declarations):
            raise RuntimeError(f'Incomplete axiom print coverage: {module}')
        attempts = []
        for meta in sorted(ROOT.glob(module + '.*.json')):
            data = json.loads(read_text(meta))
            log = ROOT / data['log']
            if not log.exists():
                raise RuntimeError(f'Missing attempt log: {log}')
            attempts.append((meta, data, log))
            paths.update([meta, log])
        successful = [(m, d, l) for m, d, l in attempts if d['exit_code'] == 0
                      and d['source_stable'] and d['proof_sha256'].lower() == digest(source)]
        if not successful:
            raise RuntimeError(f'No successful compilation for exact source: {module}')
        meta, data, log = successful[-1]
        output = read_text(log)
        rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
        if sorted(name.split('.')[-1] for name, _ in rows) != sorted(prints):
            raise RuntimeError(f'Compiler log coverage mismatch: {module}')
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        for name, axioms in rows:
            if not set(axioms.split(', ')) <= allowed:
                raise RuntimeError(f'Unexpected axioms: {name}: {axioms}')
        if 'sorryAx' in output or re.search(r'\berror:', output):
            raise RuntimeError(f'Invalid successful log: {log}')
        records.append({'module': module, 'theorems': sum(k == 'theorem' for k, _ in declarations),
                        'definitions': sum(k == 'def' for k, _ in declarations),
                        'axioms': [{'declaration': n, 'axioms': a.split(', ')} for n, a in rows],
                        'final_log': str(log), 'final_metadata': str(meta),
                        'attempts': [{'metadata': str(m), 'exit_code': d['exit_code']} for m, d, _ in attempts]})
        paths.update([source, ROOT / (module + '.olean')])
        paths.update(ROOT.glob(module + '.lean.bak_*'))
    # Source closure for pre-existing bench imports; canonical binary snapshots are separate.
    seen = set()
    def visit(module):
        path = ROOT / (module.replace('.', '/') + '.lean')
        if module in seen or not path.exists():
            return
        seen.add(module)
        paths.add(path)
        compiled = path.with_suffix('.olean')
        if compiled.exists():
            paths.add(compiled)
        for imported in re.findall(r'^import\s+(\S+)', read_text(path), re.M):
            visit(imported)
    for module in MODULES:
        visit(module)
    for namespace in ['TGL', 'TGLExt']:
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in ['ORDEM006_DERIVACAO_PREVIA.md', 'ORDEM006_PARECER_FINAL.md',
                 'ORDEM005_MASSA_CONTROLES.json', 'verify_stage.ps1', 'audit_order006.py']:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('ORDEM006_DERIVACAO_PREVIA.md.bak_*'))
    paths.update(ROOT.glob('audit_order006.py.bak_*'))
    paths.update(ROOT.glob('ORDEM006_MANIFESTO.json.bak_*'))
    paths.update(DELIVERY.parent.glob(DELIVERY.name + '.bak_*'))
    for name in ['BisognanoWichmann', 'ContinuousModularZero', 'WedgeNet']:
        paths.add(ROOT / f'fontes/tgl_kernel/TGLExt/{name}.lean')
    files = [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': digest(p)}
             for p in sorted(paths) if p.is_file()]
    return {'status': 'REAL: byte audit and successful Lean compiler logs; not independent approval',
            'modules': records, 'theorems': sum(r['theorems'] for r in records),
            'definitions': sum(r['definitions'] for r in records), 'files': files,
            'dependency_limit': 'Local bench sources and copied TGL/TGLExt olean files pinned. '
              'External mathlib/toolchain are those resolved by verify_stage.ps1; this is not a portable package.'}

def deliver(data):
    lines = [
        '[REAL / DERIVED / OPEN] ENTREGA 006 — esperança local e tracial construída; invariância de sítios provada; extensão não tracial com parede nomeada.',
        '', 'A incorporação depende de auditoria independente da gerência. Nenhum original, memória canônica, um.py ou gate foi escrito.',
        '', '## Critérios, um a um', '',
        '| Item | Estatuto | Resultado |', '|---|---|---|',
        '| A.1 | PAGO (derivação); PAREDE NOMEADA (Lean periódico) | Derivação prévia, média vetorial/fraca, perfil ½ e correção: perfil não estacionário pode ser periódico. |',
        '| A.2 | PAGO local/tracial; PAREDE NOMEADA geral | into global para entradas locais; passagem via E_N formalizada; faltam operador médio e comutação da média com E_N. |',
        '| A.3 | PAGO local/tracial; NÃO PAGO não tracial global | fixes e ortho construídos nos escopos declarados. |',
        '| A.4 | PAGO | Restrição de qualquer contrato global ao pinching; incompatibilidade com esperança de andar quando P.w(0)≠½. Existência global não tracial não é pressuposta como conclusão. |',
        '| A.5 | PAGO no máximo entregue; PAREDE NOMEADA geral | Cinco módulos, habitante local e habitante original tracial; quatro obrigações suficientes nomeadas no parecer. |',
        '| A.6 | PAGO | Resultado matemático, sem escolha do operador; incorporação pela gerência após auditoria. |',
        '| B.1 | PAGO rede/caudas; PAREDE NOMEADA shift | Invariância para todo t e todo perfil; θ(M) condicionado à imagem ser a cauda. Nenhum shift normal foi fabricado. |',
        '| B.2 | PAGO após correção do enunciado | Formalmente não há compressão estrita. A condição fraca aceita igualdade. Não ciclicidade da cauda demonstrada por escrito, não em Lean. |',
        '| B.3 | PAGO | Inventário e custos das rotas alternativas no parecer, limitado às fontes examinadas. |',
        '| B.4 | NÃO PAGO / ramo positivo não obtido | Nenhum U(a) não trivial ou inclusão própria com vetor comum construída. |',
        '| B.5 | PAGO | Não há decisão matemática delegada ao operador; incorporação pela gerência. |',
        '| C.1 | PAGO como subsídio negativo | Condições dinâmicas escritas; normalização e borda não derivadas de morfologia/raio. |',
        '| C.2 | PAREDE NOMEADA | Seis classificações INDETERMINADAS; dados independentes ausentes e razões já conhecidas desde 005, sem fingir cegueira. |',
        '| C.3 | PAGO com escopo corrigido | Não há critério executável derivado das premissas atuais. Isso não prova impossibilidade universal nem extingue um enunciado condicional lógico. |',
        '| C.4 | PAGO | Sem alteração de um.py, veto GA, errata ou contorno. |',
        '| C.5 | PAGO | Decisões v98, errata e JOINT_CONTOUR continuam com o operador. |',
        '', '## Verificação', '',
        f"{data['theorems']} teoremas e {data['definitions']} definições construídas; cada declaração tem #print axioms. Logs finais sem sorryAx. Os axiomas efetivamente impressos estão abaixo e no manifesto, sem inferência por nome.", '',
        'Reprodução no ambiente desta bancada (dependências indicadas no verificador):', '', '```powershell',
        "Set-Location -LiteralPath 'C:\\IALD\\Central de Patentes'",
        r'python .\Chatgpt\audit_order006.py']
    for module in MODULES:
        lines.append(r'.\Chatgpt\verify_stage.ps1 -Module ' + module)
        lines.append('if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }')
    lines += ['```', '', 'As recompilações criam novos logs na bancada. O manifesto preserva as tentativas desta entrega, inclusive falhas; não as reclassifica como sucesso.', '', '```text']
    for record in data['modules']:
        for item in record['axioms']:
            lines.append(item['declaration'] + ': [' + ', '.join(item['axioms']) + ']')
    lines += ['```', '', '## Arquivos e custódia', '',
              f'Manifesto completo: `{MANIFEST}` — SHA256 `{digest(MANIFEST)}`.',
              f"O manifesto lista {len(data['files'])} arquivos por caminho absoluto, tamanho e SHA256 dos bytes, incluindo dependências locais compiladas, fontes da bancada, backups e logs de todas as tentativas.", '',
              '| Arquivo principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m + '.lean')) for m in MODULES}
    primary.update(str(ROOT / n) for n in ['ORDEM006_DERIVACAO_PREVIA.md', 'ORDEM006_PARECER_FINAL.md', 'audit_order006.py'])
    primary.update(r['final_log'] for r in data['modules'])
    for item in data['files']:
        if item['path'] in primary:
            lines.append(f"| `{item['path']}` | `{item['sha256']}` |")
    lines += ['', 'Não entregue: esperança global não tracial, integral periódica formalizada, prova Lean da não ciclicidade, translação de energia positiva não trivial, reconstrução gravitacional geral ou domínio observacional certificado da v98.', '',
              'A gerência pode auditar e incorporar a matemática. Só o operador decide v98, sua errata e JOINT_CONTOUR; esta entrega não antecipa essas decisões.']
    put_new(DELIVERY, '\n'.join(lines) + '\n')

if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        if MANIFEST.exists() or DELIVERY.exists():
            raise RuntimeError('Delivery already exists; refusing partial overwrite')
        data = inventory()
        put_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        deliver(data)
        print(json.dumps({'theorems': data['theorems'], 'definitions': data['definitions'],
                          'files': len(data['files']), 'delivery': str(DELIVERY),
                          'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        data = json.loads(read_text(MANIFEST))
        for item in data['files']:
            path = Path(item['path'])
            if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
                raise RuntimeError(f'Custody mismatch: {path}')
        current = inventory()
        if (current['theorems'], current['definitions']) != (data['theorems'], data['definitions']):
            raise RuntimeError('Declaration count changed')
        print(f"PASS: {len(data['files'])} byte hashes; {data['theorems']} theorems; "
              f"{data['definitions']} constructed definitions; all final axiom logs checked")
    else:
        raise SystemExit('Usage: audit_order006.py [--write]')
