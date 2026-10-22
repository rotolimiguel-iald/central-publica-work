"""Offline fixture using coordinator's staging ffmpeg; installs nothing."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch
import iald_mimo_multimodal as media

root=Path(__file__).resolve().parent
dependency=root.parent/'media_dependency'
receipt=json.loads((dependency/'RECEIPT.json').read_text(encoding='utf-8'))
for name in ('ffmpeg.exe','ffprobe.exe'):
    expected=next(row['sha256'] for row in receipt['files'] if row['name']==name)
    assert hashlib.sha256((dependency/name).read_bytes()).hexdigest()==expected
factory=tempfile.TemporaryDirectory
def local_temp(*args,**kwargs):
    kwargs['dir']=root
    return factory(*args,**kwargs)
with factory(prefix='real_decoder_',dir=root) as directory:
    fixture=Path(directory)/'tiny.mp4'
    subprocess.run([str(dependency/'ffmpeg.exe'),'-v','error','-f','lavfi','-i',
        'color=c=black:s=32x32:d=1','-c:v','mpeg4','-y',str(fixture)],check=True,timeout=15,
        capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    with patch.object(media,'VENDOR',dependency),patch.object(media.tempfile,'TemporaryDirectory',local_temp):
        caps=media.media_capabilities()
        assert caps['video'] is True
        measured=media.probe_media(fixture.read_bytes(),'video/mp4')
        assert 'video' in measured['types'] and 0<measured['duration']<=10
        result=dict(status='PASS',capabilities=caps,measured=measured,
            fixture_bytes=fixture.stat().st_size,installed=False,network_calls=0,
            scope='real pinned ffprobe snapshot and synthetic MP4; not provider/browser/device validation')
(root/'real_decoder_result_R4.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
