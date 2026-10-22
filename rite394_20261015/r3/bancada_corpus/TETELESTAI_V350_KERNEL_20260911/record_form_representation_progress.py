"""Record the reviewed full form representation with exact-byte memory backups."""
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
MODULES = ['DualSquareRootFormBound', 'DualFormVariationalBound', 'DualFormRepresentation']
MARKER = 'TETELESTAI_V350_DUAL_FORM_REPRESENTATION_20260912'
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
review = ROOT / 'revisao/REVIEW_DUAL_FORM_REPRESENTATION.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'square_root_custody.json').read_bytes())
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
report_path = ROOT / 'RELATORIO_REPRESENTACAO_DA_FORMA_DUAL.md'
report = f'''# Representação completa da forma dual

{DATE}. [REAL — Lean incremental em cópia, revisão independente delimitada.]

As duas inclusões de domínio e a igualdade de energia estão demonstradas:
D(q_A)=D(S) no suporte K=closure(D(q_A)), e q_A(x)=ofReal(‖Sx‖²) para
todo x∈D(S). No Hilbert ambiente, q_A(w)<∞ se e somente se w é o vetor
subjacente de algum x∈D(S). O suporte continua sendo construído da forma;
não se presume que seja todo o espaço, não nulo ou o projetor Three Locks.

## Como as duas inclusões foram obtidas

1. D(S)⊆D(q_A): escrever S(Bu)=Cu, B=√R_K, C=√(I−R_K).
   A energia já coincide em D(T)=Ran(B²). Ran B é densa no espaço
   dos parâmetros. O epígrafo fechado da forma e a continuidade de
   u↦‖Cu‖² estendem a cota para todo u: q_A(Bu)≤ofReal(‖Cu‖²).
   A finitude resulta dessa cota; não é assumida na passagem ao limite.
2. D(q_A)⊆D(S): a minimalidade em Rv fornece, para w de energia finita,
   2 Re⟨w,v⟩≤Re⟨Rv,v⟩+‖w‖²+q_A(w).toReal.
   No suporte, Re⟨R_Kv,v⟩=‖Bv‖². Testar escalas reais e a fase
   complexa dá |⟨w,v⟩|≤sqrt(c)‖Bv‖, c=‖w‖²+q_A(w).toReal.
   Estender esse funcional pela imagem densa de B e aplicar Riesz
   constrói z com Bz=w e ‖z‖²≤c. B²+C²=I fornece
   ‖Cz‖²≤q_A(w).toReal, isto é, a cota oposta para S.
3. As cotas se encontram. `exists_dualFormRepresentation` recebe apenas
   o perfil P e A≥0 pertencente ao core regular e constrói R,T,S com
   os vínculos: limite dos mesmos cortes, resolvente de T, S²=T com
   domínio, auto-adjunção efetiva, domínio finito da forma e energia.

`toReal` só é usado após prova de finitude. A fase complexa é testada
explicitamente; não se troca o módulo do produto interno pela parte real.
A extensão de Riesz recebe densidade e estimativa demonstradas; nenhuma
preimagem ou igualdade de domínio é entregue como hipótese ao existencial.
As identidades valem inclusive quando K={{0}}. A forma sobre o ambiente
pode tomar ∞; não se declara um operador densamente definido no ambiente
inteiro nesses casos.

## O que continua aberto para o gate

[OPEN] Identificar o cone ampliado da base/pontos fixos e construir nele
o peso operadorial. Demonstrar semifinitude do domínio do peso na álgebra,
estado modular da base, gerador afiliado e perturbação que produz o traço
canônico fiel normal semifinito, com sua escala dual. A representação
vetorial da forma provada aqui não é, sozinha, esse peso ou esse traço.

[OPEN] Three Locks e H1; H2 (quadro modular e identificação geométrica),
H3 (área/calor/equilíbrio no mesmo horizonte físico); setor quântico
interagente, BRST/QME, anomalias e UV; contrato dependente efetivamente
consumido pelo gate; execução integral isolada do monólito. Unicidade
abstrata da raiz e cálculo espectral não limitado completo não são
reivindicados. A identificação Fourier da normalização (2π)⁻¹ continua
com o estatuto anterior; não é inferida deste teorema de representação.

As seis flags abertas continuam falsas. Corpo Python e gate legado
inalterados por AST em relação ao estrato anterior. Não houve execução
integral, transposição canônica, publicação ou confirmação física.

## Evidência

{len(targets)} alvos novos (5+3+8), {len(build['records'])} registros Lean
integrados válidos, {tests['passed']} controles aprovados,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas
contidos no trio propext/Classical.choice/Quot.sound; {integration['embedded_files']}
arquivos embutidos. Compilação incremental com dependências conferidas;
não é recompilação integral da biblioteca nem runtime completo do um.py.

Base `{integration['base_sha256']}`.
Cópia `{integration['working_sha256']}`.

[Revisão independente](<{review.as_posix()}>).
O parecer distingue recompilações próprias da inspeção dos logs integrados.
Os relatórios anteriores continuam como estratos históricos: as pendências
de domínio/energia que registravam foram resolvidas neste novo pacote.
O objetivo integral permanece ativo.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualSquareRootFormBound`, `DualFormVariationalBound`,
`DualFormRepresentation`: D(q_A)=D(S) no suporte construído K e
q_A(x)=ofReal(‖Sx‖²) em todo D(S). No ambiente, energia finita equivale
à existência do mesmo vetor em D(S). Epígrafo fechado/densidade dão uma
inclusão; estimativa variacional ótima, extensão contínua e Riesz dão a
outra. O existencial constrói R,T,S para A≥0 no mesmo core regular.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit; {len(targets)}
alvos novos. Axiomas no trio. Base `{integration['base_sha256']}`;
cópia `{integration['working_sha256']}`. Corpo Python/gate inalterado por AST.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

Adendo aos estratos anteriores: as duas inclusões de domínio e a extensão
da energia, então abertas, agora estão provadas. K pode ser zero e não é
P_F. Não confundir domínio vetorial da forma com domínio de peso na álgebra.
[OPEN] Cone ampliado da base, peso e semifinitude, estado modular,
gerador/perturbação/traço; Three Locks/H1/H2/H3; interações/BRST/QME/anomalias/UV;
contrato dependente ampliado e runtime integral. Unicidade abstrata da raiz
e cálculo espectral completo não reivindicados. Seis flags abertas false;
objetivo integral ativo; sem confirmação física. Backups e história preservados.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md', 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md')]
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
    'full_form_representation': True, 'full_goal_complete': False,
}
write_atomic(ROOT / 'form_representation_custody.json',
             json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
