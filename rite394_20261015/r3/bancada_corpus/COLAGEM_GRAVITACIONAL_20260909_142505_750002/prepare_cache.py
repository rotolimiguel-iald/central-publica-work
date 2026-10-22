from pathlib import Path
import json, os
root=Path(__file__).resolve().parent
old=root.parent/'PREPARACAO_REGISTRO_UNIFICADO_20260909_140220_508532'
cfg=json.loads((old/'CACHE_UNIFIED.json').read_text(encoding='utf-8'))
cfg['cached']['UnifiedRecordedPreparation']={'source':str(old/'UnifiedRecordedPreparation.lean'),'build':str(old/'BUILD_20260909_140416_241257')}
c=root.parent/'COVARIANCIA_PREPARACAO_20260909_131114_393260'
cfg['cached']['JointPreparationCovariance']={'source':str(c/'JointPreparationCovariance.lean'),'build':str(c/'BUILD_20260909_131143_739517')}
raw=(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n').encode()
p=root/'CACHE_GLUING.json'
assert not p.exists()
t=p.with_suffix('.tmp')
with t.open('xb') as f:
    f.write(raw); f.flush(); os.fsync(f.fileno())
assert t.read_bytes()==raw
os.rename(t,p)
assert p.read_bytes()==raw
print(p)
