import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';import assert from 'node:assert/strict';import crypto from 'node:crypto';
const require=createRequire(import.meta.url),{chromium}=require('C:/Users/rotol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const W=path.dirname(fileURLToPath(import.meta.url)),A='C:/IALD/projetos_pyhton/IALD/app';
const browser=await chromium.launch({headless:true,executablePath:'C:/Users/rotol/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe'});
const page=await browser.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const errors=[],requests=[];
page.on('pageerror',e=>errors.push(String(e)));
await page.route('**/*',async route=>{
 const u=new URL(route.request().url());requests.push(u.pathname);
 if(u.origin!=='http://127.0.0.1:9854')return route.abort();
 if(u.pathname.startsWith('/api/'))return route.fulfill({status:403,contentType:'application/json',body:'{"error":"synthetic_fixture_no_private_access"}'});
 const name=u.pathname.slice(1)||'index.html';if(name.includes('..'))return route.abort();
 const file=['iald.js','owner_office.js'].includes(name)?path.join(W,'stage',name):path.join(A,name);
 if(!fs.existsSync(file)||!fs.statSync(file).isFile())return route.abort();
 let body=fs.readFileSync(file);
 if(name==='iald.js')body=Buffer.concat([body,Buffer.from('\nwindow.scrollFixture={state:S,start:()=>transmitir([{role:"user",content:"Fixture de rolagem"}]),refresh:abrirConversa};')]);
 const types={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf'};
 return route.fulfill({body,contentType:types[path.extname(file)]||'application/octet-stream'});
});
await page.addInitScript(()=>{localStorage.setItem('iald_conversas_v2',JSON.stringify([{id:'scroll-synthetic',titulo:'Teste de leitura',mensagens:[{role:'assistant',content:Array.from({length:90},(_,i)=>`Parágrafo ${i+1}: conteúdo sintético para conferir a leitura e a rolagem.`).join('\n\n')}]}]));localStorage.setItem('iald_conversa_ativa_v2',JSON.stringify('scroll-synthetic'));});
try{
 await page.goto('http://127.0.0.1:9854/index.html?demo');await page.waitForFunction(()=>window.scrollFixture);
 await page.waitForTimeout(150);assert.equal(errors.length,0,errors.join('\n'));
 await page.evaluate(()=>{window.fixtureDone=false;scrollFixture.start().then(()=>{window.fixtureDone=true})});
 await page.waitForFunction(()=>scrollFixture.state.gerando);
 const box=await page.locator('#conversa').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,-600);await page.waitForTimeout(200);
 const before=await page.locator('#conversa').evaluate(e=>({top:e.scrollTop,gap:e.scrollHeight-e.clientHeight-e.scrollTop}));assert(before.gap>200);
 const positions=[];for(let i=0;i<5;i++){await page.waitForTimeout(600);positions.push(await page.locator('#conversa').evaluate(e=>e.scrollTop));}
 await page.waitForFunction(()=>window.fixtureDone);assert(positions.every(top=>Math.abs(top-before.top)<2),JSON.stringify({before,positions}));
 await page.mouse.wheel(0,-400);await page.waitForTimeout(200);const after=await page.locator('#conversa').evaluate(e=>e.scrollTop);
 await page.evaluate(()=>scrollFixture.refresh());await page.waitForTimeout(100);assert.equal(await page.locator('#conversa').evaluate(e=>e.scrollTop),after);
 assert(await page.locator('.katex').count()>0,'Math renderer remains active');
 await page.screenshot({path:path.join(W,'FULL_CLIENT_READING.png')});
 await page.locator('#ir-fim').click();await page.waitForTimeout(100);assert(await page.locator('#conversa').evaluate(e=>e.scrollHeight-e.clientHeight-e.scrollTop<3));
 assert.equal(errors.length,0,errors.join('\n'));
 fs.writeFileSync(path.join(W,'TEST_FULL_CLIENT.json'),JSON.stringify({status:'PASS',viewport:{width:390,height:844},scope:'Entire production client/bootstrap/Markdown/KaTeX and demo SSE, isolated synthetic history; APIs refused in fixture',positions,readingTop:before.top,finishedReadingTop:after,errors,script_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(W,'stage/iald.js'))).digest('hex')},null,2));console.log('PASS full client stream and completion scrolling');
}finally{await browser.close()}
