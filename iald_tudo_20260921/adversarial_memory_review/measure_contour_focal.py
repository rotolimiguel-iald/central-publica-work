"""Read-only focal source/capsule audit; no project imports or network."""
from pathlib import Path
import hashlib, json, math, os, re, socket
BASE=Path(__file__).resolve().parent
WORK=BASE.parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(raw):return hashlib.sha256(raw).hexdigest()
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes()
assert sha(source_raw)==entry['public_sha256']
topic=json.loads(source_raw)['core']['contour_theory']
capsule_path=WORK/'semantic_capsules/contour_theory.md'
capsule_raw=capsule_path.read_bytes()
assert sha(capsule_raw)=='e4d1f2bbe787f7ba5f05621ce677c9af4832fd3d056ee88965bbe79411420c93'
capsule=capsule_raw.decode('utf-8')
candidate_raw=(WORK/'haiku_candidate.md').read_bytes()
candidate=candidate_raw.decode('utf-8')
match=re.search(r'(?m)^### contour_theory\nFonte: resultado_publicado_integral /core/contour_theory\n([^\n]+)',candidate)
assert match
assert len(topic['steps'])==7 and all(s['status']=='REAL' for s in topic['steps'])
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'.iald_runtime/tokenizer_cache')
def blocked(*a,**k):raise RuntimeError('No network permitted')
socket.socket=blocked
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
def tokens(value):return len(enc.encode(value,disallowed_special=()))
result={'status':'FOCAL_SOURCE_FIDELITY_REVIEW_NOT_PHYSICAL_VALIDATION',
 'source_sha256':sha(source_raw),'capsule_sha256':sha(capsule_raw),'candidate_sha256':sha(candidate_raw),
 'o200k':{'old_json_body':tokens(match[1]),'old_heading_source_and_body':tokens(match[0]),
          'new_full_capsule':tokens(capsule),'saving_vs_full_old_block':tokens(match[0])-tokens(capsule)},
 'anthropic_tokens':'NOT_MEASURED',
 'source_recorded_steps':len(topic['steps']),
 'inherited_limit_inconsistency':{'source_field':'neutrino_candidate',
   'formula':'alpha=sin^2(theta_M)/sqrt(e)',
   'literal_claim':'theta->90 (alpha->1, o Um)',
   'computed_limit_under_same_formula':1/math.sqrt(math.e),
   'scope':'Conditional algebra check only: same theta and same alpha; source gives no changed normalization here.'},
 'missing_explicit_source_relations':[
  {'pointer':'/core/contour_theory/steps/1','content':'GKLS rho_kappa fixed point; 0<rho<1; saturation, not supersaturation/condensation'},
  {'pointer':'/core/contour_theory/steps/2','content':'q=(g- - g+)/(g- + g+)'},
  {'pointer':'/core/contour_theory/steps/3','content':'alpha=2 sqrt(g+ g-)/(g+ + g-)'},
  {'pointer':'/core/contour_theory/steps/5','content':'q_static=0'},
  {'pointer':'/core/contour_theory/steps/6','content':'{Z,L_nu}=0; [Q_em,L_nu]=0; L^d L != 0'}],
 'files_unchanged':capsule_path.read_bytes()==capsule_raw and (WORK/'haiku_candidate.md').read_bytes()==candidate_raw and Path(entry['path']).read_bytes()==source_raw}
assert result['files_unchanged']
payload=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
target=BASE/'contour_focal_measurements.json';temp=target.with_suffix('.tmp')
assert not target.exists()
with temp.open('xb') as f:f.write(payload)
assert temp.read_bytes()==payload;temp.replace(target)
print(json.dumps(result,ensure_ascii=False,indent=2))
