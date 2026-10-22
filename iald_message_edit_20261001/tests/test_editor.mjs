// Independent offline regressions. Never bootstraps the full app or sends requests.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { fixture, extractFunction } from './editor_fixture.mjs';

const jsPath = new URL('../stage/iald.js', import.meta.url);
const cssPath = new URL('../stage/iald.css', import.meta.url);
const source = readFileSync(jsPath, 'utf8');
const css = readFileSync(cssPath, 'utf8');
const setup = () => fixture(source);
const clickSend = h => h.buttons().find(button => button.textContent === 'Enviar editada').click();
const history = h => JSON.stringify(h.c.mensagens);

test('source functions parse independently without executing app imports or bootstrap', () => {
  for (const name of ['editarMensagem', 'ajustarEdicaoMensagem', 'acompanharTeclado', 'transmitir']) {
    assert.ok(extractFunction(source, name).includes(name));
  }
});

test('opens exact multiline Unicode text as value, focuses without scrolling and keeps composer draft', () => {
  const h = setup(), before = history(h), attachments = JSON.stringify(h.S.anexos);
  const ta = h.open();
  assert.equal(ta.value, h.c.mensagens[2].content);
  assert.equal(ta.children.length, 0); assert.equal(ta.className, 'msg-edicao-texto');
  assert.equal(ta.getAttribute('aria-label'), 'Editar mensagem');
  assert.equal(ta.getAttribute('enterkeyhint'), 'enter');
  assert.equal(ta.focusOptions.preventScroll, true);
  assert.equal(ta.selectionStart, ta.value.length); assert.equal(ta.selectionEnd, ta.value.length);
  assert.equal(h.line.dataset.editando, '1'); assert.equal(h.S.colarNoFim, false);
  assert.equal(h.followEnd.dataset.visivel, '');
  assert.equal(h.composer.value, 'COMPOSER_DRAFT'); assert.equal(JSON.stringify(h.S.anexos), attachments);
  assert.equal(history(h), before); assert.equal(h.sent.length, 0); assert.equal(h.saved.length, 0);
});

test('warning and background pending rows do not change the edited history index', () => {
  const h = setup();
  for (const key of ['aviso', 'backgroundPending']) {
    const row = h.make('div', 'msg'); row.dataset[key] = '1';
    h.list.children.unshift(row); row.parentNode = h.list;
  }
  assert.equal(h.run('indiceDaLinha', h.line), 2);
  assert.equal(h.open().value, h.c.mensagens[2].content);
});

test('pending job or active generation prevents opening editor and touching history', () => {
  for (const blocked of ['pending', 'generating']) {
    const h = setup(), before = history(h);
    if (blocked === 'pending') h.setPending(true); else h.S.gerando = true;
    assert.equal(h.open(), null); assert.equal(history(h), before); assert.equal(h.saved.length, 0);
  }
});

test('Stop sends explicit cancellation and editing waits until terminal state', () => {
  const h = setup(); h.S.aborto = new AbortController(); h.S.gerando = true; h.setPending(true);
  h.run('parar');
  assert.equal(h.S.aborto.signal.aborted, true); assert.equal(h.S.aborto.signal.reason.type, 'user_cancel');
  assert.equal(h.open(), null);
  h.S.gerando = false; assert.equal(h.open(), null);
  h.setPending(false); assert.equal(h.open().value, h.c.mensagens[2].content);
  assert.equal(h.sent.length, 0);
});

test('opening another edit preserves the existing unsent editor', () => {
  const h = setup(), ta = h.open(); ta.value = 'UNSAVED EDIT';
  h.run('editarMensagem', h.lines[0]); h.flush();
  assert.equal(h.list.querySelectorAll('textarea').length, 1);
  assert.equal(h.editor(), ta); assert.equal(ta.value, 'UNSAVED EDIT'); assert.equal(h.saved.length, 0);
});

