"""Close the two-module review by a byte-preserving, bounded final addendum."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/"bounded_finite_squares_latest_run.txt").read_text(encoding="utf-8"))
M=json.loads((RUN/"manifest.json").read_bytes())
C=json.loads((RUN/"compilation.json").read_bytes())
FIRST=Path(M["bounded_values_previous_run"])
FM=json.loads((FIRST/"manifest.json").read_bytes())
FC=json.loads((FIRST/"compilation.json").read_bytes())
CAP=max(RUN.glob("final_integrated_*"))
V=json.loads((CAP/"verification.json").read_bytes())
S=json.loads((CAP/"supplemental_verification.json").read_bytes())
BASE=json.loads((CAP/"base_preservation.json").read_bytes())
DOC=max(RUN.glob("documentary_*"))
D=json.loads((DOC/"verification.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
for compilation in [C,FC]:
    assert all(compilation[k] for k in ["complete","all_exit_zero","full_audit_names_exact","all_axioms_allowed","sources_unchanged","dependencies_unchanged","previous_reviews_preserved"])
assert len(C["records"][-1]["axioms"])==13
assert all(V[k] for k in ["exact_expected_file_set","all_exit_zero","all_hashes_match","gate_checks_all_passed","um_matches_gate_report","um_matches_integration_report","python_ast_outside_embedded_unchanged","gate_extension_byte_identical_to_56","previous_reviews_preserved"])
assert all(S[k] for k in ["evidence_axioms_equal_Audit_log","exact_13_targets_in_integrated_audit","all_13_axioms_match_own_auditor","first_10_axioms_match_combined_audit","second_imports_own_first_binary","new_integrated_records_source_unchanged_during_compile","incremental_build_ok","gate_count_matches_passed","gate_audit_count_matches","documentary_snapshot_unchanged","previous_custodied_reviews_preserved","exact_new_names_equal_13_targets"])
assert not S["first_and_second_shared_dependency_hash_mismatches"]
assert not V["audit_unexpected_axioms"] and not V["removed_embedded_files"]
assert BASE["equal_integration_base"]
assert (V["integrated_modules"],V["gate_checks_count"],V["audit_distinct"],V["embedded_files"])==(58,62,6176,760)
assert all(not v for v in S["six_open_flags"].values())
assert all(S[k] is False for k in ["legacy_gate_changed","full_plan_complete","full_runtime"])
for sm in V["source_matches"].values(): assert sm["dev_still_frozen"] and sm["same_except_import_paths"] and sm["embedded_matches"]
for manifest in [M,FM]:
    for row in manifest["sources"].values(): assert sha(Path(row["path"]).read_bytes())==row["sha256"]
    for row in manifest["dependencies"].values():
        assert sha(Path(row["frozen_source"]).read_bytes())==row["source_sha256"]
        assert sha(Path(row["frozen_binary"]).read_bytes())==row["sha256"]
assert sha((ROOT/"um.py").read_bytes())==V["um_sha256"]
for name in ["integration.json","integrated_compile.json","gate_tests.json","kernel_incremental_evidence.json","gate_extension.py","test_gate_extension.py"]:
    assert (ROOT/name).read_bytes()==(CAP/name).read_bytes()
for name in ["MINUTA_VALORES_LIMITADOS.md","record_bounded_values_progress.py","verify_bounded_values_custody.py"]:
    assert sha((ROOT/name).read_bytes())==D["hashes"][name]
report=REVIEW/"REVIEW_BOUNDED_DUAL_VALUES.md"
old=report.read_bytes()
initial=json.loads((FIRST/"first_review_receipt.json").read_bytes())
assert sha(old)==initial["report_sha256"]
stamp=datetime.datetime.now().astimezone()
backup=report.with_name(report.name+".bak_"+stamp.strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as f:f.write(old)
assert backup.read_bytes()==old
module=M["sources"]["TGLV350/BoundedFiniteSquares.lean"]
lines=Path(module["snapshot"]).read_text(encoding="utf-8").splitlines()
line_n={m.group(1):i+1 for i,l in enumerate(lines) if (m:=re.match(r'^theorem ([\w.]+)',l))}
own_table='\n'.join(f'| `{r["module"]}` | rc0 | {r["seconds"]} s | `{r["output_sha256"]}` |' for comp in [FC,C] for r in comp["records"])
mapping='\n'.join(f'| {n} | `{r["dev_sha256"]}` | `{r["integrated_sha256"]}` |' for n,r in V["source_matches"].items())
new_records='\n'.join(f'| `{r["file"]}` | `{r["timestamp"]}` | `{r["binary_sha256"]}` |' for r in V["records"] if r["file"] in V["new_compilations_relative_to_56"])
dep=M["dependencies"]["TGLV350.DualSemifiniteIdeal"]
text=f'''

## Adendo FINAL — {stamp.isoformat(timespec="seconds")} — dois módulos, 13 alvos e integração

**[REAL] Revisão delimitada CONCLUÍDA, sem achados P0, P1 ou P2.** Este adendo encerra as pendências declaradas no primeiro estrato. Foram examinadas as duas fontes finais, recompiladas independentemente, conferidos os 13 tipos/axiomas e a composição, e inspecionados a integração final, a minuta e os scripts de registro/custódia. Não permanece análise específica pendente dentro desse escopo.

O resultado conjunto é a existência e unicidade de representantes positivos limitados em **F da mesma realização regular**, para q_A sob uma cota uniforme explícita, e sua aplicação aos quadrados do ideal anterior. A aproximação forte agora possui **valores operatoriais limitados efetivos em F**; esse passo não fica reduzido à finitude escalar em um domínio de vetores. A identidade F=base original, a interface padrão de peso e o traço continuam abertos.

### Três enunciados novos de BoundedFiniteSquares

Fonte final: **{module['lines']} linhas**, SHA **`{module['sha256']}`**. Log do autor `{Path(module['author_log']).name}`, rc0, fonte inalterada durante a compilação, três alvos no trio, confrontado antes do build próprio. A prova e o stdout do auditor próprio foram lidos. O aviso de `change` redundante não altera o tipo elaborado.

- **Linha {line_n['HasFiniteDualSquare.exists_bounded_value']}, `HasFiniteDualSquare.exists_bounded_value`:** recebe A∈N e o predicado anterior `∃ C:ℝ≥0, ∀v, q_(A* A)(v)≤C·ofReal(‖v‖²)`. A prova estabelece A* A∈N e sua positividade, e converte a cota usando C≥0 e `ofReal_mul`. O resultado anterior fornece um único operador B≥0 em F cuja leitura representa q_(A* A) em todos os vetores. O ∃B vem antes de ∀v; não se escolhe um representante por vetor. A unicidade é herdada do lema já conferido, embora não seja repetida como uma cláusula deste enunciado. Não há passagem adicional por `toReal`.
- **Linha {line_n['regularAverage_bounded_value']}, `regularAverage_bounded_value`:** para h>0, o operador exibido é literalmente **h⁻¹·I** no mesmo Hilbert regular. Sua pertença a F decorre de unidade e estabilidade por escalares da álgebra; sua positividade usa h⁻¹>0. A igualdade quadrática aplica a avaliação Fourier/Haar da etapa anterior e `inner_smul_right`. Não escolhe outra normalização, não omite o fator 2π da derivação herdada e não afirma esse enunciado para h≤0. O resultado representa **q_(X_h*X_h)**; não afirma q_(h⁻¹I), que seria outro objeto.
- **Linha {line_n['boundedFiniteSquares_strong_approximation']}, `boundedFiniteSquares_strong_approximation`:** para cada A∈N, usa exatamente A·X_h, pertencente a N para todo h. Para cada h>0 existe B_(A,h)≥0 em F representando q_((A X_h)*(A X_h)) em todos os vetores; a mesma família A·X_h tende fortemente a A no filtro real **𝓝[>]0**. O filtro é não vazio e a variável de aproximação é comum a todos os vetores. O enunciado é uma testemunha explícita de aproximação/densidade forte de entradas cujos quadrados têm valores limitados; não é convergência na norma operatorial e não impõe cota uniforme dos valores B_(A,h) quando h→0. O crescimento h⁻¹ já aparece nas médias e é compatível com o setor infinito da forma da unidade.

As hipóteses estão nos tipos, incluindo A∈N, positividade da entrada no teorema representador, a cota uniforme ou `HasFiniteDualSquare`, e h>0 nas médias. Não se pressupõe a existência do representante para construí-lo, nem se identifica F com a base por homônimo. A composição conserva q, P, N, F e a representação Lebesgue L² anteriores.

### Recompilação própria e herança exata

**Dois módulos e dois auditores próprios, quatro processos rc0.** O primeiro auditor conferiu os dez nomes da fonte 1; o segundo importou a fonte 2 e conferiu **todos os 13 nomes exatos**, por `#check` com universos e `#print axioms`. Os 13 alvos têm somente `propext`, `Classical.choice`, `Quot.sound`; os dez primeiros mantêm os mesmos axiomas nos dois auditores.

| Processo independente | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
{own_table}

Auditor conjunto SHA de fonte **`{C['records'][-1]['source_sha256']}`**. A segunda árvore congela **{len(M['dependencies'])} dependências de projeto**, inclui o `.olean` de BoundedDualValues produzido na primeira árvore e não apresenta divergência de hash nas dependências compartilhadas entre as duas árvores. `LEAN_PATH`, compilador, fontes, binários e logs estão nos manifests/compilation.json; os hashes congelados e as fontes novas foram relidos após os processos. Pacotes e dependências não foram recompilados.

**Proveniência específica da dependência reutilizada:** a árvore própria conserva o `.olean` de `DualSemifiniteIdeal` anteriormente recompilado pelo revisor, SHA `{dep['sha256']}`, associado à fonte `{dep['source_sha256']}`. A fonte viva dessa dependência tem SHA `{dep['live_source_sha256']}` após a errata documental já encerrada. A comparação literal foi repetida durante o congelamento: todos os bytes fora daquele único comentário continuam idênticos. O manifest registra ambas as versões e os dois comentários; isso preserva a proveniência do artefato herdado, sem reconstruir essa dependência.

Consequentemente, a evidência própria da segunda fonte é uma elaboração sobre essa árvore explicitamente pinada. Seu `.olean` próprio `{C['records'][0]['output_sha256']}` **difere** do `.olean` dev do autor `{module['author_binary_sha256']}`; não declaro reprodução binária idêntica da árvore atual do autor. As fontes dos dois módulos novos são exatamente as finais, seus tipos e provas foram conferidos e a única divergência de fonte de projeto herdada em relação à árvore viva é o comentário documentado acima. A primeira fonte produziu `.olean` igual ao do autor. A auditoria transitiva dos 13 alvos passou em ambas as evidências comparadas.

Evidências próprias: [primeira compilation.json](<{(FIRST/'compilation.json').as_posix()}>), [segunda compilation.json](<{(RUN/'compilation.json').as_posix()}>), [manifest da segunda árvore](<{(RUN/'manifest.json').as_posix()}>). As falhas iniciais de acesso aos pacotes registradas no primeiro estrato permanecem preservadas como histórico de ambiente, sem defeito de elaboração pendente da fonte final.

### Integração final — inspeção, não rebuild de raízes pelo revisor

Cópia final `um.py`, SHA-256 **`{V['um_sha256']}`**, lido de bytes e igual ao declarado em `integration.json` e `gate_tests.json`. Original canônico e cópia-base foram relidos apenas para hash: **`{BASE['original_sha256']}`**, ambos iguais ao `base_sha256`. Nenhum monólito foi executado/importado.

[REAL — inspeção de execuções do autor] **58 registros integrados rc0**, com hashes atuais de todas as fontes e `.olean` conferidos. **54 registros preservam fonte e binário do estrato anterior; dois módulos novos e as duas raízes foram recompilados pelo autor**, com fonte inalterada durante os quatro processos:

| Registro recompilado pelo autor | Timestamp do log | SHA-256 `.olean` integrado lido |
|---|---|---|
{new_records}

**760 arquivos embutidos** lidos por AST/literal_eval. Apenas os dois módulos novos foram acrescentados; as únicas fontes antigas alteradas são TGLExt e Audit, com os dois imports e os 13 novos alvos pertinentes. Nenhum arquivo embutido foi removido. Dev e integrado coincidem mediante somente a reescrita dos imports; integrado e embutido coincidem byte a byte:

| Módulo | SHA-256 dev recompilado pelo revisor | SHA-256 integrado |
|---|---|---|
{mapping}

O Audit integrado contém **6176 declarações distintas**, somente no trio ou sem axiomas, e seu mapa coincide com `kernel_incremental_evidence.json`. A diferença de nomes contra o Audit anterior é exatamente o conjunto dos 13 alvos novos, cujos axiomas coincidem com o auditor próprio. O relatório atual registra **62/62 controles aprovados**. O novo controle `bounded_values_in_fixed_algebra_do_not_discharge_base_trace_or_physics` verifica presença dos alvos pertinentes e as seis flags falsas. Ele foi lido, não reexecutado pelo revisor; não é prova substituta dos lemas Lean.

A AST Python fora de `_EMBEDDED_KERNEL_FILES` e os bytes de `gate_extension.py` permanecem iguais ao snapshot anterior `{V['previous_um_sha256']}`. As seis flags maiores seguem falsas; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`. O frescor de dependências do rebuild integrado é relatado pelo procedimento do autor; minha inspeção acrescenta hashes atuais, comparação com o estrato custodiado, leitura de logs/diffs e a recompilação própria delimitada acima. Não houve rebuild integral de Mathlib ou kernel, nem repetição dos controles Python pelo revisor.

Evidências congeladas: [verification.json](<{(CAP/'verification.json').as_posix()}>), [supplemental_verification.json](<{(CAP/'supplemental_verification.json').as_posix()}>), [preservação da base](<{(CAP/'base_preservation.json').as_posix()}>). Fontes integradas, stdout/stderr, relatórios e diffs pertinentes estão na mesma pasta.

### Minuta e scripts de custódia

Leitura integral e sintaxe AST conferidas, sem execução; nenhum achado documental P0–P2. Os bytes finais continuam iguais aos examinados:

- `MINUTA_VALORES_LIMITADOS.md`: **`{D['hashes']['MINUTA_VALORES_LIMITADOS.md']}`**.
- `record_bounded_values_progress.py`: `{D['hashes']['record_bounded_values_progress.py']}`.
- `verify_bounded_values_custody.py`: `{D['hashes']['verify_bounded_values_custody.py']}`.

A minuta distingue o valor B da forma q e do operador de entrada, a representação h⁻¹I dos quadrados das médias e a aproximação de todo A∈N. O termo “valores limitados em F” é justificado pelos enunciados atuais. A descrição permanece vinculada às formas uniformemente limitadas e à mesma álgebra F; não declara peso canônico geral, identificação da base ou traço. Os placeholders de contagem/hash/data pertencem ao modelo de relatório que o recorder preencherá, não são evidências de execução por si.

O recorder exige `--review-read`, verifica fontes/binários, os alvos e axiomas, as seis flags, o SHA da cópia e a AST externa ao dicionário contra o estrato anterior; programa backups de bytes e escrita temporária. São **{D['surface_count']} superfícies de append** (15 na ROOT e Atlas/índice), com custódia posterior dos hashes. O verifier programado compara os hashes e os prefixos dos backups. Esta é inspeção estática desse mecanismo; o registro e sua verificação posteriores cabem ao autor, e não são declarados executados aqui.

O inventário I/O continua histórico, SHA `{D['hashes']['runtime_io_inventory.json']}`, vinculado à fonte `{D['historical_inventory_source_sha256']}` pelos campos históricos da custódia anterior. A minuta não o promove a inspeção de runtime da cópia atual. [Evidência documental](<{(DOC/'verification.json').as_posix()}>).

### Limites e encerramento

**[OPEN]** F=base original; correspondência geral espectral/predual; interface padrão de peso operatorial, incluindo a formulação e quitação de suas obrigações de semifinitude; estado modular/gerador/perturbação e traço canônico; Three Locks/H1–H3, física e interações/BRST/QME/anomalias/UV; contrato ampliado e runtime integral. A densidade forte com quadrados de valores limitados efetivos em F está provada neste pacote; isso não equivale a construir o traço ou a resolver as identificações/interfaces restantes. Nenhuma flag maior, QG, publicação ou transposição canônica é aprovada pelo parecer.

`FixedCoreShiftCommutation` é desenvolvimento posterior e não foi lido ou incluído nesta revisão. Fontes novas, originais, logs, monólito, memórias e pareceres custodiados permaneceram intocados pelo revisor. As leituras das etapas anteriores ficaram limitadas às dependências/proveniência necessárias aos dois módulos.

Backup imediato do primeiro estrato antes deste adendo: `{backup.name}`, **{len(old)} bytes**, SHA `{sha(old)}`; seu prefixo é preservado byte a byte. **Escopo final dos dois módulos, 13 alvos, integração e documentação encerrado; nenhum achado P0–P2 ou verificação específica pendente.**
'''
new=old+text.encode('utf-8')
tmp=report.with_name(report.name+'.tmp_'+stamp.strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(new)
assert tmp.read_bytes()==new and len(new)>len(old)
tmp.replace(report)
assert report.read_bytes()==new and report.read_bytes().startswith(old) and backup.read_bytes()==old
for p,h in M['previous_reviews'].items():
    if Path(p).name!='REVIEW_BOUNDED_DUAL_VALUES.md': assert sha(Path(p).read_bytes())==h
receipt={'timestamp':stamp.isoformat(),'report':str(report),'report_sha256':sha(new),'report_bytes':len(new),'backup':str(backup),'backup_sha256':sha(old),'backup_bytes':len(old),'exact_old_prefix_preserved':True,'bounded_joint_review_complete':True,'findings_P0_P1_P2':[],'independent_module_compilations_rc0':2,'independent_auditor_compilations_rc0':2,'exact_distinct_new_targets':13,'author_integrated_records':V['integrated_modules'],'author_controls':V['gate_checks_count'],'author_audit_distinct':V['audit_distinct'],'embedded_files':V['embedded_files'],'current_um_sha256':V['um_sha256'],'minuta_sha256':D['hashes']['MINUTA_VALORES_LIMITADOS.md'],'frozen_previous_comment_only_dependency_explicitly_disclosed':True,'previous_custodied_reviews_preserved':True,'recorder_or_monolith_executed':False,'scope_expanded':False}
with (CAP/'final_report_receipt.json').open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
