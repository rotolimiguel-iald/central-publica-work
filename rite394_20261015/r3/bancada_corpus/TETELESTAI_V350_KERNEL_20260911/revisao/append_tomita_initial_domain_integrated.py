"""Append read-only integrated evidence; preserve DEV prefix with an immediate byte backup."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'tomita_initial_domain_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
M=json.loads((RUN/'manifest.json').read_bytes());V=json.loads((CAP/'verification.json').read_bytes());S=json.loads((CAP/'supplemental_verification.json').read_bytes())
C=json.loads((RUN/'closure_dev.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for k in ['exact_expected_file_set','all_exit_zero','all_hashes_match','gate_checks_all_passed','um_matches_gate_report','um_matches_integration_report','python_ast_outside_embedded_unchanged','gate_extension_byte_identical_to_92','previous_reviews_preserved','evidence_axioms_equal_log']:assert V[k],k
for k in ['original_local_base_equal_integration_pin','previous_custody_matches_AST_baseline','new_targets_exact','new_target_axioms_match_own_auditor','six_new_compiles_source_unchanged','all_previous_literal_control_calls_identical_AST','entire_test_AST_unchanged_after_only_added_controls_removed','runtime_inventory_pinned_to_history','working_um_unchanged','four_DEV_sources_unchanged','previous_reviews_preserved','sealed_GNS_review_matches_custody']:assert S[k],k
assert all(all(r[k] for k in ['dev_still_frozen','same_except_import_paths','embedded_matches']) for r in V['source_matches'].values())
assert all(V['posterior_modules_absent_from_embedded'].values())
assert not V['audit_unexpected_axioms'] and all(x is False for x in V['six_flags'].values())
assert all(not x for x in S['new_stdout_warnings'].values())
assert not V['legacy_gate_changed'] and not V['full_plan_complete'] and not V['full_monolithic_runtime_run']
for n,h in V['artifact_sha256'].items():assert sha(ROOT/n)==h,n
assert sha(ROOT/'um.py')==V['um_sha256']
for p,h in M['previous_reviews'].items():assert sha(Path(p))==h,p
p=R/'REVIEW_TOMITA_INITIAL_DOMAIN.md';assert sha(p)==C['review_sha256']
old=p.read_bytes();oldhash=sha(p)
now=datetime.datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
bak=p.with_name(p.name+'.bak_'+stamp)
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
records={r['file']:r for r in V['records']}
table='\n'.join('| '+name+' | `'+row['integrated_sha256']+'` | `'+records['TGLExt/V350'+name+'.lean']['binary_sha256']+'` |' for name,row in V['source_matches'].items())
artifacts=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','MINUTA_DOMINIO_INICIAL_TOMITA.md']
hashes='\n'.join('| '+n+' | `'+V['artifact_sha256'][n]+'` |' for n in artifacts)
text=f'''

## Adendo de conferência integrada — {now.isoformat(timespec='seconds')}

**Integração conferida, sem defeito P0/P1 ou divergência nas provas. P2 documental aberto:** {link(ROOT/'MINUTA_DOMINIO_INICIAL_TOMITA.md')}, linhas 5–7, omite a condição **A∈I** antes de afirmar A_h=X_h*A∈I∩I* para h>0. O teorema efetivo `scalarGNSLeftRegularization_mem_starCore` recebe `A : finiteDualLeftIdeal P` (`ScalarGNSStarApproximation.lean:21–27`). A condição permite concluir que X_h*A pertence a I por fechamento à esquerda; não deve ficar implícita numa frase iniciada apenas pela referência à álgebra N. Correção documental sugerida: “Para A∈I, a regularização A_h=X_h* A pertence a I∩I* para h>0 e Λ_ν(A_h) converge para Λ_ν(A) na norma de H_I.” Este achado não pede mudança de Lean nem invalida a conclusão DEV anterior. A minuta inspecionada está congelada com o hash registrado abaixo.

[REAL — inspeção independente de bytes, hashes, imports, AST e registros autorais] Snapshot integrado final medido: **`{V['um_sha256']}`**, {V['embedded_files']} embutidos. A cópia coincide com os pins de `integration.json` e `gate_tests.json`. O original canônico e `fontes/um_v350_original.py` foram relidos somente para SHA256: ambos `{S['original_sha256']}`, igual ao pin de base. Nenhum monólito foi executado/importado.

| Evidência | Resultado e alcance |
|---|---|
| Recompilação própria anterior | Quatro DEV + auditor rc0; 14 tipos/alvos, somente trio. Continua sendo a evidência independente do estrato DEV, preservada acima; não foi repetida. |
| Build integrado autoral | {V['integrated_modules']} registros rc0, todos com hashes de fonte e .olean conferidos. {S['reused_source_and_binary_count']} mantêm fonte/binário do estrato GNS custodiado; seis compilações são novas: quatro módulos e duas raízes. Não significa 96 recompilações. |
| Audit integrado autoral | {V['audit_distinct']} declarações distintas, somente `propext`, `Classical.choice`, `Quot.sound`; mapa extraído do stdout exatamente igual ao mapa de `kernel_incremental_evidence.json`. Os 14 alvos novos coincidem em nomes e conjuntos de axiomas com o auditor próprio. |
| Controles autorais | {V['gate_checks_count']}/{V['gate_checks_count']} registrados como passados. Relatório, vínculo ao snapshot e texto/AST do novo controle foram inspecionados; nenhum teste autoral foi executado pelo revisor. |
| Gate/runtime | Seis flags maiores `false`; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`. São estatutos conferidos nos registros, sem autorização de runtime ou fechamento de gate. |

**Fontes e tipos.** As quatro fontes integradas `TGLExt/V350*.lean` são exatamente os DEV congelados após a troca do prefixo de imports `TGLV350.` por `TGLExt.V350`. A comparação não precisou modificar finais de linha ou qualquer outro texto. Cada texto embutido coincide byte a byte com sua fonte integrada. Assim os corpos, tipos, quantificações e hipóteses conferidos na revisão DEV foram preservados; não houve um segundo `#check` independente das raízes nesta inspeção. A compilação integrada desses bytes é a execução autoral registrada.

| Módulo integrado | SHA256 fonte integrada | SHA256 .olean integrado autoral lido |
|---|---|---|
{table}

`TGLExt.lean` e `TGL/Audit.lean` importam explicitamente os quatro módulos. Contra o dicionário anterior custodiado, há somente quatro entradas novas, nenhuma removida e apenas as duas raízes alteradas entre as entradas preexistentes. As seis compilações novas declaram fonte inalterada durante a execução e seus seis stdout não têm warnings. Os hashes de **stdout e stderr de cada uma das seis**, timestamps e equivalência dos streams vivos às cópias congeladas constam de {link(CAP/'supplemental_verification.json')}; fontes e streams dos 96 registros foram preservados no mesmo snapshot. Os hashes de todos os binários foram relidos. A afirmação de identidade binária própria × autoral permanece limitada aos quatro DEV previamente recompilados, com as dependências herdadas e limitações explicitadas no primeiro estrato.

**AST e controle de fronteira.** A referência é a cópia anterior `{V['previous_um_sha256']}`, validada contra `gns_representation_custody.json`. Retirada somente a atribuição `_EMBEDDED_KERNEL_FILES`, a AST inteira de Python é idêntica. `gate_extension.py` também é idêntico em bytes, SHA256 `{V['artifact_sha256']['gate_extension.py']}`.

O único controle novo, `dense_initial_Tomita_graph_does_not_discharge_closed_Tomita_KMS_trace`, em `test_gate_extension.py:343`, exige a presença de seis declarações sobre limite, regularização, densidade e gráfico inicial, juntamente com as seis flags maiores falsas. Ele verifica presença de evidência e preservação da fronteira; não prova fechabilidade, Tomita fechado, KMS ou traço. Removida somente essa nova chamada, a AST inteira do teste coincide com a anterior. Nenhuma chamada antiga foi alterada/removida. As chamadas literais passam de 35 para 36; essa contagem sintática é distinta dos 69 controles do relatório autoral.

**Minuta e fronteira documental.** A minuta foi lida integralmente. Além do P2 de quantificação acima, preserva as distinções corretas: transferência por fatoração, densidade na norma de H_I, gráfico inicial como conjunto de pares, troca de coordenadas sem simetria de operador, fechabilidade e domínio máximo abertos. Seus placeholders de resultados são uma minuta de registro, não foram usados como evidência. Recorders específicos ainda não faziam parte desta solicitação e não foram inspecionados ou executados; esta revisão não atesta a futura execução/custódia desses scripts.

`ScalarGNSStrongContinuity` e `ScalarGNSNormality` foram confirmados ausentes das entradas e das referências embutidas. Não se leram nem compilaram suas fontes/logs para este adendo. Nenhum resultado posterior entra nos quatro módulos/14 alvos ou nas conclusões deste parecer. O inventário I/O conserva seu pin histórico `{S['runtime_inventory_sha256']}` e a fonte histórica `{S['runtime_inventory_historical_source_sha256']}`, comparados aos campos históricos da custódia anterior; não passa a ser liberação de runtime da cópia atual.

| Artefato integrado/documental lido | SHA256 |
|---|---|
{hashes}

Evidência detalhada: {link(CAP/'verification.json')} e {link(CAP/'supplemental_verification.json')}. Os arquivos pinados e a cópia foram reconferidos antes deste append. A integração foi inspecionada; **não houve novas recompilações próprias, rebuild de biblioteca/raízes ou execução de testes, recorders, verifiers ou monólito autorais**.

**Conclusão:** a conferência integrada dos quatro módulos/14 alvos está encerrada. Permanece a conclusão matemática do DEV: densidade GNS de Λ(I∩I*) e gráfico inicial univalente, invariante por troca, com domínio denso. Não há achado Lean pendente; há a correção P2 documental de A∈I a fazer na minuta. Fechabilidade, normalidade GNS, domínio máximo, KMS/traço, gate e runtime seguem fora da conclusão. As afirmações anteriores de “sem integração certificada” descrevem o estrato DEV e ficam superadas apenas pela inspeção integrada delimitada deste adendo.

Preservação: os {len(old)} bytes anteriores, SHA256 `{oldhash}`, foram guardados imediatamente em {link(bak)}. O novo texto é append desse prefixo exato. Nenhum parecer/custódia anterior foi modificado e nenhuma escrita saiu de `revisao/`.
'''.encode('utf-8')
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old
raw=old+text;tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and raw.startswith(old) and len(raw)>len(old)
tmp.replace(p);assert p.read_bytes()==raw
result={'timestamp':now.isoformat(),'status':'INTEGRATED_INSPECTION_COMPLETE_ONE_DOCUMENTARY_P2_OPEN','review_path':str(p),'review_sha256':sha(p),'review_bytes':len(raw),'backup':str(bak),'backup_sha256':sha(bak),'exact_DEV_prefix_preserved':raw.startswith(bak.read_bytes()),'working_sha256':sha(ROOT/'um.py'),'integrated_records':V['integrated_modules'],'author_controls':V['gate_checks_count'],'audit_distinct':V['audit_distinct'],'own_new_compiles_in_this_addendum':0,'new_Lean_findings':[],'documentary_findings':[{'priority':'P2','file':'MINUTA_DOMINIO_INICIAL_TOMITA.md','line':5,'issue':'Explicitly quantify A in I in the regularization claim','status':'OPEN','source_sha256':V['artifact_sha256']['MINUTA_DOMINIO_INICIAL_TOMITA.md']}],'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items())}
out=CAP/'final_closure.json';assert not out.exists();b=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');t=out.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(out)
print(json.dumps(result,ensure_ascii=False,indent=2))
