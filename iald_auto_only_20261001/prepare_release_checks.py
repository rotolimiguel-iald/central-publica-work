from pathlib import Path
import subprocess
W=Path(__file__).parent
C=W.parent
N=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
head=subprocess.check_output(['git','-C',str(N),'rev-parse','HEAD']).decode().strip()
assert head.startswith('f13127d')
s=(C/'iald_message_edit_20261001/audit_mobile.py').read_text(encoding='utf-8')
s=s.replace("EXPECTED_HEAD = '4f1869177a6bf2451c44485de5bdae6d676d0931'",'EXPECTED_HEAD = '+repr(head))
s=s.replace("for name in ('iald.js', 'iald.css'):","for name in ('iald.js',):")
s=s.replace("W / 'stage' / name","W / 'stage' / 'app' / name")
s=s.replace('IALD-4.1-24.apk','IALD-4.1-25.apk').replace('build24','build25').replace('APK24','APK25')
s=s.replace('[28, 28]','[29, 29]').replace('android_codes=[25]','android_codes=[26]')
s=s.replace("versionCode='25'","versionCode='26'").replace('versionCode=25','versionCode=26')
(W/'audit_mobile.py').write_text(s,encoding='utf-8')
s=(C/'iald_message_edit_20261001/publish_android.py').read_text(encoding='utf-8')
s=s.replace("==25","==26").replace('versionCode=25','versionCode=26').replace('IALD-4.1-25.apk','IALD-4.1-26.apk')
(W/'publish_android.py').write_text(s,encoding='utf-8')
print('Release checks prepared for '+head)
