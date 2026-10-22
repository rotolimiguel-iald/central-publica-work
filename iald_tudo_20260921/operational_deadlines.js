// Dates only: credentials and account administration never reach the client.
export function renderDeadlines(data, failed = false) {
  let panel = document.getElementById('iald-operational-deadlines');
  if (!data && !failed) { if (panel) panel.remove(); return; }
  if (!panel && !data) return;
  if (!panel) {
    const main = document.querySelector('main.principal');
    if (!main) return;
    panel = document.createElement('section');
    panel.id = 'iald-operational-deadlines';
    panel.setAttribute('aria-label', 'Validade das chaves e testes');
    panel.style.cssText = 'flex-shrink:0;padding:8px 16px;border-bottom:1px solid #b7985860;font:12px/1.45 system-ui;max-height:150px;overflow:auto';
    main.prepend(panel);
  }
  panel.replaceChildren();
  const title = document.createElement('strong');
  title.textContent = 'Chaves e testes · painel do operador';
  panel.append(title);
  if (failed) {
    const text = document.createElement('p');
    text.textContent = 'Não foi possível atualizar os prazos. Confira antes de usar.';
    panel.append(text); return;
  }
  for (const item of data.items || []) {
    const line = document.createElement('div');
    const date = item.expires_at ? new Date(item.expires_at).toLocaleString('pt-BR', {timeZone:'America/Sao_Paulo'}) + ' (Brasília)' : '';
    line.textContent = `${item.label}: ${item.message}${date ? ' · '+date : ''}`;
    line.dataset.level = item.level;
    if (['critical', 'expired'].includes(item.level)) line.style.color = '#d95757';
    if (['warning', 'attention', 'unknown'].includes(item.level)) line.style.fontWeight = '600';
    panel.append(line);
  }
  if (data.error) {
    const error = document.createElement('div'); error.textContent = data.error; panel.append(error);
  }
}
