"""Append the measured integrated verdict, preserving the exact preliminary prefix."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
OUT=Path((REV/'base_polar_integrated_latest_run.txt').read_text().strip());v=load(OUT/'verification.json');s=load(OUT/'static_verification.json')
assert v['integrated_records']==180 and v['unchanged_parent_records']==174 and v['new_author_compilations']==6
assert v['gate_passed_author_records']==95 and v['audit_distinct']==6820
assert not any(v[k] for k in ['P0','P1','P2']) and v['external_memory_pins_inherited']==0
assert all(hf(ROOT/f)==h for f,h in v['artifact_pins'].items())
assert hf(ROOT/'um.py')==v['working_sha256'] and hf(REV/'REVIEW_BASE_POLAR_DEV.md')==s['own_DEV_review_sha256']
assert hf(load(ROOT/'environment.json')['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==s['original_sha256']
for p,r in s['memory_surfaces'].items():assert hf(p)==r['sha256'] and hf(r['backup'])==r['backup_sha256']
assert not any((ROOT/f).exists() for f in s['future_custody_artifacts_absent'])
link=lambda label,p:'['+label+'](<'+str(p).replace(chr(92),'/')+'>)'
a=v['final_Audit_record'];date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
lines=['','','---','','## Adendo final — evidências integradas conferidas','',
f"{date}. **[REAL] Revisão integrada concluída, sem P0–P2.** Este adendo encerra as pendências do estrato preliminar, preservado integralmente acima. Escopo: quatro módulos/19 alvos e respectivos helpers; nenhuma recompilação DEV, biblioteca ou runtime foi repetida.",'',
f"Cópia relida: `{v['working_sha256']}`; **882 embutidos, 180 registros rc0, 95/95 controles relatados e 6.820 declarações distintas no Audit corrente**. Os registros se decompõem em **174 exatamente herdados + seis novas execuções autorais**, quatro módulos e duas raízes. Não são 180 recompilações novas.",'',
'Foram relidos os 180 pares fonte/binário, os JSONs dos logs e seus streams stdout/stderr. Hashes, existência do binário, rc0 e conteúdo embutido conferem. As seis novas execuções registram fonte inalterada durante a compilação; seus imports diretos de projeto têm binários presentes e anteriores ao resultado. As quatro transposições preservam literalmente os bytes DEV, exceto o prefixo dos imports. Os conjuntos de axiomas novos coincidem com os auditores próprios já concluídos; não se confundem binários DEV e integrados, pois os imports são diferentes.','',
'| Módulo integrado | SHA256 fonte | SHA256 .olean relido |','|---|---|---|']
for r in v['new_records']:
 if r['file'] in ['TGLExt.lean','TGL/Audit.lean']:continue
 lines.append(f"| {link(Path(r['file']).name,ROOT/'kernel'/r['file'])} | `{r['source_sha256']}` | `{r['binary_sha256']}` |")
lines+=['',
f"**Audit atual:** {link(a['log_name'],ROOT/'logs'/a['log_name'])}, SHA256 do log `{a['log_sha256']}`; stdout bruto `{a['stdout_sha256']}`. O mapa foi reextraído desse stream e coincide com `axiom_report`: os 6.801 nomes da mãe e seus conjuntos de axiomas estão preservados, somados exatamente aos 19 nomes do manifesto. Todos os 6.820 conjuntos estão contidos em `propext`, `Classical.choice`, `Quot.sound`; os 19 novos correspondem ao auditor próprio. Nenhum print de tentativa rc1 foi aceito.",'',
'`audit_stdout_sha256` e `audit_capture_sha256_full` são iguais ao hash do stdout corrente, no escopo `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`; `historical_v350_audit_metadata` permanece igual ao baseline e à mãe. As raízes `TGLExt.lean` e `TGL/Audit.lean` têm logs novos rc0, fontes e binários conferidos.','',
f"**Controles:** os 94 registros da mãe são preservados e o novo controle é `{v['added_controls'][0]}`. São 95 nomes únicos e todos aprovados no relatório autoral. A inspeção confirmou `legacy_gate_changed=false`, as seis flags maiores falsas, `full_plan_complete=false` e runtime integral não executado. `gate_extension.py` e o AST Python externo ao dicionário continuam iguais aos da mãe. O revisor leu essas evidências; não executou os testes autorais.",'',
'**Helpers e custódia:** as versões efetivas de maker/preparador/recorder/verifier continuam iguais às lidas no DEV e no estrato estático. A redação distingue M, N, ι, π, Δ=S†S e o J efetivo; não amplia a comutação da base para igualdade global dos comutantes. Os 34 pares de memória/backup e o original canônico foram relidos, sem alterações. A futura escrita prevê backups imediatos de bytes e preservação de prefixos. Recorder/verifier não foram executados pelo revisor; a nova custódia, verificação e relatório integrado autorais permaneciam ausentes nesta conferência.','',
'| Artefato final | SHA256 lido |','|---|---|']
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','prepare_base_polar_stage.py','record_base_polar_progress.py','verify_base_polar_custody.py']:
 lines.append(f"| {link(f,ROOT/f)} | `{v['artifact_pins'][f]}` |")
lines+=['',
f"Evidência consolidada: {link('verification.json',OUT/'verification.json')} (SHA256 `{hf(OUT/'verification.json')}`), {link('axioms.json do stream atual',OUT/'axioms.json')} e capturas dos 180 logs/streams nessa árvore. Evidência matemática própria herdada: {link('REVIEW_BASE_POLAR_DEV.md',REV/'REVIEW_BASE_POLAR_DEV.md')}. Permanece explícita sua limitação: 150 dependências históricas foram herdadas por comparação de bytes com a base/canônico e copiadas à árvore isolada, sem recompilação própria delas; os quatro módulos novos e os auditores DEV foram recompilados.",'',
'**Conclusão delimitada:** nenhuma análise necessária desta integração ficou pendente. Vale a comutação de Jπ(ι(x))J⁻¹ com π(y), para todo x∈M e y∈N, no mesmo H_I/J. Igualdade global Jπ(N)J=π(N)′, identificação de Δ^it/fluxo/KMS, traço, Three Locks, física e consumo pelo gate continuam fora do resultado. Não houve execução/importação de monólito, escrita de memórias ou alteração dos pareceres DEV/custodiados.','']
p=REV/'REVIEW_BASE_POLAR_INTEGRATED.md';before=p.read_bytes();assert b'BASE_POLAR_INTEGRATED_REVIEW' in before
assert '## Adendo final'.encode() not in before
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');backup=p.with_name(p.name+'.bak_'+stamp)
with backup.open('xb') as f:f.write(before)
assert backup.read_bytes()==before
raw=before+'\n'.join(lines).encode('utf-8');tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==before and len(raw)>len(before)
tmp.replace(p);assert p.read_bytes()==raw and raw.startswith(backup.read_bytes())
publication={'timestamp':date,'review_path':str(p),'review_sha256':sha(raw),'backup_path':str(backup),'backup_sha256':sha(before),'exact_prefix_preserved':True,'verification_sha256':hf(OUT/'verification.json')}
q=OUT/'review_publication.json';assert not q.exists();b=(json.dumps(publication,ensure_ascii=False,indent=2)+'\n').encode('utf-8');t=q.with_name(q.name+'.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(q)
print(json.dumps(publication,ensure_ascii=False))
