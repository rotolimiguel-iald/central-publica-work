from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
OUT = Path(__file__).resolve().parent
NAMES = [
 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
 'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
 'COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md',
 'NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md',
 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md',
 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md',
 'APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704/APLICACAO_OFFSHELL_E_FONTES_CENTRAIS.md',
]
def pin(p):
 b=p.read_bytes()
 return {'path':p.as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
records=[pin(ROOT/n) for n in NAMES]
target=OUT/'PINS_ENTRADA_088.json'
assert not target.exists()
data=json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scope':'Pins documentais de fontes; nenhuma execução matemática ou canônica','sources':records},ensure_ascii=False,indent=2).encode('utf-8')
tmp=target.with_suffix('.json.tmp_new')
with tmp.open('xb') as f:
 f.write(data); f.flush(); os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.replace(tmp,target)
print(json.dumps({'input_receipt':pin(target),'sources':records},ensure_ascii=False,indent=2))
