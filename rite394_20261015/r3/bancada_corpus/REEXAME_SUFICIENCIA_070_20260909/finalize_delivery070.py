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
assert len(sys.argv) == 2, 'Supply the final report review directory.'
review_directory = Path(sys.argv[1]).resolve()
assert review_directory.is_relative_to(ROOT) and review_directory.is_dir()
names = [
    'EQUIVALENCIA_BV_METRICA_VIELBEIN_070_20260909',
    'NORMALIDADE_RELATIVA_070_20260909_233414',
    'TOPOLOGIA_BRST_SIGMA_070_20260909_233042_647697',
    'REDUCAO_ON_SHELL_RG_070_20260909_232623_681687',
    'REVISAO_EQUIVALENCIA_BV_070_20260909_233408_420695',
    'REVISAO_ADMISSIBILIDADE_070_20260909_233732_295574',
    'REVISAO_REDUCAO_RG_070_20260909_233431_384880',
]
directories = [ROOT / name for name in names] + [review_directory]
pins = {}
checks = []


def pin(path):
    path = path.resolve()
    raw = path.read_bytes()
    entry = {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    if entry['path'] in pins:
        assert pins[entry['path']] == entry, 'Source changed: ' + str(path)
    pins[entry['path']] = entry
    return entry


def check(name, condition, detail=None):
    item = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        item['detail'] = detail
    checks.append(item)
    assert condition, item


def load(path):
    pin(path)
    return json.loads(path.read_text(encoding='utf-8-sig'))


def recorded_pins(value, origin, locator='root'):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(value.get('sha256', ''))):
            path = Path(value['path'])
            check('absolute_pin:' + origin + ':' + locator, path.is_absolute())
            actual = pin(path)
            check('recorded_pin:' + origin + ':' + locator,
                  actual['sha256'] == value['sha256'] and ('bytes' not in value or actual['bytes'] == value['bytes']),
                  actual['path'])
        for key, child in value.items():
            recorded_pins(child, origin, locator + '.' + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            recorded_pins(child, origin, locator + '[' + str(index) + ']')


def new_bytes(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    return pin(path)


def new_json(path, value):
    return new_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def new_text(path, value):
    return new_bytes(path, value.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))


snapshot = load(OUT / 'ESTADO_CANONICO_070.json')
check('snapshot_stable', snapshot['status'] == 'READ_ONLY_STABLE_SNAPSHOT' and snapshot['all_read_sources_unchanged'])
check('canonical_four_unchanged_from069', len(snapshot['comparison_with_delivery069']) == 4 and all(x['unchanged'] for x in snapshot['comparison_with_delivery069']))
check('canonical_seal_match', snapshot['seal_um_hash_matches'])
check('canonical_presence', snapshot['present'] == 77 and len(snapshot['absent']) == 21 and len(snapshot['modules']) == 98 and snapshot['embedded_files'] == 683)
recorded_pins(snapshot['pins'], 'snapshot070')
prior_result = load(ROOT / 'REEXAME_SUFICIENCIA_069_20260909/RESULTADO_ENTREGA_069.json')
check('pending_modules_unchanged', snapshot['absent'] == prior_result['pending_canonical_modules'])
recorded_pins(prior_result['previous_benchmark']['working_copy'], 'historical_working_copy98')
prior_manifest_pin = pin(ROOT / 'REEXAME_SUFICIENCIA_069_20260909/MANIFESTO_ENTREGA_069.json')
prior_audit_note = pin(ROOT / 'AUDITORIA_DOCUMENTAL_069_20260909_231554_923421/PARECER_DOCUMENTAL_069.md')

for directory in directories:
    check('directory:' + directory.name, directory.is_dir())
    for path in sorted(directory.iterdir()):
        if path.is_file():
            pin(path)
            if path.suffix.lower() == '.json':
                recorded_pins(load(path), directory.name + '/' + path.name)

cas_path = directories[3] / 'VERIFICACAO_REDUCAO_RG.json'
cas = load(cas_path)
cas_rows = list(cas['checks'].values()) if isinstance(cas['checks'], dict) else cas['checks']
check('cas_count16', len(cas_rows) == 16)
check('cas_exact_pass', all(row.get('passed') is True and row.get('residual') == '0' for row in cas_rows))
check('cas_scope_not_lean', 'NOT_LEAN' in cas['status'])

report = OUT / 'REEXAME_SUFICIENCIA.md'
pin(report)
tunnel = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_070_ESPONTANEA_cohomologia_relativa_e_rg.md'
destinations = [OUT / name for name in ['RESULTADO_ENTREGA_070.json', 'MEMORIA_DE_TRABALHO_070.md', 'DESENHO_DO_FECHAMENTO_ADENDO_070.md', 'ADENDO_REVISOES_070.md', 'MANIFESTO_ENTREGA_070.json']] + [tunnel]
for path in destinations:
    check('new_destination:' + path.name, not path.exists() and path.parent.is_dir())
for entry in list(pins.values()):
    check('stable_pre_write:' + entry['path'], pin(Path(entry['path'])) == entry)

created = datetime.now(timezone.utc).isoformat()
canonical = next(entry for entry in snapshot['pins'] if entry['path'].endswith('/Nós/um.py'))
result = {
    'status': 'DELIVERY_070_FORMAL_BV_RELATIVE_REDUCTION_AND_RG__SMOOTH_ANOMALY_CONTRACT_OPEN',
    'created_utc': created,
    'canonical': canonical,
    'canonical_unchanged_from069': True,
    'canonical_modules_present': snapshot['present'],
    'pending_canonical_modules': snapshot['absent'],
    'previous_benchmark': prior_result['previous_benchmark'],
    'prior_manifest': prior_manifest_pin,
    'prior_audit_note': prior_audit_note,
    'new_lean_modules': 0,
    'new_lean_compilations': 0,
    'new_exact_symbolic_controls': 16,
    'cas': {'receipt': pin(cas_path), 'count': 16, 'scope': cas['status'], 'previous31_rerun': False},
    'written_results': [
        'Explicit local formal BV equivalence between metric and vielbein, including ghosts, antifields and relative cohomology modulo horizontal d',
        'Target volume descent of total degree3, explicit primitive for the mixed target2-form/gravitational-descent candidate, and smooth-coefficient Lie reduction',
        'Finite ghost-degree5 reduction to the precisely stated covariant characteristic cohomology degree2 contract',
        'Finite derivative-weight transport from Lambda0 to fixed Lambda under a controlled base relative primitive',
        'Direct absence of universal Einstein-sigma reducibility parameters using dphi and dQ, without adding inverse-gradient coefficients',
        'Normality and antifield-degree2 relative vanishing in the stated formal completion, with the smooth primitive problem retained',
        'Explicit on-shell C4 reduction, EOM/divergence certificate and chosen field redefinition, one-loop logarithmic RG in declared conventions',
        'Counterterm admissibility distinctions, explicit background transgression and conditional compact averaging of existing primitives'
    ],
    'relative_contract': {
        'smooth_open': 'M2 quadratic in field antifields: delta M2+d b1=0 implies M2=delta c3+d e2 in the smooth natural class, together with covariantization; or a direct smooth H2_char_cov homotopy',
        'formal_paid': 'H4_2(delta_Lambda|d) in the stated completion, polynomial in differentiated jets with bounded K and formal in undifferentiated values',
        'not_inferred': 'Formal vanishing is not smooth global vanishing or a primitive for the actual anomaly without the remaining class/descent/admissibility contracts'
    },
    'renormalization': {
        'A1': '-13*s**2/16+7*s/6+1/6',
        'A2': '27*s**2/8-s+1/3',
        'AB': '15*s**2/16+5*s/2+5/6',
        's4': {'A1': '-49/6', 'A2': '151/3', 'AB': '155/6'},
        'euclidean_bare_convention': 'g_B^E=g_R^E(mu)+hbar/(4*pi)^2*A*log(rho^2/mu^2)',
        'euclidean_beta': '2*hbar/(4*pi)^2*A at one loop',
        'lorentzian_conversion': 't_L=-i*tau_E;g_L^W=-g_E;S_E=-i*S_L^W;Lambda_E=-Lambda_L;g_Q2^E=-b1;g_W2^E=-b2',
        'lorentzian_beta_B_s4': '-155*hbar/(3*(4*pi)^2)',
        'reduced_explicit_divergence_background': '3*x/4',
        'previous_explicit_divergence_before_Bochner': '5*x/4',
        'same_total_C4': '(7440*x**2+1616*x-211)/96',
        'finite_values_fixed': False,
        'unique_off_shell_backreaction_claimed': False
    },
    'remaining': [
        'Smooth natural relative primitive/covariant characteristic degree2 and compatible descent/globalization in the Q2 admissible algebra',
        'Remove actual local anomalies by admissible finite renormalizations and satisfy the quantum master equation at all formal orders',
        'Physical interacting cohomology and state/positivity requirements',
        'Background/split independence and global or discrete anomaly questions in the intended scope',
        'Finite renormalization conditions and the chosen UV completion/control',
        'Physical correspondence/action and gravitational reconstruction scope beyond the constructed classes/background',
        'Independent probability-field measure/vertical BRST if claimed, and port the pending21 modules plus new formalizations'
    ],
    'originals_written': False,
    'um_executed_or_imported': False,
    'nature_tests_run': False,
    'canonical_gate_modified': False,
    'goal_complete': False,
    'review_scope': 'Written results have separately authored bounded internal reviews. Byte checks and enumerated CAS controls do not certify the full analytic or physical objective.'
}
new_json(OUT / 'RESULTADO_ENTREGA_070.json', result)

new_text(OUT / 'MEMORIA_DE_TRABALHO_070.md', f'''# Memória local de continuidade — entrega 070

Registro UTC {created}. Esta é uma nota de continuidade da bancada. O relatório e o resultado estruturado ao lado fornecem as referências completas; o manifesto registra os bytes das fontes. O Atlas permanece como fonte canônica de consulta.

[REAL] Os quatro artefatos canônicos conferem com a captura 069. O programa v338 contém 683 arquivos embutidos. Dos 98 módulos do conjunto comparado, 77 estão presentes e 21 continuam pendentes. Nenhum um.py foi executado ou importado. Originais, gates e ritos permanecem intactos. A cópia histórica de 98 módulos serve para portar deltas ao programa vivo, sem substituí-lo. Fase e ramo, seletor, H3 interno e falsificadores existentes permanecem preservados. As contagens da auditoria 069 são históricas: 105 arquivos, 560 condições repetíveis, 6 condições históricas e 14 verificações adicionais.

[DERIVED] Equivalência BV formal: S=sqrt(gbar^-1 g) e e=exp(chi) ebar S. A raiz é uma série formal local em assinatura indefinida. A variável upsilon=s chi é invertivelmente relacionada ao ghost Lorentz, com a compensação de difeomorfismos mantida. O levantamento cotangente local aos antifields separa Snew=Smetric+chi*upsilon. Os pares (chi,upsilon) e (upsilon*,p=s upsilon*) são contráteis também módulo d. Sob mudança externa Omega(x), o ghost antigo obedece cL'=Ad(Omega)cL−(Lie_C Omega)Omega^-1; chi e upsilon transformam adjuntamente. Naturalidade simultânea nos dados de fundo não demonstra independência de fundo.

[DERIVED] Topologia e redução de graus: o volume de S³ tem descida de grau total 3. Para uma 2-forma fechada no alvo fixo, Hodge fornece uma primitiva global alpha1. A identidade D(alpha1 q3)=Omega2 q3 decorre de alpha1 P4 ter cinco direções horizontais em dimensão quatro. A primitiva pode conter Chern–Simons e pertence à classe explicitada na nota. A cohomologia de Lie relevante tem graus 0, 3 e 6. Em ghost total 5, somente o nível xi² multiplicando uma classe de grau 3 pode sobreviver; H²_char,cov=0 permite eliminá-lo por uma indução finita. Coeficientes suaves no alvo são compatíveis com a etapa de Lie. Uma partição de unidade comuta com s0, mas não automaticamente com s ou d. Questões globais e discretas continuam próprias.

[DERIVED, KNOWN] Normalidade: a fonte BBH inclui Einstein com ou sem constante cosmológica. Com K=N_deriv+2N_field*+3N_ghost*, temos delta_Lambda=delta_0+Lambda delta_-2. Uma primitiva relativa de base com K controlado transporta-se por descida finita em K. Na completação formal dos valores não diferenciados, o quadrático Pauli–Fierz mais três escalares fornece a normalidade e a eliminação formal de M2. Esse resultado preserva a polinomialidade nos jatos diferenciados; não permite afirmar que uma série formal seja uma função suave na carta inteira.

[DERIVED] Reducibilidade: Lie_v g≈0 e v·dphi≈0 implicam v·dQ≈0. O jato u_i^A=delta_i^A, u_0=0 e B01^1=B10^1=b tem tau=0 e dQ=−2b dx0. Adjugata, densidade da região não degenerada e continuidade dão v≈0, sem introduzir inversos de gradientes. Aqui B=Du=D(dy) é o Hessiano. Isso elimina f em a2=C* f+M2; ainda falta eliminar M2 na classe relativa suave covariante. O próximo contrato é essa primitiva, ou uma homotopia direta de H²_char,cov.

[DERIVED] Admissibilidade: um contratermo que cancela a quebra não precisa já ser invariante sob o gauge quântico. Naturalidade sob transporte simultâneo dos dados de fundo é uma exigência distinta. A transgressão T3(A,Abar) satisfaz dT3=tr(F²)−tr(Fbar²), mas não é uma primitiva de toda anomalia. A média por O(4) preserva primitivas globais já existentes em uma classe estável; não prova sua existência. A condição de realidade exige uma involução graduada compatível.

[DERIVED] Renormalização: C4 reduzido tem coeficientes A1=−13s²/16+7s/6+1/6 e A2=27s²/8−s+1/3, onde s=kappa c. Em s=4, A1=−49/6, A2=151/3 e 3A1+A2=155/6. Há um certificado explícito C42_poly=Cred+div J+E:M+s|tau|²/6. Trata-se de uma extensão polinomial escolhida, sem calcular a verdadeira Hessiana fora das soluções. A convenção euclidiana gB=gR+K A log(rho²/mu²), K=hbar/(4pi)², dá beta=2KA. A conversão local de ação declarada dá beta_B_FRW=−155K/3 em s=4. Ela não fixa o valor finito de B, um fluxo único de kappa, o sinal da energia ou a retroação completa. Após Bochner, a divergência explícita vale 3x/4; antes, valia 5x/4. Ambos os representantes recuperam o mesmo C4 total.

[REAL] Os 16 controles simbólicos exatos novos de RG passaram. Nenhuma compilação Lean nova foi feita. As revisões internas delimitadas e as verificações de bytes não certificam o objetivo físico completo.

[OPEN] Primitiva relativa suave M2 ou H²_char,cov; descida e admissibilidade na classe Q2; remoção da anomalia e equação mestra quântica; setor e estado físico interagentes; independência de fundo e questões globais; condições finitas e controle UV; correspondência física e alcance da reconstrução; medida independente do campo de probabilidades e BRST vertical, se alegados; integração dos 21 módulos e formalização das deduções novas. O objetivo geral permanece ativo.
''')

new_text(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_070.md', '''# Caminho crítico local — adendo 070

Resultados preservados: registro de fase e ramo, seleção, reconstruções condicionais com ação declarada, fundo global, inverso variacional, estado físico livre, BRST completo e construção Q2 de produtos renormalizados na álgebra auxiliar.

A comparação métrica–vielbein agora dispõe de equivalência BV formal com antifields e derivada horizontal. A normalidade relativa formal, o transporte finito em Lambda e a ausência de reducibilidade universal por dphi e dQ também estão demonstrados nos alcances indicados. Essas etapas já não devem ser listadas como lacunas integrais.

O caminho local das anomalias é: H²_char,cov na classe suave admissível → eliminação do nível xi² vezes CE de grau 3 → descida e comparação no mesmo espaço → primitiva da quebra → renormalização finita e equação mestra quântica. O resíduo concreto é a primitiva de M2, quadrático nos antifields, preservando coeficientes suaves e covariância; uma homotopia direta de H²_char,cov seria uma alternativa. A aciclicidade KT ordinária e o teste C0 de grau quatro não substituem esse passo.

No alvo S³, o volume tem grau total três. O candidato misto Omega2 q3 tem primitiva na álgebra explicitada. A colagem para s0 não é automaticamente colagem para s ou d. A transgressão com fundo ilustra admissibilidade, sem remover uma quebra específica. Questões globais, discretas e de independência de fundo continuam separadas.

A redução de C4 fornece um representante EFT, um certificado em equações de movimento e divergências e coeficientes logarítmicos de RG, com 16 controles simbólicos novos. Restam condições de renormalização finitas, observáveis com cancelamento da dependência de escala e as construções de estado e de retroação exigidas. O fluxo de uma volta não fornece a conclusão UV.

Permanecem também o alcance geral da correspondência entre dados e geometria, a comparação de fundos, uma eventual quantização independente do campo de probabilidades e a integração dos 21 módulos anteriores com formalização dos resultados novos. Nenhuma compilação Lean nova em 070; gates intactos; objetivo ativo.
''')

new_text(OUT / 'ADENDO_REVISOES_070.md', f'''# Revisões e correções ao lado — entrega 070

[DERIVED] Equivalência BV e admissibilidade foram examinadas por outro agente. A raiz revisou integralmente topologia, redução de graus, normalidade e reducibilidade. A redução RG recebeu revisão de outro agente, autor do coeficiente de entrada e não da redução nova. Os escopos estão explícitos nos pareceres. Essas revisões são internas e delimitadas.

A revisão documental do relatório está em <{review_directory.as_posix()}>. O manifesto final registra os bytes do relatório, notas, revisões e fontes referidas. As verificações documentais são distintas dos 16 controles simbólicos e das demonstrações analíticas.

Correções ao lado: Lambda isoladamente não é um obstáculo de normalidade; o resíduo envolve primitivas suaves covariantes relativas. O ghost Lorentz antigo tem um termo compensador sob mudança Omega(x). O Hessiano é B=Du=D(dy). C0 não é a hipótese residual da redução específica em ghost cinco. As divergências 3x/4 e 5x/4 pertencem a representantes diferentes antes e depois de Bochner, com C4 total inalterado. Os documentos congelados permanecem intactos.

O resultado H4_2 formal não fornece a primitiva suave M2. A prova de ausência de reducibilidade por densidade anula o parâmetro; ela não produz primitivas regulares por inversão de um determinante. A equivalência BV usa a completação declarada e um fundo fixo. A construção Q2 da entrega 069 continua sendo uma álgebra auxiliar com quebra consistente; a equação mestra quântica ainda precisa ser satisfeita.
''')

tunnel_pin = new_text(tunnel, f'''# Entrega 070 — cohomologia relativa, equivalência BV e renormalização

[Relatório](<{report.as_posix()}>) · [Resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_070.json').as_posix()}>) · [Manifesto](<{(OUT / 'MANIFESTO_ENTREGA_070.json').as_posix()}>).

[REAL] Os quatro artefatos canônicos v338 permanecem iguais aos da captura 069. Dos 98 módulos comparados, 77 estão presentes e 21 continuam pendentes. Nenhum um.py foi executado ou importado. Nenhum original foi escrito; nenhuma compilação Lean ou teste de natureza foi realizado. A integração deve portar deltas da cópia histórica ao programa vivo.

[DERIVED, KNOWN] Resultados novos: equivalência BV local formal entre métrica e vielbein, incluindo ghosts e antifields, também módulo d; descida do volume de S³ e primitiva do candidato Omega2 q3 na classe declarada; redução finita de ghost cinco a H²_char,cov; transporte finito em Lambda; ausência de reducibilidade universal via dphi e dQ sem inversos de gradientes; normalidade e H4_2 na completação formal indicada; redução de C4, certificado em EOM e divergências, redefinição de campos e fluxo logarítmico de RG.

Os coeficientes são A1=−13s²/16+7s/6+1/6 e A2=27s²/8−s+1/3. Em s=4: A1=−49/6, A2=151/3 e 3A1+A2=155/6. A convenção euclidiana gB=gR+K A log(rho²/mu²) dá beta=2KA. Na conversão local de ação especificada, beta_B_FRW=−155K/3, com K=hbar/(4pi)². O valor finito de B, um fluxo único de kappa e a retroação completa permanecem por determinar. A divergência reduzida vale 3x/4; antes de Bochner, 5x/4. O C4 total permanece (7440x²+1616x−211)/96.

[OPEN] O próximo contrato é a primitiva relativa M2 com coeficientes suaves e covariantização, ou uma homotopia direta de H²_char,cov. Depois é necessário ligar a descida e a admissibilidade à quebra interagente produzida, removê-la e satisfazer a equação mestra quântica. O resultado formal H4_2 não foi promovido a H²_char,cov suave. A ausência de reducibilidade também não fornece, por si, primitivas globais.

[REAL] Há 16 controles simbólicos exatos novos aprovados e nenhuma compilação Lean nova. Notas e revisões têm seus bytes registrados no manifesto. Fase e ramo, H3 interno e falsificadores existentes permanecem preservados. Continuam abertos o setor e estado físico interagentes, questões globais e de fundo, controle UV, condições finitas, correspondência física e alcance da reconstrução, medida independente e BRST vertical do campo de probabilidades se alegados, além da integração e formalização. Memória e desenho locais são arquivos novos; Atlas e memórias canônicas permanecem somente leitura. O objetivo geral continua ativo.
''')

for path in sorted(OUT.iterdir()):
    if path.is_file():
        pin(path)
for document in [report, tunnel]:
    for index, target in enumerate(re.findall(r'\]\(<(C:/[^>]+)>\)', document.read_text(encoding='utf-8'))):
        if target == (OUT / 'MANIFESTO_ENTREGA_070.json').as_posix():
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
    'checks_passed': sum(item['passed'] for item in checks),
    'tunnel': tunnel_pin,
    'exact_symbolic_controls': 16,
    'new_lean_compilation': False,
    'um_execution_or_import': False,
    'originals_written': False,
    'goal_complete': False,
    'limits': 'Direct source and byte checks, preserved historical pins, and the16 enumerated newCAS controls. Not a count of analytic theorems and not a proof that the full physical or interacting objective is complete.'
}
manifest_pin = new_json(OUT / 'MANIFESTO_ENTREGA_070.json', manifest)
print(json.dumps({'status': manifest['status'], 'checks': len(checks), 'passed': manifest['checks_passed'], 'files': len(manifest['files']), 'cas': 16, 'new_lean': 0, 'report': pin(report), 'manifest': manifest_pin, 'tunnel': tunnel_pin}, ensure_ascii=True))
