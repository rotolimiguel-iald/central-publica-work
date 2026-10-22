from pathlib import Path
from datetime import datetime
import hashlib, json, re, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
OUT = ROOT / 'revisao'
NOW = datetime.now().astimezone()
TAG = NOW.strftime('%Y%m%d_%H%M%S_%f')
NAME = 'REVIEW_A1_FASE_RESOLVENTE_PARCIAL'
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
PAIRS = [
 ('V351ResolventPhaseFunctions', '20260914_095907_662952', 9),
 ('V351ResolventPhaseCalculus', '20260914_100402_294282', 10),
]

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def atomic(p, b):
    assert p.parent == OUT
    if p.exists():
        old = p.read_bytes()
        bk = p.with_name(p.name + '.bak_' + TAG)
        bk.write_bytes(old)
        assert bk.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + TAG)
    tmp.write_bytes(b)
    assert tmp.read_bytes() == b
    os.replace(tmp, p)

def axioms(txt):
    pat = r"(?m)^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    result = {}
    for m in re.finditer(pat, txt):
        assert m.group(1) not in result
        result[m.group(1)] = [x.strip() for x in (m.group(2) or '').split(',') if x.strip()]
    return result

mods = []
for stem, attempt, count in PAIRS:
    source = ROOT / 'kernel/TGLExt' / (stem + '.lean')
    obj = ROOT / 'build/TGLExt' / (stem + '.olean')
    folder = ROOT / 'attempts' / attempt
    run = json.loads((folder / 'run.json').read_text(encoding='utf-8-sig'))
    src = source.read_text(encoding='utf-8-sig')
    targets = re.findall(r'(?m)^#print axioms\s+(\S+)', src)
    stdout = (folder / 'stdout.txt').read_text(encoding='utf-8-sig')
    stderr = (folder / 'stderr.txt').read_text(encoding='utf-8-sig')
    actual = axioms(stdout)
    expected = {'TGLV350.Regular.' + n for n in targets}
    declarations = []
    for n in targets:
        m = re.search(r'(?m)^(def|theorem)\s+' + re.escape(n) + r'(?=\s|[(:])', src)
        assert m, n
        tail = src[m.start():]
        stop = tail.find(' :=')
        assert stop >= 0
        declarations.append({'name': n, 'kind': m.group(1), 'line': src[:m.start()].count('\n') + 1, 'statement': tail[:stop]})
    prohibited = re.findall(r'\b(?:sorry|axiom|native_decide|trustCompiler)\b', re.sub(r'/\-[\s\S]*?\-/|--[^\n]*', '', src))
    checks = {
        'returncode_zero': run['returncode'] == 0,
        'source_pin': pin(source)['sha256'] == run['source_sha256'],
        'attempt_snapshot_byte_equal': source.read_bytes() == (folder / (stem + '.lean')).read_bytes(),
        'exact_targets': len(targets) == count and set(actual) == expected,
        'trio_only': all(set(a) <= TRIO for a in actual.values()),
        'stderr_empty': not stderr.strip(),
        'no_warnings_or_errors': not re.search(r'(?i)\b(?:warning|error):', stdout + stderr),
        'no_prohibited_source_tokens': not prohibited,
    }
    history = []
    for path in sorted((ROOT / 'attempts').glob('*/' + stem + '.lean')):
        log = path.parent / 'run.json'
        if not log.exists() or path.parent.name == attempt:
            continue
        r = json.loads(log.read_text(encoding='utf-8-sig'))
        history.append({'attempt': path.parent.name, 'run': pin(log), 'returncode': r.get('returncode'), 'accepted_as_final': False})
    mods.append({'module': stem, 'source': pin(source), 'object_current': pin(obj), 'run': pin(folder/'run.json'),
        'snapshot': pin(folder/(stem+'.lean')), 'stdout': pin(folder/'stdout.txt'), 'stderr': pin(folder/'stderr.txt'),
        'checks': checks, 'axioms_from_author_final_stdout': actual, 'declarations': declarations,
        'section_hypotheses': re.findall(r'(?m)^variable.*(?:\n\s+\[.*)*', src),
        'toolchain_version_reported': run['lean_version'], 'toolchain_executable': pin(Path(run['command'][0])),
        'author_command': run['command'], 'author_lean_path': run['lean_path'], 'history_excluded': history})

dep_file = ROOT / 'DEPENDENCIAS_A1_FASE_RESOLVENTE.json'
deps = json.loads(dep_file.read_text(encoding='utf-8-sig'))
dep_results = []
for d in deps:
    s, o = pin(Path(d['source'])), pin(Path(d['object']))
    dep_results.append({'module': d['module'], 'source': s, 'object': o,
        'source_pin_match': s['sha256'] == d['source_sha256'],
        'object_pin_match': o['sha256'] == d['object_sha256']})

