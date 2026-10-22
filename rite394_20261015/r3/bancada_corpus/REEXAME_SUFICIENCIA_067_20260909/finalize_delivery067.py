from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
DIRS = [
    'COARSE_GRAINING_VARIACIONAL_LIVRE_20260909_212902_6343960',
    'ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751',
    'CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498',
    'REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531',
    'MODOS_TENSORIAIS_EXATOS_20260909',
    'HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912',
    'REVISAO_COMPOSICAO_HADAMARD_20260909_214530',
]
pins = {}
checks = []

def pin(path):
    path = path.resolve()
    data = path.read_bytes()
    value = {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if value['path'] in pins:
        assert pins[value['path']] == value, 'Input changed: ' + str(path)
    pins[value['path']] = value
    return value

def check(name, condition, detail=None):
    row = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    assert condition, row

def load(path):
    pin(path)
    return json.loads(path.read_text(encoding='utf-8-sig'))

def new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and data
    tmp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    tmp.rename(path)
    assert path.read_bytes() == data
    return pin(path)

def new_text(path, value):
    return new(path, value.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))

def validate_recorded_pins(obj, source, locator='root'):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(obj.get('sha256', ''))):
            path = Path(obj['path'])
            check('absolute_recorded_pin:' + source + ':' + locator, path.is_absolute())
            current = pin(path)
            check('recorded_pin:' + source + ':' + locator,
                  current['sha256'] == obj['sha256'] and ('bytes' not in obj or current['bytes'] == obj['bytes']),
                  current['path'])
        for key, value in obj.items():
            validate_recorded_pins(value, source, locator + '.' + key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            validate_recorded_pins(value, source, locator + '[' + str(index) + ']')

snapshot = load(OUT / 'ESTADO_CANONICO_067.json')
check('canonical_four_unchanged_from066', len(snapshot['comparison_with_delivery066']) == 4 and all(x['unchanged'] for x in snapshot['comparison_with_delivery066']))
check('canonical_seal_pin', snapshot['seal_um_hash_matches'])
check('canonical_presence', snapshot['present'] == 77 and len(snapshot['absent']) == 21 and len(snapshot['modules']) == 98)
validate_recorded_pins(snapshot['pins'], 'current_snapshot')
previous = load(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json')
check('pending_matches066', snapshot['absent'] == previous['pending_canonical_modules'])
validate_recorded_pins(previous['working_copy'], 'working_copy066')
pin(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/MANIFESTO_ENTREGA_066.json')

for folder in DIRS:
    for path in sorted((ROOT / folder).iterdir()):
        if path.is_file():
            pin(path)
            if path.suffix.lower() == '.json':
                validate_recorded_pins(load(path), folder + '/' + path.name)

cas_specs = [
    (ROOT / DIRS[4] / 'VERIFICACAO_CARTA_LIVRE.json', 84),
    (ROOT / DIRS[3] / 'VERIFICACAO_REDUCAO.json', 17),
    (ROOT / DIRS[4] / 'VERIFICACAO_MODOS_TT.json', 12),
]
cas = []
for path, expected in cas_specs:
    obj = load(path)
    rows = list(obj['checks'].values()) if isinstance(obj['checks'], dict) else obj['checks']
    check('cas_count:' + path.name, len(rows) == expected)
    check('cas_pass:' + path.name, all(row.get('passed', row.get('pass', False)) is True and row.get('residual') == '0' for row in rows))
    check('cas_scope:' + path.name, 'NOT_LEAN' in obj['status'])
    cas.append({'receipt': pin(path), 'exact_controls': len(rows), 'scope': obj['status']})
check('cas_total', sum(x['exact_controls'] for x in cas) == 113)

report = OUT / 'REEXAME_SUFICIENCIA.md'
pin(report)
for index, target in enumerate(re.findall(r'\]\(<(C:/[^>]+)>\)', report.read_text(encoding='utf-8'))):
    check('report_link:' + str(index), Path(target).is_file(), target)

review_note = ROOT / DIRS[6] / 'REVISAO_MATEMATICA_PROPRIA.md'
sign_note = ROOT / DIRS[2] / 'CONVENCAO_SINAL_E_TRANSPORTE.md'
review_pin, sign_pin = pin(review_note), pin(sign_note)
new_text(OUT / 'ADENDO_REVISAO_E_CONVENCOES.md', f'''# Revisão final e convenções da entrega 067

[DERIVED — revisão escrita] A raiz leu integralmente as notas livre, linearizada, S/V, TT, Hadamard, sinal e revisão própria. Os contratos e as contas examinados sustentam o enunciado local/linear delimitado, com os resultados de literatura importados explicitamente. Isso não é uma revisão externa humana nem compilação Lean.

A [revisão da composição](<{review_note.as_posix()}>) acrescenta a prova de alcance dos testes: em calibre de Donder, para θ zero no passado e um no futuro, F=H(θv) é compacto e invariante; E_gf F=v−K E_Q C(θv). Portanto cada classe física de solução é atingida. O autor dessa revisão construiu S/V; sua revisão independente incide sobre a composição Hadamard e TT, não constitui segunda autoria independente de S/V. A raiz e o autor da composição também leram S/V.

A [convenção de sinal](<{sign_note.as_posix()}>) fixa C=c, S_phys=−S_old e S_P,phys=S_phys∘Φ. H, corrente e forma simplética acompanham o mesmo sinal; λ_phys=c λ_geom quando explicitado. A composição quântica usa a forma física, sem identificar Ω com −Ω.

O transporte ao representante probabilístico permanece local e exige o mesmo domínio, grupo de gauge e condições de contorno. Não se apresenta a restrição do estado global I×S³ como um teorema automático para qualquer álgebra local definida de outra maneira. Uma parametrização probabilística global e a positividade operatorial não linear continuam abertas.

As fontes foram novamente medidas no manifesto final. Nenhuma nota congelada foi editada.
''')

created = datetime.now(timezone.utc).isoformat()
canonical = next(p for p in snapshot['pins'] if p['path'].endswith('/Nós/um.py'))
result = {
    'status': 'DELIVERY_067_WRITTEN_CLASSICAL_LOCAL_AND_PHYSICAL_LINEAR_QUANTUM_PROGRESS__GENERAL_INTERACTING_QG_OPEN',
    'created_utc': created, 'canonical': canonical,
    'canonical_unchanged_from066': True, 'canonical_modules_present': 77,
    'pending_canonical_modules': snapshot['absent'],
    'previous_benchmark': {'modules': 98, 'theorems': previous['accumulated']['theorems'], 'declarations': previous['accumulated']['total'], 'working_copy': previous['working_copy'], 'new_run_this_delivery': False},
    'new_lean_modules': 0, 'new_lean_theorems': 0,
    'new_exact_symbolic_controls': 113, 'cas': cas,
    'written_results': [
        'Grouped same-data metric/sigma representation with explicit free block and local joint-variation right inverse',
        'Local classical variational equivalence conditional on adopted Einstein-sigma action and representation inputs',
        'Restricted Hessian factorization and support-preserving linearized/symplectic correspondence with explicit boundary terms',
        'Complete scalar/vector/tensor reduction on specified compact-Cauchy Einstein-sigma background',
        'Exact modes, positive physical quasifree covariance, CCR on gauge-invariant quotient and microlocal representative',
        'Explicit time-cutoff proof of invariant-test surjectivity modulo gauge',
        'Action-sign matching for local probabilistic transport'
    ],
    'remaining': [
        'Physical adoption or derivation of correspondence/action and global/fixed-selected-clock domain',
        'Matter/general-background extension to claimed scope',
        'Strong gauge/ghost propagator construction for nonlinear observables',
        'Interacting quantum dynamics, quantum master identities and possible anomalies',
        'Chosen UV route and counterterm/limit control',
        'Global probabilistic charts, nonlinear integrability and operator positivity when claimed',
        'Port 21 pending compiled modules and formalize current written proofs without promoting CAS counts'
    ],
    'um_executed_or_imported': False, 'originals_written': False, 'nature_tests_run': False,
    'canonical_gate_modified': False, 'goal_complete': False,
    'review_scope': 'Root reviews plus bounded cross-reviews; no external or operator approval claimed.'
}
new(OUT / 'RESULTADO_ENTREGA_067.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

new_text(OUT / 'MEMORIA_DE_TRABALHO_067.md', f'''# Memória local — entrega 067 — {created}

[REAL] Canonical v338 unchanged by fresh four-artifact byte comparison; 77/98 benchmark leaves present, 21 pending. The prior integration98 remains frozen. No um.py was imported/executed and no canonical memory was modified. Source pins and pending names are in RESULTADO_ENTREGA_067.json.

[DERIVED] Grouped probabilities retain conditionals and give explicit AR=Id. Local free realization uses a sufficient 429-category alphabet and an explicit15-category normal block. Fixed clocks require the stated positive residual; freely chosen slow clocks give general local realization. Einstein-sigma action/partition are explicit inputs. Variational converse closes locally in this class; the old five-category pure-gauge result/counterexample remain valid.

[DERIVED] B=A*HA for restricted sigma Hessian. AR implies R*A*=Id, linear solution/gauge correspondence and exact on-shell current transport with boundary terms. Physical action sign is fixed by the new convention note. No global positive probability chart or quantum probability-operator positivity follows automatically.

[DERIVED + KNOWN] On g=dr²−4cos²(r/2)γ, φ=id, κc=4, Λ=3/4, c>0 and I⊂(0,π), all S/V/TT physical ℓ≥2 modes have positive kinetic terms and exact Darboux modes. Physical quotient has explicit positive quasifree covariance, CCR and oriented microlocal representative. Gauge/ghost completion for nonlinear functionals remains separate. Time-cutoff review proves invariant-test reachability modulo gauge.

[REAL] 113 exact CAS controls:84 free chart,17 S/V,12 TT. Zero new Lean declarations/compilations this delivery. Written analytic theorems are not CAS results.

[OPEN] General interacting quantum gravity, anomalies, claimed UV route, global/fixed-data physical correspondence, nonlinear integrability and formal incorporation. Goal remains active; this is a progress turn, not blocked. All new outputs and tunnel note are within Chatgpt. Originals and canonical Atlas/index/lineage remain read-only under the operator's instruction.
''')

new_text(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_067.md', '''# Adendo local ao caminho de suficiência — entrega 067

Registro → fase/ramo completos: resultados existentes preservados.

Dados finos agrupados → (g,φ) → AR=Id → ação Einstein–sigma adotada → equivalência variacional local: demonstração escrita agora disponível. Escolha física dos dados/ação e alcance global não são deduzidos da normalização.

Representante livre on-shell → B=A*HA → equivalência linear e simplética nas mesmas condições de fronteira: demonstração escrita disponível. O sinal físico da ação foi explicitamente casado.

Fundo curvo específico → redução completa S/V/TT → modos Darboux exatos → covariância positiva física + CCR + representante microlocal: demonstração escrita disponível. A passagem probabilística é local/condicionada ao mesmo contrato de álgebra.

Próximo caminho crítico: transporte forte gauge/ghost para funcionais não lineares; teoria quântica interagente e identidades/anomalias; tratamento da rota UV. Em paralelo, portar21 módulos e formalizar as notas novas. Não reabrir H3 interno, ramo/fase ou ausência de falsificadores; não fechar a teoria geral por contagens de testes.

Este é um adendo novo em Chatgpt. Não altera nem bifurca o Atlas canônico.
''')

tunnel = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_067_ESPONTANEA_dinamica_livre_estado_quantico_linear.md'
tunnel_pin = new_text(tunnel, f'''# Entrega 067 — dinâmica livre local e estado físico linear

[DERIVED — demonstrações escritas; REAL — controles e hashes medidos] Há dois avanços em relação à entrega066: (1) construção de probabilidades agrupadas com inverso à direita da variação conjunta de métrica/matéria, dando equivalência variacional local sob a ação Einstein–sigma; (2) estado quase livre positivo do quociente físico linearizado no fundo curvo sigma especificado, com CCR e representante microlocal. Não há nova compilação Lean nesta entrega.

[Relatório completo](<{report.as_posix()}>) · [Resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_067.json').as_posix()}>) · [Convenção de sinal](<{sign_note.as_posix()}>) · [Revisão por corte temporal](<{review_note.as_posix()}>).

Canônico novamente lido: v338,77 dos98 módulos da bancada incorporados,21 pendentes. Programa/selo/manifesto/rodada coincidem em bytes com066. Nenhum um.py executado/importado. A integração98 é cópia histórica de bancada: portar deltas, jamais substituir a versão viva por ela.

O bloco livre explícito permite429 probabilidades finas como construção suficiente, preservando as condicionais. Relógio fixado exige residual positivo; relógio livre pode ser escolhido lento localmente. A ação e a partição são INPUT/POSTULATE. A limitação antiga de cinco categorias permanece válida.

No linearizado: B=A*HA, AR=Id, transporte de corrente com termos de fronteira. Para casar a quantização usar S_P=S_phys∘Φ, com S_phys=−EH+c sigma; não misturar os sinais globais das notas. No fundo I×S³,κc=4,Λ=3/4, os três setores têm modos exatos normalizados. Hadamard aqui significa estado físico linear no quociente, não matriz BRST completa para testes arbitrários.

Controles CAS:84+17+12=113 identidades exatas; isso não são113 teoremas Lean. Formalizar separadamente os contratos e não promover demonstrações escritas a flags de compilação. Interações quânticas, anomalias, UV, extensão global e positividade operatorial não linear permanecem abertas.

O manifesto MANIFESTO_ENTREGA_067.json na pasta do relatório registra os artefatos e seus pins após conferência. Nenhum original, Atlas, índice canônico ou gate foi alterado.
''')

for path in sorted(OUT.iterdir()):
    if path.is_file():
        pin(path)

for value in list(pins.values()):
    current = pin(Path(value['path']))
    check('stable_final:' + value['path'], current == value)

manifest = {
    'status': 'PASS_DOCUMENTARY_BYTE_AND_CAS_SCOPE__WRITTEN_MATHEMATICS_NOT_LEAN',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'files': sorted(pins.values(), key=lambda p: p['path']),
    'checks': checks, 'checks_total': len(checks), 'checks_passed': sum(c['passed'] for c in checks),
    'tunnel': tunnel_pin, 'new_lean_compilation': False, 'um_execution_or_import': False,
    'originals_written': False, 'goal_complete': False,
    'limits': 'Byte and CAS validation does not certify analytic proofs. Written mathematical results have explicitly scoped root and cross-reviews. Prior canonical runtime is referenced evidence; not rerun.'
}
manifest_pin = new(OUT / 'MANIFESTO_ENTREGA_067.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'status': manifest['status'], 'checks': manifest['checks_total'], 'passed': manifest['checks_passed'], 'files': len(manifest['files']), 'cas': 113, 'new_lean': 0, 'manifest': manifest_pin, 'report': pin(report), 'tunnel': tunnel_pin}, ensure_ascii=True))
