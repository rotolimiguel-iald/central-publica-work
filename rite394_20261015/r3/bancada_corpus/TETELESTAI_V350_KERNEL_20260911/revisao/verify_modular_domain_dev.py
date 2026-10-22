"""Verify only frozen DEV artifacts and own compilation, without author execution."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/'modular_domain_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
D=json.loads((RUN/'author_modular_domain_draft_status.json').read_bytes())
K=json.loads((RUN/'scalar_weight_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert C['complete'] and C['all_exit_zero'] and C['full_audit_names_exact'] and C['all_axioms_allowed']
own={r['module']:r for r in C['records']}
records={}
for rel,r in M['sources'].items():
    name=Path(rel).stem
    row=D['records'][name]
    log=Path(row['log'])
    author=json.loads((RUN/'author_logs'/log.name).read_bytes())
    binary=ROOT/'build'/Path(rel).with_suffix('.olean')
    ownbin=RUN/'build'/Path(rel).with_suffix('.olean')
    records[name]={
        'source_sha256':sha(Path(r['path'])),
        'source_equals_status_and_frozen':sha(Path(r['path']))==row['sha256']==r['sha256']==sha(Path(r['snapshot'])),
        'author_log':str(log),'author_log_sha256':sha(log),
        'author_log_identical_to_frozen':log.read_bytes()==(RUN/'author_logs'/log.name).read_bytes(),
        'author_log_rc0_source_unchanged':author['returncode']==0 and author['source_unchanged_during_compile'] is True,
        'author_binary_sha256':sha(binary),
        'author_binary_equals_status_and_log':sha(binary)==row['output_sha256']==author['output_sha256'],
        'own_binary_sha256':sha(ownbin),
        'own_binary_equals_compilation_record':sha(ownbin)==own[rel]['output_sha256'],
        'own_binary_equals_author':sha(ownbin)==sha(binary),
        'targets_exact':set(own[rel]['axioms'])==set(r['declarations']),
        'author_stream_sha256':{kind:sha(Path(author[kind])) for kind in ['stdout','stderr']},
        'author_streams_identical_to_frozen':all(Path(author[kind]).read_bytes()==(RUN/'author_logs'/Path(author[kind]).name).read_bytes() for kind in ['stdout','stderr']),
        'own_stream_sha256':{kind:sha(Path(own[rel][kind])) for kind in ['stdout','stderr']},
    }
audit=own['ModularDomainFullAudit.lean']
text=Path(audit['stdout']).read_text(encoding='utf-8')
certificate=(RUN/'sources/TGLV350/RegularScalarWeightCertificate.lean').read_text(encoding='utf-8')
fields=re.findall(r'^  ([a-z_]+) :',certificate.split('theorem regularScalarWeightCertificate')[0],re.M)
assert len(fields)==13
own_ax=audit['axioms']
verification={
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'mode':'INDEPENDENT_DEV_RECOMPILATION_FIVE_MODULES_AND_OWN_AUDITOR',
    'records':records,
    'source_count':len(records), 'audited_targets':len(own_ax), 'named_declaration_types':len(M['all_named_declarations']),
    'six_compiles_rc0':len(C['records'])==6 and all(r['returncode']==0 for r in C['records']),
    'status_target_set_exact':set(D['targets'])==set(own_ax)==set(M['declarations']),
    'axioms_match_status_as_sets':all(set(D['targets'][n])==set(own_ax[n]) for n in own_ax),
    'all_axioms_allowed':all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in own_ax.values()),
    'own_auditor_source_sha256':audit['source_sha256'],'own_auditor_olean_sha256':audit['output_sha256'],
    'own_auditor_stdout_sha256':sha(Path(audit['stdout'])),
    'certificate_fields':fields, 'certificate_field_count':len(fields),
    'certificate_universe_explicit_in_source':'RegularScalarWeightCertificate.{u} P' in certificate,
    'certificate_structure_printed_by_own_auditor':'structure TGLV350.Regular.RegularScalarWeightCertificate' in text,
    'frozen_project_dependency_count':len(M['dependencies']),
    'dependency_comment_only_exceptions':{n:{k:r.get(k) for k in ['source_sha256','live_source_sha256','sha256','previously_reviewed_comment_only_erratum']}
        for n,r in M['dependencies'].items() if not r['live_source_matches_frozen']},
    'frozen_dependencies_preserved':C['dependencies_unchanged'],
    'lean_path_excludes_author_project_builds':str(ROOT/'build') not in M['lean_path'] and str(ROOT/'kernel') not in M['lean_path'],
    'draft_status_sha256':sha(RUN/'author_modular_domain_draft_status.json'),
    'draft_status_unchanged':sha(ROOT/'modular_domain_draft_status.json')==M['draft_status_sha256'],
    'route_sha256':sha(ROOT/'ROTA_DOMINIO_MODULAR_RASCUNHO.md'),
    'route_equals_status_and_frozen':sha(ROOT/'ROTA_DOMINIO_MODULAR_RASCUNHO.md')==D['draft_note_sha256']==sha(RUN/'ROTA_DOMINIO_MODULAR_RASCUNHO.md'),
    'custody_sha256':sha(ROOT/'scalar_weight_custody.json'),
    'custody_equals_pinned_status':sha(ROOT/'scalar_weight_custody.json')==D['integrated_custody_sha256'],
    'sealed_scalar_review_sha256':sha(REVIEW/'REVIEW_SCALAR_DUAL_WEIGHT.md'),
    'sealed_scalar_review_matches_custody':sha(REVIEW/'REVIEW_SCALAR_DUAL_WEIGHT.md')==K['review_sha256'],
    'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),
    'integrated_custody_historical_counts':{k:K[k] for k in ['integrated_records','controls','audit_declarations','working_sha256']},
    'integration_of_new_stage_reviewed_here':False,
    'author_monolith_recorders_tests_executed':False,
}
assert verification['status_target_set_exact'] and verification['axioms_match_status_as_sets']
raw=json.dumps(verification,ensure_ascii=False,indent=2).encode('utf-8')
p=RUN/'verification_dev.json';assert not p.exists()
tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(json.dumps({k:v for k,v in verification.items() if k!='records'},ensure_ascii=False,indent=2))
