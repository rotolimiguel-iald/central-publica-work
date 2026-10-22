"""Native count of the public v390 package for Haiku 5.5; no generation."""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import sys, json, hashlib
W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(W/'stage'), str(R), 'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
from claude_profiles import HAIKU, context_budget, reasoning_parameters
from claude_native_counter import count_native_request
from iald_motor_claude import converter_pedido
import iald_kernel, iald_fontes_publicas, iald_core_indexado
from dotenv import dotenv_values
import anthropic

def main():
    receipt = W/'native_count.json'
    assert not receipt.exists()
    provenance = json.loads((W/'public_memory_provenance.json').read_bytes())
    raw = (W/'package/prefix.md').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == provenance['prefix_sha256']
    assert provenance['private_atlas_included'] is False
    prefix = raw.decode()
    defs = iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()
    cfg = SimpleNamespace(modelo=HAIKU.model, max_saida=HAIKU.default_output, cache_ttl='5m', esforco_claude='medium')
    wire = converter_pedido(cfg, {'model':HAIKU.model, 'max_completion_tokens':HAIKU.default_output,
        'messages':[{'role':'system','content':prefix},{'role':'user','content':'Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.'}],
        'tools':defs}, prefixo=prefix)
    wire.update(reasoning_parameters(HAIKU.model, HAIKU.default_output))
    minimal = {'model':HAIKU.model,'system':wire['system'], 'messages':[{'role':'user','content':'.'}],
               **reasoning_parameters(HAIKU.model,HAIKU.default_output)}
    key = dotenv_values(R/'.env').get('IALD_CLAUDE_API_KEY')
    with anthropic.Anthropic(api_key=key,max_retries=0,timeout=90) as client:
        permanent = count_native_request(client,minimal)
        whole = count_native_request(client,wire)
    budget = context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=permanent,
                            request_input_tokens=whole,reserved_output_tokens=HAIKU.default_output)
    assert budget['ready'] and budget['remaining_tokens'] >= 10000
    result = {'utc':datetime.now(timezone.utc).isoformat(),'model':HAIKU.model,
        'deployment':provenance['deployment'],'prefix_sha256':provenance['prefix_sha256'],
        'budget':budget,'count_requests':2,'generation_requests':0,
        'native_tools_sha256':hashlib.sha256(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
        'scope':'PUBLIC_SCIENCE_PLUS_APPROVED_KERNEL_AND_CORE_NO_PRIVATE_ATLAS'}
    receipt.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode())
    manifest = {'schema':'iald.claude.memory.v1','model':HAIKU.model,'prefix_file':'prefix.md',
        'prefix_sha256':result['prefix_sha256'],'budget':budget,'tools_sha256':result['native_tools_sha256'],
        'deployment':result['deployment'],'measurement_receipt':str(receipt),
        'coverage':'FULL_PUBLIC_CONTEXT_V390_NOT_PRIVATE_ATLAS_NOT_ALL_LEAN_FILES_IN_PROMPT'}
    (W/'package/manifest.json').write_bytes(json.dumps(manifest,ensure_ascii=False,indent=2).encode())
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED','type':type(exc).__name__,'http_status':getattr(exc,'status_code',None)}))
        sys.exit(1)
