import { readFileSync, writeFileSync, renameSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { extractFunction } from './editor_fixture.mjs';
const js = readFileSync(new URL('../stage/iald.js', import.meta.url), 'utf8');
const css = readFileSync(new URL('../stage/iald.css', import.meta.url), 'utf8');
const names = ['indiceDaLinha','editarMensagem','ajustarEdicaoMensagem','pertoDoFim','rolarSePerto','acompanharTeclado','parar'];
const code = names.map(name => extractFunction(js, name)).join('\n\n');
const hashes = {js:createHash('sha256').update(js).digest('hex'),css:createHash('sha256').update(css).digest('hex')};
const html = `<!doctype html><html lang="pt-BR" data-theme="light"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; font-src 'none'; base-uri 'none'; form-action 'none'">
<title>IALD — fixture isolada do editor</title><style>${css.replaceAll('</style','<\\/style')}</style>
<style>html,body{height:100%;margin:0;overflow:hidden}body{display:flex;flex-direction:column;background:var(--bg);color:var(--txt)}
.fixture-toolbar{padding:8px;display:flex;flex-wrap:wrap;gap:8px;flex:none;border-bottom:1px solid var(--borda)}
.fixture-toolbar button{padding:6px 10px;border:1px solid var(--borda);border-radius:8px;min-height:40px;background:var(--bg-elevado);color:var(--txt)}
.fixture-frame{display:flex;flex:1;min-height:0;flex-direction:column}.fixture-frame.compact{flex:none;height:330px}
#conversa{min-height:0}#measurements{flex:none;margin:0;padding:8px;max-height:96px;overflow:auto;font:11px monospace;white-space:pre-wrap}
#fixture-label{font-size:12px;padding:3px 8px}#ir-fim{display:none}</style>
<body><div class="fixture-toolbar"><button id="light">Tema claro</button><button id="dark">Tema escuro</button>
<button id="long">Texto longo</button><button id="short">Texto curto</button><button id="compact">Área reduzida</button>
<button id="edit">Editar</button><button id="stop">Parar sintético</button><button id="measure">Medir</button></div>
<div id="fixture-label">Fixture OFFLINE. Somente dados sintéticos; nenhum envio ou login.</div>
<div class="fixture-frame"><div id="conversa" class="conversa"><div id="conversa-interna" class="conversa-interna"></div></div>
<div class="compositor-area"><textarea id="entrada" aria-label="Rascunho do compositor">Rascunho independente</textarea></div></div>
<button id="ir-fim"></button><pre id="measurements" aria-label="Medições"></pre>
<script>
'use strict';
const hashes=${JSON.stringify(hashes)};
const $=selector=>document.querySelector(selector);
const el=(tag,cls,text)=>{const node=document.createElement(tag);if(cls)node.className=cls;if(text!=null)node.textContent=text;return node;};
const S={ativaId:'synthetic',gerando:false,colarNoFim:true,anexos:[]};
const sample='Primeira linha com acentuação e α.\\nSegunda linha: texto editável, 🙂 e <b>marcação literal</b>.';
const c={id:S.ativaId,mensagens:[{role:'user',content:sample},{role:'assistant',content:'Aviso sintético: a resposta foi interrompida a seu pedido.'}]};
const sent=[];const conversaAtiva=()=>c;const respostaPendenteBackground=()=>false;
const salvarConversas=()=>{};
function abrirConversa(){const area=$('#conversa-interna');area.replaceChildren();for(const message of c.mensagens){const row=el('div','msg');row.dataset.papel=message.role==='user'?'user':'ai';row._bruto=message.content;row.append(el('div','msg-corpo',message.content),el('div','msg-acoes'));area.append(row);}requestAnimationFrame(measure);}
function enviarTexto(text,attachments){sent.push({text,attachments});c.mensagens.push({role:'user',content:text});abrirConversa();}
window.fetch=()=>Promise.reject(new Error('NETWORK_DISABLED_FIXTURE'));
${code.replaceAll('</script','<\\/script')}
function measure(){const ta=document.querySelector('.msg-edicao-texto');const style=ta&&getComputedStyle(ta);const area=$('#conversa');
const data={hashes,syntheticOnly:true,sentCount:sent.length,theme:document.documentElement.dataset.theme,conversationHeight:area.clientHeight,conversationScroll:area.scrollTop,
editor:ta?{valueLength:ta.value.length,color:style.color,fill:style.webkitTextFillColor,background:style.backgroundColor,fontSize:style.fontSize,height:ta.clientHeight,scrollHeight:ta.scrollHeight,scrollTop:ta.scrollTop,selection:[ta.selectionStart,ta.selectionEnd],rect:ta.getBoundingClientRect().toJSON()}:null};$('#measurements').textContent=JSON.stringify(data,null,2);}
function open(){editarMensagem($('#conversa-interna .msg'));requestAnimationFrame(measure);}
$('#light').onclick=()=>{document.documentElement.dataset.theme='light';measure();};
$('#dark').onclick=()=>{document.documentElement.dataset.theme='dark';measure();};
$('#long').onclick=()=>{c.mensagens=[{role:'user',content:Array.from({length:28},(_,i)=>(i+1)+'. '+sample).join('\\n')}];abrirConversa();open();};
$('#short').onclick=()=>{c.mensagens=[{role:'user',content:sample}];abrirConversa();open();};
$('#compact').onclick=()=>{document.querySelector('.fixture-frame').classList.toggle('compact');ajustarEdicaoMensagem();measure();};
$('#edit').onclick=open;
$('#stop').onclick=()=>{S.aborto=new AbortController();S.gerando=true;parar();S.gerando=false;document.getElementById('fixture-label').textContent='Parada sintética confirmada: '+S.aborto.signal.reason.type;open();};
$('#measure').onclick=measure;document.addEventListener('input',()=>requestAnimationFrame(measure));
window.addEventListener('resize',()=>{ajustarEdicaoMensagem();measure();});
abrirConversa();acompanharTeclado();
</script></body></html>`;
const output = new URL('./editor_preview.html', import.meta.url);
const temporary = new URL('./editor_preview.html.tmp', import.meta.url);
writeFileSync(temporary, html, 'utf8');
renameSync(temporary, output);
console.log(JSON.stringify({output:output.pathname,hashes,bytes:Buffer.byteLength(html)}));
