"""Register the requested Claude handoff; no scientific execution or installation."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT,WORK,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as reg

BASE=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'
OUT=BASE/'F1.REGRA.MOTOR/ENCAMINHAMENTO_V393_20261014'
UNIT='F1.REGRA.MOTOR'

def main():
    reg.DEST=OUT
    assert not (OUT/'RESULTADO_ENCAMINHAMENTO.json').exists(), 'Recover existing delivery; do not duplicate.'
    claim=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert claim['quem']==WHO and 'AVISO_GERENCIA.md' in claim['nota']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    packet=json.loads((OUT/'PACOTE_FONTES.json').read_bytes())
    for item in packet['sources']+[packet['message'],packet['operator_order']]:
        assert pin(Path(item['path']))['sha256']==item['sha256'],item['path']
    msg=Path(packet['message']['path'])
    result=OUT/'RESULTADO_ENCAMINHAMENTO.json'
    new(result,{'unit':UNIT,'destination':'Claude Code / gerencia c1','requested_integration':'um.py v393',
        'status':'ENTREGUE_NO_TUNEL_OFICIAL','recipient_read_receipt':False,'canonical_integration_performed':False,
        'operator_order':packet['operator_order'],'message':pin(msg),'source_package':pin(OUT/'PACOTE_FONTES.json'),
        'source_hashes_verified':True,'claim':claim,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    marker='rule_v393_handoff_20261014'
    note=f'''\n\n## 14/10/2026 — Ordem de integrar a regra na v393, encaminhada ao Claude
<!-- {marker} -->

Em nome de codex-gerente-tgl, sob reivindicação de F1.REGRA.MOTOR.
[INPUT — operador] “transmita para o claude o que fizemos também sobre a prova da "regra" e seu conceito isso também precisa entrar no um.py na v 393”. Verbatim e hash no pacote.
[REAL — entrega documental] As quatro cunhagens integrais, F1.REGRA.P1 (60 teoremas), ponte F1.REGRA.MOTOR (42 novos; 22 reutilizados), execução sintética (76 verificações / 241 pontos), fontes e revisões foram reunidas no canal oficial de entrega à gerência Claude c1. Correção/completude, leitura fiel em Fix(R), alvo fixado, estado bruto versus inscrição, dimensão fixa oito e resíduo binário da P1 permanecem explícitos. Não refazer as provas; integrar e auditar na cadeia v393.
Mensagem: `{msg}`; SHA256 `{pin(msg)['sha256']}`.
Resultado: `{result}`; SHA256 `{pin(result)['sha256']}`.
Integração canônica e leitura pelo destinatário ainda não atestadas. Este encaminhamento não executa provedor, não muda programa/kernel/Bancada nem gate.
'''
    paths=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',BASE/'AVISO_GERENCIA.md']
    new(OUT/'MEMORY_RECEIPT.json',{'claim':claim,'surfaces':[append_bytes(p,note,marker) for p in paths]})
    entry=OUT/'MAP_ENTRY.json'
    new(entry,{'tipo':'ROTA','rota_id':'formal.regra.integracao_v393','dominio':'FORMAL',
        'titulo':'Ordem do operador: conceito e prova da regra para integrar na v393',
        'pergunta':'Qual pacote deve a gerencia Claude reaproveitar para integrar a regra na v393?',
        'dados':['Quatro cunhagens verbatim','Prova P1 e ponte MOTOR verificadas anteriormente','Ordem humana atual de transmissao'],
        'metodo':'Releitura dos recibos, conferencia dos hashes e entrega no tunel/quadro com memoria sob reivindicacao.',
        'resultado':'Pacote entregue a gerencia pelo canal oficial; integracao e aceite pendentes.',
        'veredito':'ENCAMINHADO_A_GERENCIA_PARA_V393','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Sem recibo de leitura do destinatario e sem integracao canonica nesta etapa.',
        'nao_refazer':'Reaproveitar F1.REGRA.P1 e F1.REGRA.MOTOR; manter hipoteses e ressalvas.',
        'proximo_passo':'Gerencia recebe, audita e incorpora na cadeia da v393 conforme ordem humana.',
        'onde':str(OUT),'artefatos':[str(msg),str(result),str(OUT/'PACOTE_FONTES.json')],'refs':[1109,1110]})
    mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO+' / ordem v393'],'MAP_RECEIPT.json')
    event=reg.call([CLI,'anotar','--quem',WHO,'--tipo','AVISO_CLAUDE','--unidade',UNIT,'--dados',json.dumps({
        'destinatario':'claude-c1','ordem':'Integrar conceito e prova da regra na v393 por ordem direta do operador.',
        'mensagem':str(msg),'sha256':pin(msg)['sha256'],'resultado':str(result),
        'resumo':'Quatro verbatims; prova 60 teoremas; ponte 42 novos; 76 checks/241 pontos; revisoes e escopo. Reaproveitar sem reconstruir. Integracao nao realizada aqui.',
        'mapa':mapped},ensure_ascii=False)],'BOARD_NOTICE.json')
    board=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',result,
        '--nota','Ordem humana entregue ao Claude pelo tunel, AVISO_GERENCIA e quadro: integrar conceito e prova da regra na v393.'], 'BOARD_DELIVERY.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    projection=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload={'operation':'project','reference':ref})
    assert projection['ok']
    revision=projection['result']['receipt']['revision']
    transition={'operation':'transition','reference':ref,'expected_revision':revision,'event_id':'rule-v393-claude-handoff-20261014',
        'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[
            {'id':'rule-v393-integration-order-20261014','kind':'decision','statute':'INPUT','text':'Operador mandou transmitir ao Claude o conceito e a prova da regra para entrar no um.py v393.',
             'sources':[{'kind':'artifact','ref':packet['operator_order']['path'],'sha256':packet['operator_order']['sha256']}]},
            {'id':'rule-v393-handoff-20261014','kind':'fact','statute':'REAL','text':'Encaminhamento documental entregue no tunel, AVISO_GERENCIA e quadro, com conceitos verbatim, prova P1, ponte MOTOR, fontes e hashes. Leitura pelo destinatario e integracao canonica ainda nao atestadas; fila externa e demais pendencias preservadas.',
             'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [result,msg,OUT/'BOARD_NOTICE.json']]}]}}
    new(OUT/'ACOM_TRANSITION.json',transition)
    acom=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT.json',transition)
    assert acom['ok']
    release=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','Encaminhamento autorizado ao Claude entregue; integracao v393 cabe a gerencia.'],'RELEASE.json')
    print(json.dumps({'message':pin(msg),'board_notice':event,'delivery':board,'map':mapped,'acom_revision':acom['result']['revision'],'release':release},ensure_ascii=False))

if __name__=='__main__':main()
