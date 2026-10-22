"""Offline real staged host capabilities -> JSON -> unchanged client -> IDB reload."""
from pathlib import Path
import hashlib,json,subprocess,sys,uuid
S=Path(__file__).resolve().parent; W=S.parent
sys.path.insert(0,str(W/'host_stage'))
import test_host as host_tests
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def main():
    out=S/('host_client_replay_'+uuid.uuid4().hex);out.mkdir()
    case=host_tests.HostTests('test_complete_motor_limits_shape_for_client_without_store_writes')
    case.setUp()
    try:
        ns=dict(PRIVATE_MEDIA_HOST=case.host,
            app_providers=host_tests.NS(allowed=lambda *a:True,limits=lambda *a,**kw:{}),
            app_router=host_tests.NS(allowed=lambda *a:True,limits=lambda:{}),
            iald_motores=host_tests.NS(consentiu=lambda *a:True))
        host_tests.extract({'_mimo_media_limits'},ns)
        limits=ns['_mimo_media_limits'](case.records['alice'],'alice',automatic=True)
        payload={'motor':{'limites':limits}}
        assert limits['media_capabilities']['media_scope']==case.host.capabilities('alice')['media_scope']
        assert not case.host.root.exists()
        (out/'HOST_JSON.json').write_bytes(json.dumps(payload).encode())
        # Source host function and real backend scope codec; mock auth/account only.
        js=r'''
const fs=require('node:fs'),path=require('node:path');let checks=0;const assert=new Proxy(require('node:assert/strict'),{get(o,k){const v=Reflect.get(o,k);return typeof v==='function'?(...a)=>{checks++;return v(...a);}:v;}});
const {setup,file}=require('../test_private_media_R6.cjs');
const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'HOST_JSON.json')));
(async()=>{
 const t=setup(); t.context.S.motor.limites=raw.motor.limites;
 assert.match(t.h.mediaStorageScope(),/^[0-9a-f]{32}$/);
 const draft=await t.h.lerMidiaLocal(file(),'audio');
 assert.equal(t.db.rows.size,1);assert.equal(t.calls.length,0);
 const fresh=setup(t.db);fresh.context.S.motor.limites=JSON.parse(JSON.stringify(raw.motor.limites));
 await fresh.h.mediaRestoreDrafts(fresh.context.S.conversas[0]);assert.equal(fresh.context.S.anexos.length,1);
 assert.equal(fresh.db.rows.size,1);assert.equal(fresh.calls.length,0);
 const missing=setup(); delete raw.motor.limites.media_capabilities.media_scope;
 missing.context.S.motor.limites=raw.motor.limites;
 await missing.h.lerMidiaLocal(file(),'audio');assert.equal(missing.db.opens,0);
 assert.ok(missing.warnings.length>0);
 fs.writeFileSync(path.join(__dirname,'NODE_RESULT.json'),JSON.stringify({status:'PASS',assertions:checks,host_scope_idb_reload:true,missing_scope_ram_warning:true,network_calls:0}),{flag:'wx'});
})().catch(e=>{console.error(e);process.exitCode=1});
'''
        (out/'test.cjs').write_bytes(js.encode())
        p=subprocess.run(['node',str(out/'test.cjs')],capture_output=True)
        (out/'NODE_LOG.txt').write_bytes(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError('Host-client replay failed; inspect offline log '+str(out))
        result=dict(status='PASS',host=pin(W/'host_stage/iald_web_server.py'),
            host_helper=pin(W/'host_stage/new_private_media_host.py'),
            client=pin(S/'release_R6/app/iald.js'),fixture=pin(out/'HOST_JSON.json'),
            result=pin(out/'NODE_RESULT.json'),scope='Real staged _mimo_media_limits + Host.capabilities -> JSON -> actual embedded client helper; account/auth mocked, no live host/UI claim.')
        (out/'RESULT.json').write_bytes(json.dumps(result,indent=2).encode());print(json.dumps(pin(out/'RESULT.json')))
    finally:case.doCleanups()
if __name__=='__main__':main()
