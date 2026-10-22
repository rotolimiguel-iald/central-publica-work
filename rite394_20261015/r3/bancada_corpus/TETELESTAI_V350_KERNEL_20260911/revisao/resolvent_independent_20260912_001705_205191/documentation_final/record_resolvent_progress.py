"""Record the verified strong resolvent limit, preserving every memory's exact prior bytes."""
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
MODULES = ['PositiveResolvent', 'DualResolvent']
MARKER = 'TETELESTAI_V350_DUAL_RESOLVENT_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')


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
review = ROOT / 'revisao/REVIEW_DUAL_RESOLVENT.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'form_normality_custody.json').read_bytes())
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
    if source.relative_to(ROOT / 'kernel').as_posix() in new_sources:
        assert row.get('source_unchanged_during_compile') is True
targets = set()
for name in MODULES:
    content = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    targets.update('TGLV350.Regular.' + target for target in
                   re.findall(r'^#print axioms ([\w]+)$', content, re.M))
for target in targets:
    assert target in evidence['axiom_report']
    assert set(evidence['axiom_report'][target]) <= {'propext', 'Classical.choice', 'Quot.sound'}
open_flags = ('qgf_continuous_modular_realization_constructed',
              'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
              'gpf_H1_internal_susy_relative_gap_discharged',
              'gpf_H2_smooth_modular_four_frame_discharged',
              'gpf_H3_local_horizon_equilibrium_discharged')
assert all(evidence[flag] is False for flag in open_flags)
report_path = ROOT / 'RELATORIO_RESOLVENTE_DUAL.md'
rows = '\n'.join(f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
                 for name in MODULES)
report = f'''# Resolvente dos cortes duais e domínio finito

{DATE}. [REAL — Lean incremental em cópia; revisão independente delimitada.]

Foi construído o limite forte R dos inversos (I+C_n)⁻¹ dos cortes normalizados
efetivos C_n=(2π)⁻¹∫_[-n,n] θ_s(A)ds. Para A positivo no core regular já construído,
R pertence à mesma álgebra, satisfaz 0≤R≤I e é o ínfimo dessa família no ambiente
de operadores limitados. Não se presume uma cota inferior estritamente positiva.

## Ligação que foi provada

Para cada vetor v da representação original:

    q_A(Rv) ≤ ‖v‖²/4 < ∞; portanto Ran R ⊆ D(q_A).

A cota vale para a integral dual efetiva, não para uma forma definida a posteriori
com o nome q. O fator (2π)⁻¹ é o mesmo dos cortes e da integral. Sua identificação
como normalização de Haar dual via Fourier continua na pendência já registrada.

O caso A=I dá R=0, pois D(q_I)={{0}}. O caso A=0 dá R=I. Os resolventes finitos
são injetivos; a prova não transfere essa propriedade indevidamente ao limite.
Isso conserva a parte infinita da forma, em vez de apagá-la por uma hipótese de
domínio denso universal.

## Passos da prova

1. Positividade de C garante que I+C é uma unidade estritamente positiva. Sua
   inversa é positiva, menor ou igual a I e inverte a ordem entre C e D.
2. O cálculo direto dos comutantes mostra que o inverso permanece na álgebra.
   A família I-(I+C_n)⁻¹ é crescente, positiva e limitada. O teorema de convergência
   monótona já existente produz seu limite forte; o fechamento WOT o mantém na
   mesma álgebra. Subtrair esse limite de I produz R e a propriedade de ínfimo.
   O lema abstrato aceita índices preordenados, dirigidos e não vazios; a aplicação
   aos cortes usa os intervalos inteiros de exaustão.
3. A equação (I+C_n)r_n=v implica
   Re⟨r_n,C_n r_n⟩=Re⟨r_n,v⟩-‖r_n‖²≤‖v‖²/4 por Cauchy–Schwarz.
   Para m≤n, o corte C_m tem energia menor que C_n. Fixando m e passando ao limite
   forte de r_n, a continuidade da forma limitada de C_m preserva a cota.
4. Tomar o supremo em m recupera exatamente q_A(Rv), pelo lema de exaustão.
   Não se trocam limites de duas variáveis nem se subtraem valores infinitos.

## O que ainda falta no caminho do gate

[OPEN] A inclusão Ran R⊆D(q_A) ainda não é a representação espectral da forma.
É necessário provar a identificação variacional/espectral completa, incluindo
o suporte correto (por exemplo ker R=D(q_A)⊥), a igualdade da forma com o operador
não limitado e os domínios correspondentes. Não foi construído ainda um operador
não limitado auto-adjunto representando q_A, nem uma medida espectral nova.

[OPEN] Depois: cone ampliado da base/pontos fixos; domínio e semifinitude do peso
operadorial; estado modular da base; gerador afiliado, perturbação e traço canônico
fiel normal semifinito com escala dual; Three Locks no mesmo modelo; H1/H2/H3 físicos
compatíveis; setor interagente/BRST/QME/anomalias/UV; contrato dependente ampliado;
runtime integral. Nenhuma das seis flags abertas foi quitada por este incremento.

O gate principal da v350 não lê essas flags de fronteira. Além de cumprir as provas,
é necessário fazer a decisão consumir o contrato compatível que as reúne. A subdecisão
experimental existente continua apenas com o alcance modular anteriormente provado.

## Evidência

{len(targets)} alvos novos impressos no auditor; {len(build['records'])} registros Lean
integrados válidos; {tests['passed']} controles Python aprovados;
{tests['axiom_report_entries']} declarações distintas no Audit com axiomas no trio.
{integration['embedded_files']} arquivos embutidos. Compilação incremental e auditoria
de hashes; a execução integral do monólito continua pendente.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

Base SHA-256 `{integration['base_sha256']}`.
Cópia SHA-256 `{integration['working_sha256']}`.

[Parecer independente](<{review.as_posix()}>). O parecer delimita o que recompilou
e o que conferiu por inspeção da integração do autor. As falhas históricas de elaboração
foram preservadas, fora da evidência aceita. O controle adicional verifica que limite
forte e domínio finito não sejam promovidos a certificado de peso, traço ou Three Locks.

Corpo Python/gate igual por AST ao estrato anterior; original preservado por hash.
Objetivo integral ativo. Não houve novo selo, transposição canônica ou confirmação física.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `PositiveResolvent` e `DualResolvent` constroem o limite forte
R dos inversos dos cortes duais normalizados da mesma álgebra, com 0≤R≤I e propriedade
de ínfimo. Foi provado q_A(Rv)≤‖v‖²/4, logo Ran R⊆D(q_A). Para A=I, R=0; para A=0,
R=I. A injetividade dos inversos finitos não é presumida no limite.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Identificação variacional/espectral completa da forma e suporte/domínios;
cone ampliado da base/pontos fixos; peso semifinito, estado modular, gerador afiliado,
perturbação e traço; Three Locks, H1/H2/H3, interações/BRST/QME/anomalias/UV,
contrato ampliado e runtime integral. Nenhuma flag de core/canto/H1/H2/H3/testemunha
total foi quitada. Objetivo integral ativo; sem transposição ou confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_NORMALIDADE_DUAL.md')]
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
write_atomic(ROOT / 'resolvent_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
