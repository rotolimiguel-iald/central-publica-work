// Minimal deterministic DOM for the selected real editor/viewport functions.
// It models events and geometry, not browser painting or a complete CSS cascade.
import assert from 'node:assert/strict';
import vm from 'node:vm';

export function extractFunction(source, name) {
  const start = new RegExp('^(?:async )?function ' + name + '\\s*\\(', 'm').exec(source);
  assert.ok(start, 'Required function missing: ' + name);
  const endings = /^\}/gm;
  endings.lastIndex = start.index + start[0].length;
  for (let end; (end = endings.exec(source));) {
    const candidate = source.slice(start.index, end.index + 1);
    try { new vm.Script('(' + candidate + ')'); return candidate; } catch { /* try complete closing brace */ }
  }
  throw new Error('No complete function: ' + name);
}

export class Events {
  listeners = new Map();
  addEventListener(type, handler, options) {
    const list = this.listeners.get(type) || [];
    list.push({ handler, once: !!options?.once }); this.listeners.set(type, list);
  }
  removeEventListener(type, handler) {
    this.listeners.set(type, (this.listeners.get(type) || []).filter(item => item.handler !== handler));
  }
  dispatch(type, fields = {}) {
    const event = { type, target: this, currentTarget: this, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }, stopPropagation() {}, ...fields };
    for (const item of [...(this.listeners.get(type) || [])]) {
      item.handler(event); if (item.once) this.removeEventListener(type, item.handler);
    }
    return event;
  }
}

