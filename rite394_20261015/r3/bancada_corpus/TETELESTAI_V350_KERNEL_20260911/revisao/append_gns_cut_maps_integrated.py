"""Append integrated inspection of the two GNS cut maps, preserving exact DEV bytes."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'gns_cut_maps_latest_run.txt').read_text(encoding='utf-8'))
CAP = max(RUN.glob('final_integrated_*'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M, C = read(RUN / 'manifest.json'), read(RUN / 'closure_dev.json')
V, S = read(CAP / 'verification.json'), read(CAP / 'supplemental_verification.json')
K = read(CAP / 'bounded_scalar_cuts_custody.json')
for key in ['exact_expected_file_set', 'all_exit_zero', 'all_hashes_match',
            'gate_checks_all_passed', 'um_matches_gate_report', 'um_matches_integration_report',
            'python_ast_outside_embedded_unchanged', 'gate_extension_byte_identical_to_101',
            'previous_reviews_preserved', 'evidence_axioms_equal_log']:
    assert V[key], key
for key in ['original_local_base_equal_integration_pin', 'previous_custody_matches_AST_baseline',
            'new_targets_exact', 'new_target_axioms_match_own_auditor', 'four_new_compiles_source_unchanged',
            'all_previous_literal_control_calls_identical_AST',
            'entire_test_AST_unchanged_after_only_added_controls_removed',
            'runtime_inventory_pinned_to_history', 'all_final_artifacts_live_hashes_unchanged',
            'working_um_unchanged', 'two_DEV_sources_unchanged',
            'previous_reviews_preserved', 'sealed_bounded_scalar_cuts_review_matches_custody']:
    assert S[key], key
assert (V['integrated_modules'], S['reused_source_and_binary_count'], V['gate_checks_count'],
        V['audit_distinct'], V['embedded_files'], len(M['declarations'])) == (103, 99, 72, 6357, 805, 9)
assert all(all(row[key] for key in ['dev_still_frozen', 'same_except_import_paths', 'embedded_matches'])
           for row in V['source_matches'].values())
assert all(all(row.values()) for row in S['root_imports'].values())
assert all(V['posterior_modules_absent_from_embedded'].values())
assert not V['audit_unexpected_axioms'] and all(x is False for x in V['six_flags'].values())
assert all(not x for x in S['new_stdout_warnings'].values())
assert not any(V[k] for k in ['legacy_gate_changed', 'full_plan_complete', 'full_monolithic_runtime_run'])
assert S['added_controls'] == ['GNS_cut_maps_do_not_discharge_closed_Tomita_KMS_trace']
assert not S['removed_controls'] and not V['removed_embedded_files']
assert set(V['added_embedded_files']) == {'TGLExt/V350' + n + '.lean' for n in V['source_matches']}
assert set(V['changed_old_embedded_files']) == {'TGLExt.lean', 'TGL/Audit.lean'}
for n, h in V['artifact_sha256'].items():
    assert sha(ROOT / n) == h, n
assert sha(ROOT / 'um.py') == V['um_sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
for r in M['sources'].values():
    assert sha(Path(r['path'])) == r['sha256']
for n in ['record_gns_cut_maps_progress.py', 'verify_gns_cut_maps_custody.py']:
    ast.parse((CAP / n).read_bytes())

def link(path, label=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + '>)'

now = datetime.datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
path = REVIEW / 'REVIEW_GNS_CUT_MAPS.md'
old = path.read_bytes()
old_hash = sha(path)
assert old_hash == C['review_sha256'] and len(old) == C['review_bytes']
backup = path.with_name(path.name + '.bak_' + stamp)
records = {r['file']: r for r in V['records']}
sources_table = '\n'.join('| ' + name + ' | `' + row['integrated_sha256'] + '` | `' +
    records['TGLExt/V350' + name + '.lean']['binary_sha256'] + '` |'
    for name, row in V['source_matches'].items())
artifact_names = ['integration.json', 'integrated_compile.json', 'gate_tests.json',
                  'kernel_incremental_evidence.json', 'MINUTA_MAPAS_GNS_DE_CORTE.md',
                  'record_gns_cut_maps_progress.py', 'verify_gns_cut_maps_custody.py',
                  'ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md', 'PESQUISA_FECHABILIDADE_PESOS_20260912.md']
artifacts_table = '\n'.join('| ' + n + ' | `' + V['artifact_sha256'][n] + '` |' for n in artifact_names)
text = f'''

## Adendo integrado — {now.isoformat(timespec='seconds')}

**Conferência concluída, sem achados P0–P2.** Escopo exclusivo: `ScalarGNSCutMaps` e `ScalarGNSCutNorm`, os mesmos nove alvos do estrato DEV. Acrescenta-se inspeção independente de fontes, hashes, imports, AST, logs e documentação; não se acrescentam recompilações próprias ou execução de testes autorais.

[REAL — hashes medidos por leitura] Snapshot da cópia: **`{V['um_sha256']}`**, coincidente com `integration.json` e `gate_tests.json`, com **805** arquivos embutidos. Original canônico e base local foram relidos somente para SHA256: ambos `{S['original_sha256']}`, iguais ao pin de base. Nenhum monólito foi importado ou executado.

| Evidência | Resultado e limite |
|---|---|
| Recompilação própria DEV, preservada acima | Dois módulos + auditor rc0; nove tipos e nove alvos, somente trio; ambos os binários próprios iguais aos autorais. Conservam-se a proveniência das 384 dependências próprias e as limitações de herança do primeiro estrato. |
| Build integrado autoral, inspecionado | **103 registros rc0**, com hashes de todas as fontes e `.olean` conferidos. **99** mantêm fonte/binário do estrato anterior; **quatro** compilações novas: dois módulos + `TGLExt.lean` + `TGL/Audit.lean`. Não são 103 recompilações. |
| Audit integrado autoral, inspecionado | **6357 declarações distintas**, somente `propext`, `Classical.choice`, `Quot.sound`. O mapa extraído do stdout é igual ao de `kernel_incremental_evidence.json`. Os nove nomes e conjuntos de axiomas coincidem com o auditor próprio. |
| Controles autorais, inspecionados | **72/72** registrados como passados e vinculados ao snapshot. Nenhum teste foi reexecutado pelo revisor. |
| Gate/runtime | Seis flags maiores `false`; `frontier.legacy_gate_changed=false`, `frontier.full_plan_complete=false` e `full_monolithic_runtime_run=false`. Nenhuma quitação de gate ou liberação de runtime. |

**Tipos preservados pela integração.** As fontes integradas são exatamente os DEV congelados após trocar apenas o prefixo de imports `TGLV350.` por `TGLExt.V350`. Não se precisou normalizar finais de linha ou outro conteúdo. Cada fonte integrada coincide byte a byte com seu texto embutido. Assim os corpos, tipos, hipóteses e coerções dos nove alvos foram preservados; não se executou outro `#check` independente das raízes nesta inspeção. Ambas as raízes importam explicitamente os dois módulos. Contra o dicionário custodiado anterior, há somente duas entradas novas, nenhuma removida e apenas as duas raízes alteradas entre as preexistentes.

| Módulo integrado | SHA256 fonte | SHA256 `.olean` autoral lido |
|---|---|---|
{sources_table}

Os quatro registros novos declaram fonte inalterada durante a compilação e seus stdout não contêm warnings. Timestamps e hashes dos oito streams stdout/stderr, comparados às cópias congeladas, constam de {link(CAP / 'supplemental_verification.json')}. Fontes e streams dos 103 registros foram preservados no snapshot; os binários foram relidos para hash. A integração foi inspecionada, sem reconstrução própria da biblioteca ou da árvore integrada inteira.

**AST e controle único.** A referência é a cópia `{V['previous_um_sha256']}`, localizada em backup e validada contra `bounded_scalar_cuts_custody.json`, SHA256 `{V['artifact_sha256']['bounded_scalar_cuts_custody.json']}`. Removida somente a atribuição `_EMBEDDED_KERNEL_FILES`, a AST inteira do Python coincide com a anterior. `gate_extension.py` é idêntico em bytes, SHA256 `{V['artifact_sha256']['gate_extension.py']}`. O parecer selado dos funcionais permanece com hash `{K['review_sha256']}`.

Em `test_gate_extension.py:379–389`, a única chamada nova é `GNS_cut_maps_do_not_discharge_closed_Tomita_KMS_trace`. Ela exige cinco declarações sobre mapa, contração, entrelaçamento, injetividade conjunta e norma exata, junto às seis flags falsas. O auditor integrado/próprio cobre os nove alvos, além dos cinco citados nesse controle. Retirada essa chamada, toda a AST dos testes coincide com a anterior: nenhuma chamada antiga foi alterada ou removida. São 39 chamadas literais contra 38 anteriores, contagem sintática distinta dos 72 controles registrados. O teste conserva a fronteira declarada; não demonstra fechabilidade, KMS ou traço.

**Minuta.** `MINUTA_MAPAS_GNS_DE_CORTE.md` foi lida integralmente. As linhas 5–20 explicitam corretamente K=L²(ℝ,TowerHilbert P), o corte na variável externa, o contradomínio ambiente, a mesma ρ de que π_I é restrição, a hipótese de campo fortemente contínuo uniformemente limitado, A∈I/R≥0 na norma e o caráter enumerável/conjunto da injetividade. A minuta não promove o alvo a H_I nem a um GNS cíclico novo, e não presume fidelidade individual. As linhas 33–43 mantêm aberta a estimativa necessária à fechabilidade e separam os desenvolvimentos posteriores.

**Precisão de domínio e notas posteriores — somente estatuto examinado.** A rota cíclica (`ROTA_GNS_CICLICO_DE_CORTE_RASCUNHO.md:3–7,40–57`) e o recorder (`182–192`) classificam `ScalarCutVacuum`, `ScalarCutCyclicSpace`, `ScalarCutVectorFunctional` e `ScalarCutGNSProperties` como quatro DEV/26 alvos posteriores, sem integração ou revisão independente neste parecer. Os quatro nomes estão ausentes das entradas e das referências embutidas. Não foram examinados seus teoremas, fontes, logs ou binários; a alegação de compilação desses DEV permanece declaração do autor, não certificação deste adendo.

A nota `PESQUISA_FECHABILIDADE_PESOS_20260912.md:23–30` distingue explicitamente o ideal I com cota uniforme da forma do domínio escalar n_ν, que exige finitude apenas na avaliação em η. **Não se presume I=n_ν nem se exige essa igualdade como obrigação automática.** A obrigação a solicitar antes de transportar resultados de outra realização é demonstrar a ponte de representação/domínio ou a propriedade adequada de núcleo que a rota de Tomita escolhida realmente utiliza. Nenhuma dessas pontes é declarada provada por este pacote. A ressalva preserva a ausência de prova de coincidência sem afirmar que a coincidência seja verdadeira ou necessária.

A referência a Strătilă está classificada na nota como consulta bibliográfica externa; a prova remetida a outro livro é explicitamente declarada não lida. Este revisor examinou apenas essa distinção de estatuto e a precisão de domínio, conforme solicitado: não verificou a referência externa neste adendo, não validou as construções cíclicas e não transportou a bibliografia para axiomas ou conclusões Lean. Ciclicidade, normalidade e injetividade conjunta continuam sem substituir o passo (0,y)∈fecho(G)⇒T_n y=0.

**Scripts e custódia futura.** Recorder/verifier foram lidos integralmente e analisados por AST, sem execução. O recorder separa os dois módulos/nove alvos integrados dos quatro DEV posteriores; o campo integrado `bounded_cuts_GNS_target` permanece `EXISTING_AMBIENT_L2` e `bounded_cuts_cyclic_GNS_constructed` permanece `false`. Os hashes das duas notas posteriores estão previstos em campos próprios, conferidos pelo verifier. O mecanismo de escrita prevê backup de bytes, append e troca por temporário. Isso é inspeção estática; não certifica uma execução/custódia ainda não realizada. Nenhuma escrita prevista nesses scripts foi executada pelo revisor.

O inventário I/O conserva o SHA256 histórico `{S['runtime_inventory_sha256']}` e a fonte histórica `{S['runtime_inventory_historical_source_sha256']}`, conforme a custódia precedente. Não se transformou em inventário de execução da cópia atual ou em liberação de runtime.

| Artefato lido e congelado | SHA256 |
|---|---|
{artifacts_table}

Evidências: {link(CAP / 'verification.json')} e {link(CAP / 'supplemental_verification.json')}. Todos os artefatos pinados, os dois DEV e a cópia foram reconferidos antes deste append. Os {len(M['previous_reviews'])} pareceres anteriores conservam os hashes do manifesto.

**Conclusão delimitada:** integração dos dois módulos/nove alvos conferida, sem divergência de prova, integração ou documentação encontrada. Permanecem os resultados DEV: contrações para o L² ambiente, entrelaçamento com a mesma representação, injetividade conjunta natural e norma exata para A∈I/R≥0. Nenhum resultado novo é atribuído a preservação de H_I, GNS cíclico/separante, igualdade I=n_ν, fechabilidade, KMS, traço, gate ou runtime. A observação anterior de “sem integração” retrata o estrato DEV; este adendo acrescenta somente a inspeção integrada delimitada.

Preservação: os **{len(old)} bytes** anteriores, SHA256 `{old_hash}`, foram guardados imediatamente em {link(backup)}. O novo parecer conserva esse prefixo byte a byte. Nenhuma fonte, original, memória, custódia ou parecer anterior foi alterado. Escritas exclusivamente em `revisao/`.
'''.encode('utf-8')
with backup.open('xb') as f:
    f.write(old)
assert backup.read_bytes() == old
raw = old + text
tmp = path.with_name(path.name + '.tmp_' + stamp)
with tmp.open('xb') as f:
    f.write(raw)
assert tmp.read_bytes() == raw and raw.startswith(old) and len(raw) > len(old)
assert path.read_bytes() == old
tmp.replace(path)
assert path.read_bytes() == raw
result = {
    'timestamp': now.isoformat(), 'status': 'INTEGRATED_COMPLETE_NO_P0_P1_P2',
    'review_path': str(path), 'review_sha256': sha(path), 'review_bytes': len(raw),
    'backup': str(backup), 'backup_sha256': sha(backup),
    'exact_DEV_prefix_preserved': raw.startswith(backup.read_bytes()),
    'working_sha256': sha(ROOT / 'um.py'), 'integrated_records': V['integrated_modules'],
    'author_controls': V['gate_checks_count'], 'audit_distinct': V['audit_distinct'],
    'own_new_compiles_in_this_addendum': 0, 'author_scripts_executed': False,
    'findings': [], 'previous_reviews_preserved': all(sha(Path(p)) == h for p, h in M['previous_reviews'].items())
}
out = CAP / 'final_closure.json'
assert not out.exists() and out.resolve().is_relative_to(REVIEW)
data = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
t = out.with_name(out.name + '.tmp')
with t.open('xb') as f:
    f.write(data)
assert t.read_bytes() == data
t.replace(out)
print(json.dumps(result, ensure_ascii=False, indent=2))
