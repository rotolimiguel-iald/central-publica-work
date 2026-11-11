"""File round trip through the HTTP handler and UI action dispatcher; only native chooser input is substituted."""
from pathlib import Path
import argparse, hashlib, http.client, json, os, sys, tempfile, threading
from contextlib import contextmanager
from importlib import import_module
@contextmanager
def patch(name, replacement=None, **opts):
    module_name, attr=name.rsplit(".",1)
    module=import_module(module_name)
    original=getattr(module,attr)
    value=replacement if replacement is not None else lambda *args,**kwargs: opts["return_value"]
    setattr(module,attr,value)
    try: yield
    finally: setattr(module,attr,original)
parser=argparse.ArgumentParser()
parser.add_argument("--app",type=Path,required=True);parser.add_argument("--codec",type=Path,required=True)
parser.add_argument("--web",type=Path,required=True);parser.add_argument("--out",type=Path,required=True)
args=parser.parse_args()
sys.path[:0]=[str(args.app.resolve()),str(args.codec.resolve())]
import host
class Window:
    def withdraw(self): pass
    def attributes(self,*args): pass
    def destroy(self):pass
with tempfile.TemporaryDirectory() as temp:
    work=Path(temp)
    fixture=work/"prueba ü.txt";fixture.write_bytes(("O Um retorna a 1.\r\n"*63).encode())
    archive=work/"arquivos α.acom";dest=work/"restauração";dest.mkdir()
    server=host.Host(args.web,host.safe_dialog)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    def call(method,path,payload=None,headers=None):
        conn=http.client.HTTPConnection("127.0.0.1",server.server_port,timeout=120)
        conn.request(method,path,json.dumps(payload).encode() if payload else None,headers or {})
        r=conn.getresponse()
        b=r.read();status=r.status;conn.close()
        return status,json.loads(b)
    try:
        assert call("GET","/acom-api/status")[0]==403
        conn=http.client.HTTPConnection("127.0.0.1",server.server_port,timeout=10)
        conn.request("GET","/launch/"+server.ticket)
        launch=conn.getresponse()
        assert launch.status==303
        cookie=launch.getheader("Set-Cookie").split(";",1)[0]
        launch.read();conn.close()
        s,body=call("GET","/acom-api/status",headers={"Cookie":cookie}); assert s==200 and body["native"]
        headers={"Content-Type":"application/json","Origin":server.origin,"Cookie":cookie,"X-ACOM-Token":body["token"]}
        def action(name):
            status, result=call("POST","/acom-api/action",{"action":name,"lang":"pt"},headers)
            assert status==200,result
            return result
        with patch("tkinter.Tk",Window), patch("tkinter.filedialog.askopenfilenames",return_value=[str(fixture)]),patch("tkinter.filedialog.asksaveasfilename",return_value=str(archive)):
            pack=action("pack-files")
        assert pack["status"]=="ok" and archive.exists(),pack
        with patch("tkinter.Tk",Window),patch("tkinter.filedialog.askopenfilename",return_value=str(archive)),patch("tkinter.filedialog.askdirectory",return_value=str(dest)):
            extract=action("extract")
        restored=list(dest.rglob(fixture.name))
        assert extract["status"]=="ok" and len(restored)==1 and fixture.read_bytes()==restored[0].read_bytes(),extract
        with patch("tkinter.Tk",Window),patch("tkinter.filedialog.askopenfilename",return_value=""):
            cancel=action("extract")
        assert cancel=={"status":"cancelled"}, cancel
        assert call("POST","/acom-api/action",{"action":"extract","path":str(fixture)},headers)[0]==400
        assert call("POST","/acom-api/action",{"action":"extract"},dict(headers,Origin="https://unrelated.invalid"))[0]==403
        data=dict(api="HTTP loopback real",picker="seletores substituídos; mesmos arquivos e motor locais",input=fixture.stat().st_size,
            archive=archive.stat().st_size,restored=restored[0].stat().st_size,sha256=hashlib.sha256(restored[0].read_bytes()).hexdigest(),
            cancelled=True,arbitrary_path_refused=True,cross_origin_refused=True)
        args.out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps(data,ensure_ascii=False))
    finally:server.shutdown();server.server_close();thread.join()

