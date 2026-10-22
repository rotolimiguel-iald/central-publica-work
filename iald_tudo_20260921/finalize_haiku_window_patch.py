"""Combine reviewed availability and tool-window fixes in an isolated stage."""
import ast
from datetime import datetime
import hashlib
import json
from pathlib import Path

W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
DIAG=W/'haiku_window_diagnostic_20260923_085246_281422'
R1=W/'r1_readiness_stage_20260923_084024_035676'

def create(path,data):
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data

def function_spans(raw):
    return {n.name:(n.lineno-1,n.end_lineno) for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)}

def main():
    target=W/('haiku_window_final_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    target.mkdir()
    server=(DIAG/'iald_web_server.py').read_bytes()
    available=(R1/'iald_web_server.py').read_bytes()
    lines=server.splitlines(keepends=True); other=available.splitlines(keepends=True)
    spans=function_spans(server); refs=function_spans(available)
    for name in sorted(('_opcoes_de_motor','api_motor_escolha'),key=lambda n:spans[n][0],reverse=True):
        lo,hi=spans[name]; a,b=refs[name]
        lines[lo:hi]=other[a:b]
    server=b''.join(lines)
    helper=(DIAG/'claude_tool_budget.py').read_bytes()
    anchor=b'    original=deepcopy(payload)\n'
    assert helper.count(anchor)==1
    guard=b'''    calls=messages[start-1]['tool_calls']
    expected=[call.get('id') for call in calls if isinstance(call,dict)]
    actual=[message.get('tool_call_id') for message in messages[start:]]
    if (len(expected)!=len(calls) or len(expected)!=len(actual)
            or any(not isinstance(value,str) or not value for value in expected+actual)
            or len(set(expected))!=len(expected) or len(set(actual))!=len(actual)
            or set(expected)!=set(actual)):
        raise ToolResultsDoNotFit('Tool results do not match the latest calls; next turn not sent.')
'''
    helper=helper.replace(anchor,guard+anchor)
    candidates={'iald_web_server.py':server,'claude_native_account.py':(DIAG/'claude_native_account.py').read_bytes(),
                'claude_tool_budget.py':helper}
    manifest={}
    for name,raw in candidates.items():
        compile(raw,name,'exec')
        live=ROOT/name
        manifest[name]={'base_sha256':hashlib.sha256(live.read_bytes()).hexdigest() if live.exists() else None,
                        'staged_sha256':hashlib.sha256(raw).hexdigest()}
        create(target/name,raw)
    for name in ('test_tool_budget.py','test_window_path.py'):
        create(target/name,(DIAG/name).read_bytes())
    for name in ('test_claude_rotas.py','test_acesso_nativa.py'):
        create(target/name,(R1/name).read_bytes())
    bootstrap=(DIAG/'offline_bootstrap.py').read_bytes().replace(
        b"globals().get('SERVER_SOURCE', ROOT / 'iald_web_server.py')",
        b"globals().get('SERVER_SOURCE', HERE / 'iald_web_server.py')")
    create(target/'offline_bootstrap.py',bootstrap)
    create(target/'patch_manifest.json',json.dumps(manifest,indent=2).encode())
    import difflib
    for name in candidates:
        live=ROOT/name; before=live.read_text(encoding='utf8') if live.exists() else ''
        after=candidates[name].decode('utf8')
        diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='ROOT/'+name,tofile='STAGED/'+name))
        create(target/(name+'.diff'),diff.encode('utf8'))
    print(str(target))

if __name__=='__main__':main()
