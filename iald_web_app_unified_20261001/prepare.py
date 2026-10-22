from pathlib import Path
import ast,hashlib,json
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');S=W/'stage';S.mkdir(exist_ok=True)
files=('iald_web_server.py','manifest.json')
assert not (W/'baseline.json').exists()
baseline={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in files}
raw=(R/files[0]).read_bytes();text=raw.decode('utf-8');tree=ast.parse(text);lines=text.splitlines(keepends=True)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_destino_web')
old=''.join(lines[node.lineno-1:node.end_lineno])
newline='\r\n' if b'\r\n' in raw else '\n'
new='''def _destino_web(username):
    """One conversation interface for web and mobile, independent of account/model."""
    pending = session.pop('pending_artifact_id', '')
    if username and isinstance(pending, str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', pending):
        return '/app/index.html?artifact=' + pending
    return '/app/index.html'
'''.replace('\n',newline)
assert text.count(old)==1;text=text.replace(old,new)
needle='def static_files(filename):'+newline+'    allowed = {'
replacement='''def static_files(filename):
    # Old bookmarks and installed web shortcuts use the same authenticated app.
    if filename == 'iald_chat.html':
        response = redirect(_destino_web(session.get('username', '')))
        response.headers['Cache-Control'] = 'no-store'
        return response
    allowed = {'''.replace('\n',newline)
assert text.count(needle)==1;text=text.replace(needle,replacement)
ast.parse(text);(S/files[0]).write_bytes(text.encode())
manifest=json.loads((R/files[1]).read_bytes())
manifest['start_url']='/app/index.html'
manifest['scope']='/'
manifest['description']='IALD — Inteligência Artificial Luminodinâmica.'
# Keep the identity formerly inferred from start_url for installed shortcuts.
manifest['id']='/iald_chat.html'
(S/files[1]).write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
(W/'baseline.json').write_bytes(json.dumps(baseline,indent=2).encode())
print('Prepared two-file web entry unification; shared clients unchanged.')
