"""Close the delimited review by exact-byte backup and append only."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/'scalar_dual_weight_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
V=json.loads((CAP/'verification.json').read_bytes())
S=json.loads((CAP/'supplemental_verification.json').read_bytes())
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def create(path,raw):
    assert path.resolve().is_relative_to(REVIEW) and not path.exists()
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes()==raw and tmp.stat().st_size==len(raw)>0
    tmp.replace(path)
    assert path.read_bytes()==raw

def link(path,label=None):
    return f'[{label or path.name}](<{path.as_posix()}>)'

old_doc=(CAP/'MINUTA_PESO_ESCALAR_DUAL.md').read_bytes()
new_doc=(ROOT/'MINUTA_PESO_ESCALAR_DUAL.md').read_bytes()
old_phrase='ofReal⟨Ω,DΩ⟩'.encode('utf-8')
new_phrase='ofReal(Re⟨Ω,DΩ⟩)'.encode('utf-8')
assert old_doc.count(old_phrase)==1 and old_doc.replace(old_phrase,new_phrase)==new_doc
backup_docs=[p for p in ROOT.glob('MINUTA_PESO_ESCALAR_DUAL.md.bak_*') if p.read_bytes()==old_doc]
assert backup_docs
create(CAP/'MINUTA_PESO_ESCALAR_DUAL.corrected.md',new_doc)

old_test=ast.parse((Path(V['previous_layer'])/'test_gate_extension.py').read_bytes())
new_test=ast.parse((CAP/'test_gate_extension.py').read_bytes())
control='scalar_dual_weight_does_not_discharge_canonical_trace_or_physical_obligations'
is_new=lambda n:(isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
    and isinstance(n.value.func,ast.Name) and n.value.func.id=='check' and n.value.args
    and isinstance(n.value.args[0],ast.Constant) and n.value.args[0].value==control)
assert sum(bool(is_new(n)) for n in new_test.body)==1
new_test.body=[n for n in new_test.body if not is_new(n)]
test_ast_equal=ast.dump(old_test,include_attributes=False)==ast.dump(new_test,include_attributes=False)
assert test_ast_equal
static_calls=lambda t:sum(1 for n in ast.walk(t) if isinstance(n,ast.Call)
    and isinstance(n.func,ast.Name) and n.func.id=='check' and n.args and isinstance(n.args[0],ast.Constant))
assert static_calls(old_test)==32
assert V['all_exit_zero'] and V['all_hashes_match'] and V['exact_expected_file_set']
assert V['python_ast_outside_embedded_unchanged'] and V['gate_extension_byte_identical_to_75']
assert V['audit_unexpected_axioms']=={} and V['evidence_axioms_equal_log']
assert S['new_targets_23_exact_own_auditor'] and S['new_target_axioms_match_own_auditor']
assert S['new_sources_and_roots_compile_unchanged'] and S['original_and_local_base_match_integration']
assert all(not x for x in V['six_flags'].values())
assert not V['legacy_gate_changed'] and not V['full_plan_complete'] and not V['full_monolithic_runtime_run']
assert sha((ROOT/'um.py').read_bytes())==V['um_sha256']
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in M['sources'].values())
assert all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
for name in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
             'gate_extension.py','record_scalar_weight_progress.py','verify_scalar_weight_custody.py']:
    assert sha((ROOT/name).read_bytes())==V['artifact_sha256'][name]

rows=[]
for name,match in V['source_matches'].items():
    assert match['same_except_import_paths'] and match['dev_still_frozen'] and match['embedded_matches']
    record=next(row for row in V['records'] if row['file']=='TGLExt/V350'+name+'.lean')
    rows.append(f'| V350{name} | `{match["integrated_sha256"]}` | `{record["binary_sha256"]}` |')
hash_rows='\n'.join(f'| {name} | `{V["artifact_sha256"][name]}` |' for name in
    ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])
new_compile_rows='\n'.join(f'- `{x["source"]}` — `{x["timestamp"]}`, rc0/fonte inalterada.' for x in S['integrated_streams'])
report=REVIEW/'REVIEW_SCALAR_DUAL_WEIGHT.md'
before=report.read_bytes()
backup=report.with_name(report.name+'.bak_'+STAMP)
create(backup,before)
note=f'''

---

**ADENDO FINAL — {DATE}. Revisão das quatro fontes/23 alvos encerrada; P2 documental resolvido.**

Este adendo completa a inspeção integrada que estava pendente no estrato de fontes de 06:22:32 e preserva integralmente aquele texto. O aviso de conclusão do autor já estava disponível durante a gravação do primeiro estrato; a pendência ali indicada era de minha conferência integrada, agora realizada. Nenhuma análise do escopo delimitado ficou incompleta. Não há P0/P1/P2 aberto nas fontes ou documentos examinados.

**Errata documental conferida.** Na linha 34 de `MINUTA_PESO_ESCALAR_DUAL.md`, a única diferença de bytes é `ofReal⟨Ω,DΩ⟩` → `ofReal(Re⟨Ω,DΩ⟩)`. O backup autoral {link(backup_docs[-1])} coincide integralmente com a minuta anteriormente inspecionada, SHA `{sha(old_doc)}`. A versão corrigida tem SHA lido **`{sha(new_doc)}`** e foi congelada em {link(CAP/'MINUTA_PESO_ESCALAR_DUAL.corrected.md')}. **P2 encerrado.** A correção não afeta provas, imports, binários, integração ou axiomas e não exigiu nova compilação. Recorder e verifier mantêm os hashes do estrato anterior; a substituição literal não altera a interpretação matemática da minuta.

**Snapshot integrado final efetivamente conferido.** SHA256 de `um.py` lido dos bytes: **`{V['um_sha256']}`**; corresponde a `integration.json` e `gate_tests.json`. Foram contados {V['embedded_files']} arquivos no dicionário extraído por `ast.literal_eval`, sem execução/importação do monólito. O original canônico foi novamente lido somente para hash às {S['timestamp']}: `{S['original_sha256']}`, igual à cópia-base em `fontes/` e ao pin da integração. A custódia anterior e seu snapshot `{V['previous_um_sha256']}` foram preservados.

| Evidência | Resultado | Modo de verificação |
|---|---|---|
| Quatro módulos DEV + auditor próprio | 5 processos rc0; 23 alvos no trio; 25 declarações tipadas | **Recompilação própria**, registrada no estrato anterior; não repetida |
| Build integrado | {V['integrated_modules']} registros válidos; 73 com fonte/binário idênticos ao estrato anterior; 4 módulos + 2 raízes recompilados | Leitura de registros do autor e hashes atuais de todas as 79 fontes/binários; **sem rebuild próprio das raízes** |
| Controles Python | {V['gate_checks_count']}/{V['gate_checks_count']} marcados como aprovados | Inspeção de `gate_tests.json` e do script; **não executados por mim** |
| Audit integrado | {V['audit_distinct']} declarações distintas, todas no trio permitido | Extração do stdout do Audit autoral e igualdade com `kernel_incremental_evidence.json` |
| Alvos desta etapa no Audit | Os 23 nomes/axiomas correspondem ao auditor próprio | Comparação explícita por conjuntos de axiomas, sem contar diferenças de ordenação |

As quatro fontes DEV congeladas correspondem às fontes `TGLExt/V350*.lean` apenas pela reescrita dos imports `TGLV350.*` → `TGLExt.V350*`, sem outras diferenças de bytes. As versões integradas coincidem com os respectivos valores embutidos; ambas as raízes importam os quatro módulos. Os seis registros novos declaram rc0 e fonte inalterada durante compilação, e os hashes dos .olean atuais conferem. Seus identificadores são:

{new_compile_rows}

| Módulo integrado | SHA256 fonte | SHA256 .olean do autor |
|---|---|---|
{chr(10).join(rows)}

O dicionário integrado recebeu exatamente esses quatro módulos; entre entradas anteriores, só `TGLExt.lean` e `TGL/Audit.lean` mudaram. Nenhuma entrada foi removida. O **AST Python externo ao dicionário Lean é idêntico** ao estrato custodiado anterior, e `gate_extension.py` é byte a byte idêntico, SHA `{V['artifact_sha256']['gate_extension.py']}`. O script de controles difere em AST apenas pela chamada adicional `{control}`: ela exige nove alvos deste pacote e mantém falsas as seis flags maiores. Excluída essa chamada, o AST inteiro do script coincide com o anterior. As 65 execuções registradas anteriormente não correspondem a 65 chamadas sintáticas literais: há 32 chamadas literais, com controles produzidos por laços. Por isso o campo exploratório `prior_65_controls_same_AST=false` em `supplemental_verification.json` foi uma comparação de cardinalidades inadequada do meu verificador, não uma alteração nos controles; a comparação integral de AST acima resolve essa ambiguidade sem executar testes.

Os registros finais preservam `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false` e as seis flags maiores falsas. `ScalarModularInvariance` está ausente dos registros e do dicionário inspecionado. `RegularScalarWeightCertificate`, informado como desenvolvimento posterior, também permanece fora desta revisão; nenhum de seus teoremas foi examinado ou somado às contagens.

| Relatório integrado congelado | SHA256 lido |
|---|---|
{hash_rows}

Evidências de inspeção em {link(CAP/'verification.json')} e {link(CAP/'supplemental_verification.json')}; os logs stdout/stderr integrados estão copiados sob `logs/` nessa mesma árvore. A alteração de hash documental assinalada no suplemento corresponde precisamente à errata encerrada neste adendo. A fonte histórica do inventário I/O continua `{S['runtime_inventory_source_sha256']}`, comparada à custódia histórica; não autoriza runtime da cópia atual. Recorder e verificador foram apenas lidos/analisados, permanecendo a futura custódia ato do autor após leitura do parecer.

**Conclusão final de alcance.** [REAL — Lean auditado] ν no cone positivo da mesma N é aditiva, homogênea não negativa, monótona, fiel e normal por supremos dirigidos internos; a fidelidade não conserva hipótese residual de resolvente ou finitude. O ideal complexo esquerdo explicitamente construído é fortemente denso e seus quadrados têm ν finito; os valores limitados são representados por elementos positivos da mesma M. [DERIVED] A semifinitude escalar usual segue pelo critério clássico e pela limitação uniforme explicitados no primeiro estrato. Essa ponte não foi adicionada como teorema Lean de predual/σ-fraco. Não se infere traço, identificação modular/KMS, interface geral de peso operatorial, Three Locks, física, gate ou runtime. Revisão independente delimitada **concluída**, sem ampliação a módulos posteriores.

Backup imediato deste parecer antes do adendo: {link(backup)}; SHA dos bytes preservados `{sha(before)}`. Todos os pareceres anteriores custodiados continuam intocados. Não se executaram monólito, testes autorais, recorder ou verifier; todas as escritas desta revisão ficaram em `revisao/`.
'''
after=before+note.encode('utf-8')
assert after.startswith(before) and len(after)>len(before) and backup.read_bytes()==before
tmp=report.with_name(report.name+'.tmp_'+STAMP)
with tmp.open('xb') as f:
    f.write(after)
assert tmp.read_bytes()==after and tmp.stat().st_size==len(after)
tmp.replace(report)
assert report.read_bytes()==after and report.read_bytes().startswith(backup.read_bytes())
closure={
    'timestamp':DATE, 'scope':'FOUR_DEV_MODULES_23_TARGETS_PLUS_STATIC_INTEGRATION_AND_DOCUMENTATION',
    'complete':True, 'own_compilations':len(C['records']), 'own_compilations_all_rc0':C['all_exit_zero'],
    'own_axiom_targets':len(M['declarations']), 'own_named_type_checks':len(M['all_named_declarations']),
    'findings_open':[], 'documentary_P2':'RESOLVED_BY_EXACT_LITERAL_DIFF_AND_BYTE_BACKUP',
    'minuta_old_sha256':sha(old_doc), 'minuta_current_sha256':sha(new_doc),
    'minuta_author_backup':str(backup_docs[-1]),
    'prior_test_AST_identical_after_removing_only_new_control':test_ast_equal,
    'prior_literal_check_calls':static_calls(old_test),
    'exploratory_prior_65_controls_same_AST_false_explained':'32 literal call sites generated 65 controls; exact whole AST comparison succeeds after removal of the new call',
    'integrated_records':V['integrated_modules'], 'author_controls':V['gate_checks_count'],
    'author_audit_distinct':V['audit_distinct'], 'embedded_count':V['embedded_files'],
    'working_sha256':V['um_sha256'],
    'did_rebuild_roots_or_run_author_tests':False,
    'report':str(report),'report_sha256':sha(after),'report_bytes':len(after),
    'report_previous_byte_backup':str(backup),'report_previous_sha256':sha(before),
    'report_preserves_exact_prefix':True,
}
create(CAP/'final_closure.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
