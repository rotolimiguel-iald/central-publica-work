import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source = readFileSync(new URL('./stage/app/iald.js',import.meta.url),'utf8');
const start = source.indexOf('async function transmitir(');
const end = source.indexOf('// ═',start);
const labels = source.slice(source.indexOf('function modeloDaResposta('),source.indexOf('function desenharMensagem('));
const conversation = {mensagens:[]};
let model = {motor:'openai',id:'gpt-5.6-luna',rotulo:'ChatGPT 5.6 Luna'};
let header;
let saved;
const noop = ()=>{};
const element = ()=>({textContent:'',hidden:false,appendChild:noop,remove:noop,innerHTML:''});
const context = vm.createContext({S:{gerando:false,motor:{modelo:'not-the-source'},servidor:{}},AbortController,Date,
  desenharMensagem:()=>{header=element();return {querySelector:s=>s==='.msg-modelo'?header:element(),parentElement:{}};},
  el:element,
  atualizarBotaoEnviar:noop,rolarSePerto:noop,atualizarDica:noop,listarConversas:noop,
  congelarTrilha:noop,renderMarkdown:()=>element(),aplicarPtbr:x=>x,
  conversaAtiva:()=>conversation,salvarConversas:()=>{saved=JSON.parse(JSON.stringify(conversation));},
  DEMO:false,fluxoHttp:async function*(){
    if(model) yield 'data: '+JSON.stringify({iald_modelo:model});
    yield 'data: '+JSON.stringify({choices:[{delta:{content:'Answer'}}]});
    yield 'data: [DONE]';
  },document:{querySelector:()=>true},setTimeout:noop,carregarMotor:noop,
  avisar:message=>{throw new Error(message);}});
vm.runInContext(labels+source.slice(start,end),context);
await vm.runInContext('transmitir([])',context);
assert.equal(saved.mensagens[0].modelo.id,'gpt-5.6-luna');
assert.equal(header.textContent,'ChatGPT 5.6 Luna');
model={motor:'nativa',id:'iald_nativa_v2_35b',rotulo:'IALD Nativa · Qwen3.6-35B'};
await vm.runInContext('transmitir([])',context);
assert.equal(saved.mensagens.length,2);
assert.equal(saved.mensagens[0].modelo.id,'gpt-5.6-luna');
assert.equal(saved.mensagens[1].modelo.id,'iald_nativa_v2_35b');
model=null;
await vm.runInContext('transmitir([])',context);
assert.equal(saved.mensagens[2].modelo,undefined);
assert.equal(vm.runInContext("modeloDaResposta({id:'',rotulo:'Luna'})",context),null);
assert.ok(source.includes("m.content, false, m.modelo"));
console.log('Response labels: 8 checks passed; server provenance persisted across model switch and legacy data preserved.');
