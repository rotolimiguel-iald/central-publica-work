"""Offline staged Flask adapter -> JSON -> R6 client, no live server or provider."""
from pathlib import Path
import io,json,hashlib,subprocess,sys,uuid
from unittest.mock import patch
S=Path(__file__).resolve().parent;W=S.parent
sys.path.insert(0,str(W/'backend_stage'))
import test_private_routes as tests
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
class ReadCounter(io.BytesIO):
    reads=0
    def read(self,*a):self.reads+=1;return super().read(*a)
    def readinto(self,*a):self.reads+=1;return super().readinto(*a)
def main():
    out=S/('scope_e2e_'+uuid.uuid4().hex);out.mkdir()
    sources=[pin(W/'backend_stage'/n) for n in ['private_media_routes.py','private_media_store.py']]
    case=tests.RouteTests();case.setUp();checks=[]
    try:
        response=case.upload();assert response.status_code==201
        data=response.get_json();assert data['media_scope']==case.token;checks.append('positive_actual_adapter_201_scope_echo')
        for label,query,owner,generation in [
            ('cookie_A_to_B',case.token,'two','g1'),('same_name_new_generation',case.token,'one','g2'),
            ('missing','','one','g1'),('malformed','bad','one','g1'),('wrong_32hex','f'*32,'one','g1')]:
            stream=ReadCounter(tests.small_wav());url='/api/private-media?conversation_id=c_first'
            if query:url+='&expected_media_scope='+query
            headers={**case.headers,'X-Owner':owner,'X-Generation':generation}
            with patch.object(case.store,'put',wraps=case.store.put) as put:
                r=case.client.open(url,method='POST',input_stream=stream,content_length=len(stream.getvalue()),headers=headers)
                assert r.status_code==403 and stream.reads==0 and put.call_count==0
                checks.append(label+'_403_zero_body_and_store_reads')
        with patch.object(case.store,'metadata',wraps=case.store.metadata) as meta:
            r=case.client.get('/api/private-media/'+data['media_ref']+'?conversation_id=c_first&expected_media_scope='+case.token,headers={**case.headers,'X-Owner':'two'})
            assert r.status_code==403 and meta.call_count==0;checks.append('GET_cookie_switch_403_before_metadata')
        r=case.client.get('/api/private-media/'+data['media_ref']+'?conversation_id=c_first&expected_media_scope='+case.token,headers=case.headers)
        assert r.status_code==200 and r.json['media_scope']==case.token;checks.append('GET_positive_actual_adapter_echo')
        (out/'RESPONSE.json').write_bytes(json.dumps(data).encode())
        script=r'''
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {setup,file}=require('../test_private_media_R6.cjs');
(async()=>{const part=JSON.parse(fs.readFileSync(path.join(__dirname,'RESPONSE.json'))),t=setup();
 t.context.S.motor.limites.media_capabilities.media_scope=part.media_scope;
 const blob=new Blob([new Uint8Array(part.bytes)],{type:part.mime});Object.defineProperty(blob,'name',{value:'fixture.wav'});
 const draft=await t.h.lerMidiaLocal(blob,'audio');
 t.context.fetchIALD=async(url)=>{assert.equal(new URL(url,'https://offline.invalid').searchParams.get('expected_media_scope'),part.media_scope);return {ok:true,json:async()=>structuredClone(part)}};
 const canonical=await t.h.mediaUpload(draft,'owner-A','conv-A');assert.equal(canonical.media_ref,part.media_ref);assert.equal('media_scope' in canonical,false);
 const fresh=setup(t.db);fresh.context.S.motor.limites.media_capabilities.media_scope=part.media_scope;
 await fresh.h.mediaRestoreDrafts(fresh.context.S.conversas[0]);assert.equal(fresh.context.S.anexos.length,1);
 fs.writeFileSync(path.join(__dirname,'CLIENT_RESULT.json'),JSON.stringify({status:'PASS',assertions:4,real_route_response_consumed:true,scope_stripped:true,reload:true}),{flag:'wx'});
})().catch(e=>{console.error(e);process.exitCode=1});
'''
        (out/'test.cjs').write_bytes(script.encode());p=subprocess.run(['node',str(out/'test.cjs')],capture_output=True)
        (out/'NODE_LOG.txt').write_bytes(p.stdout+p.stderr);assert p.returncode==0
        assert sources==[pin(x['path']) for x in sources],'Backend changed during control'
        result=dict(status='PASS_OFFLINE_REAL_ADAPTER_CLIENT',checks=checks,backend=sources,client=pin(S/'release_R6/app/iald.js'),
            client_result=pin(out/'CLIENT_RESULT.json'),provider_calls=0,real_network_calls=0,
            authority='Builder reproduction of independent finding; independent final acceptance remains required.')
        p=out/'INDEPENDENT_CONTROLS_R1.json';p.write_bytes(json.dumps(result,indent=2).encode());print(json.dumps(pin(p)))
    finally:case.tearDown()
if __name__=='__main__':main()
