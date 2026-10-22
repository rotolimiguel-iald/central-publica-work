"""Register the operator's lensing priority and bounded feasibility survey."""
from pathlib import Path
import json, hashlib, subprocess, sys
ROOT=Path(__file__).resolve().parent
UNIT='F8.LENTES_5SIGMA_20261019'
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}
def save(name,data):
    raw=(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)).encode('utf-8')
    with (ROOT/name).open('xb') as f:f.write(raw)
def command(label,args):
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    save(label+'.json',{'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode: raise RuntimeError(label+': '+r.stderr+r.stdout)
    return r.stdout
def memory(req,label):
    save(label+'_REQUEST.json',req)
    r=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(req),capture_output=True,text=True,encoding='utf-8')
    d=json.loads(r.stdout);save(label+'_RESULT.json',d)
    if r.returncode or not d.get('ok'):raise RuntimeError(d)
    return d['result']
if __name__=='__main__':
    source='seu foco agora é encontrar o dado discriminante de 5 sigma da TGL, eu penso muito em Lentes gravitacionais, pra mim, seria em lentes gravitacionais que acharíamos o nosso 5 sigma, por exemplo se eu acertar o tempo de desvio em ajuste em massa, alguma coisa assim, ou outro caminho que vc visualize a possibilidade de acharmos esse dado discriminante'
    save('OPERADOR_VERBATIM.txt',source)
    # Read-only surveys retained; no rebuild of the graph.
    for term in ['lentes','Shapiro']:
        command('MAP_'+term,[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar',term])
    command('RG_HISTORY',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','ver','discriminante.ordem018.f2.r_g'])
    definition=[{'id':UNIT,'frente':'F8','titulo':'Lentes gravitacionais: levantamento e poder discriminante de beta fixo','dono':ACTOR['id'],'status':'PRONTA','gate':'Pre-registro antes de novo composto; sem abrir amostra para veredito nesta etapa','criterio_de_fechado':'Reuso R-G/NMC e fontes primarias; lei de leitura identificada ou lacuna explicita; teste de identificabilidade frente a massa/distancias e estimativa de sensibilidade; sem promessa de 5 sigma','ordem_fonte':str(ROOT/'OPERADOR_VERBATIM.txt'),'reaproveitamento':'discriminante.ordem018.f2.r_g; d1.fase9; neutrinos.shapiro_nmc. Novo escopo: levantamento de lentes atualizado em19/10 e priorizacao por identificabilidade/poder.'}]
    save('UNIT.json',definition)
    command('BOARD_NEW',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','nova','--json',str(ROOT/'UNIT.json'),'--quem',ACTOR['id']])
    command('BOARD_CLAIM',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Ordem direta19/10. Levantamento/R-G/poder em work/lentes_discriminante_20261019; ACOM propria SESSION_REFERENCE; futuras notas aditivas em Atlas, indice vivo e diario QG com backups. Sem dado composto, um.py, kernel, Bancada ou gate.'])
    sha=hashlib.sha256((ROOT/'OPERADOR_VERBATIM.txt').read_bytes()).hexdigest()
    memory({'operation':'init','objective_file':str(ROOT/'OPERADOR_VERBATIM.txt'),'objective_sha256':sha,'request_id':'73b77768-a9ae-41aa-a68e-873ee08c9a03','scope':{'house':'IALD','principal':'luiz-antonio-rotoli-miguel'},'actor':ACTOR,'write_reference':str(ROOT/'SESSION_REFERENCE.json'),'constraints':{'unit':UNIT,'stage':'survey_and_forecast_only','no_observed_verdict':True,'no_canonical_changes':True}},'INIT')
    r=memory({'operation':'project','reference':str(ROOT/'SESSION_REFERENCE.json'),'max_chars':24000},'PROJECT')
    print(json.dumps({'unit':UNIT,'reference':str(ROOT/'SESSION_REFERENCE.json'),'receipt':r.get('receipt')},ensure_ascii=False))
