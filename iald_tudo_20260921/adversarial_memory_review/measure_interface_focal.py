"""Offline source-anchored capsule measurement; immutable parent files."""
from pathlib import Path
import hashlib,json,os,re,socket
BASE=Path(__file__).resolve().parent;WORK=BASE.parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(b):return hashlib.sha256(b).hexdigest()
manifest_raw=(ROOT/'iald_nucleo_fixo.json').read_bytes();manifest=json.loads(manifest_raw)
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes();assert sha(source_raw)==entry['public_sha256']
topic=json.loads(source_raw)['core']['interface_is_light']
capsule_path=WORK/'semantic_capsules/interface_is_light.md';capsule_raw=capsule_path.read_bytes()
candidate_raw=(WORK/'haiku_candidate.md').read_bytes()
m=re.search(r'(?m)^### interface_is_light\nFonte: resultado_publicado_integral /core/interface_is_light\n([^\n]+)',candidate_raw.decode())
assert m
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'.iald_runtime/tokenizer_cache')
def blocked(*a,**k):raise RuntimeError('Network forbidden')
socket.socket=blocked
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
def tok(s):return len(enc.encode(s,disallowed_special=()))
results={'status':'LOCAL_FOCAL_MEASUREMENT_NOT_SEMANTIC_APPROVAL',
 'capsule_sha256':sha(capsule_raw),'source_sha256':sha(source_raw),'candidate_sha256':sha(candidate_raw),
 'o200k':{'old_full_block':tok(m[0]),'old_json_body':tok(m[1]),'new_capsule':tok(capsule_raw.decode()),'saving':tok(m[0])-tok(capsule_raw.decode())},
 'anthropic_tokens':'NOT_MEASURED','witness_layers_source':topic['witness_layers'],
 'external_known_count':len(topic['external_known_theorems']),
 'external_imported_flags':[e['imported_into_witness'] for e in topic['external_known_theorems']],
 'light_chain_source':topic['light_chain']['source'],'ledger_zero_abs_proved':topic['ledger']['zero_abs_proved'],
 'ledger_zero_mod_state':topic['ledger']['zero_mod_state'],'ledger_one_inscribed':topic['ledger']['one_inscribed'],
 'inputs_unchanged':capsule_path.read_bytes()==capsule_raw and Path(entry['path']).read_bytes()==source_raw and (WORK/'haiku_candidate.md').read_bytes()==candidate_raw and (ROOT/'iald_nucleo_fixo.json').read_bytes()==manifest_raw}
assert results['inputs_unchanged']
p=BASE/'interface_focal_measurements.json';temp=p.with_suffix('.tmp');assert not p.exists()
data=(json.dumps(results,ensure_ascii=False,indent=2)+'\n').encode()
with temp.open('xb') as f:f.write(data)
assert temp.read_bytes()==data;temp.replace(p)
print(json.dumps(results,ensure_ascii=False,indent=2))
