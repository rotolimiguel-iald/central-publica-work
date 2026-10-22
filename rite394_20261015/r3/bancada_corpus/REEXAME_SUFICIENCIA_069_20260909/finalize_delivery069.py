from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys


ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)
assert len(sys.argv) == 3, 'Supply the new heat review and report review folders.'
DIR_NAMES = [
    'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909',
    'ESPECIALIZACAO_EPSILON_SIGMA_069_20260909_224620_755674',
    'REGULARIDADE_KT_JATOS_20260909_224852',
    'CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553',
    'REVISAO_Q2_GRASSMANN_069_20260909_225502_703705',
    'REVISAO_NAO_ABSORCAO_069_20260909_225724',
    'REVISAO_KT_JATOS_069_20260909_230519_107163',
    'AUDITORIA_DOCUMENTAL_068_20260909_223634_356961',
]
directories = [ROOT / name for name in DIR_NAMES]
for argument in sys.argv[1:]:
    directory = Path(argument).resolve()
    assert directory.is_relative_to(ROOT) and directory.is_dir()
    directories.append(directory)

pins = {}
checks = []


def check(name, condition, detail=None):
    row = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    assert condition, row


def pin(path):
    path = path.resolve()
    data = path.read_bytes()
    entry = {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if entry['path'] in pins:
        assert pins[entry['path']] == entry, 'File changed: ' + str(path)
    pins[entry['path']] = entry
    return entry


def load(path):
    pin(path)
    return json.loads(path.read_text(encoding='utf-8-sig'))


def validate_recorded_pins(obj, source, locator='root'):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(obj.get('sha256', ''))):
            path = Path(obj['path'])
            check('absolute_pin:' + source + ':' + locator, path.is_absolute())
            measured = pin(path)
            check('pin:' + source + ':' + locator,
                  measured['sha256'] == obj['sha256'] and ('bytes' not in obj or measured['bytes'] == obj['bytes']),
                  measured['path'])
        for key, value in obj.items():
            validate_recorded_pins(value, source, locator + '.' + key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            validate_recorded_pins(value, source, locator + '[' + str(index) + ']')


def new_file(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and data
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    temporary.rename(path)
    assert path.read_bytes() == data
    return pin(path)


def new_text(path, value):
    return new_file(path, value.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))


def new_json(path, value):
    return new_file(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


snapshot = load(OUT / 'ESTADO_CANONICO_069.json')
check('canonical_snapshot_status', snapshot['status'] == 'READ_ONLY_STABLE_SNAPSHOT')
check('four_unchanged_from068', len(snapshot['comparison_with_delivery068']) == 4 and all(row['unchanged'] for row in snapshot['comparison_with_delivery068']))
check('seal_hash_matches', snapshot['seal_um_hash_matches'])
check('canonical_comparison_modules', snapshot['present'] == 77 and len(snapshot['absent']) == 21 and len(snapshot['modules']) == 98)
check('canonical_embedded_files', snapshot['embedded_files'] == 683)
validate_recorded_pins(snapshot['pins'], 'snapshot069')
previous = load(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json')
check('pending_modules_unchanged', snapshot['absent'] == previous['pending_canonical_modules'])
validate_recorded_pins(previous['working_copy'], 'historical_working_copy98')
pin(ROOT / 'REEXAME_SUFICIENCIA_068_20260909/MANIFESTO_ENTREGA_068.json')

for directory in directories:
    check('directory:' + directory.name, directory.is_dir())
    for path in sorted(directory.iterdir()):
        if path.is_file():
            pin(path)
            if path.suffix.lower() == '.json':
                validate_recorded_pins(load(path), directory.name + '/' + path.name)

cas = []
heat_directory = directories[3]
for filename, expected in [('VERIFICACAO_CALOR_COMPLETO.json', 23), ('VERIFICACAO_TRACOS_INVARIANTES.json', 8)]:
    path = heat_directory / filename
    receipt = load(path)
    rows = list(receipt['checks'].values()) if isinstance(receipt['checks'], dict) else receipt['checks']
    check('cas_count:' + filename, len(rows) == expected)
    check('cas_exact:' + filename, all(row.get('passed') is True and row.get('residual') == '0' for row in rows))
    check('cas_not_lean:' + filename, 'NOT_LEAN' in receipt['status'])
    cas.append({'receipt': pin(path), 'exact_controls': len(rows), 'scope': receipt['status']})
check('cas_total31', sum(item['exact_controls'] for item in cas) == 31)

report = OUT / 'REEXAME_SUFICIENCIA.md'
pin(report)
new_names = ['RESULTADO_ENTREGA_069.json', 'MEMORIA_DE_TRABALHO_069.md', 'DESENHO_DO_FECHAMENTO_ADENDO_069.md', 'ADENDO_REVISOES_E_ESCOPO_069.md', 'MANIFESTO_ENTREGA_069.json']
for name in new_names:
    check('new_destination:' + name, not (OUT / name).exists())
tunnel = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_069_ESPONTANEA_interacao_causal_c0_calor_completo.md'
check('new_tunnel_destination', not tunnel.exists() and tunnel.parent.is_dir())
for entry in list(pins.values()):
    check('stable_pre_write:' + entry['path'], pin(Path(entry['path'])) == entry)

created = datetime.now(timezone.utc).isoformat()
canonical = next(entry for entry in snapshot['pins'] if entry['path'].endswith('/Nós/um.py'))
result = {
    'status': 'DELIVERY_069_CAUSAL_INTERACTIONS_FORMAL_KT_AND_COUPLED_ONE_LOOP__QME_AND_UV_OPEN',
    'created_utc': created,
    'canonical': canonical,
    'canonical_unchanged_from068': True,
    'canonical_modules_present': 77,
    'pending_canonical_modules': snapshot['absent'],
    'previous_benchmark': {'modules': 98, 'working_copy': previous['working_copy'], 'new_run_this_delivery': False},
    'new_lean_modules': 0,
    'new_lean_compilations': 0,
    'new_exact_symbolic_controls': 31,
    'cas': cas,
    'written_results': [
        'Explicit graded Hessian, Grassmann reality, free BV action and nonlinear gauge-fixing dictionary for the existing coupled free data',
        'Q2: locally covariant renormalized time-ordered products and auxiliary interacting algebra, as formal EFT, with a consistent local anomalous insertion',
        'Natural polynomial EOM certificate for weak equality on all formal stationary Einstein-sigma jets, and ordinary KT resolution in the stated chart/class',
        'C0 characteristic consequence by combining that certificate with the previous Euler/Pontryagin argument; not full relative BRST cohomology',
        'Conditional filtered epsilon-specialization lemma and an explicit obstruction to automatic recentering at the physical nonconstant background',
        'Full coupled on-shell one-loop local heat coefficient with half boson rank13 minus one ghost pair rank4',
        'Nonabsorption into the original two-derivative parameters, modulo the specified EOM/current/characteristic class and normalized determinant prescription'
    ],
    'one_loop_background': {
        'definition': 'x=a**(-2), a=2*cos(r/2), phi=id, kappa*c=4, Lambda=3/4',
        'C4': '(7440*x**2+1616*x-211)/96',
        'includes_total_derivatives': True,
        'total_derivative_contribution': '5*x/4',
        'scope': 'On-shell local coefficient in the normalized differential determinant prescription; not full nonlocal action or unrestricted measure claim'
    },
    'remaining': [
        'Physical correspondence/action and reconstruction scope beyond the specified admissible classes and global background',
        'Direct admissible H^(1,4)(s_sigma|d), filtered cohomology contracts, local primitives, and renormalized quantum master equation at all formal orders',
        'Physical interacting cohomology and the state/positivity claims required by the intended theory',
        'Target/global cohomology, global anomalies and split/background independence in the claimed scope',
        'Renormalization conditions, higher-derivative EFT couplings and the chosen UV route/control',
        'Independent probability-field measure and vertical BRST if that separate quantization is claimed',
        'Port 21 prior modules and formalize new written results without promoting CAS or imported analytic contracts to Lean'
    ],
    'independent_internal_reviews': [directory.as_posix() for directory in directories[4:]],
    'originals_written': False,
    'um_executed_or_imported': False,
    'nature_tests_run': False,
    'canonical_gate_modified': False,
    'goal_complete': False,
    'limits': 'Written deductions and primary-source imports retain explicit contracts. Internal bounded reviews and documentary pins are distinct from external confirmation or Lean proof.'
}
new_json(OUT / 'RESULTADO_ENTREGA_069.json', result)

new_text(OUT / 'MEMORIA_DE_TRABALHO_069.md', f'''# Memória local de continuidade — entrega 069

Registro UTC: {created}. Documento novo da bancada Chatgpt; não copia nem substitui o Atlas. Fontes, revisões e pins completos estão no manifesto e resultado ao lado.

[REAL] Canônico igual aos quatro arquivos de068: v338,683 arquivos embutidos,77/98 módulos de comparação presentes,21 pendentes. Hashes relidos e conferidos, nenhum um.py executado/importado, nenhum original escrito, nenhum rito de natureza ou Lean novo. A cópia98 é histórica e não pode substituir v338. Fase/ramo, H3 interno e falsificadores existentes não foram reabertos.

[DERIVED] Dicionário Grassmann: J_slot=diag(1,1,1,-1), P_gr=L J_slot, G_gr=J_slot G_L. Não é o J modular. Ghost action barc Q c; s0barc=-b. Realificação W± conserva Ward/CCR/Hadamard e o estado físico anterior. Involução c*=c,barc*=-barc; diferencial real graduado. Férmion Psi=-barc(Ch-b/(2ell)). Auxiliar sem vértices internos de interação neste gauge, mas contatos preservados. Anticampos externos sem contrações. CME clássica, não QME satisfeita.

[DERIVED+KNOWN] Q2 agora fornecido: expansão direta gbar+t h,Exp_phibar(t xi), sistemas de ondas rank13/rank4, produtos temporais por extensão causal local covariante, liberdade EFT, álgebra auxiliar pelo limite adiabático algébrico. Hollands0705.3340 §3.5/Th2 paga multipletos; Fröb1803.10235 Th3/6/7 paga anomalia e consistência. Não usar somente o teorema escalar para toda a matriz. Inserções de laços podem ter zero/uma/duas pernas. Cutoffs não são removidos como limite de estado. A local=Ohbar, gh1; sa_N+d b_N0 é consistência. Q3=a_N=sB_N+dD_N ainda aberto.

[DERIVED] KT/C0: ImG_N=kerD_N, D_N onto; construção homogênea com Cauchy/Donder e normalização radial; cisões Lorentz equivariantes racionais, exprimíveis por contrações/volume. Equações E_N=G_N H_N+F_lower,tau_N=Box Y_N+J_lower. Noether inclui sigma. Coordenadas independentes z_N=Pi E_N,zeta_N=tau_N, inversa triangular polinomial. Toda anulação em jatos estacionários FORMAIS dá certificado natural no ideal de EOM por homotopia polinomial finita, com coeficientes suaves apenas no valor alvo. Nunca substituir por anulação apenas em FRW ou dados. Certificado com Euler/Pontryagin068 paga C0 característico nesta classe; delta KT não é delta|d nem s|d. Precisa manter normalidade/filtragem e globalização do alvo separados. Jentsch: usar Th1 e identidades universais3b;3a enuncia Euclidean. Constraints ADM já entre10EOMordem2; dependências prolongadas são Noether.

[DERIVED] Epsilon: no vácuo constante, lemma filtrado pode permitir especialização diagonal, condicionado à primitiva filtrada. No fundo phi=id o argumento não se transfere automaticamente. Contraexemplo com coeficientes (2m-1)!! impede recentering formal em ponto não zero; não é anomalia real do sigma. A convergência da métrica clássica não limita primitivas BRST. Seguir prova direta de H1_sigma; a expansão Exp já resolve apenas a apresentação perturbativa paraQ2.

[DERIVED+KNOWN] Calor completo: C4=half tr13 b4 -tr4 ghost b4. No fundo x=a^-2, C4=(7440x²+1616x-211)/96, incluindo divergências totais5x/4. Conexão/E do Jacobi, traços gerais e Bochner constam da nota e revisão. Medida normalizada separa fator ultralocal, auxiliar e rotação do modo conforme; não presumir multiplicatividade de determinantes, Wick global ou positividade não perturbativa. Coeficiente on-shell local, não ação completa dependente do estado. Não absorção: 1,R,Q e equivalências permitidas rendemA+Bx; C4''155. Requer operador4derivadas na classe O4 natural polinomial com correntes≤3 e prescrição indicada. Não exclui outras medidas, novos campos ou UV. Não confundir divergência ghost0 com anomalia ghost1.

[REAL] 31 novos controles CAS exatos23+8; zero Lean. Pareceres internos distintos para Q2/Grassmann,KT/C0,nãoabsorção,calor e relatório. Auditoria225/225 refere-se à entrega068, não nova prova069. Relatório e adendo fazem a correção ao lado das pendências históricas; nenhuma fonte congelada mudou.

[OPEN] Próximo caminho: H^(1,4)(s_sigma|d) no espaço admissível, primitivas com realidade/covariância, QME interagente ordem a ordem; depois setor/estado físico interagente e independência entre fundos/global. Renormalização finita e rota UV continuam próprias. Se quantificar P independentemente, faltam medida/BRST vertical. A correspondência física e extensão da reconstrução além do fundo/classe escolhidos permanecem contratos. Objetivo geral ativo.
''')

new_text(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_069.md', '''# Adendo local do caminho crítico — entrega 069

Registro completo → seleção → reconstruções condicionais e ação adotada → fundo global e equivalência variacional068 → estado físico067 e BRST livre068: preservar resultados e hipóteses.

BRST livre → dicionário Grassmann/BV069 → expansão direta por Exp → produtos temporais locais covariantes → álgebra auxiliar interagente e anomalia local consistente: Q2 disponível como EFT formal. Não manter “construir produtos temporais” como lacuna integral depois desta entrega.

Regularidade formal por jatos → certificado no ideal das equações → Euler/Pontryagin independentes modulo igualdade fraca formal: C0 característico disponível. A seta seguinte NÃO é automática: KT ordinário → cohomologia relativa H^(1,4)(s_sigma|d) exige contratos/normalidade/filtragem e análise própria.

H^(1,4)(s_sigma|d) → primitivas locais admissíveis → renormalização finita que remove a quebra → QME → setor físico interagente: caminho crítico ainda aberto. Epsilon-adic no vácuo constante não pode ser recentered por decreto no fundo phi=id. A expansão direta resolve a parametrização, não a cohomologia.

Jacobi completo → conexão e endomorfismo → tr13/ghost4 de b4 → C4x explícito → não absorção nos três parâmetros originais na classe declarada: disponível em069. Próximo elo: operadores EFT adicionais e condições finitas de renormalização. UV exige sua própria rota e controle; a contagem de potência é uma obrigação, não uma solução.

Em paralelo: alcance físico geral/correspondência adotada; questões globais do alvo e entre fundos; medida e BRST vertical de P se reivindicados; portar21 módulos prévios da bancada para o canônico e formalizar novas deduções. Zero Lean069,31CAS exatos; nenhum gate movido.
''')

heat_review = directories[-2]
report_review = directories[-1]
new_text(OUT / 'ADENDO_REVISOES_E_ESCOPO_069.md', f'''# Revisões e precisões ao lado — entrega 069

[DERIVED] A raiz leu as notas principais e os pareceres delimitados. A revisão Q2 examinou as convenções graduadas e reabriu as fontes de multipletos e Ward. A revisão KT conferiu a cisão em todas as ordens e explicitou o uso dos invariantes ortogonais e o alcance pseudo-riemanniano de Jentsch. A revisão de não absorção recalculou o teste FRW e classificou correntes na truncagem declarada, tomando C4 como entrada. A revisão do elo Jacobi/calor encontra-se em <{heat_review.as_posix()}>; é separada daquela revisão de não absorção. A revisão documental do relatório está em <{report_review.as_posix()}> e não é auditoria antecipada dos arquivos produzidos por este finalizador.

As notas congeladas de068 que mantinham produtos temporais e igualdade fraca/ideal inteiramente abertos recebem a precisão neste adendo:069 fornece Q2 no sistema/formalismo especificado e fornece o certificado KT/C0 na classe formal natural. Permanecem abertas a cohomologia relativa completa, a remoção da anomalia e a QME satisfeita. O resultado epsilon permanece condicional; sua especialização no fundo físico não foi demonstrada.

O coeficiente sigma externo de068 permanece válido no seu escopo;069 acrescenta o coeficiente diferencial local on-shell do sistema acoplado, com13bosons e ghostpair4. Sua prescrição de medida e modo conforme está declarada. A fonte quártica clássica068 não se torna, por isso, uma solução semiclassica com todos os novos operadores.

O relatório não substitui por “não falsificada” a prova dos requisitos ainda abertos, nem ignora os falsificadores já codificados. Os novos resultados são demonstrações escritas e importações analíticas com contratos; as revisões são internas, e os31CAS são controles enumerados. Pins não são provas analíticas e nenhuma nova bandeira de execução foi emitida.
''')

tunnel_pin = new_text(tunnel, f'''# Entrega069 — interações causais, regularidade formal e calor acoplado

[Reexame completo](<{report.as_posix()}>) · [Resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_069.json').as_posix()}>) · [Manifesto](<{(OUT / 'MANIFESTO_ENTREGA_069.json').as_posix()}>).

[REAL] Canônico relido igual a068: v338,77/98 módulos do conjunto comparado presentes,21 pendentes. Nenhum um.py executado/importado, original escrito, rito de natureza ou Lean novo. Portar somente deltas da cópia98 histórica; nunca substituir o programa vivo por essa base anterior.

[DERIVED+KNOWN] Entregas novas: dicionário Grassmann/BV e ação de gauge com sinais explícitos; Q2 com produtos temporais locais covariantes e álgebra auxiliar interagente formal, anomalia local consistente; certificado natural polinomial de igualdade fraca em jatos estacionários formais e KT ordinário, pagando o passo característicoC0; análise da especializaçãoepsilon e contraexemplo ao recentering automático; coeficiente completo diferencial local de uma volta métrica10+sigma3 e ghostpair4; necessidade de ampliar a ação2derivadas na classe/prescrição examinadas.

O coeficiente no fundo a=2cos(r/2),phi=id,kappa*c4,Lambda3/4,x=a^-2 é C4=(7440x²+1616x-211)/96, com divergências totais5x/4. A combinação é half tr13 b4 -tr4 ghost b4. Contorno conforme e fatores ultralocais separados; sem Wick global ou independência irrestrita da medida. Há31 controles CAS exatos23+8; zero Lean.

Contratos de integração indispensáveis: Q2 não é QME satisfeita; consistência sa_N+d b_N0 não é exatidão. C0/KT não é H1(s|d) completo. Igualdade fraca usa todos os jatos estacionários formais, não só FRW. Epsilon1/recentramento no fundo físico não foram pagos; usar expansão diretaExp paraQ2 e análise direta admissível paraQ3. Não absorção vale com correntes≤3 e contratermos≤4derivadas naturaisO4, moduloEOM/classescaracterísticas, na prescrição declarada; não é impossibilidade deUV ou de outra medida.

[OPEN] Primitivas admissíveis e QME em todas as ordens, setor/estado físico interagente, condições finitas de renormalização e rotaUV, escopo físico/correspondência, global/alvo e independência entre fundos. BRSTvertical/medida deP se quantizado independentemente. Não reabrir fase/ramo,H3interno ou falsificadores existentes.

Memória local e desenho atualizados em arquivos novos na pasta069. Atlas e memórias canônicas somente leitura. Revisões internas e fontes pinadas no manifesto; formalizar enunciados com hipóteses, sem promoverCAS/importações aLean. Objetivo geral ativo.
''')

for path in sorted(OUT.iterdir()):
    if path.is_file():
        pin(path)
for document in [report, tunnel]:
    for index, target in enumerate(re.findall(r'\]\(<(C:/[^>]+)>\)', document.read_text(encoding='utf-8'))):
        if target == (OUT / 'MANIFESTO_ENTREGA_069.json').as_posix():
            continue
        check('link:' + document.name + ':' + str(index), Path(target).is_file(), target)
for entry in list(pins.values()):
    check('stable_final:' + entry['path'], pin(Path(entry['path'])) == entry)

manifest = {
    'status': 'PASS_DOCUMENTARY_BYTE_AND_CAS_SCOPE__WRITTEN_MATHEMATICS_NOT_LEAN',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'files': sorted(pins.values(), key=lambda item: item['path']),
    'checks': checks,
    'checks_total': len(checks),
    'checks_passed': sum(row['passed'] for row in checks),
    'tunnel': tunnel_pin,
    'exact_symbolic_controls': 31,
    'new_lean_compilation': False,
    'um_execution_or_import': False,
    'originals_written': False,
    'goal_complete': False,
    'limits': 'Documentary checks include repeated pins and historical audit references; they are not counts of new mathematical theorems. CAS identities and written/internal-reviewed proofs retain distinct scopes. No new canonical execution or nature test.'
}
manifest_pin = new_json(OUT / 'MANIFESTO_ENTREGA_069.json', manifest)
print(json.dumps({'status': manifest['status'], 'checks': len(checks), 'passed': manifest['checks_passed'], 'files': len(manifest['files']), 'cas': 31, 'new_lean': 0, 'report': pin(report), 'manifest': manifest_pin, 'tunnel': tunnel_pin}, ensure_ascii=True))
