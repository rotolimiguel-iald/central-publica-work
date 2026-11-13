"""Record only the measured partial v410 route. No publication, deployment or final receipt."""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent
if __name__ == '__main__':
    result=json.loads((W/'RESULTADO_PARCIAL_APP_R1.json').read_bytes())
    assert result['estado']=='parcial' and result['release_instalada']=='v409'
    for row in result['arquivos']:
        p=Path(row['path']);assert p.is_relative_to(W) and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
    receipt=W/'ROUTE_PARTIAL_RECEIPT_R1.json'
    if receipt.exists():raise SystemExit('Receipt already exists; inspect it, never repeat blindly.')
    p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'ROUTE_PARTIAL_R1.json'),'--quem','codex-coordenadora-01a0ce2b'],capture_output=True)
    raw=p.stdout;data=json.loads(raw)
    with receipt.open('xb') as f:f.write(raw)
    assert receipt.read_bytes()==raw
    if p.returncode:raise SystemExit('Route registration failed; receipt preserved.')
    print(json.dumps(data,ensure_ascii=False))
