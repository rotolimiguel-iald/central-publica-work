"""Move internal operational alerts out of every consumer app surface."""
from pathlib import Path
from datetime import datetime
import ast, hashlib, json

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
W=Path(__file__).resolve().parent
out=W/('admin_only_deadlines_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
out.mkdir()
rows=[]

def emit(relative,old,new):
    path=out/relative;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb')as f:f.write(new)
    rows.append(dict(relative=relative,old_sha256=hashlib.sha256(old).hexdigest(),
                     new_sha256=hashlib.sha256(new).hexdigest()))

p=ROOT/'iald_web_server.py';raw=p.read_bytes();text=raw.decode('utf-8')
nl='\r\n' if '\r\n' in text else '\n';text=text.replace('\r\n','\n')
tree=ast.parse(text);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='api_alertas')
lines=text.splitlines(keepends=True)
replacement='''def api_alertas():
    # Compatibility for installed clients: internal operations stay in /admin.
    return jsonify({"alertas": []})


@app.route("/admin/api/prazos", methods=["GET"])
def admin_prazos():
    check = require_admin()
    if check:
        return check
    from iald_deadlines import snapshot
    response = jsonify({"prazos": snapshot(os.path.join(SERVE_DIR, "iald_deadlines.json"))})
    response.headers["Cache-Control"] = "no-store"
    return response
'''
text=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:])
old="fetch('/api/alertas',{{cache:'no-store'}})"
assert text.count(old)==1
text=text.replace(old,"fetch('/admin/api/prazos',{{cache:'no-store'}})")
ast.parse(text)
emit('iald_web_server.py',raw,text.replace('\n',nl).encode('utf-8'))

p=ROOT/'app/iald.js';raw=p.read_bytes();text=raw.decode('utf-8')
nl='\r\n' if '\r\n' in text else '\n';text=text.replace('\r\n','\n')
for line in ["import { renderDeadlines } from './operational_deadlines.js';\n",
             "  if (S.servidor.estado !== 'offline') verificarAlertas();\n",
             "  alertasMostrados: new Set(),     // 15/09/2026: bandeira do crédito da OpenAI, uma vez por nível na sessão\n"]:
    assert text.count(line)==1; text=text.replace(line,'')
start=text.index('async function verificarAlertas() {')
end=text.index('\n// ═════════',start)
text=text[:start]+text[end:]
# Remove the now misleading comment block immediately before the deleted function.
start=text.rfind('// ═════════',0,start)
previous=text.rfind('// ═════════',0,start)
if 'ALERTA' in text[previous:start] or '/api/alertas' in text[previous:start]:
    text=text[:previous]+text[start+len('// ══════════════════════════════════════════════════════════════\n'):]
assert 'renderDeadlines' not in text and 'verificarAlertas' not in text and '/api/alertas' not in text
emit('app/iald.js',raw,text.replace('\n',nl).encode('utf-8'))
with (out/'receipt.json').open('x',encoding='utf-8')as f:json.dump(rows,f,indent=2)
print(out)
