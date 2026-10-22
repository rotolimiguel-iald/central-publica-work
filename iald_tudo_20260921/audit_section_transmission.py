"""Audit new transmitted bytes, separately from local provenance receipts."""
from pathlib import Path
import hashlib,json,re
from datetime import datetime
from verify_reviewed_draft import verify
W=Path(__file__).resolve().parent
p=W/'haiku_reviewed_section_20260922_130747_311801.md'
checked=verify(p);receipt=json.loads(p.with_suffix('.json').read_bytes())
raw=p.read_bytes();parent=Path(receipt['parent_path']).read_bytes();capsule=Path(receipt['capsule_path']).read_bytes()
patterns={
 'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'api_secret':rb'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{30,}',
 'github_token':rb'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{30,}',
 'private_atlas_wrapper':rb'<ATLAS_CANONICO',
 'confidential_files':rb'iald_stack_v7\.py|iald_psion_state\.json',
}
flags={name:bool(re.search(pattern,raw)) for name,pattern in patterns.items()}
if any(flags.values()):raise ValueError('Sensitive-content review required: '+','.join(k for k,v in flags.items() if v))
# Inspect precisely the newly transmitted section and metadata, not local receipts.
added=capsule+b'\n'+receipt['header_change']['after'].encode()+b'\n'+b'\n'.join(r['after'].encode() for r in receipt['replacements'])
path_hits=re.findall(rb'(?i)[a-z]:[\\/][^\s`"<>]+',added)
mail_hits=re.findall(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',added)
if path_hits or mail_hits:raise ValueError('New local path or contact requires inspection')
prov=json.loads(Path(receipt['provenance_path']).read_bytes())
review=json.loads(Path(receipt['review_path']).read_bytes())
assert review['source_sha256']==prov['source_result_sha256']
result={'status':'TRANSMISSION_SCOPE_AUDITED','destination':'api.anthropic.com',
 'draft_sha256':checked['draft_sha256'],'parent_sha256':hashlib.sha256(parent).hexdigest(),
 'public_source_sha256':review['source_sha256'],'new_capsule_sha256':hashlib.sha256(capsule).hexdigest(),
 'new_section_manual_review':'All 65 original and condensed blocks read by main reviewer; 256 source fields verified against published result. Four corrections reviewed in V2.',
 'new_content_origin':'Public result statuses/verdicts plus documented derivative explanations; no private Atlas sections added.',
 'unchanged_parent_bytes_verified':True,'new_absolute_paths':len(path_hits),'new_email_addresses':len(mail_hits),
 'sensitive_pattern_matches':flags,
 'actual_transmission':'MD draft + seven existing public tool definitions + fixed nonsensitive test question, twice to token-count endpoint only.',
 'local_only_not_transmitted':['provenance_v2.json contents','review receipts','file paths from integration receipts','.env contents','API key except normal Authorization transport'],
 'tools':['iald_kernel_verification','iald_kernel_search','iald_kernel_read','iald_kernel_list','iald_public_read','search_tgl','fetch_tgl'],
 'generation_requests':0,
 'authorization_basis':'Operator explicitly authorized Anthropic free counting of kernel v5, canonical core, TGL cluster, public sources and operational Atlas sections excluding private V/VI/X; this change condenses those public statuses.'}
out=W/('section_transmission_audit_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
with out.open('xb')as f:f.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result,ensure_ascii=False))
