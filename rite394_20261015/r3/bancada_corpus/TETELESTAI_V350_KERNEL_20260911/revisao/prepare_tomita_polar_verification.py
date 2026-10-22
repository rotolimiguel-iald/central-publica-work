"""Prepare the bounded-scope reconciliation using the established own protocol."""
from pathlib import Path
REV=Path(__file__).resolve().parent
s=(REV/'verify_scalar_tomita_domain_review.py').read_text(encoding='utf-8')
changes=[
 ('six DEV modules, all 25','three DEV modules, all 16'),
 ('scalar_tomita_domain_latest_run.txt','scalar_tomita_polar_latest_run.txt'),
 ('tomita_root_domain_draft_status.json','tomita_polar_draft_status.json'),
 ('RELATORIO_DOMINIO_RAIZ_TOMITA_DEV.md','RELATORIO_FATOR_POLAR_TOMITA_DEV.md'),
 ('len(blocks)==25','len(blocks)==16'),
 ("assert local_instances=={'TGLV350/RealGraphCore.lean':['realGraphHilbert'],\n 'TGLV350/ScalarTomitaGraphCore.lean':['scalarGraphRealHilbert'],'TGLV350/PartialSquareGraphCore.lean':['squareGraphRealHilbert']}", 'assert not local_instances'),
 ("len(history)==12 and sum(h['returncode']==0 for h in history)==7 and sum(h['accepted_final'] for h in history)==6", "len(history)==5 and sum(h['returncode']==0 for h in history)==3 and sum(h['accepted_final'] for h in history)==3"),
 ('SIX_DEV_MODULES_25_TARGETS_VERIFIED','THREE_DEV_MODULES_16_TARGETS_VERIFIED'),
 ("'all_25_types_printed'","'all_16_types_printed'"),
 ("'all_6_own_binaries_byte_equal_author'","'all_3_own_binaries_byte_equal_author'"),
 ("'history_rc0':7,'accepted_final_rc0':6,'superseded_rc0':1,'history_rc1':5", "'history_rc0':3,'accepted_final_rc0':3,'superseded_rc0':0,'history_rc1':2"),
]
for a,b in changes:
    assert a in s,a
    s=s.replace(a,b)
anchor="assert hf(ROOT/'tomita_root_custody.json')==STATUS['parent_custody_sha256']"
s=s.replace(anchor,anchor+"\nassert hf(ROOT/'tomita_root_domain_draft_status.json')==STATUS['domain_manifest_sha256']\nassert hf(REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md')==STATUS['domain_review_sha256']")
anchor="result={'timestamp':datetime.datetime.now().astimezone().isoformat()"
extra="""# Read-only source pins for the two Mathlib APIs inspected in this review.
package_base=next(Path(p).parents[3] for p in lp[1:] if '\\\\mathlib\\\\' in p)
mathlib_pins={}
for rel in ['Mathlib/Analysis/Normed/Operator/Extend.lean','Mathlib/Analysis/InnerProductSpace/LinearPMap.lean']:
    p=package_base/rel
    mathlib_pins[str(p)]={'sha256':hf(p),'bytes':p.stat().st_size}
"""
s=s.replace(anchor,extra+anchor)
s=s.replace("'new_targets_absent_from_current_integrated_Audit':True", "'Mathlib_API_source_pins':mathlib_pins,'new_targets_absent_from_current_integrated_Audit':True")
out=REV/'verify_scalar_tomita_polar_review.py';assert not out.exists();raw=s.encode();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out)
print(str(out))
