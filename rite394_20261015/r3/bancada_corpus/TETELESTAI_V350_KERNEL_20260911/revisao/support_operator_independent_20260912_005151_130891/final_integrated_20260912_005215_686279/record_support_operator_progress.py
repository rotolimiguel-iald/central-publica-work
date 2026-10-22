"""Record the reviewed support/operator construction with exact-byte memory backups."""
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
MODULES = ['DualVariational', 'DualFormSupport', 'ResolventGraph', 'DualSupportOperator']
MARKER = 'TETELESTAI_V350_DUAL_SUPPORT_OPERATOR_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')


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
review = ROOT / 'revisao/REVIEW_DUAL_SUPPORT_OPERATOR.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'resolvent_custody.json').read_bytes())
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
report_path = ROOT / 'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md'
rows = '\n'.join(f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
                 for name in MODULES)
report = f'''# Suporte da forma dual e operador auto-adjunto construído

{DATE}. [REAL — Lean incremental em cópia; revisão independente delimitada.]

A partir dos cortes normalizados efetivos C_n e do limite forte R de (I+C_n)⁻¹,
foram provados a minimalidade variacional, o suporte correto e a existência de
um operador positivo auto-adjunto nesse suporte. O teorema final
`exists_dualSupportOperator` recebe somente o perfil P e A≥0 pertencente ao core
regular correspondente. Ele constrói R, o domínio e o operador; não os exige
como hipóteses. Os objetos pertencem à mesma representação regular construída.

## O que passou no kernel

1. Para F_v(w)=‖w-v‖²+q_A(w), com valores em ENNReal, F_v(Rv)≤F_v(w)
   para todo w. A prova usa a identidade de energia dos inversos finitos,
   fixa um corte e passa ao limite forte, depois toma o supremo dos cortes.
   Não subtrai ∞−∞ nem troca indevidamente limites conjuntos.
2. ker R=D(q_A)⊥ e closure(Ran R)=closure(D(q_A)). A direção nova usa
   competidores t·w e i·w no domínio finito e a minimalidade em zero.
   A parte real de um polinômio quadrático não negativo para todo t força
   o coeficiente linear a zero; a aplicação a i·w elimina a parte imaginária.
3. K=closure(D(q_A)) é o suporte construído. A restrição R_K é positiva,
   menor ou igual a I e injetiva em K. Não se presume injetividade em todo H.
4. Em K, define-se D(T)=Ran R_K e T(R_K u)=(I−R_K)u. O grafo satisfaz
   (x,y)∈Graph(T) ↔ (I−R_K)x=R_K y. A recíproca usa u=x+y.
   O grafo é fechado, o domínio é denso, T é positivo e T*=T para o adjunto
   efetivo de LinearPMap da Mathlib. Não se usa um campo que apenas afirme
   a auto-adjunção. A equação (I+T)x=u com x=R_K u também foi provada.

O operador é da classe de operadores com domínio possivelmente próprio;
não se afirma que todo A produza um operador não limitado. Os casos já provados
q_I(v)=∞ para v≠0 e q_0=0 continuam válidos: a construção respeita suporte zero
e suporte total. A densidade de D(T) é em K, não necessariamente em todo H.
O suporte K desta etapa não é ainda o projetor P_F dos Three Locks.

## O que continua faltando para o gate

[OPEN] D(q_A)=D(T^(1/2)) dentro de K, q_A(w)=‖T^(1/2)w‖² e o tratamento
espectral da parte infinita. A construção de T e a minimalidade não são, por
si, a prova dessa identificação completa. Nenhuma nova medida espectral foi
construída aqui. A próxima ligação possível é identificar q_A em Ran R com
Re⟨x,Tx⟩ e provar a extensão aos domínios da forma; isso não está quitado.

[OPEN] Depois: valores no cone ampliado da base/pontos fixos; domínio e
semifinitude do peso operadorial; estado modular da base; gerador afiliado,
perturbação e traço canônico fiel normal semifinito com escala dual;
Three Locks e H1/H2/H3 físicos no mesmo modelo; setor interagente, BRST/QME,
anomalias e UV; contrato dependente ampliado e execução integral do monólito.
A identificação Fourier da normalização (2π)⁻¹ mantém o estatuto anterior:
convenção implementada, identificação pesquisada, ainda não formalizada.

O gate principal da v350 não lê as flags de fronteira. Além de construir as
provas, é necessário fazer a decisão consumir o contrato compatível que as
reúne. Neste incremento o corpo Python permaneceu igual por AST ao estrato
anterior; as seis flags abertas continuam falsas e o gate legado não mudou.

## Evidência e custódia

{len(targets)} alvos novos impressos no auditor, {len(build['records'])} registros Lean
integrados válidos, {tests['passed']} controles Python aprovados e
{tests['axiom_report_entries']} declarações distintas no Audit, com axiomas
contidos em propext, Classical.choice e Quot.sound. {integration['embedded_files']}
arquivos embutidos. Compilação incremental com artefatos de dependências
conferidos; não é recompilação integral do universo de bibliotecas.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

Base `{integration['base_sha256']}`.
Cópia `{integration['working_sha256']}`.

[Parecer independente](<{review.as_posix()}>). Seu escopo distingue a
recompilação independente da inspeção dos registros integrados do autor.
Os logs das tentativas com erros de elaboração foram preservados.
O novo controle impede promover suporte e auto-adjunção a quitação do peso,
traço, canto ou hipóteses físicas. Runtime integral ainda não executado.

Objetivo integral ativo. Original preservado; sem novo selo, transposição
canônica ou confirmação física.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualVariational`, `DualFormSupport`, `ResolventGraph`
e `DualSupportOperator`: F_v(Rv)≤F_v(w), ker R=D(q_A)⊥,
closure(Ran R)=closure(D(q_A)); restrição R_K injetiva no suporte construído;
operador positivo auto-adjunto T, com domínio denso em K e (I+T)⁻¹=R_K.
O teorema existencial final constrói R e T a partir de A≥0 do mesmo core.
O suporte da forma não é o projetor Three Locks. Não há hipótese de
injetividade global, densidade universal ou auto-adjunção pronta.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Igualdade da forma com a raiz quadrada de T e domínios correspondentes;
cone ampliado da base/pontos fixos; peso semifinito, estado modular, gerador
afiliado, perturbação e traço; Three Locks, H1/H2/H3, interações/BRST/QME/
anomalias/UV, contrato ampliado e runtime integral. As seis flags abertas
continuam falsas. Objetivo integral ativo; sem confirmação física.

Adendo à rota variacional: as etapas 1–3 antes DERIVED agora têm os teoremas
compilados descritos acima. A etapa 4, representação completa da forma,
permanece OPEN. O registro anterior é histórico e foi preservado.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_RESOLVENTE_DUAL.md')]
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
write_atomic(ROOT / 'support_operator_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
