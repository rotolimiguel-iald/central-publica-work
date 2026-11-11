"""Build the ACOM per-user Windows test installer using CPython x64 and Windows SDK tools."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'installer'))
from msi_db import write_msi, ident

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def archive(out, sources):
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for rel,path in sorted(sources.items()):
            info=zipfile.ZipInfo(rel,(2026,1,1,0,0,0));info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,path.read_bytes())

def main():
    q=argparse.ArgumentParser(description=__doc__)
    q.add_argument('--python-root',type=Path,default=Path(sys.base_prefix))
    q.add_argument('--ui',type=Path,required=True,help='Bancada com index.html, src e mídias')
    q.add_argument('--codec',type=Path,default=HERE/'app',help='acom_archive.py, acom_auto.py, acom_codec.py')
    q.add_argument('--out',type=Path,required=True);q.add_argument('--development',action='store_true',help='Permitir prévia da Bancada anterior à integração do ACOM')
    args=q.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    rt=args.python_root.resolve();ui=args.ui.resolve()
    if sys.version_info[:2]!=(3,14) or sys.maxsize<=2**32:raise RuntimeError('Build requer CPython 3.14 x64')
    system=Path(os.environ['SystemRoot'])
    csc=system/'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
    work=Path(tempfile.mkdtemp(prefix='build-',dir=HERE if (HERE/'installer').is_dir() else None))
    files={};source={}
    def add(target,name,path):
        if not path.is_file() or path.is_symlink():raise FileNotFoundError(path)
        if name in target:raise ValueError('Duplicate '+name)
        target[name]=path
    def first(*choices):return next((p for p in choices if p.is_file()),choices[0])
    try:
        for name in ('host.py','archive_safe.py','acom_archive.py','acom_auto.py','acom_codec.py'):
            add(files,'app/'+name,first(HERE/'app'/name,args.codec/name))
        for name in ('README.md','LICENSE-IALD.txt'):
            add(files,name,HERE/name)
        for name in ('runtime-notices.txt',):
            add(files,'notices/'+name,HERE/'installer'/name)
        add(files,'notices/Python-LICENSE.txt',rt/'LICENSE.txt')
        add(files,'notices/Tcl-Tk-license.terms',rt/'tcl/tk8.6/license.terms')
        for name in ('python.exe','pythonw.exe','python314.dll','python3.dll','vcruntime140.dll','vcruntime140_1.dll'):
            add(files,'runtime/'+name,rt/name)
        deps=('select.pyd','_socket.pyd','_tkinter.pyd','_bz2.pyd','_lzma.pyd','_ctypes.pyd','_queue.pyd',
              'unicodedata.pyd','_hashlib.pyd','_ssl.pyd','_wmi.pyd','_uuid.pyd','_zstd.pyd','_decimal.pyd',
              'libffi-8.dll','tcl86t.dll','tk86t.dll','libssl-3.dll','libcrypto-3.dll','zlib1.dll')
        for name in deps:add(files,'runtime/'+name,rt/'DLLs'/name)
        pth=work/'python314._pth';pth.write_bytes(b'python314.zip\r\n.\r\n../app\r\n')
        add(files,'runtime/python314._pth',pth)
        lib=rt/'Lib';stdlib={}
        for p in lib.glob('*.py'):
            if p.stem in sys.stdlib_module_names:add(stdlib,p.name,p)
        for p in lib.iterdir():
            if not p.is_dir() or p.name not in sys.stdlib_module_names or p.name in {'idlelib','ensurepip','turtledemo','venv','test'}:continue
            for mod in p.rglob('*.py'):
                if {'tests','test','__pycache__'}.intersection(mod.relative_to(p).parts):continue
                add(stdlib,mod.relative_to(lib).as_posix(),mod)
        libzip=work/'python314.zip';archive(libzip,stdlib);add(files,'runtime/python314.zip',libzip)
        for family in ('tcl8.6','tk8.6','tcl8'):
            for p in (rt/'tcl'/family).rglob('*'):
                if not p.is_file() or 'demos' in p.relative_to(rt/'tcl').parts:continue
                # All Tcl/Tk resources here originate from the CPython runtime distribution.
                add(files,'runtime/tcl/'+p.relative_to(rt/'tcl').as_posix(),p)
        add(files,'web/index.html',ui/'index.html')
        text_names={'main.js','styles.css','scene.js','data.js','i18n.js','content-i18n.js','favicon.svg'}
        media_names={'angulo-de-miguel.jpg','breu-ilhado.jpg','breu-um-traco-global.mp4','filme1_720p_pt-BR.mp4',
                     'filme1_poster.jpg','inscricao-066.png','inscricao-136.png','inscricao-226.png','universo-visto-de-fora.jpg'}
        for p in (ui/'src').iterdir():
            if re.fullmatch(r'acom(?:[-.][a-z0-9]+)*\.(?:css|js|svg)',p.name):text_names.add(p.name)
        for name in sorted(text_names|media_names):add(files,'web/src/'+name,ui/'src'/name)
        for lang in ('ar','en','pt-BR'):
            for prefix in ('breu','inscricao'):
                name=f'{prefix}.{lang}.vtt';add(files,'web/src/legendas/'+name,ui/'src/legendas'/name)
        if not args.development and not any('/acom-api/status' in p.read_text(encoding='utf8') for n,p in files.items() if n.endswith('.js')):
            raise RuntimeError('Aguardando a UI com o contrato nativo ACOM')
        for k,p in files.items():
            if k.startswith(('runtime/','web/')):continue
            source[k]=p
        for n in ('Setup.cs','msi_db.py','runtime-notices.txt','verify_package.py','verify_admin.py'):source['installer/'+n]=HERE/'installer'/n
        source['build_release.py']=Path(__file__)
        source['sample.py']=HERE/'sample.py'
        source['COMO-MONTAR.txt']=HERE/'installer'/'COMO-MONTAR.txt'
        source['installer/COMO-MONTAR.txt']=HERE/'installer'/'COMO-MONTAR.txt'
        # Ship a readable copy of the interface. Cinematic media remains part of the Bancada.
        for n,p in files.items():
            if n.startswith('web/') and p.suffix in {'.js','.css','.html','.svg','.vtt'}:source[n]=p
        sz=work/'ACOM-fonte.zip';archive(sz,source);add(files,'web/downloads/ACOM-fonte.zip',sz)
        sample=out/'Primeira-luz.acom'
        if sample.is_file():add(files,'web/downloads/Primeira-luz.acom',sample)
        data=sorted(files.items())
        ddf=work/'payload.ddf'
        # Build in an ASCII TEMP working directory if makecab cannot round-trip the source code page.
        ddf.write_bytes(('\r\n'.join(['.OPTION EXPLICIT','.Set Cabinet=on','.Set Compress=on','.Set CompressionType=MSZIP',
                          '.Set MaxDiskSize=0','.Set MaxCabinetSize=0','.Set MaxDiskFileCount=0',
                          '.Set CabinetNameTemplate=payload.cab','.Set DiskDirectoryTemplate=.',
                          '.Set RptFileName=payload.rpt','.Set InfFileName=payload.inf']+
                          [f'"{p}" {ident("F",rel)}' for rel,p in data])+'\r\n').encode('mbcs'))
        with (work/'makecab.log').open('wb') as log:
            r=subprocess.run([str(system/'System32/makecab.exe'),'/V0','/F',str(ddf)],cwd=work,stdout=log,stderr=log)
        if r.returncode:raise RuntimeError((work/'makecab.log').read_text(encoding='mbcs',errors='replace')[-1600:])
        manifest=[{'name':k,'size':v.stat().st_size,'sha256':sha(v)} for k,v in data]
        encoded=json.dumps(manifest,sort_keys=True).encode('ascii')
        digest=hashlib.sha256(encoded).hexdigest()
        cab=work/'payload.cab';msi=work/'ACOM.msi';code=write_msi(msi,work,data,cab,digest,'1.0.0')
        setup=work/'ACOM-Setup.exe'
        cmd=[str(csc),'/nologo','/optimize+','/target:winexe','/platform:x64','/utf8output',
             '/reference:System.Windows.Forms.dll','/reference:System.Drawing.dll','/out:'+str(setup),
             '/resource:'+str(msi)+',msi','/resource:'+str(HERE/'LICENSE-IALD.txt')+',license',str(HERE/'installer/Setup.cs')]
        subprocess.run(cmd,check=True)
        for src in (sz,setup):
            temp=out/(src.name+'.tmp');shutil.copyfile(src,temp);os.replace(temp,out/src.name)
        report={'version':'1.0.0','productCode':code,'files':len(files),'payloadBytes':sum(row['size'] for row in manifest),
                'msiSHA256':sha(msi),'setupSHA256':sha(setup),'sourceSHA256':sha(sz),'ui':str(ui),
                'runtime':sys.version.split()[0],'development':args.development,'manifest':manifest}
        receipts=HERE/'build-info';receipts.mkdir(exist_ok=True)
        (receipts/'last-build.json').write_text(json.dumps(report,indent=1),encoding='utf8')
        print(json.dumps({k:v for k,v in report.items() if k!='manifest'},ensure_ascii=False))
    finally:
        # Only this invocation's new temporary folder is removed.
        if work.parent.resolve()==HERE and work.name.startswith('build-'):shutil.rmtree(work)

if __name__=='__main__':main()

