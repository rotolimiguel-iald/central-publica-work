"""One-use local clipboard page; no credential in logs or tool output."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import threading

PATH = Path(r'C:\Users\rotol\.iald_keys\apple-beta\review-account.json')
credential = json.loads(PATH.read_bytes())
token = secrets.token_urlsafe(32)
used = False


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):
        pass

    def do_GET(self):
        global used
        if self.path != '/'+token or used:
            self.send_error(404)
            return
        used = True
        password = json.dumps(credential['password'])
        html = ('<!doctype html><meta charset="utf-8"><title>Credencial de revisão Apple</title>'
                '<h1>Credencial exclusiva de revisão</h1><p>Conta: iald_review_beta</p>'
                '<button id="copy">Copiar senha para a Apple</button><p id="state"></p>'
                '<script>document.getElementById("copy").onclick=async()=>{'
                'await navigator.clipboard.writeText('+password+');'
                'document.getElementById("state").textContent="Copiada. Use somente no App Store Connect.";'
                '};</script>').encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; frame-ancestors 'none'")
        self.send_header('Content-Length',str(len(html)))
        self.end_headers()
        self.wfile.write(html)


server = HTTPServer(('127.0.0.1',0),Handler)
threading.Timer(900,server.shutdown).start()
print('LOCAL_REVIEW_CLIPBOARD_URL=http://127.0.0.1:'+str(server.server_port)+'/'+token,flush=True)
server.serve_forever()
