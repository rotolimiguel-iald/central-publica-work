"""Additive delivery, memory custody, map and programme registration."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys
from datetime import datetime,timezone
from prepare import ROOT,PARENT,CORE,REF,ACTOR,TASK,OUT,new,pin,source,project,call

CENTRAL=PARENT.parent.parent
UNIT='F9.MEMORIA_MISSAO_20261016'
BOARD=Path(r'C:\IALD\PROGRAMA_IALD\iald.py')

def command(args,name):
    r=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    try:j=json.loads(r.stdout)
    except ValueError:j={'text':r.stdout}
    new(name+'.json',{'command':list(map(str,args)),'exit_code':r.returncode,'result':j,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(j)
    return j

def main():
    p=project('FINAL_CURRENT')
    accepted=next(t for t in p['projection']['settled'] if t['id']==TASK)
    assert accepted['status']=='satisfied' and accepted['reviewed_by']!=ACTOR['id']
    board=command([BOARD,'ver',UNIT],'CLAIM_CHECK')
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id'] and 'DIARIO_CONSTRUCAO_QG.md' in claim['nota']
    assert datetime.fromisoformat(claim['vence_em'])>datetime.now(timezone.utc)
    deployment=json.loads((ROOT/'DEPLOYMENT_E1.json').read_bytes())
    for row in deployment['files']:
        assert pin(row['target'])['sha256']==row['new_sha256']
        assert pin(row['backup']['path'])['sha256']==row['old_sha256']
    names=['FINDING.json','mission_bridge_candidate.py','PROTOCOL_ADDENDUM.md','verify.py','verify_synthetic.py',
           'VERIFICATION_CANDIDATE.json','SYNTHETIC_MCP.json','REVIEW_E1.json','DEPLOYMENT_E1.json',
           'VERIFICATION_INSTALLED.json','REVIEW_INSTALLED_E1.json','ACCEPT_E1_RECEIPT.json','ENVIRONMENT_NOTE.json']
    evidence=[pin(ROOT/n) for n in names]
    delivery=new('DELIVERY_E1.json',{'unit':UNIT,'author':ACTOR['id'],'at':datetime.now(timezone.utc).isoformat(),
        'statute':'REAL','status':'INSTALLED_INDEPENDENTLY_ACCEPTED','requirement':TASK,
        'mission_revision':p['receipt']['revision'],'reference':pin(REF),'technical_reviewer':accepted['reviewed_by'],
        'claim':claim,'evidence':evidence,'runtime':'Actual MCP new process; no existing process restarted.',
        'measurements':{'real_mission_chars':41660,'synthetic_chars':40191,'synthetic_requirements':8,
                        'negative_cases':4,'installed_targets':2},
        'limits':['Consumers must use the protocol; old processes were not reloaded.',
                  'No measured percentage of token savings; no Lindblad operation in model weights.',
                  'Scientific requirements and pending external handles remain open. No gate change.']})
    text='''\n\n## 16/10/2026 — Repasse da missão extensa pelo MCP corrigido
<!-- mission_handoff_capacity_e1_20261016 -->

[REAL — codex-gerente-tgl; reivindicação 904 em F9.MEMORIA_MISSAO_20261016]
A missão cresceu além do padrão de 24000 caracteres; o MCP de handoff não expunha a capacidade que sync já aceitava. A recusa foi reproduzida sem truncamento. Corrigidos somente o parâmetro max_chars e seu repasse ao controlador existente; protocolo recebeu adendo com backup de bytes. Quatro ferramentas e guardas de revisão, posse, dependências e integralidade preservadas.

[REAL] Teste da missão real com 41660 caracteres e sintético com 40191/8 requisitos: a projeção de handoff é integralmente igual à de sync. Quatro controles recusaram orçamento padrão insuficiente, um caractere a menos, orçamento inválido e revisão antiga. MCP instalado conferido em processo novo; revisão independente aceitou M1_HANDOFF_CAPACITY. As instruções globais AGENTS/CLAUDE já apontam para este protocolo; não foram reescritas neste complemento.

[ESCOPO] Clientes precisam sincronizar antes da ação e da integração; processos antigos não foram recarregados. Preservação da inscrição, evolução por revisão e PODA são controles operacionais. Não se afirma Lindblad nos pesos, memória infalível ou redução percentual de tokens medida. Nenhum um.py, kernel, Bancada, dado ou gate alterado. Os critérios científicos continuam separados.

Evidência: '''+str(delivery)+''' . Referência única: '''+str(REF)+''' .
'''
    new('MEMORY_ADDITION_E1.txt',text.encode('utf-8'))
    spec=importlib.util.spec_from_file_location('memory_append',CENTRAL/'work/rede_quantica_20261013/diary_r1.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    surfaces=[CENTRAL/'memory/DIARIO_CONSTRUCAO_QG.md',CENTRAL/'memory/TGL_ATLAS.md',
        CENTRAL/'memory/TGL_INDICE_VIVO.md',OUT.parent/'AVISO_GERENCIA.md']
    rows=[]
    for i,surface in enumerate(surfaces,1):
        row=module.append_bytes(surface,text,'mission_handoff_capacity_e1_20261016')
        rows.append(row);new(f'MEMORY_APPEND_E1_{i}.json',row)
    memories=new('MEMORY_E1.json',{'unit':UNIT,'claim':claim,'surfaces':rows,'append_only':True})
    entry={'tipo':'ROTA','rota_id':'infra.memoria_missao.ancoragem_e_poda_20261016','dominio':'INFRAESTRUTURA',
        'titulo':'Missão ancorada: repasse MCP acompanha o crescimento do estado',
        'pergunta':'O agente consegue receber a projeção integral atual quando a missão ultrapassa 24 mil caracteres?',
        'dados':[],'metodo':'Reprodução local, alteração mínima, missão real/sintética por MCP, revisão independente e instalação por hash.',
        'resultado':'Handoff=sync em 41660 caracteres reais e 40191 sintéticos; 4 recusas preservadas; M1 aceito independentemente.',
        'veredito':'INSTALLED_AND_INDEPENDENTLY_ACCEPTED','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Clientes legados precisam aderir/recarregar. Ganho percentual de tokens não medido; memória não é infalível.',
        'nao_refazer':'Reutilizar as quatro ferramentas e a referência exata. Passar a mesma capacidade explícita a sync e handoff; não truncar nem refazer entregas já satisfeitas.',
        'proximo_passo':'Retomar somente os resíduos científicos atuais após sincronizar; não reconstruir memória nem critérios já aceitos.',
        'onde':str(CORE/'MISSION_PROTOCOL.md'),'artefatos':[str(delivery),str(memories),str(ROOT/'ACCEPT_E1_RECEIPT.json')],
        'refs':['infra.memoria_missao.ancoragem_e_poda_20261016'],
        'nota':'Complemento material ao mapa 1162, em nome de codex-gerente-tgl; nenhuma alteração de gate.'}
    entry_path=new('MAP_ENTRY_E1.json',entry)
    mapped=command([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry_path,'--quem',ACTOR['id']],'MAP_RECEIPT_E1')
    command([BOARD,'avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',delivery,memories,
        ROOT/'MAP_RECEIPT_E1.json',ROOT/'ACCEPT_E1_RECEIPT.json','--nota',
        'Complemento MCP grande instalado e aceito independentemente; sem reiniciar sessões, sem ciência/gate. Quatro memórias com backup.'],'BOARD_DELIVERY_E1')
    p=project('BEFORE_FINAL_FLOW')
    record={'id':'memory-e1-delivered','kind':'fact','statute':'REAL',
        'text':'Memory correction delivered: explicit MCP handoff capacity, real/synthetic large mission verified, independent technical acceptance, additive map/board/memories. Existing science requirements preserved; resume only current residues.',
        'sources':[source(delivery),source(memories),source(ROOT/'MAP_RECEIPT_E1.json')]}
    call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'event_id':'memory-e1-delivered',
        'changes':{'records':[record],'flow':{'phase':'memory_correction_delivered',
        'next_action':'Project exact mission; continue R4/R5/R7/R8 residues with preflight. R7 R11 handle already running; prefix probe complete. Final R3/R10 await dependencies.'}}},'FINAL_FLOW')
    call('session_memory.py',{'operation':'verify','reference':str(REF)},'FINAL_VERIFY')
    own_ref=PARENT/'ACOM_REFERENCE.json'
    own=call('session_memory.py',{'operation':'project','reference':str(own_ref),'max_chars':100000},'OWN_CURRENT')
    call('session_memory.py',{'operation':'transition','reference':str(own_ref),'actor':ACTOR,
        'expected_revision':own['receipt']['revision'],'event_id':'memory-e1-delivered',
        'changes':{'records':[record],'flow':{'phase':'handoff_correction_delivered',
        'next_action':'Current mission reference carries scientific progress; memory unit awaits programme review.'}}},'OWN_FINAL_FLOW')
    command([BOARD,'liberar',UNIT,'--quem',ACTOR['id'],'--nota','Complemento E1 entregue, memória registrada sob reivindicação904.'],'BOARD_RELEASE_E1')
    new('FINAL_E1.json',{'ok':True,'unit':UNIT,'delivery':pin(delivery),'memory':pin(memories),
        'map':pin(ROOT/'MAP_RECEIPT_E1.json'),'board':pin(ROOT/'BOARD_DELIVERY_E1.json'),
        'acceptance':pin(ROOT/'ACCEPT_E1_RECEIPT.json'),'claim_released':True})
    print(json.dumps({'ok':True,'unit':UNIT,'map':mapped,'delivery':str(delivery)},ensure_ascii=False))

if __name__=='__main__':main()
