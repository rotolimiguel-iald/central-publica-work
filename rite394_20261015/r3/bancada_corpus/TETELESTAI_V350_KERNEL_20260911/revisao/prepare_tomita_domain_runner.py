"""Derive a new isolated reviewer runner from the already reviewed own protocol."""
from pathlib import Path
REV=Path(__file__).resolve().parent
old=REV/'run_scalar_tomita_root_review.py';out=REV/'run_scalar_tomita_domain_review.py'
s=old.read_text(encoding='utf-8')
replacements=[
 ('only the five root DEV modules','only the six root-domain DEV modules'),
 ("PRE=Path((REV/'tomita_square_latest_run.txt')", "PRE=Path((REV/'scalar_tomita_root_latest_run.txt')"),
 ("scalar_tomita_root_independent_", "scalar_tomita_domain_independent_"),
 ("pc['exact_53_targets']", "pc['exact_30_targets']"),
 ("tomita_root_draft_status.json", "tomita_root_domain_draft_status.json"),
 ("tomita_square_custody", "tomita_root_custody"),
 ("RELATORIO_RAIZ_TOMITA_DEV.md", "RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md"),
 ("len(status['modules'])==5", "len(status['modules'])==6"),
 ("len(status['targets'])==30", "len(status['targets'])==25"),
 ("len(set(targets))==30", "len(set(targets))==25"),
 ("FIVE_DEV_MODULES_AND_30_TARGET_AUDITOR_ONLY", "SIX_DEV_MODULES_AND_25_TARGET_AUDITOR_ONLY"),
 ("write(REV/'scalar_tomita_root_latest_run.txt'", "write(REV/'scalar_tomita_domain_latest_run.txt'"),
 ("ScalarTomitaRootAudit", "ScalarTomitaDomainAudit"),
 ("len(records)==6", "len(records)==7"),
 ("'exact_30_targets'", "'exact_25_targets'"),
 ("'five_binaries_equal_author'", "'six_binaries_equal_author'"),
]
for a,b in replacements:
    assert a in s,a
    s=s.replace(a,b)
s=s.replace("assert cv['custody_ok'] and cv['custody_sha256']==sha(custodyraw)",
 "assert cv['custody_ok'] and cv['custody_sha256']==sha(custodyraw)==status['parent_custody_sha256']")
assert not out.exists();raw=s.encode('utf-8');q=out.with_suffix('.tmp')
with q.open('xb') as f:f.write(raw)
assert q.read_bytes()==raw;q.replace(out)
print(str(out))
