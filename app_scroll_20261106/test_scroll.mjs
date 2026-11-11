import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/rotol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const W=path.dirname(fileURLToPath(import.meta.url));
const fn=(s,n)=>{const start=s.indexOf('function '+n+'(');assert(start>=0,n);return s.slice(start,s.indexOf('\n}',start)+2);};
const browser=await chromium.launch({headless:true,executablePath:'C:/Users/rotol/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe'});
const results=[];
async function fixture(kind){
 const s=fs.readFileSync(path.join(W,kind,'iald.js'),'utf8').replaceAll('\r\n','\n');
 const page=await browser.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});
 await page.route('**/*',r=>r.abort());
 await page.setContent(`<style>body{margin:0}#conversa{height:600px;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}#conversa-interna{padding:20px}p{margin:0;height:40px}</style><main id="conversa"><div id="conversa-interna"></div></main><button id="ir-fim">Fim</button>`);
 let binding;
 if(kind==='stage')binding=fn(s,'createConversationScroll')+`\nconversationScroll=createConversationScroll({container:$('#conversa'),button:$('#ir-fim'),getFollowing:()=>S.colarNoFim,setFollowing:v=>S.colarNoFim=v,isEditing:()=>!!document.querySelector('.msg-edicao-texto')});`;
 else binding=s.slice(s.indexOf('  // rolagem\n  const conversa'),s.indexOf('\n  // exportacao',s.indexOf('  // rolagem\n  const conversa')));
 const code=`const $=s=>document.querySelector(s);
 const S={colarNoFim:true,ativaId:'test',conversas:[],gerando:false};
 let renderedPublicView=null,publicRenderRevision=0,renderingConversation=false,conversationScroll=null;
 let backgroundOwner='a'.repeat(64),backgroundEpoch=0, opens=0, privateMode=false;
 const c={id:'test',mensagens:Array.from({length:60},(_,i)=>({role:'assistant',content:'Linha '+i}))}; S.conversas=[c];
 const ownerSyncCurrentView=()=>{},atualizarBotaoEnviar=()=>{},conversaAtiva=()=>c,atualizarTitulo=()=>{},ownerPrivateActive=()=>privateMode,mediaRestoreDrafts=async()=>{},avisar=()=>{},boasVindas=()=>{},atualizarDica=()=>{},pintarAviso=()=>{};
 function desenharMensagem(role,text){const p=document.createElement('p');p.textContent=text;$('#conversa-interna').append(p);rolarSePerto();return p;}
 ${fn(s,'pertoDoFim')}
 ${fn(s,'rolarSePerto')}
 ${fn(s,'abrirConversa').replace('function abrirConversa() {','function abrirConversa() { opens++;')}
 ${binding}
 const DEMO=false,portaoNecessario=()=>false,tokenApp=()=>'',fetchIALD=async()=>({ok:true,status:200,json:async()=>({account:backgroundOwner})}),detached=()=>Error('detached'),desanexarRespostasBackground=()=>{},PendingChatJobError=Error;
 const mediaRecoverLegacyHistory=async()=>{},novaConversa=()=>{},listarConversas=()=>{},refreshNativeNotificationsUI=()=>{},artifactAccessUI=null;
 ${'async '+fn(s,'identificarContaBackground')}
 window.h={S,c,open:abrirConversa,identify:identificarContaBackground,follow:rolarSePerto,controller:conversationScroll,privateMode:v=>{privateMode=v},opens:()=>opens,
  add:()=>desenharMensagem('ai','novo texto'),top:()=>$('#conversa').scrollTop,end:()=>$('#conversa').scrollHeight-$('#conversa').clientHeight,
  up:n=>{$('#conversa').scrollTop-=n},down:()=>{$('#conversa').scrollTop=$('#conversa').scrollHeight},
  touch:(type,y)=>{const e=new Event(type,{bubbles:true});Object.defineProperty(e,'touches',{value:type==='touchend'||type==='touchcancel'?[]:[{clientY:y}]});$('#conversa').dispatchEvent(e)}};
 abrirConversa();`;
 await page.evaluate(code);await page.waitForTimeout(50);return page;
}
async function check(name,fnc){await fnc();results.push({name,status:'PASS'});}
try{
 await check('reproduced_original_small_upward_scroll_stolen',async()=>{const p=await fixture('baseline');await p.evaluate(()=>h.up(30));await p.waitForTimeout(30);const before=await p.evaluate(()=>h.top());await p.evaluate(()=>h.add());assert(await p.evaluate(()=>h.top())>before+30);await p.close();});
 await check('reproduced_original_completed_refresh_jumps_to_end',async()=>{const p=await fixture('baseline');await p.evaluate(()=>h.up(500));await p.waitForTimeout(30);const before=await p.evaluate(()=>h.top());await p.evaluate(()=>h.identify());await p.waitForTimeout(50);assert(await p.evaluate(()=>h.top())>before+400);await p.close();});
 await check('stream_does_not_capture_small_upward_scroll',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(30));await p.waitForTimeout(30);const before=await p.evaluate(()=>h.top());await p.evaluate(()=>{for(let i=0;i<15;i++)h.add()});assert.equal(await p.evaluate(()=>h.top()),before);await p.close();});
 await check('touch_pauses_before_scroll_event_and_keeps_momentum_free',async()=>{const p=await fixture('stage');const before=await p.evaluate(()=>h.top());await p.evaluate(()=>{h.touch('touchstart',100);h.add();h.touch('touchmove',140);h.up(40);h.touch('touchend',140)});await p.waitForTimeout(30);const read=await p.evaluate(()=>h.top());await p.evaluate(()=>{h.add();h.follow()});assert(read<before);assert.equal(await p.evaluate(()=>h.top()),read);await p.close();});
 await check('wheel_and_keyboard_pause_before_next_frame',async()=>{const p=await fixture('stage');for(const event of ['wheel','keydown']){await p.click('#ir-fim');const before=await p.evaluate(()=>h.top());await p.evaluate(e=>{if(e==='wheel')document.querySelector('#conversa').dispatchEvent(new WheelEvent('wheel',{deltaY:-20}));else document.dispatchEvent(new KeyboardEvent('keydown',{key:'PageUp'}));h.add()},event);assert.equal(await p.evaluate(()=>h.top()),before);}await p.close();});
 await check('recovery_completed_identity_preserves_dom_position_and_selection',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(650));await p.waitForTimeout(30);await p.evaluate(()=>{window.originalRow=document.querySelector('#conversa-interna p');const r=document.createRange();r.selectNodeContents(originalRow);getSelection().addRange(r)});const before=await p.evaluate(()=>({top:h.top(),opens:h.opens(),selection:getSelection().toString()}));for(let i=0;i<4;i++)await p.evaluate(()=>h.identify());await p.waitForTimeout(50);assert.deepEqual(await p.evaluate(()=>({top:h.top(),opens:h.opens(),selection:getSelection().toString()})),before);assert(await p.evaluate(()=>originalRow===document.querySelector('#conversa-interna p')));await p.close();});
 await check('end_button_resumes_following_after_manual_reading',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(450));await p.waitForTimeout(30);await p.click('#ir-fim');await p.evaluate(()=>h.add());assert.equal(await p.evaluate(()=>h.top()),await p.evaluate(()=>h.end()));await p.close();});
 await check('manual_down_to_exact_end_resumes_but_near_end_does_not',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(450));await p.waitForTimeout(30);await p.evaluate(()=>h.down());await p.waitForTimeout(30);await p.evaluate(()=>h.add());assert.equal(await p.evaluate(()=>h.top()),await p.evaluate(()=>h.end()));await p.close();});
 await check('same_view_rebuild_preserves_reading_position',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(400));await p.waitForTimeout(30);const before=await p.evaluate(()=>h.top());await p.evaluate(()=>h.open());await p.waitForTimeout(50);assert.equal(await p.evaluate(()=>h.top()),before);await p.close();});
 await check('late_open_animation_frame_does_not_override_user_gesture',async()=>{const p=await fixture('stage');await p.evaluate(()=>{h.S.ativaId='new';h.open();h.touch('touchstart',100);h.up(120);h.touch('touchmove',140);h.touch('touchend',140)});const before=await p.evaluate(()=>h.top());await p.waitForTimeout(50);assert.equal(await p.evaluate(()=>h.top()),before);await p.close();});
 await check('resize_selection_and_editing_do_not_force_follow',async()=>{const p=await fixture('stage');await p.evaluate(()=>h.up(450));await p.waitForTimeout(30);const before=await p.evaluate(()=>h.top());await p.evaluate(()=>{document.querySelector('#conversa').style.height='480px';h.follow()});assert.equal(await p.evaluate(()=>h.top()),before);await p.evaluate(()=>{h.S.colarNoFim=true;const t=document.createElement('textarea');t.className='msg-edicao-texto';document.body.append(t);h.add()});assert.equal(await p.evaluate(()=>h.top()),before);await p.close();});
 const pins={};for(const name of ['iald.js','owner_office.js'])pins[name]=crypto.createHash('sha256').update(fs.readFileSync(path.join(W,'stage',name))).digest('hex');
 fs.writeFileSync(path.join(W,'TEST_SCROLL.json'),JSON.stringify({status:'PASS',engine:'Chromium actual DOM, touch events synthetic',tests:results,pins,scope:'No provider, no user conversation; tests exercise extracted production functions and browser scroll layout'},null,2));
 console.log(JSON.stringify({status:'PASS',tests:results.length}));
}catch(error){console.error(error);fs.writeFileSync(path.join(W,'TEST_SCROLL_FAILURE.json'),JSON.stringify({tests:results,error:String(error)},null,2));process.exitCode=1;}finally{await browser.close()}
