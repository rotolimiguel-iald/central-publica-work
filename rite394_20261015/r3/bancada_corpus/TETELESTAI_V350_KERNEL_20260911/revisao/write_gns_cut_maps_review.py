"""Write the independent nine-target DEV review without changing author files."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'gns_cut_maps_latest_run.txt').read_text(encoding='utf-8'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M, C, V = (read(RUN / n) for n in ['manifest.json', 'compilation.json', 'verification_dev.json'])
D = read(RUN / 'author_gns_cut_maps_draft_status.json')
K = read(RUN / 'bounded_scalar_cuts_custody.json')
for k in ['complete', 'all_exit_zero', 'full_audit_names_exact', 'all_axioms_allowed',
          'sources_unchanged', 'dependencies_unchanged', 'previous_reviews_preserved']:
    assert C[k], k
for k in ['three_compiles_rc0', 'exact_target_set', 'axioms_match_status', 'all_axioms_allowed',
          'dependencies_frozen_preserved', 'author_project_builds_excluded', 'status_unchanged',
          'route_equals_status_and_frozen', 'custody_equals_status',
          'previous_bounded_scalar_cuts_review_equals_custody', 'previous_reviews_preserved']:
    assert V[k], k
for row in V['records'].values():
    for k in ['source_equals_status_and_frozen', 'author_log_identical_to_frozen',
              'author_log_rc0_source_unchanged', 'author_binary_equals_status_and_log',
              'own_binary_equals_compilation_record', 'own_binary_equals_author',
              'target_names_exact', 'author_streams_frozen_equal']:
        assert row[k], k
for row in M['sources'].values():
    assert sha(Path(row['path'])) == sha(Path(row['snapshot'])) == row['sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
assert sha(ROOT / 'gns_cut_maps_draft_status.json') == V['status_sha256']
assert sha(ROOT / 'ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md') == V['route_sha256']
assert sha(ROOT / 'bounded_scalar_cuts_custody.json') == V['custody_sha256']
assert sha(ROOT / 'um.py') == M['initial_um_sha256'] == D['working_sha256'] == K['working_sha256']
assert len(M['declarations']) == len(M['all_named_declarations']) == 9
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

def link(path, label=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + '>)'

old_verification_raw = (ROOT / 'bounded_scalar_cuts_custody_verification.json').read_bytes()
old_verification = json.loads(old_verification_raw)
assert old_verification['custody_ok'] is True and len(old_verification['exact_prefix_backups']) == 26
write_new(RUN / 'author_bounded_scalar_cuts_custody_verification.json', old_verification_raw)
now = datetime.datetime.now().astimezone()
source_table = '\n'.join('| ' + name + ' | ' + str(len(M['sources']['TGLV350/' + name + '.lean']['declarations'])) +
    ' | `' + row['source_sha256'] + '` | `' + row['own_binary_sha256'] + '` |'
    for name, row in V['records'].items())
logs_table = '\n'.join('| ' + link(Path(row['author_log'])) + ' | `' + row['author_log_sha256'] + '` |'
    for row in V['records'].values())
time_table = '\n'.join('| ' + row['module'] + ' | 0 | ' + str(row['seconds']) + ' |' for row in C['records'])
ex = V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
report = f'''# Revisão independente — mapas GNS dos cortes

{now.isoformat(timespec='seconds')}. **DEV concluído, sem achados P0–P2.**

[REAL — inspeção integral de fontes/documentação e recompilação própria] Foram lidos os dois módulos finais e a rota completa, conferidos seus nove enunciados e recompilados **dois DEV + auditor próprio**, todos rc0. O auditor emite nove `#check` com universos explícitos e nove `#print axioms`, cobrindo todas as declarações nomeadas novas, inclusive `scalarGNSCutMap`. Somente `propext`, `Classical.choice`, `Quot.sound`; os dois `.olean` próprios coincidem byte a byte com os autorais pinados. Não há análise necessária deste escopo DEV pendente.

O resultado é uma família de contrações do mesmo H_I para o L² ambiente, entrelaçando π_I e ρ, conjuntamente injetiva nos raios naturais, com ‖T_RΛ(A)‖²=Re ψ_R(A*A) para A∈I e R≥0. Não se concluem preservação de H_I pelo corte, novo GNS cíclico, vetor separante, fechabilidade ou integração desses DEV.

## Nove alvos e hipóteses conferidos

| Fonte/linhas | Alvos | Conclusão da revisão |
|---|---|---|
| `ScalarGNSCutMaps.lean:14–25` | `measurableCut_operatorFieldLift` | Qualquer conjunto S mensurável, sem hipótese de medida finita. F é uma `StrongIntegral.Family`: campo de operadores limitados, uniformemente limitado e fortemente contínuo. A comutação com indicador não requer comutação entre operadores do campo ou invariância de H_I. Não se ampliou o enunciado para campos arbitrários apenas mensuráveis. |
| `ScalarGNSCutMaps.lean:28–46` | `measurableCut_nat_joint_zero` | Para um f fixo, cortes Ioc(-n,n) nulos para todos os naturais implicam f=0 como classe L². A única interseção infinita de conjuntos conulos é enumerável, sobre ℕ. |
| `ScalarGNSCutMaps.lean:50–56` | `scalarGNSCutMap`, `scalarGNSCutMap_norm_le` | CLM complexo `measurableCut.comp subtypeL`, definido para todo R∈ℝ, com ‖T_Rv‖≤‖v‖. A inclusão de H_I no ambiente conserva a norma. O contradomínio está explicitamente fora do subtipo H_I. |
| `ScalarGNSCutMaps.lean:58–68` | `scalarGNSCutMap_intertwines`, `scalarGNSCutMap_joint_zero` | Para todo B∈N e v∈H_I, T_Rπ_I(B)v=ρ(B)T_Rv. A aplicação do lema de campo usa exatamente `dualIntegralFamily B.val`; π_I é a restrição da mesma ρ. A injetividade conjunta em H_I segue por `Subtype.ext` da injetividade conjunta ambiente, sem novo pressuposto de separação. |
| `ScalarGNSCutNorm.lean:13–19` | `measurableCut_norm_sq` | ‖1_Sf‖²=∫_S‖f‖² para todo S mensurável e f∈L², sem exigir μ(S)<∞. A integral é real e efetivamente integrável por f∈L²; não há uso indevido do valor padrão de uma integral divergente. |
| `ScalarGNSCutNorm.lean:21–35` | `dualCutFunctional_square_re` | Re ψ_(R,v)(A*A)=c∫_(-R)..R‖θ_s(A)v‖² para todo R e A ambiente. A conjugação dual preserva produto e estrela; o passo de adjunto usa o produto interno na orientação correta. Não é necessário A positivo, pois a entrada avaliada é A*A. |
| `ScalarGNSCutNorm.lean:39–48` | `scalarGNSCutMap_embedding_norm_sq` | Para A no ideal já construído I e R≥0, identifica a norma do corte da mesma Λ(A) com o mesmo ψ_R(A*A). R≥0 é usado exatamente para converter a integral orientada no integral restrito a Ioc(-R,R). |

**Espaços e objetos exatos.** A abreviação `RegularHilbert H` é `Lp H 2 (volume : Measure ℝ)`. Neste pacote, o K da notação L²(ℝ,K) da rota corresponde a **RegularHilbert(TowerHilbert P)**. Portanto o contradomínio de T_R é

`RegularHilbert (RegularHilbert (TowerHilbert P)) = L²(ℝ_s, L²(ℝ_t, TowerHilbert P))`.

H_I é o fecho da imagem de `scalarGNSLinear P` nesse ambiente. O corte atua na variável externa s da órbita dual; não é uma projeção finita da torre, nem a definição de um suporte espectral. O tipo impresso pelo auditor confirma ambas as camadas L². `scalarGNSRepresentation` restringe `dualOrbitRepresentation` a H_I; esta última é `operatorFieldLift (dualIntegralFamily B.val)`. O entrelaçamento tem como lado direito a ação **ambiente** sobre T_Rv, sem precisar demonstrar T_Rv∈H_I. Essa igualdade não usa apenas representações homônimas: as definições de restrição e campo foram relidas nas dependências congeladas.

**Quociente L² e mensurabilidade.** `L2MeasurableCut.lean:12–17,42–57`, relido, constrói o recorte com `MemLp.indicator hS`, `toLp` e igualdade a.e.; a cota vem de dominação pontual a.e. `StrongOperatorField.lean:15–37,64–69` fornece a mensurabilidade do campo aplicado ao vetor L² pela continuidade forte com limite uniforme. Não se presume continuidade pontual de representantes L² ou separabilidade de H.

Em `measurableCut_operatorFieldLift`, quatro igualdades a.e. são combinadas para o f fixo: os dois lifts e os dois recortes relevantes. A análise x∈S/x∉S usa respectivamente a identidade do campo e `map_zero`. Não existe interseção sobre todos os vetores, operadores ou conjuntos mensuráveis. Em `measurableCut_nat_joint_zero`, primeiro se obtém ∀n, a.e. x∈Ioc(-n,n)⇒f(x)=0; somente então `ae_all_iff` troca a quantificação sobre ℕ. Para cada x escolhe-se n>|x|, incluindo corretamente os endpoints e x=0, e conclui-se igualdade de classes por `Lp.ext`. Assim a exigência conjunta não foi substituída por fidelidade de um único corte.

**Norma, adjunto e Haar.** O lema herdado `Fourier.L2_integral_norm_sq` (`FourierL1L2.lean:56–60`) foi relido: decorre do produto interno L² com `L2.integrable_inner`. Não requer uma hipótese de Fourier nem transforma ∞ por `toReal`. Aplicado ao recorte e seguido da fórmula do indicador, justifica a norma para qualquer S mensurável, mesmo de medida infinita.

A identidade do funcional usa a preservação do produto e do adjunto pela ação dual, seguida de Re⟨v, adjoint(θ_s(A))(θ_s(A)v)⟩=‖θ_s(A)v‖². `adjoint_inner_right` transfere o adjunto para o primeiro argumento, preservando a convenção complexa linear no segundo. Na identidade final, `scalarGNSOrbit_ae` fornece Λ(A)(s)=√c·θ_s(A)η; após restringir essa igualdade a.e. ao intervalo, `Real.sq_sqrt dualHaarFactor_pos.le` devolve **c=(2π)⁻¹**, exatamente o fator usado em ψ. Nenhuma escala adicional ou normalização por comprimento entra.

As coerções `A.val.val` recuperam o mesmo operador de A∈`finiteDualLeftIdeal P`; não trocam o ideal por seu domínio escalar máximo. R=0 é permitido. Para R<0, T_R continua definido e contrativo, mas a identidade final de norma não é reivindicada: Ioc(-R,R) e a integral orientada não podem ser identificados nessa orientação. A fórmula intermediária com integral orientada vale para todo R, como a rota declara.

## Recompilação e proveniência

Árvore própria: {link(RUN)}. Foram selecionadas e copiadas **{len(M['dependencies'])} dependências de projeto** necessárias, com hashes de fontes e `.olean` conferidos antes/depois. Os catálogos vieram das árvores próprias já revisadas {link(Path(M['previous_run']))} e {link(Path(M['secondary_catalog']))}; a segunda fornece as dependências GNS não necessárias ao pacote anterior de funcionais. Não se recompilaram essas dependências.

`LEAN_PATH` contém um único build de projeto, o desta revisão, seguido apenas de oito caminhos de pacotes externos readonly. Nenhum build de projeto autoral ou diretório de fontes autoral integra esse caminho. TMP/TEMP são próprios. Compilador: `{M['lean_version']}`, SHA256 `{M['compiler_sha256']}`. Os pacotes/compiler são herdados em leitura, sem reconstrução global.

Permanece a exceção histórica já revisada de comentário em `DualSemifiniteIdeal`: fonte própria `{ex['source_sha256']}`, binário `{ex['sha256']}` e fonte autoral atual `{ex['live_source_sha256']}`. Ao congelar, a substituição literal do comentário foi novamente conferida; não há diferença de provas nessa exceção. As limitações binárias herdadas permanecem as dos pareceres anteriores; não se reivindica reprodução autoral de toda a cadeia. A identidade binária nova é a dos dois módulos abaixo.

| Módulo DEV | Alvos | SHA256 fonte final lida | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
{source_table}

| Processo próprio | rc | Segundos |
|---|---|---|
{time_table}

Os três processos ficaram sem warnings e com stderr vazio. Auditor: fonte `{V['own_auditor_source_sha256']}`; `.olean` `{V['own_auditor_binary_sha256']}`; stdout `{V['own_auditor_stdout_sha256']}`. Não foram acrescentados axiomas, hipóteses ou provas substitutas ao auditor. Nove nomes exatos e seus conjuntos de axiomas coincidem com o status e com os módulos recompilados.

| Log autoral final inspecionado | SHA256 JSON |
|---|---|
{logs_table}

Os dois logs autorais registram rc0 e fonte inalterada. Fontes, binários e streams vivos foram comparados aos pins e às cópias congeladas; stdout/stderr próprios também têm hashes registrados. Evidência: {link(RUN / 'manifest.json')}, {link(RUN / 'compilation.json')}, {link(RUN / 'verification_dev.json')} e {link(RUN / 'logs/GNSCutMapsAudit.stdout.txt')}. O rc0 próprio é execução desta revisão; os logs autorais são evidência inspecionada. Nenhum teste autoral foi executado.

## Documentação e limites finais

`ROTA_MAPAS_GNS_DE_CORTE_RASCUNHO.md` foi lida inteira, SHA256 **`{V['route_sha256']}`**, igual ao pin do status e ao snapshot. Seus alcances são corretos: contradomínio ambiente, entrelaçamento com a mesma ρ, norma ligada ao funcional já construído, R≥0 na identificação com o integral restrito, interseção enumerável e injetividade conjunta. O texto distingue esses mapas de um novo GNS cíclico, de vetor separante e de uma prova de fechabilidade. Não se encontrou P2 documental.

Status `gns_cut_maps_draft_status.json`: SHA256 `{V['status_sha256']}`. A custódia anterior `bounded_scalar_cuts_custody.json`, `{V['custody_sha256']}`, foi comparada ao pin do status e ao parecer selado `{V['previous_bounded_scalar_cuts_review_sha256']}`. O arquivo autoral de verificação da custódia, SHA256 `{hashlib.sha256(old_verification_raw).hexdigest()}`, foi somente lido e congelado: declara `custody_ok=true` e 26 prefixos/backups; não se reexecutou o verifier nem se revalidaram seus 26 pares neste escopo.

As contagens **101/71/6348** e a cópia `{M['initial_um_sha256']}` pertencem à integração anterior, conforme a custódia lida. O hash da cópia permaneceu igual ao concluir. Não houve inspeção integrada nova ou soma destes dois DEV às contagens anteriores. Os {len(M['previous_reviews'])} pareceres precedentes mantiveram seus pins. Não foram alterados fontes, originais, memórias ou custódias; saídas exclusivamente em `revisao/`.

**Conclusão:** dois módulos/nove alvos revisados e recompilados independentemente, sem P0–P2. Foram conferidos mensurabilidade, comutação com o campo previsto no tipo, contração, entrelaçamento para o L² ambiente, injetividade conjunta enumerável e identidade de norma com o fator Haar correto. Não se certificam preservação de H_I por T_R, espaço GNS novo/cíclico, vetor separante, fidelidade individual dos cortes, domínio escalar máximo, fechabilidade/Tomita fechado, KMS, traço, gate ou runtime. Não houve inspeção de provas posteriores nem execução/importação de monólito, recorders ou verifiers autorais.
'''
path = REVIEW / 'REVIEW_GNS_CUT_MAPS.md'
write_new(path, report.encode('utf-8'))
result = {
    'timestamp': now.isoformat(timespec='seconds'), 'status': 'DEV_COMPLETE_NO_P0_P1_P2',
    'review_path': str(path), 'review_sha256': sha(path), 'review_bytes': path.stat().st_size,
    'new_sources': 2, 'new_targets': 9, 'own_compiler_processes_rc0': 3,
    'own_bins_equal_author': True, 'project_dependencies': len(M['dependencies']),
    'previous_reviews_preserved': all(sha(Path(p)) == h for p, h in M['previous_reviews'].items()),
    'integrated_inspection_performed': False, 'author_programs_executed': False,
    'working_sha256_at_close': sha(ROOT / 'um.py'), 'findings': []
}
write_new(RUN / 'closure_dev.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
