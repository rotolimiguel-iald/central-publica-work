"""Final read-only source integrity measurement; new immutable receipt."""
import ast
import hashlib
import json
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')

def main():
    baseline=json.loads((OUT/'SOURCE_BASELINE.json').read_bytes())
    checks=[]
    for x in baseline['copied']:
        for role in ['source','copy']:
            p=Path(x[role]['path']);checks.append({'role':role,'path':str(p),'sha256':pin(p)['sha256'],'expected':x[role]['sha256'],'ok':pin(p)['sha256']==x[role]['sha256']})
    for x in baseline['embedded_materialized']:
        p=CANON/'tgl_kernel'/x['relative'];actual=pin(p)['sha256']
        checks.append({'role':'canonical_source','path':str(p),'sha256':actual,'expected':x['candidate']['sha256'],'ok':actual==x['candidate']['sha256']})
    cache=json.loads((OUT/'formal_verified/CACHE_RECEIPT.json').read_bytes())
    for x in cache['entries']:
        p=Path(cache['source'])/x['relative'];actual=pin(p)['sha256']
        checks.append({'role':'canonical_cached_olean','path':str(p),'sha256':actual,'expected':x['sha256'],'ok':actual==x['sha256']})
    candidate=OUT/'candidate_r2/um.py';tree=ast.parse(candidate.read_text(encoding='utf-8'))
    embedded=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets))
    materialized=[]
    for rel,body in embedded.items():
        p=candidate.parent/'tgl_kernel'/rel;expected=hashlib.sha256(body.encode()).hexdigest()
        materialized.append({'relative':rel,'sha256':pin(p)['sha256'],'ok':pin(p)['sha256']==expected})
    pyc=[str(p.relative_to(OUT)) for p in OUT.rglob('__pycache__')]
    links=[str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_symlink() or p.is_junction()]
    result={'passed':all(x['ok'] for x in checks+materialized) and not links,'candidate':pin(candidate),'baseline_checks':checks,
            'baseline_check_count':len(checks),'materialized':materialized,'materialized_count':len(materialized),'junctions_or_links':links,'pycache_directories':pyc,
            'scope':'Original pinned program/results/seal/proofmanifest,1232canonical materialized sources and1225cachedoleans compared by bytes; no claim about unrelated concurrent files.'}
    new(OUT/'FINAL_SOURCE_INTEGRITY_R1.json',result)
    print(json.dumps({k:result[k] for k in ['passed','baseline_check_count','materialized_count','junctions_or_links','pycache_directories']}))

if __name__=='__main__':main()
