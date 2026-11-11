"""Verify the finished tester without registering a product under the operator's account."""
from pathlib import Path
import argparse, ctypes, hashlib, json, os, subprocess, sys, tempfile
from msi_db import H,W,P,api,call,handle,ident

for n,args in {
    'MsiViewFetch':[H,ctypes.POINTER(H)],
    'MsiRecordGetStringW':[H,H,ctypes.c_wchar_p,ctypes.POINTER(H)],
    'MsiRecordReadStream':[H,H,ctypes.c_void_p,ctypes.POINTER(H)]
}.items():
    getattr(api,n).argtypes=args;getattr(api,n).restype=H

def query(db,sql,col_count):
    import re
    match=re.fullmatch(r'SELECT (\w+(?:,\w+)*) FROM (\w+)',sql)
    if match:sql='SELECT '+','.join(chr(96)+v+chr(96) for v in match[1].split(','))+' FROM '+chr(96)+match[2]+chr(96)
    with handle() as view:
        call(api.MsiDatabaseOpenViewW(db,sql,P(view)),sql);call(api.MsiViewExecute(view,0),'execute')
        rows=[]
        while True:
            with handle() as row:
                result=api.MsiViewFetch(view,P(row))
                if result==259:break
                call(result,'fetch')
                values=[]
                for i in range(1,col_count+1):
                    size=H(4096);buf=ctypes.create_unicode_buffer(size.value)
                    call(api.MsiRecordGetStringW(row,i,buf,P(size)),'read table')
                    values.append(buf.value)
                rows.append(values)
        return rows

def cabinet(db,dst):
    with handle() as view, handle() as row:
        call(api.MsiDatabaseOpenViewW(db,"SELECT \x60Data\x60 FROM \x60_Streams\x60 WHERE \x60Name\x60='payload.cab'",P(view)),'cab')
        call(api.MsiViewExecute(view,0),'query cab');call(api.MsiViewFetch(view,P(row)),'fetch cab')
        with dst.open('xb') as f:
            while True:
                size=H(256*1024);buf=ctypes.create_string_buffer(size.value)
                call(api.MsiRecordReadStream(row,1,buf,P(size)),'read cabinet')
                if not size.value:break
                f.write(buf.raw[:size.value])

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def verify(setup,built,out):
    with tempfile.TemporaryDirectory(prefix='verify-acom-',dir=out.parent) as tmp:
        d=Path(tmp);msi=d/'ACOM.msi';cab=d/'payload.cab';flat=d/'flat';flat.mkdir();product=d/'product';product.mkdir()
        subprocess.run([str(setup),'--extract-msi',str(msi)],check=True,timeout=30)
        receipt=json.loads(built.read_text(encoding='utf8'))
        assert digest(msi)==receipt['msiSHA256'] and digest(setup)==receipt['setupSHA256']
        with handle() as db:
            call(api.MsiOpenDatabaseW(str(msi),0,P(db)),'open MSI')
            properties=dict(query(db,'SELECT Property,Value FROM Property',2))
            assert 'ALLUSERS' not in properties
            dir_rows={i:(parent,long.split('|')[-1]) for i,parent,long in query(db,'SELECT Directory,Directory_Parent,DefaultDir FROM Directory',3)}
            def rel(d):
                if d=='APPDIR':return ''
                parent,name=dir_rows[d];return (Path(rel(parent))/name).as_posix()
            components=dict(query(db,'SELECT Component,Directory_ FROM Component',2))
            files={i:(Path(rel(components[c]))/name.split('|')[-1]).as_posix() for i,c,name in query(db,'SELECT File,Component_,FileName FROM File',3)}
            registry=query(db,'SELECT Root,Key,Name,Value,Component_ FROM Registry',5)
            assert all(row[0]=='1' and 'userchoice' not in row[1].lower() for row in registry)
            assert not any(row[1].lower()=='software\\classes\\.acom' and not row[2] for row in registry)
            assert any(row[1].endswith('OpenWithProgids') and row[-1]=='RegExplorer' for row in registry)
            assert any('protocol "%1"' in row[3] for row in registry)
            assert sum('pack "%1"' in row[3] for row in registry)==2
            assert sum('extract "%1"' in row[3] for row in registry)==2
            assert dict(query(db,'SELECT Feature,Level FROM Feature',2))=={'Core':'1','Explorer':'2'}
            assert query(db,'SELECT Shortcut,Target,Arguments FROM Shortcut',3)[0][2].endswith(' home')
            cabinet(db,cab)
        r=subprocess.run([str(Path(os.environ['WINDIR'])/'System32/expand.exe'),str(cab),'-F:*',str(flat)],capture_output=True)
        if r.returncode:raise ValueError(r.stdout[-500:])
        manifest={row['name']:row['sha256'] for row in receipt['manifest']}
        assert set(manifest)==set(files.values())
        for fid,name in files.items():
            src=flat/fid
            if digest(src)!=manifest[name]:raise ValueError('Payload mismatch '+name)
            dst=product/name;dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
        assert not list(flat.iterdir())
        code=('import pathlib,sys,tkinter,ctypes,ssl,hashlib,archive_safe,host,json;'
              't=tkinter.Tcl();meta={"prefix":sys.base_prefix,"library":t.eval("info library"),"iso":sys.flags.isolated,'
              '"imports":True,"host":host.VERSION,"package_local":False};'
              'meta["package_local"]=all(str(pathlib.Path(sys.executable).parent.parent.resolve()).lower() in str(pathlib.Path(i).resolve()).lower() for i in sys.path);'
              'assert pathlib.Path(meta["library"]).resolve().is_relative_to(pathlib.Path(sys.executable).parent);'
              'assert meta["iso"] and meta["package_local"]; print(json.dumps(meta))')
        proc=subprocess.run([str(product/'runtime/python.exe'),'-B','-c',code],capture_output=True,timeout=30)
        if proc.returncode:raise ValueError(proc.stderr.decode(errors='replace'))
        rt=json.loads(proc.stdout);rt.pop('prefix');rt.pop('library')
        report={'setup_sha256':digest(setup),'msi_sha256':digest(msi),'verified_payload_files':len(files),
                'feature_level':{'Core':1,'Explorer':2},'hkcu_values':len(registry),'shortcut':True,
                'portable_runtime':rt,'live_account_install':False,'mode':'MSI database, embedded CAB, exact extraction and isolated runtime'}
        out.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))
if __name__=='__main__':
    q=argparse.ArgumentParser();q.add_argument('setup',type=Path);q.add_argument('build',type=Path);q.add_argument('out',type=Path)
    a=q.parse_args();verify(a.setup.resolve(),a.build.resolve(),a.out.resolve())

