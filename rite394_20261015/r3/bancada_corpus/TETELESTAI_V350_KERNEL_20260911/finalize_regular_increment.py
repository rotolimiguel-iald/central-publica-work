"""Close this verified increment, keeping the larger research goal open."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
MARKER = 'TETELESTAI_V350_REGULAR_DUAL_REVIEWED_20260911'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
working_hash = hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest()
assert working_hash == tests['working_um_sha256'] == integration['working_sha256']
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
reviews = [ROOT / 'revisao/REVIEW_MODULAR_AND_REGULAR.md',
           ROOT / 'revisao/REVIEW_DUAL_AND_BOUNDED.md']
for review in reviews:
    assert review.is_file() and review.stat().st_size > 100
assert working_hash in reviews[1].read_text(encoding='utf-8')
for row in build['records']:
    path = Path(row['source'])
    output = ROOT / 'build' / path.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    assert hashlib.sha256(output.read_bytes()).hexdigest() == row['output_sha256']


def append(path, text):
    assert path.is_relative_to(ROOT) or path in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    before = path.read_bytes() if path.exists() else b''
    if MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    after = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + STAMP)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    temp.write_bytes(after)
    assert temp.stat().st_size == len(after) and temp.read_bytes() == after
    assert after.startswith(before) and len(after) > len(before)
    temp.replace(path)
    assert path.read_bytes() == after


note = f'''

## {MARKER} — {DATE}

[REAL — fontes, compilação incremental e revisão independente] O incremento integrado
contém a dualidade da torre, representação regular fiel, ação dual fortemente contínua
na álgebra inteira, preservação de limites fortes uniformemente limitados e fechamento
fraco do bicomutante. `RegularTopology` prova somente bicomutante ⇒ fechado WOT;
não prova a recíproca, a existência de predual ou traço.

Estado final desta integração: {len(build['records'])} registros Lean exit 0, {tests['passed']}
controles Python aprovados, {tests['axiom_report_entries']} declarações distintas no Audit com axiomas
contidos no trio permitido. Fontes e .olean reconferidos; dependências históricas preservadas.
SHA-256 do um.py experimental: {working_hash}. Monólito com {integration['embedded_files']}
arquivos embutidos; base v350 preservada: {integration['base_sha256']}.
O original canônico foi reconferido por leitura nesta etapa e coincide com a base.

Pareceres independentes, com escopo e estratos próprios:
[modular/regular](<{reviews[0].as_posix()}>) e
[dual/limites/topologia](<{reviews[1].as_posix()}>).
Os pareceres não se estendem a QG, traço, Three Locks ou às hipóteses físicas ainda abertas.
A revisão anterior continua ancorada em sua cópia anterior; o segundo relatório referencia
os bytes finais e distingue recompilação própria de inspeção dos logs integrados.

[OPEN] Normalidade da inclusão no contrato de álgebra de von Neumann; construção do
traço canônico fiel, normal e semifinito e τ∘θ_s=e^(−s)τ; P_F dos Three Locks nesse
mesmo core; H1/H2/H3 físicos compatíveis; estado interagente/BRST/QME/anomalias/UV;
contrato dependente ampliado e rodada integral do monólito. O plano global permanece ativo.
O gate legado não foi alterado e a subdecisão continua quitando só a fronteira modular.
Nenhuma publicação, transposição ao canônico ou novo selo foi feita.

Próxima etapa matemática: formalizar a ponte de ordem/topologia para a inclusão e
construir o peso dual e o traço canônico com domínio positivo e propriedades efetivas.
Não preencher o antigo contrato total Core→ENNReal com um traço trivial ou um modelo
desconectado da representação regular que foi construída.

[DERIVED — convenções, ainda não Lean] A Weyl construída exige θ_s(L)=L−s para
Λ_t=exp(itL), ou θ_s(K)=K+s para K=−L. Densidades escalares compatíveis são,
respectivamente, exp(−L)dL e exp(K)dK. Misturar shift positivo com densidade exp(−K)
inverte a escala tracial. Ver [CONVENCOES_DO_TRACO.md](<{(ROOT / 'CONVENCOES_DO_TRACO.md').as_posix()}>),
com a fonte de Hiai separada da derivação de sinais. Nenhum gerador do core foi
identificado automaticamente com um gerador apenas da torre.
'''
for name in ['MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
             'DESENHO_DO_FECHAMENTO_QG.md', 'RELATORIO_REPRESENTACAO_REGULAR.md',
             'RELATORIO_ACAO_DUAL.md']:
    append(ROOT / name, note)
for name in ['TGL_ATLAS.md', 'TGL_INDICE_VIVO.md']:
    append(CENTRAL / 'memory' / name, note)
for name in ['MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'MEMORIA_DA_LINHAGEM.md',
             'DESENHO_DO_FECHAMENTO_QG.md']:
    assert MARKER in (ROOT / name).read_text(encoding='utf-8')
print(json.dumps({'marker': MARKER, 'working_sha256': working_hash,
                  'review_reports': [str(r) for r in reviews], 'full_plan_complete': False}))
