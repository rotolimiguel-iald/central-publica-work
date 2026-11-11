import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const R=path.dirname(fileURLToPath(import.meta.url)), W=path.dirname(R);
const {chromium}=createRequire(import.meta.url)('C:/Users/rotol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const js=fs.readFileSync(path.join(W,'stage/iald.js'),'utf8').replaceAll('\r\n','\n');
const owner=fs.readFileSync(path.join(W,'stage/owner_office.js'),'utf8').replace(/^export /gm,'');
const fn=n=>{const a=js.indexOf('function '+n+'(');return js.slice(a,js.indexOf('\n}',a)+2)};
const browser=await chromium.launch({headless:true,executablePath:'C:/Users/rotol/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe'});
const tests=[];let requests=0;
async function fixture(){
 const p=await browser.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});
 await p.route('**/*',r=>{requests++;return r.abort()});
 await p.setContent('<style>#conversa{height:600px;overflow:auto;overflow-anchor:none}.msg{min-height:48px}#conversa-interna[hidden]{display:none}</style><div id="cab-estado"></div><main id="conversa"><div id="conversa-interna">PUBLIC-SYNTHETIC</div></main><button id="ir-fim">Fim</button>');
 await p.evaluate(owner+'\n'+fn('createConversationScroll')+`
 let following=true, callbackCount=0, view='fixture-a', pendingGet=null, pendingHistory=null, historyCount=40;
 const handle='11111111-1111-4111-8111-111111111111';
 const container=document.querySelector('#conversa');
 const policy=createConversationScroll({container,button:document.querySelector('#ir-fim'),getFollowing:()=>following,setFollowing:v=>following=v,isEditing:()=>false});
 const messages=()=>Array.from({length:historyCount},(_,i)=>({role:'assistant',status:'completed',content:'PRIVATE-SYNTHETIC-'+i}));
 const api={capability:async()=>({available:true}), resetIdentity(){},preflight:async()=>({route:'private',private_handle:handle}),
 history:()=>pendingHistory?new Promise(r=>{window.resolveHistory=r}):Promise.resolve({private_conversation_id:handle,items:messages()}),
 start:async()=>({job_id:'synthetic-job',private_conversation_id:handle,status:'running'}),
 get:()=>pendingGet?new Promise(r=>{window.resolveGet=r}):Promise.resolve({status:'completed',answer:'NEW PRIVATE SYNTHETIC ANSWER'})};
 const mounted=mountOwnerMainChat({api,uuid:()=>handle,getConversationId:()=>view,schedule:()=>1,cancel:()=>{},onContentChanged:()=>{callbackCount++;policy.follow()}});
 window.h={mounted,policy,api,handle,container,get following(){return following},get callbacks(){return callbackCount},
 historyCount:n=>historyCount=n,holdGet:()=>pendingGet=true,holdHistory:()=>pendingHistory=true,
 switchView:()=>{view='fixture-b';mounted.newConversation();policy.reset()},
 touch:(type,y)=>{const e=new Event(type);Object.defineProperty(e,'touches',{value:type==='touchend'||type==='touchcancel'?[]:[{clientY:y}]});container.dispatchEvent(e)},
 top:()=>container.scrollTop,end:()=>container.scrollHeight-container.clientHeight};`);
 await p.evaluate(()=>h.mounted.controller.recover(h.handle));await p.waitForTimeout(40);return p;
}
async function test(name,f){let p;try{p=await fixture();const detail=await f(p);tests.push({name,status:'PASS',detail});}catch(e){tests.push({name,status:'FAIL',error:String(e)});}finally{await p?.close()}}
try{
 await test('real_mount_initial_private_follow_shared_callback',async p=>{assert.equal(await p.evaluate(()=>h.top()),await p.evaluate(()=>h.end()));assert(await p.evaluate(()=>h.callbacks)>0);assert(await p.evaluate(()=>document.querySelector('#conversa-interna').hidden));});
 await test('real_mount_pending_and_completed_preserve_upward_reading',async p=>{await p.evaluate(()=>{h.container.dispatchEvent(new WheelEvent('wheel',{deltaY:-30}));h.container.scrollTop-=30});await p.waitForTimeout(30);const top=await p.evaluate(()=>h.top());await p.evaluate(()=>h.mounted.controller.submit({message:'synthetic followup'}));await p.evaluate(()=>h.mounted.controller.poll());assert.equal(await p.evaluate(()=>h.top()),top);assert.equal(await p.evaluate(()=>h.following),false);});
 await test('real_mount_touch_before_scroll_and_delayed_completion',async p=>{await p.evaluate(async()=>{await h.mounted.controller.submit({message:'synthetic'});h.holdGet();window.pendingPoll=h.mounted.controller.poll();h.touch('touchstart',100);h.touch('touchmove',180);h.container.scrollTop-=80;h.touch('touchend',180)});await p.waitForTimeout(30);const top=await p.evaluate(()=>h.top());await p.evaluate(async()=>{resolveGet({status:'completed',answer:'SYNTHETIC NEW'.repeat(100)});await pendingPoll});assert.equal(await p.evaluate(()=>h.top()),top);});
 await test('real_mount_same_history_keeps_nodes_selection_position',async p=>{await p.evaluate(()=>{h.container.scrollTop-=400});await p.waitForTimeout(30);await p.evaluate(()=>{window.row=document.querySelector('[data-owner-private-canvas] .conteudo');const r=document.createRange();r.selectNodeContents(row);getSelection().addRange(r)});const before=await p.evaluate(()=>({top:h.top(),text:getSelection().toString(),callbacks:h.callbacks}));await p.evaluate(()=>h.mounted.controller.recover(h.handle));assert.deepEqual(await p.evaluate(()=>({top:h.top(),text:getSelection().toString(),callbacks:h.callbacks})),before);assert(await p.evaluate(()=>row===document.querySelector('[data-owner-private-canvas] .conteudo')));});
 await test('real_mount_end_button_resumes_completed_answer_follow',async p=>{await p.evaluate(()=>{h.container.scrollTop-=300});await p.waitForTimeout(30);await p.click('#ir-fim');await p.evaluate(async()=>{await h.mounted.controller.submit({message:'synthetic'});await h.mounted.controller.poll()});assert.equal(await p.evaluate(()=>h.top()),await p.evaluate(()=>h.end()));});
 await test('private_stale_poll_after_identity_reset_cannot_resurrect',async p=>{await p.evaluate(async()=>{await h.mounted.controller.submit({message:'synthetic'});h.holdGet();window.pendingPoll=h.mounted.controller.poll();h.mounted.reset();resolveGet({status:'completed',answer:'STALE-PRIVATE-ANSWER'});await pendingPoll});assert.equal(await p.evaluate(()=>h.mounted.controller.snapshot().privacy),false);assert.equal(await p.evaluate(()=>document.body.textContent.includes('STALE-PRIVATE-ANSWER')),false);assert.equal(await p.evaluate(()=>document.querySelector('[data-owner-private-canvas]').hidden),true);});
 await test('private_stale_history_after_view_switch_cannot_resurrect',async p=>{await p.evaluate(()=>{h.holdHistory();window.pendingRecovery=h.mounted.controller.recover(h.handle);h.switchView()});await p.evaluate(async()=>{resolveHistory({private_conversation_id:h.handle,items:[{role:'assistant',content:'STALE-HISTORY'}]});await pendingRecovery});assert.equal(await p.evaluate(()=>h.mounted.controller.snapshot().privacy),false);assert.equal(await p.evaluate(()=>document.body.textContent.includes('STALE-HISTORY')),false);});
 await test('private_auth_denial_clears_rows_and_stale_completion',async p=>{await p.evaluate(async()=>{await h.mounted.controller.submit({message:'synthetic'});h.holdGet();window.pendingPoll=h.mounted.controller.poll();h.api.capability=async()=>({available:false,reauthenticate:false});await h.mounted.refresh();resolveGet({status:'completed',answer:'STALE-DENIED'});await pendingPoll});assert.equal(await p.evaluate(()=>h.mounted.controller.snapshot().mode),'private-locked');assert.equal(await p.evaluate(()=>document.querySelectorAll('[data-owner-private-canvas] .msg').length),0);assert.equal(await p.evaluate(()=>document.body.textContent.includes('STALE-DENIED')),false);});
 await test('touch_cancel_stays_paused_and_input_keyboard_does_not_pause',async p=>{await p.evaluate(()=>{h.touch('touchstart',10);h.touch('touchcancel',10)});assert.equal(await p.evaluate(()=>h.following),false);await p.click('#ir-fim');await p.evaluate(()=>{const input=document.createElement('textarea');document.body.append(input);input.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}))});assert.equal(await p.evaluate(()=>h.following),true);});
}finally{await browser.close();fs.writeFileSync(path.join(R,'PRIVATE_REGRESSION.json'),JSON.stringify({status:tests.every(t=>t.status==='PASS')?'PASS':'FAIL',tests,networkRequestsAborted:requests,scope:'Actual complete owner_office module and mountOwnerMainChat; extracted shared production scroll controller; synthetic API injection; no real case/provider/authenticated browser'},null,2));console.log(JSON.stringify(tests));}
