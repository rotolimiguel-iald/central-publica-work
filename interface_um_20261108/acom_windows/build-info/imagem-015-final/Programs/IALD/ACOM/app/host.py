"""ACOM desktop host: local selectors, same-origin UI, no absolute paths from HTTP."""
from __future__ import annotations
import ctypes
import hmac
import http.server
from http.cookies import SimpleCookie, CookieError
import json
import locale
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import threading
import time
from urllib.parse import unquote, urlsplit
import webbrowser

VERSION = "1.0-test"
APP = Path(__file__).resolve().parent
ROOT = APP.parent
WEB = ROOT / "web"
COMMANDS = {"pack-files", "pack-folder", "extract"}
LANG = {
    "pt": ("Selecione os arquivos para compactar", "Selecione a pasta para compactar",
           "Salvar como um novo pacote .acom", "Abrir um pacote ACOM", "Escolha a pasta onde criar a restauração",
           "Pacote criado", "Arquivos restaurados", "Não foi possível concluir", "Arquivos ACOM", "Todos os arquivos",
           "A Bancada encerrou esta sessão local. Abra o ACOM pelo menu Iniciar para continuar."),
    "en": ("Choose files to compress", "Choose a folder to compress", "Save as a new .acom archive",
           "Open an ACOM archive", "Choose where to create the restoration folder",
           "Archive created", "Files restored", "Could not complete the operation", "ACOM archives", "All files",
           "This local session ended. Open ACOM from the Start menu to continue."),
    "ar": ("اختر الملفات المراد ضغطها", "اختر المجلد المراد ضغطه", "احفظ أرشيف ‎.acom جديدًا",
           "افتح أرشيف ACOM", "اختر مكان إنشاء مجلد الاستعادة", "تم إنشاء الأرشيف",
           "تمت استعادة الملفات", "تعذّر إكمال العملية", "أرشيفات ACOM", "كل الملفات",
           "انتهت الجلسة المحلية. افتح ACOM من قائمة ابدأ للمتابعة."),
}
def language(value=None):
    if value is None and os.name == "nt":
        buffer = ctypes.create_unicode_buffer(85)
        if ctypes.windll.kernel32.GetUserDefaultLocaleName(buffer, len(buffer)):
            value = buffer.value
    label = str(value or locale.getlocale()[0] or "pt").lower().replace("_","-").split("-")[0]
    return label if label in LANG else "pt"

def restore_target(parent, archive):
    label = archive.stem or "ACOM"
    result = parent / label
    n = 1
    while os.path.lexists(result):
        result = parent / (label + " (" + str(n) + ")")
        n += 1
    return result

def dialog_action(mode, lang, selected=None):
    from tkinter import Tk, filedialog
    import archive_safe
    t = LANG[language(lang)]
    window = Tk()
    window.withdraw()
    try:
        window.attributes("-topmost", True)
        opts = {"parent": window}
        if mode == "extract":
            filename = str(selected) if selected else filedialog.askopenfilename(
                **opts, title=t[3], filetypes=[(t[8], "*.acom"), (t[9], "*.*")])
            if not filename: return {"status":"cancelled"}
            archive = Path(filename)
            parent = filedialog.askdirectory(**opts, title=t[4], initialdir=str(archive.parent), mustexist=True)
            if not parent: return {"status":"cancelled"}
            output = restore_target(Path(parent), archive)
            result = archive_safe.extract_archive(archive, output)
        else:
            if selected: paths = [Path(selected)]
            elif mode == "pack-files":
                paths = [Path(p) for p in filedialog.askopenfilenames(**opts, title=t[0])]
            elif mode == "pack-folder":
                folder = filedialog.askdirectory(**opts, title=t[1], mustexist=True)
                paths = [Path(folder)] if folder else []
            else: raise ValueError("Unsupported action")
            if not paths: return {"status":"cancelled"}
            first = paths[0]
            filename = filedialog.asksaveasfilename(**opts, title=t[2], defaultextension=".acom",
                filetypes=[(t[8],"*.acom")], initialdir=str(first.parent),
                initialfile=(first.name or "ACOM") + ".acom")
            if not filename: return {"status":"cancelled"}
            output = Path(filename)
            result = archive_safe.pack_paths(paths, output)
        return {"status":"ok", **{k:result[k] for k in ("files","inputBytes","outputBytes")},
                "message": (t[6] if mode=="extract" else t[5]) + ": " + str(output)}
    finally: window.destroy()

