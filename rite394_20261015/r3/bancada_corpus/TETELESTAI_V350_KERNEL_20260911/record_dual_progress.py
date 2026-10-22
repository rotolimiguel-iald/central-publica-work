"""Record the verified dual-action increment without promoting its scope."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
MARKER = 'TETELESTAI_V350_DUAL_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
working_hash = hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest()
assert working_hash == integration['working_sha256'] == tests['working_um_sha256']
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0
    assert hashlib.sha256(source.read_bytes()).hexdigest() == row['sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == row['output_sha256']


def write(path, text, append=False):
    assert path.is_relative_to(ROOT) or path in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else b''
    if append and MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    suffix = text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    after = before + suffix if append else suffix
    if before == after:
        return
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + STAMP)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    temporary.write_bytes(after)
    assert temporary.stat().st_size == len(after) and temporary.read_bytes() == after
    if append:
        assert after.startswith(before) and len(after) > len(before)
    temporary.replace(path)
    assert path.read_bytes() == after


report = f'''# Ação dual da representação regular — incremento verificado

{DATE}. [REAL — compilação Lean incremental, na cópia].

**A ação dual está construída sobre a álgebra gerada inteira.** No mesmo espaço
Lebesgue L²(ℝ,TowerHilbert P), o multiplicador D_s f(x)=exp(−isx)f(x) é unitário,
fortemente contínuo e satisfaz D_s S_t D_s*=exp(−ist)S_t.
O automorfismo θ_s=Ad(D_s) restringe-se a `regularCoreAlgebra P` e satisfaz:

- θ_0=id e θ_{{s+t}}=θ_t∘θ_s;
- θ_s(π(A))=π(A) para a inclusão `regularCoreEmbedding` da mesma torre;
- θ_s(Λ_t)=exp(−ist)Λ_t para Λ_t=π(Δ^{{it}})S_t;
- para cada X na álgebra e f no Hilbert, s↦θ_s(X)f é contínua.

A restrição foi provada transportando centralizadores e bicomutantes por um
automorfismo com involução e usando preservação dos geradores nos dois sentidos.
Não foi postulada extensão de um mapa definido apenas nos geradores.

**Também provado:** se T_i→T fortemente e os T_i são uniformemente limitados,
π(T_i)→π(T) fortemente. O enunciado admite filtros arbitrários, além de sequências.
Este é um resultado de continuidade limitada; a normalidade de um homomorfismo
de álgebras de von Neumann ainda requer a ponte com o contrato topológico/de ordem.

## Fontes e verificação

Os quatro módulos novos são `V350L2CharacterMultiplier`, `V350GeneratedEquivariance`,
`V350RegularDualAction` e `V350L2BoundedStrongContinuity`, sob `kernel/TGLExt` e
embutidos em `um.py`. As fontes de desenvolvimento correspondentes estão em `kernel/TGLV350`.

- {len(build['records'])} registros integrados válidos: 11 módulos anteriores reutilizados por
  hash e dependências, quatro módulos novos e duas raízes compilados nesta integração.
- {tests['passed']} controles Python passaram; {tests['axiom_report_entries']} declarações distintas
  auditadas com axiomas contidos em propext, Classical.choice, Quot.sound.
- Cópia integrada SHA-256: `{working_hash}`.
- Evidências: `integrated_compile.json`, `gate_tests.json`, `kernel_incremental_evidence.json`.

A revisão independente anterior (`revisao/REVIEW_MODULAR_AND_REGULAR.md`) recompilou
11 módulos e não encontrou defeito no pacote modular/regular até a álgebra gerada.
Seu parecer refere-se à cópia anterior e aos módulos delimitados. Uma revisão nova,
dos quatro incrementos acima, está em andamento; não é coberta retroativamente pelo parecer anterior.

## O que isto permite e o que continua aberto

A representação regular e sua ação dual estão realizadas no mesmo objeto. **Ainda não
há traço canônico fiel, normal e semifinito construído**, nem prova de τ∘θ_s=e^(−s)τ
para esse traço. O canto P_F dos Three Locks também não foi construído nesse core.
Essas são obrigações matemáticas distintas da relação de Weyl já provada.

As flags qgf de core/canto e gpf de H1/H2/H3 seguem abertas; nenhum novo gate foi habilitado
por esses quatro módulos. O gate legado conserva sua string e a subdecisão modular conserva
seu alcance. Rodada integral do monólito, estado quântico interagente/BRST/QME/UV,
certificado dependente ampliado e revisão do restante do plano continuam pendentes.

Incidentes: primeiras tentativas de GeneratedEquivariance e RegularDualAction falharam
em elaboração/tipagem e foram preservadas. Não se contou um stdout com sorryAx como prova.
O compilador auxiliar agora rejeita expressamente mudança de fonte durante a invocação;
o log final da ação dual declara fonte inalterada e exit 0.
'''
write(ROOT / 'RELATORIO_ACAO_DUAL.md', report)
note = f'''

## {MARKER} — {DATE}

[REAL — Lean na cópia] Construídos os multiplicadores D_s f(x)=exp(−isx)f(x),
unitariedade, continuidade forte e Weyl. `regularDualAction` é um automorfismo da
álgebra gerada inteira: fixa `regularCoreEmbedding`, transforma Λ_t por exp(−ist),
compõe como grupo e é fortemente contínuo. `GeneratedEquivariance` prova a restrição
pelo transporte de bicomutantes. `fibre_tendsto_of_uniformly_bounded` preserva limites
fortes uniformemente limitados para filtros arbitrários, no verdadeiro Lebesgue L².

{len(build['records'])} registros integrados válidos, {tests['passed']} controles Python, {tests['axiom_report_entries']}
declarações distintas no Audit sem axiomas fora do trio. Cópia um.py: {working_hash}.
Correção lateral: ação dual já construída na cópia; a pendência de traço permanece.
[OPEN] Normalidade da inclusão no contrato W*, traço canônico fiel/normal/semifinito
e sua escala dual, Three Locks no mesmo core, H1/H2/H3 físicos, interações/BRST/QME/UV,
gate ampliado e rodada integral. Nenhuma nova flag de core/canto habilitada.

Revisão anterior favorável apenas ao pacote modular/regular/álgebra gerada; nova revisão
dos quatro incrementos em andamento. Remissão:
[RELATORIO_ACAO_DUAL.md](<{(ROOT / 'RELATORIO_ACAO_DUAL.md').as_posix()}>).
Módulos: V350L2CharacterMultiplier, V350GeneratedEquivariance, V350RegularDualAction,
V350L2BoundedStrongContinuity, sob kernel/TGLExt na bancada {ROOT}.
'''
for name in ['MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
             'DESENHO_DO_FECHAMENTO_QG.md']:
    write(ROOT / name, note, append=True)
for name in ['TGL_ATLAS.md', 'TGL_INDICE_VIVO.md']:
    write(CENTRAL / 'memory' / name, note, append=True)
print(json.dumps({'marker': MARKER, 'sha256': working_hash,
                  'full_plan_complete': False, 'gate_changed': False}))
