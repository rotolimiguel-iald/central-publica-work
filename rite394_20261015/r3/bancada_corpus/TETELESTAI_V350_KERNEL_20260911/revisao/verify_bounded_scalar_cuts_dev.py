"""Record measured hashes and audit coverage for the three bounded scalar cut DEV modules."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/'bounded_scalar_cuts_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
D=json.loads((RUN/'author_bounded_scalar_cuts_draft_status.json').read_bytes())
K=json.loads((RUN/'gns_normality_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert C['complete'] and C['all_exit_zero'] and C['full_audit_names_exact'] and C['all_axioms_allowed']
own={r['module']:r for r in C['records']};records={}
for rel,r in M['sources'].items():
    name=Path(rel).stem;row=D['records'][name];log=Path(row['log'])
    author=json.loads((RUN/'author_logs'/log.name).read_bytes())
    authorbin=ROOT/'build'/Path(rel).with_suffix('.olean');ownbin=RUN/'build'/Path(rel).with_suffix('.olean')
    records[name]={
        'source_sha256':sha(Path(r['path'])),
        'source_equals_status_and_frozen':sha(Path(r['path']))==row['sha256']==r['sha256']==sha(Path(r['snapshot'])),
        'author_log':str(log),'author_log_sha256':sha(log),
        'author_log_identical_to_frozen':log.read_bytes()==(RUN/'author_logs'/log.name).read_bytes(),
        'author_log_rc0_source_unchanged':author['returncode']==0 and author['source_unchanged_during_compile'] is True,
        'author_binary_sha256':sha(authorbin),
        'author_binary_equals_status_and_log':sha(authorbin)==row['output_sha256']==author['output_sha256'],
        'own_binary_sha256':sha(ownbin),
        'own_binary_equals_compilation_record':sha(ownbin)==own[rel]['output_sha256'],
        'own_binary_equals_author':sha(ownbin)==sha(authorbin),
        'target_names_exact':set(own[rel]['axioms'])==set(r['declarations']),
        'author_stream_sha256':{kind:sha(Path(author[kind])) for kind in ['stdout','stderr']},
        'author_streams_frozen_equal':all(Path(author[kind]).read_bytes()==(RUN/'author_logs'/Path(author[kind]).name).read_bytes() for kind in ['stdout','stderr']),
        'own_stream_sha256':{kind:sha(Path(own[rel][kind])) for kind in ['stdout','stderr']},
    }
audit=own['BoundedScalarCutsAudit.lean'];ax=audit['axioms']
result={
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'mode':'INDEPENDENT_THREE_DEV_MODULES_AND_11_TARGET_OWN_AUDIT',
    'records':records,'source_count':len(records),'audited_targets':len(ax),
    'type_checks':len(M['all_named_declarations']),
    'four_compiles_rc0':len(C['records'])==4 and all(r['returncode']==0 for r in C['records']),
    'exact_target_set':set(ax)==set(D['targets'])==set(M['declarations']),
    'axioms_match_status':all(set(ax[n])==set(D['targets'][n]) for n in ax),
    'all_axioms_allowed':all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()),
    'own_auditor_source_sha256':audit['source_sha256'],'own_auditor_binary_sha256':audit['output_sha256'],
    'own_auditor_stdout_sha256':sha(Path(audit['stdout'])),
    'project_dependency_count':len(M['dependencies']),
    'dependency_comment_only_exceptions':{n:{k:r.get(k) for k in ['source_sha256','live_source_sha256','sha256','previously_reviewed_comment_only_erratum']} for n,r in M['dependencies'].items() if not r['live_source_matches_frozen']},
    'dependencies_frozen_preserved':C['dependencies_unchanged'],
    'previous_certificate_not_imported':'TGLV350.RegularScalarWeightCertificate' not in M['dependencies'],
    'author_project_builds_excluded':str(ROOT/'build') not in M['lean_path'] and str(ROOT/'kernel') not in M['lean_path'],
    'status_sha256':sha(RUN/'author_bounded_scalar_cuts_draft_status.json'),
    'status_unchanged':sha(ROOT/'bounded_scalar_cuts_draft_status.json')==M['draft_status_sha256'],
    'route_sha256':sha(ROOT/'ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md'),
    'route_equals_status_and_frozen':sha(ROOT/'ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md')==D['draft_note_sha256']==sha(RUN/'ROTA_FUNCIONAIS_LIMITADOS_RASCUNHO.md'),
    'custody_sha256':sha(ROOT/'gns_normality_custody.json'),
    'custody_equals_status':sha(ROOT/'gns_normality_custody.json')==D['integrated_custody_sha256'],
    'previous_gns_normality_review_sha256':sha(REVIEW/'REVIEW_GNS_NORMALITY.md'),
    'previous_gns_normality_review_equals_custody':sha(REVIEW/'REVIEW_GNS_NORMALITY.md')==K['review_sha256'],
    'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),
    'historical_custody_counts':{k:K[k] for k in ['integrated_records','controls','audit_declarations','working_sha256']},
    'new_integration_inspected':False,'author_monolith_recorders_tests_executed':False,
}
assert result['exact_target_set'] and result['axioms_match_status']
raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');p=RUN/'verification_dev.json';assert not p.exists()
tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
