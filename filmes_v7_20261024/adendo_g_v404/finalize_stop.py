"""Publish only the local stop receipt; never audio, video or public website."""
import json
import subprocess
from inspect_audio_scope import *
from bootstrap import cli


def run_cli(name, command):
    r = subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',*command],capture_output=True,text=True,encoding='utf-8')
    create(G/name,{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)


def main():
    assert not (T/'RESULTADO.json').exists(),'Recover existing receipt; do not repeat transitions'
    review_path=G/'INDEPENDENT_AUDIO_SCOPE_REVIEW.json'
    review=read(review_path)
    assert str(review['verdict']).startswith('PASS'),review
    p=mission.call({'operation':'project','max_chars':350000})
    task=next(t for t in p['projection']['active'] if t['id']=='ADENDO_G_V404')
    check=mission.call({'operation':'check',**current(),'task_id':task['id'],'lease_id':task['lease']['id'],'max_chars':350000})
    assert check['ready']
    create(G/'FINAL_PREFLIGHT.json',check)
    result=read(G/'AUDIO_SCOPE_CHECK.json')
    assert result['status']=='STOP_ADDITIONAL_TTS_REQUIRES_AUTHORIZATION'
    for key in ('public_pointer','public_manifest'):assert pin(Path(result[key]['path']))==result[key]
    intake=read(G/'SOURCE_INTAKE.json')
    for key in ('program','seal','core'):assert pin(Path(intake[key]['path']))==intake[key],'Source advanced; update stop reason'
    assert read(N/'um_absoluto_selo.json')['um_version']=='v404'
    result.update({'independent_review':pin(review_path),'origin_verified':pin(G/'ORIGIN_VERIFIED.json'),'source_unchanged_before_delivery':True,'local_diagnostics':pin(G/'LOCAL_DIAGNOSTICS_R1.json'),'delivery_scope':'Parada prévia por duas sínteses adicionais não abrangidas pelo Adendo G. Não é entrega de render v404 nem aceite final.','required_decision':'Gerência decide a inclusão de film1/return/cue0 PT e EN no escopo TTS, ou outro encaminhamento explícito. Não executar áudio/render antes.','previous_stop_resolution':'As duas frases do gate do Adendo F foram decididas pelo G; a nova parada é distinta e se refere à escada na cena return.'})
    create(T/'RESULTADO.json',result)
    create(G/'FINAL_STOP_DELIVERY.json',result)
    extra={u['language']:u for u in result['additional_new_units']}
    lines=[
        '# ORDEM 022 — ADENDO G: duas sínteses adicionais antes da v404',
        '[REAL] STOP_ADDITIONAL_TTS_REQUIRES_AUTHORIZATION; a decisão das frases do gate foi recebida e conferida.',
        '[REAL] Fonte v404 lida sem executar/importar um.py: escada 9698/9698, 1438 arquivos formais, 29484 declarações; gate 18 calculadas/0 literais, 15 lidas pelo veredito.',
        '[REAL] Inventário completo de fala: 58 unidades únicas/76 ocorrências; 52 reutilizáveis, 4 novas autorizadas e 2 novas fora do escopo. Nenhuma das seis está no cache concluído.',
        'As quatro autorizadas são film1/horizon/cue1 e film2/einstein/cue1, em português e inglês; textos verbatim do Adendo G.',
        'Adicionais: film1/return/cue0, cena 168–192s, somente troca dinâmica de 9679 por 9698. Não é o início exato do áudio da fala.',
        'PT (122 caracteres): '+extra['pt-BR']['text'],
        'EN (114 caracteres): '+extra['en']['text'],
        '[DERIVED — estimativa] Cobrança direta incremental esperada: US$0 pelas duas adicionais e US$0 pelas seis novas, usando o transporte Edge já existente.',
        'Não é tarifa/cotação/fatura oficial Microsoft; custo local de máquina, energia e assinaturas não medido. Base e fontes no RESULTADO.json.',
        '[REAL] Zero novas chamadas TTS, zero render, zero publicação. Filmes, ponteiro e manifesto v402 preservados.',
        '[REAL] Conferidos 12 textos alterados: 8 verbatim autorizados e 4 traduções da mesma contagem no retorno; revisão independente pinada no resultado.',
        '[OPEN] Comparação integral dos demais números e render v404 não iniciados após a parada de escopo; não se declara v404 pronta.',
        '[OPEN] Gerência deve decidir as duas unidades adicionais antes do áudio/render, conforme item 2 do Adendo G. O aceite editorial anterior permanece.',
        'PUBLIC_DELIVERY_V7.json não reemitido: não existe render v404 concluído nesta etapa. Integração/publicação continuam com a gerência após custódia.',
        'Recibos, fontes, cache e custos no RESULTADO.json; referência ACOM própria preservada. Nenhuma alteração científica ou do gate.'
    ]
    assert len(lines)<=20
    create(T/'RELATORIO.md','\n'.join(lines)+'\n')
    create(G/'MEMORY_DEPOSIT_TEXT.txt','[REAL] Adendo G decide as duas frases do gate e determina render v404 com somente quatro novas unidades TTS. Inventário local revisado encontrou outras duas: film1/return/cue0 PT/EN, 122/114 caracteres, troca dinâmica da escada9679→9698; sem áudio correspondente no cache. Total58únicas/76ocorrências,52reutilizáveis e6novas. [DERIVED] Cobrança direta estimada US$0 pelas duas adicionais e pelo conjunto das seis, no transporte Edge existente; não é cotação/fatura oficial ou custo de máquina, que não foi medido. [REAL] Parada explícita antes de qualquer nova síntese/render/importação de um.py/publicação. Ponteiro e filmesv402 preservados; fonte v404 conferida. [OPEN] Gerência decide as duas adicionais; demais números ainda não integralmente comparados. A parada anterior do F sobre redação do gate foi resolvida pelo G, e o aceite editorial anterior permanece.\n')
    sources=[{'path':str(T/'RESULTADO.json'),'sha256':pin(T/'RESULTADO.json')['sha256']},{'path':str(ORDER),'sha256':pin(ORDER)['sha256']}]
    blocked=mission.call({'operation':'block',**current(),'task_id':task['id'],'reason':'Adendo G item2: film1/return/cue0 PT/EN exige duas novas sínteses fora das quatro autorizadas. Escada9679→9698; cache ausente. Informados textos e estimativa de cobrança diretaUS$0 antes de qualquer TTS/render.','sources':sources,'event_id':REQUEST+'-extra-tts-stop'})
    create(G/'MISSION_BLOCKED.json',blocked)
    state=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'get','reference':str(REF)})['result']
    tr=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':REQUEST+'-stop-delivery','changes':{'records':[{'id':'v404_adendo_g_extra_tts_stop','kind':'fact','statute':'REAL','text':'G resolveu a redação do gate do F, mas exige parada por qualquer TTS adicional. Inventário revisado:52/58 unidades reutilizáveis;4 novas autorizadas;2 extras film1/return/cue0 PT/EN pela escada9679→9698,122/114caracteres, sem cache. Cobrança direta estimadaUS$0, não tarifa/fatura/custo de máquina. Zero TTS/render/importação de um.py/publicação; v402 preservada. Demais números não comparados integralmente. Gerência decide extras antes de executar.','sources':[{'kind':'artifact','ref':str(T/'RESULTADO.json'),'sha256':pin(T/'RESULTADO.json')['sha256']}]}],'flow':{'phase':'v404_stopped_additional_tts_management_decision','next_action':'Gerência lê ADENDO_G/RESULTADO.json e decide as duas unidades adicionais film1/return/cue0 PT/EN. Depois conferir selo, comparar demais números e executar apenas unidades autorizadas e único render v404. Não renderizar v403 nem repetir chamadas encerradas.'}}})
    assert tr['ok'];create(G/'STOP_DELIVERY_ACOM.json',tr)
    route={'tipo':'RESULTADO','rota_id':'site.filmes.v7.ordem022','dominio':'SITE_E_PUBLICACAO','titulo':'Adendo G v404: parada por duas falas adicionais da escada','resultado':'52 unidades reutilizáveis,4 novas autorizadas,2 novas adicionaisPT/ENno retorno. Estimativa cobrança diretaUS$0; nenhumTTS/rendernovo.','veredito':result['status'],'estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'AdendoG exige decisão anterior a TTS fora das4unidades; returnPT/EN precisam9698.','nao_refazer':'Não repetirv402; não iniciarv403; não sintetizarreturnsemdecisão. Reutilizar inventário e cache verificados.','proximo_passo':'Gerência decide as duas adicionais; depois conferência integral e render único autorizado.','onde':str(G),'artefatos':[str(T/'RESULTADO.json'),str(review_path)],'refs':[],'nota':'A decisão de redação do F foi resolvida; esta é outra condição explícita do G, sem mudança de ciência/gate.'}
    create(G/'STOP_ROUTE.json',route)
    run_cli('BOARD_STOP.json',[r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F0.FILMES_V7_20261024','--quem',ACTOR['id'],'--status','BLOQUEADA','--evidencia',str(T/'RESULTADO.json'),str(review_path),'--nota','AdendoG:duasTTSadicionaisreturnPT/EN; estimativaUS$0. Decisão da gerência antes de qualquer síntese/render.'])
    run_cli('ROUTE_STOP.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(G/'STOP_ROUTE.json'),'--quem',ACTOR['id']])
    print(json.dumps({'status':result['status'],'result':pin(T/'RESULTADO.json'),'report_lines':len(lines)},ensure_ascii=False))


if __name__=='__main__':main()
