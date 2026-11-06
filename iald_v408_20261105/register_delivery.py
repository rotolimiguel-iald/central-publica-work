"""Register the completed app release in its own mission and route map."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import task

def main():
    w=task.W
    handoff=w/'007_RESULTADO.json'
    doc=json.loads(handoff.read_bytes())
    assert doc['estado']=='cumprida'
    source={'kind':'artifact','ref':str(handoff),'sha256':hashlib.sha256(handoff.read_bytes()).hexdigest()}
    change={'records':[{'id':'f_app_v408_installed','kind':'fact','statute':'REAL',
                        'text':doc['resumo'],'sources':[source]}],
            'flow':{'phase':'entregue','next_action':'Gerência confere o recibo de custódia integrado.','handles':[]}}
    file=w/'FINAL_CHANGES.json'
    task.new(file.name,change)
    current=task.call({'operation':'project','reference':str(task.REF)},False)
    receipt=task.call({'operation':'transition','reference':str(task.REF),'expected_revision':current['receipt']['revision'],
                       'event_id':'v408-final-delivery','actor':{'id':task.OWNER,'kind':'agent'},
                       'changes_file':str(file),'changes_sha256':hashlib.sha256(file.read_bytes()).hexdigest()},False)
    if 'receipt' in receipt:
        receipt = receipt['receipt']
    assert receipt['event_id'] == 'v408-final-delivery'
    task.new('FINAL_ACOM.json',receipt)
    subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',task.UNIT,
                    '--quem',task.OWNER,'--status','ENTREGUE','--evidencia',str(handoff)],check=True)
    route={'tipo':'ROTA','rota_id':'app.release.v408','titulo':'Memória científica v408 no app, JEV e fila',
           'dominio':'APP','estatuto':'REAL','status':'EXAMINADA','resultado':doc['resumo'],
           'metodo':'Reconstrução independente dos trechos e enunciados, testes de continuidade e implantação em janela ociosa.',
           'artefatos':[str(handoff),str(w/'LICOES_v408.md')],'refs':['app.release.v407']}
    file=w/'ROTA.json'
    task.new(file.name,route)
    subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(file),'--quem',task.OWNER],check=True)

if __name__=='__main__':
    main()
