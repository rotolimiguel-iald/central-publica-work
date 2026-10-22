"""Record the verified closed-form increment; preserve every prior memory byte."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MARKER = 'TETELESTAI_V350_DUAL_CLOSED_FORM_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MODULES = ['DualQuadraticLaws', 'DualClosedForm']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path, raw):
    assert path.is_relative_to(ROOT) or path in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else None
    if before == raw:
        return
    if before is not None:
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as handle:
            handle.write(before)
        assert backup.read_bytes() == before
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as handle:
        handle.write(raw)
    assert temporary.stat().st_size == len(raw) > 0 and temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw


def append(path, text):
    before = path.read_bytes()
    if MARKER.encode() in before:
        raise RuntimeError('This increment is already recorded: ' + str(path))
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    assert raw.startswith(before) and len(raw) > len(before)
    write_atomic(path, raw)


def python_ast_without_embedded(raw):
    tree = ast.parse(raw)
    found = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in node.targets):
            node.value = ast.Constant(value='KERNEL_CONTENT_EXCLUDED_FROM_PYTHON_BODY_COMPARISON')
            found = True
    assert found
    return ast.dump(tree, include_attributes=False)


assert '--review-read' in sys.argv, 'Read the completed independent review before running this recorder.'
review = ROOT / 'revisao/REVIEW_DUAL_CLOSED_FORM.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'dual_weight_custody.json').read_bytes())
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
assert all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run']
assert digest(ROOT / 'um.py') == tests['working_um_sha256'] == integration['working_sha256']
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']

prior_copy = next((p for p in ROOT.glob('um.py.bak_*')
                   if digest(p) == previous['working_sha256']), None)
assert prior_copy is not None
assert python_ast_without_embedded(prior_copy.read_bytes()) == python_ast_without_embedded(
    (ROOT / 'um.py').read_bytes()), 'This stage must not alter the Python body or gate.'

new_sources = {'TGLExt/V350' + name + '.lean' for name in MODULES} | {'TGLExt.lean', 'TGL/Audit.lean'}
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
    relative = source.relative_to(ROOT / 'kernel').as_posix()
    if relative in new_sources or 'source_unchanged_during_compile' in row:
        assert row.get('source_unchanged_during_compile') is True
    # Earlier accepted records predate this field; never invent a freeze observation.
for name in ('dualQuadraticIntegral_smul_vector', 'dualQuadraticIntegral_smul_operator',
             'dualQuadraticIntegral_parallelogram', 'dualQuadraticIntegral_lowerSemicontinuous',
             'dualClosedPositiveForm', 'dualClosedPositiveForm_one_domain',
             'dualClosedPositiveForm_zero_domain', 'dualQuadraticIntegral_commutant_invariant',
             'dualAffiliatedPositiveForm'):
    target = 'TGLV350.Regular.' + name
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
for flag in ('qgf_continuous_modular_realization_constructed',
             'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
             'gpf_H1_internal_susy_relative_gap_discharged',
             'gpf_H2_smooth_modular_four_frame_discharged',
             'gpf_H3_local_horizon_equilibrium_discharged'):
    assert evidence[flag] is False

module_rows = '\n'.join(
    f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
    for name in MODULES)
report_path = ROOT / 'RELATORIO_FORMA_DUAL_FECHADA.md'
report = f'''# Forma positiva fechada do integral dual

{DATE}. [REAL — construção e compilação Lean na cópia; revisão independente com escopo próprio.]

**A avaliação do integral dual agora tem as leis de uma forma positiva estendida,
semicontinuidade inferior, domínio finito construído e invariância unitária pelo
comutante da mesma álgebra. O traço canônico continua aberto.**

Para A≥0 na representação regular, q_A(v) é o integral em ENNReal dos cortes da ação
dual, com a constante (2π)⁻¹ já adotada. Foram provadas:

    q_A(c v) = |c|² q_A(v),
    q_A(v+w) + q_A(v−w) = 2q_A(v) + 2q_A(w),
    q_(r A)(v) = r q_A(v),  r≥0.

As igualdades valem com infinito, inclusive c=0. A prova não subtrai infinitos.
A semicontinuidade é obtida da igualdade, já compilada, com o supremo das avaliações
contínuas dos cortes. `ClosedPositiveForm` reúne exatamente essas leis e q(0)=0;
nela não foi incluída como campo uma representação espectral ainda não construída.

`finiteDomain` é o submódulo complexo construído a partir de {{v | q(v)<∞}}.
Os subníveis {{v | q(v)≤c}} são fechados. Isso não diz que o domínio finito inteiro é
fechado ou denso. Os controles formais distinguem os extremos:

    D(q_I) = {{0}},    D(q_0) = H.

Para A na mesma `regularCoreAlgebra P`, todo unitário U que comuta com essa álgebra
preserva q_A(Uv)=q_A(v). A prova usa que cada corte pertence à álgebra e passa pelo
supremo, sem pressupor um operador ilimitado já afiliado. O tipo
`AffiliatedPositiveForm` expressa essa invariância da forma, não entrega sozinho
uma medida espectral, um operador auto-adjunto ou o cone ampliado da álgebra de base.

[KNOWN — referência conceitual] As definições A.13–A.15 de
[Hiai](https://arxiv.org/pdf/2004.02383#page=154) ligam formas positivas estendidas
semicontínuas à representação por operador auto-adjunto no fecho do domínio finito.
**Essa equivalência de representação ainda não foi formalizada neste incremento.**

## Obrigações que permanecem

1. Construir a representação da forma no cone ampliado e identificar os pontos fixos
   da ação dual com a imagem da base. A invariância no comutante do core não substitui
   essa identificação com a base.
2. Construir o peso com valores nessa base e provar bimodularidade, fidelidade,
   normalidade e semifinitude. O ideal/domínio finito relevante para semifinitude
   é na álgebra; não se deve exigir D(q_A) denso em H para todo A positivo.
   D(q_I)={{0}} não contradiz, por si só, a semifinitude de um peso futuro.
3. Compor com o peso normal fiel da base, identificar o grupo modular correspondente
   e construir o operador afiliado de Λ_t, sua perturbação e o traço com a lei de escala.
4. Construir Three Locks e H1/H2/H3 nos mesmos objetos; completar o setor quântico
   interagente no alcance pretendido; ligar um contrato dependente forte ao gate.

A v350 canônica permanece com o gate que não consome as oito flags de fronteira.
Nesta etapa nem a função legada nem o corpo Python da cópia foram modificados: a
comparação AST com a etapa anterior excluiu somente o conteúdo embutido do kernel.
As novas formas não quitam core, canto, H1/H2/H3 ou testemunha total.

## Evidência e limites

{len(build['records'])} registros Lean integrados válidos; {tests['passed']} controles Python
aprovados; {tests['axiom_report_entries']} declarações distintas no Audit, com axiomas
no trio propext, Classical.choice e Quot.sound. {integration['embedded_files']} arquivos
embutidos. A compilação e os controles são incrementais; o monólito inteiro não foi executado.

Original SHA-256 `{integration['base_sha256']}`.
Cópia SHA-256 `{integration['working_sha256']}`.

| Fonte integrada | SHA-256 lido |
|---|---|
{module_rows}

[Parecer independente](<{review.as_posix()}>): ler ali quais fontes foram recompiladas
pelo revisor e quais evidências de integração foram apenas conferidas por leitura e hash.
Os logs das tentativas com erros de elaboração foram preservados; só execuções com
rc=0 e fontes/binários correspondentes entram na evidência aceita.

O original continua intacto. Não houve transposição canônica, publicação ou novo selo.
O objetivo integral permanece ativo: este incremento reduz uma obrigação, não fecha
o plano nem estabelece confirmação física.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualQuadraticLaws` e `DualClosedForm` compilados e integrados:
homogeneidade e paralelogramo em ENNReal, semicontinuidade inferior por supremo dos
cortes, domínio finito construído como submódulo, subníveis fechados e invariância
unitária pelo comutante da mesma álgebra. D(q_I)={{0}} e D(q_0)=H. Não foi assumida
densidade universal de D(q_A). Semifinitude do peso exige trabalho sobre seu domínio
na álgebra, não essa densidade para cada forma.

{len(build['records'])} registros Lean válidos, {tests['passed']} controles aprovados,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado em relação ao incremento anterior, conferido por AST.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente e escopo](<{review.as_posix()}>).

[OPEN] Representação espectral/cone ampliado da base e pontos fixos; peso fiel normal
semifinito, afiliação do gerador/perturbação/traço, Three Locks, H1/H2/H3 físicos,
setor interagente/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
A construção de forma fechada não quita o traço. Não há novo selo ou transposição.
O objetivo integral segue ativo.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_PESO_DUAL.md')]
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
    'surface_sha256': {str(p): digest(p) for p in surfaces},
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'], 'full_runtime': False,
    'full_goal_complete': False,
}
write_atomic(ROOT / 'closed_form_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
