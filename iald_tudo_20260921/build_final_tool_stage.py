from pathlib import Path
import ast, hashlib, json, difflib
from datetime import datetime
W=Path(__file__).parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
D=W/'haiku_window_diagnostic_20260923_085246_281422'
P=W/'r1_readiness_stage_20260923_084024_035676'
F=W/('haiku_tool_budget_final_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
F.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
base=(R/'iald_web_server.py').read_bytes()
assert sha(base)==json.loads((P/'patch_manifest.json').read_text())['base_sha256']
assert sha(base)==json.loads((D/'candidate_manifest.json').read_text())['iald_web_server.py']['base_sha256']
def span(text,name):
 n=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
 lines=text.splitlines(keepends=True)
 return sum(map(len,lines[:n.lineno-1])),sum(map(len,lines[:n.end_lineno]))
server=(D/'iald_web_server.py').read_bytes().decode('utf-8')
r1=(P/'iald_web_server.py').read_bytes().decode('utf-8')
for name in ('_opcoes_de_motor','api_motor_escolha'):
 a,b=span(server,name); c,d=span(r1,name)
 server=server[:a]+r1[c:d]+server[b:]
(F/'iald_web_server.py').write_bytes(server.encode())
for name in ('claude_native_account.py','claude_tool_budget.py','test_tool_budget.py','test_window_path.py'):
 (F/name).write_bytes((D/name).read_bytes())
# Preserve measured artifact; only reject malformed/mismatched batches before counting.
helper=(F/'claude_tool_budget.py').read_text()
anchor='    original=deepcopy(payload)\n'
guard='''    call_ids=[call.get('id') for call in messages[start-1]['tool_calls']]
    result_ids=[message.get('tool_call_id') for message in messages[start:]]
    if (any(not isinstance(i,str) or not i for i in call_ids+result_ids)
            or len(set(call_ids))!=len(call_ids)
            or len(set(result_ids))!=len(result_ids)
            or set(call_ids)!=set(result_ids)):
        raise ToolResultsDoNotFit('Tool results do not match the latest assistant batch; unchanged, not sent.')
'''
assert helper.count(anchor)==1
(F/'claude_tool_budget.py').write_text(helper.replace(anchor,guard+anchor),encoding='utf-8',newline='\n')
for name in ('test_claude_rotas.py','test_acesso_nativa.py','offline_bootstrap.py'):
 (F/name).write_bytes((P/name).read_bytes())
boot=(F/'offline_bootstrap.py').read_text()
boot=boot.replace("source = (HERE / 'iald_web_server.py').read_text(encoding='utf-8-sig')","source = globals().get('SERVER_SOURCE', HERE / 'iald_web_server.py').read_text(encoding='utf-8-sig')")
boot=boot.replace('    return module\n', '''    if globals().get('SERVER_SOURCE', HERE / 'iald_web_server.py') != ROOT / 'iald_web_server.py':
        import importlib.util
        spec=importlib.util.spec_from_file_location('staged_native_account', HERE/'claude_native_account.py')
        account=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(account)
        module._HaikuNativeAccount=account.NativeAccount
    return module
''')
(F/'offline_bootstrap.py').write_text(boot,encoding='utf-8')
t=(F/'test_window_path.py').read_text()
t=t.replace("ROOT = Path(r'C:\\IALD\\projetos_pyhton\\IALD')","ROOT = Path(r'C:\\IALD\\projetos_pyhton\\IALD')\nif not STAGED: offline_bootstrap.SERVER_SOURCE=ROOT/'iald_web_server.py'")
t=t.replace("'sent_wires':client.chamadas}","'initial_no_send_message':'Nenhuma chamada de geração foi enviada nesta solicitação.' in body,\n                'partial_status':'Resultados em excertos parciais' in body,\n                'sent_wires':client.chamadas}")
t=t.replace("self.assertEqual((result['sends'],result['reserves']),(0,0))","self.assertEqual((result['sends'],result['reserves']),(0,0))\n        if STAGED:self.assertTrue(result['initial_no_send_message'])")
t=t.replace("self.assertEqual((result['sends'],result['reserves']),(2,2))","self.assertEqual((result['sends'],result['reserves']),(2,2))\n        if STAGED:self.assertTrue(result['partial_status'])")
(F/'test_window_path.py').write_text(t,encoding='utf-8')
manifest={'root':str(R),'files':{},'measured_helper_sha256':sha((D/'claude_tool_budget.py').read_bytes()),'helper_delta':'Only batch ID validation; measured source preserved in diagnostic folder. Valid inputs keep same output algorithm. New artifact not API remeasured.'}
for name in ('iald_web_server.py','claude_native_account.py','claude_tool_budget.py'):
 before=(R/name).read_bytes() if (R/name).exists() else b''
 after=(F/name).read_bytes()
 manifest['files'][name]={'base_sha256':sha(before) if before else None,'staged_sha256':sha(after),'bytes':len(after)}
 (F/(name+'.diff')).write_text(''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(True),after.decode('utf-8-sig').splitlines(True),fromfile='ROOT/'+name,tofile='STAGED/'+name)),encoding='utf-8')
# Verify every byte outside the four authorized functions and no Selo line deletion.
def without(text):
 for name in ('agent_loop','_chat_externo','_opcoes_de_motor','api_motor_escolha'):
  a,b=span(text,name);text=text[:a]+f'# OMIT {name}\n'+text[b:]
 return text
assert without(base.decode())==without(server)
diff=list(difflib.ndiff(base.decode().splitlines(),server.splitlines()))
assert not any(line.startswith('- ') and 'selo' in line.lower() for line in diff)
manifest['outside_four_functions_byteexact']=True
manifest['deleted_selo_lines']=0
(F/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(W/'latest_tool_stage_path.txt').write_text(str(F),encoding='utf-8')
print(F)
