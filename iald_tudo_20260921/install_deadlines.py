"""Install the operator-authorized deadline panel, preserving concurrent changes."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def put(path,data):
    before=path.read_bytes() if path.exists() else None
    if before==data:return
    if before is not None:
        backup=path.with_name(path.name+'.bak_'+STAMP)
        if path.parent.name=='www':
            folder=path.parent.parent/('_backups_deadlines_'+STAMP)
            folder.mkdir(exist_ok=True)
            backup=folder/(path.name+'.bak')
        backup.open('xb').write(before);assert backup.read_bytes()==before
    temp=path.with_name(path.name+'.tmp_'+STAMP)
    temp.open('xb').write(data);assert temp.read_bytes()==data
    assert (path.read_bytes() if path.exists() else None)==before
    temp.replace(path);assert path.read_bytes()==data

def replace_once(text,old,new):
    assert text.count(old)==1,(old[:90],text.count(old))
    return text.replace(old,new,1)

def main():
    server=ROOT/'iald_web_server.py'; before=server.read_bytes();s=before.decode('utf-8')
    nl='\r\n' if b'\r\n' in before else '\n'
    old='    return jsonify({"alertas": alertas})'
    new='    from iald_deadlines import snapshot\n    deadlines = snapshot(os.path.join(SERVE_DIR, "iald_deadlines.json"))\n    return jsonify({"alertas": alertas, "prazos": deadlines})'
    s=replace_once(s,old,new.replace('\n',nl))
    anchor='<div class="wrap">'
    card='<section id="operator-deadlines" aria-label="Validade de chaves e testes" style="margin:12px auto;padding:12px 16px;max-width:1400px;border:1px solid #b79858;border-radius:12px;font-size:13px"><strong>Chaves e testes · vencimentos</strong><div id="operator-deadlines-items">Conferindo prazos...</div></section>'
    s=replace_once(s,anchor,card+nl+anchor)
    js="""async function deadlinesLoad(){
const box=document.getElementById('operator-deadlines-items');
try{const r=await fetch('/api/alertas',{cache:'no-store'});if(!r.ok)throw Error();const d=await r.json();
if(!d.prazos)throw Error();box.replaceChildren();
for(const p of d.prazos.items||[]){const row=document.createElement('div');
row.textContent=p.label+': '+p.message+(p.expires_at?' · '+new Date(p.expires_at).toLocaleString('pt-BR',{timeZone:'America/Sao_Paulo'})+' (Brasília)':'');
if(['critical','expired'].includes(p.level))row.style.color='#b42318';box.append(row);}
if(d.prazos.error){const e=document.createElement('div');e.textContent=d.prazos.error;box.append(e);}
}catch(e){box.textContent='Prazos indisponíveis — confira o cadastro antes de usar.';}}
deadlinesLoad();setInterval(deadlinesLoad,60000);
"""
    s=replace_once(s,'async function mtLoad()',js.replace('{','{{').replace('}','}}').replace('\n',nl)+'async function mtLoad()')
    compile(s,str(server),'exec')
    put(ROOT/'iald_deadlines.py',(WORK/'iald_deadlines.py').read_bytes())
    config={'version':1,'checked_at':datetime.now().astimezone().isoformat(),'items':{
        'anthropic_key':{'expires_at':'2026-11-29T10:00:00-03:00','source':'Anthropic Console: Save your API key dialog, observed by browser','label':'IALD servidor'},
        'openai_key':{'expires_at':None},'testflight_internal':{'expires_at':None},'testflight_external':{'expires_at':None}}}
    target=ROOT/'iald_deadlines.json'
    assert not target.exists(),'Preserve existing deadline data'
    put(target,json.dumps(config,ensure_ascii=False,indent=2).encode())
    assert server.read_bytes()==before,'Server changed concurrently'
    put(server,s.encode())
    appjs=ROOT/'app/iald.js'; raw=appjs.read_bytes();j=raw.decode('utf-8');jn='\r\n' if b'\r\n' in raw else '\n'
    j=replace_once(j,"import { SYSTEM_PROMPT, PTBR_FIXES } from './kernel_prompt.js';","import { renderDeadlines } from './operational_deadlines.js';"+jn+"import { SYSTEM_PROMPT, PTBR_FIXES } from './kernel_prompt.js';")
    start=j.index('async function verificarAlertas()');end=j.index('// ═',start)
    block=j[start:end]
    block=replace_once(block,'    if (!r.ok) return;',"    if (!r.ok) { renderDeadlines(null, ![401, 403].includes(r.status)); return; }")
    block=replace_once(block,'    const d = await r.json();','    const d = await r.json();'+jn+'    renderDeadlines(d.prazos || null);')
    block=replace_once(block,'  } catch (e) { /* alerta nunca derruba o app */ }','  } catch (e) { renderDeadlines(null, true); /* alerta nunca derruba o app */ }')
    j=j[:start]+block+j[end:]
    assert appjs.read_bytes()==raw,'Client changed concurrently'
    put(appjs,j.encode())
    put(ROOT/'app/operational_deadlines.js',(WORK/'operational_deadlines.js').read_bytes())
    for name in ('iald.js','operational_deadlines.js'):
        put(ROOT/'iald-app/www'/name,(ROOT/'app'/name).read_bytes())
    paths=[server,appjs,ROOT/'iald_deadlines.py',target,ROOT/'app/operational_deadlines.js',ROOT/'iald-app/www/iald.js',ROOT/'iald-app/www/operational_deadlines.js']
    receipt={'at':datetime.now().astimezone().isoformat(),'new_request_overrides_old_js_hash_gate':True,
             'files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
             'deployed':False,'mobile_builds_pending':True,'unknown_deadlines':['openai_key','testflight_internal','testflight_external']}
    put(WORK/'deadlines_install.json',json.dumps(receipt,indent=2).encode())
    print(json.dumps({'files_updated':len(paths),'deployed':False}))

if __name__=='__main__':main()
