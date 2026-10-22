from pathlib import Path
import json,os
base=Path(r'C:\IALD\Central de Patentes\Chatgpt')
folder=Path(__file__).resolve().parent
src=base/'INTERACAO_LOCAL_GERAL_20260909_164621_372960'/'CACHE_TESTEMUNHA.json'
config=json.loads(src.read_text(encoding='utf-8'))
config['cached']['UnitaryCocycleUniqueness']={
    'source':(folder/'UnitaryCocycleUniqueness.lean').as_posix(),
    'build':(folder/'BUILD_20260909_170053_662440').as_posix()}
path=folder/'CACHE_LOCAL_UNIQUENESS.json'
assert not path.exists()
data=(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=path.with_name(path.name+'.tmp')
with tmp.open('xb') as f:
    f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,path)
print(path)
