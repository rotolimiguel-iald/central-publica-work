"""Publish only the independent four-module cyclic cut GNS DEV review."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'cyclic_cut_gns_latest_run.txt').read_text(encoding='utf-8'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M, C, V = (read(RUN / n) for n in ['manifest.json', 'compilation.json', 'verification_dev.json'])
D = read(RUN / 'author_cyclic_cut_gns_draft_status.json')
K = read(RUN / 'gns_cut_maps_custody.json')
for k in ['complete', 'all_exit_zero', 'full_audit_names_exact', 'all_axioms_allowed',
          'sources_unchanged', 'dependencies_unchanged', 'previous_reviews_preserved']:
    assert C[k], k
for k in ['five_compiles_rc0', 'exact_target_set', 'axioms_match_status', 'all_axioms_allowed',
          'dependencies_frozen_preserved', 'author_project_builds_excluded', 'status_unchanged',
          'route_equals_status_and_frozen', 'custody_equals_status',
          'previous_gns_cut_maps_review_equals_custody', 'previous_reviews_preserved']:
    assert V[k], k
for row in V['records'].values():
    for k in ['source_equals_status_and_frozen', 'author_log_identical_to_frozen',
              'author_log_rc0_source_unchanged', 'author_binary_equals_status_and_log',
              'own_binary_equals_compilation_record', 'own_binary_equals_author',
              'target_names_exact', 'author_streams_frozen_equal']:
        assert row[k], k
for row in M['sources'].values():
    assert sha(Path(row['path'])) == sha(Path(row['snapshot'])) == row['sha256']
for row in M['dependencies'].values():
    assert sha(Path(row['frozen_source'])) == row['source_sha256']
    assert sha(Path(row['frozen_binary'])) == row['sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
assert sha(ROOT / 'cyclic_cut_gns_draft_status.json') == V['status_sha256']
assert sha(ROOT / 'ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md') == V['route_sha256']
assert sha(ROOT / 'gns_cut_maps_custody.json') == V['custody_sha256']
assert sha(ROOT / 'um.py') == M['initial_um_sha256'] == D['working_sha256'] == K['working_sha256']
assert len(M['declarations']) == 26 and len(M['all_named_declarations']) == 27
assert set(M['all_named_declarations']) - set(M['declarations']) == {'TGLV350.Regular.ScalarCutHilbert'}
paths = M['lean_path'].split(os.pathsep)
assert paths[0] == str(RUN / 'build') and len(paths) == 9
assert all('\\.lake\\packages\\' in p for p in paths[1:])
assert all('warning:' not in Path(row['stdout']).read_text(encoding='utf-8') and
           Path(row['stderr']).stat().st_size == 0 for row in C['records'])

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

old_verification_raw = (ROOT / 'gns_cut_maps_custody_verification.json').read_bytes()
old_verification = json.loads(old_verification_raw)
assert old_verification['custody_ok'] is True and len(old_verification['exact_prefix_backups']) == 27
write_new(RUN / 'author_gns_cut_maps_custody_verification.json', old_verification_raw)
now = datetime.datetime.now().astimezone()
source_table = '\n'.join('| ' + name + ' | ' + str(len(M['sources']['TGLV350/' + name + '.lean']['declarations'])) +
    ' | `' + row['source_sha256'] + '` | `' + row['own_binary_sha256'] + '` |'
    for name, row in V['records'].items())
logs_table = '\n'.join('| ' + link(Path(row['author_log'])) + ' | `' + row['author_log_sha256'] + '` |'
    for row in V['records'].values())
time_table = '\n'.join('| ' + row['module'] + ' | 0 | ' + str(row['seconds']) + ' |' for row in C['records'])
ex = V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
src = lambda name, line: link(ROOT / 'kernel/TGLV350' / (name + '.lean'), name + '.lean:' + str(line), line)
hist = V['historical_custody_counts']

report = f'''# Revisão independente — GNS cíclico dos cortes

{now.isoformat(timespec='seconds')}. **Escopo DEV concluído, sem achados P0–P2.**

[REAL — inspeção integral e recompilação própria] Os quatro módulos finais e a rota cíclica foram lidos integralmente. **Quatro módulos + auditor próprio passaram rc0**, com 26 `#print axioms` e 27 `#check` com universos explícitos; o tipo adicional é a abreviação `ScalarCutHilbert`. Todos os 26 alvos usam somente `propext`, `Classical.choice`, `Quot.sound`. Os quatro `.olean` produzidos nesta revisão coincidem byte a byte com os binários autorais pinados. Não há análise necessária deste escopo DEV pendente.

O pacote constrói o fecho da órbita de um vetor de corte, a restrição da mesma representação a esse Hilbert e mapas contrativos H_I→H_R com imagem densa. Para R≥0, realiza o funcional ψ_R e sua seminorma por esse vetor. A injetividade provada para os mapas é conjunta sobre os raios naturais. Não se atribuem fidelidade individual, vetor separante, normalidade de π_R ou fechabilidade a essas conclusões.

## Enunciados, tipos e composição

Use-se N=`regularCoreAlgebra P`, K=`RegularHilbert (TowerHilbert P)` e η=`regularVacuum P`. O ambiente comum é **L²(ℝ_s,K)=RegularHilbert (RegularHilbert (TowerHilbert P))**, com medida de Lebesgue. A variável s é a da órbita dual; não é uma projeção finita da torre. A representação ρ é a mesma `dualOrbitRepresentation`, obtida pelo campo θ_s(A). H_I é o espaço anteriormente construído a partir de Λ(I), com I=`finiteDualLeftIdeal P`.

| Fonte/linhas | Alvos conferidos | Alcance efetivo |
|---|---|---|
| {src('ScalarCutVacuum',15)} (15–32) | `scalarCutVacuum`, `scalarCutVacuum_ae` | Ω_R=√c·1_(-R,R]η como classe L², para todo R real; a igualdade de representantes é a.e. |
| {src('ScalarCutVacuum',35)} (35–66) | `scalarGNSCutMap_embedding_eq_action`, `scalarCutVacuum_mem_closure_cut_range` | Para A∈I, o corte de Λ(A) é ρ(A)Ω_R; Ω_R está no fecho da imagem do mapa de corte ambiente. Sem exigir R>0. |
| {src('ScalarCutCyclicSpace',11)} (11–37) | `scalarCutLinear`, `scalarCutSubspace`, `scalarCutCompleteSpace`, `scalarCutEmbedding`; tipo adicional `ScalarCutHilbert` | Γ_R:N→ₗ[ℂ]L², Γ_R(B)=ρ(B)Ω_R. H_R é precisamente o fecho da imagem de Γ_R; completude e codrestrição decorrem desse fecho. |
| {src('ScalarCutCyclicSpace',39)} (39–75) | `scalarCutAmbientAction_preserves`, `scalarCutRepresentation`, `scalarCutCyclicVector`, `scalarCutCyclicVector_val`, `scalarCutRepresentation_intertwines` | Ação preserva H_R, π_R é uma `StarAlgHom` para CLMs complexos de H_R, o vetor cíclico tem valor ambiente Ω_R, e π_R(B)Γ_R(A)=Γ_R(BA). |
| {src('ScalarCutCyclicSpace',77)} (77–112) | `scalarCutEmbedding_denseRange`, `scalarCutCyclicVector_generates`, `scalarGNSCutMap_mem_cyclicSubspace`, `scalarGNSCutCyclicMap` | Órbita cíclica densa, pertinência do corte de todo v∈H_I em H_R, e CLM T_R:H_I→H_R. Não afirma que o recorte preserve H_I. |
| {src('ScalarCutVectorFunctional',13)} (13–49) | `scalarCutVacuum_inner_action`, `scalarCutLinear_norm_sq` | Para R≥0 e todo A∈B(K), igualdade **complexa** ⟨Ω_R,ρ(A)Ω_R⟩=ψ_R(A) e ‖ρ(A)Ω_R‖²=Re ψ_R(A*A). |
| {src('ScalarCutGNSProperties',13)} (13–44) | `scalarCutCyclicVector_functional`, `scalarCutEmbedding_norm_sq`, `scalarGNSCutCyclicMap_embedding`, `scalarGNSCutCyclicMap_intertwines`, `scalarGNSCutCyclicMap_norm_le` | As duas identidades funcionais requerem R≥0. Para todo R: T_RΛ(A)=Γ_R(A) para A∈I, T_Rπ_I(B)=π_R(B)T_R para B∈N e ‖T_Rv‖≤‖v‖. |
| {src('ScalarCutGNSProperties',46)} (46–77) | `scalarGNSCutCyclicMap_joint_zero`, `scalarGNSCutCyclicMap_denseRange` | ∀n∈ℕ, T_n v=0 ⇒ v=0; cada T_R tem `DenseRange`. Não há enunciado de sobrejetividade ou injetividade individual. |

**Haar, raio e produto interno.** `scalarCutVacuum` usa `indicatorConstLp` sobre Ioc(-R,R), cuja medida é finita para todo R. A escala é √c, com c=`dualHaarFactor`=(2π)⁻¹. Na prova do funcional, a linearidade do operador e as leis do produto interno produzem conjugado(√c)·√c=c; `Complex.conj_ofReal` e `Real.sq_sqrt dualHaarFactor_pos.le` justificam exatamente esse fator. Não aparece normalização pelo comprimento do intervalo nem uma segunda multiplicação indevida por c.

R≥0 é usado em `ScalarCutVectorFunctional.lean:19` para -R≤R e para identificar a integral orientada com a integral restrita a Ioc(-R,R). O operador A nessa igualdade pode ser qualquer CLM complexo de K; não se acrescenta positividade de A. A identidade quadrática avalia A*A e transfere o adjunto com `adjoint_inner_right`, respeitando o produto interno complexo linear no segundo argumento. As igualdades no subtipo H_R preservam esse mesmo produto interno.

[DERIVED — inspeção da definição] Se R≤0, Ioc(-R,R) é vazio e Ω_R é a classe zero; o fecho da órbita correspondente é o espaço zero. O pacote não contém uma premissa de não nulidade que exclua esse caso. Isso é compatível com uma representação no Hilbert zero e com as conclusões de densidade. Não se transforma a ciclicidade em separação ou fidelidade. Para R<0, a identidade com ψ_R não é afirmada: o indicador vazio não representa a integral orientada de sinal invertido. Essa análise de borda não foi acrescentada como novo teorema Lean ao auditor.

**Mesma realização, fecho e redução.** `scalarCutSubspace` fecha a imagem de Γ_R sobre **todos os elementos de N**, e não declara por hipótese que o espaço seja cíclico. A linearidade de Γ_R torna sua imagem um submódulo. Em `scalarCutAmbientAction_preserves`, ρ(B)Γ_R(A)=Γ_R(BA) dá invariância da imagem; a continuidade da CLM passa ao fecho. O quantificador é todo B∈N, portanto também inclui B*. A aplicação herdada de `reducingStarRepresentation` é assim legítima e preserva a estrela na restrição. Não se usa normalidade de π_R para construí-la.

O vetor de H_R é Γ_R(1), cujo valor é Ω_R por ρ(1)=1. A igualdade π_R(B)Ω_R=Γ_R(B) e a definição por fecho provam sua ciclicidade. `ScalarCutCyclicSpace.lean:98–107` prova que o mapa de corte de todo H_I chega a H_R usando a preimagem fechada por uma CLM e a densidade **na norma Hilbert** de Λ(I). Em Λ(A), a pertinência é verificada pela identidade efetiva com ρ(A)Ω_R. Somente depois se define a codrestrição `scalarGNSCutCyclicMap`. Os nomes anteriores de corte ambiente e este novo mapa não são identificados apenas por notação: o segundo tem o primeiro como valor ambiente, e `Subtype.ext` fornece os entrelaçamentos.

**Densidade de T_R sem premissa residual.** Em `ScalarCutGNSProperties.lean:54–77`, para cada B∈N toma-se F_h=BX_h, com X_h a mesma média regular contrativa. Para h>0, X_h∈I e a propriedade de ideal à esquerda dá BX_h∈I. A orientação BX_h é essencial e coincide com `scalarGNSLeftProduct`; não é substituída por X_hB. A estimativa ‖BX_h‖≤‖B‖ vale para todo h, inclusive zero, e o limite forte BX_h→B é herdado de X_h→1.

O lema já revisado `dualOrbit_tendsto_of_uniformly_bounded` transfere esse limite para ρ(BX_h)Ω_R→ρ(B)Ω_R na norma ambiente. Sua prova por W₊·fibre(A)·W₋ foi relida na dependência congelada: opera sobre um vetor fixo e não supõe continuidade SOT da operação estrela nem intersecta conjuntos conulos sobre uma rede não enumerável. Em seguida `tendsto_subtype_rng` dá o limite na norma de H_R. O filtro 𝓝[>]0 é não vazio; `nhdsGT_le_nhdsNE 0` restringe corretamente o limite pontuado. Para cada h>0 há uma testemunha concreta Λ(BX_h) na pré-imagem por T_R. Fechar a imagem e usar a densidade de Γ_R conclui `DenseRange T_R`.

A demonstração análoga de `scalarCutVacuum_mem_closure_cut_range` usa X_h e a cota 1. Não se presumem densidade da imagem de T_R, fidelidade de ψ_R ou separação por Ω_R. Não se troca densidade forte em N por densidade Hilbert sem a passagem explícita por ρ. `DenseRange` não demonstra sobrejetividade nem a negação de sobrejetividade.

**Igualdades a.e. e injetividade.** As provas novas de representantes combinam somente um número finito de igualdades a.e. para os vetores e operadores fixados. A injetividade conjunta usa `congrArg Subtype.val` para reduzir ao resultado anterior dos cortes naturais; a interseção enumerável correspondente já foi auditada naquele pacote. Não há uma nova uniformização a.e. sobre todos os vetores ou todos os operadores. A hipótese ∀n,T_n v=0 não é reduzida a um único raio.

## Evidência própria e herança

Árvore independente: {link(RUN)}. O congelamento selecionou **{len(M['dependencies'])} dependências de projeto** necessárias, com fonte e `.olean` pinados e preservados. Reutilizou os catálogos próprios {link(Path(M['previous_run']))} e {link(Path(M['secondary_catalog']))}; o segundo fornece, em particular, `DualOrbitStrongLimits`. Não houve recompilação das dependências ou dos pacotes.

`LEAN_PATH` contém o build único desta revisão e oito diretórios de pacotes externos readonly. Nenhum build autoral de projeto ou diretório autoral de fontes compõe esse caminho. TMP/TEMP são próprios. Compilador: `{M['lean_version']}`; SHA256 `{M['compiler_sha256']}`. A revisão independente usa esse compilador e os pacotes existentes, sem reconstruir sua base de confiança.

A exceção histórica de comentário em `DualSemifiniteIdeal` permanece explícita: fonte própria `{ex['source_sha256']}`, binário próprio herdado `{ex['sha256']}`, fonte autoral atual `{ex['live_source_sha256']}`. A substituição literal do comentário já corrigido foi novamente conferida ao congelar; as provas não diferem nessa exceção. Permanecem as limitações binárias da cadeia herdada registradas nos pareceres anteriores; não se declara igualdade de todos os binários herdados com os autorais. `RegularScalarWeightCertificate` não é importado nesta cadeia. A igualdade binária nova conferida é a dos quatro módulos abaixo.

| Módulo DEV | Alvos | SHA256 fonte final lida | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
{source_table}

| Processo próprio | rc | Segundos |
|---|---|---|
{time_table}

Os cinco processos terminaram sem warnings e com stderr vazio. Auditor: fonte `{V['own_auditor_source_sha256']}`; `.olean` `{V['own_auditor_binary_sha256']}`; stdout `{V['own_auditor_stdout_sha256']}`. A lista exata de 26 nomes e seus axiomas coincide com o status e com as quatro recompilações. O `#check` adicional de `ScalarCutHilbert` confere a abreviação do submódulo usado como tipo; ela também é dependência dos alvos auditados, sem introdução de axioma extra.

| Log autoral final inspecionado | SHA256 JSON |
|---|---|
{logs_table}

Os quatro logs autorais registram rc0 e fonte inalterada. Binários, fontes e streams foram lidos e comparados aos pins e aos snapshots. Os hashes individuais de stdout/stderr próprios e autorais estão em {link(RUN / 'verification_dev.json')}. Comandos, tempos e resultados próprios estão em {link(RUN / 'compilation.json')}; a proveniência por dependência e o caminho de compilação, em {link(RUN / 'manifest.json')}; os tipos completos e axiomas, em {link(RUN / 'logs/CyclicCutGNSAudit.stdout.txt')}. O rc0 próprio é execução desta revisão; os logs autorais são evidência inspecionada. Não foram executados testes autorais.

## Documentação, custódia e limite

A rota `ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md` foi lida inteira, SHA256 **`{V['route_sha256']}`**, igual ao pin e ao snapshot. Suas descrições de Haar, seminorma GNS, fecho cíclico, raio, codomínio, ponte de densidade e injetividade conjunta correspondem aos tipos/provas. A indicação inicial de ausência de revisão independente é o estatuto histórico do arquivo congelado antes deste parecer, não um resultado integrado. Nenhum P2 documental encontrado.

As linhas 40–44 deixam corretamente em aberto a separação necessária para usar os cortes em uma prova de fechabilidade. As linhas 53–57 não presumem I=n_ν e não convertem uma rota bibliográfica em axioma. O presente resultado usa I de quadrados uniformemente limitados; a realização concreta do funcional de corte sobre N não identifica I com o domínio escalar máximo de ν nem fornece por si a ponte de domínio/core exigida por um teorema externo. Nenhuma prova posterior foi examinada. **`ROTA_GAUSSIANA_PARA_FECHABILIDADE.md` não foi lida**, conforme a exclusão expressa.

Status `cyclic_cut_gns_draft_status.json`: SHA256 `{V['status_sha256']}`. Custódia anterior `gns_cut_maps_custody.json`: `{V['custody_sha256']}`, igual ao pin do status; o parecer selado anterior permanece `{V['previous_gns_cut_maps_review_sha256']}`. O arquivo autoral de verificação da custódia foi somente lido e congelado, SHA256 `{hashlib.sha256(old_verification_raw).hexdigest()}`: declara `custody_ok=true` e 27 prefixos/backups. Não se reexecutou o verifier nem se revalidaram os 27 pares neste escopo.

As contagens **{hist['integrated_records']} registros/{hist['controls']} controles/{hist['audit_declarations']} Audit** pertencem à custódia anterior. A cópia permanece `{M['initial_um_sha256']}`, conferida por hash ao encerrar. **Este parecer é DEV: nenhuma integração nova foi inspecionada ou atribuída aos quatro módulos.** Os {len(M['previous_reviews'])} pareceres anteriores mantêm seus hashes; fontes autorais, originais, memórias e custódias não foram alterados. Todas as saídas desta revisão ficam em `revisao/`.

**Conclusão delimitada:** quatro módulos/26 alvos e rota cíclica conferidos, com recompilação e auditor próprios, sem P0, P1 ou P2. Construídos o Hilbert cíclico concreto, sua representação restrita, o funcional vetorial para R≥0 e as contrações entrelaçadoras de imagem densa e conjuntamente injetivas. Não se certificam fidelidade de ψ_R ou π_R, vetor Ω_R separante, normalidade de π_R, sobrejetividade ou injetividade individual de T_R, igualdade I=n_ν, fechabilidade/Tomita fechado, KMS, traço, gate ou runtime. Monólito, recorders e verifiers autorais não foram executados/importados. Não há pendência dentro deste escopo DEV.
'''

path = REVIEW / 'REVIEW_CYCLIC_CUT_GNS.md'
write_new(path, report.encode('utf-8'))
result = {
    'timestamp': now.isoformat(timespec='seconds'), 'status': 'DEV_COMPLETE_NO_P0_P1_P2',
    'review_path': str(path), 'review_sha256': sha(path), 'review_bytes': path.stat().st_size,
    'new_sources': 4, 'new_targets': 26, 'type_checks': 27, 'own_compiler_processes_rc0': 5,
    'own_bins_equal_author': True, 'project_dependencies': len(M['dependencies']),
    'previous_reviews_preserved': all(sha(Path(p)) == h for p, h in M['previous_reviews'].items()),
    'integrated_inspection_performed': False, 'author_programs_executed': False,
    'gaussian_route_read': False, 'working_sha256_at_close': sha(ROOT / 'um.py'), 'findings': []
}
write_new(RUN / 'closure_dev.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
