"""Rebuild only this client staging directory from the production JS read-only.

No deployment, native build, network request or dependency installation occurs.
Deliver iald.js; helper sources are embedded, requiring no extra public route.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD\app\iald.js')


def build(source):
    original = source.read_bytes()
    text = original.decode('utf-8').replace('\r\n', '\n')
    def replace(old, new, count=1):
        nonlocal text
        if text.count(old) != count:
            raise RuntimeError(f'Anchor count differs ({text.count(old)} != {count}): {old[:90]!r}')
        text = text.replace(old, new)

    helper = (HERE / 'chat_jobs.js').read_text(encoding='utf-8').replace('export ', '')
    push_root = HERE.parent / 'notifications' / 'client'
    push_core = (push_root / 'native-notifications.mjs').read_text(encoding='utf-8').replace('export ', '')
    push_registration = (push_root / 'registration.mjs').read_text(encoding='utf-8')
    push_registration = '\n'.join(line for line in push_registration.splitlines() if not line.startswith('import ')).replace('export ', '')
    push_settings = (HERE / 'notification_settings.js').read_text(encoding='utf-8').replace('export ', '')
    helper += '\nconst NativePushSidecar = (() => {\n' + push_core + '\n' + push_registration + '\n' + push_settings + '\nreturn { connectNotifications, createNotificationSettings };\n})();\n'
    integration = (HERE / 'background_integration.js').read_text(encoding='utf-8')
    integration += '\n' + (HERE / 'native_notifications_integration.js').read_text(encoding='utf-8')
    replace("const VERSAO =", helper + '\n\nconst VERSAO =')
    replace('const svg =', integration + '\n\nconst svg =')
    replace('function desanexarRespostasBackground(sair = false) {', 'function desanexarRespostasBackground(sair = false) {\n  if (sair) disconnectNativeNotificationsUI();')
    replace('  return backgroundOwner;\n}', '  refreshNativeNotificationsUI();\n  return backgroundOwner;\n}')
    replace("pintarUsuario(); abrirFolha('folha-config');", "pintarUsuario(); abrirFolha('folha-config'); refreshNativeNotificationsUI(true);")
    replace("export function guardarTokenApp(t) {\n  guardar", "export function guardarTokenApp(t) {\n  if (tokenApp() !== (t || '')) desanexarRespostasBackground(true);\n  guardar")
    replace("export function limparTokenApp() {\n  sheetAfterRegistration", "export function limparTokenApp() {\n  desanexarRespostasBackground(true);\n  sheetAfterRegistration")
    replace("function salvarConversas() {\n  guardar", "function salvarConversas() {\n  if (!DEMO && backgroundOwner) { persistirConversasBackground(); return; }\n  guardar")
    replace("S.conversas.unshift({ id, titulo: 'Nova conversa',", "S.conversas.unshift({ id, background_owner: backgroundOwner || undefined, titulo: 'Nova conversa',")
    replace("function desenharMensagem(papel, conteudo, vazia, modelo) {\n  const area = $('#conversa-interna');", "function desenharMensagem(papel, conteudo, vazia, modelo, destino = null) {\n  const area = destino || $('#conversa-interna');")
    replace(".msg:not([data-aviso])", ".msg:not([data-aviso]):not([data-background-pending])")
    replace("function enviar() {\n  const texto", "function enviar() {\n  if (!DEMO && !backgroundOwner) { recuperarRespostasBackground(); avisarBackground('Aguarde a identificação da conta antes de enviar.'); return; }\n  const texto")
    replace("function enviarTexto(texto, anexos) {\n  const c", "function enviarTexto(texto, anexos) {\n  if (!DEMO && !backgroundOwner) { recuperarRespostasBackground(); return; }\n  const c")
    for signature in ['function enviar() {', 'function enviarTexto(texto, anexos) {', 'function editarMensagem(linha) {', 'function refazer(linha) {', 'function reenviarUltima() {']:
        replace(signature, signature + '\n  if (respostaPendenteBackground()) return;')
    replace("async function transmitir(mensagens) {", "async function transmitir(mensagens, retomada = null) {\n  if (S.gerando) return;")
    replace("  const origem = conversaAtiva();\n  const selagem", "  const origem = retomada ? conversaDoJob(retomada) : conversaAtiva();\n  if (!origem) return;\n  const epoch = backgroundEpoch;\n  const turn = {}; S.backgroundTurn = turn;\n  const currentTurn = () => S.backgroundTurn === turn && epoch === backgroundEpoch;\n  let job = retomada, doneReceived = false, failure = null;\n  const selagem")
    replace("  S.aborto = new AbortController();\n\n  const corpo = desenharMensagem('ai', '', true);", "  const controller = new AbortController();\n  S.aborto = controller;\n  if (retomada) document.querySelectorAll('[data-background-job=\"' + retomada.request_id + '\"]').forEach((n) => n.remove());\n  const corpo = desenharMensagem('ai', '', true, null, origem.id === S.ativaId ? null : document.createElement('div'));\n  corpo.parentElement.dataset.backgroundPending = '1';")
    replace("  const pintarAgora = () => {\n    if (retirada) return;", "  const pintarAgora = () => {\n    if (retirada || !currentTurn()) return;")
    replace("  try {\n    const linhas = DEMO\n      ? fluxoDemo()\n      : fluxoHttp(mensagens, S.aborto.signal, selagem);", """  try {
    if (!DEMO) {
      if (!backgroundOwner || origem.background_owner !== backgroundOwner) throw detached();
      persistirConversasBackground();
      job ||= await backgroundJobs.begin(corpoPedidoBackground(mensagens, selagem));
      if (!currentTurn()) throw detached();
      activeBackgroundJob = job;
      corpo.parentElement.dataset.backgroundJob = job.request_id;
      const cancelExplicitly = () => {
        if (controller.signal.reason?.type === 'user_cancel') {
          backgroundJobs.cancel(job).catch((error) => backgroundJobs.report(error)).finally(agendarRecuperacaoBackground);
        }
      };
      controller.signal.addEventListener('abort', cancelExplicitly, { once: true });
      if (controller.signal.aborted) { cancelExplicitly(); throw detached(); }
    }
    const linhas = DEMO ? fluxoDemo() : fluxoHttp(mensagens, controller.signal, selagem, job);""")
    replace("      if (carga === '[DONE]') break;", "      if (!currentTurn()) throw detached();\n      if (carga === '[DONE]') { doneReceived = true; break; }")
    start = text.index('  } catch (e) {\n    tirarDigitando();', text.index('async function transmitir('))
    end = text.index('\n}\n\n// ═', start)
    text = text[:start] + (HERE / 'transmit_finally.js').read_text(encoding='utf-8').rstrip() + text[end:]
    start = text.index('async function* fluxoHttp(')
    end = text.index('// ── modo demonstracao', start)
    text = text[:start] + """async function* fluxoHttp(mensagens, signal, selagem, job) {
  if (!job) throw new PendingChatJobError('Pedido durável ausente; nenhum envio foi iniciado.');
  yield* backgroundJobs.stream(job, { signal });
}

""" + text[end:]
    replace("function parar() {\n  if (S.aborto) S.aborto.abort();", "function parar() {\n  if (S.aborto) S.aborto.abort({ type: 'user_cancel' });")
    replace("  falha_motor: ['Falha na resposta', ICONE.alerta, 'erro'],", "  falha_motor: ['Falha na resposta', ICONE.alerta, 'erro'],\n  resposta_interrompida: ['Resposta interrompida', ICONE.alerta, ''],")
    replace("  $('#btn-sair').addEventListener('click', () => {\n    desfazerPendente", "  $('#btn-sair').addEventListener('click', async () => {\n    if (SUPERFICIE === 'app' && !await prepareNativePushLogout()) return;\n    desanexarRespostasBackground(true);\n    desfazerPendente")
    replace("  verificarIdentificacaoCadastro();\n  $('#entrada').focus();", "  verificarIdentificacaoCadastro();\n  recuperarRespostasBackground();\n  $('#entrada').focus();")
    replace("  if (!portaoNecessario()) verificarIdentificacaoCadastro();\n}", "  if (!portaoNecessario()) verificarIdentificacaoCadastro();\n  ligarRespostasBackground();\n  startNativeNotificationsUI();\n}")
    replace("function apagarConversa(id) {\n  const indice", "async function apagarConversa(id) {\n  if (!await apagarJobsDaConversa(id)) return;\n  const indice")
    start = text.index('  // a resposta em curso é gravada', text.index('async function apagarConversa'))
    end = text.index('  const conversa = S.conversas[indice];', start)
    text = text[:start] + text[end:]
    replace("  $('#exp-limpar').addEventListener('click', () => {\n    const c = conversaAtiva();\n    if (c) { c.mensagens = [];", "  $('#exp-limpar').addEventListener('click', async () => {\n    const c = conversaAtiva();\n    if (c && !await apagarJobsDaConversa(c.id)) return;\n    if (c) { delete c.chat_job_deliveries; c.mensagens = [];")
    replace("  desfazerPendente = null;                               // conta excluída", "  if (backgroundOwner) {\n    localStorage.removeItem(backgroundHistoryKey(backgroundOwner));\n    backgroundJobs.forgetOwner();\n  }\n  desanexarRespostasBackground(true);\n  desfazerPendente = null;                               // conta excluída")
    replace("  for (const m of c.mensagens) desenharMensagem(m.role === 'assistant' ? 'ai' : 'user', m.content, false, m.modelo);", """  for (const m of c.mensagens) desenharMensagem(m.role === 'assistant' ? 'ai' : 'user', m.content, false, m.modelo);
  for (const delivery of Object.values(c.chat_job_deliveries || {})) {
    if (!delivery.notice) continue;
    const body = desenharMensagem('ai', '', true);
    pintarAviso(body.parentElement, body.querySelector('.conteudo'), delivery.notice, '');
  }""")
    # Keep the public production file untouched; only files beside this builder are outputs.
    outputs = {
        'iald.js': text.encode('utf-8'),
        'client.patch': ''.join(difflib.unified_diff(original.decode('utf-8').replace('\r\n', '\n').splitlines(True), text.splitlines(True), fromfile='a/app/iald.js', tofile='b/app/iald.js')).encode('utf-8'),
        'build_manifest.json': json.dumps({'source': str(source), 'source_sha256': hashlib.sha256(original).hexdigest(), 'output_sha256': hashlib.sha256(text.encode()).hexdigest(), 'deploy_files': ['app/iald.js'], 'native_changes': False}, indent=2).encode(),
    }
    for name, raw in outputs.items():
        target = HERE / name
        temporary = target.with_suffix(target.suffix + '.tmp')
        temporary.write_bytes(raw)
        if temporary.read_bytes() != raw: raise OSError('Staging write verification failed')
        os.replace(temporary, target)
    print(json.dumps({'staged': str(HERE / 'iald.js'), 'bytes': len(text.encode())}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    build(parser.parse_args().source.resolve())
