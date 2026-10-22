import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {test} from 'node:test';
const source=readFileSync('C:/IALD/projetos_pyhton/IALD/app/iald.js','utf8');
const funcs=source.slice(source.indexOf('async function responderConsentimento('),source.indexOf('async function alternarConsentimento('));
function setup(mode='success') {
 const status={textContent:'',hidden:true},button={disabled:false,textContent:'Concordo e continuar'};
 const state={consentimentoFolha:{provedor:'Anthropic',versao:1},motor:{provedor:'Anthropic',consentimento:{provedor:'Anthropic',dado:false},consentimentos:[]}};
 const calls=[];let closed=0,replayed=0;
 const context={S:state,Number,AbortSignal,document:{getElementById:id=>id==='btn-consentir'?button:status},
 avisar:()=>{},pintarMotor:()=>{},fecharFolhas:()=>closed++,reenviarUltima:()=>replayed++,
 carregarMotor:async()=>{},consentimentoDe:()=>({texto:'new terms',provedor:'Anthropic',versao:2}),
 abrirConsentimento:(t,p,v)=>{state.consentimentoFolha={provedor:p,versao:v}},
 fetchIALD:async(path,opts)=>{
  calls.push({path,body:JSON.parse(opts.body)});
  await new Promise(r=>setTimeout(r,5));
  if(mode==='offline')throw new Error('offline');
  return {ok:mode!=='conflict',status:mode==='conflict'?409:200,json:async()=>{
   if(mode==='invalid')throw new Error('not json');
   return {ok:true,consentido:true,provedor:mode==='wrong-provider'?'OpenAI':'Anthropic'};
  }};
 }};
 vm.createContext(context);vm.runInContext(funcs,context);
 return {context,state,calls,status,button,get closed(){return closed},get replayed(){return replayed}};
}
test('one confirmed provider-specific request despite duplicate click',async()=>{
 const f=setup();let removed=0;f.state.avisoConsentimento={remove:()=>removed++};
 const p=f.context.consentirEContinuar();assert.equal(f.button.disabled,true);
 await f.context.consentirEContinuar();await p;
 assert.equal(f.calls.length,1);assert.deepEqual(f.calls[0].body,{aceito:true,provedor:'Anthropic',versao:1});
 assert.equal(f.state.motor.consentimento.dado,true);assert.equal(f.closed,1);assert.equal(f.replayed,1);assert.equal(removed,1);assert.equal(f.button.disabled,false);
});
for(const mode of ['offline','invalid','wrong-provider','conflict'])test(mode+' keeps chat closed until valid consent',async()=>{
 const f=setup(mode);await f.context.consentirEContinuar();
 assert.equal(f.closed,0);assert.equal(f.replayed,0);assert.equal(f.state.motor.consentimento.dado,false);
 assert.equal(f.button.disabled,false);assert.ok(f.status.textContent);assert.equal(f.status.hidden,false);
 if(mode==='conflict')assert.equal(f.state.consentimentoFolha.versao,2);
});
test('incomplete notice never posts a default OpenAI consent',async()=>{
 const f=setup();f.state.consentimentoFolha=null;await f.context.consentirEContinuar();assert.equal(f.calls.length,0);assert.equal(f.closed,0);
});
