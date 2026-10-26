"""Submit the bounded source investigation; approval/integration remain management acts."""
from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import task
B=Path(__file__).resolve().parent
D=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025\FONTES_FISICAS')

def new(n,d):
    with (B/n).open('xb') as f:f.write(json.dumps(d,ensure_ascii=False,indent=2).encode())

def board(args):
    p=subprocess.run([task.PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True)
    if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
    r=json.loads(p.stdout);assert r['ok'];return r

def main():
    for n in ['SUBMIT.json','BOARD_DELIVERY.json','MEMORY.json','BOARD_RELEASE.json','MEMORY_VERIFY.json']:
        if (B/n).exists():raise FileExistsError(B/n)
    p=task.project();t=next(x for x in p['projection']['active'] if x['id']=='physical_sources')
    assert task.act('check',task_id=t['id'],lease_id=t['lease']['id'])['ready']
    final=D/'RESULTADO_FONTES_FISICAS.json';review=D/'REVIEW_PHYSICAL_SOURCES.json'
    result=json.loads(final.read_text(encoding='utf-8'))
    for s in result['files']:
        assert task.pin(Path(s['path']))['sha256']==s['sha256']
    new('SUBMIT.json',task.act('submit',task_id=t['id'],lease_id=t['lease']['id'],
         evidence=[task.pin(final),task.pin(review)],event_id='o25-physical-sources-submit'))
    b=board(['avancar',task.UNIT,'--quem',task.OWNER,'--status','ENTREGUE','--evidencia',str(final),str(D/'RESULTADO.md'),
             '--nota','Fornecedores autorais de massa/Clausius recuperados:66 fontes, contratos e limites, revisão independente documental. Ponte parcial; nenhum build/provedor/original/gate alterado. Gerência registra mapa e decide integração.'])
    new('BOARD_DELIVERY.json',b)
    p=task.call({'operation':'project','reference':str(task.REF),'max_chars':100000},False)
    new('MEMORY.json',task.call({'operation':'transition','reference':str(task.REF),
      'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],
      'event_id':'o25-physical-sources-material',
      'changes':{'records':[{'id':'o25-physical-sources-reuse','kind':'fact','statute':'DERIVED',
        'text':'Levantamento dirigido de66fontes conferido/revisado. Calor do boost e H3 em família plane-wave já construídos; não registrar ausência genérica. Massa por energia confinada, potenciais e clock/Gauss exige dados físicos; normalização do clock não seleciona fluxo/amplitude. Gibbs finito v394 conservado na v401 fixa Eref no estado/clock fornecidos, não kappa físico. R84-R90 e R13-R16 reutilizados. Falta fornecedor simultâneo do mesmo estado/campo, massa/carga normalizada, T completo conservado e área universal; contrato concreto anexado. M11Chandrasekhar corrigido pela retirada explícita no artigo. Nenhuma nova prova Lean, dado/sigma ou confirmação física. Gerência ainda examina/registra mapa; não repetir essas provas/inventários sem fonte nova.',
        'sources':[{'kind':'artifact','ref':str(final),'sha256':task.pin(final)['sha256']},
                   {'kind':'artifact','ref':str(review),'sha256':task.pin(review)['sha256']}]}],
        'flow':{'phase':'physical_sources_delivered_awaiting_management',
                'next_action':'Reutilizar contrato FONTES_FISICAS: construir fornecedor único e delimitado de estado/fonte/carga/área ou nova subfamília física. Não repetir escala/E=mc2/calor/plane-wave/R84-R90; gerência examina e registra mapa.'}}},False))
    new('BOARD_RELEASE.json',board(['liberar',task.UNIT,'--quem',task.OWNER,
                                 '--nota','Camada fontes físicas entregue; análise e integração são da gerência.']))
    verify=task.call({'operation':'verify','reference':str(task.REF)},False)
    new('MEMORY_VERIFY.json',verify)
    print(json.dumps({'board':b.get('evento'),'evidence':task.pin(final),
        'revision':task.project()['receipt']['revision'],'memory_verified':verify},ensure_ascii=False))

if __name__=='__main__':main()
