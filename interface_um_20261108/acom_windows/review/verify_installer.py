"""Read-only, native MSI audit of the EXE. No installation, HKCU changes or subscriptions."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument("downloads",type=Path)
ap.add_argument("--receipt",type=Path,default=HERE.parent/"build-info"/"last-build.json")
ap.add_argument("--trial",action="store_true")
opt=ap.parse_args()
setup=opt.downloads/"ACOM-Setup.exe"; sources=opt.downloads/"ACOM-fonte.zip"
pinned=json.loads(opt.receipt.read_text(encoding="utf8"))
W=ctypes.c_wchar_p; I=ctypes.c_uint32; PI=ctypes.POINTER(I); B=ctypes.byref
api=ctypes.WinDLL("msi")
def bind(name,types):
    f=getattr(api,name);f.argtypes=types;f.restype=I;return f
open_db=bind("MsiOpenDatabaseW",[W,ctypes.c_void_p,PI])
close=bind("MsiCloseHandle",[I])
view=bind("MsiDatabaseOpenViewW",[I,W,PI])
execute=bind("MsiViewExecute",[I,I])
fetch=bind("MsiViewFetch",[I,PI])
field=bind("MsiRecordGetStringW",[I,I,W,PI])
read_stream=bind("MsiRecordReadStream",[I,I,ctypes.c_void_p,PI])
def ok(code): assert code==0,code
def rows(db,query,n):
    v=I();ok(view(db,query,B(v)));items=[]
    try:
        ok(execute(v,0))
        while True:
            r=I();rc=fetch(v,B(r))
            if rc==259:break
            ok(rc)
            try:
                a=[]
                for i in range(1,n+1):
                    buff=ctypes.create_unicode_buffer(8192);size=I(8191);ok(field(r,i,buff,B(size)));a.append(buff.value)
                items.append(a)
            finally:ok(close(r))
        return items
    finally:ok(close(v))
def stream_to_disk(db,target):
    v=I();query="SELECT \x60Data\x60 FROM \x60_Streams\x60 WHERE \x60Name\x60='payload.cab'"
    ok(view(db,query,B(v)))
    try:
        ok(execute(v,0));record=I();ok(fetch(v,B(record)))
        try:
            with target.open('xb') as f:
                while True:
                    buff=ctypes.create_string_buffer(65536);size=I(len(buff));ok(read_stream(record,1,buff,B(size)))
                    if size.value==0:break
                    f.write(buff.raw[:size.value])
        finally:ok(close(record))
    finally:ok(close(v))
def sha(p):
    with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
checks={}
def ck(k,v):checks[k]=bool(v)
with tempfile.TemporaryDirectory(prefix="review-msi-",dir=HERE) as temp:
    staging=Path(temp)
    msi=staging/"product.msi"
    p=subprocess.run([str(setup.resolve()),"--extract-msi",str(msi)],capture_output=True,timeout=45)
    assert p.returncode==0,p.returncode
    ck("exe_contains_actual_msi",msi.read_bytes()[:8]==b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" and sha(msi)==pinned["msiSHA256"])
    ck("source_and_setup_bytes_match_release",sha(setup)==pinned["setupSHA256"] and sha(sources)==pinned["sourceSHA256"])
    db=I();ok(open_db(str(msi),None,B(db)))
    try:
        props=dict(rows(db,"SELECT * FROM Property",2))
        ck("per_user_package",props.get("ALLUSERS","")=="" and props["Manufacturer"]=="IALD Ltda.")
        features=dict(rows(db,"SELECT Feature, Level FROM Feature",2))
        ck("explorer_is_optional",features["Core"]=="1" and features["Explorer"]=="2" and props["INSTALLLEVEL"]=="1")
        actions=[r[0] for r in rows(db,"SELECT Action FROM InstallExecuteSequence",1)]
        tables={r[0] for r in rows(db,"SELECT Name FROM _Tables",1)}
        ck("no_custom_actions", "CustomAction" not in tables and "SelfReg" not in tables)
        reg=rows(db,"SELECT Registry, Root, \x60Key\x60, Name, Value FROM Registry",5)
        ck("registry_only_hkcu",all(r[1]=="1" for r in reg))
        ck("default_association_preserved",all("userchoice" not in r[2].lower() and not (r[2].lower()=="software\\classes\\.acom" and not r[3]) for r in reg))
        cmds=[r for r in reg if r[2].endswith("\\command")]
        ck("all_commands_bind_exe_inside_msi",all(r[4].startswith('"[#F') and '"[APPDIR]app\\host.py" ' in r[4] and r[4].endswith(' "%1"') for r in cmds) and len(cmds)>=5)
        ck("uninstall_removes_registered_entries",set(["RemoveRegistryValues","RemoveShortcuts","RemoveFiles","PublishProduct"]).issubset(actions))
        removes=rows(db,"SELECT FileName, DirProperty, InstallMode FROM RemoveFile",3)
        ck("no_wildcard_removal",all(name=='' and dir_=="APPDIR" and mode=="2" for name,dir_,mode in removes))
        shortcut=rows(db,"SELECT Directory_, Target, Arguments FROM Shortcut",3)
        ck("start_menu_launches_packaged_host",len(shortcut)==1 and shortcut[0][0]=="ProgramMenuFolder" and shortcut[0][1].startswith("[#F") and shortcut[0][2].endswith('app\\host.py" home'))
        dirs={id_:(parent,name.split('|')[-1]) for id_,parent,name in rows(db,"SELECT Directory, Directory_Parent, DefaultDir FROM Directory",3)}
        ck("destination_current_account",dirs.get("APPDIR")==("IALDRoot","ACOM") and dirs.get("IALDRoot")==("ProgramsUnderLocal","IALD") and dirs.get("ProgramsUnderLocal")==("LocalAppDataFolder","Programs"))
        components=dict(rows(db,"SELECT Component, Directory_ FROM Component",2))
        media=rows(db,"SELECT Cabinet FROM Media",1)
        ck("offline_cabinet",media==[["#payload.cab"]])
        listed=rows(db,"SELECT File, Component_, FileName, FileSize FROM File",4)
        def rel(cid):
            names=[];d=components[cid]
            while d!="APPDIR":
                parent,name=dirs[d]
                assert parent and name not in (".","..") and "/" not in name and "\\" not in name
                names.append(name);d=parent
            return "/".join(reversed(names))
        cab=staging/"embedded.cab";stream_to_disk(db,cab)
        cache=staging/"cabinet";cache.mkdir()
        expand=Path(os.environ["SystemRoot"])/"System32"/"expand.exe"
        expanded=subprocess.run([str(expand),str(cab),"-F:*",str(cache)],capture_output=True,timeout=80)
        if expanded.returncode:raise RuntimeError(f"cab extraction {expanded.returncode}")
        actual={}
        for f,cid,name,size in listed:
            pkg=(rel(cid)+"/"+name.split("|")[-1]).lstrip("/")
            assert pkg not in actual
            path=cache/f
            assert path.stat().st_size==int(size)
            actual[pkg]=sha(path)
        ck("all_extracted_bytes_equal_release_manifest",actual=={item["name"]:item["sha256"] for item in pinned["manifest"]})
        ck("no_unlisted_cabinet_members",len(list(cache.iterdir()))==len(actual))
    finally:ok(close(db))
    ck("packaged_runtime_and_notices",set(["runtime/python314.dll","runtime/python.exe","runtime/pythonw.exe","runtime/python314.zip",
                                         "runtime/python314._pth","notices/Python-LICENSE.txt","notices/Tcl-Tk-license.terms"]).issubset(actual))
    ck("inspected_security_files_are_installed",actual["app/host.py"]==sha(HERE.parent/"app"/"host.py") and actual["app/archive_safe.py"]==sha(HERE.parent/"app"/"archive_safe.py"))
    ck("source_present_in_installed_files",actual["web/downloads/ACOM-fonte.zip"]==sha(sources))
    with zipfile.ZipFile(sources) as z:
        files=set(z.namelist())
        ck("source_code_present",{"app/acom_archive.py","app/acom_auto.py","app/acom_codec.py","app/archive_safe.py","app/host.py",
            "LICENSE-IALD.txt","build_release.py","installer/Setup.cs","web/index.html"}.issubset(files))
        ck("sources_match_install",all(hashlib.sha256(z.read(k)).hexdigest()==actual[k] for k in files & actual.keys()))
        if not opt.trial:
            ck("native_ui_contract_is_in_package",any(b"/acom-api/status" in z.read(k) and b"/acom-api/action" in z.read(k) for k in files if k.endswith(".js")))
            ck("test_sample_in_product",actual.get("web/downloads/Primeira-luz.acom")==sha(opt.downloads/"Primeira-luz.acom"))
    report={"checks":checks,"passed":sum(checks.values()),"total":len(checks),"payload_files":len(actual),"registry_values":len(reg),
        "setupSha256":sha(setup),"msiSha256":sha(msi),"sourceSha256":sha(sources),"development":pinned["development"],
        "scope":"Read-only Win32 MSI database/CAB and full hash verification; no registration performed in the operator account."}
    path=HERE/("INSTALLER_REVIEW_"+report["setupSha256"][:12]+".json")
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
    print(json.dumps(dict(passed=report["passed"],total=len(checks),files=len(actual),failed=[k for k,v in checks.items() if not v],report=str(path))))
    raise SystemExit(int(not all(checks.values())))

