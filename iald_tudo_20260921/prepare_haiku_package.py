"""Prepare, but do not activate, the measured Haiku package."""
from pathlib import Path
from datetime import datetime
import json
from verify_metadata_draft import verify
from check_haiku_conversation_capacity import assess
from claude_memory_package import load_package
W=Path(__file__).resolve().parent
draft=W/'haiku_metadata_proposal_20260922_141555_464161.md'
checked=verify(draft)
receipts=[(p,json.loads(p.read_bytes()))for p in W.glob('haiku_native_wire_count_*.json')]
matches=[(p,v)for p,v in receipts if v.get('draft_sha256')==checked['draft_sha256']]
assert len(matches)==1
count_path,count=matches[0]
assert assess(count)['capacity_ready']
out=W/('haiku_package_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
out.mkdir()
raw=draft.read_bytes()
with (out/'prefix.md').open('xb')as f:f.write(raw)
manifest={'schema':'iald.claude.memory.v1','status':'PREPARED_NOT_ACTIVATED',
 'model':count['model'],'prefix_file':'prefix.md','prefix_sha256':checked['draft_sha256'],
 'budget':count['budget'],'tools_sha256':count['native_tools_sha256'],
 'measurement_receipt':count_path.name,'source_draft':draft.name,
 'scope':'Measured authorized public/operational corpus. No private Atlas. Per-call count still required.'}
with (out/'manifest.json').open('x',encoding='utf-8')as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
package=load_package(out)
assert package.prefix.encode()==raw
print(json.dumps({'path':str(out),'permanent_tokens':package.measurement.permanent_tokens,
                  'dynamic_tokens':package.available_dynamic_tokens,'status':'PREPARED_NOT_ACTIVATED'}))
