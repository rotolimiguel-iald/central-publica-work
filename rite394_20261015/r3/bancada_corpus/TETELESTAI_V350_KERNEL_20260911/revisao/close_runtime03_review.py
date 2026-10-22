"""Read existing Run03 artifacts only; never import or execute author code."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
RUN = ROOT / 'r'
ARCHIVE = RUN / 'completed_attempt_03'
NOW = datetime.now().astimezone()
STAMP = NOW.strftime('%Y%m%d_%H%M%S_%f')
OUT = ROOT / 'revisao' / ('runtime03_final_review_' + STAMP)
OUT.mkdir()
PINS = {}
CHECKS = {}
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(p):
    with p.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def pin(label, p):
    result = dict(path=str(p), bytes=p.stat().st_size, sha256=digest(p))
    PINS[label] = result
    return result

def read(label, p):
    raw = p.read_bytes()
    assert raw == p.read_bytes(), ('changed_during_read', p)
    PINS[label] = dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    return json.loads(raw)

def check(name, condition):
    CHECKS[name] = bool(condition)

def atomic(path, raw):
    tmp = path.with_name(path.name + '.tmp_' + STAMP)
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, path)

author = read('author_archive_verification', ARCHIVE/'verification.json')
data = read('final_json', ARCHIVE/'um_absoluto.json')
seal = read('final_seal', ARCHIVE/'um_absoluto_selo.json')
proof = read('final_proof_manifest', ARCHIVE/'tgl_kernel_proof_manifest.json')
state = read('process', ARCHIVE/'runtime_process_03.json')
integration = read('reader_integration', ARCHIVE/'reader_integration_manifest.json')
baseline = read('baseline_seal', ROOT/'fontes/um_absoluto_selo.json')
oldproof = read('run02_proof', RUN/'completed_attempt_02/tgl_kernel_proof_manifest.json')
formal = read('inherited_formal_evidence', ROOT/'revisao/full_runtime_formal_stage_20260913_093418_886098/evidence.json')
prior = read('inherited_round02_evidence', ROOT/'revisao/runtime_seals_preliminary_20260913_100700_656494/final_inspection.json')
read('active_contract', ROOT/'CONTRATO_ATIVO_GATE_V350.json')
for name in ['REVIEW_FULL_RUNTIME_FORMAL_STAGE.md', 'REVIEW_FULL_RUNTIME_ROUND02_AND_REGRESSIONS.md', 'REVIEW_READER_CORRECTION_V2.md']:
    pin(name, ROOT/'revisao'/name)
pin('inherited_reader_partial', ROOT/'revisao/runtime03_readers_partial_20260913_111801_054664/evidence.json')
pin('author_verifier_static_only', ROOT/'verify_and_archive_runtime03.py')

programs = [pin(label, p)['sha256'] for label,p in [
    ('root_program', ROOT/'um.py'), ('runtime_program', RUN/'um.py'),
    ('archived_program', ARCHIVE/'um.py'), ('approved_v2', ROOT/'reader_correction_v2/um.py')]]
check('same_approved_v2_source', len(set(programs + [state['working_sha256'], state['program_sha256_after'], integration['working_sha256']])) == 1)
check('v2_review_pin_preserved', integration['review_sha256'] == PINS['REVIEW_READER_CORRECTION_V2.md']['sha256'])
check('process_completed_rc0', state['status']=='PROCESS_EXITED' and state['returncode']==0 and state['full_runtime_completed'] is True)
check('archive_process_matches_live', digest(ARCHIVE/'runtime_process_03.json') == digest(RUN/'runtime_process_03.json'))
archive_rows = []
for name, expected in author['archive_files'].items():
    actual = pin('archive:'+name, ARCHIVE/name)
    archive_rows.append(dict(name=name, matches=actual['sha256']==expected['sha256'] and actual['bytes']==expected['bytes']))
check('archived_bytes_match_author_manifest', all(r['matches'] for r in archive_rows))

seal_rows = []
for name, expected in seal['sha256'].items():
    archived = digest(ARCHIVE/name)
    live = digest(RUN/name)
    seal_rows.append(dict(name=name, expected=expected, archive_sha256=archived, live_sha256=live, matches=expected==archived==live))
check('thirteen_sealed_hashes', len(seal_rows)==13 and all(r['matches'] for r in seal_rows))
source_rows = []
for name, expected in proof['formal_files_sha256'].items():
    actual = digest(RUN/'tgl_kernel'/name)
    source_rows.append(dict(name=name, expected=expected, actual=actual, matches=expected==actual))
check('922_restored_sources', len(source_rows)==922 and all(r['matches'] for r in source_rows))
check('inherited_embedded_mapping_unchanged', proof['formal_files_sha256']==oldproof['formal_files_sha256']==data['core']['kernel_formalization']['formal_files_sha256'])

def axmap(text):
    result, conflicts, messages = {}, [], 0
    for m in re.finditer(r"'([\w.']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", text):
        messages += 1
        values = [v.strip() for v in (m[2] or '').split(',') if v.strip()]
        if m[1] in result and set(result[m[1]]) != set(values):
            conflicts.append(m[1])
        result[m[1]] = values
    assert not conflicts, conflicts
    return result, messages

captures, parsed, capture_rows = {}, {}, []
for stage in ['', '_selftest_tampered', '_selftest_restored']:
    for kind in ['build', 'audit']:
        name = f'tgl_kernel_{kind}_capture{stage}.txt'
        raw = (ARCHIVE/name).read_bytes()
        text = raw.decode('utf-8-sig')
        rc = int(re.search(r'^# returncode: (-?\d+)', text, re.M)[1])
        mapping, messages = axmap(text)
        captures[(stage,kind)] = text
        parsed[(stage,kind)] = mapping
        capture_rows.append(dict(name=name, returncode=rc, header=text.split('--- STDOUT ---')[0], messages=messages, unique=len(mapping), sha256=hashlib.sha256(raw).hexdigest()))
check('six_capture_returncodes_zero', all(r['returncode']==0 for r in capture_rows))
build = parsed['','build']; audit = parsed['','audit']
check('principal_cross_stream_no_conflicts', all(build[n]==audit[n] for n in build.keys()&audit.keys()))
union = {**build, **audit}
restored = {**parsed['_selftest_restored','build'], **parsed['_selftest_restored','audit']}
kf = data['core']['kernel_formalization']
check('7133_audit_matches_inherited_formal', len(audit)==7133 and audit==formal['axiom_report'])
check('7985_union_matches_json_manifest', len(union)==7985 and union==proof['axiom_report']==kf['axiom_report'])
check('restored_union_same', restored==union and parsed['_selftest_restored','audit']==audit)
check('all_union_axioms_permitted', all(set(v)<=ALLOWED for v in union.values()))
tampered = parsed['_selftest_tampered','audit']
forbidden = {n:v for n,v in tampered.items() if not set(v)<=ALLOWED}
check('tamper_detected_with_sorryAx', bool(forbidden) and any('sorryAx' in v for v in forbidden.values()))
stdout = (ARCHIVE/'runtime_stdout_03.txt').read_text(encoding='utf-8')
check('selftest_actual_fail_and_recovery_messages',
      'com sorry injetado : verdict=TGL_KERNEL_FORMALIZATION_FAILED ; sorryAx_absent=False' in stdout and
      'restaurado da fonte: verdict=TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED ; all_verified=True' in stdout and
      'FAIL_CLOSED_SELFTEST_PASSED' in stdout)
check('selftest_seal_and_zero_checkpoints', seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED' and seal['rite_checkpoints']['switch_on'] is False and seal['rite_checkpoints']['reused']==0)
check('formal_status_green', all(kf[k] is True for k in ['all_verified','formal_release_ready','sorryAx_absent','lake_build_ok','audit_file_ok']))
gate = {k:v for k,v in kf.items() if k.startswith(('qgc_','qgp_'))}
check('eleven_gate_inputs_true', len(gate)==11 and all(v is True for v in gate.values()))
gate_rows = []
for row in prior['gate_entries']:
    flag, name = row['flag'], row['declaration']
    group = 'formal_flags' if flag.startswith('qgc_') else 'physics_flags'
    gate_rows.append(dict(flag=flag, declaration=name, axioms=union.get(name), present=name in union,
                          kernel_value=kf.get(flag), consumed_value=data['core']['qg_closure'][group].get(flag[4:])))
check('eleven_consumed_named_providers', len(gate_rows)==11 and all(r['present'] and r['kernel_value'] is True and r['consumed_value'] is True and set(r['axioms'])<=ALLOWED for r in gate_rows))
check('terminal_seal_json_stdout_consistent', seal['qg_closure_verdict']==data['core']['qg_closure']['gate']['verdict'] and seal['qg_closure_verdict'] in stdout)
check('result_hash_consistency_only', seal['result_hash']==data['result_hash_before_external_comparison'])

readers = {name:data['core'][name] for name in ['the_assembly_and_the_single_debt','the_atlas_and_the_index']}
check('both_readers_final_pass', all(v['all_verified'] is True and all(c[1] is True for c in v['checks']) for v in readers.values()))
check('reader_counts_correct', readers['the_assembly_and_the_single_debt']['clauses_proved']==8 and readers['the_assembly_and_the_single_debt']['flag_lit'] is True and readers['the_atlas_and_the_index']['n_atlas']==6 and readers['the_atlas_and_the_index']['n_indice']==6)
input_rows=[]
for entry in integration['files']:
    p=Path(entry['runtime_destination']); actual=digest(p)
    input_rows.append(dict(relative_path=entry['relative_to_runtime'], expected=entry['sha256'], actual=actual, bytes=p.stat().st_size, matches=actual==entry['sha256'] and p.stat().st_size==entry['bytes']))
check('four_installed_inputs_pinned', len(input_rows)==4 and all(i['matches'] for i in input_rows))
results = json.loads((RUN/'results.json').read_bytes())
consumption = dict(stokes_doc_sha256=data['core']['stokes_contour']['doc_sha256'], fifth_entry=data['core']['evidence_audit']['values']['fifth_entry_live'],
    streamed_galaxies=data['core']['void_density_power']['n_galaxies_streamed'], lenses=data['core']['void_floor_v2']['n_lenses'], shear_voids=data['core']['void_shear_v2']['n_voids'])
check('four_input_consumption_outputs', consumption['stokes_doc_sha256']==digest(RUN/'STOKES_A_Prova_do_Contorno.md') and consumption['fifth_entry']==results['multiprobe_D1_D9']['D10']['beta_acoustic_crosslock'] and consumption['streamed_galaxies']>0 and consumption['lenses']['REVOLVER']>0 and consumption['lenses']['total']==1049 and consumption['shear_voids']==700)
aux_names=['arc_consolidation','closure_roadmap','evidence_audit','love_reading','stokes_contour','void_floor_final','void_floor_v2','void_density_opening','void_density_power','void_density_v41','void_shear_v2']
aux={n:dict(all_verified=data['core'][n]['all_verified'],verdict=data['core'][n]['verdict']) for n in aux_names}
check('eleven_preparation_regressions_resolved', all(v['all_verified'] is True for v in aux.values()))
check('not_sealed_exact_baseline_four_plus_six', seal['not_sealed_this_run']==baseline['not_sealed_this_run'] and len(seal['not_sealed_this_run']['formais'])==4 and len(seal['not_sealed_this_run']['recusas_de_dado'])==6)

failures=[k for k,v in CHECKS.items() if not v]
evidence=dict(timestamp=NOW.isoformat(), status='ROUND03_REVIEW_COMPLETE' if not failures else 'REVIEW_FAILURE_VISIBLE', checks=CHECKS, failures=failures, pins=PINS,
    process=state, archive_file_checks=archive_rows, seal_hashes=seal_rows, formal_files=source_rows, captures=capture_rows,
    axioms=dict(audit_unique=len(audit), union_unique=len(union), build_only=len(set(union)-set(audit)), no_axioms_audit=sum(not v for v in audit.values()), apostrophe_names=[n for n in audit if "'" in n], tampered_forbidden=forbidden, principal_map=union),
    gate=gate_rows, terminal=seal['qg_closure_verdict'], readers=readers, inputs=input_rows, consumption=consumption, auxiliary_results=aux, not_sealed=seal['not_sealed_this_run'],
    checkpoints=seal['rite_checkpoints'], full_project_complete=False, memories_or_final_custody_updated_by_reviewer=False,
    limitations=['No monolith, author helper, build, or tests executed by reviewer in this closeout.', 'Prior formal/type and V2 guard/test reviews inherited with current source and evidence pins.', 'Runtime science not independently recomputed.', 'result_hash consistency checked; not independently reconstructed.', 'Final memory/custody update remains with author.'])
atomic(OUT/'evidence.json',(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
if failures:
    print(json.dumps(dict(status='FAILURES',failures=failures,evidence=str(OUT/'evidence.json')),ensure_ascii=False)); sys.exit(1)
report=f'''# Fecho delimitado — Run03

{NOW.isoformat()}

**[REAL] Revisão final da rodada concluída: nenhum P0–P2 pendente no escopo examinado.** As regressões dos dois leitores e da preparação de insumos identificadas na Run02 estão resolvidas na saída executada da Run03. Memória e custódia final ainda serão registradas pelo autor; este parecer não declara essa etapa documental concluída.

- Registro autoral de processo: **rc0**, término `{state['finished']}`, duração **{state['elapsed_seconds']:.5f} s**. ROOT, runtime, arquivo da rodada e V2 aprovada têm o mesmo SHA256 `{programs[0]}`.
- **13/13 hashes do selo** relidos na cópia arquivada e no runtime; **922/922 fontes restauradas** relidas e iguais ao manifesto. O mapa de fontes permanece igual ao da revisão formal anterior, que conferiu os embutidos. Artefatos arquivados conferidos contra seus pins.
- Streams atuais reparseados, sem compilação: **7.133** termos únicos no Audit e **7.985** na união build+Audit, exatamente o mapa do JSON e proof_manifest; **852** são adicionais do build. Preservados os **50** termos sem axiomas e nomes com apóstrofo. Axiomas da união restritos a `propext`, `Classical.choice`, `Quot.sound`.
- **11/11 entradas qgc/qgp** verdadeiras e consumidas, com provedores nomeados presentes no mapa auditado. Terminal consistente entre stdout, JSON e selo. Reutilizada a revisão dos tipos/contratos e das guardas V2; booleanos isolados não foram tratados como prova, nem foram acrescentadas exigências original-S/KMS/flags ao gate principal.
- **FAIL_CLOSED_SELFTEST_PASSED**: capturas tampered e restored têm rc0 de Lean, mas a primeira contém `sorryAx` e é recusada pelo programa (`FAILED`, `sorryAx_absent=False`). A restauração retorna `all_verified=True`, recupera exatamente a união de axiomas aprovada e as 922 fontes. Checkpoint desligado, **0 ritos reaproveitados**. Rc0 do compilador durante a adulteração não equivale a aceite formal.
- Quatro insumos instalados com hashes conferidos; consumo visível no documento Stokes, leitura negativa preservada `beta_acoustic_crosslock={consumption['fifth_entry']}`, **{consumption['streamed_galaxies']:,}** galáxias lidas, **1049** lentes (611 REVOLVER) e **700** vazios no shear. Não houve recálculo científico independente neste fecho.
- Montagem **8/8**, bandeira acesa; Atlas/índice **6+6**. Ambos `all_verified=True` no JSON regravado. Ausência anterior à segunda gravação e KeyError da observação prematura não são regressões do programa.
- `not_sealed_this_run` é **idêntico à baseline: quatro entradas formais e seis recusas de dado**, sem novas entradas nem remoção das anteriores. As onze ocorrências ligadas aos insumos voltaram a passar sua verificação; vereditos inconclusivos, underpowered e signal-not-opened permanecem explícitos. Isso não transforma `NOT_FALSIFIED` em confirmação.

**Proveniência e limites.** Herdadas as revisões formal, Run02, V2 e parcial dos leitores, todas pinadas na evidência nova. Neste fecho executei somente meu script de leitura/comparação. Não executei/importei monólito, compilador, testes ou helper autoral, nem acessei sessão de execução. O arquivamento autoral existe e foi conferido; a futura memória/custódia final não foi executada por mim. Conferi consistência de `result_hash`, sem reconstruir independentemente seu algoritmo. Nenhum parecer anterior foi alterado e nenhuma nova prova foi exigida.

Evidência própria: [{OUT.name}/evidence.json](<{(OUT/'evidence.json').as_posix()}>).

Pins finais: JSON `{PINS['final_json']['sha256']}`; selo `{PINS['final_seal']['sha256']}`; proof_manifest `{PINS['final_proof_manifest']['sha256']}`; arquivo/verificação autoral `{PINS['author_archive_verification']['sha256']}`. Todos lidos dos bytes.
'''
report_path=ROOT/'revisao/REVIEW_FULL_RUNTIME_ROUND03.md'
if report_path.exists():
    previous=report_path.read_bytes(); backup=report_path.with_name(report_path.name+'.bak_'+STAMP)
    with backup.open('xb') as stream: stream.write(previous)
    assert backup.read_bytes()==previous
    report_raw=previous+b'\n\n'+report.encode('utf-8')
else: report_raw=report.encode('utf-8')
atomic(report_path,report_raw)
atomic(OUT/'report_pin.json',(json.dumps(dict(path=str(report_path),sha256=digest(report_path),evidence_sha256=digest(OUT/'evidence.json'),script_sha256=digest(Path(__file__))),indent=2)+'\n').encode('utf-8'))
print(json.dumps(dict(status=evidence['status'],checks=len(CHECKS),failures=failures,report=str(report_path),report_sha256=digest(report_path),evidence=str(OUT/'evidence.json')),ensure_ascii=False,indent=2))
