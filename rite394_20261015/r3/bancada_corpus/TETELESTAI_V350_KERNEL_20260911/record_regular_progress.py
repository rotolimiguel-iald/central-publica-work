"""Append measured regular-representation progress with exact-byte custody."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
MARKER = 'TETELESTAI_V350_REGULAR_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
integration = json.loads((ROOT / 'integration.json').read_bytes())
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
working_hash = hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest()
base_hash = hashlib.sha256((ROOT / 'fontes/um_v350_original.py').read_bytes()).hexdigest()
assert working_hash == integration['working_sha256'] == tests['working_um_sha256']
assert base_hash == integration['base_sha256']
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
for item in build['records']:
    source = Path(item['source'])
    binary = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert item['returncode'] == 0
    assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sha256']
    assert hashlib.sha256(binary.read_bytes()).hexdigest() == item['output_sha256']


def write(path, text, append=False):
    assert path.is_relative_to(ROOT) or path in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else b''
    if append and MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    suffix = text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    after = before + suffix if append else suffix
    if after == before:
        return
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + STAMP)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    temp.write_bytes(after)
    assert temp.stat().st_size == len(after) and temp.read_bytes() == after
    if append:
        assert after.startswith(before) and len(after) > len(before)
    temp.replace(path)
    assert path.read_bytes() == after


report = f'''# Representação regular da torre — evidência integrada

{DATE}. [REAL — Lean incremental na cópia experimental].

Construídos em `L²(ℝ,H)`, com Lebesgue e H = TowerHilbert P:

1. A representação fiel por fibras π(A)f(x)=Af(x), como homomorfismo com involução.
2. As translações S_t f(x)=f(x−t): grupo unitário fortemente contínuo.
3. O levantamento de famílias fortemente contínuas de isometrias, usando densidade
   de funções simples apoiadas em conjuntos de medida finita.
4. Λ_t=π(Δ^{{it}})S_t: grupo unitário fortemente contínuo e covariância
   Λ_t π(A) Λ_t*=π(σ_t A). A ação σ_t é o `factorFlow` da mesma torre.
5. O bicomutante estelar das duas famílias, `regularCoreAlgebra`, e a inclusão fiel
   `regularCoreEmbedding`; provada sua minimalidade entre álgebras de von Neumann
   concretas que contêm esses geradores.

As provas estão em `kernel/TGLExt/V350L2OperatorLift.lean`, `V350L2Translation.lean`,
`V350L2StrongContinuity.lean`, `V350RegularTowerRepresentation.lean` e
`V350RegularGeneratedAlgebra.lean`. Todos os arquivos estão embutidos na cópia única `um.py`.
As provas da inclusão recíproca e do certificado modular anterior permanecem integradas.

**Alcance:** é uma realização regular concreta gerada pela mesma álgebra/fluxo.
A caracterização completa como core contínuo com traço fiel, normal e semifinito
ainda não foi entregue. Normalidade da inclusão, ação dual e traço precisam de suas
próprias provas; a definição por bicomutante não as substitui. Não há campo de traço
preenchido com uma função trivial para satisfazer o contrato antigo.

**Gate:** a nova representação regular não muda flags de core/Three Locks nem H1–H3.
A subdecisão modular continua reconhecendo apenas a dualidade e seu certificado.
O gate legado continua `{tests['legacy_gate']}`. O plano integral permanece incompleto.

## Verificação medida

- {len(build['records'])} compilações integradas, todas exit 0; hashes dos fontes e .olean conferidos.
- {tests['axiom_report_entries']} declarações distintas no Audit, todas no trio permitido.
- {tests['passed']} controles Python aprovados: fontes/dependências, tipo dos contratos,
  rejeição de evidência ausente e reprodução do gate legado com as entradas seladas.
- Compilação incremental sobre dependências preservadas; rodada integral do monólito pendente.
- Revisão adversarial em outra execução em andamento no momento deste registro.

Base preservada: `{base_hash}`.
Cópia integrada: `{working_hash}`.
Evidência: `integration.json`, `integrated_compile.json`, `gate_tests.json`,
`kernel_incremental_evidence.json` e logs referidos nesses arquivos.

## Próximos elos

Ação dual na álgebra inteira → normalidade/traço canônico → Three Locks no mesmo core →
H1/H2/H3 e estado interagente/BRST/QME/UV compatíveis → contrato ampliado → rodada integral.
Nenhuma dessas condições é quitada por uma identidade de nomes.

Correção ao lado do relatório anterior: o módulo de amplificação foi agora integrado,
e translações, continuidade forte, covariância e álgebra gerada foram construídas.
Este registro não reescreve os resultados históricos nem altera a v350 canônica.
'''
write(ROOT / 'RELATORIO_REPRESENTACAO_REGULAR.md', report)
note = f'''

## {MARKER} — {DATE}

[REAL — Lean incremental] Na cópia `{ROOT}`, construídas a representação fiel por
fibras, translações unitárias fortemente contínuas, Λ_t=π(Δ^{{it}})S_t e a covariância
com `factorFlow` da mesma torre. `regularCoreAlgebra` é o bicomutante estelar das duas
famílias; `regularCoreEmbedding` é injetiva e `regularCore_minimal` prova minimalidade.
São {len(build['records'])} compilações integradas exit 0 e {tests['passed']} controles Python; fontes,
.olean e dependências conferidos por hash. Audit: {tests['axiom_report_entries']} declarações distintas,
somente propext/Classical.choice/Quot.sound. Cópia um.py: {working_hash}; base preservada: {base_hash}.

Correção lateral do registro AUDIT_L2: a amplificação foi integrada, e agora há
representação regular e álgebra gerada. Isso não quita o core com traço nem Three Locks.
[OPEN] Ação dual integral, normalidade da inclusão, traço canônico fiel/normal/semifinito,
Three Locks e H1/H2/H3 físicos compatíveis, interações/BRST/QME/UV, contrato ampliado,
rodada integral e revisão independente. Gate legado preservado; somente fronteira modular quitada.
Relatório/remissões: [RELATORIO_REPRESENTACAO_REGULAR.md](<{(ROOT / 'RELATORIO_REPRESENTACAO_REGULAR.md').as_posix()}>).
Índice: `V350L2OperatorLift`, `V350L2Translation`, `V350L2StrongContinuity`,
`V350RegularTowerRepresentation`, `V350RegularGeneratedAlgebra`, sob kernel/TGLExt na cópia.
'''
for name in ['MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
             'DESENHO_DO_FECHAMENTO_QG.md']:
    write(ROOT / name, note, append=True)
for name in ['TGL_ATLAS.md', 'TGL_INDICE_VIVO.md']:
    write(CENTRAL / 'memory' / name, note, append=True)
print(json.dumps({'marker': MARKER, 'working_sha256': working_hash,
                  'compiled_modules': len(build['records']), 'full_plan_complete': False}))
