"""Additive authenticated-download artifact; requires reviewed audit and current deploy preflight."""
from pathlib import Path
import json,hashlib,os,sys
from prepare import W,save
from guards import preflight
def new(name,value):save(W/name,value)
from mobile_release import checked,resource_pins
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(source,audit):
    source=Path(source).resolve(strict=True);audit=Path(audit).resolve(strict=True)
    assert source.is_relative_to(W/'mobile_stage') and audit.is_relative_to(W/'mobile_stage')
    review=json.loads((W/'validation/mobile_review.json').read_bytes());assert review['status']=='PASS'
    assert review['publisher_sha256']==sha(Path(__file__))
    assert review['audit_sha256']==sha(audit)
    a=json.loads(audit.read_bytes());assert a['status']=='PASS' and a['versionCode']==33 and a['apk_sha256']==sha(source)
    plan=checked();assert a['resources']==resource_pins(plan) and a['signer_matches_previous'] is True
    preflight()
    dest=Path(r'C:\IALD\projetos_pyhton\IALD\downloads\IALD-4.1-33.apk')
    assert not dest.exists() and not (W/'APK_PUBLICATION.json').exists()
    before={p.name:sha(p) for p in dest.parent.glob('*.apk')}
    new('APK_PUBLICATION_INTENT.json',dict(source=str(source),source_sha256=sha(source),audit=str(audit),audit_sha256=sha(audit),destination=str(dest),no_repeat=True))
    temp=dest.with_name(dest.name+'.tmp_attachments_beta');raw=source.read_bytes()
    temp.open('xb').write(raw);assert temp.read_bytes()==raw;assert not dest.exists()
    os.rename(temp,dest);assert dest.read_bytes()==raw
    assert all(sha(dest.parent/name)==pin for name,pin in before.items())
    new('APK_PUBLICATION.json',dict(status='PUBLISHED_AUTH_DOWNLOAD_PENDING',path=str(dest),bytes=len(raw),sha256=sha(dest),older_apks_preserved=len(before),url='https://demo.iald.ia.br/downloads/IALD-4.1-33.apk'))
if __name__=='__main__':run(*sys.argv[1:])
