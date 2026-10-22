"""Record only verified dual-integral work, with byte-preserving memory backups."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
ORIGINAL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
MARKER = 'TETELESTAI_V350_DUAL_WEIGHT_CUTS_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MODULES = ['StrongOperatorIntegral', 'DualWeightCuts', 'DualWeightForm', 'DualWeightExhaustion']


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
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    temp.write_bytes(raw)
    assert temp.stat().st_size == len(raw) > 0 and temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw


def append(path, text):
    before = path.read_bytes() if path.exists() else b''
    if MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    raw = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    assert raw.startswith(before) and len(raw) > len(before)
    write_atomic(path, raw)


integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
assert all(row['passed'] for row in tests['checks'])
assert not tests['full_monolithic_runtime_run']
assert digest(ROOT / 'um.py') == tests['working_um_sha256'] == integration['working_sha256']
assert digest(ORIGINAL) == digest(ROOT / 'fontes/um_v350_original.py') == integration['base_sha256']
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']
    relative = source.relative_to(ROOT / 'kernel').as_posix()
    new_sources = {'TGLExt/V350' + name + '.lean' for name in MODULES} | {'TGLExt.lean', 'TGL/Audit.lean'}
    if relative in new_sources:
        assert row.get('source_unchanged_during_compile') is True
    elif 'source_unchanged_during_compile' in row:
        assert row['source_unchanged_during_compile'] is True
    # Older accepted records predate this field. Their source and binary hashes
    # were verified above; do not manufacture a historical freeze observation.
targets = [
    'TGLV350.StrongIntegral.operatorIntegral_mem',
    'TGLV350.Regular.dualWeightCut_mono_radius',
    'TGLV350.Regular.dualQuadraticIntegral_add',
    'TGLV350.Regular.dualQuadraticIntegral_dual_invariant',
    'TGLV350.Regular.dualQuadraticIntegral_eq_iSup_cuts',
    'TGLV350.Regular.dual_unit_cut_supremum_infinite',
]
for name in targets:
    assert name in evidence['axiom_report']
    assert set(evidence['axiom_report'][name]) <= {'propext', 'Classical.choice', 'Quot.sound'}
assert evidence['qgf_continuous_modular_realization_constructed'] is False
assert evidence['qgf_unconditional_continuous_corner_proved'] is False
assert evidence['qgf_full_TGL_witness_constructed'] is False
review = ROOT / 'revisao/REVIEW_DUAL_WEIGHT_CUTS.md'
assert review.is_file(), 'Independent review must be received and read before recording completion.'

module_rows = '\n'.join(
    f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
    for name in MODULES)
report = f'''# Integral da ação dual: avanço e obrigações restantes

{DATE}. [REAL — quatro módulos compilados na cópia isolada; escopo de revisão no parecer.]

O avanço é a construção de integrais fortes finitas e de sua avaliação positiva ampliada
na mesma representação regular. **Ainda não é o peso dual canônico nem o traço do core.**
Nenhuma flag de core, canto, H1/H2/H3 ou testemunha completa foi quitada por este incremento.

Para X positivo, foram construídos

    T_R(X)v = ∫[-R,R] θ_s(X)v ds,
    q_X(v) = (1/(2π)) ∫ℝ ofReal(Re⟨v,θ_s(X)v⟩) ds.

O primeiro integral é Bochner em vetores. Ele produz um operador limitado, com norma
≤ 2R‖X‖ para R≥0, e pertence à mesma álgebra de von Neumann dos integrandos. Não foi
pressuposta integração Bochner de θ_s(X) na norma de B(H).

[REAL — Lean] Positividade e monotonicidade dos cortes em R; permanência no mesmo core;
T_R(ι(a))=2Rι(a); aditividade de q em entradas positivas; invariância q_θr(X)=q_X;
igualdade da avaliação de T_R com integral escalar restrito; e, sem hipótese de finitude,

    q_X(v) = sup[n∈ℕ] (1/(2π))·ofReal(Re⟨v,T_n(X)v⟩).

Para todo v≠0, q_I(v)=∞. Logo esse limite não é um estado normalizado nem foi promovido
a supremo limitado em B(H). A expressão foi definida para toda entrada usando ofReal;
as leis de peso aqui verificadas têm explicitamente entradas positivas.

[INPUT — convenção implementada; DERIVED — compatibilidade de Fourier na nota]
A constante é (2π)⁻¹ para Lebesgue dt e caracteres exp(−ist). Ela não depende de R.
Seu valor foi escolhido segundo a medida dual da convenção adotada. O arquivo Lean
ainda não prova o teorema de Fourier que identifica essa medida dual.
[Fonte primária: Hiai, Teorema 10.13](https://arxiv.org/pdf/2004.02383#page=96).
[Pesquisa e derivação de sinais](<{(ROOT / 'revisao/DUAL_WEIGHT_CONSTRUCTION.md').as_posix()}>).
Multiplicar τ por uma constante positiva preserva a lei de escala. A tabela anterior
de sinais em CONVENCOES_DO_TRACO.md fixava densidades compatíveis, não a constante.
Fixar adicionalmente τ(P)=1 é uma escolha que requer conferir a normalização usada.

## O que continua faltando para o traço

1. Construir o cone positivo ampliado e colocar o integral nele; identificar os pontos
   fixos da ação dual com a imagem da álgebra de base. A família finita não está em geral
   nessa imagem. As leis quadráticas em v e sua semicontinuidade ainda não foram formalizadas.
2. Exibir domínio finito denso, provando a identidade dos integrados e a semifinitude.
   A existência de cortes positivos não fornece esse domínio por si só.
3. Compor com o peso fiel normal da base e identificar seu grupo modular na mesma
   realização. Preservar um estado e normalizar uma álgebra não basta para essa identificação.
4. Construir o operador afiliado A com Λ_t=A^it e a perturbação
   τ=(φ̃)_{{A⁻¹}}; provar fidelidade, normalidade, semifinitude, propriedade tracial e
   τ∘θ_s=e⁻ˢτ. Essa é a rota publicada; tais etapas não foram quitadas em Lean aqui.

Depois vêm o canto dos Three Locks com 0<τ(P_F)<∞, H1/H2/H3 compatíveis, setor quântico
interagente e o contrato dependente consumido pelo gate. O contrato antigo de core ainda
precisa ser fortalecido: o contraexemplo de traço zero permanece válido e não passa Three Locks.
[Peças da torre já existentes e próximo passo](<{(ROOT / 'ROTA_APOS_CORTES_DUAIS.md').as_posix()}>).

## Evidência da integração

{len(build['records'])} registros Lean integrados válidos; {tests['passed']} controles Python
aprovados; {tests['axiom_report_entries']} declarações distintas no Audit, com axiomas
limitados a propext, Classical.choice e Quot.sound. Os controles novos verificam que
a integral ampliada não quite o traço e que a unidade infinita não quite o canto finito.

Base original SHA-256 `{integration['base_sha256']}`.
Cópia experimental SHA-256 `{integration['working_sha256']}`.

| Fonte integrada | SHA-256 lido do arquivo |
|---|---|
{module_rows}

[Revisão independente e seus limites](<{review.as_posix()}>).
A revisão das fontes e a integração pelo autor são evidências distintas; a abrangência
exata das recompilações independentes está no parecer. O incremento não recebe uma
declaração de revisão da execução integral: ela continua pendente.

Os arquivos originais não foram alterados. Logs das tentativas que falharam foram preservados.
A compilação é incremental com dependências verificadas; não houve execução integral do
monólito, transposição canônica ou publicação. O objetivo integral continua ativo.
'''
write_atomic(ROOT / 'RELATORIO_PESO_DUAL.md', report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — cópia isolada] Quatro módulos novos: StrongOperatorIntegral, DualWeightCuts,
DualWeightForm, DualWeightExhaustion. Integrais fortes em vetores pertencem à mesma
álgebra; cortes positivos crescentes; avaliação ENNReal aditiva em positivos e invariante
pela ação dual; igualdade exata com supremo dos cortes; q_I(v)=∞ para v≠0.
Constante (2π)⁻¹ implementada [INPUT de convenção]; identificação como Haar dual é
[DERIVED na pesquisa], ainda não teorema Fourier compilado. Não é média dividida por 2R.

Integração: {len(build['records'])} registros Lean válidos, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit com axiomas no trio.
Base lida `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
[Relatório](<{(ROOT / 'RELATORIO_PESO_DUAL.md').as_posix()}>).
[Parecer independente com escopo](<{review.as_posix()}>).
[Inventário das peças reutilizáveis da base](<{(ROOT / 'ROTA_APOS_CORTES_DUAIS.md').as_posix()}>).

[OPEN] Cone ampliado/pontos fixos, domínio finito denso/semifinitude, peso da base/grupo
modular, afiliação/perturbação/traço, Three Locks e H1/H2/H3 físicos compatíveis,
setor interagente/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
O gate legado permanece; a subdecisão quita apenas a parte modular anterior.
Nada neste incremento é confirmação física. Objetivo integral ativo.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md',
    'MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md',
    'TRACO_PROXIMAS_OBRIGACOES.md')]
surfaces += [CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md']
for surface in surfaces:
    append(surface, note)
    assert MARKER.encode() in surface.read_bytes()
conventions = ROOT / 'CONVENCOES_DO_TRACO.md'
append(conventions, f'''

## {MARKER} — {DATE}: normalização além do sinal

[DERIVED — convenção de Haar/Fourier; ainda não teorema Lean de Fourier]
Para dt de Lebesgue e caracteres exp(−ist), a medida dual usada na construção de
Hiai é ds/(2π). A tabela anterior determina o sinal da densidade, mas não sua
constante multiplicativa. A mesma lei τ∘θ_s=e⁻ˢτ vale para qualquer múltiplo
positivo de τ; ela sozinha não autoriza dizer que τ(P)=1.
Os cortes implementados usam (2π)⁻¹ fixo e não dividem pelo comprimento 2R.
O traço canônico continua aberto. Ver revisao/DUAL_WEIGHT_CONSTRUCTION.md e
RELATORIO_PESO_DUAL.md. A escolha de medida é preservada como entrada explícita.
''')
surfaces.append(conventions)
custody = {
    'timestamp': DATE, 'original_unchanged': True,
    'original_sha256': digest(ORIGINAL), 'working_sha256': digest(ROOT / 'um.py'),
    'modules': {name: digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean')) for name in MODULES},
    'review_sha256': digest(review), 'report_sha256': digest(ROOT / 'RELATORIO_PESO_DUAL.md'),
    'surface_sha256': {str(p): digest(p) for p in surfaces},
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'], 'full_runtime': False,
    'full_goal_complete': False,
}
write_atomic(ROOT / 'dual_weight_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
