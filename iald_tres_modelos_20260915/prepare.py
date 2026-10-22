from datetime import datetime
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
STAGE = WORK / 'stage'
EXPECTED = {'iald_web_server.py':'4f486f702527984f', 'iald_motores.py':'f193d71e758a8f68',
            'iald_memoria_canonica.py':'a93dda0c633dc083', 'app/iald.js':'7106e815d65e1e64',
            'app/index.html':'4bcbcbc60a7ef196','app/iald.css':'3c1ce4488beb16ab'}
ASSETS = ['app', 'iald-app/www', 'iald-app/ios/App/App/public', 'iald-app/android/app/src/main/assets/public']

def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f: f.write(data)
    assert path.read_bytes() == data

def edit(name, pairs):
    before = (ROOT / name).read_bytes()
    text = before.decode().replace('\r\n','\n')
    for old, new in pairs:
        assert text.count(old) == 1, f'{name}: expected one occurrence of {old[:100]!r}, found {text.count(old)}'
        text = text.replace(old,new)
    if b'\r\n' in before: text = text.replace('\n','\r\n')
    create(STAGE / name, text.encode())

def main():
    for name, expected in EXPECTED.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest().startswith(expected), 'Baseline differs: ' + name
    files = ['iald_web_server.py','iald_motores.py','iald_orcamento.py'] + [a+'/'+f for a in ASSETS for f in ['iald.js','iald.css']]
    baseline = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}
    create(WORK/'baseline.json', json.dumps(baseline, indent=2).encode())
    edit('iald_motores.py', [('def config_da_conta(cfg, registro):', '''def rotulo_do_modelo(modelo):
    """Display a server-selected model without relabeling unrelated models."""
    if modelo == "gpt-5.6-luna" or str(modelo).startswith("gpt-5.6-luna-"):
        return "ChatGPT 5.6 Luna"
    return "ChatGPT · " + str(modelo)


def config_da_conta(cfg, registro):''')])
    edit('iald_orcamento.py', [('    def summary(self):', '''    def by_model_today(self):
        """Daily inference costs and reservations by actual recorded model."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT model, COUNT(*), SUM(COALESCE(actual,cap)) FROM calls "
                "WHERE day=? GROUP BY model ORDER BY model", (_today(self.clock),)).fetchall()
        return [{"model": model, "calls": count, "usd": round(amount, 8)}
                for model, count, amount in rows]

    def summary(self):''')])
    edit('iald_web_server.py', [
        ('def _opcoes_de_motor(registro):', '''def _modelo_nativo_resposta():
    model = str(ACTIVE_MODEL_ID)
    label = "IALD Nativa · Qwen3.6-35B" if ("35b" in model.lower() or "qwen3.6" in model.lower()) else "IALD Nativa · " + model
    return {"motor": "nativa", "id": model, "rotulo": label}


def _identificar_resposta(resposta, modelo):
    """Attach server provenance; forward the original SSE bytes and close it on cancel."""
    if resposta.status_code != 200:
        return resposta
    if resposta.mimetype == "text/event-stream":
        original = resposta.response
        def identified():
            try:
                yield "data: " + json.dumps({"iald_modelo": modelo}, ensure_ascii=False) + "\\n\\n"
                yield from original
            finally:
                close = getattr(original, "close", None)
                if close:
                    close()
        resposta.response = identified()
    elif resposta.is_json:
        data = resposta.get_json()
        if isinstance(data, dict) and data.get("choices"):
            data["iald_modelo"] = modelo
            resposta.set_data(json.dumps(data, ensure_ascii=False))
    return resposta


def _opcoes_de_motor(registro):'''),
        ('{"id": iald_motores.NATIVA, "rotulo": "IALD Nativa", "detalhe": "Qwen3.6-35B · servidor da IALD",',
         '{"id": iald_motores.NATIVA, "rotulo": _modelo_nativo_resposta()["rotulo"], "detalhe": "Servidor da IALD",'),
        ('{"id": iald_motores.OPENAI, "rotulo": "ChatGPT", "detalhe": f"OpenAI · {modelo_ext}",',
         '{"id": iald_motores.OPENAI, "rotulo": iald_motores.rotulo_do_modelo(modelo_ext), "detalhe": f"OpenAI · {modelo_ext}",'),
        ('        resposta = Response(fluxo, status=200, content_type="text/event-stream",\n                            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})',
         '        resposta = Response(fluxo, status=200, content_type="text/event-stream",\n                            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})\n        resposta = _identificar_resposta(resposta, {"motor": "openai", "id": modelo,\n                                    "rotulo": iald_motores.rotulo_do_modelo(modelo)})'),
        ('            return Response(\n                _medir_saida_sse(generate(), user, "agente"),',
         '            return _identificar_resposta(Response(\n                _medir_saida_sse(generate(), user, "agente"),'),
        ('                    "X-Accel-Buffering": "no",\n                }\n            )',
         '                    "X-Accel-Buffering": "no",\n                }\n            ), _modelo_nativo_resposta())'),
        ('            return _stream_proxy(subpath, body, user=user, origem="chat")',
         '            return _identificar_resposta(_stream_proxy(subpath, body, user=user, origem="chat"),\n                                         _modelo_nativo_resposta())'),
        ('        return result\n\n# ══════════════════════════════════════════════════════════════\n# CRÉDITO DE USO',
         '        return _identificar_resposta(result, _modelo_nativo_resposta()) if subpath == "chat/completions" else result\n\n# ══════════════════════════════════════════════════════════════\n# CRÉDITO DE USO'),
        ('    return jsonify({\n        "chave_definida": bool(cfg.chave), "prompt_sha256": PROMPT_EXTERNO_SHA,',
         '    try:\n        gasto_modelos = _guarda_openai().by_model_today()\n    except Exception:\n        gasto_modelos = None\n        erro = (erro + "; " if erro else "") + "gasto por modelo indisponível"\n    return jsonify({\n        "gasto_por_modelo_hoje": gasto_modelos,\n        "chave_definida": bool(cfg.chave), "prompt_sha256": PROMPT_EXTERNO_SHA,'),
        ("+((d.cobrancas_acima_da_reserva||[]).length?", "+(d.gasto_por_modelo_hoje||[]).map(function(x){{return ' \\u00b7 '+x.model+': US$ '+Number(x.usd).toFixed(4)+' (inclui reservas)'}}).join('')+((d.cobrancas_acima_da_reserva||[]).length?")
    ])
    js = [
        ("for (const m of c.mensagens) desenharMensagem(m.role === 'assistant' ? 'ai' : 'user', m.content);", "for (const m of c.mensagens) desenharMensagem(m.role === 'assistant' ? 'ai' : 'user', m.content, false, m.modelo);"),
        ('function desenharMensagem(papel, conteudo, vazia) {', '''function modeloDaResposta(valor) {
  if (!valor || typeof valor !== 'object' || typeof valor.id !== 'string' || typeof valor.rotulo !== 'string') return null;
  if (!valor.id.trim() || !valor.rotulo.trim() || valor.id.length > 200 || valor.rotulo.length > 200) return null;
  return { id: valor.id, rotulo: valor.rotulo, motor: typeof valor.motor === 'string' ? valor.motor.slice(0, 40) : '' };
}

function pintarModeloResposta(corpo, modelo) {
  const rotulo = corpo.querySelector('.msg-modelo');
  if (!rotulo) return;
  const dado = modeloDaResposta(modelo);
  rotulo.textContent = dado ? dado.rotulo : '';
  rotulo.hidden = !dado;
  if (dado) rotulo.title = dado.id;
}

function desenharMensagem(papel, conteudo, vazia, modelo) {'''),
        ("  if (papel === 'ai') {\n    corpo.appendChild(el('div', 'trilha'));", "  if (papel === 'ai') {\n    corpo.appendChild(el('div', 'msg-modelo'));\n    pintarModeloResposta(corpo, modelo);\n    corpo.appendChild(el('div', 'trilha'));"),
        ('  let aviso = null;\n', '  let aviso = null;\n  let modeloRespondente = null;\n'),
        ('      if (ck.iald_status) { tirarDigitando();', '      if (ck.iald_modelo) {\n        const modelo = modeloDaResposta(ck.iald_modelo);\n        if (modelo && !modeloRespondente) { modeloRespondente = modelo; pintarModeloResposta(corpo, modelo); }\n        continue;\n      }\n      if (ck.iald_status) { tirarDigitando();'),
        ("        c.mensagens.push({ role: 'assistant', content: limpo });", "        const resposta = { role: 'assistant', content: limpo };\n        if (modeloRespondente) resposta.modelo = modeloRespondente;\n        c.mensagens.push(resposta);")
    ]
    css = '\n/* Model provenance supplied by the server for this response. */\n.msg-modelo { color: var(--texto-2); font-size: 11px; line-height: 1.5; margin-bottom: 8px; }\n.msg-modelo[hidden] { display: none; }\n'
    for asset in ASSETS:
        edit(asset+'/iald.js', js)
        before = (ROOT / asset / 'iald.css').read_bytes()
        create(STAGE/asset/'iald.css', before + css.replace('\n','\r\n' if b'\r\n' in before else '\n').encode())
    for name in files:
        if name.endswith('.py'): compile((STAGE/name).read_bytes(), name, 'exec')
    create(WORK/'requirements.json', json.dumps({'at':datetime.now().astimezone().isoformat(),
        'errata':'SEM O SOL; T2 and T3.1/T3.2 canceled/satisfied',
        'tasks':{'T1':'two options, server response labels, daily per-model spending',
                 'T3':'specified env caps x3, global shared with luiz = 3 USD/day',
                 'T4':'new build 16 APK/AAB signature verification, audited private push, Xcode Cloud/TestFlight',
                 'T5':'new regression tests, entire suite under write/network guard, no new red suites'},
        'status':'PREPARED_NOT_INSTALLED'},ensure_ascii=False,indent=2).encode())
    print('Prepared two-model labels and cost display; no production edits.')

if __name__ == '__main__': main()
