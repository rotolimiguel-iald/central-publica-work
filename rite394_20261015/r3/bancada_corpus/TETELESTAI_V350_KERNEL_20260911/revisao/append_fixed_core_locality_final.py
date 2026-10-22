"""Append the final integration/documentation stratum; never execute author scripts."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/"fixed_core_locality_latest_run.txt").read_text(encoding="utf-8"))
CAP=max(RUN.glob("final_integrated_*"));DOC=max(RUN.glob("documentary_*"))
V=json.loads((CAP/"verification.json").read_bytes());S=json.loads((CAP/"supplemental_verification.json").read_bytes());D=json.loads((DOC/"verification.json").read_bytes())
M=json.loads((RUN/"manifest.json").read_bytes());C=json.loads((RUN/"compilation.json").read_bytes());FIRST=json.loads((RUN/"source_review_receipt.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert all(C[k] for k in ["complete","all_exit_zero","full_audit_names_exact","all_axioms_allowed","sources_unchanged","dependencies_unchanged","previous_reviews_preserved"])
assert all(V[k] for k in ["exact_expected_file_set","all_exit_zero","all_hashes_match","gate_checks_all_passed","um_matches_gate_report","um_matches_integration_report","python_ast_outside_embedded_unchanged","gate_extension_byte_identical_to_58","previous_reviews_preserved"])
assert all(S[k] for k in ["evidence_axioms_equal_actual_Audit_log","exact_new_audit_names_equal_16_printed_targets","old_audit_names_and_axioms_preserved","all_16_axioms_match_own_auditor","auxiliary_not_counted_as_new_printed_target","new_records_source_unchanged_during_compile","incremental_build_ok","gate_count_matches_passed","gate_audit_count_matches","base_and_original_match_integration","documents_unchanged_since_review","previous_reviews_preserved","snapshot_reports_still_live"])
assert not V["audit_unexpected_axioms"] and not V["removed_embedded_files"]
assert (V["integrated_modules"],V["gate_checks_count"],V["audit_distinct"],V["embedded_files"])==(63,63,6192,765)
assert len(V["reused_same_binary_and_source_as_58"])==56 and len(V["new_compilations_relative_to_58"])==7
assert all(not value for value in S["six_open_flags"].values())
assert all(S[k] is False for k in ["legacy_gate_changed","full_plan_complete","full_monolithic_runtime_run"])
assert all(x["dev_still_frozen"] and x["same_except_import_paths"] and x["embedded_matches"] for x in V["source_matches"].values())
assert all(FIRST["source_binary_equal_author"].values())
assert sha((ROOT/"um.py").read_bytes())==V["um_sha256"]
for name in ["integration.json","integrated_compile.json","gate_tests.json","kernel_incremental_evidence.json","gate_extension.py","test_gate_extension.py"]:
    assert (ROOT/name).read_bytes()==(CAP/name).read_bytes()
for n in ["MINUTA_LOCALIDADE_FIXA.md","record_fixed_locality_progress.py"]:assert sha((ROOT/n).read_bytes())==D["hashes"][n]
for row in M["sources"].values():assert sha(Path(row["path"]).read_bytes())==row["sha256"]
for row in M["dependencies"].values():
    assert sha(Path(row["frozen_source"]).read_bytes())==row["source_sha256"]
    assert sha(Path(row["frozen_binary"]).read_bytes())==row["sha256"]
for p,h in M["previous_reviews"].items():assert sha(Path(p).read_bytes())==h
report=REVIEW/"REVIEW_FIXED_CORE_LOCALITY.md";old=report.read_bytes();assert sha(old)==FIRST["report_sha256"]
stamp=datetime.datetime.now().astimezone();backup=report.with_name(report.name+".bak_"+stamp.strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as f:f.write(old)
assert backup.read_bytes()==old
mapping='\n'.join(f'| {n} | `{x["integrated_sha256"]}` |' for n,x in V['source_matches'].items())
builds='\n'.join(f'| `{r["file"]}` | `{r["timestamp"]}` | `{r["binary_sha256"]}` |' for r in V['records'] if r['file'] in V['new_compilations_relative_to_58'])
text=f'''

## Adendo FINAL — {stamp.isoformat(timespec="seconds")} — integração e documentação

**[REAL] Revisão delimitada CONCLUÍDA, sem achados P0, P1 ou P2.** Este adendo encerra a pendência de integração do primeiro estrato. O escopo efetivo foi: cinco fontes finais, 16 alvos impressos, auxiliar ae conferido, seis processos independentes, integração por leitura de fontes/bytes/AST/logs, minuta e recorder. Nenhuma análise específica permanece pendente nesse escopo.

**Conclusão matemática:** no mesmo L² de Lebesgue, todo B∈F comuta com as translações ordinárias e com a multiplicação por indicadora de qualquer conjunto mensurável S, sem hipótese de `volume S<∞`. A passagem pelos pareamentos L¹ é válida e não assume avaliação pontual contínua, conjunto excepcional comum a todos os vetores, decomposição de B ou constância da ação na fibra. Não houve alteração das cinco fontes desde seus snapshots e recompilações.

### Separação das evidências

| Evidência | O que foi efetivamente feito |
|---|---|
| Cinco fontes dev e auditor próprio | **Executados pelo revisor:** 5 recompilações + 1 auditor rc0; 16 #print axioms exatos, 17 #check incluindo o auxiliar; somente o trio. Fontes, binários e 341 dependências pinadas conforme o primeiro estrato. |
| Build integrado | **Executado pelo autor; inspecionado pelo revisor:** 63 registros rc0 com fontes e `.olean` atuais verificados por hash. 56 registros conservam fonte/binário; 5 módulos novos + 2 raízes recompilados. |
| Controles Python | **Executados pelo autor; registros e novo controle lidos pelo revisor:** 63/63 aprovados. Nenhuma repetição pelo revisor. |
| Audit integrado | Stdout lido: 6192 declarações distintas, mapa igual ao evidence; exatamente 16 nomes acrescidos, com axiomas iguais aos do auditor próprio. |
| Runtime/registro de memórias | Não executados pelo revisor. Runtime integral continua pendente; recorder foi somente lido e analisado estaticamente. |

Os cinco `.olean` dev próprios coincidem byte a byte em SHA com os do autor, como registra o recibo do primeiro estrato. Os novos `.olean` integrados são artefatos distintos, pois os imports usam os nomes TGLExt/V350; sua proveniência é a dos processos do autor abaixo. O frescor de dependências do build integrado é relatado pelo procedimento do autor, além do confronto de hashes atuais e do estrato anterior aqui efetuado.

### Snapshot integrado efetivamente lido

SHA-256 de `um.py`: **`{V['um_sha256']}`**, igual a `integration.json` e `gate_tests.json`. Extraídos por AST/literal_eval **765 arquivos embutidos**, sem importação ou execução do monólito. O original canônico e a cópia-base foram relidos para hash: ambos **`{S['original_sha256']}`**, iguais ao `base_sha256` registrado.

As cinco cópias integradas coincidem com os respectivos dev mediante **somente a reescrita dos caminhos de import**, e com os textos embutidos byte a byte:

| Módulo | SHA-256 de `kernel/TGLExt/V350*.lean` |
|---|---|
{mapping}

Em relação ao estrato custodiado `{V['previous_um_sha256']}`, foram acrescentados exatamente esses cinco arquivos; nenhum embutido foi excluído. Apenas `TGLExt.lean` e `TGL/Audit.lean` mudaram entre as fontes antigas, pelos cinco imports, comentário de alcance e 16 alvos. O namespace `TGLV350.Fourier` de `fourier_integral_ae_injective` foi preservado corretamente; os outros alvos estão em `TGLV350.Regular`. `measurableCutLp_ae` não foi contado como alvo novo impresso.

Os sete registros novos do autor têm rc0 e fonte inalterada durante a compilação; hashes de saída lidos:

| Registro | Timestamp do log | SHA-256 `.olean` integrado |
|---|---|---|
{builds}

A AST Python fora de `_EMBEDDED_KERNEL_FILES` e os bytes de `gate_extension.py` permanecem iguais ao estrato anterior. O único controle acrescido, `fixed_core_locality_does_not_discharge_base_trace_or_physics`, verifica os nomes pertinentes e as seis flags maiores falsas. Os registros mantêm `legacy_gate_changed=false`, `full_plan_complete=false` e `full_monolithic_runtime_run=false`; nenhuma inferência de runtime/QG é extraída dessas contagens.

Evidências congeladas: [verification.json](<{(CAP/'verification.json').as_posix()}>), [supplemental_verification.json](<{(CAP/'supplemental_verification.json').as_posix()}>). Fontes integradas, stdout/stderr, relatórios e diffs dos agregadores/novo controle estão na mesma pasta. Os mapas inteiros de hashes/axiomas foram preservados, sem reescrever registros do autor.

### Minuta e recorder

Leitura integral, confronto conceitual e sintaxe AST concluídos, sem achados documentais. Hashes finais lidos, iguais aos snapshots examinados:

- `MINUTA_LOCALIDADE_FIXA.md`: **`{D['hashes']['MINUTA_LOCALIDADE_FIXA.md']}`**.
- `record_fixed_locality_progress.py`: **`{D['hashes']['record_fixed_locality_progress.py']}`**.

A minuta descreve corretamente unicidade Fourier em L¹, igualdade ae dos pareamentos, integração restrita e comutação P_S B=B P_S. A cota de norma do recorte decorre da construção `mkContinuous 1`; não exige medida finita de S. Os termos B*f(x) e Bg(x) devem ser lidos como `(B.adjoint f)(x)` e `(B g)(x)`, conforme os tipos formais, sem presumir B como campo pontual de operadores. As menções à futura ação constante/F=base estão explicitamente OPEN; o resultado atual é uma identidade de operadores no quociente L².

O recorder distingue corretamente `FourierUniqueness` pelo namespace Fourier, preserva o alcance das provas e mantém as flags maiores e os indicadores de base/interface de peso/traço abertos. Programa **{D['append_surfaces']} superfícies de append** (16 na ROOT e Atlas/índice), backups imediatos de bytes e escrita temporária verificada; exige `--review-read` e confronta fonte/binário, axiomas e snapshot antes de registrar. Essa leitura não certifica uma execução futura: não executei recorder ou verificador de custódia, nem escrevi nessas superfícies.

O inventário I/O permanece histórico, SHA `{D['hashes']['runtime_io_inventory.json']}`, associado à fonte `{D['historical_inventory_source_sha256']}` pelos campos históricos da custódia anterior. Não houve promoção desse inventário a liberação de runtime da cópia atual. [Registro documental](<{(DOC/'verification.json').as_posix()}>).

### Encerramento e preservação

**[OPEN]** Constância da ação na fibra e sua pertença à álgebra original/F=base; correspondência geral espectral/predual; interface padrão de peso operatorial, estado/gerador/perturbação e traço canônico; Three Locks/H1–H3 e física; contrato ampliado e runtime integral. Esses limites não são defeitos dos enunciados de localidade conferidos. **`UnitIntervalProjection` e a projeção posterior da componente constante não foram lidos, recompilados ou incluídos nesta revisão.**

Backup imediato deste parecer antes do adendo: `{backup.name}`, **{len(old)} bytes**, SHA `{sha(old)}`. O novo arquivo conserva integralmente esse prefixo. Todos os pareceres custodiados anteriores mantêm seus hashes; originais, fontes do autor, integração, logs, monólito e memórias permaneceram intocados pelo revisor. Escrita exclusivamente em `revisao/`. **Parecer final encerrado: nenhuma falha P0–P2 ou verificação delimitada pendente; nenhuma aprovação de F=base, traço, gate, QG ou runtime.**
'''
new=old+text.encode('utf-8');tmp=report.with_name(report.name+'.tmp_'+stamp.strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(new)
assert tmp.read_bytes()==new and len(new)>len(old);tmp.replace(report)
assert report.read_bytes()==new and report.read_bytes().startswith(old) and backup.read_bytes()==old
receipt={'timestamp':stamp.isoformat(),'report':str(report),'report_sha256':sha(new),'report_bytes':len(new),'backup':str(backup),'backup_sha256':sha(old),'backup_bytes':len(old),'exact_previous_prefix_preserved':True,'bounded_review_complete':True,'findings_P0_P1_P2':[],'independent_module_compilations_rc0':5,'independent_auditor_compilations_rc0':1,'printed_targets':16,'all_named_types_checked':17,'project_dependencies_frozen':341,'author_integrated_records':V['integrated_modules'],'author_controls':V['gate_checks_count'],'audit_distinct':V['audit_distinct'],'embedded_files':V['embedded_files'],'working_sha256':V['um_sha256'],'minuta_sha256':D['hashes']['MINUTA_LOCALIDADE_FIXA.md'],'recorder_sha256':D['hashes']['record_fixed_locality_progress.py'],'previous_custodied_reviews_preserved':True,'author_recorder_or_monolith_executed':False,'later_projection_module_read':False}
with (CAP/'final_report_receipt.json').open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
