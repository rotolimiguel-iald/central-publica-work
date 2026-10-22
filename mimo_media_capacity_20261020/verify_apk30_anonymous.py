"""One unauthenticated read per endpoint; no session or credential handling."""
from pathlib import Path
import http.client,json
W=Path(__file__).resolve().parent
rows=[]
for remote in (False,True):
    conn=(http.client.HTTPSConnection('demo.iald.ia.br',timeout=20) if remote
          else http.client.HTTPConnection('127.0.0.1',8082,timeout=20))
    try:
        conn.request('GET','/downloads/IALD-4.1-30.apk')
        response=conn.getresponse();raw=response.read(1048577)
        assert response.status in (302,303,401,403)
        assert not raw.startswith(b'PK') and len(raw)<1048577
        location=response.getheader('Location')
        if response.status in (302,303):assert location and '/login' in location
        rows.append(dict(endpoint='https://demo.iald.ia.br' if remote else 'local8082',
                         status=response.status,location=location,body_bytes=len(raw),
                         content_type=response.getheader('Content-Type'),apk_bytes_delivered=0))
    finally:conn.close()
with (W/'mobile_stage/ANDROID30_ANONYMOUS_DOWNLOAD.json').open('xb') as f:
    f.write(json.dumps(dict(status='PASS_ANONYMOUS_BLOCKED',checks=rows),indent=2).encode())
print('Anonymous APK delivery blocked at local and public endpoints')