def safe_dialog(mode, lang, selected=None):
    try: return dialog_action(mode,lang,selected)
    except Exception as exc: return {"status":"error","message":LANG[language(lang)][7] + ": " + str(exc)}

def popup(message, error=False):
    ctypes.windll.user32.MessageBoxW(None, str(message), "ACOM · IALD", (0x10 if error else 0x40)|0x10000)

def run_picker(action, lang):
    # Tk always runs on the main thread of a separate short-lived process.
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    python = Path(sys.executable).with_name("python.exe")
    proc = subprocess.run([str(python), "-B", "-X", "utf8", str(APP/"host.py"), "_dialog", action, lang],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=flags)
    if proc.returncode: raise RuntimeError("ACOM: selector indisponível.")
    return json.loads(proc.stdout.decode("utf-8"))

class Host(http.server.ThreadingHTTPServer):
    allow_reuse_address = False
    def __init__(self, web, picker=run_picker):
        self.web = Path(web).resolve(strict=True)
        self.token = secrets.token_urlsafe(32)
        self.ticket = secrets.token_urlsafe(32)
        self.ticket_lock = threading.Lock()
        self.cookie_name = "acom_" + secrets.token_hex(8)
        self.cookie_value = secrets.token_urlsafe(32)
        self.busy = threading.Lock()
        self.touched = time.monotonic()
        self.picker = picker
        super().__init__(("127.0.0.1", 0), Handler)
        self.authority = "127.0.0.1:" + str(self.server_port)
        self.origin = "http://" + self.authority

TYPES={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8",
       ".json":"application/json",".vtt":"text/vtt; charset=utf-8",".svg":"image/svg+xml",".png":"image/png",
       ".jpg":"image/jpeg",".webp":"image/webp",".mp4":"video/mp4",".woff2":"font/woff2",".ico":"image/x-icon",
       ".zip":"application/zip",".acom":"application/octet-stream",".webm":"video/webm"}