test('Cancel and Escape leave conversation, composer draft and attachments unchanged', () => {
  for (const kind of ['button', 'escape']) {
    const h = setup(), before = history(h), attachments = JSON.stringify(h.S.anexos);
    const ta = h.open(); ta.value = 'SHOULD NOT BE SENT';
    if (kind === 'button') h.buttons().find(button => button.textContent === 'Cancelar').click();
    else ta.dispatch('keydown', { key: 'Escape' });
    assert.equal(history(h), before); assert.equal(h.opens.length, 1);
    assert.equal(h.saved.length, 0); assert.equal(h.sent.length, 0);
    assert.equal(h.composer.value, 'COMPOSER_DRAFT'); assert.equal(JSON.stringify(h.S.anexos), attachments);
  }
});

test('Enter and Shift+Enter preserve browser default newline and do not submit', () => {
  for (const shiftKey of [false, true]) {
    const h = setup(), ta = h.open(), before = history(h);
    const event = ta.dispatch('keydown', { key: 'Enter', shiftKey });
    assert.equal(event.defaultPrevented, false);
    assert.equal(h.sent.length, 0); assert.equal(h.saved.length, 0); assert.equal(history(h), before);
  }
});

test('Ctrl+Enter and Cmd+Enter submit one edited text and preserve the preceding history', () => {
  for (const modifier of ['ctrlKey', 'metaKey']) {
    const h = setup(), prefix = history(h).slice(); const original = h.c.mensagens.slice(0, 2);
    const ta = h.open(); ta.value = '  NOVA\nmensagem α 🙂  ';
    const event = ta.dispatch('keydown', { key: 'Enter', [modifier]: true });
    assert.equal(event.defaultPrevented, true);
    assert.deepEqual(h.sent, [{ text: 'NOVA\nmensagem α 🙂', attachments: [] }]);
    assert.equal(JSON.stringify(h.c.mensagens), JSON.stringify(original));
    assert.equal(h.saved.length, 1); assert.equal(h.opens.length, 1);
    assert.equal(h.composer.value, 'COMPOSER_DRAFT'); assert.notEqual(history(h), prefix);
  }
});

test('IME composition never submits on modified Enter or cancels on Escape', () => {
  for (const key of ['Enter', 'Escape']) {
    const h = setup(), ta = h.open(), before = history(h);
    const event = ta.dispatch('keydown', { key, ctrlKey: true, metaKey: true, isComposing: true });
    assert.equal(event.defaultPrevented, false);
    assert.equal(h.sent.length, 0); assert.equal(h.opens.length, 0); assert.equal(history(h), before);
  }
});

test('IME legacy keyCode 229 never submits an unfinished composition', () => {
  const h = setup(), ta = h.open();
  ta.dispatch('keydown', { key: 'Enter', keyCode: 229, ctrlKey: true, isComposing: false });
  assert.equal(h.sent.length, 0); assert.equal(h.saved.length, 0);
});

test('blank edited text is rejected before truncating history', () => {
  const h = setup(), before = history(h), ta = h.open(); ta.value = ' \n\t ';
  clickSend(h); assert.equal(history(h), before); assert.equal(h.sent.length, 0); assert.equal(h.saved.length, 0);
});

test('send rechecks generation, pending job and current conversation', () => {
  for (const changed of ['generating', 'pending', 'conversation']) {
    const h = setup(), before = history(h), ta = h.open(); ta.value = 'EDIT';
    if (changed === 'generating') h.S.gerando = true;
    if (changed === 'pending') h.setPending(true);
    if (changed === 'conversation') h.S.ativaId = 'synthetic-b';
    clickSend(h);
    assert.equal(history(h), before); assert.equal(h.sent.length, 0); assert.equal(h.saved.length, 0);
  }
});

test('autosize grows, shrinks and caps height without changing text, selection or internal scroll', () => {
  const h = setup(), ta = h.open();
  for (const [area, contentHeight, expected] of [[700, 1000, 320], [360, 1000, 220], [200, 1000, 72], [500, 120, 122]]) {
    h.conversation.clientHeight = area; ta.scrollHeight = contentHeight; ta.style.height = '82px'; ta.scrollTop = 31;
    ta.setSelectionRange(3, 8); const value = ta.value;
    assert.equal(h.run('ajustarEdicaoMensagem'), true);
    assert.equal(ta.style.height, expected + 'px'); assert.equal(ta.scrollTop, Math.min(31, Math.max(0, contentHeight - (expected - 2))));
    assert.equal(ta.value, value); assert.equal(ta.selectionStart, 3); assert.equal(ta.selectionEnd, 8);
  }
});

