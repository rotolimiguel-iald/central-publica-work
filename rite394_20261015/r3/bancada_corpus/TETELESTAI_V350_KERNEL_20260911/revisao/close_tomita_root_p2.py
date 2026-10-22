"""Inspect only the custody P2 correction and append with an immediate byte backup."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
OLD=max(p for p in RUN.glob('final_integrated_*') if (p/'review_closure.json').exists())
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');DEST=RUN/('custody_p2_'+stamp)
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def link(label,p,line=None):return '['+label+'](<' +Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
V=load(OLD/'verification.json');CL=load(OLD/'review_closure.json')
review=REV/'REVIEW_SCALAR_TOMITA_ROOT_INTEGRATED.md';before=review.read_bytes()
assert sha(before)==CL['review_sha256'] and b'TOMITA_ROOT_P2_RESOLVED' not in before
files=['verify_tomita_root_custody.py','test_root_custody_binary_check.py','root_custody_binary_check.json','record_tomita_root_progress.py']
pins={}
for n in files:
    raw=(ROOT/n).read_bytes();write(DEST/n,raw);pins[n]=sha(raw)
    if n.endswith('.py'):ast.parse(raw)
for n in ['verify_tomita_root_custody.py','record_tomita_root_progress.py']:
    diff='\n'.join(difflib.unified_diff((OLD/n).read_text(encoding='utf-8').splitlines(),(DEST/n).read_text(encoding='utf-8').splitlines(),fromfile='prior/'+n,tofile='corrected/'+n,lineterm=''))
    write(DEST/(n+'.diff.txt'),diff.encode('utf-8'))
current=ast.parse((DEST/'record_tomita_root_progress.py').read_bytes());old=ast.parse((OLD/'record_tomita_root_progress.py').read_bytes())
assign=next(n for n in current.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='artifacts' for t in n.targets))
added=['test_root_custody_binary_check.py','root_custody_binary_check.json']
assert [x.value for x in assign.value.elts[-2:]]==added
assign.value.elts=assign.value.elts[:-2]
assert ast.dump(current,include_attributes=False)==ast.dump(old,include_attributes=False)
report=load(DEST/'root_custody_binary_check.json')
assert report['verifier_sha256']==pins['verify_tomita_root_custody.py']
assert report['actual_source_binary_pairs_verified']==130
assert all(report[k] is True for k in ['isolated_copy_positive_control','modified_binary_rejected','restored_copy_accepted','compiled_original_binary_unchanged'])
# Re-read report hashes, not the 130 compiled binaries; do not rerun author tests.
for n in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    assert hf(ROOT/n)==V['artifacts'][n]
B=load(ROOT/'integrated_compile.json');assert len(B['records'])==130
row=next(r for r in B['records'] if r['source'].endswith('V350PartialSquareEnergy.lean'))
source=Path(row['source']);binary=ROOT/'build'/source.relative_to(ROOT/'kernel').with_suffix('.olean')
fixture=Path(report['fixture']).resolve();assert fixture.is_relative_to(ROOT/'tests')
assert hf(source)==hf(fixture/'kernel/Control.lean')==row['sha256']
assert hf(binary)==hf(fixture/'build/Control.olean')==row['output_sha256']
assert hf(REV/'REVIEW_SCALAR_TOMITA_ROOT.md')==CL['DEV_review_preserved_sha256']
assert not (ROOT/'tomita_root_custody.json').exists() and not (ROOT/'tomita_root_custody_verification.json').exists()
evidence={'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'P2 correction only; static source/AST/report/hash inspection',
 'verifier_function_lines':[12,18],'all_records_loop_lines':[32,36],'recorder_only_two_added_artifact_pins':True,
 'author_report_matches_current_verifier_hash':True,'author_report_count':130,'author_report_negative_control_rejected':True,
 'restored_fixture_source_binary_equal_pinned_reference':True,'author_test_executed_by_reviewer':False,
 'author_rc0':'reported by author; JSON contains no exit-code field; its result is written only after assertions pass',
 'integration_evidence_hashes_unchanged':True,'new_Lean_compilations':0,'mathematics_reexamined':False,
 'own_read_of_130_binaries_repeated':False,'custody_not_executed_at_capture':True,
 'P2_resolved':True,'new_findings':[],'pins':pins,'reference_source_sha256':row['sha256'],'reference_binary_sha256':row['output_sha256']}
save(DEST/'verification.json',evidence)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
table='\n'.join('| '+link(n,ROOT/n)+' | `'+h+'` |' for n,h in pins.items())
addition=f'''

## Adendo — {now} — P2 encerrado

TOMITA_ROOT_P2_RESOLVED

**[REAL — inspeção documental/AST e hashes] O único P2 do estrato anterior está resolvido na versão abaixo.** O diagnóstico anterior e seus pins permanecem preservados como histórico da versão que não relia os binários. Não há achado P0–P2 pendente neste escopo delimitado.

Li integralmente o verifier corrigido (60 linhas), o teste (54 linhas) e seu relatório. Em {link('verify_tomita_root_custody.py:12',ROOT/'verify_tomita_root_custody.py',12)}–18, `verify_compile_record` resolve e restringe a fonte à árvore `kernel`, deriva o `.olean` correspondente em `build`, exige `returncode == 0` e `output_exists`, relê o hash da fonte e exige arquivo binário existente com hash igual a `output_sha256`. Nas linhas 32–36, o verifier exige `incremental_build_ok`, confronta a quantidade de registros com a custódia e chama a função para **cada** registro. O hash de `integrated_compile.json` continua sendo verificado pelo loop anterior de artefatos. Assim, a alteração posterior de `.olean` descrita no P2 agora falha na própria verificação posterior.

O teste autoral extrai por AST as funções reais `sha` e `verify_compile_record`, sem executar o corpo do verifier; percorre os 130 registros e aplica à cópia isolada o ciclo íntegro → alterado → restaurado. O JSON pinado ao verifier atual registra aceitação, rejeição e nova aceitação. Conferi os bytes finais restaurados da fixture contra a fonte/binário integrados de `V350PartialSquareEnergy` e seus pins anteriores. **Não reexecutei o teste nem repeti a leitura dos 130 binários**; a rejeição intermediária é evidência autoral relida, apoiada pelo fluxo concreto da função. O rc0 foi informado pelo autor; o JSON não contém campo de exit code e é gravado pelo teste somente após suas asserções.

O diff do recorder acrescenta somente os pins de `test_root_custody_binary_check.py` e `root_custody_binary_check.json`: retiradas essas duas entradas, seu AST coincide com a versão já revisada. Os hashes dos quatro relatórios de integração continuam iguais aos do parecer: 130 registros, 78 controles e 6.539 Audit permanecem o mesmo estrato, sem novos resultados matemáticos. Recorder/custódia/verifier posterior ainda não executados na captura; esta inspeção não antecipa sua execução.

| Versão corrigida / evidência lida | SHA256 |
|---|---|
{table}

Evidência própria, diffs e cópias dos quatro arquivos: {link('verification.json',DEST/'verification.json')}. O parecer anterior a este adendo tinha SHA `{sha(before)}`; seu backup imediato em bytes está em {link('backup do estrato anterior',review.with_name(review.name+'.bak_'+stamp))}. A escrita preserva esse conteúdo como prefixo integral. O parecer DEV e o reexame custodiados permanecem intocados. Mantidos todos os limites anteriores: nenhuma nova compilação, exame matemático, promoção de gate ou certificação dos DEV posteriores. **Encerrada a correção e a revisão integrada delimitada, agora sem P0–P2 pendentes.**
'''
raw=before+addition.encode('utf-8');backup=review.with_name(review.name+'.bak_'+stamp)
assert review.read_bytes()==before
with backup.open('xb') as f:f.write(before)
assert backup.read_bytes()==before
temp=review.with_name(review.name+'.tmp_'+stamp)
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw and review.read_bytes()==before
temp.replace(review)
assert review.read_bytes()==raw and raw.startswith(backup.read_bytes()) and len(raw)>len(before)
closure={'timestamp':now,'review':str(review),'review_sha256':hf(review),'bytes':len(raw),'lines':len(raw.splitlines()),
 'backup':str(backup),'backup_sha256':hf(backup),'exact_prefix_preserved':True,'P2_resolved':True,
 'verification_path':str(DEST/'verification.json'),'verification_sha256':hf(DEST/'verification.json')}
save(DEST/'closure.json',closure);print(json.dumps(closure,ensure_ascii=False,indent=2))
