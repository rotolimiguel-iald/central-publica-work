from flask import request,g
# Static extraction of existing runtime function; no server imports or secrets.
URL_PUBLICA="https://demo.iald.ia.br" # documented default only, not a secret/config read
ORIGENS_APP={"https://localhost","capacitor://localhost","ionic://localhost","http://localhost"}
def _private_media_origin_ok():
    origin = request.headers.get('Origin', '')
    origins = set(ORIGENS_APP) | {URL_PUBLICA.rstrip('/'), request.host_url.rstrip('/')}
    if origin and origin not in origins:return False
    if request.headers.get('Sec-Fetch-Site') == 'cross-site' and origin not in ORIGENS_APP:return False
    if not origin and not getattr(g,'app_bearer',False) and request.method != 'GET':return False
    return True
