from pathlib import Path
import json, hashlib
from task import W, check, pin, save
check('fix')
R=Path(r'C:\IALD\projetos_pyhton\IALD')
(W/'baseline').mkdir(exist_ok=True);(W/'stage').mkdir(exist_ok=True)
for name in ('iald.js','owner_office.js'):
 p=R/'app'/name
 if not (W/'baseline'/name).exists(): (W/'baseline'/name).write_bytes(p.read_bytes())
def change(s,a,b):
 assert s.count(a)==1,(a[:80],s.count(a))
 return s.replace(a,b,1)
s=(W/'baseline/iald.js').read_bytes().decode()
nl='\r\n' if '\r\n' in s else '\n';s=s.replace('\r\n','\n')
s=change(s,"  else { listarConversas(); abrirConversa(); }\n  refreshNativeNotificationsUI();", "  // An identity check is not navigation. Rebuilding here detached streaming\n  // nodes and forced the reader to the bottom on every recovery/status check.\n  refreshNativeNotificationsUI();")
s=change(s,"function abrirConversa() {\n", "let renderedPublicView = null, publicRenderRevision = 0, renderingConversation = false;\nlet conversationScroll = null;\nfunction abrirConversa() {\n  const scroll = $('#conversa');\n  const view = backgroundOwner + ':' + S.ativaId;\n  const newView = view !== renderedPublicView;\n  const oldTop = scroll.scrollTop;\n  const renderRevision = ++publicRenderRevision;\n  renderedPublicView = view;\n  if (newView) conversationScroll?.reset();\n  const gestureRevision = conversationScroll?.revision();\n")
s=change(s,"  for (const m of c.mensagens) desenharMensagem", "  renderingConversation = true;\n  try {\n  for (const m of c.mensagens) desenharMensagem")
s=change(s,"  atualizarDica();\n  requestAnimationFrame(() => {\n    if (!document.querySelector('.msg-edicao-texto')) $('#conversa').scrollTop = $('#conversa').scrollHeight;\n  });", "  } finally { renderingConversation = false; }\n  if (!newView) conversationScroll?.restore(oldTop);\n  atualizarDica();\n  requestAnimationFrame(() => {\n    if (renderRevision !== publicRenderRevision || view !== backgroundOwner + ':' + S.ativaId ||\n        gestureRevision !== conversationScroll?.revision()) return;\n    rolarSePerto();\n  });")
start=s.index('function rolarSePerto() {');end=s.index('\n}',start)+2
s=s[:start]+'''function rolarSePerto() {
  if (!renderingConversation) conversationScroll?.follow();
}

// Follow new text only while the reader has not taken control. Geometry alone
// cannot express intent: even a small upward gesture must stop auto-following.
function createConversationScroll({ container, button, getFollowing, setFollowing, isEditing,
  getSelection = () => window.getSelection(), root = document }) {
  let lastTop = container.scrollTop, revision = 0, touch = null;
  const atBottom = () => container.scrollHeight - container.clientHeight - container.scrollTop <= 2;
  const selected = () => { const s = getSelection(); return s && !s.isCollapsed; };
  const updateButton = () => { button.dataset.visivel = atBottom() ? '' : '1'; };
  const pause = () => { setFollowing(false); revision++; };
  const restore = top => { container.scrollTop = top; lastTop = container.scrollTop; updateButton(); };
  const follow = () => {
    if (!getFollowing() || touch || isEditing() || selected()) { updateButton(); return; }
    restore(container.scrollHeight);
  };
  container.addEventListener('scroll', () => {
    const top = container.scrollTop, delta = top - lastTop;
    if (isEditing() || delta < -1) pause();
    // Only an actual downward scroll reaching the end resumes following.
    // Content growth, layout changes and a passive status refresh cannot do it.
    else if (!touch && delta > 1 && atBottom()) setFollowing(true);
    lastTop = top; updateButton();
  }, { passive: true });
  container.addEventListener('wheel', event => { if (event.deltaY < 0) pause(); }, { passive: true });
  container.addEventListener('touchstart', event => {
    const point = event.touches[0];
    if (!point) return;
    touch = { y: point.clientY, moved: false, following: getFollowing() };
    pause();
  }, { passive: true });
  container.addEventListener('touchmove', event => {
    if (touch && event.touches[0] && Math.abs(event.touches[0].clientY - touch.y) > 2) touch.moved = true;
  }, { passive: true });
  const endTouch = event => {
    const previous = touch; touch = null;
    if (event.type !== 'touchcancel' && previous && !previous.moved && previous.following && !selected()) {
      setFollowing(true); follow();
    }
    updateButton();
  };
  container.addEventListener('touchend', endTouch, { passive: true });
  container.addEventListener('touchcancel', endTouch, { passive: true });
  root.addEventListener('keydown', event => {
    if (event.target?.closest?.('input,textarea,select,[contenteditable="true"]')) return;
    if (['ArrowUp','PageUp','Home'].includes(event.key) || (event.key === ' ' && event.shiftKey)) pause();
  });
  button.addEventListener('click', () => {
    touch = null; revision++; setFollowing(true); follow();
  });
  updateButton();
  return { follow, restore, revision: () => revision,
    reset() { touch = null; revision++; lastTop = container.scrollTop; setFollowing(true); } };
}''' + s[end:]
a=s.index('  // rolagem\n  const conversa');b=s.index('\n  // exportacao',a)
s=s[:a]+'''  // One scroll policy for public and private conversation rendering.
  conversationScroll = createConversationScroll({
    container: $('#conversa'), button: $('#ir-fim'),
    getFollowing: () => S.colarNoFim, setFollowing: value => { S.colarNoFim = value; },
    isEditing: () => !!document.querySelector('.msg-edicao-texto'),
  });
''' +s[b:]
s=change(s,"  ownerOfficeUI = mountOwnerOffice({ request: fetchIALD,", "  ownerOfficeUI = mountOwnerOffice({ request: fetchIALD,\n    onContentChanged: () => rolarSePerto(),")
(W/'stage/iald.js').write_bytes(s.replace('\n',nl).encode())
s=(W/'baseline/owner_office.js').read_bytes().decode();nl='\r\n' if '\r\n' in s else '\n';s=s.replace('\r\n','\n')
s=change(s,'  renderPrivateMarkdown, createPrivateWait, onExport }) {','  renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged }) {')
s=change(s,'    if (changed && followBottom && !preserveSelection) scroll.scrollTop = scroll.scrollHeight;', '''    if (changed && !preserveSelection) {
      if (onContentChanged) onContentChanged();
      else if (followBottom) scroll.scrollTop = scroll.scrollHeight;
    }''')
s=change(s,'preflightTransport = null, renderPrivateMarkdown, createPrivateWait, onExport }) {','preflightTransport = null, renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged }) {')
s=change(s,'    renderPrivateMarkdown, createPrivateWait, onExport });','    renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged });')
(W/'stage/owner_office.js').write_bytes(s.replace('\n',nl).encode())
print(json.dumps({'stage':[pin(W/'stage'/n) for n in ('iald.js','owner_office.js')]}))
