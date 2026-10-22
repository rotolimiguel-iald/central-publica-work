"""Measure own compilation, author pins, and inherited provenance; no author execution."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'gns_representation_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
PREV=Path(M['previous_run']);PM=json.loads((PREV/'manifest.json').read_bytes());PC=json.loads((PREV/'compilation.json').read_bytes())
D=json.loads((RUN/'author_gns_representation_draft_status.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for c in [C,PC]:assert all(c[k] for k in ['complete','all_exit_zero','full_audit_names_exact','all_axioms_allowed','sources_unchanged','dependencies_unchanged','previous_reviews_preserved'])
own={r['module']:r for r in PC['records']+C['records']};rows={}
for rel,r in M['sources'].items():
    name=Path(rel).stem;entry=D['records'][name];log=Path(entry['log']);a=json.loads(log.read_bytes())
    folder=RUN if name=='ScalarGNSRepresentation' else PREV
    bin=folder/'build'/Path(rel).with_suffix('.olean');authorbin=ROOT/'build'/Path(rel).with_suffix('.olean')
    rows[name]={'source_sha256':sha(Path(r['path'])),'source_equals_frozen_status_log':sha(Path(r['path']))==sha(Path(r['snapshot']))==r['sha256']==entry['sha256']==a['sha256'],
        'author_log':str(log),'author_log_sha256':sha(log),'author_log_frozen_identical':log.read_bytes()==(folder/'author_logs'/log.name).read_bytes(),
        'author_rc0_source_unchanged':a['returncode']==0 and a['source_unchanged_during_compile'] is True,
        'author_binary_sha256':sha(authorbin),'author_binary_matches_log_status':sha(authorbin)==entry['output_sha256']==a['output_sha256'],
        'own_binary_sha256':sha(bin),'own_binary_matches_compilation':sha(bin)==own[rel]['output_sha256'],'own_binary_equals_author':sha(bin)==sha(authorbin),
        'targets_exact':set(own[rel]['axioms'])==set(r['declarations']),
        'streams':{kind:{'author_sha256':sha(Path(a[kind])),'author_equals_frozen':Path(a[kind]).read_bytes()==(folder/'author_logs'/Path(a[kind]).name).read_bytes(),'own_sha256':sha(Path(own[rel][kind]))} for kind in ['stdout','stderr']},
        'own_warnings':[l for l in Path(own[rel]['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in l]}
audit=C['records'][-1];ax=audit['axioms']
assert set(ax)==set(M['declarations']) and len(ax)==21
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'FIVE_NEW_MODULES_RECOMPILED_AND_CUMULATIVE_21_TARGET_AUDIT','records':rows,
    'five_new_modules_rc0':all(own[r]['returncode']==0 for r in M['sources']),
    'successful_compiler_processes_this_stage':len(PC['records'])+len(C['records']),
    'own_auditors_rc0':PC['records'][-1]['returncode']==0 and audit['returncode']==0,
    'exact_21_targets':len(ax)==21 and set(ax)==set(M['declarations']),'named_types_checked':len(M['all_named_declarations']),
    'axioms_match_author_status':all(set(v)==set(D['targets'][n]) for n,v in ax.items()),'axioms_allowed':all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()),
    'own_auditor_source_sha256':audit['source_sha256'],'own_auditor_binary_sha256':audit['output_sha256'],'own_auditor_stdout_sha256':sha(Path(audit['stdout'])),
    'prior_14_targets_not_recompiled':True,'prior_orbit_run':M['prior_orbit_run'],
    'inherited_dependencies_first_four':len(PM['dependencies']),'inherited_modules_fifth':M['inherited_project_module_count'],
    'frozen_dependency_pins_preserved':all(sha(Path(p))==h for p,h in M['frozen_dependency_pins'].items()),
    'comment_only_dependency_exceptions':{n:{k:r.get(k) for k in ['source_sha256','live_source_sha256','sha256','previously_reviewed_comment_only_erratum']} for n,r in PM['dependencies'].items() if not r['live_source_matches_frozen']},
    'RegularScalarWeightCertificate_not_imported':'TGLV350.RegularScalarWeightCertificate' not in PM['dependencies'],
    'author_project_builds_excluded':str(ROOT/'build') not in M['lean_path'] and str(ROOT/'kernel') not in M['lean_path'],
    'lean_path':M['lean_path'],'compiler_sha256':M['compiler_sha256'],'status_sha256':sha(RUN/'author_gns_representation_draft_status.json'),
    'status_unchanged':sha(ROOT/'gns_representation_draft_status.json')==M['draft_status_sha256'],
    'documents_current_sha256':{n:sha(ROOT/n) for n in M['documents']},
    'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),
    'sealed_orbit_review_sha256':sha(R/'REVIEW_GNS_ORBIT.md'),
    'own_failed_import_layout_attempt':str(R/'gns_representation5_independent_20260912_073201_614035'),
    'failed_attempt_is_preserved_and_not_counted_as_success':True,'author_programs_executed':False}
assert all(result[k] for k in ['five_new_modules_rc0','own_auditors_rc0','exact_21_targets','axioms_match_author_status','axioms_allowed','frozen_dependency_pins_preserved','author_project_builds_excluded','previous_reviews_preserved'])
p=RUN/'verification_dev.json';assert not p.exists();b=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');tmp=p.with_suffix('.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.replace(p)
print(json.dumps({k:v for k,v in result.items() if k not in ['records','lean_path']},ensure_ascii=False,indent=2))
print(json.dumps({'binary_equalities':{n:r['own_binary_equals_author'] for n,r in rows.items()},'warnings':{n:r['own_warnings'] for n,r in rows.items()}},ensure_ascii=False))
