import json
import subprocess
from inspect_audio_scope import *

target=G/'MEMORY_DEPOSIT_RECEIPT.json'
assert not target.exists(),'Recover receipt; do not repeat a deposit'
args=[r'C:\Python314\python.exe','-B','-X','utf8',r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py','depositar','--quem','codex-video-v7','--tipo','project','--estatuto','REAL','--alvo','novo:filmes-v7','--casa','Física/TGL','--slug','filmes-v7-v404-parada-tts-adicional','--texto-arquivo',str(G/'MEMORY_DEPOSIT_TEXT.txt'),'--fonte',str(T/'RESULTADO.json'),'--fonte',str(G/'INDEPENDENT_AUDIO_SCOPE_REVIEW.json')]
r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
create(target,{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
assert r.returncode==0,r.stdout+r.stderr
receipt=json.loads(r.stdout)
assert receipt['ok']
assert pin(Path(receipt['arquivo']))['sha256']==receipt['sha256_deposito']
print(json.dumps(receipt,ensure_ascii=False))
