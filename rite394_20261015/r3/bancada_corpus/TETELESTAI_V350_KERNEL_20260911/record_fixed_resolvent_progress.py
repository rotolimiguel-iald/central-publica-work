"""Record the reviewed dual-fixed resolvent with exact-byte memory backups."""
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
MODULES = ['FormMinimizerUniqueness', 'DualResolventFixed', 'DualFixedCore']
MARKER = 'TETELESTAI_V350_DUAL_FIXED_RESOLVENT_20260912'
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
review = ROOT / 'revisao/REVIEW_DUAL_FIXED_RESOLVENT.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'form_representation_custody.json').read_bytes())
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
report_path = ROOT / 'RELATORIO_RESOLVENTE_FIXO_DUAL.md'
report = f'''# Resolvente na álgebra de pontos fixos da ação dual

{DATE}. [REAL — prova Lean em cópia, compilação incremental e revisão independente delimitada.]

Para o mesmo A≥0 no core regular N, o resolvente R construído dos cortes
satisfaz θ_s(R)=R para todo s. Ele pertence à álgebra de von Neumann
F=N∩{{D_s}}', construída explicitamente. O existencial entrega os mesmos
R,T,S da representação completa da forma, acrescentando R∈F.

## Cadeia demonstrada

1. `ClosedPositiveForm.minimizer_unique`: o funcional
   ‖w−v‖²+q(w) tem no máximo um minimizador. A comparação com w=0 prova
   primeiro a finitude; a cota convexa no ponto médio e o paralelogramo
   da norma forçam a igualdade. Não se assume positividade estrita de q
   nem domínio finito denso. Este lema isolado não afirma existência.
2. Se uma isometria unitária e preserva q, transporta minimizadores.
   Unicidade fornece R(e v)=e(Rv). Na forma dual construída, e=D_s,
   logo R comuta com todos os implementadores duais e θ_s(R)=R.
   A mesma prova vale para unitários no comutante de N.
3. `dualFixedCore` é o comutante estrela de N'∪{{D_s}}. O lema de
   pertinência demonstra exatamente R∈F ↔ R∈N e ∀s, θ_s(R)=R.
   A base amplificada está contida em F. A inclusão inversa não foi provada.
4. `exists_dualFixedFormRepresentation` conserva os testemunhos R,T,S:
   limite dos cortes do mesmo A, R positivo e contrativo, T e S fechados,
   densamente definidos e auto-adjuntos no suporte K, S positivo, S²=T
   com domínio, D(q)=D(S), q(x)=ofReal(‖Sx‖²), e equação do resolvente.
   A fixação de R não é uma hipótese de entrada nem uma existência
   separada, desligada do operador que representa a forma.

O suporte K continua sendo closure(D(q)); pode ser zero. Nenhum projetor
Three Locks, domínio finito denso no ambiente ou traço finito foi assumido.
A construção de F não pressupõe que F seja a base original: isso exige
outro teorema. Também não se declara aqui afiliação completa de T/S a F,
cone ampliado com todas as operações, peso operadorial ou semifinitude.

## Próximas obrigações que podem alimentar o gate

[OPEN] Identificação F=base amplificada e colocação do operador positivo
ampliado nessa base, incluindo o setor infinito. Peso operadorial com
suas leis, semifinitude na álgebra, estado modular da base, gerador e
perturbação que produz o traço canônico fiel normal semifinito e sua escala.
O domínio vetorial finito da forma não substitui o domínio do peso na álgebra.

[OPEN] Three Locks/H1, H2 (quadro modular e geometria), H3 (horizonte,
área/calor/equilíbrio na mesma realização); setor quântico interagente,
BRST/QME/anomalias/UV; contrato dependente ampliado consumido pelo gate;
runtime completo e isolado do monólito. O sinal e a normalização do traço
não se deduzem deste pacote. Unicidade abstrata da raiz e cálculo espectral
não limitado completo continuam sem reivindicação.

As seis flags dessa fronteira permanecem falsas. Corpo Python e gate legado
iguais ao estrato anterior por AST, excetuado o conteúdo Lean embutido.
Nenhum original modificado, runtime integral, publicação ou confirmação física.

## Evidência e limites da verificação

{len(targets)} alvos novos (3+6+7, incluindo duas definições),
{len(build['records'])} registros Lean integrados válidos,
{tests['passed']} controles aprovados, {tests['axiom_report_entries']}
declarações distintas no Audit e {integration['embedded_files']} arquivos
embutidos. Axiomas dos alvos contidos em propext/Classical.choice/Quot.sound.
Dependências válidas reutilizadas com hashes; não é rebuild completo da biblioteca.

Base `{integration['base_sha256']}`.
Cópia `{integration['working_sha256']}`.

[Revisão independente](<{review.as_posix()}>).
O parecer distingue recompilações próprias da leitura dos logs integrados.
Os relatórios anteriores permanecem históricos, com adendo datado.
O objetivo integral permanece ativo.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `FormMinimizerUniqueness`, `DualResolventFixed`,
`DualFixedCore`: a unicidade do minimizador variacional implica
R(D_s v)=D_s(Rv) e θ_s(R)=R. Construída a álgebra de von Neumann
F=N∩{{D_s}}' e provada a inclusão da base amplificada em F. O existencial
entrega os mesmos R,T,S da representação completa da forma, agora com R∈F.
A finitude dos minimizadores precede toReal; estritude vem da distância
quadrática. Domínio da forma não precisa ser denso no ambiente; K pode ser zero.

{len(targets)} alvos novos, {len(build['records'])} registros Lean,
{tests['passed']} controles, {tests['axiom_report_entries']} declarações
distintas no Audit. Axiomas no trio. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python/gate inalterado por AST.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

Adendo: a fixação do resolvente e a álgebra concreta fixa agora estão provadas.
[OPEN] Inclusão inversa F⊆base, cone ampliado/afiliação com setor infinito,
peso e semifinitude na álgebra, estado modular/gerador/perturbação/traço;
Three Locks/H1/H2/H3; interações/BRST/QME/anomalias/UV; contrato ampliado e
runtime integral. Não confundir finitude vetorial com semifinitude do peso.
Seis flags abertas false, objetivo integral ativo, sem confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md',
    'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md')]
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
    'same_form_resolvent_dual_fixed': True, 'fixed_algebra_identified_with_base': False,
    'canonical_trace_constructed': False, 'full_goal_complete': False,
}
write_atomic(ROOT / 'fixed_resolvent_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
