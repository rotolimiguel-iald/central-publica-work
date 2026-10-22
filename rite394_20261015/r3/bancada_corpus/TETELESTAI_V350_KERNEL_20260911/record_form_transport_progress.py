"""Record verified transport and faithfulness laws without promoting them to a trace."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MARKER = 'TETELESTAI_V350_DUAL_FORM_TRANSPORT_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MODULES = ['DualFormTransport', 'DualFormFaithfulness']


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
        raise RuntimeError('Already recorded: ' + str(path))
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


assert '--review-read' in sys.argv, 'Read the completed review before recording this stage.'
review = ROOT / 'revisao/REVIEW_DUAL_FORM_TRANSPORT.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'closed_form_custody.json').read_bytes())
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
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
    if source.relative_to(ROOT / 'kernel').as_posix() in new_sources or 'source_unchanged_during_compile' in row:
        assert row.get('source_unchanged_during_compile') is True
for name in ('dualQuadraticIntegral_bimodule', 'dualBaseConjugatedForm_value',
             'dualQuadraticIntegral_transport', 'dualQuadraticIntegral_vector_dual_invariant',
             'dualFiniteDomain_dual_invariant', 'dualQuadraticIntegral_zero_iff_integrand_zero',
             'dualQuadraticIntegral_zero_implies_apply_zero', 'dualQuadraticIntegral_faithful',
             'dualQuadraticIntegral_detects_nonzero_positive', 'dualQuadraticIntegral_mono'):
    target = 'TGLV350.Regular.' + name
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[flag] is False for flag in open_flags)

report_path = ROOT / 'RELATORIO_TRANSPORTE_E_FIDELIDADE_DUAL.md'
rows = '\n'.join(f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
                 for name in MODULES)
report = f'''# Transporte e fidelidade da família de formas duais

{DATE}. [REAL — Lean incremental em cópia; revisão independente delimitada.]

A família q_A agora satisfaz a identidade bimodular, o transporte dual no vetor e
um critério de detecção de operadores positivos. **O peso com valores na base, a
normalidade e a semifinitude desse peso e o traço canônico continuam abertos.**

## O que foi construído

Se b é a amplificação por fibras de um operador da base, então

    q_(b* A b)(v) = q_A(bv).

A identidade de avaliações é demonstrada para operadores A arbitrários usando a
definição total de q. Para construir a forma positiva afiliada resultante, o tipo
exige A≥0 e A na álgebra regular; exige também B na álgebra da base, com b=ι(B).
`base_conjugate_mem` prova que b*Ab permanece no mesmo core e a positividade é
fornecida por conjugação de um operador positivo. `dualBaseConjugatedForm_value`
liga explicitamente as duas formas construídas. Não se substitui a álgebra de base
por uma realização diferente.

Para D_r, o multiplicador que implementa a ação dual, foram provadas

    q_(θ_r A)(v) = q_A(D_(-r)v),
    q_A(D_r v) = q_A(v).

O sinal na primeira igualdade foi conferido na implementação θ_r=Ad(D_r).
A segunda combina a primeira com invariância já provada do integral na entrada.
O domínio finito é preservado: D_r v ∈ D(q_A) se e somente se v ∈ D(q_A).
As igualdades aceitam infinito e não pressupõem que o domínio seja todo o Hilbert.

Para A≥0, a nova fidelidade da família é precisamente

    (∀v, q_A(v)=0) ↔ A=0.

O integrando é contínuo em s. Integral zero implica integrando zero quase em toda
parte; o suporte pleno de Lebesgue e a continuidade tornam a igualdade pontual.
Em s=0, a positividade e a estimativa operatorial já existente na v350 dão A v=0.
Logo, todo A positivo não nulo tem pelo menos um vetor com q_A(v)>0; esse valor pode
ser infinito. Isso não afirma detecção por um único vetor pré-escolhido, nem por
todo vetor não nulo. Também foi provada monotonicidade: A≤B implica q_A(v)≤q_B(v).

## O que esses resultados não entregam

Essas leis pertencem à família de formas na representação concreta. Ainda é
necessário identificar o valor como elemento do cone ampliado da **base**, provar
normalidade e construir o domínio/ideal na álgebra necessário à semifinitude.
A fidelidade da família não é um teorema de fidelidade de um traço ainda não construído.
Invariância da forma pelo transporte dual não substitui o teorema dos pontos fixos.

Depois vêm o peso da base e seu grupo modular, o operador afiliado que implementa
Λ_t e a perturbação que produz o traço, com todas as propriedades exigidas e a lei
τ∘θ_s=e⁻ˢτ. Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente,
contrato dependente ampliado e runtime integral continuam no objetivo ativo.

As oito flags de fronteira continuam fora da função legada da v350. Neste incremento,
o corpo Python foi comparado por AST ao estrato anterior e permaneceu igual;
somente fontes embutidas do kernel e raízes foram acrescentadas/atualizadas.
Nenhuma das seis flags ainda abertas foi quitada por estas leis.

## Evidência

{len(build['records'])} registros Lean integrados válidos; {tests['passed']} controles
Python aprovados; {tests['axiom_report_entries']} declarações distintas no Audit,
com axiomas no trio. {integration['embedded_files']} arquivos embutidos.

Base SHA-256 `{integration['base_sha256']}`.
Cópia SHA-256 `{integration['working_sha256']}`.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

[Revisão independente](<{review.as_posix()}>): o parecer distingue recompilação
independente de inspeção dos logs, fontes e hashes da integração do autor.
Os controles novos impedem que bimodularidade ou fidelidade da família sejam
contabilizadas como construção de peso canônico, traço semifinito ou canto finito.
Os logs das tentativas que falharam foram preservados e não compõem evidência aceita.

O original foi conferido por hash e permanece intacto. Compilação incremental e
controles não substituem a execução integral do monólito; ela ainda não foi feita.
Não houve transposição canônica, publicação ou novo selo.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualFormTransport` e `DualFormFaithfulness`:
q_(b*Ab)(v)=q_A(bv), com b da base; conjugado positivo permanece no mesmo core;
q_(θ_rA)(v)=q_A(D_-rv), q_A(D_rv)=q_A(v) e domínio finito preservado.
Para A≥0, (∀v q_A(v)=0)↔A=0, e A≤B implica q_A(v)≤q_B(v).
Fidelidade aqui é da família de avaliações; não é fidelidade de um traço pronto.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Cone ampliado da base/pontos fixos; normalidade e domínio semifinito do peso;
identificação modular do peso da base, gerador afiliado/perturbação/traço;
Three Locks, H1/H2/H3, interações/BRST/QME/anomalias/UV, contrato ampliado e runtime
integral. Nenhuma flag de core/canto/H1/H2/H3/testemunha total foi quitada nesta etapa.
Objetivo integral ativo; nenhum novo selo, transposição ou confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_FORMA_DUAL_FECHADA.md')]
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
write_atomic(ROOT / 'form_transport_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
