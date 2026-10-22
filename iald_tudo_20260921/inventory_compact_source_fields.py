from pathlib import Path
import os,json
os.environ.setdefault('TIKTOKEN_CACHE_DIR',r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken
from compact_source_fields import pack,unpack,KEY
W=Path(__file__).resolve().parent
p=W/'haiku_reviewed_runtime_20260922_134847_707064.md'
t=p.read_bytes().decode();changed=[];out=[];count=0
def size(v):
    if isinstance(v,list):return sum(size(x) for x in v)
    if not isinstance(v,dict):return 0
    return len(v.get(KEY,[]))+sum(size(x) for k,x in v.items() if k!=KEY)
for line in t.splitlines(keepends=True):
    try:node=json.loads(line)
    except (ValueError,TypeError):out.append(line);continue
    new=pack(node);assert unpack(new)==node
    if new==node:out.append(line);continue
    nl='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
    rendered=json.dumps(new,ensure_ascii=False,separators=(',',':'))+nl
    out.append(rendered);count+=size(new);changed.append((line,rendered))
e=tiktoken.get_encoding('o200k_base');before=len(e.encode(t));after=len(e.encode(''.join(out)))
print(json.dumps({'changed_json_lines':len(changed),'references_grouped':count,
 'old_o200k':before,'new_o200k_without_protocol_header':after,'saving_o200k_before_header':before-after,
 'all_json_structures_roundtrip_exact':True,'sources_changed':False,'api_calls':0}))
