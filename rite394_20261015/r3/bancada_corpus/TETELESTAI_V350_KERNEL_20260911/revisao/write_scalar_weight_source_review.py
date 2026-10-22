"""Write the source-review stratum only; never run author code."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'scalar_dual_weight_latest_run.txt').read_text(encoding='utf-8'))
M = json.loads((RUN / 'manifest.json').read_bytes())
C = json.loads((RUN / 'compilation.json').read_bytes())
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
DEST = RUN / ('documentary_' + STAMP)
DEST.mkdir()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def create(path, raw):
    assert path.resolve().is_relative_to(REVIEW) and not path.exists()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw and len(raw) > 0
    tmp.replace(path)
    assert path.read_bytes() == raw

def link(path, label=None, line=None):
    return f'[{label or path.name}](<{path.as_posix()}{":"+str(line) if line else ""}>)'

docs = ['MINUTA_PESO_ESCALAR_DUAL.md', 'record_scalar_weight_progress.py',
        'verify_scalar_weight_custody.py', 'fixed_base_custody.json']
hashes = {}
for name in docs:
    raw = (ROOT / name).read_bytes()
    create(DEST / name, raw)
    hashes[name] = sha(raw)
    if name.endswith('.py'):
        ast.parse(raw)
template = (DEST / docs[0]).read_text(encoding='utf-8')
issue_line = next(n for n, line in enumerate(template.splitlines(), 1) if 'ofReal⟨Ω,DΩ⟩' in line)
assert all(C[k] is True for k in ['complete', 'all_exit_zero', 'full_audit_names_exact',
    'all_axioms_allowed', 'sources_unchanged', 'dependencies_unchanged', 'previous_reviews_preserved'])
assert len(M['declarations']) == 23 and len(M['all_named_declarations']) == 25
own = {r['module']: r for r in C['records']}
rows = []
for rel, source in M['sources'].items():
    raw = Path(source['path']).read_bytes()
    assert sha(raw) == source['sha256'] == own[rel]['source_sha256']
    assert own[rel]['output_sha256'] == source['author_binary_sha256']
    rows.append(f'| {Path(rel).stem} | {len(source["declarations"])} | `{sha(raw)}` | `{own[rel]["output_sha256"]}` |')
deps = M['dependencies']
exception = deps['TGLV350.DualSemifiniteIdeal']
audit = C['records'][-1]
named = '\n'.join(f'- `{name}`' for name in M['declarations'])
proof = lambda name, line: link(ROOT / 'kernel/TGLV350' / (name + '.lean'), name + '.lean', line)
docrows = '\n'.join(f'| {name} | `{digest}` |' for name, digest in hashes.items())
text = f'''# Revisão independente — peso escalar dual

{DATE}. **Estrato de fontes e documentação; integração final ainda pendente do aviso do autor.**

**Conclusão delimitada.** [REAL — inspeção e recompilação próprias] Não encontrei P0/P1 nem defeito matemático P2 nas quatro fontes finais. Os 23 alvos passaram no auditor próprio, com apenas `propext`, `Classical.choice` e `Quot.sound`. Há um **P2 documental** na fórmula da minuta, detalhado abaixo. O pacote constrói a avaliação escalar fiel e normal da mesma família de formas e um ideal complexo esquerdo fortemente denso com quadrados de peso finito. A interpretação clássica da semifinitude escalar é explicitada separadamente daquilo que foi formalizado em Lean.

**Achado P2 — parte real omitida na minuta.** Em {link(ROOT / docs[0], docs[0], issue_line)}, `ofReal⟨Ω,DΩ⟩` aplica literalmente uma função real a um produto interno complexo. O resultado efetivamente provado em {proof('ScalarDualWeight',81)} é `ENNReal.ofReal (inner ℂ Ω (D Ω)).re`. Correção sugerida: `ofReal(Re⟨Ω,DΩ⟩)`. Para o valor positivo D construído, o produto interno é real, portanto isto é uma imprecisão documental de tipagem, sem invalidar o teorema. O último teorema aceita D por uma hipótese de representação e não exige positividade explícita de D; nesse enunciado geral, a parte real é indispensável. A cópia da minuta examinada foi preservada em {link(DEST / docs[0])}. Não alterei a minuta nem os scripts do autor.

**Tipos, composição e hipóteses.** Foram lidas integralmente as quatro fontes (58, 64, 88 e 96 linhas) e as saídas de tipos/axiomas. Para o mesmo `P : SiteProfile`, M é `theFactorObject P`, N é `regularCoreAlgebra P`, F é `dualFixedCore P`, H é `TowerHilbert P` e a representação é `RegularHilbert H`, o L² de Lebesgue em ℝ já construído. O vetor η é `testVector (hOmega P)`, isto é, eΩ no intervalo (0,1]; tem norma 1. Não é um representante pontual arbitrário de uma classe L².

- {proof('FixedBaseEquivalence',12)}: a ida é a amplificação efetiva `fibre`, com codomínio restringido a F. A sobrejetividade usa a identificação anterior F=imagem de M; a injetividade usa `fibre_injective`. A equivalência não troca essa aplicação por um isomorfismo abstrato sem vínculo: `fixedBaseEquiv_apply` é `rfl` e a inversa tem valor `fibreCandidate`, e*Be. `fixedBaseOrderIso` reutiliza a mesma equivalência e reflete exatamente a ordem positiva herdada, por `fibre_le_iff`. Nenhuma equivalência ultra-fraca/predual nova está declarada aqui.
- {proof('BoundedBaseDualValues',15)}: a existência do valor D em M exige A∈N, A≥0 e uma única cota real não negativa `q_A(v) ≤ ofReal(c‖v‖²)` para todos os vetores. São hipóteses explícitas do caso limitado, não uma solução tácita do caso geral. A positividade de D é refletida por `fibre_nonneg_iff`; o valor representa a mesma q em todos os vetores. Na unicidade (linha 37), D e E são explicitamente positivos, evitando a perda de informação pela parte real/`ofReal`. A existência aplicada aos quadrados finitos e a aproximação `A X_h` preservam a mesma N e M. O enunciado retorna D positivo limitado pelo seu tipo CLM, mas não enuncia adicionalmente uma cota numérica ‖D‖≤c.
- {proof('ScalarDualWeightFaithfulness',23)}: η é separante para **F**, mediante F=imagem de M, `fibre_testVector`, a isometria e e a separação de Ω para M (`factor_omega_separating`). Não se presume que η seja separante para toda N. A minimalidade da energia em ENNReal fornece `Rη=η` quando q_A(η)=0: o termo distância é não negativo e tem cota zero. O resolvente R∈F é obtido por `exists_dualResolvent_fixed`; aplicar separação a R−I∈F dá R=I. Para cada v, a finitude de q_A(Rv) e a identidade de energia são obtidas antes da recuperação de q_A(v) a partir de `toReal`: a linha 78 usa explicitamente `ne_of_lt hfinite`. Assim q_A(v)=0 para **todo** v, e só então a fidelidade anterior da família dá A=0. O teorema final recebe apenas P, A∈N e A≥0; não sobra premissa R, limite forte, separação ou finitude global. Não há conclusão ilícita a partir de um vetor qualquer com valor zero.
- {proof('ScalarDualWeight',15)}: ν é uma função em `PositiveCoreInput P`, cujo subtipo impõe simultaneamente pertinência à mesma N e positividade. Soma e escala permanecem nesse cone. A escala usa NNReal, inclusive zero, com aritmética ENNReal e `0·∞=0`. A normalidade (linha 46) quantifica um preordenado arbitrário, dirigido e não vazio; exige monotonia, positividade dos Aᵢ e `IsLUB (range A) S` **interno à mesma N**. A positividade de S é derivada e o lema anterior de normalidade de q fornece a igualdade com `⨆ i`; não há hipótese final SOT, enumerabilidade ou supremo ambiente. A condição de não vazio é usada no argumento de positividade. Não é circular assumir existência desse supremo como dado do enunciado de preservação.

**Alcance exato da semifinitude.** [REAL — Lean] `HasFiniteDualSquare.scalar_finite` avalia a cota uniforme da forma em η, de norma 1, e conclui ν(A*A)<∞. `scalarDualWeight_square_finite_strong_density` fornece, para todo A∈N, elementos A X_h∈N, de quadrado ν-finito para h>0, convergindo fortemente a A pelo filtro não trivial `𝓝[>] 0`. O ideal complexo esquerdo `finiteDualLeftIdeal` já construído está contido em 𝔫_ν={{x∈N : ν(x*x)<∞}}. Isto é domínio de peso na **álgebra**, distinto de D(q_A) no espaço de Hilbert. Não se afirma que todo A positivo tenha valor finito, nem convergência em norma, nem que A X_h sejam positivos menores que A.

[DERIVED — interpretação matemática, não novo teorema Lean deste pacote] A normalidade por supremos positivos e a densidade obtida dão a semifinitude escalar usual pelo critério de densidade σ-fraca de 𝔫_ν. A ponte topológica é legítima: a dependência `regularAverage_norm_le_one` dá ‖X_h‖≤1, logo ‖A X_h‖≤‖A‖; nessa família limitada, convergência forte implica convergência σ-fraca. Portanto 𝔫_ν é σ-fracamente denso. Trata-se de consequência clássica dos resultados, não de uma formalização adicional da equivalência predual, nem de um enunciado Lean de aproximação crescente por positivos ν-finitos abaixo de cada A. Referência primária: [Blackadar, I.3.1.4 e III.2.2.20–22](https://www.bruceblackadar.com/Mathematics/Cycr.pdf). A expressão “peso escalar fiel, normal e semifinito” é matematicamente compatível com essa ponte explicitada; a minuta escolhe corretamente registrar só as propriedades diretamente provadas.

**Evidência própria.** Árvore: {link(RUN, RUN.name)}. O compilador foi identificado como `{M['lean_version']}`; SHA256 lido `{M['compiler_sha256']}`. Foram executados os quatro módulos e `ScalarDualWeightFullAudit.lean` em árvore própria, todos rc0. O auditor fez `#check` das 25 declarações nomeadas, incluindo as auxiliares `fixedBaseEmbedding` e `regularVacuum`, e `#print axioms` dos 23 alvos solicitados; as duas auxiliares são auditadas transitivamente. Não se somam alvos de módulos futuros. Os quatro binários próprios coincidem byte a byte com os binários DEV finais do autor registrados no congelamento.

| Módulo | Alvos | SHA256 fonte DEV lido | SHA256 .olean próprio lido |
|---|---:|---|---|
{chr(10).join(rows)}

Auditor: fonte `{audit['source_sha256']}`, .olean `{audit['output_sha256']}`. {link(RUN / 'compilation.json')} registra os cinco processos, comandos, saídas e mapa de axiomas; {link(RUN / 'manifest.json')} registra fontes, dependências e `LEAN_PATH`; {link(Path(audit['stdout']), 'tipos e axiomas completos')} contém a saída efetivamente inspecionada. O status DEV congelado tem SHA `{sha((RUN / 'author_scalar_weight_draft_status.json').read_bytes())}`. Os logs finais do autor foram conferidos no congelamento quanto a rc0, fonte inalterada e hashes; isso é inspeção de evidência alheia, distinta das cinco execuções próprias. Tentativas anteriores de elaboração não foram apagadas nem contadas como falhas da versão final.

**Herança controlada.** Foram congeladas {len(deps)} dependências de projeto a partir das árvores próprias anteriores `fixed_core_base_independent_20260912_055602_826535` e `bounded_finite_squares_independent_20260912_042631_245095`, com fontes e binários pinados no manifest. Elas não foram recompiladas nesta etapa. O `LEAN_PATH` aponta para o build próprio e pacotes instalados somente para leitura; não inclui os dois builds autorais do projeto. Mathlib/pacotes e o compilador são herdados, sem rebuild ou alegação de reauditoria integral de seus bytes nesta rodada.

Há uma exceção documental explicitamente medida entre dependência congelada e fonte viva: `DualSemifiniteIdeal` conserva no snapshot o comentário anterior, fonte `{exception['source_sha256']}`, binário `{exception['sha256']}`. A fonte viva corrigida tem SHA `{exception['live_source_sha256']}`. A substituição literal dos bytes do comentário antigo pelo comentário corrigido reproduz integralmente a fonte viva; a errata já havia sido revisada. Não houve mudança de provas. As outras 370 fontes de dependências coincidem com as vivas no congelamento. Não afirmo, portanto, identidade byte a byte de todas as fontes herdadas com o estado autoral atual. Fontes novas, dependências congeladas e pareceres antigos foram conferidos novamente ao fim da compilação e preservados.

**Revisão documental e do mecanismo proposto.** A minuta e o recorder foram lidos integralmente; os dois scripts foram apenas analisados por AST, jamais executados/importados. A minuta distingue normalidade por supremos internos, densidade forte, finitude dos quadrados, valores limitados na base e obrigações ainda abertas. O recorder exige `--review-read`, verifica fontes/binários, imports reescritos, axiomas, SHA do monólito, AST fora do dicionário Lean e seis flags; propõe backup imediato de bytes, append que preserva prefixo e substituição atômica em 21 superfícies. Esta é inspeção estática do mecanismo, não execução ou atestado de custódia futura. A fonte histórica do inventário I/O é comparada ao campo histórico da custódia anterior; não é tratada como liberação do monólito atual. A única correção documental identificada neste estrato é o P2 acima.

| Artefato documental lido | SHA256 |
|---|---|
{docrows}

**Limites e pendência deste estrato.** A inspeção integrada final será acrescentada após o aviso de build/controles finais do autor; ainda não atribuo os relatórios históricos a este incremento. Não houve execução/importação de monólito, recorder, verificador ou testes autorais, nem escrita fora de `revisao/`. Não foram modificados pareceres custodiados, fontes autorais ou memórias. `ScalarModularInvariance` permanece fora do escopo. A identificação do grupo modular/KMS, a construção de traço canônico, a interface geral de peso operatorial/predual, Three Locks/H1–H3, física, contrato ampliado/gate e runtime integral não são resultados desta revisão. Nenhuma flag ou aprovação QG decorre deste parecer.
'''
report = REVIEW / 'REVIEW_SCALAR_DUAL_WEIGHT.md'
create(report, text.encode('utf-8'))
record = {'timestamp': DATE, 'report': str(report), 'report_sha256': sha(report.read_bytes()),
          'report_bytes': report.stat().st_size, 'documents': hashes, 'documentary_snapshot': str(DEST),
          'finding': {'priority': 'P2', 'file': docs[0], 'line': issue_line,
                      'status': 'OPEN_DOCUMENTARY_ONLY', 'missing': 'Re in ENNReal.ofReal'},
          'own_build_complete': True, 'integrated_review_complete': False}
create(DEST / 'source_review.json', json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(record, ensure_ascii=False))
