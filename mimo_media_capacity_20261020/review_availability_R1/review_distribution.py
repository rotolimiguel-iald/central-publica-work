import hashlib,json,re,sys
from pathlib import Path
W=Path(__file__).resolve().parent.parent;M=W/'mobile_stage'
sys.path.insert(0,str(W));import task
p=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
plan=json.loads((M/'apk30_publication/FINAL_R3/APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R3.json').read_bytes())
publication=json.loads((M/'apk30_publication/FINAL_R3/PUBLICATION_RESULT.json').read_bytes())
assert sha(publication['plan']['path'])==publication['plan']['sha256']
assert sha(publication['destination']['path'])==plan['source']['sha256']==publication['destination']['sha256']
for entry in plan['preserve_existing_apks']:assert sha(entry['path'])==entry['sha256']
anon=json.loads((M/'ANDROID30_ANONYMOUS_DOWNLOAD.json').read_bytes());auth=json.loads((M/'ANDROID30_AUTHENTICATED_DOWNLOAD.json').read_bytes())
assert len(anon['checks'])==2 and all(r['status']==302 and r['location']=='/login' and r['apk_bytes_delivered']==0 for r in anon['checks'])
assert sha(auth['path'])==auth['sha256']==plan['source']['sha256'] and Path(auth['path']).stat().st_size==auth['bytes']==4991283
ios=json.loads((M/'IOS35_DISTRIBUTION.json').read_bytes())
for e in ios['sources']:assert sha(e['path'])==e['sha256']
assert ios['build']=='35' and {x['name'] for x in ios['groups']}=={'IALD Equipe','IALD Piloto'} and all(x['status']=='Em testes' for x in ios['groups'])
for name in ('IOS35_EQUIPE_FULL.txt','IOS35_PILOTO_FULL.txt'):
    t=(M/name).read_text(encoding='utf-8');assert '35' in t and 'Em testes' in t
operator=(M/'IOS35_OPERATOR_PARTICIPATION_FULL.txt').read_text(encoding='utf-8');assert '35' in operator and 'Luiz' in operator
assert ios['physical_installation_verified'] is False and ios['expires_at'] is None
A=W/'admin_deadlines35stage';applied=json.loads((A/'DELIVERY_APPLIED_R1.json').read_bytes())
assert sha(applied['destination'])==applied['sha256'] and sha(applied['backup'])==applied['backup_sha256']
before=Path(applied['backup']).read_bytes();after=Path(applied['destination']).read_bytes()
def mask(raw):
    s=raw.decode('utf-8');spans=[]
    for k in ('testflight_internal','testflight_external'):
        matches=list(re.finditer('"'+k+'"'+r'\s*:\s*',s));assert len(matches)==1
        start=matches[0].end();_,end=json.JSONDecoder().raw_decode(s,start);spans.append((start,end))
    for start,end in sorted(spans,reverse=True):s=s[:start]+'<ALLOWED_SUBTREE>'+s[end:]
    return s.encode('utf-8')
assert mask(before)==mask(after)
admin=json.loads(after)
for k in ('testflight_internal','testflight_external'):assert admin['items'][k]['build']=='4.1 (35)' and admin['items'][k]['expires_at'] is None
evidence=[pin(M/n) for n in ('ANDROID30_ANONYMOUS_DOWNLOAD.json','ANDROID30_AUTHENTICATED_DOWNLOAD.json','IOS35_DISTRIBUTION.json','apk30_publication/FINAL_R3/PUBLICATION_RESULT.json')]+[pin(A/'DELIVERY_APPLIED_R1.json')]
report=dict(status='PASS_DOCUMENTARY_DISTRIBUTION_WITH_LIMITS',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=p['receipt']['revision'],final_delivery='NOT_ACCEPTED_PENDING_MEMORY_APPLICATION_AND_REAL_SUBMISSION',findings=[],evidence=evidence,
    checks=dict(published_apk_source_target_download_hash_match=True,old15_apks_preserved=True,two_anonymous_302_zero_apk_receipts=True,ios35_group_source_pins_and_fulltext_match=True,operator_participation_documented=True,admin_actual_and_backup_hashes_match=True,admin_bytes_outside_two_subtrees_identical=True),
    matrix=dict(android='4.1(30) published authenticated download verified from local downloaded bytes; no GooglePlay or physical installation claim',ios='4.1(35) Cloud success and both existing groups Em testes supported by pinned source records/full texts; Apple-reported installed35 is not physical verification',web='Engineering/runtime installation reviewed earlier; this bounded distribution check does not create provider perception PASS'),
    limits=['Actual HTTP behavior reviewed through parent receipts; no new HTTP/browser/provider request by reviewer. Anonymous302/login with zeroAPK is accepted.','JPEG proofs hash-checked; distribution fulltext inspected, not a new interactive Apple session.','Memory DRAFT_R3_FINAL is not an application receipt; eight applied surfaces/backups and final parent delivery/submit remain to review.','Audio perception negative and video failed/uncertain remain results. Engineering distribution does not prove model perception or maximum-context use.','No originais/memories/runtime edited and no mission requirement accepted.'])
out=W/'REVIEW_DISTRIBUTION_POSTPUBLICATION_R1.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode()
with out.open('xb') as f:f.write(raw)
assert out.read_bytes()==raw
print(json.dumps(dict(status=report['status'],checks=len(report['checks']),report=str(out),sha256=sha(out))))
