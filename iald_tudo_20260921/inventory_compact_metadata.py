from pathlib import Path
import os,json
os.environ.setdefault('TIKTOKEN_CACHE_DIR',r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken
from compact_source_fields import pack,unpack
from compact_source_items import pack_items,unpack_items
W=Path(__file__).resolve().parent
p=W/'haiku_reviewed_runtime_20260922_134847_707064.md';t=p.read_bytes().decode()
start=t.index('\n## Fundamento, Um, Meia-Nat e custo geométrico')
end=t.index('\n## Exposição canônica integral: fórmulas e derivações')
out=[];changed=0;position=0
for line in t.splitlines(keepends=True):
    within=start<=position<end;position+=len(line)
    if not within:out.append(line);continue
    try:node=json.loads(line)
    except (ValueError,TypeError):out.append(line);continue
    value=pack_items(pack(node));assert unpack(unpack_items(value))==node
    if value==node:out.append(line);continue
    nl='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
    out.append(json.dumps(value,ensure_ascii=False,separators=(',',':'))+nl);changed+=1
e=tiktoken.get_encoding('o200k_base');new=''.join(out)
assert new[:start]==t[:start] and new[new.index('\n## Exposição canônica integral: fórmulas e derivações'):]==t[end:]
print(json.dumps({'old_o200k':len(e.encode(t)),'new_o200k_before_protocol_header':len(e.encode(new)),
 'saved_o200k_before_header':len(e.encode(t))-len(e.encode(new)),
 'changed_json_lines':changed,'all_json_structures_roundtrip_exact':True,'protected_prefix_and_exposition_unchanged':True}))
