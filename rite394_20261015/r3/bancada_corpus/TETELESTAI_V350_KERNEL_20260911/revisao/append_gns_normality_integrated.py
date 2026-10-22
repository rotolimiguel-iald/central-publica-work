"""Append integrated inspection, preserving the exact DEV review bytes."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'gns_normality_latest_run.txt').read_text(encoding='utf-8'))
CAP = max(RUN.glob('final_integrated_*'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
V = read(CAP / 'verification.json')
S = read(CAP / 'supplemental_verification.json')
M = read(RUN / 'manifest.json')
C = read(RUN / 'closure_dev.json')
P = read(CAP / 'tomita_domain_custody.json')

for key in ['exact_expected_file_set', 'all_exit_zero', 'all_hashes_match',
            'gate_checks_all_passed', 'um_matches_gate_report', 'um_matches_integration_report',
            'python_ast_outside_embedded_unchanged', 'gate_extension_byte_identical_to_96',
            'previous_reviews_preserved', 'evidence_axioms_equal_log']:
    assert V[key], key
for key in ['original_local_base_equal_integration_pin', 'previous_custody_matches_AST_baseline',
            'new_targets_exact', 'new_target_axioms_match_own_auditor',
            'four_new_compiles_source_unchanged',
            'all_previous_literal_control_calls_identical_AST',
            'entire_test_AST_unchanged_after_only_added_controls_removed',
            'runtime_inventory_pinned_to_history', 'all_final_artifacts_live_hashes_unchanged',
            'working_um_unchanged', 'two_DEV_sources_unchanged',
            'previous_reviews_preserved', 'sealed_Tomita_review_matches_custody']:
    assert S[key], key
assert V['integrated_modules'] == 98 and S['reused_source_and_binary_count'] == 94
assert V['gate_checks_count'] == 70 and V['audit_distinct'] == 6337
assert V['embedded_files'] == 800 and len(M['declarations']) == 7
assert all(all(r[k] for k in ['dev_still_frozen', 'same_except_import_paths', 'embedded_matches'])
           for r in V['source_matches'].values())
assert all(all(x.values()) for x in S['root_imports'].values())
assert all(V['posterior_modules_absent_from_embedded'].values())
assert not V['audit_unexpected_axioms']
assert all(x is False for x in V['six_flags'].values())
assert all(not x for x in S['new_stdout_warnings'].values())
assert not any(V[k] for k in ['legacy_gate_changed', 'full_plan_complete', 'full_monolithic_runtime_run'])
assert S['added_controls'] == ['GNS_order_normality_does_not_discharge_closed_Tomita_KMS_trace']
assert S['removed_controls'] == []
assert V['removed_embedded_files'] == []
assert set(V['added_embedded_files']) == {'TGLExt/V350' + n + '.lean' for n in V['source_matches']}
assert set(V['changed_old_embedded_files']) == {'TGLExt.lean', 'TGL/Audit.lean'}
for name, h in V['artifact_sha256'].items():
    assert sha(ROOT / name) == h, name
assert sha(ROOT / 'um.py') == V['um_sha256']
for path, h in M['previous_reviews'].items():
    assert sha(Path(path)) == h, path
for row in M['sources'].values():
    assert sha(Path(row['path'])) == row['sha256']
for name in ['record_gns_normality_progress.py', 'verify_gns_normality_custody.py']:
    ast.parse((CAP / name).read_bytes())

def link(path, label=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + '>)'

def save_new(path, raw):
    assert path.resolve().is_relative_to(REVIEW) and not path.exists()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw and tmp.stat().st_size == len(raw) > 0
    tmp.replace(path)
    assert path.read_bytes() == raw

now = datetime.datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
path = REVIEW / 'REVIEW_GNS_NORMALITY.md'
old = path.read_bytes()
old_hash = sha(path)
assert old_hash == C['review_sha256'] and len(old) == C['review_bytes']
backup = path.with_name(path.name + '.bak_' + stamp)
records = {r['file']: r for r in V['records']}
source_table = '\n'.join(
    '| ' + name + ' | `' + row['integrated_sha256'] + '` | `' +
    records['TGLExt/V350' + name + '.lean']['binary_sha256'] + '` |'
    for name, row in V['source_matches'].items())
artifact_names = ['integration.json', 'integrated_compile.json', 'gate_tests.json',
                  'kernel_incremental_evidence.json', 'MINUTA_NORMALIDADE_GNS.md',
                  'record_gns_normality_progress.py', 'verify_gns_normality_custody.py']
artifact_table = '\n'.join('| ' + n + ' | `' + V['artifact_sha256'][n] + '` |' for n in artifact_names)
text = f'''

## Adendo integrado — {now.isoformat(timespec='seconds')}

**Conferência integrada concluída, sem achados P0–P2.** Escopo exclusivo: `ScalarGNSStrongContinuity` e `ScalarGNSNormality`, sete alvos. Mantém-se integralmente o parecer DEV acima. Este adendo acrescenta inspeção independente de fontes, hashes, imports, AST, logs e documentação; não acrescenta recompilações próprias nem execução de testes autorais.

[REAL — hashes e comparação estática medidos aqui] A cópia `um.py` tem SHA256 **`{V['um_sha256']}`**, coincidente com `integration.json` e `gate_tests.json`, e contém **{V['embedded_files']}** arquivos. A base local e o original canônico, relidos apenas para hash, têm ambos `{S['original_sha256']}`, igual ao pin de base. Nenhum monólito foi executado/importado.

| Evidência | Resultado e limite |
|---|---|
| Recompilação própria DEV, estrato anterior | Dois módulos + auditor rc0; sete `#check` e sete `#print axioms`; somente trio. Os dois binários DEV próprios coincidiram com os autorais. Dependências próprias congeladas e limitações de herança permanecem as do primeiro estrato. |
| Build integrado autoral, inspecionado | **98 registros rc0**, todos com fonte e `.olean` relidos e seus hashes conferidos. **94** preservam fonte/binário da custódia Tomita; **quatro** compilações novas: dois módulos + `TGLExt.lean` + `TGL/Audit.lean`. Não são 98 recompilações. |
| Auditor integrado autoral, inspecionado | **6337 declarações distintas**, somente `propext`, `Classical.choice`, `Quot.sound`. Mapa extraído do stdout igual ao de `kernel_incremental_evidence.json`; os sete alvos coincidem em nomes e conjuntos de axiomas com o auditor próprio. |
| Controles autorais, inspecionados | **70/70** registrados como passados. Foram conferidos o vínculo ao snapshot e a alteração do controle; não houve execução de testes pelo revisor. |
| Gate e runtime | Seis flags maiores `false`, `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`, conforme os registros. Nenhuma quitação de gate ou liberação de runtime. |

**Preservação dos enunciados e imports.** As duas fontes `TGLExt/V350*.lean` são exatamente os DEV congelados após substituir somente o prefixo de import `TGLV350.` por `TGLExt.V350`. Nem normalização adicional de finais de linha foi necessária. Cada fonte integrada coincide byte a byte com o respectivo texto embutido; ambas as raízes importam explicitamente os dois módulos. Contra a cópia Tomita anterior, há somente essas duas entradas novas, nenhuma removida e apenas as duas raízes alteradas entre entradas preexistentes. Os sete tipos e corpos revisados no DEV foram conservados; esta comparação de tipos por identidade textual não é um novo `#check` das raízes integradas.

| Módulo | SHA256 fonte integrada | SHA256 `.olean` integrado autoral lido |
|---|---|---|
{source_table}

As quatro compilações novas registram fonte inalterada durante a execução e não contêm warnings. Seus timestamps e hashes de **stdout e stderr**, com comparação aos streams congelados, estão em {link(CAP / 'supplemental_verification.json')}. Fontes e streams dos 98 registros foram congelados no mesmo diretório. Não se reivindica recompilação independente da árvore integrada inteira ou identidade binária de toda a cadeia herdada.

**AST e controle.** O baseline foi localizado em backup cujo hash é `{V['previous_um_sha256']}` e validado contra `tomita_domain_custody.json` (SHA256 `{V['artifact_sha256']['tomita_domain_custody.json']}`). Removida somente a atribuição `_EMBEDDED_KERNEL_FILES`, a AST inteira de Python é igual à anterior. `gate_extension.py` é idêntico em bytes, SHA256 `{V['artifact_sha256']['gate_extension.py']}`. O parecer Tomita permanece no hash selado `{P['review_sha256']}`.

Em `test_gate_extension.py:356–367`, o único controle novo é `GNS_order_normality_does_not_discharge_closed_Tomita_KMS_trace`: exige cinco declarações sobre transferência, positividade, monotonicidade e supremos, juntamente com as seis flags maiores falsas. O exame dos axiomas cobre os sete alvos, inclusive os dois auxiliares. Retirada somente a chamada nova, toda a AST do teste coincide com a anterior; nenhuma chamada antiga foi removida ou alterada. Há 37 chamadas literais contra 36 anteriores, contagem sintática distinta dos 70 controles registrados. Esse teste protege a fronteira declarada; não demonstra fechabilidade, KMS ou traço.

**Matemática e documentação.** A minuta foi lida integralmente. `MINUTA_NORMALIDADE_GNS.md:5–19` distingue corretamente SOT vetorial de norma de operador e normalidade em ordem de uma equivalência geral ultra-fraca/predual. O teorema de transferência recebe o limite forte a transferir; os teoremas finais de supremo **constroem** esse limite na mesma N, identificam-no com o supremo interno por unicidade e concluem supremo contra todos os majorantes em B(H_I). Conservam positividade, monotonicidade, direção e não vacuidade; não recebem normalidade ou fechabilidade como premissa. A quantificação de filtros/índices permanece a conferida no auditor DEV. Não se acrescentou uma alegação sobre famílias sem supremo interno dado.

O recorder e o verifier foram lidos integralmente e tiveram a AST analisada, sem execução. O texto principal do recorder (`158–178`) e os campos `GNS_normality_scope`/`GNS_general_predual_equivalence_proved` (`243–245`) conservam esse estatuto. O mecanismo previsto utiliza backup de bytes e substituição por temporário; o verifier prevê conferir hashes e prefixos. Isso é inspeção estática, não certificação de uma custódia ainda não executada. Os placeholders da minuta são dados de registro futuro, não evidência de execução. As escritas previstas nesses scripts não foram realizadas pelo revisor.

`DualCutLinearMap`, `ScalarBoundedCuts` e `ScalarCutNormality` foram confirmados ausentes do dicionário e das referências embutidas. A nota posterior do recorder os marca como DEV sem integração nem revisão independente e os conta separadamente. Seus teoremas, fontes, logs e binários não foram examinados ou recompilados para este adendo; a leitura da nota verifica somente essa separação de estatutos. O inventário I/O continua histórico, SHA256 `{S['runtime_inventory_sha256']}`, ligado à fonte histórica `{S['runtime_inventory_historical_source_sha256']}` conforme os campos da custódia anterior; não é inventário executado nem liberação da cópia atual.

| Artefato lido e congelado | SHA256 |
|---|---|
{artifact_table}

Evidência verificável: {link(CAP / 'verification.json')} e {link(CAP / 'supplemental_verification.json')}. Todos os artefatos pinados foram reconferidos antes deste append. Os 24 pareceres anteriores continuam iguais aos pins do manifesto; fontes autorais, originais, monólito, memórias e custódias não foram alterados.

**Conclusão delimitada:** a integração preserva a normalidade em ordem da mesma representação π_I:N→B(H_I), com o alcance dos sete alvos revisados. Fechabilidade do gráfico inicial, domínio escalar máximo, equivalência geral predual/ultra-fraca, Tomita fechado, KMS, traço e os demais fechamentos de gate/runtime não decorrem deste pacote. As observações de “sem integração” no primeiro estrato continuam retratando aquela execução DEV; este adendo acrescenta exclusivamente a inspeção integrada acima.

Preservação: backup imediato dos **{len(old)} bytes** anteriores, SHA256 `{old_hash}`, em {link(backup)}. O novo parecer conserva esse prefixo byte a byte; nenhuma escrita saiu de `revisao/`.
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
save_new(CAP / 'final_closure.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
