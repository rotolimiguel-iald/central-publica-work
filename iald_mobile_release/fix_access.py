from pathlib import Path
from datetime import datetime
import ast
import textwrap

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

def write(path, text):
    old = path.read_bytes()
    new = text.encode('utf-8')
    backup = path.with_name(path.name + '.bak_' + STAMP)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_release')
    temp.write_bytes(new)
    assert temp.stat().st_size == len(new) and new
    temp.replace(path)
    assert path.read_bytes() == new

path = ROOT / 'iald_web_server.py'
source = path.read_text(encoding='utf-8-sig')

def replace_function(name, replacement):
    global source
    nodes = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(nodes) == 1, name
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    indent = ' ' * node.col_offset
    body = textwrap.indent(textwrap.dedent(replacement).strip(), indent) + '\n'
    source = ''.join(lines[:node.lineno - 1]) + body + ''.join(lines[node.end_lineno:])

source = source.replace('session, redirect, url_for, make_response, jsonify', 'session, redirect, url_for, make_response, jsonify, g, has_request_context')
source = source.replace("app = Flask(__name__, static_folder=SERVE_DIR, static_url_path='')", "app = Flask(__name__, static_folder=None)")
source = source.replace('app.secret_key = load_or_create_secret_key()', 'app.secret_key = load_or_create_secret_key()\napp.config["SESSION_REFRESH_EACH_REQUEST"] = False')
source = source.replace('FERRAMENTAS_FORA_DA_LOJA = {"request_contract"}', 'FERRAMENTAS_FORA_DA_LOJA = {"request_contract", "tgl_transfer", "psinet_send", "lembrar", "esquecer", "consultar_memoria"}')

replace_function('require_auth', '''
def require_auth():
    if request.endpoint in PUBLIC_ROUTES or request.path.lstrip('/') in PUBLIC_FILES:
        return None
    def denied():
        if request.path.startswith(('/api/', '/v1/', '/admin/api/')) or request.is_json:
            return jsonify({'error': 'Não autenticado'}), 401
        return redirect(url_for('login'))
    if request.headers.get('Authorization'):
        username = _usuario_do_token()
        session.clear()
        if not username:
            return denied()
        # Only this request may use a bearer identity. It must not become a cookie.
        session.update(authenticated=True, username=username, is_admin=False, app_surface=True)
        g.app_bearer = True
        return None
    username = session.get('username', '')
    user = load_users().get(username)
    version = hashlib.sha256((user or {}).get('password_hash', '').encode()).hexdigest()
    if (not session.get('authenticated') or not user or session.get('app_surface')
            or session.get('auth_version') != version):
        session.clear()
        return denied()
    try:
        last = datetime.fromisoformat(session.get('last_active', ''))
        if datetime.now() - last > timedelta(hours=SESSION_TIMEOUT_HOURS):
            session.clear()
            return denied()
    except (ValueError, TypeError):
        session.clear()
        return denied()
    session['is_admin'] = bool(user.get('admin'))
    session['last_active'] = datetime.now().isoformat()
    return None
''')

source = source.replace('return _serializador_token().dumps({"u": username})', '''user = load_users().get(username)
        if not user:
            return ""
        version = hashlib.sha256(user.get("password_hash", "").encode()).hexdigest()
        return _serializador_token().dumps({"u": username, "v": version})''')
