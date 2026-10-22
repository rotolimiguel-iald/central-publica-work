"""Record the verified normality increment and the remaining gate obligations."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
MARKER = 'TETELESTAI_V350_ORDER_NORMALITY_20260911'
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
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw) > 0
    temp.replace(path)
    assert path.read_bytes() == raw


def append(path, text):
    before = path.read_bytes() if path.exists() else b''
    if MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    after = before + text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    assert after.startswith(before) and len(after) > len(before)
    write_atomic(path, after)


build = json.loads((ROOT / 'integrated_compile.json').read_bytes())
tests = json.loads((ROOT / 'gate_tests.json').read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
working_hash = digest(ROOT / 'um.py')
assert working_hash == tests['working_um_sha256'] == integration['working_sha256']
assert build['incremental_build_ok'] and tests['passed'] == len(tests['checks'])
for row in build['records']:
    source = Path(row['source'])
    output = ROOT / 'build' / source.relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert row['returncode'] == 0 and digest(source) == row['sha256']
    assert digest(output) == row['output_sha256']

evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
targets = [
    'TGLV350.Regular.fibre_preserves_positive_isLUB',
    'TGLV350.Regular.regularCoreEmbedding_preserves_positive_isLUB',
    'TGLV350.Regular.regularCoreEmbedding_preserves_positive_directed_isLUB',
    'TGLV350.ContractAudit.legacy_contract_accepts_zero_trace',
    'TGLV350.ContractAudit.zeroTraceLegacyCore_has_no_threeLocks',
]
for name in targets:
    assert name in evidence['axiom_report']
    assert set(evidence['axiom_report'][name]) <= {'propext', 'Classical.choice', 'Quot.sound'}
review = ROOT / 'revisao/REVIEW_NORMALITY.md'
review_complete = review.is_file() and working_hash in review.read_text(encoding='utf-8')
if review_complete:
    review_description = 'Revisão independente registrada no parecer vinculado.'
else:
    review = ROOT / 'revisao/normality_independent_20260911_220022_483681/NormalityFullAudit.json'
    independent = json.loads(review.read_bytes())
    assert independent['returncode'] == 0 and independent['axioms_allowed']
    review_description = ('Recompilação e auditoria independentes disponíveis. '
                          'Parecer textual de alcance ainda em finalização; '
                          'não contado como aprovação concluída nesta nota.')

report = f'''# Kernel da v350: o que falta para ampliar o gate

{DATE}. [REAL — fontes e verificação incremental na cópia; recompilação independente.]

**O gate principal da v350 já está no último degrau que seu código prevê.
As oito flags `qgf_`/`gpf_` de fronteira não são entradas dessa função.**
Cumprir uma dessas obrigações altera o respectivo registro de prova; para isso alterar
o veredito principal, o programa também precisa consumir um contrato que contenha as
novas provas e a compatibilidade entre seus objetos.

Fonte original preservada: SHA-256 `{integration['base_sha256']}`.
[Função do gate](<{(ROOT / 'fontes/um_v350_original.py').as_posix()}:168907>).
[Auditoria das oito flags e controles da função](<{(ROOT / 'AUDITORIA_DAS_PENDENCIAS_V350.md').as_posix()}>).

| Obrigação | v350 canônica | Cópia de trabalho nesta etapa |
|---|---|---|
| Dualidade `J M J = M′` na torre | Fronteira modular e habitante do Ato III ainda não quitados. | Certificado construído e subdecisão modular verificada. |
| Core da mesma torre e fluxo | Falta a realização contínua completa. | Representação regular fiel, ação dual na álgebra inteira, fechamento WOT e agora **normalidade da inclusão no sentido da ordem** provados. Falta o traço canônico fiel, normal e semifinito com escala dual. |
| Three Locks / H1 | Falta o canto e o gap relativo na realização contínua efetiva. | Falta construir o suporte no mesmo core, com `0 < τ(P_F) < ∞`, e as identificações necessárias. Os construtores condicionais existentes serão reutilizados. |
| H2 | Falta descarregar a hipótese geométrica na realização pretendida. | Fluxo modular e frame construídos separadamente não bastam: é necessária sua identificação na mesma geometria. |
| H3 | A ponte de importação está registrada, mas os dados do horizonte não foram produzidos. | Conferir as hipóteses e aplicar o resultado ao horizonte correto. A importação pode quitar a etapa no modo IMPORTADO; não é necessário refazer a literatura como prova própria. |
| Testemunha composta | `qgf_full_TGL_witness_constructed` continua falsa. | Reunir dados compatíveis em um contrato dependente suficientemente forte e ligá-lo à decisão que os consome. |

Para o alcance quântico interagente, há outra distinção de tipo: o teorema que alimenta
`relevant_anomalies_absent` demonstra o Ward **clássico-linear**. A construção de estado
quântico interagente, controle de anomalias e domínio de validade UV não é consequência
desse enunciado. [Tipo atual](<{(ROOT / 'kernel/TGLExt/PhysicsCertificates.lean').as_posix()}:292>).

## Avanço formal desta etapa

Em `L2Order`, a amplificação preserva todo supremo positivo crescente dirigido. A prova
reutiliza `TGLExt.MonotoneOperatorLimit`, que já pertence à v350: ela constrói o limite
forte e o identifica ao supremo, em vez de receber convergência como hipótese adicional.

Em `RegularNormality`, o limite permanece na álgebra pelo fechamento WOT. Isso permite
identificar o supremo **interno** ao ambiente e provar a preservação dos supremos internos
por `regularCoreEmbedding P`, tanto para redes gerais quanto para conjuntos dirigidos
não vazios. Não se restringe a sequências ou matrizes finitas. Normalidade aqui tem
esse conteúdo explícito de ordem; a equivalência com continuidade ultra-fraca e predual
não é reivindicada.

[Fonte da normalidade](<{(ROOT / 'kernel/TGLExt/V350RegularNormality.lean').as_posix()}>).

## O contrato antigo precisa ser fortalecido

Foi compilado um contraexemplo: `ContinuousCoreData` aceita inclusão identidade,
ação dual trivial e traço identicamente zero. Logo, o nome e a assinatura antiga do core
não garantem as propriedades anunciadas de um traço canônico. **Esse mesmo exemplo não
pode ter `ThreeLocksCoreData`**, pois os Three Locks exigem traço estritamente positivo.
Não se afirma que o contraexemplo atravesse o certificado completo ou quite uma flag.

[Contraexemplo e limite do contraexemplo](<{(ROOT / 'kernel/TGLExt/V350CoreContractCounterexample.lean').as_posix()}>).
[Inventário dos traços existentes e suas obrigações](<{(ROOT / 'TRACO_PROXIMAS_OBRIGACOES.md').as_posix()}>).

## Evidência e limite da rodada

{len(build['records'])} registros Lean integrados válidos, {tests['passed']} controles Python
aprovados e {tests['axiom_report_entries']} declarações distintas no Audit, com axiomas
contidos em `propext`, `Classical.choice`, `Quot.sound`.
Cópia SHA-256 `{working_hash}`; {integration['embedded_files']} arquivos embutidos.
Fontes, binários e dependências foram conferidos por hash.
{review_description}
[Evidência independente](<{review.as_posix()}>).

A compilação é incremental; a execução integral do monólito atualizado ainda está pendente.
O protótipo `TGLV350/OperatorOrderLimits.lean`, que falhou e repetia resultados existentes,
ficou fora da integração e da evidência aceita. Os logs das tentativas não foram apagados.

O gate legado conserva sua função; a subdecisão experimental continua com alcance modular.
Normalidade e o contraexemplo não acendem flags de core, canto, H1/H2/H3 ou testemunha total.
O original canônico permanece preservado; não houve transposição, publicação ou novo selo.
O objetivo global segue ativo: traço/canto, hipóteses geométricas e físicas compatíveis,
contrato ampliado, rodada integral e revisão do restante do plano continuam abertos.
'''
write_atomic(ROOT / 'RESPOSTA_GATE_V350.md', report.encode('utf-8'))

note = f'''

## {MARKER} — {DATE}

[INPUT] Consulta do operador: “o que falta resolver no um.py do ponto de vista de kernel
que pode mover o gate? observe a última versão do um.py (v350)”.

[REAL — Lean incremental e recompilação independente] Na bancada {ROOT}, a normalidade de
`regularCoreEmbedding P` foi provada como preservação de supremos positivos dirigidos
INTERNOS nas álgebras de von Neumann. O limite forte é construído pela peça já existente
`TGLExt.MonotoneOperatorLimit`; não é hipótese escondida. Vale para índices dirigidos
gerais, além de sequências. A equivalência com continuidade ultra-fraca/predual não foi provada.
Módulos novos: `V350L2Order`, `V350RegularNormality` e `V350CoreContractCounterexample`.

[REAL — contraexemplo formal] O contrato legado `ContinuousCoreData` admite traço zero
e ação dual trivial; o mesmo exemplo NÃO admite `ThreeLocksCoreData`, pelo traço positivo.
Assim, a assinatura do core sozinha não garante um traço fiel, normal e semifinito.
Nenhum desses resultados foi usado para acender indevidamente flag do core/canto.

Integração: {len(build['records'])} registros Lean válidos, {tests['passed']} controles Python,
{tests['axiom_report_entries']} alvos distintos no Audit, todos com axiomas no trio.
SHA-256 experimental {working_hash}; base preservada {integration['base_sha256']}.
{review_description}
Evidência: [{review.name}](<{review.as_posix()}>).
Relatório: [RESPOSTA_GATE_V350.md](<{(ROOT / 'RESPOSTA_GATE_V350.md').as_posix()}>).

[OPEN] Traço canônico e escala dual na mesma álgebra, Three Locks/H1, identificação
geométrica H2, aplicação de H3 ao horizonte, estado quântico interagente/anomalias/UV,
contrato dependente ampliado e execução integral. O gate canônico não lê qgf/gpf; a
subdecisão experimental continua quitando somente a fronteira modular. O plano integral
permanece ativo. Protótipo OperatorOrderLimits excluído: tentativas falhas preservadas.
'''
surfaces = [ROOT / name for name in (
    'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md',
    'MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md')]
surfaces += [CENTRAL / 'memory' / name for name in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md')]
for path in surfaces:
    append(path, note)
    assert MARKER.encode() in path.read_bytes()
print(json.dumps({'marker': MARKER, 'working_sha256': working_hash,
                  'memory_surfaces': len(surfaces), 'full_plan_complete': False}))
