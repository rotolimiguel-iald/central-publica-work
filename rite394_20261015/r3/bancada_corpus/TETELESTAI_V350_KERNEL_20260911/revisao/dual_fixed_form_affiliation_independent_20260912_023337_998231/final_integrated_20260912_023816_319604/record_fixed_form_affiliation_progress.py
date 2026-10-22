"""Record the reviewed fixed-algebra form affiliation with exact-byte memory backups."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MODULES = ['ResolventGraphTransport', 'DualSupportTransport', 'DualFixedFormAffiliation']
MARKER = 'TETELESTAI_V350_DUAL_FIXED_FORM_AFFILIATION_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
BACKUPS = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path, raw):
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else None
    if before == raw:
        return
    if before is not None:
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as handle:
            handle.write(before)
        assert backup.read_bytes() == before
        BACKUPS[str(path)] = str(backup)
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as handle:
        handle.write(raw)
    assert temporary.stat().st_size == len(raw) > 0 and temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw


def append(path, text):
    before = path.read_bytes()
    assert MARKER.encode() not in before, 'Already recorded: ' + str(path)
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    assert raw.startswith(before) and len(raw) > len(before)
    write_atomic(path, raw)


def python_body(raw):
    tree = ast.parse(raw)
    found = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in node.targets):
            node.value = ast.Constant(value='EMBEDDED_KERNEL_EXCLUDED')
            found = True
    assert found
    return ast.dump(tree, include_attributes=False)


assert '--review-read' in sys.argv, 'Read the completed review before recording.'
review = ROOT / 'revisao/REVIEW_DUAL_FIXED_FORM_AFFILIATION.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'fixed_resolvent_custody.json').read_bytes())
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
assert all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run']
assert digest(ROOT / 'um.py') == tests['working_um_sha256'] == integration['working_sha256']
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
prior_copy = next((p for p in ROOT.glob('um.py.bak_*')
                   if digest(p) == previous['working_sha256']), None)
assert prior_copy is not None
assert python_body(prior_copy.read_bytes()) == python_body((ROOT / 'um.py').read_bytes())
new_sources = {'TGLExt/V350' + name + '.lean' for name in MODULES} | {'TGLExt.lean', 'TGL/Audit.lean'}
assert new_sources <= {Path(r['source']).relative_to(ROOT / 'kernel').as_posix()
                       for r in build['records']}
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
    if source.relative_to(ROOT / 'kernel').as_posix() in new_sources:
        assert row.get('source_unchanged_during_compile') is True
targets = set()
for name in MODULES:
    content = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    integrated = (ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')).read_text(encoding='utf-8')
    assert re.sub(r'^import TGLV350\.', 'import TGLExt.V350', content, flags=re.M) == integrated
    targets.update('TGLV350.Regular.' + target for target in
                   re.findall(r'^#print axioms ([\w.]+)$', content, re.M))
for target in targets:
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[flag] is False for flag in open_flags)
report_path = ROOT / 'RELATORIO_AFILIACAO_DA_FORMA_FIXA.md'
report = f'''# A forma dual é afiliada à álgebra fixa

{DATE}. [REAL — Lean incremental em cópia, revisão independente delimitada.]

Para A≥0 no mesmo core regular N, a forma fechada q_A agora pertence a
`AffiliatedPositiveForm (dualFixedCore P)`. Concretamente, para todo
unitário U que comuta com a álgebra fixa F e todo vetor w do Hilbert
ambiente, q_A(Uw)=q_A(w) em ENNReal, inclusive quando vale infinito.
A forma de saída continua literalmente a integral dos mesmos cortes;
não foi substituída por outra forma com nome semelhante.

## Ligação entre resolvente, suporte, grafos e forma

1. Um operador limitado U que comuta com R preserva closure(Ran R).
   A prova usa uma preimagem fechada e a imagem dos vetores de Ran R;
   não presume que a própria imagem seja fechada. A igualdade já provada
   closure(Ran R)=closure(D(q_A)) transfere essa propriedade ao suporte K.
2. A restrição U_K é uma CLM efetiva em K. Ela comuta com R_K.
   Cálculo funcional limitado fornece comutação com B=√R_K e C=√(I−R_K).
   Os parâmetros dos grafos, x=Bz e y=Cz, são transportados para U_K z.
   Isso preserva o domínio real do grafo da raiz; o mesmo argumento vale
   para T, cujo grafo usa R_K e I−R_K.
3. Para U unitário, a auto-adjunção de R dá também comutação com U*.
   As duas restrições se cancelam. As equivalências de pertinência aos
   grafos de T e S estão provadas nos dois sentidos. Não se trata apenas
   de uma inclusão de grafo ou igualdade de fórmulas fora do domínio.
4. Para w de energia finita, a representação completa da forma fornece
   w∈D(S). O transporte do grafo e a preservação da norma dão
   q_A(Uw)=‖S(U_K w)‖²=‖S w‖²=q_A(w).
   Se q_A(w)=∞ e q_A(Uw) fosse finita, aplicar o resultado a U* daria
   q_A(w)<∞. Essa contradição demonstra a igualdade também no setor infinito.
5. O resolvente construído pertence a F. Portanto todo U∈F' comuta com R,
   e o resultado anterior fornece a afiliação da mesma q_A a F. O tipo
   `AffiliatedPositiveForm` exige forma positiva fechada e invariância por
   todo unitário do comutante. Essas leis são demonstradas, não hipóteses
   novas no construtor da forma dual.

A passagem de N para F é substantiva: F⊆N implica N'⊆F'. A prova anterior
só tratava os unitários de N'; a nova trata todos os de F'. Os grafos são
os de T e S no suporte já construído, possivelmente próprio ou zero.
Não se afirma um operador densamente definido no Hilbert ambiente inteiro.
Não se constrói por decreto um suporte não nulo ou o projetor P_F.

## Fronteira restante

[OPEN] Identificar F com a base amplificada. Equipar o cone de formas
ampliadas com as operações/ordem e a correspondência necessária ao peso
operadorial; completar as leis do peso com valores nessa base e a sua
semifinitude na álgebra. A afiliação da forma não prova semifinitude do peso.
Também não se reivindica aqui a construção de predual ou um teorema geral
de representação espectral não limitada do cone.

[OPEN] Estado modular da base, gerador e perturbação para o traço canônico
fiel normal semifinito e sua escala; Three Locks/H1; H2 e H3 na mesma
realização física; setor quântico interagente, BRST/QME/anomalias/UV;
contrato dependente ampliado consumido pelo gate e runtime integral isolado.
A normalização e o sinal do traço continuam com as obrigações anteriores.

As seis flags maiores continuam falsas. O corpo Python, fora dos arquivos
Lean embutidos, permanece igual ao estrato anterior por AST. O gate legado
não mudou. Nenhuma transposição canônica, publicação ou confirmação física.

## Evidência

{len(targets)} alvos novos (5+7+10), {len(build['records'])} registros Lean
integrados válidos, {tests['passed']} controles aprovados,
{tests['axiom_report_entries']} declarações distintas no Audit e
{integration['embedded_files']} arquivos embutidos. Axiomas dos alvos no
trio propext/Classical.choice/Quot.sound. Dependências verificadas e reutilizadas;
compilação incremental, sem rebuild completo da biblioteca ou runtime do monólito.

Base `{integration['base_sha256']}`.
Cópia `{integration['working_sha256']}`.

[Revisão independente](<{review.as_posix()}>).
O parecer distingue recompilações próprias e inspeção dos registros integrados.
Os estratos anteriores permanecem intactos com adendo datado. O objetivo integral
continua ativo.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `ResolventGraphTransport`, `DualSupportTransport`,
`DualFixedFormAffiliation`: a mesma q_A agora pertence a
`AffiliatedPositiveForm F`, F=dualFixedCore P. Para todo U∈F' unitário,
q_A(Uw)=q_A(w) no Hilbert inteiro, incluindo ∞. A prova usa o mesmo R∈F,
a restrição ao suporte K, comutação CFC e grafos de T/S com os domínios
preservados nos dois sentidos. O inverso U* controla o setor infinito.

{len(targets)} alvos novos; {len(build['records'])} registros Lean,
{tests['passed']} controles, {tests['axiom_report_entries']} declarações
distintas no Audit, axiomas no trio. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python/gate inalterado por AST.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

Adendo: a afiliação da forma à álgebra fixa, antes aberta, agora está
provada no sentido concreto de invariância por todo unitário de F'.
A equivalência de grafos no suporte também está provada; K pode ser zero
ou próprio, sem declarar domínio denso no ambiente inteiro.
[OPEN] F=base; operações/ordem do cone ampliado e peso com valores na base,
semifinitude na álgebra; estado modular/gerador/perturbação/traço;
Three Locks/H1/H2/H3; interações/BRST/QME/anomalias/UV; contrato ampliado e
runtime integral. Predual/cálculo espectral não limitado geral não construídos.
Seis flags abertas false, objetivo integral ativo; sem confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md',
    'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md', 'RELATORIO_RESOLVENTE_FIXO_DUAL.md')]
surfaces += [CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md']
for surface in surfaces:
    append(surface, note)
    assert MARKER.encode() in surface.read_bytes()
custody = {
    'timestamp': DATE, 'original_unchanged': True,
    'original_sha256': digest(ORIGINAL), 'working_sha256': digest(ROOT / 'um.py'),
    'previous_working_copy': str(prior_copy), 'python_body_unchanged_from_previous_stage': True,
    'modules': {name: digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) for name in MODULES},
    'review_sha256': digest(review), 'report_sha256': digest(report_path),
    'surface_sha256': {str(p): digest(p) for p in surfaces}, 'backups': BACKUPS.copy(),
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'], 'full_runtime': False,
    'fixed_form_affiliation_including_infinity': True,
    'unitary_graph_equivalences_on_support': True,
    'fixed_algebra_identified_with_base': False,
    'operator_valued_weight_semifinite': False,
    'canonical_trace_constructed': False, 'full_goal_complete': False,
}
write_atomic(ROOT / 'fixed_form_affiliation_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
