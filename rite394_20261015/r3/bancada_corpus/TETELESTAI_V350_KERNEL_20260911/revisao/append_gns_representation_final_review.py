"""Append the integrated inspection with immediate exact-byte backup of this new report only."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'gns_representation_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
M=json.loads((RUN/'manifest.json').read_bytes());D=json.loads((RUN/'verification_dev.json').read_bytes())
V=json.loads((CAP/'verification.json').read_bytes());S=json.loads((CAP/'supplemental_verification.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for k in ['all_exit_zero','all_hashes_match','exact_expected_file_set','gate_checks_all_passed','um_matches_gate_report','um_matches_integration_report','python_ast_outside_embedded_unchanged','gate_extension_byte_identical_to_84','previous_reviews_preserved','evidence_axioms_equal_log']:assert V[k],k
for k in ['original_local_base_equal_integration_pin','previous_custody_matches_AST_baseline','new_targets_exact','new_target_axioms_match_own_auditor','ten_new_compiles_source_unchanged','all_previous_literal_control_calls_identical_AST','entire_test_AST_unchanged_after_only_added_controls_removed','runtime_inventory_pinned_to_history','all_final_artifacts_live_hashes_unchanged','working_um_unchanged','five_DEV_sources_unchanged','previous_reviews_preserved','sealed_modular_review_matches_custody','cumulative_35_targets_exact','prior_14_axioms_match_integration']:assert S[k],k
assert not V['audit_unexpected_axioms'] and all(v is False for v in V['six_flags'].values())
assert not V['full_monolithic_runtime_run'] and not V['legacy_gate_changed'] and not V['full_plan_complete']
assert all(all(r[k] for k in ['dev_still_frozen','same_except_import_paths','embedded_matches']) for r in V['source_matches'].values())
assert all(V['posterior_modules_absent_from_embedded'].values())
for n,h in V['artifact_sha256'].items():assert sha(ROOT/n)==h,n
assert sha(ROOT/'um.py')==V['um_sha256']
for p,h in M['previous_reviews'].items():assert sha(Path(p))==h,p
for row in D['records'].values():
    assert all(v for v in row.values() if isinstance(v,bool))
    assert all(row['streams'][k]['author_equals_frozen'] for k in ['stdout','stderr'])
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
time=datetime.datetime.now().astimezone();stamp=time.strftime('%Y%m%d_%H%M%S_%f')
p=R/'REVIEW_GNS_REPRESENTATION.md';old=p.read_bytes();oldhash=sha(p)
bak=p.with_name(p.name+'.bak_'+stamp)
artifacts=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','MINUTA_REPRESENTACAO_GNS.md','record_gns_representation_progress.py','verify_gns_representation_custody.py']
tab='\n'.join('| '+n+' | `'+V['artifact_sha256'][n]+'` |' for n in artifacts)
source_table='\n'.join('| '+n+' | `'+r['integrated_sha256']+'` |' for n,r in V['source_matches'].items())
new=f'''

## Adendo final — integração e documentação encerradas

{time.isoformat(timespec='seconds')}. [REAL — inspeção independente de fontes, binários, AST e registros autorais; sem recompilação própria das raízes ou execução dos controles]

**Escopo concluído. Nenhum achado P0–P2 nas cinco fontes finais nem na integração/documentação delimitada.** O estrato DEV acima permanece preservado. A menção anterior à pendência de integração é superada por este adendo, que conserva a distinção entre execuções próprias e registros inspecionados.

Snapshot final medido: **`{V['um_sha256']}`**, {V['embedded_files']} arquivos embutidos. O hash da cópia coincide com `integration.json` e `gate_tests.json`. Original canônico e cópia-base foram lidos somente para hash e coincidem com o pin: `{S['original_sha256']}`. Nenhum deles foi importado/executado.

| Evidência | Resultado | Como foi conferida |
|---|---|---|
| Cinco DEV desta revisão | 21 alvos; cinco recompilações próprias rc0 | Duas árvores próprias sucessivas e auditor cumulativo de 21 alvos/22 tipos; sete processos rc0 contando os dois auditores. |
| Três DEV do parecer GNS_ORBIT | 14 alvos anteriores reutilizados | Pins e axiomas da revisão anterior comparados ao novo status e Audit integrado; sem nova recompilação. |
| Build integrado autoral | {V['integrated_modules']} registros válidos | Fonte e .olean de cada registro conferidos por hash; 82 registros preservam fonte/binário do estrato 84, e dez compilações são novas: oito módulos GNS e duas raízes. Não significa 92 recompilações. |
| Controles Python autorais | {V['gate_checks_count']}/{V['gate_checks_count']} registrados como passados | JSON, hash da cópia e AST do controle novo inspecionados. Não executados pelo revisor. |
| Audit integrado autoral | {V['audit_distinct']} nomes distintos, todos no trio | Extração do stdout e igualdade exata com `kernel_incremental_evidence.json`; 35 alvos GNS cumulativos, sendo 21 novos nesta revisão e 14 anteriores. |
| Gate e runtime | Seis flags maiores `false`; `legacy_gate_changed=false`; `full_plan_complete=false`; runtime `false` | Registros finais, AST e bytes do helper inspecionados; não constituem autorização de runtime ou fechamento do gate. |

**Correspondência da integração.** Os oito DEV finais são iguais às fontes TGLExt e aos textos embutidos após a única tradução `import TGLV350.` → `import TGLExt.V350`. Não foi necessária normalização adicional de finais de linha. As duas raízes importam os oito módulos; em relação ao snapshot custodiado anterior só esses oito arquivos foram acrescentados ao dicionário e só as duas raízes anteriores mudaram. Os quatro desenvolvimentos posteriores estão ausentes do dicionário e das referências embutidas.

| Módulo integrado TGLExt/V350 | SHA256 da fonte integrada |
|---|---|
{source_table}

Os dez logs novos, seus timestamps, stdout/stderr e hashes estão preservados no snapshot {link(CAP)}. Em todos os dez registros a fonte permaneceu inalterada durante a compilação; não há warnings nesses dez stdout. Os resultados não autorizam extrapolar a reprodução binária própria para as raízes ou toda a biblioteca. A igualdade byte a byte **própria × autoral** afirmada neste parecer refere-se aos cinco .olean DEV medidos, com a herança explicitada no primeiro estrato.

**Python e controle novo.** A AST de `um.py`, excluída somente a atribuição `_EMBEDDED_KERNEL_FILES`, é idêntica à da cópia anterior pinada por `modular_domain_custody.json` (`{V['previous_um_sha256']}`). `gate_extension.py` é byte a byte idêntico, SHA256 `{V['artifact_sha256']['gate_extension.py']}`. O único controle acrescentado é `finite_ideal_GNS_representation_does_not_discharge_Tomita_KMS_trace`, em `test_gate_extension.py:331`: exige a presença de oito declarações representativas e a manutenção das seis flags falsas. É um controle de fronteira e presença de evidência, não uma prova de Tomita/KMS/traço. Removida apenas essa chamada nova, a AST inteira do teste coincide com a anterior; nenhuma chamada antiga foi alterada ou removida. A contagem sintática de chamadas literais passa de 34 para 35, distinta dos 68 controles gerados/executados pelo autor.

**Minuta e recorder finais.** A minuta permanece idêntica ao pin já lido; seu relato distingue a completude de H_I, a fidelidade provada e as obrigações abertas. O recorder e o verifier atualizados foram lidos estaticamente, inclusive o adendo posterior, e ambos passam `ast.parse`. O recorder usa backup binário imediato e append preservando prefixos, substituição por temporário verificado, pin do parecer GNS_ORBIT e validação de fontes/binários/AST; o verifier confere esses hashes e os prefixos. Nenhum dos dois foi executado nesta revisão, portanto não há aqui atestado de custódia já produzida ou de execução futura bem-sucedida.

A nota adicionada pelo autor separa nominalmente quatro módulos posteriores/14 alvos em `post_scope_development`, com `independently_reviewed=False` e `integrated=False`, sem somá-los aos oito/35 deste registro. Conferi somente essa separação de estatuto e a ausência no pacote embutido. **Não revisei os enunciados, provas, logs ou binários desses quatro módulos**, nem a rota posterior; as afirmações matemáticas dessa nota permanecem [DECLARADO — autor, fora desta revisão]. A presença da nota não certifica densidade por I∩I* ou gráfico de Tomita neste parecer.

O inventário I/O é explicitamente histórico: hash `{S['runtime_inventory_sha256']}`, fonte histórica `{S['runtime_inventory_historical_source_sha256']}`, ambos comparados aos campos históricos da custódia anterior. Essa comparação não o transforma em inventário da cópia atual nem em liberação de execução.

| Artefato final lido | SHA256 |
|---|---|
{tab}

Evidência de inspeção: {link(CAP/'verification.json')}, {link(CAP/'supplemental_verification.json')}; evidência de execução própria: {link(RUN/'verification_dev.json')} e os dois `compilation.json` ligados acima. Todos os arquivos finais pinados foram reconferidos antes deste append. O parecer anterior GNS_ORBIT e os demais pareceres permanecem byte a byte preservados.

**Conclusão verificável:** representação complexa unital fiel da mesma N sobre o fecho H_I da inscrição do ideal I, com imagem densa, entrelaçamento e cota de norma. Nenhuma análise necessária dentro dos cinco módulos/21 alvos ficou pendente. A integração dos oito/35 foi conferida pelos meios descritos; controles/raízes são evidência autoral inspecionada. Permanecem os limites de domínio máximo, normalidade, Tomita/KMS/traço, gate e runtime já delimitados. Escopo encerrado; sem extensão às fontes posteriores.

Preservação deste parecer: prefixo anterior de {len(old)} bytes, SHA256 `{oldhash}`, guardado imediatamente em {link(bak)} antes do append. Pareceres custodiados anteriores não foram tocados.
'''.encode('utf-8')
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old
raw=old+new;tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and raw.startswith(old) and len(raw)>len(old)
tmp.replace(p);assert p.read_bytes()==raw
closure={'timestamp':time.isoformat(),'status':'COMPLETE_DELIMITED_NO_P0_P1_P2','review':str(p),'review_sha256':sha(p),'review_bytes':len(raw),'backup':str(bak),'backup_sha256':sha(bak),'prefix_preserved':raw.startswith(bak.read_bytes()),'working_sha256':sha(ROOT/'um.py'),'own_new_sources':5,'own_targets':21,'inherited_targets':14,'integrated_records':len(V['records']),'author_controls':V['gate_checks_count'],'author_audit_distinct':V['audit_distinct'],'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),'author_monolith_scripts_tests_executed':False}
out=CAP/'final_closure.json';assert not out.exists();b=json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8');t=out.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(out)
print(json.dumps(closure,ensure_ascii=False,indent=2))
