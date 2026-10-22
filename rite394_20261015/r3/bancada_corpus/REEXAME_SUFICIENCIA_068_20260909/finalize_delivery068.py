from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
DIRS = [
    ROOT / 'GLOBALIZACAO_PROBABILIDADES_S3_20260909_220238_785086',
    ROOT / 'EXTENSAO_BRST_COMPLETA_20260909_220941_811364',
    ROOT / 'RENORMALIZACAO_SIGMA_EFT_20260909',
    ROOT / 'BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557',
    ROOT / 'CLASSES_CARACTERISTICAS_C0_20260909_221649',
    ROOT / 'REVISAO_ADVERSARIAL_BRST_068_20260909_221529_258581',
    ROOT / 'REVISAO_FONTE_QUARTICA_20260909_221154',
    ROOT / 'REVISAO_FEYNMAN_BRST_20260909_222614',
]
assert len(sys.argv) == 2, 'Supply the independently written C0 review folder.'
c0_review = Path(sys.argv[1]).resolve()
assert c0_review.is_relative_to(ROOT) and c0_review.is_dir()
DIRS.append(c0_review)
pins = {}
checks = []


def pin(path):
    path = path.resolve()
    data = path.read_bytes()
    value = {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if value['path'] in pins:
        assert pins[value['path']] == value, 'Source changed: ' + str(path)
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
    return new(path, value.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))


