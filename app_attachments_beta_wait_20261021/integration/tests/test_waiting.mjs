import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=new URL('./',import.meta.url),source=fs.readFileSync(new URL('../stage/app/iald.js',root),'utf8').replace(/\r\n/g,'\n');
const extract=name=>{const start=source.indexOf(name);assert(start>=0,name);return source.slice(start,source.indexOf('\n}',start)+2);};
const durable=source.slice(source.indexOf('// Optional local module:'),source.indexOf('// Called only after a complete stream'));
const helpers=['function failedJobNotice','function applyChatJobDelivery','function createBetaWaitIndicator','function backgroundFailureText','function avisarBackground','function limparEsperaBackground','async function transmitir','async function* fluxoHttp'].map(extract).join('\n');
class Node {
 constructor(tag){this.tag=tag;this.dataset={};this.attrs={};this.childNodes=[];this.parentElement=null;this.className='';this.textContent='';}
 setAttribute(k,v){this.attrs[k]=v;}
 appendChild(n){n.remove();this.childNodes.push(n);n.parentElement=this;return n;}
 remove(){if(this.parentElement){const a=this.parentElement.childNodes;a.splice(a.indexOf(this),1);}this.parentElement=null;}
 get firstElementChild(){return this.childNodes[0];}
 get isConnected(){return !!this.parentElement;}
 set innerHTML(v){for(const n of [...this.childNodes])n.remove();}
 querySelector(s){return this.querySelectorAll(s)[0]||null;}
 querySelectorAll(s){return this.childNodes.flatMap(n=>[...(s.startsWith('.')&&n.className.split(' ').includes(s.slice(1))?[n]:[]),...n.querySelectorAll(s)]);}
 focus(){} isEqualNode(n){return this.textContent===n.textContent;} replaceChild(n,old){const i=this.childNodes.indexOf(old);old.remove();this.childNodes.splice(i,0,n);n.parentElement=this;}
}
function harness({failure=null,status='completed',resume=false,onPage=null,serverNotice=null}={}){
 const area=new Node('main'),made=[],input=new Node('textarea');
 const doc={hidden:false,createElement:t=>{const n=new Node(t);made.push(n);return n;},querySelector:s=>s==='#entrada'?input:s==='#conversa-interna'?area:null,querySelectorAll:s=>area.querySelectorAll(s)};
 const account='a'.repeat(64),id='12345678-1234-4234-8234-123456789abc',calls=[],saved=[],messages=[];let polls=0, persisted=null;
 const storage=new Map(),conv={id:'conversation1',background_owner:account,mensagens:[]};
 const ctx={document:doc,AbortController,AbortSignal,TextEncoder,TextDecoder,console,Date,Uint8Array,Response,
  setTimeout:()=>1,clearTimeout:()=>{},DEMO:false,ICONE_BETATGL:'./img/betatgl.png',S:{gerando:false,backgroundTurn:null,ativaId:conv.id},backgroundEpoch:0,backgroundOwner:account,backgroundNotice:'',activeBackgroundJob:null,
  el:(tag,cls,txt)=>{const n=doc.createElement(tag);n.className=cls||'';n.textContent=txt||'';return n;},$:s=>doc.querySelector(s),
  avisar:text=>{messages.push(text);const n=doc.createElement('div');n.className='faixa';const label=doc.createElement('span');label.textContent=text;n.appendChild(label);area.appendChild(n);return n;},
  conversaAtiva:()=>conv,conversaDoJob:()=>conv,ultimoSelo:()=>'',atualizarBotaoEnviar:()=>{},persistirConversasBackground:()=>{},corpoPedidoBackground:()=>({iald_conv:conv.id,messages:[{role:'user',content:'test'}]}),
  desenharMensagem:()=>{const line=doc.createElement('div'),body=doc.createElement('div');line.appendChild(body);for(const cls of ['trilha','conteudo']){const n=doc.createElement('div');n.className=cls;body.appendChild(n);}area.appendChild(line);return body;},
  rolarSePerto:()=>{},congelarTrilha:()=>{},passoTrilha:()=>{},splitThinking:s=>({text:s,thinking:''}),aplicarPtbr:s=>s,
  renderMarkdown:s=>{const n=doc.createElement('div');n.textContent=s;return n;},pintarAviso:(line,content,notice)=>{content.innerHTML='';messages.push(notice.texto);},salvarEntregaBackground:async(...a)=>{saved.push(a);const [job,answer,notice,status]=a;await ctx.backgroundJobs.delivered(job,()=>{ctx.applyChatJobDelivery(conv,job,{answer,notice,status});persisted=JSON.stringify(conv);});},listarConversas:()=>{},atualizarDica:()=>{},carregarMotor:()=>{},agendarRecuperacaoBackground:()=>{},
  request:async(path,options)=>{
   calls.push({path,options});
   if(path==='/api/chat-jobs/session')return new Response(JSON.stringify({account}));
   if(options.method==='POST'){
    if(failure==='post_network')throw Error('offline');
    if(failure==='post_http')return new Response('{}',{status:503});
    return new Response(JSON.stringify({id,conversation_id:conv.id,status:'queued'}));
   }
   polls++;onPage?.(ctx,made,polls);
   if(failure==='page_network')throw Error('offline');
   const state=polls===1?'running':status;
   const events=polls===1?[]:[{seq:1,data:JSON.stringify(serverNotice?{iald_aviso:serverNotice}:{choices:[{delta:{content:'Vermelho e azul.'}}]})},...(failure==='missing_done'?[]:[{seq:2,data:'[DONE]'}])];
   return new Response(JSON.stringify({id,conversation_id:conv.id,status:state,events,cursor:events.length,has_more:false}));
  },storage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)}};
 vm.createContext(ctx);vm.runInContext(durable+'\n'+helpers+`\nbackgroundJobs=createDurableChatJobs({request,storage,randomUUID:()=> '${id}',sleep:async()=>{},onState:record=>{if(activeBackgroundJob?.request_id===record.request_id)S.backgroundTurn?.betaWaiting?.setState(record.status);}});backgroundJobs.setOwner('${account}');`,ctx);
 return {ctx,area,made,calls,saved,messages,reload:()=>JSON.parse(persisted),async run(){let r=null;if(resume){r=await ctx.backgroundJobs.begin({iald_conv:conv.id,messages:[]});r.id=id;r.attempted=true;r.phase='streaming';r.status='running';}await ctx.transmitir([],r);},active(){return area.querySelectorAll('.beta-wait').length;}};
}
const results=[];async function test(name,fn){try{await fn();results.push({name,pass:true});}catch(e){results.push({name,pass:false,error:e.stack});}}
await test('real_transmit_and_durable_queued_running_completed_end_without_stale_notice',async()=>{
 let states=[];const h=harness({onPage:(ctx,made)=>states.push(made.find(n=>n.className==='beta-wait')?.dataset.state)});
 h.ctx.avisar('A resposta continua no servidor. Você pode sair e voltar.');
 await h.run();assert.equal(h.active(),0);assert.equal(h.ctx.S.gerando,false);assert.equal(h.saved[0][1].content,'Vermelho e azul.');assert(states.includes('queued')&&states.includes('running'));assert.equal(h.area.querySelectorAll('.faixa').length,0);assert.equal(h.calls.filter(c=>c.options.method==='POST'&&!c.path.endsWith('/ack')).length,1);
});
for(const status of ['failed','cancelled','interrupted','expired'])await test('terminal_'+status,async()=>{const h=harness({status});await h.run();assert.equal(h.active(),0);assert.equal(h.ctx.S.gerando,false);assert.equal(h.saved[0][3],status);assert.equal(h.saved[0][1],null);});
for(const failure of ['post_network','post_http','page_network','missing_done'])await test('failure_'+failure+'_stops_no_false_completion_no_resend',async()=>{const h=harness({failure});await h.run();assert.equal(h.active(),0);assert.equal(h.saved.length,0);assert.equal(h.calls.filter(c=>c.options.method==='POST'&&!c.path.endsWith('/ack')).length,1);assert(h.messages.some(m=>/confirm|Reconecte/.test(m)));assert(!h.messages.some(m=>/chegará|continua no servidor/.test(m)));});
await test('recovery_existing_job_no_new_post',async()=>{let initial;const h=harness({resume:true,onPage:(c,m)=>{initial??=m.find(n=>n.className==='beta-wait').dataset.state;}});await h.run();assert.equal(initial,'recovery');assert.equal(h.calls.filter(c=>c.options.method==='POST'&&!c.path.endsWith('/ack')).length,0);assert.equal(h.active(),0);});
await test('indicator_abort_is_terminal_and_accessible',()=>{const h=harness();const abort=new AbortController();const v=h.ctx.createBetaWaitIndicator({document:h.ctx.document,iconSrc:'official.png',signal:abort.signal,initialState:'queued'});h.area.appendChild(v.node);assert.equal(v.node.attrs.role,'status');assert.equal(v.node.attrs['aria-live'],'polite');assert.equal(v.node.childNodes[0].attrs['aria-hidden'],'true');abort.abort();v.setState('running');assert.equal(v.node.dataset.state,'stopped');assert.equal(h.active(),0);});
await test('cleanup_preserves_unrelated_errors',()=>{const h=harness();const wait=h.ctx.avisar('waiting');wait.dataset.backgroundWait='1';h.ctx.avisar('Arquivo não enviado.');h.ctx.limparEsperaBackground();assert.equal(h.area.querySelectorAll('.faixa').length,1);assert.equal(h.area.firstElementChild.firstElementChild.textContent,'Arquivo não enviado.');});
await test('css_motion_and_existing_font_rules_preserved',()=>{const before=fs.readFileSync(new URL('../../waiting/iald.css.baseline',root),'utf8').replace(/\r\n/g,'\n'),after=fs.readFileSync(new URL('../stage/app/iald.css',root),'utf8').replace(/\r\n/g,'\n');assert(after.startsWith(before));assert(after.includes('@media (prefers-reduced-motion: reduce) {\n  .beta-wait__icon { animation: none; transform: none; }'));assert(before.includes('font-size: 15.5px;'));assert(before.includes('font-size: 16px;'));});