class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "ACOM"
    def log_message(self, *args): pass
    def end_headers(self):
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","DENY")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cross-Origin-Resource-Policy","same-origin")
        self.send_header("Content-Security-Policy","default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self' blob:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none'")
        super().end_headers()
    def respond(self, code, payload):
        data=json.dumps(payload,ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        if self.command!="HEAD": self.wfile.write(data)
    def authorized_origin(self):
        return self.headers.get("Host")==self.server.authority and self.headers.get("Origin",self.server.origin)==self.server.origin
    def has_session(self):
        try:
            cookies=SimpleCookie(self.headers.get("Cookie",""))
            value=cookies[self.server.cookie_name].value
            return hmac.compare_digest(value.encode(),self.server.cookie_value.encode())
        except (KeyError,CookieError): return False
    def do_HEAD(self): self.do_GET()
    def do_GET(self):
        if not self.authorized_origin(): return self.respond(403,{"status":"error"})
        name=unquote(urlsplit(self.path).path)
        if name.startswith("/launch/"):
            with self.server.ticket_lock:
                if self.command!="GET" or not self.server.ticket or not hmac.compare_digest(
                        name[8:].encode(),self.server.ticket.encode()):
                    return self.respond(403,{"status":"error"})
                self.server.ticket=None
            self.send_response(303)
            self.send_header("Set-Cookie", f"{self.server.cookie_name}={self.server.cookie_value}; Path=/acom-api/; HttpOnly; SameSite=Strict")
            self.send_header("Location","/?ferramenta=acom");self.send_header("Cache-Control","no-store")
            self.send_header("Content-Length","0");self.end_headers();return
        if name=="/acom-api/status":
            if not self.has_session() or self.headers.get("Sec-Fetch-Site","same-origin") not in {"same-origin","none"}:
                return self.respond(403,{"status":"error"})
            self.server.touched=time.monotonic()
            return self.respond(200,{"native":True,"token":self.server.token,"version":VERSION})
        if name=="/": name="/index.html"
        downloadable = name in {"/downloads/ACOM-fonte.zip", "/downloads/Primeira-luz.acom"}
        allowed=name=="/index.html" or name.startswith("/src/") or downloadable
        if not allowed or any(c in name for c in ("\\","\0",":")) or ".." in name.split("/"):
            return self.respond(404,{"status":"error"})
        file=(self.server.web/name.lstrip("/")).resolve()
        if downloadable and not file.is_file():
            fallback=self.server.web.parent/"downloads"/Path(name).name
            if fallback.is_file(): file=fallback.resolve()
        else:
            if not file.is_relative_to(self.server.web): return self.respond(404,{"status":"error"})
        if not file.is_file() or file.suffix.lower() not in TYPES: return self.respond(404,{"status":"error"})
        self.server.touched=time.monotonic()
        with file.open("rb") as src:
            size=os.fstat(src.fileno()).st_size
            start,end=0,size-1
            partial=self.headers.get("Range")
            if partial:
                m=re.fullmatch(r"bytes=([0-9]{1,18})-([0-9]{0,18})",partial)
                if not m or int(m[1])>=size or (m[2] and int(m[2])<int(m[1])):
                    self.send_response(416);self.send_header("Content-Range",f"bytes */{size}");self.end_headers();return
                start=int(m[1]);end=min(end,int(m[2])) if m[2] else end
            self.send_response(206 if partial else 200)
            self.send_header("Content-Type",TYPES[file.suffix.lower()]); self.send_header("Accept-Ranges","bytes")
            if partial: self.send_header("Content-Range",f"bytes {start}-{end}/{size}")
            if downloadable: self.send_header("Content-Disposition",'attachment; filename="'+Path(name).name+'"')
            self.send_header("Content-Length",str(end-start+1)); self.end_headers()
            if self.command=="HEAD": return
            src.seek(start)
            left=end-start+1
            try:
                while left:
                    chunk=src.read(min(left,128*1024))
                    if not chunk: break
                    self.wfile.write(chunk);left-=len(chunk)
            except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError): pass
    def do_POST(self):
        if self.path!="/acom-api/action": return self.respond(404,{"status":"error"})
        if not self.has_session() or not self.authorized_origin() or self.headers.get("Origin")!=self.server.origin or not hmac.compare_digest(
                self.headers.get("X-ACOM-Token","").encode(),self.server.token.encode()):
            return self.respond(403,{"status":"error"})
        try:
            n=int(self.headers.get("Content-Length","0"))
            if self.headers.get_content_type()!="application/json" or not 1<=n<=256: raise ValueError()
            data=json.loads(self.rfile.read(n))
            if type(data)!=dict or set(data)-{"action","lang"} or data.get("action") not in COMMANDS: raise ValueError()
            lang=language(data.get("lang") or "pt")
        except (ValueError,TypeError): return self.respond(400,{"status":"error"})
        if not self.server.busy.acquire(False): return self.respond(409,{"status":"error","message":{"pt":"Já existe uma operação aberta.","en":"Another operation is open.","ar":"توجد عملية أخرى مفتوحة."}[lang]})
        try:
            self.server.touched=time.monotonic()
            result=self.server.picker(data["action"],lang)
            if not isinstance(result,dict) or result.get("status") not in {"ok","cancelled","error"}:raise ValueError()
        except Exception: result={"status":"error","message":LANG[lang][7]}
        finally: self.server.touched=time.monotonic();self.server.busy.release()
        self.respond(200,result)

def serve():
    with Host(WEB) as server:
        # No persistent service: the session expires after inactivity. No firewall rule or fixed port.
        server.timeout=1
        url=server.origin+"/launch/"+server.ticket
        if not webbrowser.open(url): popup(url)
        while server.busy.locked() or time.monotonic()-server.touched<1800: server.handle_request()

def main(argv):
    if not argv or argv==["home"] or argv==["protocol","iald-acom:home"]:
        serve();return 0
    if len(argv)==3 and argv[0]=="_dialog" and argv[1] in COMMANDS:
        sys.stdout.buffer.write(json.dumps(safe_dialog(argv[1],argv[2]),ensure_ascii=False).encode("utf-8"));return 0
    if len(argv)==2 and argv[0] in {"pack","extract"}:
        path=Path(argv[1])
        if not path.is_absolute() or not path.exists(): raise ValueError("ACOM: caminho indisponível.")
        mode="extract" if argv[0]=="extract" else ("pack-folder" if path.is_dir() else "pack-files")
        result=safe_dialog(mode,language(),path)
        if result["status"]!="cancelled": popup(result["message"], result["status"]=="error")
        return 1 if result["status"]=="error" else 0
    raise ValueError("ACOM: comando não reconhecido.")
if __name__=="__main__":
    try: sys.exit(main(sys.argv[1:]))
    except Exception as exc: popup(exc,True);sys.exit(2)

