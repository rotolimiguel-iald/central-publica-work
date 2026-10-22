"""Append final integration inspection, preserving the independent source review."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "fixed_core_base_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
FIRST = Path(M["previous_run"])
FM = json.loads((FIRST / "manifest.json").read_bytes())
CAP = max(p for p in RUN.glob("final_integrated_*") if (p / "supplemental_verification.json").exists())
V = json.loads((CAP / "verification.json").read_bytes())
S = json.loads((CAP / "supplemental_verification.json").read_bytes())
R = json.loads((RUN / "source_review_receipt.json").read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
assert (V["integrated_modules"], V["gate_checks_count"], V["audit_distinct"], V["embedded_files"]) == (75, 65, 6241, 777)
assert all(V[k] for k in ("exact_expected_file_set", "all_exit_zero", "all_hashes_match", "gate_checks_all_passed",
                         "um_matches_gate_report", "um_matches_integration_report", "python_ast_outside_embedded_unchanged",
                         "gate_extension_byte_identical_to_70", "previous_reviews_preserved", "evidence_axioms_equal_log",
                         "recorder_ast_parse_ok"))
assert not V["audit_unexpected_axioms"] and all(x is False for x in V["six_flags"].values())
assert V["full_monolithic_runtime_run"] is False and V["legacy_gate_changed"] is False and V["full_plan_complete"] is False
assert all(S[k] for k in ("integration_build_ok", "own23_axioms_equal_integrated", "all75_embedded_sources_equal_disk",
                         "seven_new_records_sources_unchanged", "all5_imported_by_root", "all23_printed_in_Audit",
                         "later_modules_not_embedded", "common_control_conditions_unchanged", "original_matches_base_and_integration",
                         "prior_custodied_review_hash_matches", "historical_io_inventory_matches_custody", "not_runtime_clearance"))
assert len(S["previous_control_rename_identical_conditions"]) == 1
assert all(S["documents_same_as_source_review"].values())
assert len(V["reused_same_binary_and_source_as_70"]) == 68 and len(V["new_compilations_relative_to_70"]) == 7
assert C["records"][-1]["axioms"] == V["new_targets_axioms"]
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
for row in {**FM["sources"], **M["sources"]}.values():
    assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
for row in V["source_matches"].values():
    assert row["same_after_import_rewrite_and_EOL_normalization"] and row["embedded_matches"] and row["dev_still_frozen"]
for name in ["MINUTA_BASE_FIXA.md", "record_fixed_base_progress.py"]:
    assert (ROOT / name).read_bytes() == (CAP / name).read_bytes()
for path, digest in M["previous_reviews"].items():
    assert sha(Path(path).read_bytes()) == digest
report = REVIEW / "REVIEW_FIXED_CORE_BASE.md"
old = report.read_bytes()
assert sha(old) == R["report_sha256"]
stamp = datetime.datetime.now().astimezone()
table = "\n".join(f'| `V350{name}.lean` | `{q["integrated_sha256"]}` |' for name, q in V["source_matches"].items())
artifacts = "\n".join(f'- `{name}`: `{V["artifact_sha256"][name]}`.' for name in
                      ["integration.json", "integrated_compile.json", "gate_tests.json", "kernel_incremental_evidence.json"])
text = f'''

---

## Adendo final — integração e encerramento da revisão

{stamp.isoformat(timespec="seconds")}. **[REAL — inspeção independente de fontes, hashes, AST e logs do autor] Escopo concluído: cinco módulos / 23 alvos, sem achados P0, P1 ou P2 matemáticos ou documentais.** O exame integrado complementa o estrato de recompilação própria, preservado integralmente acima.

Snapshot final lido: **`{V['um_sha256']}`**, com **777 arquivos embutidos**. `um.py` foi somente lido e analisado com AST/literal_eval; não foi executado nem importado.

| Evidência | Alcance efetivamente conferido |
|---|---|
| Recompilação independente | Cinco fontes e dois auditores próprios, sete processos rc0; 23 alvos somente no trio; 26 tipos nomeados examinados. Os cinco `.olean` dev próprios coincidem com os do autor. |
| Build integrado do autor | 75 registros rc0, com hashes atuais das 75 fontes e dos 75 `.olean` concordantes; 68 reutilizados por identidade de fonte/binário com o estrato anterior, mais cinco módulos e duas raízes recompilados. Não refiz o rebuild das raízes ou da biblioteca. |
| Controles do autor | 65/65 no relatório, todos aprovados. Foram lidos e inspecionados; não reexecutei os controles Python. |
| Audit integrado | 6.241 declarações distintas extraídas do stdout, axiomas no trio; mapa idêntico ao evidence JSON. Os 23 novos alvos coincidem com o mapa do auditor próprio. |
| Fontes embutidas/imports | As 75 fontes dos registros correspondem aos bytes embutidos. As cinco novas aparecem nos imports das raízes e os 23 alvos no Audit. |

### Reescrita das fontes e hashes

As cinco fontes finais permanecem iguais aos snapshots dev. A passagem para `TGLExt/V350*.lean` preserva o conteúdo Lean, com troca de imports `TGLV350.`→`TGLExt.V350`. **Há também normalização de finais de linha em TwistedCommutantField**: a fonte dev contém 95 CRLF e o integrado contém zero; por isso a comparação byte a byte com apenas a troca de imports é falsa nesse arquivo. Após explicitar essa normalização, a igualdade é exata. Nos outros quatro arquivos basta a troca dos imports. Não atribuo a diferença de CRLF a mudança de prova e não declaro uma identidade de bytes inexistente.

| Fonte integrada | SHA-256 lido |
|---|---|
{table}

O dicionário embutido mudou exatamente pelos cinco arquivos novos e pelas duas raízes `TGLExt.lean`/`TGL/Audit.lean`, sem remoções. A comparação com o backup da cópia anterior, SHA `{V['previous_um_sha256']}`, mostra **AST Python fora do dicionário idêntico**. `gate_extension.py` também permaneceu byte a byte igual, SHA `{V['artifact_sha256']['gate_extension.py']}`.

No `test_gate_extension.py`, comparei o AST das condições: a renomeação de `constant_fibre_identification_does_not_discharge_base_membership_trace_or_physics` para `constant_fibre_identification_preserves_six_remaining_frontier_flags` conserva exatamente a condição anterior. Todas as demais condições comuns estão intactas. O controle novo `fixed_base_identification_preserves_trace_corner_and_physical_obligations` exige a presença dos lemas centrais e as mesmas seis flags falsas; a inspeção corresponde às linhas 294–305 da versão congelada. Nenhuma mudança de gate foi deduzida do nome de um teorema.

`gate_tests.json.frontier` registra `legacy_gate_changed=false` e `full_plan_complete=false`; as seis flags maiores estão falsas no evidence e o relatório registra `full_monolithic_runtime_run=false`. São dados dos artefatos inspecionados, não uma execução independente do runtime.

Original canônico e cópia-base lidos novamente: **`{S['original_sha256']}`**, iguais entre si e ao hash-base de `integration.json`. O parecer anterior custodiado permanece no hash da custódia. Não houve escrita nesses arquivos, nas fontes do autor ou em memórias.

Evidência reproduzível da inspeção: [verification.json](<{(CAP/'verification.json').as_posix()}>) e [supplemental_verification.json](<{(CAP/'supplemental_verification.json').as_posix()}>). Hashes dos relatórios lidos:

{artifacts}

### Documento final e alcance do parecer

A minuta e o recorder da captura final são byte a byte os mesmos já lidos integralmente no exame de fontes:

- `MINUTA_BASE_FIXA.md`: **`{V['artifact_sha256']['MINUTA_BASE_FIXA.md']}`**.
- `record_fixed_base_progress.py`: **`{V['artifact_sha256']['record_fixed_base_progress.py']}`**.

A minuta descreve corretamente a identificação **F=imagem amplificada de M**, a unicidade de C∈M e a continuidade necessária para refletir a igualdade ae antes da avaliação em zero. Os estatutos matemáticos e os limites são adequados. O recorder e sua futura custódia **não foram executados** pelo revisor. O inventário I/O permanece histórico, com hash `{S['historical_io_inventory_sha256']}`, referente à cópia `{S['historical_io_inventory_source_sha256']}` e conferido contra a custódia anterior; não libera o runtime atual.

**Resultado reconhecido neste pacote:** B∈F ↔ ∃ C∈M, B=fibre(C), com C único e igual a e*Be, na mesma torre, medida de Lebesgue, representação regular e fluxo. A conclusão é expressa por pertença e preimagem única; não é a construção adicional de uma equivalência empacotada ou de valores de peso transportados à base. `FixedBaseEquivalence` e `BoundedBaseDualValues` estão ausentes do dicionário inspecionado e seus teoremas não foram lidos, recompilados ou incluídos.

**[OPEN]** Permanecem a correspondência geral espectral/predual, a interface padrão de peso operatorial e sua semifinitude, as construções de estado/gerador/perturbação e traço canônico, Three Locks/H1–H3 físicos e demais obrigações físicas, contrato ampliado e runtime integral. Não são bugs das cinco provas delimitadas e não são quitadas pela identificação F=base. Nenhuma aprovação de QG, gate, traço ou runtime é emitida.

**Parecer final encerrado, sem análise específica pendente no escopo recebido.** As cinco fontes foram recompiladas independentemente; a integração/raízes e os controles foram conferidos por inspeção dos registros do autor. O presente adendo foi acrescentado com backup imediato byte a byte e preservação do prefixo anterior. Todos os pareceres custodiados anteriores permanecem intocados; toda escrita do revisor ficou em `revisao/`.
'''
backup = report.with_name(report.name + ".bak_" + stamp.strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as f:
    f.write(old)
assert backup.read_bytes() == old
raw = old + text.encode("utf-8")
tmp = report.with_name(report.name + ".tmp_" + stamp.strftime("%Y%m%d_%H%M%S_%f"))
with tmp.open("xb") as f:
    f.write(raw)
assert tmp.read_bytes() == raw and raw.startswith(old) and len(raw) > len(old)
tmp.replace(report)
assert report.read_bytes() == raw and backup.read_bytes() == old
receipt = {"timestamp": stamp.isoformat(), "report": str(report), "report_sha256": sha(raw),
           "report_bytes": len(raw), "immediate_backup": str(backup), "backup_sha256": sha(old),
           "old_prefix_preserved": True, "review_complete": True, "P0": [], "P1": [], "P2": [],
           "independent_module_compiles": 5, "independent_auditor_compiles": 2, "all_exit_zero": True,
           "targets": 23, "named_types": 26, "all5_binaries_equal_author": True,
           "integrated_records_inspected": 75, "author_controls_read_not_rerun": 65, "integrated_Audit_distinct": 6241,
           "embedded_files": 777, "working_sha256": V["um_sha256"], "template_sha256": V["artifact_sha256"]["MINUTA_BASE_FIXA.md"],
           "sources_and_prior_custodied_reviews_preserved": True, "recorder_monolith_tests_executed": False,
           "F_equals_amplified_base_proved_in_this_representation": True, "trace_gate_runtime_approved": False}
with (RUN / "final_report_receipt.json").open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
print(json.dumps(receipt, ensure_ascii=False, indent=2))
