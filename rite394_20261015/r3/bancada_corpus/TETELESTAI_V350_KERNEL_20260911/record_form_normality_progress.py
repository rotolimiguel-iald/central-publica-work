"""Record proved order normality of dual form evaluations, not a completed trace."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MARKER = 'TETELESTAI_V350_DUAL_FORM_NORMALITY_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MODULES = ['DualCutNormality', 'DualFormNormality']


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
review = ROOT / 'revisao/REVIEW_DUAL_FORM_NORMALITY.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'form_transport_custody.json').read_bytes())
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
for name in ('intervalIntegral_tendsto_of_uniform', 'dualRealQuadratic_continuous',
             'dualRealQuadratic_mono', 'dualAmbient_tendsto_strong',
             'dualRealQuadratic_uniform_on_compact', 'dualWeightCut_tendsto_quadratic',
             'dualQuadraticIntegral_of_monotone_strong_limit',
             'dualQuadraticIntegral_preserves_positive_isLUB',
             'dualQuadraticIntegral_preserves_internal_isLUB',
             'regularDualForm_preserves_internal_isLUB'):
    target = 'TGLV350.Regular.' + name
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[flag] is False for flag in open_flags)

report_path = ROOT / 'RELATORIO_NORMALIDADE_DUAL.md'
rows = '\n'.join(f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
                 for name in MODULES)
report = f'''# Normalidade da família de formas duais

{DATE}. [REAL — Lean incremental em cópia, com revisão independente delimitada.]

A integral dual preserva agora supremos positivos dirigidos na mesma álgebra
regular. A prova aceita redes não enumeráveis e o supremo **interno** à álgebra;
convergência forte e normalidade não são hipóteses do enunciado final.
O peso com valores na base, sua semifinitude e o traço canônico permanecem abertos.

## Enunciado entregue

Para qualquer tipo de índices ι não vazio, preordenado e dirigido, qualquer rede
A_i≥0 monótona no core regular e qualquer S que seja seu supremo interno, foi provado,
para todo vetor v da mesma representação:

    q_S(v) = sup_i q_(A_i)(v).

`regularDualForm_preserves_internal_isLUB` tem explicitamente a álgebra
`regularCoreAlgebra P` dos módulos anteriores. Seu enunciado não exige que a rede
seja enumerável, não troca um supremo interno por um supremo ambiente presumido e
aceita valores infinitos. A existência de um supremo para redes positivas limitadas
em ordem é fornecida pelo módulo `RegularNormality` já construído; este incremento
prova a preservação desse supremo pela família de avaliações q.

## Como a prova fecha

1. Conjugação pela implementação dual preserva convergência forte em qualquer filtro.
   As avaliações reais são contínuas no parâmetro s e crescem com A.
2. O teorema de Dini da mathlib, cuja assinatura aceita um preordenado arbitrário,
   fornece convergência uniforme em cada compacto. A estimativa da integral pelo
   comprimento do intervalo transforma isso em convergência de cada corte real.
3. Cada corte normalizado está abaixo de q_(A_i)(v). Passando ao limite da rede,
   o corte de S fica abaixo de sup_i q_(A_i)(v). O supremo dos cortes é q_S(v),
   pelo teorema de exaustão já construído. A desigualdade inversa vem da monotonicidade.
   Não se invoca um teorema de convergência monótona de sequências para uma rede arbitrária.
4. O limite forte é construído pelo teorema de operadores positivos monótonos da v350.
   Sua unicidade como supremo o identifica com S. O fechamento da álgebra de von Neumann
   e a equivalência dos supremos internos/ambientes, já provados em `RegularNormality`,
   eliminam a hipótese de convergência forte no enunciado final.

## Alcance no caminho do gate

[REAL] Normalidade **em ordem da família de formas**: preservação de todos os supremos
positivos dirigidos que existem no core regular. Ela se soma à aditividade positiva,
homogeneidade, fechamento, bimodularidade e fidelidade das avaliações já demonstrados.

[OPEN] Identificar essas formas com valores no cone ampliado da **base**; representação
espectral/pontos fixos; domínio/ideal semifinito do peso; peso da base com o grupo modular
correto; gerador afiliado da implementação regular; perturbação que constrói o traço
fiel, normal e semifinito e sua lei τ∘θ_s=e⁻ˢτ. Não há promoção das avaliações a um peso
com valores na base enquanto essa identificação permanecer ausente.

Three Locks no mesmo modelo, H1/H2/H3 físicos compatíveis, setor quântico interagente,
BRST/QME/anomalias/UV, contrato dependente ampliado e runtime monolítico continuam abertos.
Nenhuma das seis flags ainda abertas foi quitada neste incremento. O corpo Python e
o gate permanecem iguais por AST ao estrato anterior; mudaram somente os dois novos
módulos embutidos e as raízes que os importam e auditam.

## Evidência

{len(build['records'])} registros Lean integrados válidos; {tests['passed']} controles
Python aprovados; {tests['axiom_report_entries']} declarações distintas no Audit,
com axiomas restritos ao trio. {integration['embedded_files']} arquivos embutidos.

Base SHA-256 `{integration['base_sha256']}`.
Cópia SHA-256 `{integration['working_sha256']}`.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

[Revisão independente](<{review.as_posix()}>). O parecer separa recompilação independente
dos módulos/auditor próprio de inspeção das fontes, hashes e logs da integração do autor.
Tentativas de elaboração que falharam foram preservadas; não integram a evidência aceita.
O controle novo impede que normalidade da família seja contada como construção de peso
com valores na base, traço canônico ou canto de Three Locks.

O original foi conferido por hash e permanece intacto. Runtime integral ainda não executado.
Objetivo integral ativo; nenhum novo selo, transposição canônica, publicação ou confirmação física.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualCutNormality` e `DualFormNormality`:
q_S(v)=sup_i q_(A_i)(v) para toda rede positiva monótona, em preordenado dirigido
não vazio, com S seu supremo interno ao mesmo core regular. Não há hipótese de
enumerabilidade, normalidade ou convergência forte no enunciado final.
Dini em compactos + limites de cortes + exaustão provam a igualdade; o limite forte
é construído e identificado com o supremo interno usando os módulos anteriores.
Trata-se de normalidade em ordem das avaliações, ainda sem peso com valores na base.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Cone ampliado da base/representação espectral/pontos fixos; domínio e
semifinitude do peso; estado modular da base, gerador afiliado, perturbação e traço;
Three Locks, H1/H2/H3, interações/BRST/QME/anomalias/UV, contrato ampliado e runtime
integral. Nenhuma flag de core/canto/H1/H2/H3/testemunha total foi quitada nesta etapa.
Objetivo integral ativo; nenhum novo selo, transposição ou confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_TRANSPORTE_E_FIDELIDADE_DUAL.md')]
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
write_atomic(ROOT / 'form_normality_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
