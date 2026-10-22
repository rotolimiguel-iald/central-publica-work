"""Explicit read-only verification; never build, deploy, authenticate or call models."""
from pathlib import Path
import argparse, datetime, hashlib, http.client, json
from urllib.parse import quote
from prepare import W, ROOT, load, safe, save, sha

def anonymous(path):
    if not path.startswith(('/app/', '/api/chat-jobs/', '/downloads/')):
        raise ValueError('Unexpected public check path')
    connection=http.client.HTTPSConnection('demo.iald.ia.br',443,timeout=20)
    try:
        # No cookie, authorization, credentials, redirects or retry.
        connection.request('GET',path)
        response=connection.getresponse()
        body=response.read(65537)
        location=response.getheader('Location','')
        accepted=(response.status==401 or (response.status==302 and
                  (location=='/login' or location.startswith('/login?'))))
        passed=accepted and len(body)<=65536 and not body.startswith(b'PK\x03\x04')
        return dict(path=path,status=response.status,passed=passed,
                    login_redirect=response.status==302 and accepted,
                    bytes_read=len(body),body_sha256=hashlib.sha256(body).hexdigest(),
                    scope='Anonymous denial/redirect only; no authenticated download or perception test')
    finally:
        connection.close()

def verify(http=False, apk=False):
    plan_path=W/'install_plan.json'
    plan=load(plan_path)
    review=load(W/'validation/review_final.json')
    if review['status']!='PASS' or review['plan_sha256']!=sha(plan_path):
        raise ValueError('Missing/stale reviewed plan')
    # Existing review pin contract; verifier itself is an additive reviewed tool.
    for name,h in review['tool_pins'].items():
        p=(W/name).resolve()
        if not p.is_relative_to(W) or sha(p)!=h:
            raise ValueError('Reviewed tool pin mismatch')
    if review.get('verifier_sha256')!=sha(Path(__file__)):
        raise ValueError('Final verifier not pinned by reviewer')
    if plan['science_sha256']!=sha(W/'SCIENCE_BASELINE.json'):
        raise ValueError('Science manifest changed')
    checked=[]
    for row in plan['files']:
        source,target=safe(row['source']),safe(row['destination'])
        if not source.is_relative_to(W) or not target.is_relative_to(ROOT):
            raise ValueError('Plan path escaped scope')
        if sha(source)!=row['sha256'] or sha(target)!=row['sha256']:
            raise ValueError('Installed/source mismatch: '+target.name)
        checked.append(str(target))
    if not checked or len(checked)!=len(set(checked)):
        raise ValueError('Empty/duplicate installation plan')
    science=load(W/'SCIENCE_BASELINE.json')
    for row in science['files']:
        if sha(row['path'])!=row['sha256']:
            raise ValueError('Science changed')
    deployment=load(W/'deployment.json')
    if deployment['plan_sha256']!=sha(plan_path):
        raise ValueError('Deployment receipt does not cover plan')
    for row in plan['files']:
        if deployment['files'][str(Path(row['destination']).resolve())]!=row['sha256']:
            raise ValueError('Deployment receipt pin mismatch')
    if deployment['status']!='INSTALLED_STATIC_NO_RESTART' or deployment['restart'] is not False:
        raise ValueError('Expected client-only application without restart')
    observed=[]
    if http:
        paths=['/api/chat-jobs/session']
        for name in plan['assets']:
            if Path(name).name!=name:
                raise ValueError('Invalid asset name')
            paths.append('/app/'+quote(name,safe=''))
        if apk:paths.append('/downloads/IALD-4.1-34.apk')
        for path in paths:
            observed.append(anonymous(path))
    elif apk:
        raise ValueError('--apk requires --http')
    passed=all(r['passed'] for r in observed)
    matrix={
        'web':dict(status='PINS_VERIFIED',anonymous_http='PASS' if http and passed else 'FAIL' if http else 'NOT_RUN',authenticated_live='PENDING'),
        'ios_internal':dict(target='4.1(39)',group='IALD Equipe',status='PENDING_OFFICIAL_RECEIPT'),
        'ios_external':dict(target='4.1(39)',group='IALD Piloto',status='PENDING_OFFICIAL_RECEIPT'),
        'android':dict(target='4.1(34)',build_signature_archive_audit='PENDING_SEPARATE_AUDIT',authenticated_download='PENDING',anonymous_download='CHECKED' if http and apk else 'NOT_RUN'),
        'google_play':dict(status='NOT_VERIFIED'),
        'physical_installation':dict(status='NOT_VERIFIED')}
    return dict(status='PASS_WITH_SCOPE' if passed else 'FAIL_PUBLIC_BOUNDARY',
        checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        plan_sha256=sha(plan_path),files=len(checked),science_files=len(science['files']),
        anonymous_checks=observed,matrix=matrix,
        scope='Bytes, reviewed pins and optional public HTTP only. No model, credential, build, Git or installation operation. Mobile availability requires separate official receipts.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--http',action='store_true')
    parser.add_argument('--apk',action='store_true')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(W):raise SystemExit('Output must stay in release')
    result=verify(args.http,args.apk)
    save(output,result)
    print(json.dumps({'status':result['status'],'output':str(output)}))
    if result['status'].startswith('FAIL'):raise SystemExit(1)