def recorded_pins(obj, source, locator='root'):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(obj.get('sha256', ''))):
            path = Path(obj['path'])
            check('absolute_recorded_pin:' + source + ':' + locator, path.is_absolute())
            current = pin(path)
            check('recorded_pin:' + source + ':' + locator,
                  current['sha256'] == obj['sha256'] and ('bytes' not in obj or current['bytes'] == obj['bytes']), current['path'])
        for key, value in obj.items():
            recorded_pins(value, source, locator + '.' + key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            recorded_pins(value, source, locator + '[' + str(index) + ']')


snapshot = load(OUT / 'ESTADO_CANONICO_068.json')
check('canonical_four_unchanged_from067', len(snapshot['comparison_with_delivery067']) == 4 and all(row['unchanged'] for row in snapshot['comparison_with_delivery067']))
check('canonical_seal_matches', snapshot['seal_um_hash_matches'])
check('canonical_presence', snapshot['present'] == 77 and len(snapshot['absent']) == 21 and len(snapshot['modules']) == 98)
recorded_pins(snapshot['pins'], 'snapshot068')
previous = load(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json')
check('pending_modules_unchanged', snapshot['absent'] == previous['pending_canonical_modules'])
recorded_pins(previous['working_copy'], 'historical_working_copy98')
pin(ROOT / 'REEXAME_SUFICIENCIA_067_20260909/MANIFESTO_ENTREGA_067.json')

for directory in DIRS:
    check('source_directory:' + directory.name, directory.is_dir())
    for path in sorted(directory.iterdir()):
        if path.is_file():
            pin(path)
            if path.suffix.lower() == '.json':
                recorded_pins(load(path), directory.name + '/' + path.name)

cas = []
for path, expected in [
    (DIRS[0] / 'VERIFICACAO_GLOBAL_S3.json', 47),
    (DIRS[2] / 'VERIFICACAO_SIGMA_HEAT.json', 13),
    (DIRS[2] / 'VERIFICACAO_FONTE_QUARTICA.json', 8),
]:
    receipt = load(path)
    rows = list(receipt['checks'].values()) if isinstance(receipt['checks'], dict) else receipt['checks']
    check('cas_count:' + path.name, len(rows) == expected)
    check('cas_exact_pass:' + path.name, all(row.get('passed') is True and row.get('residual') == '0' for row in rows))
    check('cas_not_lean:' + path.name, 'NOT_LEAN' in receipt['status'])
    cas.append({'receipt': pin(path), 'exact_controls': len(rows), 'scope': receipt['status']})
check('cas_total', sum(item['exact_controls'] for item in cas) == 68)

global_manifest = load(DIRS[0] / 'MANIFESTO_GLOBALIZACAO_S3.json')
check('probability_alphabet', global_manifest['construction_inputs']['fine_categories_total'] == 1289)
check('probability_count_arithmetic', 1 + 8 * (21 + 140) == 1289)
check('source_notes_present', all(path.is_file() for path in [
    DIRS[0] / 'PROVA_GLOBAL_S3_ASSINADA_E_LIVRE.md',
    DIRS[1] / 'EXTENSAO_BRST_E_CORRECOES_SUAVES.md',
    DIRS[1] / 'ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md',
    DIRS[2] / 'CONTRATERMOS_SIGMA_E_ORDEM_EFT.md',
    DIRS[2] / 'FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md',
    DIRS[3] / 'BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md',
    DIRS[4] / 'EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md',
]))

report = OUT / 'REEXAME_SUFICIENCIA.md'
pin(report)
created = datetime.now(timezone.utc).isoformat()
canonical = next(entry for entry in snapshot['pins'] if entry['path'].endswith('/Nós/um.py'))
result = {
    'status': 'DELIVERY_068_GLOBAL_FIXED_BACKGROUND_AND_FREE_BRST_PROGRESS__INTERACTING_QG_OPEN',
    'created_utc': created,
    'canonical': canonical,
    'canonical_unchanged_from067': True,
    'canonical_modules_present': 77,
    'pending_canonical_modules': snapshot['absent'],
    'previous_benchmark': {'modules': 98, 'working_copy': previous['working_copy'], 'new_run_this_delivery': False},
    'new_lean_modules': 0,
    'new_lean_compilations': 0,
    'new_exact_symbolic_controls': 68,
    'cas': cas,
    'written_results': [
        'Global positive 1289-category representation of the specified open S3 cylinder, with a Nash existence input and global joint-variation right inverse',
        'Global classical/linear physical quotient transport under the adopted Einstein-sigma action and matched domain',
        'Full Einstein-sigma free BRST covariances and Feynman inverse, exact linear Ward/contact identities and positivity on physical quotient',
        'External-metric sigma one-loop heat coefficient requiring four-derivative operators in that sector',
        'Explicit quartic classical source and exact corrected truncated FRW solution',
        'Conditional epsilon-adic cohomology lifting and conditional renormalized-QME induction',
        'Euler/Pontryagin nontriviality modulo the specified natural algebraic EOM ideal, with weak-equality/KT compatibility still explicit'
    ],
    'remaining': [
        'Physical correspondence/action and scope beyond the specified global background',
        'Renormalized time-ordered products for the full coupled interacting theory',
        'Cohomology contracts, physical-parameter specialization or direct sigma theorem, quantum master identity',
        'Background independence and global anomalies in claimed scope',
        'Chosen UV completion/control and renormalization conditions',
        'Vertical BRST/functional measure/operator positivity if independent probability-field quantization is claimed',
        'Port 21 prior modules and formalize new written results without promoting CAS to Lean'
    ],
    'originals_written': False,
    'um_executed_or_imported': False,
    'nature_tests_run': False,
    'canonical_gate_modified': False,
    'goal_complete': False,
    'review_scope': 'Root reading plus separately authored bounded internal reviews; no external approval or machine proof of analytic theorems claimed.'
}
new(OUT / 'RESULTADO_ENTREGA_068.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

new_text(OUT / 'MEMORIA_DE_TRABALHO_068.md', f'''# Memória local de continuidade — entrega 068

Registro em {created}. Esta memória é nova, pertence à bancada Chatgpt e não substitui nem copia o Atlas canônico.

[REAL] O retrato de quatro artefatos canônicos coincide com 067; v338, 683 arquivos embutidos, 77/98 módulos da bancada presentes e 21 pendentes. Pins e nomes estão no resultado estruturado. Nenhum um.py executado/importado, nenhum original escrito, nenhum teste de natureza ou compilação Lean novo. A integração 98 histórica permanece congelada; portar deltas ao programa vivo.

[DERIVED + KNOWN] A representação global em (0,pi)×S3 usa 1289 probabilidades positivas, relógio q=1−a²/8, oito B assinados, bloco livre21 e residual140. O residual importa existência de Nash em S3; não alegar funções numéricas todas construídas. A=DΦ tem inverso à direita R global, com suportes compactos interiores. Ação/partição/correspondência explícitas; extremos temporais excluídos. O estado físico067 transporta-se ao mesmo quociente global. Cinco probabilidades antigas continuam insuficientes no escopo anterior.

[DERIVED + KNOWN] Sistema Einstein–sigma livre completo (u,b,c,barc): correções Ward suaves, substituição física suave, CCR/CAR e Hadamard, positividade somente física. Feynman com E=ret−adv, epsilon=i hbar, Z=(+,+,−,−), G_F=G_ret−i Z Lambda_minus/hbar. Contato misto ell² C(i hbar G_D^F)C*=i hbar ell I; cancela-se no complemento de Schur do bloco b-b. A prova usa phi=id e Hubble diferente de zero. Não confundir com ghosts das direções verticais do campo probabilístico redundante ou QME interagente.

[DERIVED + KNOWN] Sigma S3 em métrica euclidiana externa: B4=Q²/3+2W²/3+RQ/3+(5R²−2Ric²+2Riem²)/120+BoxQ/3+BoxR/10. Exemplo toroidal on-shell dá k⁴ e exige quatro derivadas nesse setor. Não é determinante completo métrica/sigma/ghost. Coeficientes finitos de EFT são entradas; operadores superiores são inserções perturbativas.

[DERIVED] Na ação lorentziana truncada com b1 Q²+b2 W², B=3b1+b2, rho4=−3B/a⁴, p4=−B/a⁴; a_B²=2+2 sqrt(1−kappa B) cos(r−r0), em domínio positivo. Duas equações de Einstein e sigma verificadas; endpoint kappa B1 tem a²2. Solução clássica truncada, não expectativa quântica, estabilidade ou cura UV.

[DERIVED condicional] Lema epsilon-ádico e indução QME dependem de cohomologia de referência e produtos temporais/consistência local. [DERIVED] Euler/Pontryagin independentes modulo ideal natural algébrico de EOM: certificado off-shell complexifica, primitiva tensorial glua, S4/CP2 determinante6. [OPEN] Compatibilizar igualdade fraca/KT no mesmo espaço; fechar H1_sigma e epsilon1 ou prova direta; interações, anomalias globais, independência entre fundos e UV.

[REAL] 68 controles simbólicos exatos:47+13+8. Zero Lean novo. Demonstrações analíticas escritas e revisões delimitadas estão nas fontes do manifesto. Não reabrir fase/ramo, H3 interno, critérios de falsificação ou resultados anteriores já integrados.

Objetivo geral continua ativo. Próximo passo concreto: fechar os contratos cohomológicos e construir produtos temporais renormalizados do sistema acoplado, mantendo separada a escolha/justificação UV. Notas BV/C0 anteriores que diziam matriz livre aberta recebem a precisão nesta memória e no relatório: esse dado livre foi fornecido em068, no fundo/complexo especificados.
''')

new_text(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_068.md', '''# Adendo local ao caminho de suficiência — entrega 068

Registro completo de fase e ramo → resultados existentes preservados.

Dados finos agrupados e assinados → representação global do fundo (0,pi)×S3 → AR=Id global → ação Einstein–sigma adotada → equivalência variacional e linear/simplética no mesmo domínio: demonstrações escritas disponíveis. Ação e correspondência continuam entradas; Nash é dependência de existência explícita.

Fundo curvo concreto → S/V/TT e estado físico067 → defeito Ward suave → covariâncias BRST completas → inverso Feynman e contatos: dado quântico livre disponível. Não reabrir essa etapa inteira ao listar interações pendentes. Outro fundo exige outros contratos, e a redundância vertical de P não ganhou ghosts por analogia.

Interação acoplada → produtos temporais renormalizados → identidade anômala local → cohomologia no complexo admissível → QME: próximo caminho crítico. A deformação formal é condicional; o teste Euler/Pontryagin foi demonstrado modulo o ideal especificado, mas igualdade fraca/KT e H1_sigma completo ainda precisam ser compatibilizados.

Sigma externo uma volta → operadores de quatro derivadas → fonte quártica clássica e família corrigida: demonstrações disponíveis. Isso não fecha o determinante quântico acoplado, condições de renormalização, convergência/UV ou estabilidade do novo fundo.

Em paralelo: portar os 21 módulos pendentes da bancada e formalizar o novo material sem reclassificar controles CAS como teoremas Lean. Para uma alegação geral, tratar alcance físico, outros fundos/matérias, independência entre fundos, anomalias globais e rota UV. Objetivo ativo; nenhum gate movido.
''')

new_text(OUT / 'ADENDO_REVISAO_E_ESCOPO_068.md', f'''# Revisões e precisão de escopo — entrega 068

[DERIVED — demonstração e revisão escritas] A raiz leu as notas principais da representação global, BRST, Feynman, contratermos, fonte quártica, deformação BV e classes características. As revisões cruzadas são internas e delimitadas; não constituem aprovação externa ou compilação Lean.

A revisão BRST independente examina a álgebra de Cauchy, Ward, diferenças suaves e contratos microlocais, usando a redução067 como resultado anterior. A revisão Feynman verifica sinais, paridade e contatos, tomando a construção Hadamard principal como entrada. A revisão quártica verifica separadamente as duas componentes de Einstein, inclusive H=0, a equação sigma e o endpoint estático. A revisão C0 encontra-se em <{c0_review.as_posix()}>; seu alcance não é a classificação completa de todas as anomalias.

O contato misto é ell² C(i hbar G_D^F)C*=i hbar ell I, cancelado no complemento de Schur; o zero do bloco b-b não permite omiti-lo. A classe característica é demonstrada modulo um ideal natural algébrico; não se presume equivalência irrestrita com toda anulação on-shell.

As marcações históricas da nota BV/C0 sobre matriz livre ainda aberta são precisadas ao lado:068 fornece o sistema livre Einstein–sigma do fundo fixado. Continuam abertos o regime interagente renormalizado, sua QME/cohomologia completa e um eventual complexo próprio das variáveis probabilísticas redundantes. A representação global1289 elimina a restrição de carta positiva apenas para o fundo descrito; não universaliza a construção a todo relógio/topologia.

Os pins das fontes e pareceres estão no manifesto. Nenhuma nota congelada foi modificada.
''')

tunnel = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_068_ESPONTANEA_global_brst_eft.md'
tunnel_pin = new_text(tunnel, f'''# Entrega 068 — representação global, BRST livre e primeiros contratermos

[DERIVED + KNOWN — demonstrações escritas; REAL — recibos e pins] O [reexame completo](<{report.as_posix()}>) e o [resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_068.json').as_posix()}>) estão prontos para consulta pela sessão que codifica.

Canônico relido: mesmos quatro artefatos da entrega067; v338,77/98 módulos presentes,21 pendentes. Não houve execução/importação de um.py ou alteração do acervo. Portar deltas da bancada histórica98; nunca substituí-la pelo programa vivo nem substituir o vivo pela cópia antiga.

Novos resultados: (1) 1289 probabilidades positivas representam globalmente g e phi no cilindro aberto S3, com AR=Id e existência de Nash explicitada; (2) extensão BRST livre Einstein–sigma completa, Hadamard e Feynman, Ward e contatos; (3) coeficiente de calor sigma externo uma volta e necessidade de termos de quatro derivadas nesse setor; (4) tensor quártico e família FRW clássica corrigida; (5) levantamento cohomológico formal condicionado e não trivialidade Euler/Pontryagin modulo ideal natural algébrico.

Escopos indispensáveis: ação/partição/correspondência como entradas; fundo (0,pi)×S3, kappa c4, Lambda3/4, Hubble não zero; Nash é existência e não tabela numérica integral. BRST pertence ao sistema Einstein–sigma, sem ghosts verticais de P automaticamente. Feynman usa E=ret−adv, epsilon=i hbar e Z=(+,+,−,−); contato ell² C(i hbar G_D^F)C*=i hbar ell I. O coeficiente sigma não é o determinante completo métrica/sigma/ghost. A família quártica não é solução semiclassica ou resolução UV.

Ficam abertos: produtos temporais renormalizados e QME interagente; compatibilidade cohomológica/KT e sigma físico epsilon1; independência entre fundos/anomalias globais; condições de renormalização e rota UV; medida/BRST vertical se P for quantizado independentemente. Não reabrir fase/ramo, H3 interno ou falsificadores já existentes.

68 controles CAS exatos=47+13+8; zero novos teoremas/compilações Lean nesta entrega. Formalizar hipóteses e enunciados separadamente. MANIFESTO_ENTREGA_068.json mede notas, recibos e revisões. Memória e desenho local estão na pasta do relatório; Atlas e memórias canônicas permanecem somente leitura.
''')

for path in sorted(OUT.iterdir()):
    if path.is_file():
        pin(path)

for document in [report, tunnel]:
    for index, target in enumerate(re.findall(r'\]\(<(C:/[^>]+)>\)', document.read_text(encoding='utf-8'))):
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
    'exact_symbolic_controls': 68,
    'new_lean_compilation': False,
    'um_execution_or_import': False,
    'originals_written': False,
    'goal_complete': False,
    'limits': 'Byte/pin checks and enumerated CAS identities do not certify analytic theorems. Written results and internal reviews retain their stated hypotheses. No new canonical runtime or nature tests.'
}
manifest_pin = new(OUT / 'MANIFESTO_ENTREGA_068.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'status': manifest['status'], 'checks': manifest['checks_total'], 'passed': manifest['checks_passed'], 'files': len(manifest['files']), 'cas': 68, 'new_lean': 0, 'report': pin(report), 'manifest': manifest_pin, 'tunnel': tunnel_pin}, ensure_ascii=True))