ficha_json = ROOT / 'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json'
ficha = json.loads(ficha_json.read_text(encoding='utf-8-sig'))
providers = [{'source': pin(Path(p['path'])), 'matches_ficha': pin(Path(p['path']))['sha256'] == p['sha256']} for p in ficha['providers']]
assert all(all(m['checks'].values()) for m in mods), 'Falha nos controles dos dois módulos'
assert all(d['source_pin_match'] and d['object_pin_match'] for d in dep_results), 'Falha em dependência pinada'
assert all(d['matches_ficha'] for d in providers), 'Falha no pin da ficha'

ml = ROOT.parent / 'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/Basic.lean'
ml_text = ml.read_text(encoding='utf-8-sig')
log_locations = {name: ml_text[:re.search(r'(?m)^theorem\s+' + name + r'\b', ml_text).start()].count('\n')+1 for name in ['log_neg_eq_log','continuousAt_log']}
f1, f2 = mods
rows = '\n'.join(f"| `{m['module']}` | `{m['source']['sha256']}` | `{m['object_current']['sha256']}` | {len(m['declarations'])} |" for m in mods)
decl_rows = '\n'.join(f"| `{d['name']}` | {d['kind']} | {m['module']}.lean:{d['line']} |" for m in mods for d in m['declarations'])
historical_count = sum(len(m['history_excluded']) for m in mods)
report = f'''# Revisão parcial A1 — funções e CFC da fase do resolvente

Data: {NOW.isoformat()}. **[REAL — inspeção independente somente leitura de dois fontes e evidências autorais]**. Escopo fechado desta leitura: **19 declarações = 9 + 10, quatro definições e quinze teoremas**. Nenhum P0, P1 ou P2 identificado nesse escopo.

**Limite da evidência:** não executei Lean nesta rodada, em respeito à solicitação de revisão somente leitura. Os dois rc0 e os 19 relatórios de axiomas são das execuções autorais identificadas abaixo, relidos e confrontados por script independente. Não há nova recompilação/auditor Lean próprio a reivindicar. A toolchain é a mesma nos dois comandos autorais ({f1['toolchain_version_reported']}); seu executável foi relido e pinado no JSON. O terceiro módulo, continuidade dos operadores e especialização ao T do peso ficam fora deste parecer.

| Módulo | SHA256 fonte corrente | SHA256 olean corrente | Alvos |
|---|---|---|---:|
{rows}

Os snapshots das tentativas finais são byte a byte iguais às fontes atuais. Tentativas aceitas para leitura: `{PAIRS[0][1]}` e `{PAIRS[1][1]}`. Ambos os run.json têm rc0, stderr vazio, stdout sem warning/error e exatamente os nomes esperados; todos os 19 conjuntos de axiomas estão no trio `propext`, `Classical.choice`, `Quot.sound`. Foram identificadas {historical_count} tentativas anteriores com snapshots dos mesmos módulos; seus códigos constam do JSON e nenhuma foi usada como aceite final. O hash do olean corrente foi medido; run.json não fornece um hash histórico do binário para confronto, logo não alego comparação com um olean independente ou com snapshot binário da tentativa.

## Significado e hipóteses

1. **Functions:** b(x)=x(1−x) e g(t,x)=b(x)·exp(i·t·Real.log((1−x)/x)). Os sete teoremas são universais em parâmetros reais, sem pressupor 0≤x≤1. As identidades de norma, tempo zero, soma, estrela e Gram estão orientadas corretamente. A continuidade demonstrada é conjunta em ℝ×ℝ, portanto fornece também a continuidade global em x para cada t.

2. **Continuidade global:** a implementação dispensa corretamente a extensão por zero sugerida como opção na consulta. Mathlib define o log real de número negativo como log do módulo, e o de zero como zero. Fora de x=0,1, o quociente é não nulo e `Real.continuousAt_log` se aplica sem exigir positividade. Nas pontas, ||g(t,x)||=||b(x)||→0 controla qualquer variação de t. Não se atribui continuidade à fase não amortecida. O comportamento escolhido fora de [0,1] não afeta a interpretação futura para um resolvente positivo contrativo. Referências: `{ml}` linhas {log_locations['log_neg_eq_log']} e {log_locations['continuousAt_log']}, hash no JSON.

3. **Calculus:** H está declarado como `Type`, com `NormedAddCommGroup H`, `InnerProductSpace ℂ H` e `CompleteSpace H`. Não há SiteProfile nem escolha de outro peso nesta camada genérica. T é um operador complexo limitado em H. C_t é efetivamente `cfc (fun z : ℂ => g(t,z.re)) T`; a função é contínua complexa, não holomorfa, que é precisamente o requisito do CFC contínuo utilizado.

4. **Hipóteses por resultado:** identificação de b(T), tempo zero, produto e Gram recebem `IsSelfAdjoint T`; positividade de b(T), identificação do módulo e identidade das normas vetoriais recebem `0≤T` e `T≤1`. `resolventPhaseOperator_star` é formulado para todo T, conforme a operação CFC total da biblioteca; isso não amplia os demais resultados a T arbitrário. Injetividade de T ou de 1−T **não é premissa nem conclusão deste par de módulos**.

5. O resultado é C_s C_t=b(T)C_(s+t), C_0=b(T) e C_t* C_t=b(T)²; não é ainda a lei de um grupo unitário. A mesma lei de produto com (t,−t), combinada com estrela, também fornece C_t C_t*=b(T)² por derivação curta, ainda não como alvo separado. A igualdade `boundedMapModulus C_t=b(T)` usa corretamente positividade de b(T) e `CFC.sqrt_mul_self`. `resolventPhaseOperator_norm` é igualdade de **normas de vetores**, para cada x, não uma alegação de ||C_t||=1.

6. Casos T=0 ou T=I fazem b(T)=C_t=0 e não contradizem os teoremas. Seriam incompatíveis com concluir unitariedade nesta camada; tal conclusão não está no código. A aplicação futura à fase de Δ precisa pagar as duas injetividades/imagem densa. O sinal +it log((1−x)/x) coincide com λ^it quando x=(1+λ)^−1, λ>0. Nenhum gap ou inversa limitada de b(T) é introduzido.

## Proveniência e fronteira

Li integralmente os dois fontes e a ficha MD/JSON. O script relê os pares fonte/objeto das **{len(deps)} entradas** de DEPENDENCIAS_A1_FASE_RESOLVENTE.json: todos correspondem aos pins declarados. Isso verifica bytes, não recompila nem reanalisa matematicamente as {len(deps)} dependências. Os oito fornecedores listados na ficha também correspondem aos hashes lidos. As fontes novas não contêm comandos `axiom`, `sorry`, `native_decide` ou `trustCompiler`, segundo inspeção e busca independente; a ausência de axiomas proibidos foi conferida também no stdout final.

A ficha anterior ao código conserva corretamente o alvo mais amplo como OPEN e separa construção unitária, grupo, continuidade forte e identificação da ação. Esses pagamentos não são atribuídos aos 19 alvos. Não há identificação nova com scalarTomitaSquare, modularidade/KMS, traço, predual completo ou promoção de gate. A1(b) continua **[OPEN]**. Originais, fontes, objetos autorais, monólito e memórias não foram modificados ou executados; apenas este relatório, script e evidência própria em revisao foram escritos.

## Inventário exato dos alvos

Namespace de todos: `TGLV350.Regular`. Enunciados completos extraídos da fonte, hipóteses de seção, comandos, hashes de streams e mapa de axiomas estão no JSON acompanhante.

| Declaração | Tipo | Locador |
|---|---|---|
{decl_rows}
'''
report_path = OUT / (NAME + '.md')
atomic(report_path, report.encode('utf-8'))
evidence = {'time': NOW.isoformat(), 'status': 'READONLY_PARTIAL_19__NO_P0_P1_P2__NO_INDEPENDENT_REBUILD',
    'findings': [], 'P0': 0, 'P1': 0, 'P2': 0, 'report': pin(report_path), 'modules': mods,
    'dependency_manifest': pin(dep_file), 'dependencies': dep_results,
    'ficha': [pin(ROOT/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md'), pin(ficha_json)], 'providers': providers,
    'mathlib_log': {'pin': pin(ml), 'locations': log_locations},
    'independent_compilations': 0, 'author_sources_modified': False, 'monolith_executed': False,
    'memory_written': False, 'third_module_read': False, 'A1_b': 'OPEN'}
atomic(OUT / (NAME + '.json'), (json.dumps(evidence, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps({'report': str(report_path), 'report_sha256': pin(report_path)['sha256'],
    'count': sum(len(m['declarations']) for m in mods), 'dependencies': len(deps),
    'history': [(m['module'],[(h['attempt'],h['returncode']) for h in m['history_excluded']]) for m in mods]}, ensure_ascii=False))
