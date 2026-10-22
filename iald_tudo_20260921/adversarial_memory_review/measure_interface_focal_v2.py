"""Offline remeasurement; no application imports and no parent-file writes."""
from pathlib import Path
import hashlib,json,os,re,socket
BASE=Path(__file__).resolve().parent;WORK=BASE.parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(b):return hashlib.sha256(b).hexdigest()
manifest_raw=(ROOT/'iald_nucleo_fixo.json').read_bytes();manifest=json.loads(manifest_raw)
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes();assert sha(source_raw)==entry['public_sha256']
previous=json.loads((BASE/'interface_focal_measurements.json').read_bytes())
assert sha(source_raw)==previous['source_sha256']
topic=json.loads(source_raw)['core']['interface_is_light']
capsule_path=WORK/'semantic_capsules/interface_is_light.md';capsule_raw=capsule_path.read_bytes()
candidate_raw=(WORK/'haiku_candidate.md').read_bytes()
m=re.search(r'(?m)^### interface_is_light\nFonte: resultado_publicado_integral /core/interface_is_light\n([^\n]+)',candidate_raw.decode())
assert m
children=['statuses','witness_layers','ledger','named_target','negative_probes_summary','light_chain','graviton_reading','external_known_theorems','seals','not_claimed','form_content','canonical_markers']
assert all(k in topic for k in children)
assert len(topic['external_known_theorems'])==12
assert all(e['imported_into_witness'] is False for e in topic['external_known_theorems'])
assert topic['form_content']['anchors_checked']==10
assert topic['witness_layers']['regular_full_witness_term_constructed'] is True
assert topic['witness_layers']['canonical_full_witness_term_constructed'] is False
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'.iald_runtime/tokenizer_cache')
def blocked(*a,**k):raise RuntimeError('Network forbidden')
socket.socket=blocked
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
def tok(s):return len(enc.encode(s,disallowed_special=()))
new_count=tok(capsule_raw.decode());old_count=tok(m[0])
results={'status':'LOCAL_FOCAL_MEASUREMENT_V2',
 'capsule_sha256':sha(capsule_raw),'source_sha256':sha(source_raw),'candidate_sha256':sha(candidate_raw),
 'o200k':{'old_full_block':old_count,'old_json_body':tok(m[1]),'new_capsule':new_count,'saving':old_count-new_count,
 'previous_capsule':previous['o200k']['new_capsule'],'increase_vs_previous':new_count-previous['o200k']['new_capsule']},
 'anthropic_tokens':'NOT_MEASURED','operational_retrieval':'NOT_VALIDATED',
 'referenced_children_exist':children,'source_identical_to_previous_review':True,
 'inputs_unchanged':capsule_path.read_bytes()==capsule_raw and Path(entry['path']).read_bytes()==source_raw and (WORK/'haiku_candidate.md').read_bytes()==candidate_raw and (ROOT/'iald_nucleo_fixo.json').read_bytes()==manifest_raw}
assert results['inputs_unchanged']
p=BASE/'interface_focal_v2_measurements.json';temp=p.with_suffix('.tmp');assert not p.exists()
data=(json.dumps(results,ensure_ascii=False,indent=2)+'\n').encode()
with temp.open('xb') as f:f.write(data)
assert temp.read_bytes()==data;temp.replace(p)
print(json.dumps(results,ensure_ascii=False,indent=2))
