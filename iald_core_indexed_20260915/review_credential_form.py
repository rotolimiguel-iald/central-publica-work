"""Single-use local masked password field for the approved Apple transfer."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import html
import json
from pathlib import Path
import secrets
import threading

credential = json.loads(Path(r'C:\Users\rotol\.iald_keys\apple-beta\review-account.json').read_bytes())
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
        page = ('<!doctype html><meta charset="utf-8"><title>Revisão Apple — transferência protegida</title>'
                '<h1>Conta iald_review_beta</h1><p>Somente para App Store Connect. A senha permanece mascarada.</p>'
                '<label for="review-password">Senha exclusiva de revisão</label>'
                '<input id="review-password" type="password" readonly autocomplete="off" value="'
                +html.escape(credential['password'],quote=True)+'">').encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'none'; frame-ancestors 'none'")
        self.send_header('Content-Length',str(len(page)))
        self.end_headers()
        self.wfile.write(page)

server = HTTPServer(('127.0.0.1',0),Handler)
threading.Timer(900,server.shutdown).start()
print('LOCAL_MASKED_FORM=http://127.0.0.1:'+str(server.server_port)+'/'+token,flush=True)
server.serve_forever()