const refusal={tipo:'pedido_invalido',texto:'A memória ou histórico não cabe no limite desta solicitação.'};
await test('failed_specific_notice_persisted_reloaded_no_model_answer',async()=>{
 const h=harness({status:'failed',serverNotice:refusal});await h.run();
 assert.equal(h.active(),0);assert.equal(h.saved[0][1],null);
 const reloaded=h.reload(),entry=Object.values(reloaded.chat_job_deliveries)[0];
 assert.equal(entry.status,'failed');assert.equal(entry.notice.tipo,refusal.tipo);assert.equal(entry.notice.texto,refusal.texto);assert.equal(entry.notice.retirar_resposta,true);
 assert.equal(reloaded.mensagens.length,0);assert(!h.messages.some(m=>m.includes('A geração não concluiu')));
 assert.equal(h.ctx.applyChatJobDelivery(reloaded,h.saved[0][0],{answer:null,notice:entry.notice,status:'failed'}),false);
 assert.equal(h.calls.filter(c=>c.path.endsWith('/ack')).length,1);
});
for(const status of ['cancelled','interrupted','expired'])await test('specific_failed_notice_not_revived_'+status,async()=>{
 const h=harness({status,serverNotice:refusal});await h.run();const entry=Object.values(h.reload().chat_job_deliveries)[0];
 assert.equal(entry.status,status);assert.notEqual(entry.notice.tipo,'pedido_invalido');assert.equal(h.reload().mensagens.length,0);assert.equal(h.active(),0);
});
await test('failed_notice_invalid_or_pending_falls_back',()=>{
 const h=harness();for(const aviso of [null,{},[],{tipo:'pedido_invalido',texto:''},{tipo:'em_andamento',texto:'aguarde'}]) assert.equal(h.ctx.failedJobNotice({terminal:true,status:'failed'},aviso),null);
 assert.equal(h.ctx.failedJobNotice({terminal:false,status:'failed'},refusal),null);
});

const report={status:results.every(r=>r.pass)?'PASS':'FAIL',tests:results.length,results,scope:'Actual staged transmitir + durable job lifecycle and indicator in Node VM; synthetic DOM/network. No physical browser rendering claim.',provider_calls:0,network_calls:0};fs.writeFileSync(new URL('WAITING_RESULTS.json',root),JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(report.status!=='PASS')process.exitCode=1;
