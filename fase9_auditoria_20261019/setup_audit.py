"""Bounded Fase9 audit; preserve older specs, data gates and results."""
from pathlib import Path
import json,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parent
UNIT='F3.AUDITORIA_20261019'
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}
def save(n,d):
    b=(d if isinstance(d,str) else json.dumps(d,ensure_ascii=False,indent=2)).encode('utf-8')
    with (ROOT/n).open('xb') as h:h.write(b)
def cmd(n,args):
    r=subprocess.run(args,text=True,encoding='utf-8',capture_output=True)
    save(n+'.json',{'cmd':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    return r.stdout
def mem(n,q):
    r=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(q),text=True,encoding='utf-8',capture_output=True)
    j=json.loads(r.stdout);save(n+'.json',j)
    if r.returncode or not j.get('ok'):raise RuntimeError(j)
    return j['result']
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
if __name__=='__main__':
    save('OPERADOR.txt','Prossiga com a auditoria da Fase 9, reaproveite o que já temos e veja o que falta corrigir nas sistemáticas e na execução para sabermos se conseguimos alcançar os 5 sigma, sem ajustar parâmetros ao dado.')
    for u in ['F3.1','F3.2']:
        cmd('NOS_'+u.replace('.','_'),[sys.executable,'-B','-X','utf8',r'C:\IALD\NOS_VIVO\consultar.py','--unidade',u])
        cmd('BOARD_'+u.replace('.','_'),[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',u])
    cmd('MAP_BEFORE',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','fase9'])
    save('UNIT.json',[{'id':UNIT,'frente':'F3','titulo':'Auditoria de suficiência da Fase9: sistemáticas, execução e poder sem ajuste','dono':ACTOR['id'],'status':'PRONTA','gate':'Somente auditoria e verificações sintéticas/precisão; abertura V2 e d72 não incluídas','criterio_de_fechado':'Matriz de correções satisfeitas/pendentes com fontes e hashes; executor vigente versus especificação; significado de5sigma/poder; próximos passos sem ajuste ou novo composto observado; revisão independente','ordem_fonte':str(ROOT/'OPERADOR.txt'),'reaproveitamento':'F3.1 R5.2/E1; F3.2 E1bytes/harnessportátil; auditorias c1 de08out; Fase9V1 histórico. Novoescopo19out: consolidar suficiência e impedimentos, sem reabrir unidades encerradas.'}])
    cmd('NEW',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','nova','--json',str(ROOT/'UNIT.json'),'--quem',ACTOR['id']])
    cmd('CLAIM',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Auditoria autorizada pelo operador19out, arquivos novos em work/fase9_auditoria_20261019. ReusoF3.1/F3.2, verificação sintética semobservado/d72/freeze/Bancada. Memórias previstas: TGL_ATLAS.md,TGL_INDICE_VIVO.md,DIARIO_CONSTRUCAO_QG.md combackups.'])
    r=mem('INIT',{'operation':'init','objective_file':str(ROOT/'OPERADOR.txt'),'objective_sha256':pin(ROOT/'OPERADOR.txt')['sha256'],'request_id':'fase9-audit-20261019-codex-gerente-tgl','scope':{'house':'IALD','principal':'luiz-antonio-rotoli-miguel'},'actor':ACTOR,'write_reference':str(ROOT/'SESSION_REFERENCE.json'),'constraints':{'unit':UNIT,'no_observed_composition':True,'no_production_write':True,'beta_fixed':True,'older_evidence_immutable':True}})
    print(json.dumps(r,ensure_ascii=False))
