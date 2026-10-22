import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace as NS
import ast
import iald_jev_control as control

HERE = Path(__file__).resolve().parent
CONTRACT = json.loads((HERE / 'jev_control_v380.json').read_bytes())
# Only deployment I/O is synthetic; all decision, scope and instruction functions remain real.
control_proxy = NS(**{name:getattr(control,name) for name in (
    'contract_state','questions','resolve','manager_instruction','allowed_tool_names',
    'check_payload','new_receipt','transition')}, load_contract=lambda root:copy.deepcopy(CONTRACT))
BINDING = hashlib.sha256(json.dumps(control.contract_state(CONTRACT),sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def typed_answers(questions, *, operator=False, worker=False, path='answer'):
    selected={'scientific_mode':'explanation','work_path':path,'memory_action':'use_loaded'}
    return {key:{'type':'choice','choice':selected[key],'confidence':0.95,
                 'probabilities':{name:float(name==selected[key]) for name in value['criteria']}}
            for key,value in questions.items() if key!='executor'}

def receipt(*, operator=False, worker=False, path='code_review'):
    qs=control.questions(operator,worker)
    decision=control.resolve(typed_answers(qs,operator=operator,worker=worker,path=path),['mimo'],'Synthetic public fixture',operator,worker)
    return dict(id='fixture-route',status='selected',control=decision,control_binding=BINDING,
                request_sha256=hashlib.sha256(b'Synthetic public fixture').hexdigest(),memory={'coverage':'synthetic public fixture'})

def _scope_functions():
    tree=ast.parse((HERE/'iald_auto_router.py').read_text(encoding='utf-8-sig'))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('route_instruction','bind_scope')]
    env=dict(ROOT=HERE,jev_control=control_proxy,json=json,hashlib=hashlib)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'real_staged_router_scope','exec'),env)
    return env

SCOPE = _scope_functions()

def bind_scope(scope,record):
    if not hasattr(scope,'record'):scope.record={}
    if not hasattr(scope,'_save'):scope._save=lambda:None
    if not hasattr(scope,'execute'):scope.execute=lambda name,args:{'status':'UNAVAILABLE'}
    return SCOPE['bind_scope'](scope,record,root=HERE)

route_instruction = SCOPE['route_instruction']
