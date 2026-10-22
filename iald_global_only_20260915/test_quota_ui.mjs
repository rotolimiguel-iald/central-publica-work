import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source = readFileSync(new URL('./stage/app/iald.js', import.meta.url), 'utf8');
function take(name) {
  const start = source.indexOf(`function ${name}(`);
  assert.ok(start >= 0);
  const end = source.indexOf('\nfunction ', start + 1);
  return source.slice(start, end);
}
function element(tag, cls, text = '') {
  return {tag, cls, text, children: [], dataset: {}, style: {}, attrs: {},
    appendChild(child) { this.children.push(child); },
    setAttribute(key, val) {this.attrs[key] = val;},
    set innerHTML(value) {assert.equal(value, ''); this.children = [];}};
}
const section = element('section');
const state = {plano:'operador', somente_limite_global: true,
  tokens_dia:{usado:3000000, limite:null}, tokens_mes:{usado:40000000, limite:null},
  global_usd_dia:{usado:.85, limite:1}};
const context = vm.createContext({el:element, num:n=>String(n), S:{},
  document:{getElementById:()=>section}, cotaAtual:()=>state,
  quandoRenova:()=>'', DEFINICAO_TOKEN_PADRAO:'Tokens', Intl});
vm.runInContext(take('periodoDeUso') + take('pintarUsoPlano'), context);
const unlimited = vm.runInContext("periodoDeUso('Hoje', {usado:3000000,limite:null}, '')", context);
assert.match(JSON.stringify(unlimited), /Sem limite individual/);
assert.doesNotMatch(JSON.stringify(unlimited), /progressbar|limite atingido/);
const zero = vm.runInContext("periodoDeUso('Hoje', {usado:0,limite:0}, '')", context);
assert.match(JSON.stringify(zero), /limite atingido/);
vm.runInContext('pintarUsoPlano()', context);
assert.match(JSON.stringify(section), /Sua conta usa somente o limite global da IALD/);
assert.match(JSON.stringify(section), /Uso global hoje/);
assert.match(JSON.stringify(section), /1,00/);
state.somente_limite_global = false;
state.tokens_dia.limite = 5000000;
state.tokens_mes.limite = 50000000;
vm.runInContext('pintarUsoPlano()', context);
assert.doesNotMatch(JSON.stringify(section), /Uso global hoje|Sem limite individual/);
console.log('UI: 7 checks passed (unlimited, zero, global visibility, other accounts).');
