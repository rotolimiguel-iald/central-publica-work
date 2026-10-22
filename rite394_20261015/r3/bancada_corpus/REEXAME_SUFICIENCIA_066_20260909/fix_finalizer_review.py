from pathlib import Path
from datetime import datetime
import ast,os
p=Path(__file__).resolve().parent/'finalize_delivery066.py'
raw=p.read_bytes();text=raw.decode('utf8')
changes=[
("    b=p.read_bytes(); pins[p.as_posix()]={'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}; return b",
 "    b=p.read_bytes(); pin={'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}\n    if p.as_posix() in pins: assert pins[p.as_posix()]==pin,'Input changed between reads.'\n    pins[p.as_posix()]=pin\n    return b"),
("rawcopy=read(COPY/'um.py');assert pins[(COPY/'um.py').as_posix()]==integration['integrated_copy']",
 "rawcopy=read(COPY/'um.py');assert pins[(COPY/'um.py').as_posix()]==integration['integrated_copy']\nassert config['root_confirmed'] is True\nassert build['plan']==pins[(BUILD/'BUILD_PLAN.json').as_posix()]\nassert plan['integration_result']==pins[(COPY/'INTEGRATION_RESULT.json').as_posix()]\nassert plan['integrated_copy']==integration['integrated_copy']==audit['final_integrated']\nassert audit['combined_build_read']['receipt']==pins[(BUILD/'TRANSPOSED_RESULT.json').as_posix()]\nassert audit['approved_configuration']==pins[(COPY/'CONFIG_APROVADA.json').as_posix()]\nassert audit['canonical_role']=='HISTORICAL_SNAPSHOT_BASE'"),
("prior={p['path']:p for p in snapshot['pins']}",
 "prior={p['path']:p for p in snapshot['pins']}\nassert snapshot['status']=='READ_ONLY_STABLE_SNAPSHOT' and snapshot['seal_um_hash_matches'] and snapshot['all_read_sources_unchanged']\nexpected_prior_paths={(CANON/n).as_posix() for n in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','rodada_v338_stdout.txt']}\nassert {c['path'] for c in snapshot['comparison_with_delivery065']}==expected_prior_paths\nassert all(c['matches_prior'] is True for c in snapshot['comparison_with_delivery065'])")]
for old,new in changes:
    assert text.count(old)==1
    text=text.replace(old,new)
data=text.encode();ast.parse(text)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==raw
tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data and p.read_bytes()==raw and len(data)>len(raw)
os.replace(tmp,p);assert p.read_bytes()==data
print('Three review corrections applied with verified immediate byte backup; syntax valid.')
