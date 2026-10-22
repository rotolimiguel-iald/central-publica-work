"""Read-only verification of the installed runtime, without an API request."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
from dotenv import dotenv_values

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
import iald_memoria_canonica as memory
import iald_kernel as kernel
import iald_motores as motor

cfg = motor.carregar_config(dotenv_values(ROOT / '.env').get)
catalog = kernel.KernelCatalog(cfg.kernel_bundle, cfg.kernel_verification)
context, metadata = memory.CanonicalMemory(cfg.atlas_path, cfg.memoria_modo).prompt('',catalog)
assert metadata['fixed_nucleus_complete'] and len(metadata['fixed_nucleus_files']) == 7
assert 'Luiz Antonio Rotoli Miguel' in memory.CANONICAL_IDENTITY
assert 'H_3L=Dc*Dc+Db*Db+Dz*Dz >= 0' in memory.FRAMEWORK_PROTOCOL
assert metadata['context_tokens'] + cfg.max_saida < cfg.janela
files = ['app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js',
         'iald-app/android/app/src/main/assets/public/iald.js']
hashes = {name:hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files}
assert len(set(hashes.values())) == 1
report = {'recorded_at':datetime.now().astimezone().isoformat(), 'status':'INSTALLED_FILES_VERIFIED',
          'memory':metadata,'kernel':catalog.status(),'model':cfg.modelo,'window':cfg.janela,
          'synced_renderer_hashes':hashes,'api_called':False}
path = WORK / ('installed_verification_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
temp = path.with_suffix('.tmp')
data = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
with temp.open('xb') as handle:
    handle.write(data)
assert temp.read_bytes() == data
temp.replace(path)
print(json.dumps({'status':report['status'],'context_tokens':metadata['context_tokens'],
                  'complete_documents':len(metadata['fixed_nucleus_files']), 'window':cfg.janela,
                  'renderer_copies':len(hashes),'receipt':str(path)},ensure_ascii=True))
