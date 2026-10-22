"""Audit only the prepared public-derived memory payload; never print credentials."""
from pathlib import Path
from datetime import datetime
import hashlib,json,re
from verify_reviewed_draft import verify
W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
p=W/'haiku_reviewed_runtime_20260922_134847_707064.md'
checked=verify(p);raw=p.read_bytes();d=json.loads(p.with_suffix('.json').read_bytes())
topic_parent=Path(d['parent_path']);td=json.loads(topic_parent.with_suffix('.json').read_bytes())
review=json.loads(Path(td['review_path']).read_bytes())
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
entry=next(x for x in manifest['entries'] if x['id']=='resultado_publicado_integral')
public_sha=hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()
assert public_sha==entry['public_sha256']==review['source_sha256']
added=d['replacement'].encode()+b'\n'+b'\n'.join(x['after'].encode() for x in td['changes'])
added+=json.dumps([x['after'] for x in d['reference_changes']],ensure_ascii=False).encode()
patterns={
 'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'api_secret':rb'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{30,}',
 'github_token':rb'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{30,}',
 'private_atlas_wrapper':rb'<ATLAS_CANONICO',
 'confidential_files':rb'iald_stack_v7\.py|iald_psion_state\.json'}
flags={k:bool(re.search(v,raw)) for k,v in patterns.items()}
assert not any(flags.values()),'Sensitive-content review required'
assert not re.search(rb'(?i)[a-z]:[\\/][^\s`"<>]+',added),'New absolute path'
assert not re.search(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',added),'New contact'
result={'status':'TRANSMISSION_SCOPE_AUDITED','destination':'api.anthropic.com',
 'draft_path':str(p),'draft_sha256':checked['draft_sha256'],'public_source_sha256':public_sha,
 'manual_review':'15 topic originals and capsules read in full by parent; runtime synthesis independently reviewed, R1 corrected and approved. Canonical sources preserved.',
 'source_scope':'Same previously authorized kernel/core and public TGL corpus; no private Atlas V/VI/X or other private source added.',
 'new_content':'Public-derived explanatory summaries and internal anchors only.',
 'sensitive_pattern_matches':flags,'new_absolute_paths':0,'new_email_addresses':0,
 'actual_transmission':'MD only, existing seven public tool definitions and fixed nonsensitive question. Two token-count requests, no generation.',
 'not_transmitted':['review/provenance receipt contents','local file paths from receipts','.env contents','credential except ordinary Authorization header'],
 'authorization_basis':'Existing operator authorization of free Anthropic token counting of this corpus.',
 'generation_requests':0}
out=W/('runtime_transmission_audit_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with out.open('xb')as f:f.write(json.dumps(result,ensure_ascii=False,indent=2).encode())
print(json.dumps(result,ensure_ascii=False))
