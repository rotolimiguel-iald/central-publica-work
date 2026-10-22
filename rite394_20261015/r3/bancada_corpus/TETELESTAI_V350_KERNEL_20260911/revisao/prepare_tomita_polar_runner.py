"""Prepare a new own runner without editing the preceding review protocol."""
from pathlib import Path
REV=Path(__file__).resolve().parent
s=(REV/'run_scalar_tomita_domain_review.py').read_text(encoding='utf-8')
changes=[
 ('six root-domain DEV modules','three polar DEV modules'),
 ("PRE=Path((REV/'scalar_tomita_root_latest_run.txt')", "PRE=Path((REV/'scalar_tomita_domain_latest_run.txt')"),
 ('scalar_tomita_domain_independent_','scalar_tomita_polar_independent_'),
 ("pc['exact_30_targets']","pc['PREVIOUS_COUNT_CHECK']"),
 ('tomita_root_domain_draft_status.json','tomita_polar_draft_status.json'),
 ('RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md','RELATORIO_FATOR_POLAR_TOMITA_DEV.md'),
 ("len(status['modules'])==6","len(status['modules'])==3"),
 ("len(status['targets'])==25","len(status['targets'])==16"),
 ("len(set(targets))==25","len(set(targets))==16"),
 ('SIX_DEV_MODULES_AND_25_TARGET_AUDITOR_ONLY','THREE_DEV_MODULES_AND_16_TARGET_AUDITOR_ONLY'),
 ("write(REV/'scalar_tomita_domain_latest_run.txt'", "write(REV/'scalar_tomita_polar_latest_run.txt'"),
 ('ScalarTomitaDomainAudit','ScalarTomitaPolarAudit'),
 ('len(records)==7','len(records)==4'),
 ("'exact_25_targets'","'exact_16_targets'"),
 ("'six_binaries_equal_author'","'three_binaries_equal_author'"),
 ("pc['PREVIOUS_COUNT_CHECK']","pc['exact_25_targets']"),
]
for a,b in changes:
    assert a in s,a
    s=s.replace(a,b)
anchor="assert len(status['modules'])==3 and len(status['targets'])==16 and status['integrated'] is False"
s=s.replace(anchor,anchor+"\nassert sha((ROOT/'tomita_root_domain_draft_status.json').read_bytes())==status['domain_manifest_sha256']\nassert sha((REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md').read_bytes())==status['domain_review_sha256']\nassert len(catalog)==417")
out=REV/'run_scalar_tomita_polar_review.py';assert not out.exists();raw=s.encode();q=out.with_suffix('.tmp')
with q.open('xb') as f:f.write(raw)
assert q.read_bytes()==raw;q.replace(out)
print(str(out))
