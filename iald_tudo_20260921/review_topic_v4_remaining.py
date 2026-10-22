"""Parent's documentary review of the twelve proposals read in full this turn."""
from pathlib import Path
from datetime import datetime
import hashlib,json
from verify_reviewed_draft import verify
from review_topic_capsules_v4 import check_references
W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
NOTES={
'kernel_formalization':'Reported strict Lean/Lake audit, forbidden axioms, conditional continuous corner versus finite theorem, external literature, measured G and historical v135/v350 scopes retained. Execution fingerprints moved to source, no new compilation claim.',
'neutrino_mass':'Assumed sin45 and 1eV, mass-versus-splitting, documentary priority erratum, postdiction/non-ex-ante status, refused fitted scale, growing JUNO tension and superseding live test retained. kg conversion and absolute residual recoverable.',
'smatrix_closure':'Formula for corner/S-matrix and tracial weights retained; finite shadow versus genuine factor and conditional continuum explicit. Negative controls, rank loss and physical/ontological scope retained. Approximate normalized/raw traces are visibly approximations; full values in source.',
'd1_camb_v3_pipeline':'PT/EN duplicate reduced without changing checks; C-free failure24/24, absorption into vacuum, beta-order effect, no rerun/relaxed criterion, synthetic validation and no gate movement retained.',
'name_index':'PP optimality required for equality versus upper bound; qubit index2 distinct from core1/beta; all five targets/failure names, Haar negative and modular-period caveat retained.',
'half_nat_continuous_corner_density':'Full chain from half-nat and trace split to area/eta/8piG retained; Planck-face normalization declared, G not derived, finite/III1 historical flags preserved; existing literal claim/status references retained.',
'name_relation':'p.q.p, geometric versus tracial weight, TL3 generic beta and corrected v28 scope retained. Spectral pure-point versus local pure state, Bell gap/CCI, III1 guardrail and canonical-selection OPEN retained.',
'selector_transport':'Transport not curvature; faithful-expectation iff, bimodularity and normality limitation retained. S-matrix weights and beta(1-beta) defect exact versus approximate beta; conjectural index and conditional Markov data remain separate from ONTO legal analogy.',
'the_imported_expectation':'Imported conclusion/dictionary versus proved hypotheses and sequential normality retained; uniqueness, omega preservation, named dependencies, literature citations, weak contract and Lemma3 not-unrestricted-solved retained.',
'right_angle_mirror':'Original NOT_A_CANDIDATE/CANDIDATA tension explicit; fixed-point formulas,37ppm, undetermined mirror/exponent, CODATA not derived and literal protected reconstruction fields retained.',
'tgl_closure':'Support versus mirror types, minimal Hamiltonian and constructors given support retained. Known-theorem composition versus Lean certification, gauge DEF/AX, historical false flag, open curved spacetime and no empirical confirmation retained.',
'ontological_relativity':'ONTO/AX versus numerical anchors and no experimental ontology claim retained; explicit contour, finite trace versus normal states, asymptotic condition, zeros and alpha guardrails retained. Slight size growth accepted for explicit concepts, not a claimed saving.'}
def sha(b):return hashlib.sha256(b).hexdigest()
base=W/'haiku_reviewed_section_20260922_130747_311801.md';verify(base)
base_raw=base.read_bytes();d=json.loads(base.with_suffix('.json').read_bytes());t=base_raw.decode()
marker='\n## Exposição canônica integral: fórmulas e derivações';s=t.index(marker)+len(marker)
expo=t[s:s+d['new_exposition_chars']]
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
entry=next(x for x in manifest['entries'] if x['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes();assert sha(source_raw)==entry['public_sha256'];source=json.loads(source_raw)
previous_path=W/'adversarial_memory_review/topic_v4_first3_20260922_133654_176011.json'
previous_raw=previous_path.read_bytes();previous=json.loads(previous_raw)
assert previous['parent_sha256']==sha(base_raw) and previous['source_sha256']==sha(source_raw)
rows=list(previous['topics'])
for topic,note in NOTES.items():
    directory=W/'topic_capsules_v4';p=json.loads((directory/(topic+'.provenance.json')).read_bytes())
    parent=Path(p['parent_path']);verify(parent);parent_raw=parent.read_bytes()
    assert sha(parent_raw)==p['parent_sha256']
    old=(directory/(topic+'.original.md')).read_bytes();new=(directory/(topic+'.md')).read_bytes()
    assert sha(old)==p['original_sha256'] and sha(new)==p['capsule_sha256']
    a,n=p['original_byte_span'];assert parent_raw[a:a+n]==old and base_raw.count(old)==1
    check_references(new,topic,source,expo)
    rows.append({'topic':topic,'original_sha256':sha(old),'capsule_sha256':sha(new),'documentary_comparison':note})
report={'status':'APPROVED_DOCUMENTARY_FIDELITY_ONLY','parent_sha256':sha(base_raw),
        'source_sha256':sha(source_raw),'topics':rows,
        'prior_first3_review':{'path':str(previous_path),'sha256':sha(previous_raw)},
        'scope':'All twelve originals/proposals read by parent; plus prior first-three review. Documentary only, not proof/API fit.'}
out=W/'adversarial_memory_review'/('topic_v4_all15_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with out.open('xb')as f:f.write(json.dumps(report,ensure_ascii=False,indent=2).encode())
assert base.read_bytes()==base_raw
print(json.dumps({'path':str(out),'status':report['status'],'topics':len(rows)}))