test('input event recalculates editor height', () => {
  const h = setup(), ta = h.open(); ta.scrollHeight = 250; ta.dispatch('input');
  assert.equal(ta.style.height, '252px');
});

test('adjuster leaves visible line still and only shifts conversation for viewport margins', () => {
  const h = setup(); h.open();
  for (const [top, bottom, expected] of [[100, 260, 200], [40, 220, 174], [410, 560, 234], [90, 650, 224]]) {
    h.conversation.scrollTop = 200;
    h.line.rect = { top, bottom, height: bottom - top, left: 0, right: 390, width: 390 };
    h.run('ajustarEdicaoMensagem'); assert.equal(h.conversation.scrollTop, expected);
  }
});

test('missing or detached editor makes adjuster a safe no-op', () => {
  const h = setup(), before = h.conversation.scrollTop;
  assert.equal(h.run('ajustarEdicaoMensagem'), false);
  const ta = h.open(); ta.remove();
  assert.equal(h.run('ajustarEdicaoMensagem'), false); assert.equal(h.conversation.scrollTop, before);
});

test('follow-end scrolling cannot override a live edit', () => {
  const h = setup(); h.open(); h.S.colarNoFim = true;
  const before = h.conversation.scrollTop; h.run('rolarSePerto');
  assert.equal(h.conversation.scrollTop, before);
  h.editor().remove(); h.run('rolarSePerto');
  assert.equal(h.conversation.scrollTop, h.conversation.scrollHeight);
});

test('visualViewport resize and scroll keep editor visible and preserve its internal state', () => {
  const h = setup(), ta = h.open(); h.run('acompanharTeclado');
  h.S.colarNoFim = true; ta.scrollHeight = 900; ta.scrollTop = 25; const before = h.conversation.scrollTop;
  h.vv.height = 440; h.vv.offsetTop = 18; h.conversation.clientHeight = 280; ta.scrollHeight = 900;
  h.vv.dispatch('resize'); h.vv.dispatch('scroll');
  assert.equal(ta.style.height, '140px'); assert.equal(ta.scrollTop, 25);
  assert.equal(h.conversation.scrollTop, before);
  assert.equal(h.document.documentElement.style.getPropertyValue('--altura-util'), '440px');
  assert.equal(h.document.documentElement.style.getPropertyValue('--topo-util'), '18px');
  assert.equal(h.document.documentElement.dataset.teclado, '1');
});

test('normal composer viewport flow still follows end only on shrink when opted in', () => {
  const h = setup(), before = h.conversation.scrollTop;
  h.run('acompanharTeclado'); assert.equal(h.conversation.scrollTop, before);
  h.vv.height = 450; h.vv.dispatch('resize'); assert.equal(h.conversation.scrollTop, h.conversation.scrollHeight);
  h.conversation.scrollTop = 20; h.vv.height = 800; h.vv.dispatch('resize');
  assert.equal(h.conversation.scrollTop, 20); assert.equal(h.document.documentElement.dataset.teclado, '');
  h.S.colarNoFim = false; h.vv.height = 450; h.vv.dispatch('resize'); assert.equal(h.conversation.scrollTop, 20);
});

test('no visualViewport does not break startup and window resize still adjusts editor', () => {
  const h = setup(); h.window.visualViewport = undefined;
  assert.doesNotThrow(() => h.run('acompanharTeclado'));
  // Execute the actual registered listener, excluding unrelated app listeners.
  const listener = source.split(/\r?\n/).find(line => line.includes("window.addEventListener('resize'"));
  assert.ok(listener); vm.runInContext(listener, h.context);
  const ta = h.open(); ta.scrollHeight = 800; h.conversation.clientHeight = 300;
  h.window.dispatch('resize'); assert.equal(ta.style.height, '160px');
});

