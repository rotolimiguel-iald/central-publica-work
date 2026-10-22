"""Authorized native counts only, exact final public bytes, max_retries=0."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime,timezone
import hashlib,json,sys
F=Path(__file__).resolve().parent;A=F.parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
assert task.check('app',actor='codex-v394-app-builder')['ready']
sys.path[:0]=[str(R),str(A)]
from prepare_science import save,write,sha
from claude_profiles import HAIKU,SONNET,context_budget,reasoning_parameters
from claude_native_counter import count_native_request,native_count_parameters
from iald_motor_claude import converter_pedido
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory
from dotenv import dotenv_values
import anthropic
binding=json.loads((F/'PREPARED_BINDING.json').read_bytes())
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
key=dotenv_values(R/'.env').get('IALD_CLAUDE_API_KEY');assert key
client=anthropic.Anthropic(api_key=key,max_retries=0,timeout=120);del key
total=0
try:
    for folder,profile in [('haiku55',HAIKU),('shared',HAIKU),('sonnet_public',SONNET)]:
        root=F/'packages'/folder;raw=(root/'prefix.md').read_bytes();prefix=raw.decode()
        assert '<ATLAS_CANONICO' not in prefix
        if folder=='sonnet_public':assert sha(raw)==binding['actual_prompts']['public']['prefix_sha256']
        else:
            prep=json.loads((root/'preparation.json').read_bytes());assert prep['private_atlas_included'] is False
            assert prep['prefix_sha256']==sha(raw) and prep['deployment']==binding['deployment']
        assert not (root/'native_count.json').exists(),'Never repeat a completed count'
        cfg=SimpleNamespace(modelo=profile.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium' if profile is HAIKU else 'high')
        wire=converter_pedido(cfg,{'model':profile.model,'max_completion_tokens':16384,
            'messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v394.'}],
            'tools':tools},prefixo=prefix)
        wire.update(reasoning_parameters(profile.model,16384))
        minimal={'model':profile.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],**reasoning_parameters(profile.model,16384)}
        values={}
        for phase,request in [('permanent',minimal),('whole_request',wire)]:
            intent=root/(phase+'_count_intent.json');assert not intent.exists(),'No retry of uncertain count'
            write(intent,{'status':'COUNT_ONLY_DISPATCH_INTENT','model':profile.model,'prefix_sha256':sha(raw),
                'request_sha256':sha(json.dumps(native_count_parameters(request),sort_keys=True,ensure_ascii=False).encode()),
                'max_retries':0,'generation':False})
            value=count_native_request(client,request);total+=1;values[phase]=value
            write(root/(phase+'_count_result.json'),{'status':'COUNT_RETURNED','input_tokens':value,
                'intent_sha256':sha(intent.read_bytes())})
        budget=context_budget(profile.model,counted_model=profile.model,permanent_tokens=values['permanent'],
            request_input_tokens=values['whole_request'],reserved_output_tokens=16384)
        tools_sha=sha(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode())
        receipt={'status':'NATIVE_COUNTED_PUBLIC_ONLY','utc':datetime.now(timezone.utc).isoformat(),
            'model':profile.model,'deployment':binding['deployment'],'public_commit':binding['commit'],
            'prefix_sha256':sha(raw),'budget':budget,'count_requests':2,'generation_requests':0,
            'native_tools_sha256':tools_sha,'private_atlas_included':False,'operator_context_sent':False,
            'scope':'EXACT_FINAL_PUBLIC_PREFIX_AND_SYNTHETIC_NATIVE_REQUEST_WITH_CURRENT_SERVER_TOOLS'}
        write(root/'native_count.json',receipt)
        if not budget['ready'] or budget['remaining_tokens']<10000:raise ValueError('Final public package not admitted; receipt preserved')
        manifest={'schema':'iald.claude.memory.v1','model':profile.model,'prefix_file':'prefix.md','prefix_sha256':sha(raw),
            'budget':budget,'tools_sha256':tools_sha,'deployment':binding['deployment'],
            'measurement_receipt':str(root/'native_count.json'),'coverage':{
                'haiku55':'EXPANDED_PUBLIC_V394_MATH_HYPOTHESES_BOOTSTRAP_AND_422_RETRIEVABLE_TOPICS',
                'shared':'SEMANTIC_COMPACT_V394_422_TOPICS_ALL_ORIGINAL_FIELDS_RETRIEVABLE',
                'sonnet_public':'CURRENT_CANONICALMEMORY_PUBLIC_PROMPT_NATIVE_SONNET_MEASUREMENT'}[folder]}
        write(root/'manifest.json',manifest)
        print(json.dumps({'package':folder,'status':'NATIVE_ADMITTED','permanent_tokens':values['permanent'],
            'whole_request_tokens':values['whole_request'],'remaining_tokens':budget['remaining_tokens']}),flush=True)
finally:client.close()
write(F/'NATIVE_COUNTS_COMPLETE.json',{'status':'PASS','public_count_requests':total,'generation_requests':0,
    'operator_context_egress':False,'max_retries':0,'publication_receipt_sha256':sha((F/'PUBLICATION_VERIFIED.json').read_bytes())})
