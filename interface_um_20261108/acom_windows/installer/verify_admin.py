"""Exercise the administrative-image action; it extracts an image without installing the product."""
from pathlib import Path
import os, subprocess, tempfile, sys, hashlib, json
def run(setup,report,keep_image=None):
    setup=setup.resolve();report=report.resolve()
    with tempfile.TemporaryDirectory(prefix='msi-admin-',dir=report.parent) as temp:
        root=Path(temp);msi=root/'ACOM.msi'
        image=keep_image.resolve() if keep_image else root/'extracted'
        if keep_image and image.parent!=report.parent:raise ValueError('A imagem persistente deve ficar ao lado do recibo.')
        image.mkdir()
        subprocess.run([str(setup),'--extract-msi',str(msi)],check=True,timeout=30)
        # Windows Installer parses the raw command line: a property with spaces requires
        # quotes around its value, while Python's default argv builder quotes the whole assignment.
        engine=str(Path(os.environ['SystemRoot'])/'System32/msiexec.exe')
        cmd=f'"{engine}" /a "{msi}" /qn /norestart TARGETDIR="{image}" /L*V "{root / "layout.log"}"'
        try: result=subprocess.run(cmd,timeout=50,check=False).returncode
        except subprocess.TimeoutExpired: result='timeout'
        try: log=(root/'layout.log').read_text(encoding='utf-16',errors='replace').splitlines()
        except FileNotFoundError:log=[]
        files=list(image.rglob('pythonw.exe')); testfile=list(image.rglob('host.py'))
        report.write_text(json.dumps({'msiexec_admin_result':result,'installer':hashlib.sha256(setup.read_bytes()).hexdigest(),
             'pythonw_files':len(files),'host_files':len(testfile),'affected_registration':False,'layout_only':True,
             'image':str(image) if keep_image else None,'pythonw':str(files[0]) if keep_image and files else None,
             'web_index':str(testfile[0].parent.parent/'web/index.html') if keep_image and testfile else None,
             'log_tail':log[-12:]},ensure_ascii=False,indent=2),encoding='utf8')
        print(result,len(files),len(testfile));return 0 if result==0 and len(files)==len(testfile)==1 else 1
if __name__=='__main__':sys.exit(run(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]) if len(sys.argv)==4 else None))