test('normal composer autosize still clears empty height and caps long text', () => {
  const h = setup(); h.composer.scrollHeight = 900; h.run('redimensionarEntrada');
  assert.equal(h.composer.style.height, '176px'); assert.equal(h.composer.value, 'COMPOSER_DRAFT');
  h.composer.value = ''; h.run('redimensionarEntrada'); assert.equal(h.composer.style.height, '');
});

const cleanCss = css.replace(/\/\*[\s\S]*?\*\//g, '');
const rules = [...cleanCss.matchAll(/([^{}]+)\{([^{}]*)\}/g)].map(match => ({ selector: match[1].trim(), body: match[2] }));
function declarations(selector) {
  const rule = rules.find(rule => rule.selector === selector); assert.ok(rule, 'CSS rule missing: ' + selector);
  return Object.fromEntries(rule.body.split(';').map(item => {
    const pos = item.indexOf(':'); return pos < 0 ? [] : [item.slice(0, pos).trim(), item.slice(pos + 1).trim()];
  }).filter(pair => pair.length));
}
function luminance(hex) {
  assert.match(hex, /^#[0-9a-f]{6}$/i);
  const rgb = hex.slice(1).match(/../g).map(value => parseInt(value, 16) / 255)
    .map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4);
  return rgb[0] * .2126 + rgb[1] * .7152 + rgb[2] * .0722;
}
function contrast(a, b) { const x = luminance(a), y = luminance(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); }

test('dedicated editor color and WebKit fill prevent white-on-white in light and dark token sets', () => {
  const editor = declarations('.msg-edicao-texto');
  assert.equal(editor.color, 'var(--txt)'); assert.equal(editor['-webkit-text-fill-color'], 'currentColor');
  assert.equal(editor['caret-color'], 'var(--txt)'); assert.equal(editor.background, 'var(--bg-elevado)');
  assert.ok(parseFloat(editor['font-size']) >= 16); assert.equal(editor['font-size'].endsWith('px'), true);
  for (const selector of [':root', ':root[data-theme="dark"]', ':root:not([data-theme="light"])']) {
    const tokens = { ...declarations(':root'), ...declarations(selector) };
    const ratio = contrast(tokens['--txt'], tokens['--bg-elevado']);
    assert.ok(ratio >= 4.5, selector + ': contrast ' + ratio);
  }
});

test('editor actions remain touchable and keyboard margin is present', () => {
  assert.ok(parseFloat(declarations('.msg-edicao-acoes button')['min-height']) >= 44);
  assert.equal(declarations('.msg-edicao-acoes')['flex-wrap'], 'wrap');
  assert.equal(declarations(':root[data-teclado="1"] .compositor-area')['padding-bottom'], '16px');
  const body = declarations('.msg[data-editando="1"] .msg-corpo');
  assert.equal(body.color, 'var(--txt)'); assert.equal(body['max-width'], '100%');
});


test('shrinking viewport keeps end-of-text visible while preserving a deliberate middle scroll', () => {
  for (const atEnd of [true, false]) {
    const h = setup(), ta = h.open(); ta.value = 'LONG SYNTHETIC TEXT '.repeat(100);
    ta.scrollHeight = 900; ta.style.height = '322px';
    ta.scrollTop = atEnd ? ta.scrollHeight - ta.clientHeight : 100;
    ta.setSelectionRange(ta.value.length, ta.value.length);
    const value = ta.value, selection = ta.selectionStart;
    h.conversation.clientHeight = 340;
    h.run('ajustarEdicaoMensagem');
    assert.equal(ta.style.height, '200px');
    assert.equal(ta.scrollTop, atEnd ? 702 : 100);
    assert.equal(ta.value, value); assert.equal(ta.selectionStart, selection); assert.equal(ta.selectionEnd, selection);
    if (atEnd) assert.equal(ta.scrollHeight - ta.clientHeight - ta.scrollTop, 0);
  }
});
