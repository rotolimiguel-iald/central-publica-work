"""Offline measurement of the revised contour capsule, with immutable inputs."""
from pathlib import Path
import hashlib, json, os, re, socket
BASE=Path(__file__).resolve().parent
WORK=BASE.parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(raw): return hashlib.sha256(raw).hexdigest()
manifest_raw=(ROOT/'iald_nucleo_fixo.json').read_bytes()
manifest=json.loads(manifest_raw)
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes()
assert sha(source_raw)==entry['public_sha256']
previous=json.loads((BASE/'contour_focal_measurements.json').read_bytes())
assert sha(source_raw)==previous['source_sha256']
topic=json.loads(source_raw)['core']['contour_theory']
capsule_path=WORK/'semantic_capsules/contour_theory.md'
capsule_raw=capsule_path.read_bytes()
assert sha(capsule_raw)=='e1a10161a858644ac3edc5d4b4c0c50041eb0bf51e12164838be547ea0459d78'
candidate_raw=(WORK/'haiku_candidate.md').read_bytes()
match=re.search(r'(?m)^### contour_theory\nFonte: resultado_publicado_integral /core/contour_theory\n([^\n]+)',candidate_raw.decode())
assert match
children=['steps','psionic_bond_unification','first_law_link','open_theorem_verdict']
assert all(k in topic for k in children)
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'.iald_runtime/tokenizer_cache')
def blocked(*a,**k): raise RuntimeError('Network prohibited')
socket.socket=blocked
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
def tokens(text): return len(enc.encode(text,disallowed_special=()))
new_count=tokens(capsule_raw.decode())
old_count=tokens(match[0])
result={'status':'LOCAL_MEASUREMENT_FOCAL_REVIEW_V2',
 'capsule_sha256':sha(capsule_raw),'source_sha256':sha(source_raw),
 'candidate_sha256':sha(candidate_raw),'manifest_sha256':sha(manifest_raw),
 'o200k':{'old_full_block':old_count,'old_json_body':tokens(match[1]),
 'new_full_capsule':new_count,'saving_vs_old_full_block':old_count-new_count,
 'previous_capsule_count_from_verified_receipt':previous['o200k']['new_full_capsule'],
 'increase_vs_previous_capsule':new_count-previous['o200k']['new_full_capsule']},
 'referenced_children_exist_in_source':children,'operational_json_pointer':'NOT_VALIDATED',
 'anthropic_tokens':'NOT_MEASURED','source_unchanged_since_previous_review':True,
 'inputs_unchanged_during_measurement':capsule_raw==capsule_path.read_bytes() and source_raw==Path(entry['path']).read_bytes() and candidate_raw==(WORK/'haiku_candidate.md').read_bytes() and manifest_raw==(ROOT/'iald_nucleo_fixo.json').read_bytes()}
assert result['inputs_unchanged_during_measurement']
payload=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
target=BASE/'contour_focal_v2_measurements.json';temporary=target.with_suffix('.tmp')
assert not target.exists()
with temporary.open('xb') as stream: stream.write(payload)
assert temporary.read_bytes()==payload
temporary.replace(target)
print(json.dumps(result,ensure_ascii=False,indent=2))
