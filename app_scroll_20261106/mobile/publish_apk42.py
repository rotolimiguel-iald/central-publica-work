"""Publish audited APK42 once, only after explicit parent authorization."""
import os
from pathlib import Path
from publication_guards import APP,D,checked,intent,pin,read,require,sha,report,HERE

def publish():
    plan,audit,authorization=checked('apk')
    require(os.name=='nt','Windows no-overwrite rename required')
    source=Path(audit['apk']);raw=source.read_bytes()
    downloads=APP/'downloads'
    require(downloads.resolve(strict=True)==downloads,'Redirected downloads directory')
    dest=downloads/'IALD-4.1-42.apk'
    temp=downloads/'IALD-4.1-42.apk.tmp_scroll42'
    require(not dest.exists() and not temp.exists(),'Existing publication: reconcile without retry')
    older={p.name:sha(p.read_bytes()) for p in downloads.glob('*.apk')}
    require(older.get('IALD-4.1-41.apk')==read(HERE/'ANDROID_TOOLS.json')['baseline_apk']['sha256'],'APK41 drift')
    intent('PUBLICATION',dict(source=pin(source),target=str(dest),older=older,authorization=pin(HERE/'PARENT_PUBLICATION_READY.json')))
    with temp.open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    require(temp.read_bytes()==raw,'Temporary APK mismatch')
    checked('apk')
    require(all(sha((downloads/n).read_bytes())==h for n,h in older.items()),'Older APK drift')
    temp.rename(dest)
    require(sha(dest.read_bytes())==audit['apk_sha256'] and
            all(sha((downloads/n).read_bytes())==h for n,h in older.items()),'Publication verification failed')
    report(D/'APK_PUBLICATION.json',dict(status='PUBLISHED_BYTES_VERIFIED',artifact=pin(dest),bytes=len(raw),
        older_preserved=len(older),authenticated_download='PENDING',anonymous_denial='PENDING',
        url='https://demo.iald.ia.br/downloads/IALD-4.1-42.apk',google_play='NOT_PUBLISHED'))

if __name__=='__main__':
    publish()
