"""Inspect final author evidence only after its completion is announced. No author execution."""
from pathlib import Path
import datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
assert '--author-final-announced' in sys.argv
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'closed_tomita_batch_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
assert C['complete'] and C['all_exit_zero'] and C['exact_99_audited'] and C['all_axioms_allowed']
PRE=max(RUN.glob('source_integration_*'));V=json.loads((PRE/'verification_source.json').read_bytes())
OLD=Path(V['previous_capture']);OLDV=json.loads((OLD/'verification.json').read_bytes())
DEST=RUN/('final_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode())
def axioms(s):
    d={n:[a.strip() for a in b.split(',') if a.strip()] for n,b in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",s,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",s):d.setdefault(n,[])
    return d
files=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gns_cut_maps_custody.json','gate_extension.py','integrate_v350.py','compile_integrated.py','compile_lean.py','test_gate_extension.py','record_closed_tomita_progress.py','verify_closed_tomita_custody.py','ROTA_APOS_TOMITA_FECHADO.md','runtime_io_inventory.json']
for f in files:write(DEST/f,(ROOT/f).read_bytes())
B=json.loads((DEST/'integrated_compile.json').read_bytes());I=json.loads((DEST/'integration.json').read_bytes());G=json.loads((DEST/'gate_tests.json').read_bytes());E=json.loads((DEST/'kernel_incremental_evidence.json').read_bytes())
oldrows={r['file']:r for r in OLDV['records']};rows=[]
for r in B['records']:
    src=Path(r['source']);rel=src.relative_to(ROOT/'kernel');binary=ROOT/'build'/rel.with_suffix('.olean')
    raw=src.read_bytes();br=binary.read_bytes();o=oldrows.get(rel.as_posix())
    row={'file':rel.as_posix(),'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':r['returncode'],'source_matches_log':sha(raw)==r['sha256'],'binary_matches_log':sha(br)==r['output_sha256'],'timestamp':r['timestamp'],'source_unchanged_during_compile':r.get('source_unchanged_during_compile'),'same_source_binary_as_previous':bool(o and sha(raw)==o['source_sha256'] and sha(br)==o['binary_sha256'])}
    write(DEST/'sources'/rel,raw)
    for k in ['stdout','stderr']:
        p=Path(r[k]);pb=p.read_bytes();write(DEST/'logs'/p.name,pb);row[k+'_sha256']=sha(pb)
    lp=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'))
    jb=lp.read_bytes();write(DEST/'logs'/lp.name,jb);row['json_sha256']=sha(jb);row['log_json_matches_record']=json.loads(jb)==r
    row['warnings']=[l for l in Path(r['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in l]
    rows.append(row)
ar=next(r for r in B['records'] if Path(r['source']).relative_to(ROOT/'kernel').as_posix()=='TGL/Audit.lean')
ax=axioms(Path(ar['stdout']).read_text(encoding='utf-8')); own=C['records'][-1]['axioms']
newfiles={'TGLExt/V350'+Path(k).name for k in M['sources']}|{'TGLExt.lean','TGL/Audit.lean'}
newrows=[r for r in rows if r['file'] in newfiles]
flags=['qgf_continuous_modular_realization_constructed','qgf_unconditional_continuous_corner_proved','qgf_full_TGL_witness_constructed','gpf_H1_internal_susy_relative_gap_discharged','gpf_H2_smooth_modular_four_frame_discharged','gpf_H3_local_horizon_equilibrium_discharged']
checks={c['name']:c['passed'] for c in G['checks']};oldchecks={c['name']:c['passed'] for c in json.loads((OLD/'gate_tests.json').read_bytes())['checks']}
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),'mode':'AUTHOR_INTEGRATED_BUILD_BINARY_LOG_HASH_INSPECTION__OWN_COMPILATION_IS_DEV_15_PLUS_AUDITOR','records':rows,'incremental_build_ok':B['incremental_build_ok'],'integrated_records':len(rows),'all_rc0':all(r['returncode']==0 for r in rows),'all_source_binary_log_hashes_match':all(r['source_matches_log'] and r['binary_matches_log'] and r['log_json_matches_record'] for r in rows),'exact_expected_files':{r['file'] for r in rows}==set(I['added_kernel_files']+I['updated_kernel_files']),'new_compilation_files':sorted(newfiles),'new_compilation_count':len(newrows),'new_compiles_source_unchanged':len(newrows)==17 and all(r['source_unchanged_during_compile'] is True for r in newrows),'reused_same_source_binary_count':sum(r['same_source_binary_as_previous'] for r in rows),'roots':{r['file']:r for r in newrows if r['file'] in {'TGLExt.lean','TGL/Audit.lean'}},'audit_distinct':len(ax),'audit_trio_only':all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values()),'all_99_present_match_own_axioms':set(own)==set(M['declarations']) and all(n in ax and set(a)==set(ax[n]) for n,a in own.items()),'evidence_axioms_equal_Audit':E['axiom_report']==ax,'gate_checks':len(G['checks']),'gate_passed':G['passed'],'gate_all_passed':all(checks.values()),'gate_added_controls':sorted(set(checks)-set(oldchecks)),'old_controls_preserved':all(checks.get(n)==v for n,v in oldchecks.items()),'audit_count_matches_gate':len(ax)==G['axiom_report_entries'],'six_flags':{f:E[f] for f in flags},'full_runtime_run':G['full_monolithic_runtime_run'],'legacy_gate_changed':G['frontier']['legacy_gate_changed'],'full_plan_complete':G['frontier']['full_plan_complete'],'working_sha256':sha((ROOT/'um.py').read_bytes()),'working_hash_consistent':sha((ROOT/'um.py').read_bytes())==I['working_sha256']==G['working_um_sha256']==V['working_sha256'],'embedded_files':I['embedded_files'],'all_previously_inspected_static_artifacts_unchanged':all(sha((ROOT/f).read_bytes())==sha((PRE/f).read_bytes()) for f in files if (PRE/f).exists()),'source15_DEV_and_integrated_unchanged':all(sha(Path(r['path']).read_bytes())==r['sha256'] and sha(Path(r['integrated_path']).read_bytes())==r['integrated_sha256'] for r in M['sources'].values()),'previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items()),'artifact_sha256':{p.name:sha(p.read_bytes()) for p in DEST.iterdir() if p.is_file()},'author_scripts_executed':False,'roots_recompiled_by_reviewer':False}
save(DEST/'verification.json',data);save(DEST/'axioms.json',ax)
print(json.dumps({k:v for k,v in data.items() if k not in ['records','roots','artifact_sha256','new_compilation_files']},ensure_ascii=False,indent=2))
