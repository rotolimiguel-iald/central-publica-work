"""Write the independent DEV review; do not mutate any author artifact."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'bounded_scalar_cuts_latest_run.txt').read_text(encoding='utf-8'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M = read(RUN / 'manifest.json')
C = read(RUN / 'compilation.json')
V = read(RUN / 'verification_dev.json')
D = read(RUN / 'author_bounded_scalar_cuts_draft_status.json')
K = read(RUN / 'gns_normality_custody.json')
assert all(C[k] for k in ['complete', 'all_exit_zero', 'full_audit_names_exact',
                          'all_axioms_allowed', 'sources_unchanged',
                          'dependencies_unchanged', 'previous_reviews_preserved'])
assert all(V[k] for k in ['four_compiles_rc0', 'exact_target_set', 'axioms_match_status',
                          'all_axioms_allowed', 'dependencies_frozen_preserved',
                          'author_project_builds_excluded', 'status_unchanged',
                          'route_equals_status_and_frozen', 'custody_equals_status',
                          'previous_gns_normality_review_equals_custody', 'previous_reviews_preserved'])
for row in V['records'].values():
    assert all(row[k] for k in ['source_equals_status_and_frozen', 'author_log_identical_to_frozen',
                               'author_log_rc0_source_unchanged', 'author_binary_equals_status_and_log',
                               'own_binary_equals_compilation_record', 'own_binary_equals_author',
                               'target_names_exact', 'author_streams_frozen_equal'])
for row in M['sources'].values():
    assert sha(Path(row['path'])) == sha(Path(row['snapshot'])) == row['sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
assert sha(ROOT / 'bounded_scalar_cuts_draft_status.json') == V['status_sha256']
assert sha(ROOT / 'ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md') == V['route_sha256']
assert sha(ROOT / 'gns_normality_custody.json') == V['custody_sha256']
assert sha(ROOT / 'um.py') == M['initial_um_sha256'] == D['working_sha256'] == K['working_sha256']
assert len(M['declarations']) == len(M['all_named_declarations']) == 11
warnings = {row['module']: [l for l in Path(row['stdout']).read_text(encoding='utf-8').splitlines()
                            if 'warning:' in l] for row in C['records']}
assert all(not x for x in warnings.values())
assert all(Path(row['stderr']).stat().st_size == 0 for row in C['records'])

def write_new(path, raw):
    assert path.resolve().is_relative_to(REVIEW) and not path.exists()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw and tmp.stat().st_size == len(raw) > 0
    tmp.replace(path)
    assert path.read_bytes() == raw

def link(path, label=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + '>)'

verification_raw = (ROOT / 'gns_normality_custody_verification.json').read_bytes()
write_new(RUN / 'author_gns_normality_custody_verification.json', verification_raw)
previous_verification = json.loads(verification_raw)
assert previous_verification['custody_ok'] is True
assert len(previous_verification['exact_prefix_backups']) == 25
now = datetime.datetime.now().astimezone()
source_table = '\n'.join('| ' + name + ' | ' + str(len(M['sources']['TGLV350/' + name + '.lean']['declarations'])) +
    ' | `' + row['source_sha256'] + '` | `' + row['own_binary_sha256'] + '` |'
    for name, row in V['records'].items())
logs_table = '\n'.join('| ' + link(Path(row['author_log'])) + ' | `' + row['author_log_sha256'] + '` |'
    for row in V['records'].values())
times_table = '\n'.join('| ' + row['module'] + ' | 0 | ' + str(row['seconds']) + ' |'
    for row in C['records'])
ex = V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
report = f'''# Revisão independente — funcionais escalares limitados de corte

{now.isoformat(timespec='seconds')}. **DEV concluído; nenhum achado P0, P1 ou P2.**

[REAL — inspeção de fontes e recompilação própria] Foram lidas integralmente as três fontes finais e `ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md`, examinados os 11 enunciados/tipos e sua composição, e recompilados os três módulos e um auditor próprio. Os quatro processos retornaram rc0. Os 11 `#check` com universos explícitos e 11 `#print axioms` cobrem exatamente todas as declarações nomeadas novas, incluindo as duas definições CLM; somente `propext`, `Classical.choice` e `Quot.sound`. Os três `.olean` próprios são byte a byte iguais aos autorais pinados.

**Alcance:** funcionais complexos limitados positivos para R≥0, dominados por ν sobre N+, exaustão natural em ENNReal e critério de convergência monótona das leituras reais ao supremo interno. Esta revisão não certifica integração destes três módulos, interface predual, fidelidade dos cortes, normalização como estados, mapas GNS dos cortes ou fechabilidade.

## Achados e provas conferidas

Não foi encontrada premissa residual, erro de coerção/sinal ou exagero documental no escopo. Os pontos abaixo delimitam precisamente o resultado; não são defeitos pendentes.

| Fonte/linhas | Alvos | Exame substantivo |
|---|---|---|
| `DualCutLinearMap.lean:12–39` | `dualWeightCut_add`, `dualWeightCut_smul`, `dualWeightCutCLM` | Linearidade complexa para todo R real. A aditividade usa integrabilidade dos vetores de ambas as órbitas, deduzida da continuidade forte. `mkContinuous` recebe a cota efetiva ‖C_R(A)‖≤|2R|‖A‖. O mapa A↦C_R(A) é limitado em norma de operador, sem supor que s↦θ_s(A) seja contínuo/integrável em norma de operador. |
| `ScalarBoundedCuts.lean:16–23` | `dualCutFunctional`, `dualCutFunctional_apply` | O funcional é CLM complexo em A sobre todo B(RegularHilbert H). Compõe C_R, avaliação em v e `innerSL ℂ v`, linear no segundo argumento: ψ_(R,v)(A)=c⟨v,C_R(A)v⟩. O primeiro argumento fica fixo; não há troca que introduza conjugação da escala. |
| `ScalarBoundedCuts.lean:25–39` | `dualCutFunctional_nonneg`, `dualCutFunctional_ofReal_re` | A positividade usa R≥0, A≥0 e a positividade de `normalizedDualCut`; `inner_nonneg_right` entrega desigualdade complexa. A identidade ENNReal é válida mesmo para A não positivo, pois depende apenas de c≥0; isso não amplia as leis positivas. |
| `ScalarBoundedCuts.lean:43–53` | `scalarDualWeight_dominates_cut`, `scalarDualWeight_eq_iSup_boundedCuts` | `PositiveCoreInput P` contém simultaneamente A∈N e A≥0. A avaliação usa a mesma η=`regularVacuum P` e a mesma família q de ν. A dominância exige R≥0; a exaustão usa raios n∈ℕ e não assume ν(A) finito. |
| `ScalarCutNormality.lean:13–22` | `dualCutFunctional_re_tendsto` | Para índice em `Type u`, apenas `Preorder`, transfere leituras reais de uma rede monótona já fortemente convergente, ao longo de `atTop`, para todo R∈ℝ e todo v. Este lema auxiliar recebe expressamente `hlim`; não foi apresentado como construção do limite. |
| `ScalarCutNormality.lean:27–41` | `scalarCut_tendsto_internal_isLUB` | A rede vive na mesma N, é positiva/crescente, com índice dirigido e não vazio e supremo B interno dado. A prova constrói o limite forte e só então aplica o auxiliar. Não recebe SOT, normalidade de ν/π ou fechabilidade como premissa. A conclusão é `Tendsto` real, não uma nova estrutura predual nem um teorema formal geral de equivalência de normalidades. |

**Positividade, escala e infinito.** O escopo `ComplexOrder` está aberto em `ScalarBoundedCuts.lean:10`. A definição Mathlib `Analysis/Complex/Order.lean:63–64` foi conferida: `0≤z ↔ 0≤z.re ∧ 0=z.im`. Portanto a prova inclui realidade e não negatividade, não apenas uma projeção real. O lema usado `ContinuousLinearMap.IsPositive.inner_nonneg_right` está em `Analysis/InnerProductSpace/Positive.lean:320–321`.

A definição herdada e relida em `DualWeightForm.lean:17–34` fixa **c=(2·Real.pi)⁻¹>0** e o corte normalizado c·C_R. O fator aparece uma única vez em ψ e uma única vez na avaliação ν; não há divisão pelo comprimento do intervalo. Para R<0 a integral é orientada e a linearidade/cota usam |2R|, enquanto a positividade e a dominância conservam R≥0. R=0 é admissível; não há positividade estrita ou fidelidade de cada corte como premissa/conclusão.

`dualCutFunctional_ofReal_re` usa `ENNReal.ofReal_mul` com c≥0. Nenhuma das três fontes converte infinito por `toReal`. A identidade ν(A)=sup_n ofReal(Re ψ_(n,η)(A)) conserva a possibilidade de ⊤. A dependência `DualWeightExhaustion.lean:14–66`, relida do snapshot próprio, usa indicadores dos intervalos Ioc(-n,n), crescimento e cobertura de ℝ, com convergência monótona ENNReal; os endpoints e a orientação são compatíveis com a integral intervalar positiva. Não se afirma supremum limitado de operadores em B(H).

**Limite construído e não circularidade.** Em `ScalarCutNormality.lean:35–40`, hpos e hB dão ‖A_i‖≤‖B‖. `vonNeumann_exists_positive_isLUB` (`RegularNormality.lean:52–67`, relido) constrói um D ambiente pelo limite de operadores positivos limitados, mantém D em N por fechamento WOT e só então restringe o supremo ambiente a um supremo interno. `hD.unique hB` identifica D=B dentro da mesma N. Assim o supremo interno não é usado circularmente como se já fosse um limite forte; o resultado ambiente é obtido pela construção herdada. Positividade de B não é uma hipótese escondida adicional: decorre dessa identificação, ou de ser majorante de uma família positiva não vazia.

O passo das leituras usa `DualCutNormality.lean:61–87`: Dini sobre compacto com índice preordenado arbitrário, seguido da estimativa da integral uniforme sobre uIcc(-R,R). Nenhuma enumerabilidade/separabilidade adicional de H é introduzida. Os novos lemas usam `atTop`, não declaram continuidade monótona para todo filtro arbitrário. O teorema final tem `IsDirectedOrder` e `Nonempty`, afastando a vacuidade de `atTop=⊥`; o auxiliar mais geral permanece uma implicação legítima inclusive em filtros degenerados. A afirmação para qualquer R é de convergência das leituras reais; para falar de funcionais positivos usa-se R≥0.

## Evidência independente e proveniência

Árvore isolada: {link(RUN)}. Reutilizaram-se **{V['project_dependency_count']} dependências de projeto** da árvore própria anterior {link(Path(M['previous_run']))}, selecionadas pelo fechamento transitivo dos imports. Fontes e `.olean` foram copiados e pinados no manifesto; hashes foram conferidos antes/depois. Nenhuma dependência de projeto foi obtida do build autoral. `LEAN_PATH` contém somente o build próprio e os oito caminhos de pacotes externos readonly registrados no manifesto. Não se recompilaram biblioteca, dependências ou raízes. TMP/TEMP apontam para a árvore própria.

Compilador: `{M['lean_version']}`; SHA256 `{M['compiler_sha256']}`. Pacotes externos foram herdados em leitura; esta etapa não é uma reconstrução nem auditoria independente de toda Mathlib/toolchain.

Exceção histórica já revisada, explicitamente preservada: `TGLV350.DualSemifiniteIdeal` usa fonte própria anterior `{ex['source_sha256']}` e binário `{ex['sha256']}`. A fonte autoral atual `{ex['live_source_sha256']}` difere somente pela errata de comentário já aceita; a substituição literal exata foi reconferida ao congelar. Não se reivindica que toda a cadeia herdada reproduza os bytes dos binários autorais atuais. As limitações de reprodução das dependências registradas nos pareceres anteriores continuam válidas. A identidade binária nova aqui é a dos três módulos da tabela seguinte.

| Módulo DEV | Alvos | SHA256 fonte final lida | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
{source_table}

| Processo próprio | rc | Segundos |
|---|---|---|
{times_table}

Todos os stdout próprios ficaram sem warnings e todos os stderr vazios. O auditor usa somente os três imports novos e `#check`/`#print axioms`; não introduz axiomas ou teoremas substitutos. Fonte do auditor: `{V['own_auditor_source_sha256']}`; binário: `{V['own_auditor_binary_sha256']}`; stdout: `{V['own_auditor_stdout_sha256']}`. O conjunto de 11 nomes e os conjuntos de axiomas coincidem com o status autoral, além de terem sido extraídos dos próprios processos.

| Log autoral final inspecionado, não executado pelo revisor | SHA256 JSON |
|---|---|
{logs_table}

Os logs autorais registram rc0 e fonte inalterada; os hashes das fontes, saídas `.olean`, stdout e stderr foram relidos e comparados às cópias congeladas. Streams e comandos próprios, pins individuais das dependências e comparações detalhadas estão em {link(RUN / 'manifest.json')}, {link(RUN / 'compilation.json')}, {link(RUN / 'verification_dev.json')} e {link(RUN / 'logs/BoundedScalarCutsAudit.stdout.txt')}. Tentativas autorais anteriores não foram alteradas ou tratadas como falhas pendentes das versões finais.

## Documentação, custódia e limites

`ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md` foi lida integralmente, SHA256 **`{V['route_sha256']}`**; o pin coincide com o status e com o snapshot próprio. As frases sobre realidade complexa, raio, ν sobre N+, supremo possivelmente infinito e critério de convergência monótona correspondem aos enunciados. A referência a Masuda permanece motivação bibliográfica, já consultada no estrato anterior; não houve nova pesquisa bibliográfica nesta etapa nem uso da referência como prova de fechabilidade. A rota separa corretamente os mapas GNS futuros e não presume η separante para N, fidelidade dos cortes ou ψ_n(1)=1.

Status autoral congelado: `{V['status_sha256']}`. A custódia anterior `gns_normality_custody.json`, SHA256 `{V['custody_sha256']}`, coincide com o pin do status e sela `REVIEW_GNS_NORMALITY.md` no hash `{V['previous_gns_normality_review_sha256']}`, reconferido. `gns_normality_custody_verification.json`, SHA256 `{hashlib.sha256(verification_raw).hexdigest()}`, foi somente lido: declara `custody_ok=true` e 25 prefixos/backups. Esse ciclo autoral não foi reexecutado nem seus 25 pares revalidados neste parecer.

O SHA256 da cópia permaneceu `{M['initial_um_sha256']}` ao congelar e ao concluir. As contagens **98/70/6337** pertencem exclusivamente à integração anterior custodiada, conforme seus registros; não constituem integração destes três DEV. Nenhum exame integrado novo, execução de testes/recorders/verifiers, importação/execução do monólito ou inspeção de fontes posteriores foi realizado. Os {len(M['previous_reviews'])} pareceres anteriores conservaram seus hashes. Escritas exclusivamente em `revisao/`; originais, fontes autorais, memórias e custódias intocados.

**Parecer final DEV:** os três módulos/11 alvos estão revisados e recompilados independentemente, sem P0–P2. Estão conferidos os funcionais limitados positivos para R≥0, dominância e exaustão de ν, e o critério de normalidade por convergência monótona das leituras reais ao supremo interno, com limite construído. Não se afirma interface predual/ultra-fraca, estados normalizados, fidelidade individual dos cortes, mapas GNS associados, fechabilidade/Tomita fechado, domínio escalar máximo, KMS, traço, Three Locks/H1–H3, gate ou runtime. Nenhuma análise necessária deste escopo DEV ficou pendente; integração e desenvolvimentos seguintes exigem outro estrato autorizado.
'''
path = REVIEW / 'REVIEW_BOUNDED_SCALAR_CUTS.md'
write_new(path, report.encode('utf-8'))
result = {
    'timestamp': now.isoformat(timespec='seconds'), 'status': 'DEV_COMPLETE_NO_P0_P1_P2',
    'review_path': str(path), 'review_sha256': sha(path), 'review_bytes': path.stat().st_size,
    'new_sources': 3, 'new_targets': 11, 'own_compiler_processes_rc0': 4,
    'own_bins_equal_author': True, 'project_dependencies': len(M['dependencies']),
    'previous_reviews_preserved': all(sha(Path(p)) == h for p, h in M['previous_reviews'].items()),
    'integrated_inspection_performed': False, 'author_programs_executed': False,
    'working_sha256_at_close': sha(ROOT / 'um.py'), 'findings': []
}
write_new(RUN / 'closure_dev.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
