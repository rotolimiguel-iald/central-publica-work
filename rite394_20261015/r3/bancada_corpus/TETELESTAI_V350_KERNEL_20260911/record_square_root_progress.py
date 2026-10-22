"""Record the reviewed energy/square-root construction with exact-byte memory backups."""
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
MODULES = ['DualEnergyOnResolvent', 'PartialOperatorSquare', 'ResolventSquareRoot', 'DualSquareRoot']
MARKER = 'TETELESTAI_V350_DUAL_SQUARE_ROOT_20260912'
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
review = ROOT / 'revisao/REVIEW_DUAL_ENERGY_AND_SQUARE_ROOT.md'
assert review.is_file() and review.stat().st_size > 500
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
previous = json.loads((ROOT / 'support_operator_custody.json').read_bytes())
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
checkpoint_path = ROOT / 'next_energy_checkpoint.json'
checkpoint = json.loads(checkpoint_path.read_bytes())
energy_source = ROOT / 'kernel/TGLV350/DualEnergyOnResolvent.lean'
energy_logs = [json.loads(p.read_bytes()) for p in
               sorted((ROOT / 'logs').glob('DualEnergyOnResolvent_*.json'), reverse=True)]
energy_log = next(r for r in energy_logs if r['sha256'] == digest(energy_source)
                  and r['returncode'] == 0 and r['source_unchanged_during_compile'])
assert digest(ROOT / 'build/TGLV350/DualEnergyOnResolvent.olean') == energy_log['output_sha256']
checkpoint.update({'source': str(energy_source), 'compile': energy_log,
                   'integrated': True, 'independent_review': True,
                   'stage': 'INTEGRATED_AND_REVIEWED__FULL_FORM_DOMAIN_STILL_OPEN',
                   'recorded_at': DATE, 'review_sha256': digest(review),
                   'working_um_sha256': digest(ROOT / 'um.py'),
                   'remaining': 'Prove D(q)=D(S) and energy equality on all D(S), then base-valued weight and trace.'})
write_atomic(checkpoint_path, json.dumps(checkpoint, ensure_ascii=False, indent=2).encode())
report_path = ROOT / 'RELATORIO_ENERGIA_E_RAIZ_DUAL.md'
rows = '\n'.join(f"| {name} | `{digest(ROOT / 'kernel/TGLExt' / ('V350' + name + '.lean'))}` |"
                 for name in MODULES)
