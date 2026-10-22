"""Loopback visual fixture, prepared only; main may start this file explicitly.

127.0.0.1:8798. Real AST-extracted staged artifact/auth routes and static app assets;
synthetic accounts/store only. No production server import, credentials or providers.
The existing tests module builds the isolated Flask application without running tests.
Temporary artifacts stay below this work directory and are cleaned on normal shutdown.
"""
import atexit
from datetime import datetime
import hashlib
import html
import importlib.util
import json
import logging
import mimetypes
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
from flask import Response, jsonify, redirect, request, session
from werkzeug.exceptions import HTTPException
from werkzeug.serving import WSGIRequestHandler

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\app')
LOCAL = 'http://127.0.0.1:8798'
PUBLIC = 'https://demo.iald.ia.br'

# Only local assets/network. This also blocks the production app's CDN fallback.
LOCAL_CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
             "img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' data: blob:; "
             "connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'")
NAVIGATION_GUARD = r"""<script>
// Fixture-only mapping AFTER app handlers: validators see the original production
// URL, while a real link activation stays on loopback. Files on disk are unchanged.
document.addEventListener('click', localFixtureNavigation);
document.addEventListener('auxclick', localFixtureNavigation);
function localFixtureNavigation(event) {
  if (event.defaultPrevented) return;
  const anchor = event.target.closest && event.target.closest('a[href]');
  if (!anchor) return;
  let url; try { url = new URL(anchor.href, location.href); } catch (_) { return; }
  if (url.origin === location.origin) return;
  event.preventDefault();
  if (url.origin !== 'https://demo.iald.ia.br' ||
      !/^\/(api\/task-artifacts\/|task-(?:download|view)\/|app\/index\.html)/.test(url.pathname)) return;
  const local = location.origin + url.pathname + url.search;
  if (anchor.target === '_blank' || event.button === 1 || event.ctrlKey || event.metaKey)
    window.open(local, '_blank', 'noopener,noreferrer');
  else location.assign(local);
}
</script>"""


