"""Independent byte reversal and full internal-anchor scan for runtime condensation."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
    if not v:raise ValueError(msg)
def verify_runtime(path):
    from verify_reviewed_draft import verify
    path=Path(path);raw=path.read_bytes();d=json.loads(path.with_suffix('.json').read_bytes())
    need(sha(raw)==d['sha256'],'Draft drift')
    parent=Path(d['parent_path']);need(parent.parent==W and parent!=path,'Unexpected parent')
    need(not json.loads(parent.with_suffix('.json').read_bytes()).get('runtime_synthesis_compaction'),'Nested runtime summaries unsupported')
    verify(parent);parent_raw=parent.read_bytes();need(sha(parent_raw)==d['parent_sha256'],'Parent drift')
    directory=W/'runtime_synthesis_proposal_20260922_133458_573933'
    review_path=Path(d['review_path']);need(review_path.parent==directory,'Unexpected review')
    rr=review_path.read_bytes();need(sha(rr)==d['review_sha256'],'Review drift');review=json.loads(rr)
    need(review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL' and not review['remaining_required_changes'],'Review not approved')
    source=Path(d['original_path']);cap=Path(d['capsule_path'])
    need(source.parent==cap.parent==directory,'Unexpected artifacts')
    original=source.read_bytes();capsule=cap.read_bytes()
    need(sha(original)==d['original_sha256']==review['pins']['original.md']['sha256'],'Original drift')
    need(sha(capsule)==d['capsule_sha256']==review['pins']['capsule_v2.md']['sha256'],'Capsule drift')
    heading,body=capsule.decode().split('\n',1)
    replacement=heading+'\n\n**Estatutos [runtime_synthesis]**\n'+body.lstrip('\n')
    need(replacement==d['replacement'],'Undeclared wrapper')
    marker='\n## Exposição canônica integral: fórmulas e derivações'
    text=raw.decode();s=text.index(marker)+len(marker);expo=text[s:s+d['new_exposition_chars']]
    pt=parent_raw.decode();ps=pt.index(marker)+len(marker);old=pt[ps:ps+d['old_exposition_chars']]
    need(sha(expo.encode())==d['new_exposition_sha256'] and sha(old.encode())==d['old_exposition_sha256'],'Exposition drift')
    a=d['section_start'];n=d['old_length'];need(old[a:a+n]==original.decode(),'Original interval differs')
    need(old[:a]+replacement+old[a+n:]==expo,'Other exposition changed')
    counts={'literal':0,'summary':0,'runtime_summary':0}
    def walk(v):
        if isinstance(v,list):
            for x in v:walk(x)
        elif isinstance(v,dict):
            if '@EXPOSITION' in v or '@SUMMARY' in v:
                x,length=v['span'];need(type(x)is int and type(length)is int and 0<=x<x+length<=len(expo),'Bad reference span')
                frag=expo[x:x+length]
                if '@EXPOSITION' in v:
                    need(frag.startswith(v['starts_with']),'Stale literal');counts['literal']+=1
                else:
                    need(frag.startswith('**Estatutos ['+v['@SUMMARY']+']**'),'Stale summary')
                    need(v['source_pointer'].startswith('/core/'),'Missing primary pointer')
                    counts['summary']+=1
                    if v['@SUMMARY']=='runtime_synthesis':
                        need(v['span']==d['summary_span'],'Runtime reference outside approved block')
                        counts['runtime_summary']+=1
            else:
                for x in v.values():walk(x)
    for line in text.splitlines():
        try:value=json.loads(line)
        except (ValueError,TypeError):continue
        walk(value)
    need(counts=={'literal':22,'summary':59,'runtime_summary':3},'Unexpected reference inventory')
    for row in d['reference_lines']:
        need(text.count(row['after'])==1,'Ambiguous metadata reversal')
        text=text.replace(row['after'],row['before'],1)
    need(text.count(replacement)==1,'Ambiguous section reversal')
    text=text.replace(replacement,original.decode(),1)
    need(text.encode()==parent_raw,'Undeclared change outside summary and anchors')
    need(parent.read_bytes()==parent_raw and path.read_bytes()==raw,'Concurrent drift')
    return {'status':'RUNTIME_INTEGRATION_VERIFIED_NOT_DEPLOYED','draft_sha256':sha(raw),
            'all_other_parent_bytes_preserved':True,'references':counts,
            'scope':'Documentary integration and references, not proof or API fit.'}
