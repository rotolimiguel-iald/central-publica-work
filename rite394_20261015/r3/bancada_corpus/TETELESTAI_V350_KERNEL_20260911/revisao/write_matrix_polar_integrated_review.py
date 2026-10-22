"""Publish only after final integration records have been independently read."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=Path((REV/'matrix_polar_integrated_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
v=load(OUT/'verification.json');s=load(OUT/'static_verification.json');w=load(OUT/'gate_wiring.json')
assert v['integrated_records']==176 and v['gate_passed_author_records']==94 and v['audit_distinct']==6801
assert not any(v[k] for k in ['P0','P1','P2'])
for f,h in v['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_MATRIX_POLAR_DEV.md')==s['own_DEV_review_sha256']
assert all(not (ROOT/n).exists() for n in s['future_custody_artifacts_absent'])
assert hf(ROOT/'fontes/um_v350_original.py')==s['original_sha256']
for p,r in s['memory_surfaces'].items():
 if not r.get('external_pin_inherited_not_reread'):assert hf(p)==r['sha256'] and hf(r['backup'])==r['backup_sha256']
link=lambda label,p:'['+label+'](<'+str(p).replace(chr(92),chr(47))+'>)'
ar=v['final_Audit_record']
lines=['# Revisão integrada — conjugação polar matricial','', 'MATRIX_POLAR_INTEGRATED_REVIEW','',
f"{datetime.datetime.now().astimezone().isoformat(timespec='seconds')}. **[REAL] Sem achados P0, P1 ou P2 pendentes nesta integração de oito módulos/32 alvos.** O P2 documental do DEV foi encerrado por adendo e sua formulação corrigida permanece no recorder. Nenhuma nova análise matemática ou recompilação DEV foi necessária.",'',
f"Cópia verificada: `{v['working_sha256']}`. Mãe: `regular_polar_custody.json`, SHA256 `{v['parent_custody_sha256']}`. Foram medidos **{v['embedded_files']} embutidos**, **{v['integrated_records']} registros rc0**, **{v['gate_passed_author_records']} controles aprovados no registro autoral** e **{v['audit_distinct']} declarações distintas no stream Audit atual**. São {v['unchanged_parent_records']} registros exatamente herdados e {v['new_author_compilations']} novas compilações autorais (oito módulos + duas raízes); não 176 execuções novas.",'',
'**O que conferi diretamente:** fontes e binários em disco, logs JSON e bytes stdout/stderr de todos os registros; transposição literal dos oito DEV para TGLExt e igualdade com o conteúdo embutido; duas raízes, imports e frescor de suas dependências diretas de projeto; AST Python fora do dicionário; preservação dos alvos e mapa completo de axiomas; controles relatados, flags e helpers. Compilação integrada e controles foram executados pelo autor: esta revisão não os reexecutou e não executou/importou monólito, integrador, recorder ou verifier. A evidência de reprodução matemática própria é a do DEV já encerrado (oito módulos + três auditores acumulativos, último com 32 tipos/axiomas).','',
'| Fonte integrada | SHA256 fonte | SHA256 binário integrado relido |','|---|---|---|']
for r in v['new_records']:
 if r['file'] in ['TGLExt.lean','TGL/Audit.lean']:continue
 lines.append(f"| {link(Path(r['file']).name,ROOT/'kernel'/r['file'])} | `{r['source_sha256']}` | `{r['binary_sha256']}` |")
lines+=['',
'Os oito textos integrados são byte a byte o resultado de trocar somente `import TGLV350.` por `import TGLExt.V350` nas fontes DEV pinadas. Não houve mudança de enunciados, hipóteses, nomes de declaração ou provas. As raízes acrescentam os oito imports e os 32 `#print axioms`; os demais embutidos existentes permanecem iguais. Os oito binários DEV permanecem nos pins da reprodução própria. Os binários integrados têm seus próprios hashes e não são confundidos com os DEV cujos imports são diferentes.', '',
f"**Audit corrente:** {link(ar['log_name'],Path(ar['stdout_path']).with_name(ar['log_name']))}, SHA256 do log `{ar['log_sha256']}`; stdout bruto `{ar['stdout_sha256']}`. O mapa foi reextraído desses bytes: 6.769 declarações da mãe preservadas, com os mesmos conjuntos de axiomas, mais exatamente os 32 alvos novos. Os mapas dos oito módulos e a restrição do Audit final aos 32 alvos novos coincidem com o auditor próprio DEV; todos os 6.801 conjuntos ficam contidos em `propext`, `Classical.choice`, `Quot.sound`. Falhas históricas não foram usadas como evidência final.",'',
'`audit_stdout_sha256` e `audit_capture_sha256_full` correspondem ambos ao stream atual, no escopo `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. O dicionário `historical_v350_audit_metadata` continua igual ao baseline e ao da mãe; seus valores históricos não foram tomados pelo stream desta rodada. Os logs efetivos de `TGLExt.lean` e `TGL/Audit.lean` são novos rc0, com fontes inalteradas durante a compilação e binários existentes nos pins lidos.', '',
f"**Controles e gate:** os 93 controles da mãe são preservados e o único controle acrescentado é `{v['added_controls'][0]}`. Os 94 registros declaram aprovação, sem nomes duplicados. O gate legado e a fronteira permanecem iguais aos da mãe; as seis flags maiores estão falsas, `full_plan_complete=false` e não há runtime integral novo. `gate_extension.py` está byte a byte igual ao pin materno.",'',
f"A igualdade do AST exclui apenas o valor de `_EMBEDDED_KERNEL_FILES`, mantendo todo o restante comparado. A fiação foi inspecionada: `evaluate_quantum_gravity_closure` recebe `formal`, `physics`, `experiment`; o chamador forma esses dados por `qgc_`, `qgp_` e feed, e só depois anexa `kernel_frontier` (linhas {w['call_line']} e {w['annex_line']} da cópia). As seis flags qgf/gpf não são entradas diretas daquele avaliador. A nova prova não cria consumo de certificado ou promoção de gate.",'',
'**Helpers — leitura/AST, sem execução:** `prepare_matrix_polar_stage.py` acrescentou somente os oito módulos na ordem, batch 412→444, oito entradas antes das raízes e um grupo negativo de testes. As diferenças do integrador/compilador/testes foram comparadas com backups cujos hashes coincidem com a mãe. `record_matrix_polar_progress.py` e `verify_matrix_polar_custody.py` mantêm mãe matemática/documental única, os dois pareceres exigidos, releitura dos pares fonte/binário, hashes Audit atuais e históricos e 34 superfícies previstas. A escrita planeja backup dos bytes imediatamente anteriores, append com prefixo intacto e substituição por temporário verificado. Nada disso foi declarado executado nesta revisão; custódia, verificação e relatório integrado autorais ainda estavam ausentes ao fechar a inspeção.', '',
'A minuta preserva o mesmo H_I, A=S†S, T, B e J efetivos. A formulação corrigida usa `S=JB` em D(B), deriva a igualdade limitada em Ran(B) e a estende por densidade/continuidade. Não presume continuidade de S, inversa limitada de B, invertibilidade da unidade matricial, nem igualdade I=nν. O alcance continua sendo escala da raiz no domínio completo, conjugação das unidades matriciais locais e comutação das direitas homogêneas construídas com toda π(N).','',
'| Artefato | SHA256 lido |','|---|---|---|']
# Table has two columns.
lines[-1]='|---|---|'
for n in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','matrix_polar_draft_status.json','prepare_matrix_polar_stage.py','record_matrix_polar_progress.py','verify_matrix_polar_custody.py']:
 lines.append(f"| {link(n,ROOT/n)} | `{v['artifact_pins'][n]}` |")
lines+=['',
f"Evidência desta revisão: {link('verification.json',OUT/'verification.json')} (SHA256 `{hf(OUT/'verification.json')}`), {link('static_verification.json',OUT/'static_verification.json')}, {link('axioms.json reextraído do stream',OUT/'axioms.json')} e capturas/diffs nessa mesma árvore. DEV herdado: {link('REVIEW_MATRIX_POLAR_DEV.md',REV/'REVIEW_MATRIX_POLAR_DEV.md')}, incluindo P2 encerrado, SHA256 `{s['own_DEV_review_sha256']}`. O parecer DEV e as evidências históricas não foram modificados.",'',
'**Limite das leituras ao ROOT:** foram relidos os 32 pares memória/backup internos. Os pins das duas superfícies externas de memória e a preservação do original canônico permanecem herdados da custódia materna, sem nova leitura fora do ROOT nesta rodada; a cópia-base local foi relida e coincide com seu pin. Nenhuma memória foi escrita. O frescor e a reprodução anteriores das bibliotecas/dependências permanecem herdados; não houve recompilação de pacotes nem nova auditoria de runtime.', '',
'**Conclusão:** inspeção integrada delimitada concluída, sem P0–P2. Os resultados não demonstram igualdade global Jπ(N)J=π(N)′, identificação de A^it com o fluxo/KMS, traço, Three Locks, física ou consumo pelo gate. Essas obrigações permanecem abertas.','']
p=REV/'REVIEW_MATRIX_POLAR_INTEGRATED.md';assert not p.exists();b='\n'.join(lines).encode('utf-8');tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p);assert p.read_bytes()==b
print(str(p));print(hf(p))
