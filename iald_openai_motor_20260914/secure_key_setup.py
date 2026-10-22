"""Single-use localhost form. Never emit a credential to stdout or HTTP responses."""
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import html
import hmac
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import threading
from urllib.parse import parse_qs

TARGET = Path(r"C:\IALD\projetos_pyhton\IALD\.env")
TOKEN = secrets.token_urlsafe(32)
CSRF = secrets.token_urlsafe(32)
SAVED = False


def protected_write(path, data):
    # Set a per-user Windows ACL on the empty file BEFORE writing any secret.
    with path.open("xb"):
        pass
    owner = subprocess.run(["whoami"], capture_output=True, text=True, check=True).stdout.strip()
    result = subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r",
                             owner + ":F", "*S-1-5-18:F"], capture_output=True)
    if result.returncode:
        raise RuntimeError("Não foi possível proteger a credencial.")
    with path.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if path.read_bytes() != data:
        raise RuntimeError("Falha ao verificar gravação protegida.")


def save_key(value):
    if not re.fullmatch(r"sk-[A-Za-z0-9_-]{20,500}", value):
        raise ValueError("Formato de chave inválido.")
    before = TARGET.read_bytes() if TARGET.exists() else b""
    original = before.decode("utf-8-sig")
    pattern = r"(?m)^\s*IALD_OPENAI_API_KEY\s*=\s*(.*?)\s*$"
    existing = re.search(pattern, original)
    if existing and existing.group(1).strip("\"'"):
        raise ValueError("Já existe uma chave configurada. Substituição exige uma nova decisão do operador.")
    suffix = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    if before:
        protected_write(TARGET.with_name(TARGET.name + ".bak_" + suffix), before)
    newline = "\r\n" if b"\r\n" in before else "\n"
    line = "IALD_OPENAI_API_KEY=" + value
    if existing:
        after = re.sub(pattern, lambda match: line, original, count=1).encode("utf-8")
    else:
        after = before + (b"" if before.endswith(b"\n") or not before else newline.encode()) + (line + newline).encode()
    temp = TARGET.with_name(TARGET.name + ".tmp_" + suffix)
    protected_write(temp, after)
    if TARGET.exists() and TARGET.read_bytes() != before:
        raise RuntimeError("O .env mudou em outra sessão; instalação recusada para preservar a alteração.")
    os.replace(temp, TARGET)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, code, body):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def valid_target(self):
        return self.path == "/" + TOKEN and self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

    def do_GET(self):
        if not self.valid_target():
            return self.reply(404, "Não encontrado.")
        self.reply(200, """<!doctype html><html lang=pt-BR><meta charset=utf-8>
<title>IALD · Configuração local da API</title><style>
body{background:#101620;color:#e8edf3;font:18px system-ui;max-width:720px;margin:8vh auto;padding:28px}input,button{font:inherit;padding:14px;border-radius:10px}input{width:95%;margin:18px 0}button{background:#86d6bf;color:#10251d;border:0}p{line-height:1.65}</style>
<h1>Conectar a API à IALD</h1><p>A chave será salva somente no <b>.env do servidor local</b>, com acesso restrito. Ela não aparece na conversa nem é incluída no aplicativo.</p>
<form method=post><input type=hidden name=csrf value="$CSRF$"><label for=key>Chave do projeto IALD</label><input id=key name=key type=password autocomplete=off required spellcheck=false>
<button type=submit>Salvar no servidor IALD</button></form><p>Esta etapa não altera o motor das contas nem reinicia a IALD nativa.</p></html>""".replace('$CSRF$', CSRF))

    def do_POST(self):
        global SAVED
        origin = f"http://127.0.0.1:{self.server.server_port}"
        # The embedded browser reports Origin:null even for a same-origin POST.
        # Accept that observed case only with browser Fetch Metadata AND the
        # independent form CSRF challenge below; cross-site requests stay refused.
        same_origin = self.headers.get("Origin") == origin or (
            self.headers.get("Origin") == "null" and self.headers.get("Sec-Fetch-Site") == "same-origin")
        if not self.valid_target() or not same_origin or SAVED:
            return self.reply(403, "Pedido recusado.")
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 1 <= length <= 4096:
                return self.reply(400, "Pedido inválido.")
            data = parse_qs(self.rfile.read(length).decode("utf-8"))
            if not hmac.compare_digest(data.get('csrf', [''])[0], CSRF):
                return self.reply(403, "Pedido recusado.")
            save_key(data.get("key", [""])[0].strip())
            SAVED = True
            self.reply(200, "<title>IALD · Chave salva</title><h1>Chave salva com acesso restrito.</h1><p>Pode voltar à conversa. Nenhuma credencial foi exibida ou enviada pela conversa.</p>")
            print("IALD_API_KEY_SAVED=true", flush=True)
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        except ValueError as error:
            self.reply(400, html.escape(str(error)))
        except Exception:
            self.reply(500, "Falha na gravação protegida. A chave não foi exibida; avise o operador.")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 0), Handler)
    print(f"SETUP_URL=http://127.0.0.1:{server.server_port}/{TOKEN}", flush=True)
    server.serve_forever()
