"""Append the bounded documentary closure with an immediate byte backup."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent
RUN=Path((REVIEW/"dual_semifinite_ideal_latest_run.txt").read_text(encoding="utf-8"))
CAP=max(p for p in RUN.glob("erratum_final_*") if (p/"verification.json").exists())
V=json.loads((CAP/"verification.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
required=["um_matches_integration_and_gate","comment_only","corrected_source_still_frozen","dev_log_source_matches","dev_source_unchanged_reported","dev_binary_matches","all_records_rc0_and_hashes_match","all_retained_source_and_binary_unchanged","python_ast_outside_embedded_unchanged","gate_byte_unchanged","test_script_byte_unchanged","audit_same_as_previous","audit_equal_evidence","axioms_allowed","independent_40_axioms_same","author_all_tests_passed","gate_audit_count_matches","incremental_build_ok","previous_custodied_reviews_preserved","draft_excluded_from_reading","draft_absent_from_embedded","live_snapshot_files_still_identical"]
assert all(V[k] is True for k in required)
assert V["dev_log_rc"]==0 and len(V["dev_audited_axioms"])==11
assert all(set(a)<={"propext","Classical.choice","Quot.sound"} for a in V["dev_audited_axioms"].values())
assert V["changed_embedded"]==["TGLExt/V350DualSemifiniteIdeal.lean"] and not V["added_embedded"] and not V["removed_embedded"]
assert V["integrated_records"]==56 and V["retained_record_count"]==53 and V["audit_distinct"]==6163
assert V["author_tests_passed"]==V["author_test_count"]==61 and V["embedded_files"]==758
assert all(not v for v in V["six_flags"].values())
assert all(V[k] is False for k in ["legacy_gate_changed","full_plan_complete","full_monolithic_runtime_run"])
assert all(d["same_as_reviewed"] for d in V["documents"].values())
assert all(d["only_import_rewrite"] and d["embedded_byte_equal"] for d in V["source_matches"].values())
assert all(r["source_unchanged_during_compile"] is True for r in V["records"] if not r["same_record_timestamp_as_previous"])
ROOT=REVIEW.parent
assert sha((ROOT/"um.py").read_bytes())==V["current_snapshot_sha256"]
assert all(sha((ROOT/n).read_bytes())==h for n,h in V["snapshot_files_sha256"].items())
assert sha((ROOT/"kernel/TGLV350/DualSemifiniteIdeal.lean").read_bytes())==V["corrected_source_sha256"]
report=REVIEW/"REVIEW_REGULAR_SEMIFINITE_ROUTE.md"
old=report.read_bytes()
assert sha(old)==V["report_before_append_sha256"]
stamp=datetime.datetime.now().astimezone()
backup=report.with_name(report.name+".bak_"+stamp.strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as f: f.write(old)
assert backup.read_bytes()==old
rows=[]
for r in V["records"]:
    if not r["same_record_timestamp_as_previous"]:
        rows.append(f'| `{r["file"]}` | `{r["timestamp"]}` | `{r["binary_sha256"]}` |')
table="\n".join(rows)
dev=V["corrected_source_sha256"]
integrated=V["source_matches"]["DualSemifiniteIdeal"]["integrated_sha256"]
comment=V["new_comment"][4:-3].strip()
text=f'''

## Adendo FINAL — {stamp.isoformat(timespec="seconds")} — errata documental e encerramento do P2

**[REAL — comparação literal e inspeção de evidências] P2 RESOLVIDO.** A correção em `kernel/TGLV350/DualSemifiniteIdeal.lean:15–17` distingue corretamente a cota uniforme da forma quadrática da obrigação de realizá-la por um operador limitado pertencente à álgebra fixa. O comentário agora diz:

> {comment.replace(chr(10), ' ')}

Todos os bytes anteriores e posteriores a esse único comentário são idênticos aos da fonte congelada recompilada independentemente. Não houve mudança de definição, hipótese, tipo, prova, import ou alvo de auditoria. O diagnóstico P2 e os resultados do estrato anterior permanecem integralmente no prefixo deste parecer; este adendo encerra a pendência documental, sem apagar a constatação histórica. Não há P0–P2 pendente no escopo delimitado.

### Proveniência da errata

- Fonte dev anterior, efetivamente recompilada pelo revisor: `{V["old_comment_source_sha256"]}`.
- Fonte dev corrigida, congelada e relida: **`{dev}`**.
- Fonte integrada `TGLExt/V350DualSemifiniteIdeal.lean`: **`{integrated}`**; coincide com dev mediante somente a reescrita dos imports, e com o texto embutido byte a byte.
- `.olean` dev atual: `{V["dev_binary_sha256"]}`, confrontado com `logs/DualSemifiniteIdeal_20260912_035730_251164.json`: rc0, fonte inalterada durante a compilação e 11 alvos com axiomas somente no trio.

**Distinção de execução:** as quatro recompilações próprias e os quatro auditores próprios anteriores, com os 40 alvos do pacote, continuam sendo a evidência independente dos corpos Lean. Para esta alteração exclusiva de comentário, fiz comparação literal, inspeção dos logs do autor, leitura dos binários para hashes e análise estática da integração; **não recompilei independentemente a nova fonte com comentário corrigido e não executei novos testes**. O registro antigo de fonte inalterada refere-se àquela compilação anterior, não ao hash posterior à errata.

### Snapshot final após a correção

SHA-256 atual de `um.py`, lido de seus bytes e igual aos campos de `integration.json` e `gate_tests.json`: **`{V["current_snapshot_sha256"]}`**. O snapshot anterior `{V["previous_snapshot_sha256"]}` fica preservado como estrato histórico.

[REAL — inspeção de execuções do autor] `integrated_compile.json` contém **56 registros rc0**, todos confrontados com os hashes atuais de fonte e `.olean`: **53 registros conservados**, com os mesmos hashes e timestamps anteriores, e os três registros recompilados abaixo. Os três registram fonte inalterada durante a compilação.

| Registro recompilado pelo autor | Timestamp do log | SHA-256 `.olean` lido |
|---|---|---|
{table}

Permanecem **758 arquivos embutidos**: nenhum acréscimo ou remoção; a única alteração textual em relação ao snapshot anterior está no comentário de `V350DualSemifiniteIdeal.lean`. As fontes dos agregadores permanecem iguais. Os outros três módulos dev permanecem byte a byte iguais aos respectivos snapshots revisados. A AST Python externa ao dicionário embutido, `gate_extension.py` e o script de testes permanecem iguais ao estrato anterior.

O stdout atual de Audit contém **6163 declarações distintas**, com o mesmo mapa de axiomas anterior, igual ao de `kernel_incremental_evidence.json`, sem axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. Os 40 alvos da auditoria própria continuam com os mesmos axiomas. O `gate_tests.json` atual registra **61/61 controles aprovados** e referencia o SHA atual acima. Essas compilações e esses controles foram executados pelo autor; o revisor conferiu seus registros. O frescor de dependências do rebuild é evidência relatada pelo procedimento do autor, além do confronto independente dos hashes aqui registrado.

As seis flags abertas permanecem falsas, assim como `legacy_gate_changed`, `full_plan_complete` e `full_monolithic_runtime_run`. Não executei nem importei o monólito.

### Documentação, limite e custódia do parecer

A minuta segue idêntica à examinada: `MINUTA_IDEAL_SEMIFINITO.md`, SHA **`{V["documents"]["MINUTA_IDEAL_SEMIFINITO.md"]["sha256"]}`**. Recorder e verifier também permanecem idênticos aos snapshots já examinados; nenhum foi executado pelo revisor. Mantém-se o estatuto histórico do inventário de I/O, sem clearance de runtime da cópia atual.

O resultado matemático revisado continua sendo a aproximação forte da identidade, a ligação Fourier/Plancherel com o fator 2π, a avaliação uniforme dos quadrados das médias para h>0 e o ideal à esquerda fortemente aproximante de formas uniformemente finitas. **[OPEN, neste pacote]** Realização dos valores finitos como operadores limitados em F, semifinitude operatorial padrão, identificação F=base, correspondência geral espectral/predual, traço, Three Locks/H1–H3, física e runtime integral. A correção documental não resolve essas obrigações. `BoundedDualValues` não foi lido, recompilado ou incluído no parecer, e está ausente da integração inspecionada.

Evidência final: [verification.json](<{(CAP/"verification.json").as_posix()}>), com fontes, registros e logs congelados na mesma pasta. A comparação literal inicial permanece em `{max(RUN.glob("comment_erratum_*")).relative_to(REVIEW).as_posix()}`.

Backup imediato deste parecer antes do adendo: `{backup.name}`, **{len(old)} bytes**, SHA `{sha(old)}`; o novo arquivo preserva exatamente esse prefixo. Os pareceres custodiados anteriores foram conferidos e permanecem intocados. Escrita exclusivamente em `revisao/`; nenhuma alteração pelo revisor em fontes do autor, originais, logs, integração ou memórias. **Revisão delimitada encerrada; P2 documental resolvido e nenhuma análise deste escopo pendente.**
'''
new=old+text.encode("utf-8")
tmp=report.with_name(report.name+".tmp_"+stamp.strftime("%Y%m%d_%H%M%S_%f"))
with tmp.open("xb") as f:f.write(new)
assert tmp.read_bytes()==new and len(new)>len(old)
tmp.replace(report)
assert report.read_bytes()==new and report.read_bytes()[:len(old)]==old and backup.read_bytes()==old
receipt={"timestamp":stamp.isoformat(),"report":str(report),"report_sha256":sha(new),"report_bytes":len(new),"backup":str(backup),"backup_sha256":sha(old),"backup_bytes":len(old),"previous_prefix_preserved":True,"P2_documentary_status":"RESOLVED","bounded_review_complete":True,"current_um_sha256":V["current_snapshot_sha256"],"verification_sha256":sha((CAP/"verification.json").read_bytes()),"no_new_independent_compilation_or_tests":True,"no_author_code_executed":True}
with (CAP/"final_addendum_receipt.json").open("xb") as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode("utf-8"))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
