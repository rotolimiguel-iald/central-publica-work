// Registration names are self-declared. They never grant access or change login IDs.
export function createRegistrationIdentity({ request, doc = document }) {
  let revision = 0, scope = '', overlay = null, fetching = false;
  const deferred = new Set();
  let closeDialog = () => {};
  let waiting = null;
  const anotherSheet = () => !!doc.querySelector('[data-folha][data-aberta="1"]');
  doc.addEventListener('iald:sheets-closed', () => {
    if (!waiting || anotherSheet()) return;
    const retry = waiting;
    waiting = null;
    check(retry);
  });

  function reset() {
    revision += 1;
    scope = '';
    fetching = false;
    waiting = null;
    closeDialog();
    deferred.clear();
  }

  async function check({ pedido = '', account = '', isCurrent = () => true } = {}) {
    const nextScope = pedido ? 'pending:' + pedido : 'account:' + account;
    if (scope !== nextScope) {
      revision += 1;
      closeDialog();
      fetching = false;
      scope = nextScope;
    }
    if (fetching || overlay || deferred.has(scope)) return;
    if (anotherSheet()) { waiting = { pedido, account, isCurrent }; return; }
    fetching = true;
    const turn = ++revision;
    const current = () => turn === revision && isCurrent();
    const url = pedido ? '/api/entrar/identificacao' : '/api/conta/identificacao';
    const options = (nome) => ({
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...(pedido ? { pedido } : {}), ...(nome === undefined ? {} : { nome }) }),
      signal: AbortSignal.timeout(10000),
    });
    try {
      const response = await request(url, pedido ? options() : { signal: AbortSignal.timeout(10000) });
      if (!response.ok) return;
      const data = await response.json();
      if (!current() || data.nome_necessario !== true) return;
      if (anotherSheet()) { waiting = { pedido, account, isCurrent }; return; }
      const previousFocus = doc.activeElement;
      const make = (tag, text, className) => {
        const element = doc.createElement(tag);
        if (text !== undefined) element.textContent = text;
        if (className) element.className = className;
        return element;
      };
      overlay = make('div', undefined, 'registration-overlay');
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');
      overlay.setAttribute('aria-labelledby', 'registration-name-title');
      const panel = make('form', undefined, 'registration-panel');
      const title = make('h2', 'Como podemos identificar você?');
      title.id = 'registration-name-title';
      const description = make('p', 'Informe seu nome para que o responsável pela IALD possa reconhecer seu cadastro e seu pedido de acesso.');
      const provider = { apple: 'Apple', google: 'Google', senha: 'usuário e senha' }[data.provedor];
      const origin = make('p', provider ? 'Entrada por ' + provider : 'Cadastro na IALD', 'registration-detail');
      const label = make('label', 'Nome para o cadastro');
      label.htmlFor = 'registration-name';
      const input = make('input');
      input.id = 'registration-name';
      input.name = 'nome';
      input.autocomplete = 'name';
      input.type = 'text';
      input.required = true;
      input.minLength = 2;
      input.maxLength = 80;
      const note = make('p', 'Esse nome será exibido ao administrador. Seu endereço privado da Apple, quando usado, continua protegido.', 'registration-detail');
      const status = make('p', '', 'registration-status');
      status.setAttribute('role', 'status');
      const actions = make('div', undefined, 'registration-actions');
      const later = make('button', 'Mais tarde');
      later.type = 'button';
      const save = make('button', 'Salvar nome');
      save.type = 'submit';
      actions.append(later, save);
      panel.append(title, description, origin, label, input, note, status, actions);
      overlay.append(panel);
      doc.body.append(overlay);
      let sending = false;
      const keydown = (event) => {
        if (event.key === 'Escape') {
          event.preventDefault(); event.stopImmediatePropagation();
          if (!sending) later.click();
        }
        if (event.key === 'Tab') {
          if (event.shiftKey && doc.activeElement === input) { event.preventDefault(); save.focus(); }
          else if (!event.shiftKey && doc.activeElement === save) { event.preventDefault(); input.focus(); }
        }
      };
      doc.addEventListener('keydown', keydown, true);
      closeDialog = () => {
        doc.removeEventListener('keydown', keydown, true);
        overlay?.remove();
        overlay = null;
        if (previousFocus?.isConnected) previousFocus.focus({ preventScroll: true });
        closeDialog = () => {};
        queueMicrotask(() => doc.dispatchEvent(new Event('iald:identification-closed')));
      };
      later.addEventListener('click', () => {
        if (sending) return;
        deferred.add(nextScope);
        closeDialog();
      });
      panel.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (sending || !current()) return;
        const name = input.value.trim().replace(/\s+/g, ' ');
        if (Array.from(name).length < 2 || Array.from(name).length > 80) {
          status.textContent = 'Informe um nome de 2 a 80 caracteres.';
          return;
        }
        sending = true;
        save.disabled = later.disabled = true;
        save.textContent = 'Salvando…';
        status.textContent = '';
        try {
          const result = await request(url, options(name));
          const saved = await result.json().catch(() => ({}));
          if (!current()) return;
          if (!result.ok || saved.nome_necessario !== false || !saved.nome) {
            status.textContent = typeof saved.error === 'string' ? saved.error : 'Não foi possível confirmar o nome. Tente novamente.';
            return;
          }
          deferred.add(nextScope);
          closeDialog();
        } catch {
          if (current()) status.textContent = 'Sem confirmação do servidor. Confira a conexão e tente novamente.';
        } finally {
          sending = false;
          save.disabled = later.disabled = false;
          save.textContent = 'Salvar nome';
        }
      });
      // No automatic keyboard: the sheet stays readable on small iPhones.
      later.focus({ preventScroll: true });
    } catch {
      // Registration lookup must not break an existing user's conversation.
    } finally {
      if (turn === revision) fetching = false;
    }
  }
  return { check, reset };
}