source = source.replace('    return usuario\n', '''    version = hashlib.sha256(load_users()[usuario].get("password_hash", "").encode()).hexdigest()
    if dados.get("v") != version:
        return ""
    return usuario
''', 1)
source = source.replace('    return resp\n\n\nPUBLIC_ROUTES', '''    if getattr(g, "app_bearer", False):
        session.modified = False
    return resp


PUBLIC_ROUTES''', 1)
# Authentication endpoints issue bearer tokens only; legacy app cookies are invalidated.
for name in ['api_apple_signin', 'api_dispositivo_signin']:
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    lines = source.splitlines(keepends=True)
    block = ''.join(lines[node.lineno-1:node.end_lineno])
    start = block.index('    session.permanent = True')
    end = block.index('    auth_log(', start)
    block = block[:start] + '    session.clear()\n' + block[end:]
    block = block.replace('    identity_token = ', "    if not isinstance(data, dict):\n        return jsonify({'error': 'JSON deve ser um objeto'}), 400\n    identity_token = ", 1) if name == 'api_apple_signin' else block.replace('    bruto = ', "    if not isinstance(data, dict):\n        return jsonify({'error': 'JSON deve ser um objeto'}), 400\n    bruto = ", 1)
    block = block.replace('elif APPLE_SIGNIN_INSEGURO:', 'elif app.testing and APPLE_SIGNIN_INSEGURO:')
    block = block.replace("(data.get('identity_token') or '').strip()", "str(data.get('identity_token') or '').strip()")
    block = block.replace('(data.get("identity_token") or "").strip()', 'str(data.get("identity_token") or "").strip()')
    block = block.replace('(data.get("device_id") or "").strip()', 'str(data.get("device_id") or "").strip()')
    source = ''.join(lines[:node.lineno-1]) + block + '\n' + ''.join(lines[node.end_lineno:])
source = source.replace('        session.permanent = True\n        session["authenticated"] = True', '''        session.clear()
        session.permanent = True
        session["auth_version"] = hashlib.sha256(user_data["password_hash"].encode()).hexdigest()
        session["authenticated"] = True''', 1)
replace_function('_verificar_identity_token', '''
def _verificar_identity_token(token):
    if not token:
        return '', '', 'identity_token ausente'
    if not APPLE_BUNDLE_ID:
        return '', '', 'IALD_APPLE_BUNDLE_ID não configurado no servidor'
    try:
        import jwt as _jwt
        key = _cliente_jwks_apple().get_signing_key_from_jwt(token).key
        claims = _jwt.decode(token, key, algorithms=['RS256'], audience=APPLE_BUNDLE_ID,
                             issuer=APPLE_ISSUER,
                             options={"require": ["exp", "iat", "iss", "aud", "sub"]})
        subject = claims['sub'].strip()
        if not subject:
            return '', '', 'token sem identidade'
        return subject, str(claims.get('email') or '').strip(), ''
    except Exception as exc:
        return '', '', f'token recusado ({type(exc).__name__})'
''')

for name in ['api_access_status', 'api_request_access', 'api_apple_auth']:
    replace_function(name, f'''
def {name}():
    return jsonify({{'error': 'Esta versão de acesso foi descontinuada. Atualize o app.'}}), 410
''')

# Tunnel connections also arrive via loopback, so both peer and host are checked.
helper = '''def _local_operator_request():
    if not has_request_context():
        return False
    return (request.remote_addr in ("127.0.0.1", "::1")
            and request.host.split(":")[0].lower() in ("localhost", "127.0.0.1")
            and not any(request.headers.get(h) for h in
                        ("CF-Connecting-IP", "X-Forwarded-For", "Forwarded", "X-Forwarded-Host")))


'''
source = source.replace('def require_admin():', helper + 'def require_admin():', 1)
replace_function('require_admin', '''
def require_admin():
    if not _local_operator_request():
        return jsonify({'error': 'Acesso restrito a localhost'}), 403
    if not session.get('is_admin'):
        return jsonify({'error': 'Apenas administradores'}), 403
    return None
''')
# Worker threads must receive an explicit authorization computed in the request.
source = source.replace('def execute_public_tool(tool_name, arguments, user="?"):', 'def execute_public_tool(tool_name, arguments, user="?", operator_authorized=False):')
replace_function('_e_operador', '''
def _e_operador(u):
    try:
        return operator_authorized and bool(load_users().get((u or '').strip().lower(), {}).get('admin'))
    except Exception:
        return False
''')
source = source.replace('               ferramentas=None):', '               ferramentas=None, operator_authorized=False):', 1)
source = source.replace('lambda: execute_public_tool(tool_name, tool_args, user=user)', '''lambda: execute_public_tool(tool_name, tool_args, user=user,
                                                operator_authorized=operator_authorized)
                    if tool_name in {(t.get("function") or {}).get("name") for t in
                                     (ferramentas if ferramentas is not None else PUBLIC_TOOLS)}
                    else "Ferramenta não autorizada para esta sessão."''', 1)
