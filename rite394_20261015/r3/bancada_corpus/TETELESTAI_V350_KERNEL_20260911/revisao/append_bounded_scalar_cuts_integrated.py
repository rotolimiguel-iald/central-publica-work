"""Append static integrated evidence with an immediate exact-byte DEV backup."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / 'bounded_scalar_cuts_latest_run.txt').read_text(encoding='utf-8'))
CAP = max(RUN.glob('final_integrated_*'))
read = lambda p: json.loads(p.read_bytes())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
M, C = read(RUN / 'manifest.json'), read(RUN / 'closure_dev.json')
V, S = read(CAP / 'verification.json'), read(CAP / 'supplemental_verification.json')
K, G = read(CAP / 'gns_normality_custody.json'), read(CAP / 'gate_tests.json')
for key in ['exact_expected_file_set', 'all_exit_zero', 'all_hashes_match',
            'gate_checks_all_passed', 'um_matches_gate_report', 'um_matches_integration_report',
            'python_ast_outside_embedded_unchanged', 'gate_extension_byte_identical_to_98',
            'previous_reviews_preserved', 'evidence_axioms_equal_log']:
    assert V[key], key
for key in ['original_local_base_equal_integration_pin', 'previous_custody_matches_AST_baseline',
            'new_targets_exact', 'new_target_axioms_match_own_auditor', 'five_new_compiles_source_unchanged',
            'all_previous_literal_control_calls_identical_AST',
            'entire_test_AST_unchanged_after_only_added_controls_removed',
            'runtime_inventory_pinned_to_history', 'all_final_artifacts_live_hashes_unchanged',
            'working_um_unchanged', 'three_DEV_sources_unchanged',
            'previous_reviews_preserved', 'sealed_GNS_normality_review_matches_custody']:
    assert S[key], key
assert (V['integrated_modules'], S['reused_source_and_binary_count'], V['gate_checks_count'],
        V['audit_distinct'], V['embedded_files'], len(M['declarations'])) == (101, 96, 71, 6348, 803, 11)
assert all(all(row[key] for key in ['dev_still_frozen', 'same_except_import_paths', 'embedded_matches'])
           for row in V['source_matches'].values())
assert all(all(row.values()) for row in S['root_imports'].values())
assert all(V['posterior_modules_absent_from_embedded'].values())
assert not V['audit_unexpected_axioms'] and all(x is False for x in V['six_flags'].values())
assert all(not x for x in S['new_stdout_warnings'].values())
assert not any(V[k] for k in ['legacy_gate_changed', 'full_plan_complete', 'full_monolithic_runtime_run'])
assert S['added_controls'] == ['bounded_scalar_cuts_do_not_discharge_closed_Tomita_KMS_trace']
assert not S['removed_controls'] and not V['removed_embedded_files']
assert set(V['added_embedded_files']) == {'TGLExt/V350' + n + '.lean' for n in V['source_matches']}
assert set(V['changed_old_embedded_files']) == {'TGLExt.lean', 'TGL/Audit.lean'}
assert 'legacy_gate_changed' not in G and G['frontier']['legacy_gate_changed'] is False
assert G['passed'] == len(G['checks']) == 71
for n, h in V['artifact_sha256'].items():
    assert sha(ROOT / n) == h, n
assert sha(ROOT / 'um.py') == V['um_sha256']
for p, h in M['previous_reviews'].items():
    assert sha(Path(p)) == h, p
for r in M['sources'].values():
    assert sha(Path(r['path'])) == r['sha256']
for n in ['record_bounded_scalar_cuts_progress.py', 'verify_bounded_scalar_cuts_custody.py']:
    ast.parse((CAP / n).read_bytes())

def link(path, label=None):
    return '[' + (label or path.name) + '](<' + path.as_posix() + '>)'

now = datetime.datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
path = REVIEW / 'REVIEW_BOUNDED_SCALAR_CUTS.md'
old = path.read_bytes()
old_hash = sha(path)
assert old_hash == C['review_sha256'] and len(old) == C['review_bytes']
backup = path.with_name(path.name + '.bak_' + stamp)
records = {r['file']: r for r in V['records']}
sources_table = '\n'.join('| ' + name + ' | `' + row['integrated_sha256'] + '` | `' +
    records['TGLExt/V350' + name + '.lean']['binary_sha256'] + '` |'
    for name, row in V['source_matches'].items())
artifact_names = ['integration.json', 'integrated_compile.json', 'gate_tests.json',
                  'kernel_incremental_evidence.json', 'MINUTA_FUNCIONAIS_LIMITADOS.md',
                  'record_bounded_scalar_cuts_progress.py', 'verify_bounded_scalar_cuts_custody.py']
artifacts_table = '\n'.join('| ' + n + ' | `' + V['artifact_sha256'][n] + '` |' for n in artifact_names)
text = f'''

## Adendo integrado — {now.isoformat(timespec='seconds')}

**Conferência integrada concluída, sem achados P0–P2.** Escopo: os mesmos três módulos/11 alvos do parecer DEV. Este adendo é inspeção independente de hashes, fontes, imports, AST, logs e documentação. Não foram repetidas recompilações próprias ou execuções autorais.

[REAL — medido por leitura de bytes] A cópia `um.py` tem SHA256 **`{V['um_sha256']}`**, coincidente com os pins de `integration.json` e `gate_tests.json`, e **803** arquivos embutidos. O original canônico e a base local foram relidos apenas para hash: ambos `{S['original_sha256']}`, igual ao pin de base. Nenhum monólito foi executado/importado.

| Evidência | Resultado e alcance |
|---|---|
| Recompilação própria, estrato DEV preservado | Três módulos + auditor rc0; 11 tipos/11 alvos, somente trio; três binários DEV próprios iguais aos autorais. Continuam válidas a proveniência das 374 dependências próprias e as limitações de herança já explicitadas acima. |
| Build integrado autoral, inspecionado | **101 registros rc0**, todos com fonte e `.olean` relidos e hashes conferidos. **96** conservam fonte/binário da custódia GNS anterior; **cinco** compilações são novas: três módulos + duas raízes. Não são 101 recompilações. |
| Audit integrado autoral, inspecionado | **6348 declarações distintas**, somente `propext`, `Classical.choice`, `Quot.sound`. Mapa extraído do stdout igual ao de `kernel_incremental_evidence.json`; os 11 alvos coincidem em nomes e axiomas com o auditor próprio. |
| Controles autorais, inspecionados | **71/71** registrados como passados, vinculados à cópia acima. O revisor não reexecutou esses testes. |
| Gate/runtime | Seis flags maiores `false`; `frontier.legacy_gate_changed=false`, `frontier.full_plan_complete=false` e `full_monolithic_runtime_run=false`. Não há quitação de gate ou liberação de runtime. |

**Imports, fontes e raízes.** Cada `TGLExt/V350*.lean` coincide exatamente com seu DEV congelado após a única troca de prefixo de imports `TGLV350.`→`TGLExt.V350`; não se precisou normalizar finais de linha ou outro texto. Os respectivos textos embutidos são idênticos em bytes. Os corpos, tipos, hipóteses e quantificação dos 11 alvos foram preservados; não se realizou outro `#check` independente das raízes integradas. `TGLExt.lean` e `TGL/Audit.lean` importam explicitamente os três módulos. Contra o dicionário custodiado anterior, há três entradas novas, nenhuma removida e apenas as duas raízes alteradas entre as preexistentes.

| Módulo integrado | SHA256 fonte | SHA256 `.olean` autoral lido |
|---|---|---|
{sources_table}

As cinco novas compilações registram fonte inalterada durante a execução e não contêm warnings. Timestamps e hashes dos dez streams stdout/stderr, comparados aos congelados, estão em {link(CAP / 'supplemental_verification.json')}. Fontes e streams dos 101 registros foram congelados no mesmo snapshot; seus binários foram relidos para hash. Esta inspeção não equivale a reconstrução independente da biblioteca/árvore integrada inteira.

**AST e controle de fronteira.** O baseline `{V['previous_um_sha256']}` foi localizado em backup e validado contra `gns_normality_custody.json`, SHA256 `{V['artifact_sha256']['gns_normality_custody.json']}`. Retirada somente a atribuição `_EMBEDDED_KERNEL_FILES`, toda a AST Python coincide com a anterior. `gate_extension.py` permanece idêntico em bytes, SHA256 `{V['artifact_sha256']['gate_extension.py']}`. O parecer selado de normalidade continua com hash `{K['review_sha256']}`.

O único controle acrescentado está em `test_gate_extension.py:368–378`: `bounded_scalar_cuts_do_not_discharge_closed_Tomita_KMS_trace`. Confere presença de cinco declarações sobre mapa limitado, positividade, dominância, supremo e convergência ao supremo interno, junto às seis flags falsas. O exame de axiomas cobre os 11 alvos, além dos cinco citados no controle. Removida somente essa chamada, a AST inteira dos testes é igual à anterior; nenhuma chamada antiga foi alterada ou removida. São 38 chamadas literais contra 37 anteriores, número sintático distinto dos 71 controles registrados.

**Nota sobre a impressão resumida dos testes.** A estrutura de `gate_tests.json` foi conferida diretamente: `legacy_gate_changed` não existe no topo; o valor está em `frontier.legacy_gate_changed`. `legacy_gate` também existe como campo próprio. O arquivo registra 71 resultados `passed=true`. A falha do resumo posterior comunicada pelo autor é compatível com a consulta de uma chave inexistente; não foi reproduzida nem usada como evidência de falha dos testes. O rc0 da chamada autoral e a ocorrência dessa falha posterior são informações do autor; nesta inspeção foram efetivamente conferidos o schema, os resultados gravados, a vinculação ao snapshot e a AST. Nenhum teste foi reexecutado.

**Minuta e scripts.** `MINUTA_FUNCIONAIS_LIMITADOS.md` foi lida integralmente. As linhas 5–23 mantêm corretamente a linearidade complexa, c=(2π)⁻¹, positividade para R≥0 com realidade e sinal, dominância sobre N+, exaustão natural potencialmente infinita e convergência real ao supremo interno com limite forte construído. A notação Re ψ≤ν e ν=sup Re ψ é acompanhada pela inclusão das avaliações finitas em ENNReal (linha 12), correspondente a `ENNReal.ofReal` nas fontes. Não se reivindicam fidelidade dos cortes, ψ_n(1)=1, interface predual ou fechabilidade. A frase sobre continuidade dos cortes está no contexto explícito do critério de convergência monótona; não substitui SOT por convergência em norma de operador.

O recorder e o verifier foram lidos integralmente e analisados por AST, sem execução. O texto principal e os campos de custódia preservam o estatuto de critério de convergência monótona, mantendo predual, Tomita e traço abertos. O mecanismo previsto usa backup de bytes e temporário; o verifier prevê conferir hashes e prefixos. Trata-se de inspeção estática, não certificação de uma execução/custódia futura. Os placeholders da minuta não foram usados como evidência. Nenhuma das escritas previstas nesses scripts foi realizada pelo revisor.

`ScalarGNSCutMaps` e `ScalarGNSCutNorm` estão ausentes das entradas e das referências embutidas. A nota posterior do recorder os marca como dois DEV/nove alvos sem revisão nem integração neste pacote. Verificou-se apenas essa separação de estatutos; não foram examinados seus teoremas, fontes, logs ou binários, nem a rota de provas posterior. O inventário I/O mantém o pin histórico `{S['runtime_inventory_sha256']}` e a fonte histórica `{S['runtime_inventory_historical_source_sha256']}`, conforme os campos da custódia anterior; isso não constitui inventário executado ou liberação da cópia atual.

| Artefato integrado/documental lido e congelado | SHA256 |
|---|---|
{artifacts_table}

Evidências detalhadas: {link(CAP / 'verification.json')} e {link(CAP / 'supplemental_verification.json')}. Artefatos pinados, três DEV e cópia foram reconferidos antes deste append. Todos os {len(M['previous_reviews'])} pareceres anteriores mantêm os hashes do manifesto.

**Conclusão delimitada:** a integração conserva integralmente o resultado dos três DEV/11 alvos, sem defeito concreto de prova, integração ou documentação identificado. Permanecem os limites do parecer DEV: funcionais positivos limitados e critério de convergência monótona; nenhuma conclusão nova sobre predual, fidelidade individual, estados normalizados, mapas GNS posteriores, fechabilidade, KMS, traço, gate ou runtime. O registro anterior de “sem integração” descreve o estrato DEV; este adendo acrescenta apenas a inspeção integrada delimitada.

Preservação: os **{len(old)} bytes** anteriores, SHA256 `{old_hash}`, foram guardados imediatamente em {link(backup)}. O novo parecer conserva esse prefixo byte a byte. Nenhuma fonte, original, memória, custódia ou parecer anterior foi alterado; escritas exclusivamente em `revisao/`.
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
