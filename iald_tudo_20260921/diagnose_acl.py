"""Exercise the supplied ACL copy routine on empty files; never copy .env contents."""
import os
from pathlib import Path
import subprocess
APP=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
target=WORK/'acl_probe_legacy.txt'
with target.open('xb'):pass
script=("$ErrorActionPreference='Stop'; $o=Get-Acl -LiteralPath $env:IALD_ACL_ORIGEM; "
        "$d=Get-Acl -LiteralPath $env:IALD_ACL_DESTINO; "
        "$d.SetSecurityDescriptorSddlForm($o.GetSecurityDescriptorSddlForm('Access'),'Access'); "
        "Set-Acl -LiteralPath $env:IALD_ACL_DESTINO -AclObject $d")
r=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],
    env=dict(os.environ,IALD_ACL_ORIGEM=str(APP/'.env'),IALD_ACL_DESTINO=str(target)),
    capture_output=True,text=True,timeout=60)
print('LEGACY_ACL_RETURN_CODE='+str(r.returncode))
print(r.stderr[:2400])