report = f'''# Energia e raiz positiva no suporte da forma dual

{DATE}. [REAL — Lean incremental na cópia, com revisão independente delimitada.]

Foi construída uma raiz positiva auto-adjunta S do operador T que vinha sendo
obtido do resolvente da forma dual: S²=T, incluindo o domínio da composição.
A energia da forma original coincide com ‖Sx‖² em D(T). A extensão dessa
igualdade a todo D(S) e a identidade D(q_A)=D(S) continuam [OPEN].

## Construção na mesma representação

1. A minimalidade variacional em r=Rv, aplicada a (1+t)r, dá
   q_A(Rv).toReal=Re⟨Rv,v−Rv⟩. O competidor e o minimizador têm energia
   finita, demonstrada antes da passagem de ENNReal para os reais.
2. Para todo x∈D(T), R(x+Tx)=x. Portanto q_A(x)<∞ e
   q_A(x)=ofReal(Re⟨x,Tx⟩). A igualdade final é em ENNReal: não se usa
   a convenção toReal(∞)=0 para encobrir uma energia infinita.
3. Em K=closure(D(q_A)), tomar B=√R_K e C=√(I−R_K), com raízes do
   cálculo funcional contínuo limitado da Mathlib. São positivos,
   comutam, B²=R_K, C²=I−R_K e B²+C²=I. B é injetivo pela injetividade
   já demonstrada de R_K. Definir D(S)=Ran B e S(Bu)=Cu.
4. As provas de grafos limitados já presentes na v350 dão fechamento,
   domínio denso em K, positividade e igualdade com o adjunto efetivo.
   A composição usa D(S²)={{x∈D(S):Sx∈D(S)}}; não se presume que S
   preserve todo o seu domínio. A equação de grafos demonstra S²=T.
5. A adjunção formal e essa igualdade de grafos dão, para x∈D(T),
   Re⟨x,Tx⟩=‖Sx‖². Cada aplicação de S tem seu testemunho de domínio.
   O existencial `exists_dualSupportSquareRoot` recebe apenas P e A≥0
   do core correspondente e constrói R,T,S com esses vínculos.

O arquivo `PartialOperatorSquare` reutiliza o domínio genérico
`partialSquareDomain` de `TGLExt.ContinuousModularSquare`; sua generalização
define a composição real em qualquer Hilbert do escopo, sem transportar
uma hipótese particular do modelo exponencial. Não se troca a torre nem
se insere outro espaço físico na construção. O suporte pode ser zero;
nenhuma densidade no ambiente inteiro é presumida.

## Fronteira que permanece

[OPEN] Provar as duas inclusões entre D(q_A) e D(S), e q_A(x)=‖Sx‖²
em todo esse domínio. Coincidência em D(T), ainda que denso em K, não
basta sem controle na norma da forma. A unicidade abstrata de uma raiz
auto-adjunta positiva arbitrária não foi provada neste pacote; S é a
raiz explicitamente construída a partir das duas raízes limitadas.
Também não se apresenta nova medida espectral ou cálculo funcional
completo para operadores não limitados.

[OPEN] Depois: cone ampliado da base/pontos fixos; peso operadorial e
semifinitude do seu domínio na álgebra; estado modular da base; gerador
afiliado, perturbação e traço canônico fiel normal semifinito, com escala
dual. Permanecem Three Locks/H1, H2/H3 físicos no mesmo modelo, setor
quântico interagente/BRST/QME/anomalias/UV, contrato dependente ampliado
consumido pelo gate e execução integral do monólito.
A identificação Fourier da convenção (2π)⁻¹ mantém a pendência anterior.

Nenhuma dessas obrigações posteriores foi substituída por S²=T. As seis
flags abertas continuam falsas. O corpo Python permaneceu idêntico por
AST ao estrato anterior; o gate legado não mudou. As duas raízes CFC
são construções operatórias, sem interpretação física acrescentada.

## Evidência e custódia

{len(targets)} alvos novos no Audit; {len(build['records'])} registros Lean
integrados válidos; {tests['passed']} controles Python aprovados;
{tests['axiom_report_entries']} declarações distintas no Audit, com axiomas
contidos em propext, Classical.choice e Quot.sound. {integration['embedded_files']}
arquivos embutidos. Build incremental com dependências reutilizadas e
conferidas; runtime integral não executado.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

Base `{integration['base_sha256']}`.
Cópia `{integration['working_sha256']}`.

[Parecer independente](<{review.as_posix()}>). O próprio parecer separa
o que recompilou do que conferiu nos registros de integração do autor.
Logs de tentativas malsucedidas permanecem preservados fora da evidência
aceita. O checkpoint de energia anterior foi atualizado, com backup,
para refletir sua integração e revisão nesta etapa.

Objetivo integral ativo. Original preservado; sem transposição canônica,
novo selo ou confirmação física.
'''
write_atomic(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualEnergyOnResolvent`, `PartialOperatorSquare`,
`ResolventSquareRoot` e `DualSquareRoot`: q_A(x)<∞ e q_A(x)=ofReal(Re⟨x,Tx⟩)
para x∈D(T); S positivo auto-adjunto construído no mesmo suporte K pelo
grafo de √R_K e √(I−R_K); composição efetiva S²=T, incluindo domínio;
q_A(x)=ofReal(‖Sx‖²) em D(T). O existencial constrói R,T,S a partir de A≥0
do core regular. D(S)=Ran √R_K; não se presume D(q_A)=D(S).

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Igualdade D(q_A)=D(S) e extensão da energia a todo D(S), unicidade
abstrata da raiz; cone ampliado da base/pontos fixos; peso semifinito,
estado modular, gerador afiliado, perturbação/traço; Three Locks, H1/H2/H3,
interações/BRST/QME/anomalias/UV, contrato ampliado e runtime integral.
As seis flags abertas continuam falsas. Objetivo integral ativo.

Adendo aos registros anteriores: a raiz S e a igualdade S²=T agora estão
construídas. A representação completa da forma ainda não. O checkpoint
`DualEnergyOnResolvent`, antes somente local, agora está integrado e revisado.
Histórico e backups preservados; sem confirmação física.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
    'DESENHO_DO_FECHAMENTO_QG.md', 'RESPOSTA_GATE_V350.md', 'TRACO_PROXIMAS_OBRIGACOES.md',
    'ROTA_APOS_CORTES_DUAIS.md', 'ROTA_VARIACIONAL_DO_RESOLVENTE.md',
    'RELATORIO_SUPORTE_E_OPERADOR_DUAL.md')]
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
    'energy_checkpoint_sha256': digest(checkpoint_path),
    'integrated_records': len(build['records']), 'controls': tests['passed'],
    'audit_declarations': tests['axiom_report_entries'], 'full_runtime': False,
    'full_goal_complete': False,
}
write_atomic(ROOT / 'square_root_custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
print(json.dumps(custody, ensure_ascii=False))
