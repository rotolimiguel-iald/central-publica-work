from pathlib import Path
import ast, json, hashlib, re
root=Path(__file__).resolve().parent
snap=root/'snapshot'
runtime=Path(r'C:\IALD\projetos_pyhton\IALD')
checks=[]
for row in json.loads((snap/'BASELINE.json').read_bytes()):
    p=Path(row['path']); raw=p.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['sha256'],'Baseline changed'
    lines=raw.decode('utf-8-sig').splitlines(keepends=True)
    patch=(snap/(p.name+'.patch')).read_text(encoding='utf-8').splitlines(keepends=True)
    result=[];pos=0;i=2
    while i<len(patch):
        m=re.match(r'@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@',patch[i])
        assert m,'Malformed hunk'
        start=int(m[1])-1
        result.extend(lines[pos:start]);pos=start;i+=1
        while i<len(patch) and not patch[i].startswith('@@ '):
            line=patch[i];kind=line[0];body=line[1:]
            if kind in ' -':
                assert lines[pos].rstrip('\r\n')==body.rstrip('\r\n'),'Patch context changed'
                pos+=1
            if kind in ' +': result.append(body)
            i+=1
    result.extend(lines[pos:]);changed=''.join(result)
    tree=ast.parse(changed)
    fixture=ast.parse((snap/('server_functions.py' if p.name=='iald_web_server.py' else p.name)).read_text(encoding='utf-8'))
    if p.name=='iald_web_server.py':
        expected={n.name:ast.dump(n,include_attributes=False) for n in fixture.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        actual={n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in expected}
        assert expected==actual,'Fixture differs from patched real AST'
        count=len(expected)
    else:
        assert ast.dump(tree,include_attributes=False)==ast.dump(fixture,include_attributes=False)
        count='whole module'
    checks.append({'path':str(p),'baseline_sha256':hashlib.sha256(raw).hexdigest(),'patch_applies':True,'ast_fixture_matches':True,'scope':count})
(root/'AST_VERIFICATION.json').write_text(json.dumps({'checks':checks,'server_preamble_emitted':False,'server_imported':False,'patched_source_written':False},indent=2),encoding='utf-8')
print(json.dumps(checks))
