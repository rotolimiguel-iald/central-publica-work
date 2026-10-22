"""Append the integrated final stratum with immediate exact-byte backup."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/'modular_domain_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
V=json.loads((CAP/'verification.json').read_bytes())
S=json.loads((CAP/'supplemental_verification.json').read_bytes())
DEV=json.loads((RUN/'verification_dev.json').read_bytes())
M=json.loads((RUN/'manifest.json').read_bytes())
DATE=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def create(p,raw):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and tmp.stat().st_size==len(raw)>0
    tmp.replace(p)
    assert p.read_bytes()==raw

def link(p,label=None):return f'[{label or p.name}](<{p.as_posix()}>)'

assert V['all_exit_zero'] and V['all_hashes_match'] and V['exact_expected_file_set']
assert V['audit_unexpected_axioms']=={} and V['evidence_axioms_equal_log']
assert V['python_ast_outside_embedded_unchanged'] and V['gate_extension_byte_identical_to_79']
assert V['gate_checks_all_passed'] and all(not v for v in V['six_flags'].values())
assert S['new_target_axioms_match_own_auditor'] and S['new_targets_exact']
assert S['entire_test_AST_unchanged_after_only_added_controls_removed']
assert S['seven_new_compiles_source_unchanged'] and S['previous_reviews_preserved']
assert all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in M['sources'].values())
assert sha((ROOT/'um.py').read_bytes())==V['um_sha256']
for name in ['MINUTA_DOMINIO_MODULAR.md','record_modular_domain_progress.py','verify_modular_domain_custody.py',
             'integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    assert sha((ROOT/name).read_bytes())==V['artifact_sha256'][name]
rows=[]
for name,match in V['source_matches'].items():
    assert match['same_except_import_paths'] and match['dev_still_frozen'] and match['embedded_matches']
    r=next(r for r in V['records'] if r['file']=='TGLExt/V350'+name+'.lean')
    rows.append(f'| V350{name} | `{r["source_sha256"]}` | `{r["binary_sha256"]}` |')
logs='\n'.join(f'- `{r["source"]}` — `{r["timestamp"]}`, rc0/fonte inalterada.' for r in S['new_compilation_streams'])
hashrows='\n'.join(f'| {n} | `{V["artifact_sha256"][n]}` |' for n in
    ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
     'MINUTA_DOMINIO_MODULAR.md','record_modular_domain_progress.py','verify_modular_domain_custody.py'])
report=REVIEW/'REVIEW_MODULAR_DOMAIN.md';before=report.read_bytes()
backup=report.with_name(report.name+'.bak_'+STAMP);create(backup,before)
note=f'''

---

**ADENDO FINAL — {DATE}. Escopo DEV, integração e documentação concluído.**

Este adendo encerra a inspeção integrada que estava pendente no estrato DEV, preservado integralmente acima. **Nenhum P0/P1/P2 foi identificado nas cinco fontes ou na documentação; nenhuma análise matemática solicitada ficou pendente.** Permanece explicitamente o limite de reprodução do .olean de `RegularScalarWeightCertificate`, cuja causa não foi isolada e cuja identidade binária não é afirmada. Essa limitação não foi ocultada nem transformada em suposta falha da prova; a fonte final e o auditor próprios elaboraram com rc0 e axiomas permitidos.

**Snapshot final lido.** `um.py` tem SHA256 **`{V['um_sha256']}`**, igual aos registros de integração e controles. O dicionário extraído por AST contém **{V['embedded_files']} arquivos**. O original canônico foi lido somente para SHA às `{S['timestamp']}`: `{S['original_sha256']}`, igual à cópia-base e ao pin de `integration.json`. Não foi executado ou importado. A custódia escalar anterior, working `{V['previous_um_sha256']}`, foi usada como baseline, e seu parecer selado permaneceu byte a byte inalterado.

| Camada de evidência | Resultado | O que efetivamente fiz |
|---|---|---|
| DEV próprio | Cinco módulos + auditor, 6 processos rc0; 17 alvos no trio e 18 tipos nomeados conferidos | Recompilação própria com dependências congeladas; sem repetição após o sucesso |
| Integração autoral | {V['integrated_modules']} registros válidos | Li os registros e conferi os hashes atuais das 84 fontes/.olean |
| Reutilização | {S['reused_source_and_binary_count']} registros idênticos em fonte/binário à etapa escalar | Comparei com o snapshot próprio anterior; não recompilei dependências |
| Novas compilações integradas | Cinco módulos + TGLExt e TGL/Audit, total 7 | Li rc0, fonte inalterada e hashes; não recompilei raízes |
| Controles autorais | {V['gate_checks_count']}/{V['gate_checks_count']} marcados aprovados | Inspecionei JSON e AST do script; não executei os controles |
| Audit integrado | {V['audit_distinct']} declarações distintas, somente trio | Extraí o stdout do autor e comparei com o mapa em `kernel_incremental_evidence.json` |
| Alvos deste pacote | 17 nomes e conjuntos de axiomas correspondentes | Comparei explicitamente o Audit integrado com o auditor próprio |

Os 84 registros **não** significam 84 recompilações desta etapa. A distribuição medida é 77 reutilizados e 7 novos. Os identificadores dos sete logs novos são:

{logs}

As cinco fontes integradas correspondem aos bytes DEV congelados apenas pela troca dos imports `TGLV350.*` por `TGLExt.V350*`. Seus textos coincidem com as entradas embutidas, e ambas as raízes importam os cinco módulos. Não houve outra mudança nessas provas. Os hashes integrados lidos são:

| Fonte integrada | SHA256 fonte | SHA256 .olean autoral |
|---|---|---|
{chr(10).join(rows)}

O monólito recebeu exatamente essas cinco novas entradas; as únicas entradas anteriores alteradas foram as duas raízes, sem remoção de arquivos. **O AST Python fora do dicionário Lean coincide com o estrato anterior**, e `gate_extension.py` é byte a byte idêntico, SHA `{V['artifact_sha256']['gate_extension.py']}`. O script de controles acrescenta apenas `{S['added_controls'][0]}`: exige oito alvos desta etapa e as seis flags maiores falsas. Removida essa chamada, o AST inteiro do script é idêntico ao anterior. Não foi introduzido consumidor novo do certificado pelo corpo Python examinado; isso não é liberação de runtime nem prova de KMS por inspeção de nomes.

Os registros mantêm `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false` e as seis flags maiores falsas. `ScalarGNSOrbit` está ausente dos registros integrados e do monólito inspecionado; nenhum resultado desse desenvolvimento posterior foi usado ou auditado neste parecer.

**Documentação final.** Minuta, recorder e verifier mantiveram os mesmos bytes do estrato documental e foram conferidos novamente. Não há correção documental pendente. A minuta limita o resultado à invariância, certificado efetivo e subálgebra de aproximação forte junto aos adjuntos, com finitude dos dois quadrados; identifica expressamente KMS e GNS completo como pendências e exclui a etapa posterior. O mecanismo proposto de custódia foi apenas lido/analisado; suas 22 superfícies e backups futuros não foram executados por mim. O inventário I/O segue histórico, fonte `{S['runtime_inventory_historical_source_sha256']}`, e confere com a custódia correspondente, não com o SHA desta cópia como se fosse um inventário novo.

| Artefato final congelado | SHA256 lido |
|---|---|
{hashrows}

Evidências integradas em {link(CAP/'verification.json')} e {link(CAP/'supplemental_verification.json')}; registros, fontes e stdout/stderr estão preservados sob a mesma árvore. A evidência de recompilação própria permanece em {link(RUN/'compilation.json')} e {link(RUN/'verification_dev.json')}. A inspeção de logs integrados é distinta da recompilação DEV própria; nenhuma delas é execução integral do monólito.

**Conclusão delimitada.** As provas justificam a invariância de ν sob **Λ_t* A Λ_t**, o certificado `Prop` de 13 campos sobre os mesmos objetos, a passagem forte ao adjunto para contrações tendendo a I e a subálgebra complexa I∩I* com aproximação A_h=X_h* A X_h, ‖A_h‖≤‖A‖, A_h→A e A_h*→A* fortemente, com ambos os quadrados de ν finito. Não justificam KMS, grupo modular de ν identificado, GNS completo, core de grafo de Tomita, traço, certificado consumido pelo gate, Three Locks, física ou runtime. Essas fronteiras não são tratadas como bugs das provas presentes.

**Parecer final encerrado**, com a limitação binária já declarada. Nenhuma fonte autoral, memória ou parecer custodiado foi alterado; nenhuma execução de monólito, recorder, verifier ou testes autorais foi feita. Todas as saídas próprias ficaram em `revisao/`. Backup imediato do primeiro estrato: {link(backup)}, SHA `{sha(before)}`, preservado como prefixo exato deste parecer.
'''
after=before+note.encode('utf-8');assert after.startswith(before) and len(after)>len(before)
assert backup.read_bytes()==before
tmp=report.with_name(report.name+'.tmp_'+STAMP)
with tmp.open('xb') as f:f.write(after)
assert tmp.read_bytes()==after and tmp.stat().st_size==len(after)
tmp.replace(report);assert report.read_bytes()==after and report.read_bytes().startswith(backup.read_bytes())
closure={'timestamp':DATE,'complete':True,'scope':'FIVE_DEV_MODULES_17_TARGETS_AND_FINAL_STATIC_INTEGRATION_DOCUMENTATION',
    'findings_P0_P1_P2':[], 'own_compiles_rc0':6,'own_axiom_targets':17,'own_named_types':18,
    'binary_reproducibility_limit':{'module':'RegularScalarWeightCertificate',
        'own_sha256':DEV['records']['RegularScalarWeightCertificate']['own_binary_sha256'],
        'author_sha256':DEV['records']['RegularScalarWeightCertificate']['author_binary_sha256'],
        'cause_isolated':False,'own_source_compiled_and_audited':True},
    'integrated_records':V['integrated_modules'],'reused_records':S['reused_source_and_binary_count'],
    'new_integrated_compiles':len(S['new_compilation_streams']),'author_controls':V['gate_checks_count'],
    'author_audit_distinct':V['audit_distinct'],'embedded_files':V['embedded_files'],'working_sha256':V['um_sha256'],
    'minuta_sha256':V['artifact_sha256']['MINUTA_DOMINIO_MODULAR.md'],
    'report':str(report),'report_sha256':sha(after),'report_bytes':len(after),
    'previous_report_backup':str(backup),'previous_report_sha256':sha(before),'exact_prefix_preserved':True,
    'sealed_scalar_review_preserved':S['sealed_scalar_review_matches_custody'],
    'author_roots_tests_recorders_monolith_executed_by_reviewer':False}
create(CAP/'final_closure.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