class Style {
  set cssText(value) {
    for (const [name, raw] of String(value).split(';').map(pair => pair.split(':'))) {
      if (name?.trim() && raw != null) this.setProperty(name.trim(), raw.trim());
    }
  }
  get cssText() { return Object.entries(this).map(([key, value]) => key + ':' + value).join(';'); }
  setProperty(name, value) { this[name] = String(value); this[name.replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = String(value); }
  getPropertyValue(name) { return this[name] || ''; }
  removeProperty(name) { delete this[name]; }
}

function simpleMatch(node, selector) {
  const denied = [...selector.matchAll(/:not\(([^)]+)\)/g)].map(match => match[1]);
  selector = selector.replace(/:not\([^)]+\)/g, '');
  if (denied.some(value => simpleMatch(node, value))) return false;
  const tag = selector.match(/^[a-z][\w-]*/i)?.[0];
  if (tag && node.tagName !== tag.toUpperCase()) return false;
  for (const match of selector.matchAll(/#([\w-]+)/g)) if (node.id !== match[1]) return false;
  for (const match of selector.matchAll(/\.([\w-]+)/g)) if (!node.classList.contains(match[1])) return false;
  for (const match of selector.matchAll(/\[([\w-]+)(?:=["']?([^\]"']+)["']?)?\]/g)) {
    const value = node.getAttribute(match[1]);
    if (value == null || (match[2] != null && value !== match[2])) return false;
  }
  return !!selector.trim();
}

export class Element extends Events {
  constructor(tag, doc) {
    super(); this.tagName = tag.toUpperCase(); this.ownerDocument = doc;
    this.style = new Style(); this.dataset = {}; this.attributes = new Map();
    this.children = []; this.className = ''; this.id = ''; this.value = ''; this._text = '';
    this.scrollTop = 0; this.scrollLeft = 0; this.scrollHeight = 120; this.clientHeight = 120;
    this.selectionStart = 0; this.selectionEnd = 0; this.disabled = false; this.hidden = false;
    this.rect = { top: 100, bottom: 260, left: 0, right: 390, width: 390, height: 160 };
    this.classList = {
      contains: name => this.className.split(/\s+/).includes(name),
      add: (...names) => { this.className = [...new Set([...this.className.split(/\s+/).filter(Boolean), ...names])].join(' '); },
      remove: (...names) => { this.className = this.className.split(/\s+/).filter(name => !names.includes(name)).join(' '); },
      toggle: (name, force) => { const next = force ?? !this.classList.contains(name); this.classList[next ? 'add' : 'remove'](name); return next; },
    };
  }
  get scrollTop() {
    return this.tagName === 'TEXTAREA' ? Math.max(0, Math.min(this._scrollTop || 0, this.scrollHeight - this.clientHeight)) : this._scrollTop || 0;
  }
  set scrollTop(value) { this._scrollTop = this.tagName === 'TEXTAREA' ? Math.max(0, Math.min(value, this.scrollHeight - this.clientHeight)) : value; }
  get clientHeight() {
    const height = parseFloat(this.style?.height);
    return this.tagName === 'TEXTAREA' && Number.isFinite(height) ? Math.max(0, height - 2) : this._clientHeight || 0;
  }
  set clientHeight(value) { this._clientHeight = value; }
  get parentElement() { return this.parentNode; }
  get isConnected() { return this === this.ownerDocument?.documentElement || !!this.parentNode?.isConnected; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  set textContent(value) { this._text = String(value); this.replaceChildren(); }
  get innerHTML() { return this._text; }
  set innerHTML(value) { this._text = String(value); this.replaceChildren(); }
  appendChild(child) { if (child.parentNode) child.remove(); child.parentNode = this; this.children.push(child); return child; }
  append(...children) { for (const child of children) this.appendChild(child); }
  replaceChildren(...children) { for (const child of this.children) child.parentNode = null; this.children = []; this.append(...children); }
  remove() { if (this.parentNode) this.parentNode.children = this.parentNode.children.filter(node => node !== this); this.parentNode = null; }
  contains(other) { return this === other || this.children.some(child => child.contains(other)); }
  matches(selector) { return selector.split(',').some(option => simpleMatch(this, option.trim())); }
  closest(selector) { return this.matches(selector) ? this : this.parentNode?.closest(selector) || null; }
  querySelectorAll(selector) {
    const result = [];
    const visit = node => { for (const child of node.children) { if (child.matches(selector)) result.push(child); visit(child); } };
    visit(this); return result;
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  setAttribute(name, value) {
    if (name === 'class') this.className = String(value);
    else if (name === 'id') this.id = String(value);
    else if (name.startsWith('data-')) this.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = String(value);
    else this.attributes.set(name, String(value));
  }
  getAttribute(name) {
    if (name === 'class') return this.className;
    if (name === 'id') return this.id;
    if (name.startsWith('data-')) return this.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] ?? null;
    return this.attributes.get(name) ?? null;
  }
  removeAttribute(name) {
    if (name.startsWith('data-')) delete this.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())];
    else this.attributes.delete(name);
  }
  focus(options) { this.ownerDocument.activeElement = this; this.focusOptions = options; this.dispatch('focus'); }
  blur() { if (this.ownerDocument.activeElement === this) this.ownerDocument.activeElement = null; }
  setSelectionRange(start, end) { this.selectionStart = start; this.selectionEnd = end; }
  click() { if (!this.disabled) return this.dispatch('click'); }
  getBoundingClientRect() { return { ...this.rect }; }
  scrollIntoView(options) { this.lastScrollIntoView = options; }
  scrollTo(arg, y) { this.scrollTop = typeof arg === 'object' ? arg.top : y; }
  scrollBy(arg, y) { this.scrollTop += typeof arg === 'object' ? arg.top || 0 : y || 0; }
}