def create_app():
    spec = importlib.util.spec_from_file_location('_artifact_fixture_routes', WORK / 'tests' / 'test_artifact_routes.py')
    routes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(routes)
    case = routes.ArtifactRouteTests(methodName='test_anonymous_metadata_and_access_require_authentication')
    case.setUpClass()
    case.setUp()
    app = case.app
    app.testing = False
    app.logger.disabled = True
    artifacts = case.artifacts
    users = case.users
    # Keep artifact publication paths below legacy Windows MAX_PATH.
    fixture_temp = tempfile.TemporaryDirectory(prefix='f', dir=WORK)
    case.addCleanup(fixture_temp.cleanup)
    case.root = Path(fixture_temp.name)
    case.store = artifacts.ArtifactStore(case.root)
    case.env['SERVE_DIR'] = case.root
    try:
        raw = (WORK / 'TGL_Pagina_de_Apresentacao.html').read_bytes()
        current = case.store.ingest('alice', 'pagina.html', raw)
        past = int(time.time()) - 1800
        with patch.object(artifacts.time, 'time', return_value=past):
            expired = case.store.ingest('alice', 'expirada.html', raw)
        foreign = case.store.ingest('bob', 'outra.html', raw)
    except Exception:
        case.doCleanups()
        raise RuntimeError('Fixture could not validate the authorized HTML copy') from None

    cleanup = case.doCleanups
    app.extensions['artifact_fixture'] = {
        'cleanup': cleanup, 'store': case.store,
        'ids': {'current': current['id'], 'expired': expired['id'], 'foreign': foreign['id']},
        'staged_client': str(WORK / 'client' / 'iald.js'),
    }
    atexit.register(cleanup)
    public = case.env['PUBLIC_ROUTES']
    public.update({'fixture_links', 'fixture_login', 'fixture_state', 'fixture_home', 'fixture_static', 'fixture_health'})

    def loopback_only():
        if (request.remote_addr not in ('127.0.0.1', '::1') or request.host != '127.0.0.1:8798'):
            return Response('Fixture local somente.', status=403)
    app.before_request_funcs[None].insert(0, loopback_only)

    @app.after_request
    def fixture_headers(response):
        # The public wrapper has a strict script-free CSP, so map its two trusted
        # navigation links in the fixture response rather than injecting scripts.
        if request.endpoint == 'task_view' and response.status_code == 200:
            raw = response.get_data()
            for route in ('/task-download/', '/app/index.html'):
                raw = raw.replace(('href="' + PUBLIC + route).encode(),
                                  ('href="' + LOCAL + route).encode())
            response.set_data(raw)
        response.headers['Cache-Control'] = 'private, no-store'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Robots-Tag'] = 'noindex, nofollow'
        # Keep the actual preview/download CSP emitted by the extracted routes.
        if 'Content-Security-Policy' not in response.headers:
            response.headers['Content-Security-Policy'] = LOCAL_CSP
        return response

    @app.errorhandler(Exception)
    def safe_error(error):
        if isinstance(error, HTTPException): return Response('Rota de fixture indisponível.', status=error.code)
        return Response('Falha local da fixture; consulte os testes independentes.', status=503)

    @app.route('/')
    def fixture_home(): return redirect('/fixture-links')

    @app.route('/fixture-login/<owner>')
    def fixture_login(owner):
        if owner not in users: return Response('Usuário sintético inválido.', status=404)
        pending = session.get('pending_artifact_id')
        case.env['_abrir_sessao_web'](owner)
        destination = case.env['_destino_web'](owner)
        return redirect(destination if pending else '/fixture-links')

    @app.route('/logout')
    def fixture_logout():
        session.clear()
        return redirect('/fixture-links')

    app.view_functions['login'] = lambda: redirect('/fixture-links')

    @app.route('/fixture-links')
    def fixture_links():
        links = [
            ('Entrar como Alice (dona)', '/fixture-login/alice'),
            ('Entrar como Bob (outro dono)', '/fixture-login/bob'),
            ('Sair da conta sintética', '/logout'),
            ('Abrir prévia no app', '/app/index.html?artifact=' + current['id']),
            ('Abrir no app o artefato com ticket antigo expirado', '/app/index.html?artifact=' + expired['id']),
            ('Artefato de Bob (Alice deve ser recusada)', '/app/index.html?artifact=' + foreign['id']),
            ('Link autenticado histórico (formato de produção)', PUBLIC + '/api/task-artifacts/' + current['id']),
            ('Link antigo realmente expirado (formato de produção)', expired['mobile_url']),
        ]
        rendered = ''.join('<li><a href="' + html.escape(url, quote=True) + '">' + html.escape(label) + '</a></li>' for label, url in links)
        message = 'Cliente proposto disponível.' if (WORK / 'client' / 'iald.js').is_file() else 'Cliente proposto ainda ausente: o app será recusado com 503 até ele existir.'
        page = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>Fixture local de artefatos</title></head><body><h1>Artefatos — somente teste local</h1>'
                '<p>Conta sintética: ' + html.escape(session.get('username', 'sem login')) + '.</p><p>' + message + '</p>'
                '<p>Entre como Alice e abra o app. Os dois últimos links mantêm o formato de produção para testar reconhecimento; '
                'esta página encaminha a navegação exclusivamente ao servidor local. Tokens não são exibidos como texto nem registrados.</p><ul>'
                + rendered + '</ul>' + NAVIGATION_GUARD + '</body></html>')
        return Response(page, mimetype='text/html')

    @app.route('/fixture-state')
    def fixture_state():
        return jsonify(fixture=True, provider_calls=0, owner=session.get('username'),
                       artifact_ids=app.extensions['artifact_fixture']['ids'],
                       staged_client_present=(WORK / 'client' / 'iald.js').is_file())

    @app.route('/health')
    def fixture_health(): return jsonify(status='ok', fixture=True, provider_calls=0)

    @app.route('/api/motor')
    def motor(): return jsonify(motor='openai', modelo='fixture', plano='teste', consentimento={'dado': True},
        limites={'imagens': False, 'pensar': False, 'ferramentas': [], 'janela': 100000, 'max_saida': 4096})

    @app.route('/api/contexto')
    def context(): return jsonify(n_ctx=100000, margem=1000, reserva_resposta=4096, cpt=2.91, teto_mensagens=40)

    @app.route('/api/active-model')
    def active(): return jsonify(id='fixture', short='Teste local', label='Modelo simulado', online=True, n_ctx=100000, vision=False)

    @app.route('/api/tgl/balance')
    def balance(): return jsonify(username=session.get('username'), balance=0)

    def account(): return hashlib.sha256(('fixture-owner:' + session.get('username', '')).encode()).hexdigest()

    @app.route('/api/chat-jobs/session')
    def job_session(): return jsonify(account=account())

    @app.route('/api/chat-jobs', methods=['GET', 'POST'])
    def jobs():
        if request.method != 'GET': return jsonify(error='Fixture não inicia geração.'), 409
        return jsonify(account=account(), jobs=[])

    @app.route('/api/native-push/status')
    def push_status(): return jsonify(ios=False, android=False)

    @app.route('/api/conta/identificacao')
    def identity(): return jsonify(nome='Conta sintética', username=session.get('username'), nome_necessario=False)

    @app.route('/v1/chat/completions', methods=['POST'])
    def no_provider(): return jsonify(error='Fixture visual sem chamada de modelo.'), 409

    @app.route('/api/<path:path>', methods=['GET', 'POST'])
    def other_api(path): return jsonify(error='Endpoint não implementado nesta fixture.'), 404

    @app.route('/app/')
    @app.route('/app/index.html')
    def fixture_index(): return fixture_static('index.html')

    @app.route('/app/<path:path>')
    def fixture_static(path='index.html'):
        rel = Path(path)
        if rel.is_absolute() or '..' in rel.parts or any(part.startswith('.') for part in rel.parts):
            return Response('Recurso recusado.', status=404)
        if rel.suffix.lower() not in {'.html', '.js', '.css', '.png', '.svg', '.ico', '.woff', '.woff2', '.ttf'} or '.bak_' in path:
            return Response('Recurso recusado.', status=404)
        if path == 'iald.js':
            source = WORK / 'client' / 'iald.js'
            if not source.is_file(): return Response('Cliente proposto ainda indisponível.', status=503)
        else:
            source = ROOT / rel
            if not source.resolve().is_relative_to(ROOT.resolve()) or not source.is_file():
                return Response('Recurso não encontrado.', status=404)
        raw = source.read_bytes()
        if path == 'index.html':
            # Only the fixture response changes: no production or staged asset is edited.
            raw = raw.replace(b'</head>', NAVIGATION_GUARD.encode('utf-8') + b'</head>', 1)
        return Response(raw, mimetype=mimetypes.guess_type(path)[0] or 'application/octet-stream')

    return app


class QuietHandler(WSGIRequestHandler):
    # Capabilities can occur in paths. No access/error request line is ever printed.
    def log_request(self, *args, **kwargs): pass
    def log_error(self, *args, **kwargs): pass
    def log_message(self, *args, **kwargs): pass


if __name__ == '__main__':
    logging.getLogger('werkzeug').disabled = True
    app = create_app()
    app.run(host='127.0.0.1', port=8798, threaded=True, debug=False, use_reloader=False,
            request_handler=QuietHandler)
