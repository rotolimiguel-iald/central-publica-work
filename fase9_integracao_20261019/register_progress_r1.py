"""Append partial progress under claim1033; no scientific requirement is accepted."""
from setup_mission import ROOT,UNIT,ACTOR,REF,pin,save,shell,call
from pathlib import Path
import json,sys,datetime,os

if __name__=='__main__':
    for n in ['MEMORY_APPLIED_R1.json','MAP_ENTRY_R1.json','REGISTRATION_R1.json']:
        assert not (ROOT/n).exists(),n
    progress=json.loads((ROOT/'PROGRESS_R1.json').read_text(encoding='utf-8'))
    for x in progress['evidence']:
        assert pin(x['path'])['sha256']==x['sha256'],x['path']
    board=shell('BOARD_PREFLIGHT_REGISTER_R1.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT])
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    state=call('GET_REGISTER_R1.json',{'operation':'get','reference':REF},False)
    note='''

## 19/10/2026 — Fase9: componentes de integração, progresso parcial
<!-- IALD_FASE9_INTEGRACAO_20261019_R1 -->
[REAL documental/sintético — em nome de codex-gerente-tgl, F3.INTEGRACAO_20261019, reivindicação1033] Reuso da auditoria anterior e deF3.1/F3.2/ORDEM018. Inventário28pares/8mapas e24controles; fornecedorCAMB real em7pontos sintéticos com16controles; consumidorD-H/convergência com17controles e ligação ao gate existente. Revisões distintas por componente, sem aceite integralc1. Correções numéricas em arquivos novos: raízes quadráticas estáveis e recusa de overflow. Os38controles iniciais da calibração não foram alegados como reexecutados naR2;4controles focais adicionais. Não repetir o fornecedor nem os controles por perda de contexto.
[DERIVED] ReduçãoGLS exata no modelo escalar de fatores uniformes permite calcular cauda gaussiana quadrática condicional; não basta sqrt(DeltaQ). Fundo sorteado gaussiano é hipótese amostral explícita, não cobertura uniforme paraH0 fixo desconhecido. J C_theta J^T preserva a incerteza comum; sem covariância externa admitida permaneceCONDITIONAL. K do pontoCAMB sintético não substitui K congelado.
[OPEN] ComponentesSN/Pantheon/âncoras e mapas físicos; evidência integrada no prior físico completo; covariância externa/erro de linearização; modelo amostral real/nuisance/multiplicidade; atosD-H/X13 e revisão/congelamento/abertura próprios. O novo consumidor devolveuPENDING_D_H,required_sources_admitted=false,n_alvos_declarados=2 (L1b,L6), sem composto observado. Concordância entre quadraturas é diagnóstico, não certificado de erro.
[REAL documental] HistóricoV1 z_disc4,2837356/INCONCLUSIVE_SYSTEMATICS preservado. Desenho nominal da auditoria anterior: primárioBG1 D5,721408–6,623219; semCefeidas D3,937917–4,395122, condicionais. Nenhum sigma observadoV2 nem demonstração5sigma. Nenhum ajuste ao dado, provedor, produção, um.py, kernel, Bancada ou gate.
Entrega parcial: C:\\IALD\\Central de Patentes\\work\\fase9_integracao_20261019\\PROGRESS_R1.json; relatórioRELATORIO_PROGRESSO_R1.txt. ReferênciaACOM própriaSESSION_REFERENCE.json; os cinco requisitos não foram aceitos/fechados. Próximo: preencher limites físicos/mapas e qualificar integração/cauda, usando os componentes já entregues.
<!-- END_IALD_FASE9_INTEGRACAO_20261019_R1 -->
'''
    save('MEMORY_APPEND_R1.txt',note)
    extra=note.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        target=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=target.read_bytes();before=pin(target)
        assert b'IALD_FASE9_INTEGRACAO_20261019_R1' not in raw
        backup=target.with_name(target.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        temp=target.with_name(target.name+'.tmp_f9integration_'+stamp)
        with temp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and target.read_bytes()==raw
        os.replace(temp,target)
        assert target.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(backup),'after':pin(target),'pure_append':True})
    save('MEMORY_APPLIED_R1.json',rows)
    entry={'tipo':'ROTA','rota_id':'d1.fase9.integracao_20261019','dominio':'D1_FUNDO_COSMOLOGICO',
           'titulo':'Fase9: fornecedor físico e controles de covariância, cauda e admissão em cópia',
           'pergunta':'Como qualificar as cinco pendências sem ajustar parâmetros ao dado?',
           'dados':['Artefatos admitidos existentes e controles sintéticos; nenhum composto observadoV2'],
           'metodo':'Reaproveitamento de contratos; sete pontosCAMB; reduçãoGLS; revisões independentes de componentes',
           'resultado':'Componentes qualificados com escopo; covariâncias/mapas, integral física, cobertura estatística e atos continuam abertos. ObservadoV2null.',
           'veredito':'PARTIAL_COMPONENTS_QUALIFIED__PHYSICAL_INFERENCE_OPEN','estatuto':'DERIVED',
           'status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
           'defeito':'Cinco requisitos não integralmente fechados; ver PROGRESS_R1.json.',
           'nao_refazer':'Não repetir gate/harness antigo, setechamadasCAMB ou controles já pinados. Revisão não executou novamenteCAMB.',
           'proximo_passo':'Limites físicos/mapas; integral/prior; cauda e nuisances; atos reais antes de freeze/opening.',
           'onde':str(ROOT/'RELATORIO_PROGRESSO_R1.txt'),
           'artefatos':[str(ROOT/'PROGRESS_R1.json'),str(ROOT/'RELATORIO_PROGRESSO_R1.txt')],
           'refs':['d1.fase9.auditoria_suficiencia_20261019'],'nota':'Sem alegação5sigma observada; sem produção/gate.'}
    save('MAP_ENTRY_R1.json',entry)
    shell('MAP_REGISTER_R1.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R1.json'),'--quem',ACTOR['id']])
    shell('BOARD_PROGRESS_R1.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'PROGRESS_R1.json'),'--nota','Progresso material parcial: componentes sintéticos revisados; cinco requisitos ainda não fechados. Sem observado/freeze/produção/gate.'])
    transition=call('TRANSITION_R1.json',{'operation':'transition','reference':REF,'actor':ACTOR,
        'expected_revision':state['revision'],'event_id':'fase9-integration-components-r1',
        'changes':{'records':[{'id':'fase9-components-r1','kind':'fact','statute':'REAL',
        'text':note,'sources':[{'kind':'artifact','ref':str(ROOT/'PROGRESS_R1.json'),'sha256':pin(ROOT/'PROGRESS_R1.json')['sha256']}]}],
        'flow':{'phase':'components_qualified_science_open','next_action':'Reuse PROGRESS_R1 and reviews. Resolve cross-reader bounds/maps, full physical integral, actual sampling/nuisance/multiplicity and admission acts. No new observed V2. All tasks remain working; refresh lease before material continuation.',
                'handles':state['p']['handles']}}},False)
    h=call('HANDOFF_REGISTER_R1.json',{'operation':'handoff','reference':REF,'max_chars':50000})
    save('REGISTRATION_R1.json',{'status':'PARTIAL_PROGRESS_REGISTERED','progress':pin(ROOT/'PROGRESS_R1.json'),
         'memory':pin(ROOT/'MEMORY_APPLIED_R1.json'),'map':pin(ROOT/'MAP_REGISTER_R1.json'),
         'board':pin(ROOT/'BOARD_PROGRESS_R1.json'),'acom':transition,'handoff':pin(ROOT/'HANDOFF_REGISTER_R1.json'),
         'script':pin(__file__)})
    print(json.dumps({'status':'PARTIAL_PROGRESS_REGISTERED','unit':UNIT,'acom':transition},ensure_ascii=False))
