"""Append the completed integrated inspection, retaining the exact DEV report prefix."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'closed_tomita_batch_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'));PRE=max(RUN.glob('source_integration_*'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
V=json.loads((CAP/'verification.json').read_bytes());S=json.loads((PRE/'verification_source.json').read_bytes());T=json.loads((RUN/'type_comparison.json').read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
for k in ['complete','all_exit_zero','all_axioms_allowed','exact_99_audited','same_15_binaries_as_previous_independent','sources_unchanged','dependencies_preserved','previous_reviews_preserved']:assert C[k],k
for k in ['exact_99_types','all_99_types_with_universes_equal_previous','no_extra_assumptions_in_auditor','all_99_axioms_trio']:assert T[k],k
for k in ['incremental_build_ok','all_rc0','all_source_binary_log_hashes_match','exact_expected_files','new_compiles_source_unchanged','audit_trio_only','all_99_present_match_own_axioms','evidence_axioms_equal_Audit','gate_all_passed','old_controls_preserved','audit_count_matches_gate','working_hash_consistent','all_previously_inspected_static_artifacts_unchanged','source15_DEV_and_integrated_unchanged','previous_reviews_preserved']:assert V[k],k
for k in ['matches_integration_hash','matches_embedded_count','python_ast_outside_embedded_unchanged','gate_extension_unchanged_bytes','audit_added_targets_exact_99','audit_old_targets_preserved','test_old_AST_preserved_in_order','original_equal_localbase_and_pin','all_previous_reviews_preserved']:assert S[k],k
assert V['integrated_records']==118 and V['gate_checks']==V['gate_passed']==75 and V['audit_distinct']==6456
assert V['new_compilation_count']==17 and V['reused_same_source_binary_count']==101 and V['embedded_files']==820
assert not V['full_runtime_run'] and not V['legacy_gate_changed'] and not V['full_plan_complete'] and all(v is False for v in V['six_flags'].values())
assert all(all(v for k,v in row.items() if isinstance(v,bool)) for row in S['transposition'].values())
assert all(r['embedded_byte_equal'] and r['imports_each_once'] for r in S['roots'].values())
assert S['removed_embedded']==[] and S['changed_old_embedded']==['TGL/Audit.lean','TGLExt.lean']
for f,h in V['artifact_sha256'].items():assert sha((ROOT/f).read_bytes())==h,f
assert sha((ROOT/'um.py').read_bytes())==V['working_sha256']
report=REV/'REVIEW_CLOSED_SCALAR_TOMITA.md';before=report.read_bytes()
assert sha(before)==M['previous_reviews'][str(report)]
marker='INTEGRATED_CLOSED_SCALAR_TOMITA_REVIEW';assert marker.encode() not in before
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def link(label,p):return f'[{label}](<{p.as_posix()}>)'
aud=C['records'][-1];rows={r['file']:r for r in V['records']}
root_table='\n'.join(f"| {n} | `{rows[n]['timestamp']}` | `{rows[n]['binary_sha256']}` |" for n in ['TGLExt.lean','TGL/Audit.lean'])
module_table='\n'.join(f"| {Path(rel).stem} | {len(r['declarations'])} | `{r['integrated_sha256']}` |" for rel,r in M['sources'].items())
text=f'''

## {marker} — {date}

**[REAL — revisão integrada delimitada concluída; nenhum achado P0, P1 ou P2.]** Este adendo cobre os mesmos 15 módulos/99 alvos: cíclicos 4/26, gaussianos 9/49 e operador fechado/subespaço padrão 2/24. Preserva integralmente o parecer DEV acima e herda as análises matemáticas dos três pareceres. Não acrescenta resultados de módulos posteriores.

**Escopo efetivo da execução própria.** Recompilei novamente as **15 fontes DEV congeladas e um auditor próprio: 16 processos rc0**, com 99 `#check` (universos explícitos) e 99 `#print axioms`. Os 99 tipos impressos coincidem com os auditores próprios anteriores, e os 15 binários DEV coincidem byte a byte com as recompilações próprias anteriores. Todos os alvos usam apenas `propext`, `Classical.choice`, `Quot.sound`. Esta execução usa os nomes de módulo **TGLV350**: a versão **TGLExt/V350**, seus binários e as duas raízes foram conferidos por transposição literal, leitura de logs e hashes; **não foram recompilados pelo revisor com os nomes integrados**. A distinção vale também para as contagens autorais abaixo.

O ambiente reutilizou {len(M['dependencies'])} dependências de projeto congeladas da árvore própria e oito pacotes externos somente leitura; nenhum build autoral de projeto entrou no `LEAN_PATH`. Fontes e binários herdados, sua proveniência e as limitações anteriores permanecem explicitados no manifesto. A errata de comentário de `DualSemifiniteIdeal` continua a exceção histórica documentada; não houve recompilação global de bibliotecas nem nova certificação dos binários herdados. Compilador: `{M['compiler_sha256']}` ({M['lean_version']}).

Evidência própria: {link('manifest.json',RUN/'manifest.json')}, {link('compilation.json',RUN/'compilation.json')}, {link('comparação dos 99 tipos',RUN/'type_comparison.json')} e {link('auditor completo',Path(aud['stdout']))}. Fonte do auditor `{aud['source_sha256']}`; binário `{aud['output_sha256']}`; stdout `{aud['stdout_sha256']}`. O manifesto registra hashes das três execuções anteriores reaproveitadas; nenhuma aprovação foi inferida apenas dos nomes.

**Transposição e mesmo objeto.** Nos 15 arquivos, a diferença byte a byte é exclusivamente `import TGLV350.` → `import TGLExt.V350`. Não mudou enunciado, hipótese, universo, definição, prova ou instância local. As fontes integradas coincidem com as strings incorporadas no monólito. Só foram acrescentados 15 arquivos; entre os arquivos antigos, só mudaram `TGLExt.lean` e `TGL/Audit.lean`. Cada raiz importa os 15 exatamente uma vez, e o Audit acrescenta exatamente os 99 alvos sem retirar os anteriores. Evidência: {link('inspeção de fontes, roots e AST',PRE/'verification_source.json')} e seus diffs congelados.

| Módulo integrado (TGLExt/V350) | Alvos | SHA256 fonte integrada |
|---|---:|---|
{module_table}

**Snapshot autoral final inspecionado.** Cópia `{V['working_sha256']}`, **{V['embedded_files']} arquivos incorporados**. `integrated_compile.json` contém **{V['integrated_records']} registros rc0: {V['reused_same_source_binary_count']} herdados com fonte/binário iguais ao estrato anterior e {V['new_compilation_count']} compilações novas (15 módulos + 2 raízes)**. Conferi hashes atuais de fontes/binários, os JSON originais dos logs, streams e fonte inalterada durante as 17 compilações novas. Estas contagens descrevem a execução autoral lida, não 118 recompilações próprias.

| Raiz compilada pelo autor | Identificação do log final | SHA256 .olean lido |
|---|---|---|
{root_table}

O stdout do Audit contém **{V['audit_distinct']} declarações distintas**, todas no trio; coincide com `kernel_incremental_evidence.json`, e os 99 alvos novos coincidem com o auditor próprio. `gate_tests.json` registra **{V['gate_passed']}/{V['gate_checks']} controles aprovados**; os três acréscimos são `cyclic_cut_GNS_does_not_discharge_KMS_trace_or_physical_frontier`, `Gaussian_closability_does_not_discharge_KMS_trace_or_physical_frontier` e `closed_Tomita_and_standard_subspace_does_not_discharge_KMS_trace_or_physical_frontier`. O único acréscimo no AST do teste é o laço desses três controles; as instruções anteriores permanecem iguais e na mesma ordem. Não executei esses testes nem as raízes.

O AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a cópia custodiada `{S['previous_um_sha256']}`; `gate_extension.py` permanece byte a byte igual. As seis flags maiores continuam falsas, `legacy_gate_changed=false`, `full_plan_complete=false` e `full_runtime=false`. Original relido e igual à cópia-base/pin: `{S['original_sha256']}`. Evidência final e todos os hashes de fontes, logs, streams e documentos: {link('verification.json',CAP/'verification.json')}. Não executei/importei monólito, integrador, testes, recorder ou verifier autorais.

**Minuta e custódia: inspeção estática dos bytes finais.** Li o texto interpolado de relatório/memórias de `record_closed_tomita_progress.py`, SHA `{V['artifact_sha256']['record_closed_tomita_progress.py']}`, e o mecanismo de `verify_closed_tomita_custody.py`, SHA `{V['artifact_sha256']['verify_closed_tomita_custody.py']}`. A redação preserva H_I, o gráfico original, a injetividade de T sem inversa limitada, Fix(S) e D=Fix(S)+iFix(S); não promove esses resultados a Fix(J), identificação polar, KMS, traço ou consumo pelo gate. O comentário documental de H2/PyCBC foi confrontado apenas com a interface nomeada no original; não foi realizado rito físico.

Os scripts preveem backup imediato de bytes, append e registro do hash do estado imediatamente anterior, inclusive mudanças intervenientes nas memórias compartilhadas. O verifier compara os prefixos/bytes atuais e documenta a diferença perante a custódia anterior; não presume imutabilidade dessas memórias desde 09h12. Esta é leitura de código, **não execução nem confirmação antecipada da futura custódia**. `ROTA_APOS_TOMITA_FECHADO.md`, SHA `{V['artifact_sha256']['ROTA_APOS_TOMITA_FECHADO.md']}`, fica somente pinada como roteiro posterior sem prova nova; a marca de que I=n_ν não é uma obrigação automática está explícita. Suas propostas não foram incluídas na revisão matemática dos 99 alvos. O inventário I/O segue histórico e não fornece liberação de runtime.

**Conclusão e limites herdados.** O pacote integrado conserva as provas DEV: cortes cíclicos com injetividade conjunta; fecho univalente do gráfico original no mesmo H_I; S antilinear fechado, densamente definido e involutivo no domínio; K=Fix(S) padrão real e D=K+iK. Não se presume I=n_ν, fidelidade/separação de cada corte, inversa gaussiana limitada ou troca de representação. Identificação com o domínio/core adequado do peso, adjunto e decomposição polar modular, KMS, traço canônico/escala dual, Three Locks/H1–H3, física, certificado consumido e runtime permanecem fora da conclusão. **Nenhuma análise necessária resta neste escopo de integração.**

Preservação: o prefixo DEV de {len(before)} bytes, SHA `{sha(before)}`, foi guardado em backup imediato exato antes deste append. Os demais pareceres, fontes, originais, logs e memórias não foram alterados. Todas as saídas do revisor permanecem em `revisao/`.
'''
bak=report.with_name(report.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(before)
assert bak.read_bytes()==before
raw=before+text.encode('utf-8');tmp=report.with_name(report.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>len(before);tmp.replace(report)
assert report.read_bytes().startswith(before) and report.read_bytes()==raw
for p,h in M['previous_reviews'].items():
    if Path(p)!=report:assert sha(Path(p).read_bytes())==h
end={'timestamp':date,'status':'INTEGRATED_SCOPE_COMPLETE_NO_P0_P1_P2','review_path':str(report),'review_sha256':sha(raw),'review_bytes':len(raw),'review_lines':len(raw.splitlines()),'backup_path':str(bak),'backup_sha256':sha(bak.read_bytes()),'DEV_prefix_preserved':True,'working_sha256':V['working_sha256'],'own_DEV_compiles_plus_auditor':16,'own_targets':99,'author_integrated_records':V['integrated_records'],'author_controls':V['gate_checks'],'author_Audit':V['audit_distinct'],'integrated_module_and_root_rebuild_by_reviewer':False,'necessary_analysis_remaining':False,'findings':[]}
out=RUN/'closure_integrated.json';assert not out.exists();blob=json.dumps(end,ensure_ascii=False,indent=2).encode();tm=out.with_suffix('.json.tmp');tm.write_bytes(blob);assert tm.read_bytes()==blob;tm.replace(out)
print(json.dumps(end,ensure_ascii=False,indent=2))
