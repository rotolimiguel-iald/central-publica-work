#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
serve_dashboard.py — servidor local do painel SkyGrid (stdlib, zero deps).

Uso:  python serve_dashboard.py [porta]        (padrao 8137)
Abre: http://localhost:8137/

Serve a pasta dashboard/ (index.html + data/*.json). Os dados sao gerados por
`python skygrid_app.py run ...`; o painel auto-atualiza a cada 3 s.
Nao ha veredito fisico em nenhum dado servido (physical_verdict_allowed=False).
"""

import os
import sys
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dashboard")


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):   # quieter console
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8137
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    httpd = ThreadingHTTPServer(("127.0.0.1", port),
                                partial(Handler, directory=ROOT))
    url = "http://localhost:%d/" % port
    print("SkyGrid dashboard: %s   (Ctrl+C para sair)" % url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nencerrado.")


if __name__ == "__main__":
    main()
