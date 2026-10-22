"""Publish the independent Gaussian closability review inside revisao only."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'gaussian_closability_latest_run.txt').read_text(encoding='utf-8'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M, C, V, S = (read(RUN / n) for n in ['manifest.json', 'compilation.json', 'verification_dev.json', 'structural_inspection.json'])
D = read(RUN / 'author_gaussian_closability_draft_status.json')
K = read(RUN / 'gns_cut_maps_custody.json')
for k in ['complete', 'all_exit_zero', 'full_audit_names_exact', 'all_axioms_allowed',
          'sources_unchanged', 'dependencies_unchanged', 'previous_reviews_preserved']:
    assert C[k], k
for k in ['ten_compiles_rc0', 'exact_target_set', 'axioms_match_status', 'all_axioms_allowed',
          'dependencies_frozen_preserved', 'author_project_builds_excluded', 'status_unchanged',
          'report_equals_status_and_frozen', 'custody_equals_status',
          'previous_gns_cut_maps_review_equals_custody', 'previous_reviews_preserved']:
    assert V[k], k
for row in V['records'].values():
    for k in ['source_equals_status_and_frozen', 'author_log_equals_status_hash',
              'author_log_identical_to_frozen', 'author_log_rc0_source_unchanged',
              'author_binary_equals_status_and_log', 'own_binary_equals_compilation_record',
              'own_binary_equals_author', 'target_names_exact', 'author_streams_frozen_equal']:
        assert row[k], k
for row in M['sources'].values():
    assert sha(Path(row['path'])) == sha(Path(row['snapshot'])) == row['sha256']
for row in M['dependencies'].values():
    assert sha(Path(row['frozen_source'])) == row['source_sha256']
    assert sha(Path(row['frozen_binary'])) == row['sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
assert sha(ROOT / 'gaussian_closability_draft_status.json') == V['status_sha256']
assert sha(ROOT / 'RELATORIO_FECHABILIDADE_GAUSSIANA_DEV.md') == V['report_sha256']
assert sha(ROOT / 'gns_cut_maps_custody.json') == V['custody_sha256']
assert sha(ROOT / 'um.py') == M['initial_um_sha256'] == D['working_sha256'] == K['working_sha256']
assert len(M['declarations']) == len(M['all_named_declarations']) == 49
assert S['acyclic_frozen_project_imports']
assert not S['faithfulness_import_ancestors_intersect_new'] and not S['original_graph_import_ancestors_intersect_new']
assert sha(REVIEW / 'REVIEW_CYCLIC_CUT_GNS.md') == S['prior_cyclic_review_sha256']
assert 'TGLV350.ScalarClosedTomita' not in M['dependencies']
paths = M['lean_path'].split(os.pathsep)
assert paths[0] == str(RUN / 'build') and len(paths) == 9
assert all('\\.lake\\packages\\' in p for p in paths[1:])
warnings = {row['module']: [line for line in Path(row['stdout']).read_text(encoding='utf-8').splitlines()
                          if 'warning:' in line] for row in C['records']}
assert not any(warnings.values()) and all(Path(row['stderr']).stat().st_size == 0 for row in C['records'])
FAILED = REVIEW / 'gaussian_closability_independent_20260912_094031_488663'
failed = read(FAILED / 'compilation.json')
assert not failed['complete'] and failed['records'][0]['returncode'] == 1
assert "unknown module prefix 'Mathlib'" in Path(failed['records'][0]['stdout']).read_text(encoding='utf-8')
failed_manifest = read(FAILED / 'manifest.json')
assert all(failed_manifest['sources'][n]['sha256'] == r['sha256'] for n, r in M['sources'].items())

def write_new(path, raw):
    assert path.resolve().is_relative_to(REVIEW) and not path.exists()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw and tmp.stat().st_size == len(raw) > 0
    tmp.replace(path)
    assert path.read_bytes() == raw

def link(path, label=None, line=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + (':' + str(line) if line else '') + '>)'

now = datetime.datetime.now().astimezone()
source_table = '\n'.join('| ' + name + ' | ' + str(len(M['sources']['TGLV350/' + name + '.lean']['declarations'])) +
    ' | `' + row['source_sha256'] + '` | `' + row['own_binary_sha256'] + '` |'
    for name, row in V['records'].items())
logs_table = '\n'.join('| ' + link(Path(row['author_log'])) + ' | `' + row['author_log_sha256'] + '` |'
    for row in V['records'].values())
time_table = '\n'.join('| ' + row['module'] + ' | 0 | ' + str(row['seconds']) + ' |' for row in C['records'])
target_table = '\n'.join('| ' + Path(rel).stem + ' | ' + ', '.join('`' + n.split('.')[-1] + '`' for n in r['declarations']) + ' |'
                         for rel, r in M['sources'].items())
src = lambda name, line: link(ROOT / 'kernel/TGLV350' / (name + '.lean'), name + '.lean:' + str(line), line)
ex = V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
hist = V['historical_custody_counts']

report = f'''# Revisão independente — fechabilidade gaussiana

{now.isoformat(timespec='seconds')}. **DEV concluído, sem achados P0–P2.**

[REAL — inspeção integral e recompilação própria] Foram lidos os nove módulos finais e o relatório autoral completo. **Nove módulos + auditor próprio passaram rc0**, com 49 tipos conferidos por `#check` com universos explícitos e 49 `#print axioms`. Todos os alvos usam somente `propext`, `Classical.choice`, `Quot.sound`. Os nove `.olean` próprios coincidem byte a byte com os autorais pinados. Não há análise necessária deste escopo pendente.

A conclusão conferida é a **univalência do fecho de `scalarTomitaGraph P` no H_I original**, inclusive ausência de fibras verticais não nulas. O transporte gaussiano não troca esse gráfico pelo de outro peso. O pacote não empacota um operador fechado antilinear, não identifica I com n_ν e não prova KMS ou traço. `ScalarClosedTomita.lean` ficou excluído, sem leitura ou compilação.

## Resultado e tipos exatos

Em {src('ScalarGaussianClosureTransport',48)}, para qualquer P e y:`ScalarGNSHilbert P`, a hipótese `(0,y) ∈ closure (scalarTomitaGraph P)` implica `y=0`. Em {src('ScalarGaussianClosureTransport',60)}, para x,y,z no **mesmo** H_I, duas pertinências `(x,y),(x,z)` ao mesmo fecho implicam `y=z`. Os tipos finais não têm premissas residuais de separação, ciclicidade, continuidade do transporte, inversa limitada, domínio máximo, normalidade de representação ou fechabilidade.

O tipo original foi relido em `ScalarTomitaGraph.lean:18–20`: o conjunto é a imagem de A∈`finiteDualStarCore P` por A↦(Λ(A),Λ(A*)). `FiniteDualStarCore.lean:16–18` usa o subálgebra sem unidade definida por `HasFiniteDualSquare A ∧ HasFiniteDualSquare (star A)`, isto é, I∩I*. `ScalarGNSStarDensity.lean:13–14` usa a mesma `scalarGNSEmbedding`. A densidade do domínio e a univalência inicial pertencem às dependências já revistas; nesta etapa prova-se a univalência **após tomar fecho**, sem assumir que o gráfico inicial já era fechado.

N=`regularCoreAlgebra P`, K=`RegularHilbert (TowerHilbert P)` e o ambiente auxiliar é **L²(ℝ_s,K)=RegularHilbert (RegularHilbert (TowerHilbert P))**, com Lebesgue. H_I é o subespaço fechado anterior nesse ambiente. Os lemas genéricos usam H:`Type` com as instâncias de grupo normado, produto interno complexo e, onde requerido, completude; os tipos impressos não exigem separabilidade ou dimensão finita. Não se promove esse `Type` a uma generalidade de universos além da efetivamente impressa.

## Pontos adversariais conferidos

**Multiplicador e Gaussiana — {src('L2PositiveMultiplier',13)} (13–70), {src('L2GaussianProfile',14)} (14–40).** O campo é g(s)·id, com g real contínua e 0≤g≤1; a cota de norma é demonstrada, e seu lift é CLM complexo contrativo no L². A injetividade acrescenta g(s)>0 para todo s. A prova cancela o escalar não nulo em igualdades a.e. para dois vetores fixos; não constrói 1/g como operador limitado nem presume limite inferior uniforme positivo. A comutação com um campo `StrongIntegral.Family` usa quatro igualdades a.e. e `map_smul` para cada vetor fixo.

O perfil escolhido é exatamente exp(-s²), com 0<g≤1. A prova `MemLp` do vetor g(s)v usa continuidade forte e integrabilidade da norma quadrática: ‖g(s)v‖²=exp(-2s²)‖v‖², seguida do lema de integral gaussiana com parâmetro **2>0**. Não trata a constante não nula na reta como L², nem usa integral real divergente com valor padrão ou `toReal` de infinito.

**Separação e Haar — {src('ScalarGaussianVacuum',14)} (14–68).** Ω_g é a classe L² de g(s)√cη, com o mesmo c=`dualHaarFactor`=(2π)⁻¹ e η=`regularVacuum P`. `gaussian_zero_action_orbit_ae` parte de ρ(A)Ω_g=0 no L² e combina as igualdades a.e. do vetor, do campo aplicado e do vetor zero. Cancela g(s)>0 e √c>0 **antes** de avaliar a integral estendida, obtendo θ_s(A)η=0 a.e. Esse passo não usa inversão limitada, troca de medida ou interseção não enumerável.

Em seguida a identidade herdada do integrando de A*A dá q_(A*A)(η)=0 por `lintegral_congr_ae`. A pertinência A*A∈N é construída por fechamento sob estrela/produto; `star_mul_self_nonneg` fornece a positividade necessária à fidelidade previamente provada. Dessa fidelidade resulta A*A=0 e a identidade de C*-álgebra dá A=0. Não se infere nulidade de A apenas de Aη=0. A primeira prova de separação tem **hA:A∈regularCoreAlgebra P**; não a reivindica para toda B(K), nem para η sob N.

A dependência `ScalarDualWeightFaithfulness.lean:54–81` foi relida. Ela usa o resolvente fixo e a separação de η para a álgebra fixa, obtém R=1, verifica finitude antes de `toReal` e conclui fidelidade da família original. Nenhum destes nove módulos ocorre em seus ancestrais de importação. Não há uso da nova separação para provar a fidelidade invocada pela própria separação.

**Bicomutante da amplificação — {src('FibreVonNeumann',12)} (12–71).** O conjunto gerador é a imagem `fibre '' N`, fechada sob estrela porque N o é e `fibre_star` preserva o adjunto. `mem_fibreImage_centralizer` verifica também o requisito de comutação com a estrela dos geradores; não confunde comutante de conjunto arbitrário com centralizador estrelado.

Para B no bicomutante, shifts e caracteres **externos** estão no primeiro comutante, pois comutam com todas as fibras constantes. Assim B satisfaz exatamente as duas hipóteses do lema genérico `eq_fibre_of_shift_character_commutation`, relido em `ConstantFibreIdentification.lean:15–39`. Obtém-se B=fibre(C) no L² inteiro. Para cada D∈N′, fibre(D) também está no primeiro comutante; a comutação com B, a multiplicatividade e a injetividade de `fibre` dão DC=CD. Logo C∈N′′=N. O sentido inverso é a inclusão de um gerador. A fibra extraída não fica apenas em B(H), e não se assume por hipótese que a amplificação já seja de von Neumann.

Essa aplicação reutiliza a identificação constante já revisada, baseada em localidade e recortes/translações. Não pressupõe uma decomposição constante adicional, F=base como premissa nova, separabilidade de H ou um ponto a.e. comum a todos os vetores. Os shifts/caracteres aqui agem na variável de amplificação; não são confundidos com geradores internos arbitrários de N.

**Unitário efetivo e imagem inteira — {src('DualOrbitVonNeumann',13)} (13–83).** As leis novas dão W_a*=W_(-a), W_aW_b=W_(a+b) e W_0=1 para o lift do campo s↦D_(as). Ambas as identidades unitárias de W=W_1 são provadas; `dualOrbitImplementer` é realmente um elemento de `unitary`. A equivalência `dualOrbitConjugation` é a conjugação A↦WAW*. O sinal de W* é o lift a=-1, consistente com o lema anterior `dualOrbit_factorization`.

`dualOrbitConjugation_fibre` identifica essa conjugação com a **mesma** ρ(A) usada na inscrição e no vetor gaussiano. `generated_transport`, relido em `GeneratedEquivariance.lean:48–54`, transporta o bicomutante por uma equivalência de *-álgebras efetiva; não assume normalidade da imagem. Aplicado à equivalência unitária e ao resultado sobre `fibre '' N`, prova

`B ∈ dualOrbitVonNeumann N ↔ ∃ A∈N, B=dualOrbitRepresentation A`.

Portanto, ao aplicar a separação ao VN auxiliar, não se passa apenas de separação dos geradores para separação de uma álgebra maior sem justificativa: todo B do VN é uma imagem de A∈N. `scalarGaussianImage_separating` (linhas 14–20 do módulo final) usa exatamente essa equivalência.

**Separação implica órbita do comutante densa — {src('SeparatingCyclicCommutant',13)} (13–69).** Para um VN concreto N e v separante, E é o fecho em norma da órbita N′v. A órbita é imagem linear, logo seu fecho é um submódulo completo. Sua invariância sob A e A* para todo A∈N′ permite aplicar `starProjection_commutes_of_invariant` com ambas as hipóteses verificadas. Assim a projeção ortogonal E.starProjection pertence a N′′=N.

Como 1∈N′, v∈E. O complemento 1−P_E está em N e anula v; a separação força 1−P_E=0 e E=⊤. Trata-se da projeção sobre o fecho dessa órbita, sem dimensão finita ou uso como P_F. O lema não supõe que Nv seja denso no ambiente. A hipótese de separação é explícita no lema genérico e é demonstrada na aplicação concreta.

**Pareamento e fechos — {src('VectorTomitaClosability',13)} (13–53).** O gráfico auxiliar é o conjunto de pares (Av,A*v), A∈N. O pareamento correto é

`⟨A*v,Bv⟩ = ⟨B*v,Av⟩` para B∈N′.

Com o produto interno complexo linear no segundo argumento, `adjoint_inner_left` reduz ambos os lados a ⟨v,ABv⟩ e ⟨v,BAv⟩. A orientação da comutação usada coincide com esses produtos. Para B fixo, essa identidade define um subconjunto fechado do produto Hilbert por continuidade dos dois pareamentos. `closure_minimal` estende a identidade ao fecho do gráfico; não há passagem de limite sob um adjunto não limitado, escolha de representantes a.e. ou hipótese de fechabilidade nessa etapa.

Para (0,y), os pareamentos com todos Bv anulam y pela densidade de N′v. Para dois pares (x,y),(x,z), a igualdade de todos esses pareamentos dá y=z. A prova de univalência é direta: não trata o gráfico antilinear como subespaço complexo linear para subtrair pontos, nem exige que a órbita Nv seja densa.

**Retorno ao H_I original — {src('ScalarGaussianGNSMap',14)} (14–59), {src('ScalarGaussianClosureTransport',22)} (22–67).** T é M_g composto com a inclusão de H_I no seu ambiente original. Contratividade e injetividade são provadas por essa composição. O contradomínio é L² ambiente; não se presume T(H_I)⊆H_I. O entrelaçamento com π_I decorre da comutação com o mesmo campo dual. Na inscrição A∈I, a igualdade TΛ(A)=ρ(A)Ω_g usa exatamente g(s)√cθ_s(A)η nos dois lados; não há troca de Haar.

Para cada A∈I∩I*, o transporte dos dois componentes do gráfico aplica essa igualdade a A e a A*, com suas pertinências ao ideal explicitadas. O segundo componente usa `map_star` de ρ, obtendo a estrela do mesmo operador do primeiro componente. `Prod.map T T` envia, portanto, o gráfico original ao gráfico auxiliar. Sua continuidade fornece somente a inclusão necessária: imagem do fecho original contida no fecho auxiliar. Não se afirma igualdade entre esses fechos ou continuidade de uma inversa.

De (0,y) no fecho original obtém-se (0,Ty) no auxiliar, depois Ty=0 e y=0 por injetividade. De dois pares com o mesmo x obtém-se Ty=Tz e y=z. O peso original, o ideal, o H_I e a topologia de seu produto permanecem os mesmos. Não há premissa I=n_ν, sobrejetividade de T ou inversa limitada oculta.

## Cobertura e evidência

Todos os nomes abaixo receberam `#check` com universos explícitos e `#print axioms` no auditor próprio. A lista coincide exatamente com os 49 alvos do status, incluindo definições e a instância de completude.

| Módulo | Alvos |
|---|---|
{target_table}

Árvore própria: {link(RUN)}. **{len(M['dependencies'])} dependências de projeto** foram selecionadas, copiadas de fontes/binários próprios já revisados e pinadas individualmente, sem recompilar pacotes ou dependências. Os catálogos vieram de {link(Path(M['previous_run']))} e {link(Path(M['secondary_catalog']))}. A revisão cíclica anterior é apenas proveniência reutilizável; seus quatro módulos não são promovidos a integração por este parecer.

O build desta árvore é o único build de projeto no `LEAN_PATH`; seguem-se oito diretórios de pacotes externos readonly. Nenhum build autoral de projeto é usado na resolução. TMP/TEMP ficam na árvore própria. Compilador `{M['lean_version']}`, SHA256 `{M['compiler_sha256']}`. A base do compilador e os pacotes são herdados em leitura, não reconstruídos nesta revisão.

Foi preservada uma primeira tentativa em {link(FAILED)}, que parou no primeiro import com `unknown module prefix 'Mathlib'` no ambiente restrito. Não é uma falha de elaboração das provas. A segunda árvore usou a leitura autorizada dos mesmos pacotes externos, manteve os mesmos bytes de fontes e concluiu os dez processos. O log da tentativa inicial não foi apagado ou aceito como compilação.

Mantém-se a exceção histórica de comentário de `DualSemifiniteIdeal`: fonte própria `{ex['source_sha256']}`, binário herdado `{ex['sha256']}`, fonte autoral atual `{ex['live_source_sha256']}`. A diferença literal é somente a errata documental já revisada, novamente conferida ao congelar. As limitações binárias herdadas continuam as registradas nos pareceres anteriores; não se afirma reprodução autoral de toda a cadeia. A identidade byte a byte nova comprovada é a dos nove módulos abaixo.

| Módulo DEV | Alvos | SHA256 fonte final | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
{source_table}

| Processo próprio | rc | Segundos |
|---|---|---|
{time_table}

Os dez processos finais ficaram sem warnings e com stderr vazio. Auditor: fonte `{V['own_auditor_source_sha256']}`, `.olean` `{V['own_auditor_binary_sha256']}`, stdout `{V['own_auditor_stdout_sha256']}`. Os nomes e conjuntos de axiomas coincidem com os pins autorais; não há `sorryAx` ou axioma adicional. O auditor não acrescenta hipóteses ou provas substitutas.

| Log autoral final inspecionado | SHA256 JSON |
|---|---|
{logs_table}

Os nove logs autorais, seus hashes declarados, fontes inalteradas, binários e streams foram comparados aos artefatos vivos e aos snapshots. **Recompilação própria**: {link(RUN / 'compilation.json')}; **hashes e confronto com logs autorais**: {link(RUN / 'verification_dev.json')}; **proveniência por dependência**: {link(RUN / 'manifest.json')}; **tipos completos/axiomas próprios**: {link(RUN / 'logs/GaussianClosabilityAudit.stdout.txt')}. Não foram executados testes ou scripts autorais.

A inspeção estrutural {link(RUN / 'structural_inspection.json')} registra imports acíclicos dos {S['frozen_project_modules']} módulos de projeto congelados, ausência destes nove nos ancestrais da fidelidade e do gráfico original e ausência de import do módulo posterior excluído. Essa verificação complementa a leitura das provas, não a substitui. `ScalarTomitaGraph` foi reutilizado com fonte `{S['original_graph_source_sha256']}` e `.olean` `{S['original_graph_olean_sha256']}`; a fidelidade com fonte `{S['faithfulness_source_sha256']}` e `.olean` `{S['faithfulness_olean_sha256']}`.

## Documentação e limite final

`RELATORIO_FECHABILIDADE_GAUSSIANA_DEV.md` foi lido integralmente, SHA256 **`{V['report_sha256']}`**, idêntico ao pin e ao snapshot. Sua afirmação de fechabilidade/univalência do fecho corresponde aos enunciados efetivos; o texto distingue o gráfico original, a separação apenas da imagem concreta, o transporte contínuo injetivo e as obrigações ainda abertas. Não foi encontrado P2 documental. Seu estatuto de revisão pendente é o do arquivo congelado antes deste parecer.

Status `gaussian_closability_draft_status.json`: `{V['status_sha256']}`. A custódia pai `gns_cut_maps_custody.json`, `{V['custody_sha256']}`, foi comparada ao pin do status e ao parecer nela selado. As contagens **{hist['integrated_records']} registros/{hist['controls']} controles/{hist['audit_declarations']} Audit** e a cópia `{M['initial_um_sha256']}` pertencem à integração anterior, lida da custódia; o hash da cópia foi conferido ao fechar. Não houve inspeção de integração nova destes nove, nem soma de seus 49 alvos às contagens antigas, nem reexecução da custódia ou de controles anteriores.

O parecer cíclico anterior permanece `{S['prior_cyclic_review_sha256']}` e os {len(M['previous_reviews'])} pareceres prévios mantiveram seus hashes. Todas as escritas foram em `revisao/`; não foram alterados fontes autorais, originais, monólito, memórias ou custódias. Não foram executados/importados monólito ou recorders. O status de 49 alvos não foi alterado.

**Conclusão delimitada:** sem P0, P1 ou P2 nos nove módulos e no relatório congelados. Está conferida, em DEV com recompilação própria, a fechabilidade do gráfico especificado no H_I original, sem hipótese residual adicional nos dois teoremas finais. Permanecem fora desta conclusão: empacotamento do operador fechado antilinear, adjunto/decomposição modular, identificação do domínio máximo ou ponte de core para teorema externo, KMS, traço canônico, escala dual do traço, Three Locks/H1–H3, física, consumo pelo gate e runtime. `ScalarClosedTomita.lean` não foi lido nem compilado. Escopo DEV encerrado.
'''
path = REVIEW / 'REVIEW_GAUSSIAN_CLOSABILITY.md'
write_new(path, report.encode('utf-8'))
result = {
    'timestamp': now.isoformat(timespec='seconds'), 'status': 'DEV_COMPLETE_NO_P0_P1_P2',
    'review_path': str(path), 'review_sha256': sha(path), 'review_bytes': path.stat().st_size,
    'new_sources': 9, 'new_targets': 49, 'type_checks': 49, 'own_compiler_processes_rc0': 10,
    'own_bins_equal_author': True, 'project_dependencies': len(M['dependencies']),
    'previous_reviews_preserved': all(sha(Path(p)) == h for p, h in M['previous_reviews'].items()),
    'integrated_inspection_performed': False, 'author_programs_executed': False,
    'excluded_ScalarClosedTomita_read_or_compiled': False,
    'working_sha256_at_close': sha(ROOT / 'um.py'), 'findings': [],
    'preserved_initial_environment_failure': str(FAILED / 'compilation.json')
}
write_new(RUN / 'closure_dev.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
