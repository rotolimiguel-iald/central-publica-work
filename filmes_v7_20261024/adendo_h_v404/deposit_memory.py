"""Deposit one evidence-backed record through the established memory queue CLI."""
from context import *
check(); stable_seal()
assert not (H/'MEMORY_DEPOSIT_SEND_INTENT.json').exists(), 'Recover the existing deposit; do not repeat.'
queue=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py')
args=[sys.executable,'-B','-X','utf8',str(queue),'depositar','--quem','codex-video-v7','--tipo','project','--estatuto','REAL','--alvo','novo:filmes-v7','--casa','Física/TGL','--slug','filmes-v404-construcao','--texto-arquivo',str(H/'MEMORY_DEPOSIT.md')]
sources=[T/'RESULTADO.json',T/'RELATORIO.md',H/'FINAL_DELIVERY_REVIEW.json',H/'MEDIA_FINAL_BINDING.json',V.parent/'PUBLIC_DELIVERY_V7.json']
for p in sources:args.extend(['--fonte',str(p)])
create(H/'MEMORY_DEPOSIT_SEND_INTENT.json',{'operation':'depositar','actor':'codex-video-v7','text':pin(H/'MEMORY_DEPOSIT.md'),'sources':[pin(p) for p in sources],'destination_queue':str(queue)})
r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
create(H/'MEMORY_DEPOSIT_RESULT.json',{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
assert r.returncode==0,r.stderr
print(r.stdout)
