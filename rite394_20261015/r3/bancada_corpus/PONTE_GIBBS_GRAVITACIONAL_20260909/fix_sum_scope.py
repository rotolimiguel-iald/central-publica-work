from pathlib import Path
import datetime,os,hashlib,json
p=Path(__file__).resolve().parent/'MixedGibbsGravitationalBridge.lean'
raw=p.read_bytes(); old=raw.decode('utf8')
a='  ∑ j, finiteEntropy (quadraticWeights (k j) (covectorRead (w j) d) t)-finiteEntropy (mixedBase (k j))'
b='  ∑ j, (finiteEntropy (quadraticWeights (k j) (covectorRead (w j) d) t)-finiteEntropy (mixedBase (k j)))'
assert old.count(a)==1 and old.count('tendsto_finset_sum')==2
new=old.replace(a,b).replace('tendsto_finset_sum','tendsto_finsetSum').encode('utf8')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:
    f.write(raw);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==raw
temp=p.with_name(p.name+'.tmp_'+stamp)
with temp.open('xb') as f:
    f.write(new);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==new and len(new)==len(raw)+0
os.replace(temp,p)
assert p.read_bytes()==new
print(json.dumps({'backup':str(bak),'bytes':len(new),'sha256':hashlib.sha256(new).hexdigest()}))
