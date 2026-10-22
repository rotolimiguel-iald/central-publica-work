"""Record the parent's completed documentary comparison; check anchors mechanically.

The prose review was performed by reading all three originals and proposals.
Hash/path checks below support that comparison; they do not establish semantics.
"""
from pathlib import Path
from datetime import datetime
import hashlib,json
from verify_reviewed_draft import verify

W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
TOPICS=('cocycle_to_einstein','ergodicity_door_mixing','inverse_parity')
NOTES={
 'cocycle_to_einstein': 'E1–E6 type-I scope and E7 composition/not-test retained; clock torsion/curvature orders, U(1) quotient, 0.9970/0.30%, RHS beta, Levi-Civita and no unrestricted Einstein proof retained. Long seals recoverable; internal literal references unchanged.',
 'ergodicity_door_mixing': 'N1 unconditional/N2 Wiener/N3 conditional Davies distinction retained; III1 does not exclude atoms, pure-point geometry versus dynamics and both negative controls retained. Auxiliary residual series recoverable, not represented as newly computed.',
 'inverse_parity': 'Population and finite-part formulas, finite-chi support, formal closure versus undetermined value, CODATA input, scheme dependence and refuted half-nat polarization retained. Source chi=0=0_abs ambiguity expressly preserved without reconciliation.'}
def sha(b):return hashlib.sha256(b).hexdigest()
def resolve(root,pointer):
    value=root
    for part in pointer.split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value

def check_references(capsule,topic,source,exposition):
    refs=json.loads(capsule.decode().splitlines()[-1])
    def walk(n):
        if isinstance(n,list):
            for x in n:walk(x)
        elif isinstance(n,dict):
            if '@' in n:
                value=resolve(source,'/core/'+topic+n['@'])
                for key,v in n.get('fields',{}).items():
                    assert resolve(value,key)==v, 'Changed protected reference field'
                if 'items' in n: assert len(value)==n['items']
            elif '@EXPOSITION' in n:
                a,length=n['span'];assert 0<=a<a+length<=len(exposition)
                assert exposition[a:a+length].startswith(n['starts_with'])
            elif '@SUMMARY' in n:
                raise ValueError('Unexpected summary reference: focal review required')
            else:
                for v in n.values():walk(v)
    walk(refs)

def main():
    manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
    entry=next(x for x in manifest['entries'] if x['id']=='resultado_publicado_integral')
    source_raw=Path(entry['path']).read_bytes();assert sha(source_raw)==entry['public_sha256']
    source=json.loads(source_raw);rows=[]
    for topic in TOPICS:
        directory=W/'topic_capsules_v4'
        prov=json.loads((directory/(topic+'.provenance.json')).read_bytes())
        parent=Path(prov['candidate_path']);verify(parent)
        raw=parent.read_bytes();assert sha(raw)==prov['candidate_sha256']
        original=(directory/(topic+'.original.md')).read_bytes()
        capsule=(directory/(topic+'.md')).read_bytes()
        assert sha(original)==prov['original_sha256'] and sha(capsule)==prov['capsule_sha256']
        a,n=prov['original_block_byte_span'];assert raw[a:a+n]==original
        d=json.loads(parent.with_suffix('.json').read_bytes());t=raw.decode()
        marker='\n## Exposição canônica integral: fórmulas e derivações'
        start=t.index(marker)+len(marker);expo=t[start:start+d['new_exposition_chars']]
        check_references(capsule,topic,source,expo)
        rows.append({'topic':topic,'original_sha256':sha(original),'capsule_sha256':sha(capsule),
                     'documentary_comparison':NOTES[topic]})
    report={'status':'APPROVED_DOCUMENTARY_FIDELITY_ONLY',
            'parent_sha256':sha(raw),'source_sha256':sha(source_raw),'topics':rows,
            'scope':'Existing loaded content; no new proof, compilation, empirical confirmation or API-fit claim.'}
    out=W/'adversarial_memory_review'/('topic_v4_first3_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
    with out.open('xb')as f:f.write(json.dumps(report,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'path':str(out),'status':report['status'],'topics':list(TOPICS)}))

if __name__=='__main__':main()
