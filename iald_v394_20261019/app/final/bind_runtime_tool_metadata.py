"""Bind fixed-seven runtime schemas separately from all counted scoped tools."""
from pathlib import Path
from types import SimpleNamespace
import json,sys
F=Path(__file__).resolve().parent;A=F.parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
assert task.check('app',actor='codex-v394-app-builder')['ready']
sys.path[:0]=[str(R),str(A)]
from prepare_science import write,sha
from claude_profiles import HAIKU
from claude_context_snapshot import native_tools_sha256
from iald_motor_claude import converter_pedido
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
rows=[]
for folder in ('haiku55','shared'):
    root=F/'packages'/folder;raw=(root/'prefix.md').read_bytes();receipt_raw=(root/'native_count.json').read_bytes();rc=json.loads(receipt_raw)
    cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium')
    wire=converter_pedido(cfg,{'model':HAIKU.model,'max_completion_tokens':16384,
        'messages':[{'role':'system','content':raw.decode()},{'role':'user','content':'Explique o alcance documentado da v394.'}],
        'tools':tools},prefixo=raw.decode())
    scoped=sha(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode())
    fixed=native_tools_sha256(wire['tools'][:7]);assert scoped==rc['native_tools_sha256']
    manifest=json.loads((root/'manifest.json').read_bytes());assert manifest['prefix_sha256']==sha(raw)
    old=manifest['tools_sha256'];manifest.update(tools_sha256=fixed,counted_scoped_tools_sha256=scoped,
        tool_binding_scope='Fixed seven reviewed runtime schemas in tools_sha256; full counted server-scoped tool list in counted_scoped_tools_sha256; request adapter pins dynamic full scope.')
    write(root/'manifest.json',manifest)
    assert (root/'native_count.json').read_bytes()==receipt_raw and (root/'prefix.md').read_bytes()==raw
    rows.append({'package':folder,'native_count_receipt_sha256':sha(receipt_raw),
        'previous_manifest_tools_sha256':old,'fixed_seven_runtime_tools_sha256':fixed,
        'all_counted_scoped_tools_sha256':scoped,'prefix_and_measured_budget_unchanged':True})
write(F/'TOOL_BINDING_METADATA_R1.json',{'status':'RUNTIME_METADATA_CORRECTED_WITHOUT_RECOUNT_OR_RUNTIME_PATCH',
    'reason':'Current verify_native_tools pins seven fixed public tools, while complete ACOM-scoped tools are separately counted and pinned per request.',
    'packages':rows,'native_count_requests':0,'runtime_changes':0})
print(json.dumps({'status':'TOOL_METADATA_BOUND_TO_CURRENT_RUNTIME','packages':len(rows),'recounts':0}))