export function fixture(source) {
  const document = new Events(); document.documentElement = new Element('html', document);
  document.body = document.documentElement.appendChild(new Element('body', document));
  document.createElement = tag => new Element(tag, document);
  document.querySelector = selector => document.documentElement.querySelector(selector);
  document.querySelectorAll = selector => document.documentElement.querySelectorAll(selector);
  document.getElementById = id => document.querySelector('#' + id);
  const make = (tag, cls, text) => {
    const node = document.createElement(tag); if (cls) node.className = cls; if (text != null) node.textContent = text; return node;
  };
  const conversation = document.body.appendChild(make('div', 'conversa')); conversation.id = 'conversa';
  conversation.clientHeight = 500; conversation.scrollHeight = 2500; conversation.scrollTop = 200;
  conversation.rect = { top: 50, bottom: 550, height: 500, left: 0, right: 390, width: 390 };
  const list = conversation.appendChild(make('div', 'conversa-interna')); list.id = 'conversa-interna';
  const composer = document.body.appendChild(make('textarea')); composer.id = 'entrada'; composer.value = 'COMPOSER_DRAFT';
  const followEnd = document.body.appendChild(make('button')); followEnd.id = 'ir-fim'; followEnd.dataset.visivel = '1';
  const S = { gerando: false, ativaId: 'synthetic-a', colarNoFim: true, anexos: [{ name: 'synthetic.txt' }] };
  const c = { id: S.ativaId, mensagens: [
    { role: 'user', content: 'FIRST' }, { role: 'assistant', content: 'BEFORE' },
    { role: 'user', content: 'Linha 1\nAcentuação, α, 🙂 e <b>texto</b>' }, { role: 'assistant', content: 'AFTER' },
  ] };
  const lines = [];
  for (const message of c.mensagens) {
    const line = list.appendChild(make('div', 'msg')); line.dataset.papel = message.role === 'user' ? 'user' : 'ai';
    line._bruto = message.content; line.appendChild(make('div', 'msg-corpo', message.content)); line.appendChild(make('div', 'msg-acoes'));
    lines.push(line);
  }
  const vv = new Events(); vv.height = 800; vv.offsetTop = 0; vv.scale = 1;
  const window = new Events(); window.innerHeight = 800; window.innerWidth = 390; window.visualViewport = vv;
  const frames = [], sent = [], saved = [], opens = [];
  let pending = false;
  const context = vm.createContext({ document, window, S, AbortController, console,
    $: selector => document.querySelector(selector), el: make,
    conversaAtiva: () => S.ativaId === c.id ? c : { id: S.ativaId, mensagens: [] },
    respostaPendenteBackground: () => pending,
    salvarConversas: () => saved.push(JSON.parse(JSON.stringify(c))),
    abrirConversa: () => { opens.push(true); for (const line of lines) { delete line.dataset.editando; } list.querySelectorAll('textarea').forEach(node => node.remove()); },
    enviarTexto: (text, attachments) => sent.push({ text, attachments: Array.from(attachments) }),
    requestAnimationFrame: callback => { frames.push(callback); return frames.length; },
    cancelAnimationFrame: () => {},
    setTimeout: callback => { frames.push(callback); return frames.length; }, clearTimeout: () => {},
    getComputedStyle: node => ({ ...node.style, lineHeight: '24px', fontSize: '16px' }),
    fetch: () => { throw new Error('Network forbidden'); },
  });
  const names = ['indiceDaLinha', 'editarMensagem', 'ajustarEdicaoMensagem', 'pertoDoFim',
    'rolarSePerto', 'acompanharTeclado', 'parar', 'redimensionarEntrada'];
  for (const name of names) vm.runInContext(extractFunction(source, name), context, { filename: name + ':real-source' });
  const flush = () => { for (let i = 0; frames.length && i < 30; i++) frames.shift()(); assert.equal(frames.length, 0, 'Unbounded animation/timer loop'); };
  const editor = () => list.querySelector('textarea');
  const buttons = () => list.querySelectorAll('button');
  return { context, document, window, vv, c, S, list, lines, line: lines[2], conversation, composer,
    sent, saved, opens, frames, flush, editor, buttons, make, followEnd,
    setPending: value => { pending = value; },
    open: () => { context.editarMensagem(lines[2]); flush(); return editor(); },
    run: (name, ...args) => context[name](...args),
  };
}