source = source.replace('    # ── SMART ROUTING:', '''    if session.get("app_surface"):
        superficie = "app"
    operator_authorized = _local_operator_request() and bool(session.get("is_admin"))

    # ── SMART ROUTING:''', 1)
source = source.replace('ferramentas=_ferramentas_para(superficie))', 'ferramentas=_ferramentas_para(superficie),\n                                      operator_authorized=operator_authorized)', 1)
replace_function('static_files', '''
def static_files(filename):
    allowed = {
        'iald_chat.html', 'iald_cartao_virtual.html', 'iald_cartao_visita.html',
        'iald_logo_header.png', 'sw.js', 'manifest.json',
        'app/index.html', 'app/iald.js', 'app/iald.css',
        'app/kernel_prompt.js', 'app/kernel_prompt_loja.js', 'app/kernel_prompt_bundle.js',
    }
    if filename not in allowed:
        return Response('Arquivo não disponível.', status=404)
    return send_from_directory(SERVE_DIR, filename)
''')
ast.parse(source)
assert 'options={"require": ["exp", "iat", "iss", "aud", "sub"]}' in source
assert 'if getattr(g, "app_bearer", False)' in source
write(path, source)

js_path = ROOT / 'app/iald.js'
js = js_path.read_text(encoding='utf-8-sig')
js = js.replace("const VERSAO = 'app v1 · 11/09/2026';", "const VERSAO = 'IALD 4.1 · beta';")
js = js.replace("function fetchIALD(caminho, opcoes)", "async function fetchIALD(caminho, opcoes)")
js = js.replace("o.credentials = (SUPERFICIE === 'app') ? 'include' : 'same-origin';", "o.credentials = (SUPERFICIE === 'app') ? 'omit' : 'same-origin';")
js = js.replace('  return fetch(BASE + caminho, o);', '''  const response = await fetch(BASE + caminho, o);
  if (response.status === 401 && SUPERFICIE === 'app' && t && tokenApp() === t) {
    limparTokenApp();
    avaliarPortao();
    erroDoPortao('Sua sessão expirou. Entre novamente para continuar.');
  }
  return response;''', 1)
js = js.replace("if (r.status === 401) { location.href = '/login'; return; }", "if (r.status === 401) { if (SUPERFICIE !== 'app') location.href = '/login'; return; }")
js = js.replace("    location.href = '/login';\n    throw new DOMException", "    if (SUPERFICIE !== 'app') location.href = '/login';\n    throw new DOMException", 1)
js = js.replace("$('#btn-sair').addEventListener('click', () => { location.href = '/logout'; });", '''$('#btn-sair').addEventListener('click', () => {
    if (SUPERFICIE !== 'app') { location.href = '/logout'; return; }
    if (S.aborto) S.aborto.abort();
    limparTokenApp();
    fecharFolhas();
    avaliarPortao();
  });''', 1)
js = js.replace('''    const plug = window.Capacitor && window.Capacitor.Plugins
      && window.Capacitor.Plugins.SignInWithApple;''', '''    const cap = window.Capacitor;
    const plug = cap && ((cap.Plugins && cap.Plugins.SignInWithApple)
      || (cap.registerPlugin && cap.registerPlugin('SignInWithApple')));''', 1)
js = js.replace("      // Último recurso: pior em qualidade, mas ainda com 16+ caracteres.\n      id = 'd' + Date.now().toString(36) + Math.random().toString(36).slice(2)\n        + Math.random().toString(36).slice(2);", "      throw new Error('Não foi possível criar um identificador seguro neste aparelho.');")
js = js.replace("'O acesso é imediato e gratuito. Não pedimos conta, e-mail '\n        + 'nem nenhum dado seu, e não há compra de espécie alguma dentro do aplicativo.'", "'O acesso é gratuito. Criamos um identificador aleatório neste aparelho. '\n        + 'Suas mensagens são enviadas ao servidor da IALD para gerar respostas.'")
write(js_path, js)
vp = ROOT / 'iald-app/scripts/validate-release.mjs'
write(vp, vp.read_text().replace('\\\\', '\\'))
print('Applied targeted access and native session fixes with byte backups.')
