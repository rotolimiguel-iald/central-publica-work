"""Register the locally completed addendum; no provider or scientific execution."""
import datetime as dt
import json
import subprocess
from diary_r1 import ROOT, WORK, PY, CLI, WHO, new

DEST = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA/TETELESTAI_20261014'


def call(args, name=None, payload=None):
    if name and (DEST/name).exists():
        saved = json.loads((DEST/name).read_text(encoding='utf-8'))
        assert saved['exit_code'] == 0, 'Inspect failed receipt before retry'
        return saved['result']
    cp = subprocess.run([PY, '-B', '-X', 'utf8', *map(str,args)],
        input=None if payload is None else json.dumps(payload,ensure_ascii=False),
        capture_output=True, text=True, encoding='utf-8')
    try:
        result = json.loads(cp.stdout)
    except json.JSONDecodeError:
        result = {'stdout':cp.stdout}
    if name:
        new(DEST/name, {'exit_code':cp.returncode, 'result':result, 'stderr':cp.stderr})
    if cp.returncode:
        raise RuntimeError(cp.stderr or cp.stdout)
    return result


def main():
    claim = call([CLI,'ver','F1.REGRA'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    mapped = call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',DEST/'MAP_ENTRY.json','--quem',WHO+' / F1.REGRA'], 'MAP_RECEIPT.json')
    board = call([CLI,'avancar','F1.REGRA','--quem',WHO,'--status','ENTREGUE','--evidencia',DEST/'RESULTADO_ADENDO.json','--nota','Adendo humano: exclusao no Tetelestai; verbatim, fontes e memoria com backup sob reivindicacao780.'], 'BOARD_RECEIPT.json')
    memory = call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_RECEIPT.json',
        json.loads((DEST/'ACOM_TRANSITION.json').read_text(encoding='utf-8')))
    released = call([CLI,'liberar','F1.REGRA','--quem',WHO,'--nota','Adendo documental entregue; memoria aditiva registrada; sem nova prova cientifica.'], 'RELEASE.json')
    print(json.dumps({'map':mapped,'board':board,'acom_ok':memory.get('ok'),'release':released},ensure_ascii=False))


if __name__ == '__main__':
    main()
