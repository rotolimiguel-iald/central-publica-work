"""Register the broad completion order without narrowing its scientific scope."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin
import register_rule_tetelestai as reg

UNIT = 'F1.FECHO_20261015'
OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT
ORDER = 'conclua você tudo que falta, por favor'
STEERING = 'Já tem muita coisa construída da rede, muita'
reg.DEST = OUT

def main():
    unit = {'id': UNIT, 'frente': 'F1', 'titulo': 'Fecho por reaproveitamento: regra quadratica, rito integral v394 e realizacao conjunta da rede',
            'dono': WHO, 'status': 'PROPOSTA', 'dependencias': ['F1.TEMPO.V394', 'F1.REDE', 'F1.TAKESAKI'],
            'criterio': 'Cumprir integralmente a ordem de conclusao: auditar realizacoes existentes; completar contrato quadratico e seu consumidor; executar main/rito completo em copia; ligar parametros ao objeto fisico nomeado; completar realizacao conjunta de rede/Poincare/localizacao, algebra de campos Fock/modular, Takesaki e Maxwell; explicitar e verificar alcance de H3 sem introduzir sua conclusao como hipotese disfarçada. Aceite somente por evidencias por requisito. Nao substituir o alvo global por modelo finito ou entrega documental.',
            'escopo': 'Copias novas no tunel, provas Lean e sintese verificada, orquestracao nas identidades existentes. Sem editar originais pinados, kernel do Nos, programa canonico, Bancada produtiva, dados observados, gate ou publicar. Memoria sob claim com backups. Ato de ratificacao c1 permanece distinto de construcao.',
            'fonte': ORDER+' / '+STEERING,
            'reaproveitamento_previo': 'F1.TEMPO.V394 R2 entregue mapa1123:108declaracoes,7153/7153,5716checks; F1.REDE possui Fubini/H1/modular/Fock cinematico; F1.2 V351 e F2.3 Einstein condicional fechadas. Consultar fontes recentes para nao reabrir ausencias historicas.'}
    saved=json.loads((OUT/'CLAIM_RECEIPT.json').read_bytes())
    created,claimed=saved['created'],saved['claimed']
    actual=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert actual['quem']==WHO and dt.datetime.fromisoformat(actual['vence_em'])>dt.datetime.now(dt.timezone.utc)
    # Prior refusal is preserved: the new unit is not yet in the read-only graph.
    reg.call([r'C:\IALD\NOS_VIVO\consultar.py', '--unidade', 'F1.REDE'], 'NOS_VIVO_REDE.json')
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'consultar', 'rede'], 'MAPA_REDE_ANTES.json')
    requirements = [
      ('R1', 'Reaproveitar toda construcao recente pertinente e corrigir pendencias historicas', 'Inventario por fontes/linhas/hashes: ligado, existente sem ligacao, conhecido, aberto.'),
      ('R2', 'Contrato quadratico da correspondencia', 'Lean: residuo nulo iff leitura=ancora, invariancia no fluxo e controles; consumidor usa prova e fontes.'),
      ('R3', 'Rito integral da candidata v394', 'Main completo na copia, kernel/consumidores/artigos/saidas e recibos; nenhum baseline substitui execucao atual.'),
      ('R4', 'Ligacao fisica do espectro e relogio', 'Estado/objeto fisico nomeado, unidades, V0/Eref/kappa e ponte ao mesmo sistema; dominios explicitos.'),
      ('R5', 'Rede global e realizacao do dispositivo', 'Representacao Poincare/localizacao e entrelacamento pertinente, com a construcao existente reutilizada.'),
      ('R6', 'Algebra de campos na mesma realizacao Fock', 'Weyl/CCR/R(K), vacuum standard, Gamma(J) e modularidade ligados no mesmo espaco.'),
      ('R7', 'Takesaki na representacao pretendida', 'Produto cruzado, acao/peso/traco entrelacados por termos ou derivacao identificada; escalaV351 reutilizada.'),
      ('R8', 'Realizacao conjunta de Maxwell e tensor de materia', 'Campos do certificado completo nao triviais na mesma rede; simetria/conservacao e fonte geometrica ligados.'),
      ('R9', 'Alcance fisico de H3 em todas as direcoes', 'Classificar hipotese conhecida vs consequencia demonstrada; nao assumir o antecedente como prova de derivacao.'),
      ('R10', 'Revisao independente e entrega conjunta', 'Cada requisito conferido contra fonte atual; ratificacao da c1 distinta; nenhuma proclamacao global sem evidencia.')]
    new(OUT/'REQUISITOS_ORIGINAIS_R1.json', {'unit':UNIT,'objective':ORDER,'steering':STEERING,
         'requirements':[{'id':i,'requirement':q,'acceptance_evidence':e,'status':'TO_VERIFY_OR_COMPLETE'} for i,q,e in requirements],
         'rule':'Escopo original preservado. Estado incompleto nao fecha a meta.'})
    notice = {'ordem':ORDER, 'correcao':STEERING, 'pasta':str(OUT),
              'escopo':'Nova continuidade por ordem do operador: reaproveitar fontes e concluir os requisitos globais, mantendo v394 R2 pinada. Nenhuma escrita de producao.'}
    reg.call([CLI,'anotar','--quem',WHO,'--tipo','AVISO_CLAUDE','--unidade',UNIT,'--dados',json.dumps(notice,ensure_ascii=False)],'NOTICE_START.json')
    payload = {'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':28,
        'event_id':'full_completion_order_20261015','actor':{'id':WHO,'kind':'agent'},'changes':{
            'records':[{'id':'full-completion-order-20261015','kind':'decision','statute':'INPUT','text':ORDER+'\n'+STEERING,
                        'sources':[{'kind':'artifact','ref':str(OUT/'OPERADOR_CONCLUSAO_VERBATIM.txt'),'sha256':pin(OUT/'OPERADOR_CONCLUSAO_VERBATIM.txt')['sha256']},
                                   {'kind':'artifact','ref':str(OUT/'REQUISITOS_ORIGINAIS_R1.json'),'sha256':pin(OUT/'REQUISITOS_ORIGINAIS_R1.json')['sha256']}]}],
            'flow':{'phase':'full_completion_inventory_and_construction','next_action':'Reaproveitar rede existente; contrato quadratico e rito integral em copias; completar R1-R10 sem reduzir objetivo. Preservar identidades dos jobs anteriores.'}}}
    new(OUT/'ACOM_START_REQUEST.json',payload)
    acom=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_START_RECEIPT.json',payload)
    print(json.dumps({'unit':UNIT,'claim':claimed,'acom_ok':acom.get('ok'),'out':str(OUT)},ensure_ascii=False))

if __name__=='__main__':main()
