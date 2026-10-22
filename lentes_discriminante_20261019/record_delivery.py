"""Additive record of the lensing survey; preserves the separate formal mission."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from pathlib import Path
import json, hashlib, datetime, os
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__=='__main__':
    review=json.loads((ROOT/'REVIEW_R1.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS')
    for e in review['evidence']: assert pin(e['path'])['sha256']==e['sha256']
    for name in ['LENTES_VIABILIDADE_R1.md','FORECAST_RESULT.json','SOURCES_INTERNAL.json','PUBLIC_SOURCE_CUSTODY_R2.json']:
        assert any(e['sha256']==pin(ROOT/name)['sha256'] for e in review['evidence']),name
    records=json.loads((ROOT/'SOURCES_INTERNAL.json').read_text(encoding='utf-8'))
    def checktree(obj):
        if isinstance(obj,dict):
            if 'path' in obj and 'sha256' in obj: assert pin(obj['path'])['sha256']==obj['sha256']
            for v in obj.values():checktree(v)
        elif isinstance(obj,list):
            for v in obj:checktree(v)
    checktree(records)
    checktree(json.loads((ROOT/'PUBLIC_SOURCE_CUSTODY_R2.json').read_text(encoding='utf-8')))
    assert not (ROOT/'DELIVERY_R1.json').exists()
    text='''

## 19/10/2026 — Prioridade do operador: discriminante TGL em lentes gravitacionais
<!-- IALD_LENSING_5SIGMA_SURVEY_20261019 -->
[INPUT — em nome de codex-gerente-tgl; unidade F8.LENTES_5SIGMA_20261019, reivindicação1009] Operador mudou o foco imediato para dado discriminante5σ, preferindo lentes/atraso em confronto com massa. A missão formal R16/H3 conserva seu estado separado; não foi encerrada como provada. Fonte integral: work/lentes_discriminante_20261019/OPERADOR_VERBATIM.txt; ACOM própria SESSION_REFERENCE.json.
[REAL documental] Reutilizadas R-G da ORDEM018 e errata f_phi: H_fit/H_bg=f_phi/(f_t F_D). Um.py v393 conferido contra selo, não executado. Levantamento interno pinou dez fontes; lei por trajetória ainda não localizada no recorte. NMC vigente conserva Shapiro do neutrino; excesso é fotônico. Não reutilizar fórmula histórica corrigida nem os50ms/21σ como previsão/poder já estabelecidos por lente. Documentos públicos TDCOSMO2025/2026, CosmoSIS e SN H0pe guardados por hash;2026 anuncia dados/likelihood após aceitação, não se afirmou liberação. Nenhum composto observado foi rodado.
[DERIVED condicional] Cenário ilustrativo δ=β, sem atribuir essa amplitude às lentes: precisão total≤0,240626% para separação gaussiana mediana5;18 sistemas com1% ou432 com5%, somente se independentes e sem piso comum. Um deslocamento livre que absorva o sinal zera a identificabilidade. PrecisãoH0 não é precisãoβ. Prioridade: imagem/arcos+atrasos+cinemática resolvida, com a mesma massa e liberdade de nuisance; SN Ia lenteada como complemento. Próxima etapa é recuperar/derivar o mapa observacional e medir poder após nuisance, antes de veredito. Levantamento não cego: centros publicados foram vistos na literatura. NOT_FALSIFIED não é confirmação; nenhum gate movido.
Evidências: work/lentes_discriminante_20261019/LENTES_VIABILIDADE_R1.md, FORECAST_RESULT.json, REVIEW_R1.json e DELIVERY_R1.json. Sem provider, instalação ou alteração de kernel/um.py/Bancada.
<!-- END_IALD_LENSING_5SIGMA_SURVEY_20261019 -->
'''
    save('MEMORY_APPEND_R1.txt',text)
    extra=text.encode('utf-8'); surfaces=[]; stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=p.read_bytes();before=pin(p)
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_lenses_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra) and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        surfaces.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R1.json',surfaces)
    save('DELIVERY_R1.json',{'status':'SURVEY_DELIVERED_PHYSICAL_MAP_AND_OBSERVED_TEST_PENDING','unit':UNIT,'claim':1009,'observed_verdict':False,'gate_changed':False,'evidence':[pin(p) for p in sorted(ROOT.iterdir()) if p.is_file()]})
    entry={'tipo':'RESULTADO','rota_id':'discriminante.lentes_5sigma_20261019','dominio':'LENTEAMENTO','titulo':'Lentes: reuso R-G, fontes2026 e identificabilidade antes do veredito','estatuto':'DERIVED condicional','status':'EM_CURSO','resultado':'Priorizar imagem+atrasos+cinematica. Cenário ilustrativo delta=beta exige0.240626% total para mediana5sigma; nao e previsao TGL de lente. Fontes publicas pinadas.','veredito':'FEASIBILITY_ONLY_NO_OBSERVED_VERDICT','olhou_dados':True,'nota':'Exposicao a centros em abstracts; sem leitura de amostra/composto para veredito.','defeito':'K escalar nao fixa f_t,F_D,f_phi; lei por trajetoria e poder apos nuisance permanecem pendentes.','nao_refazer':'Reusar ORDEM018 R-G e errata; nao repetir testes anteriores.','proximo_passo':'Obter previsao fisica por lente e resposta nao absorvivel por massa/distancias; fixar protocolo antes do teste observado.','refs':['discriminante.ordem018.f2.r_g','neutrinos.shapiro_nmc'],'onde':str(ROOT),'artefatos':[str(ROOT/'DELIVERY_R1.json'),str(ROOT/'LENTES_VIABILIDADE_R1.md')]}
    entry['nao_refazer']='Reusar ORDEM018 R-G/errata e protocolos existentes; nao repetir testes nem promover forecasts antigos.'
    save('MAP_ENTRY_R1.json',entry)
    command('MAP_REGISTER_R1',[os.sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R1.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R1',[os.sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R1.json'),'--nota','Levantamento revisado entregue; mapa fisico por trajetoria e poder apos nuisance pendentes. Sem veredito observado.'])
    ref=str(ROOT/'SESSION_REFERENCE.json'); state=memory({'operation':'get','reference':ref},'GET_FINAL_R1')
    memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':state['revision'],'event_id':'lensing-survey-r1-delivered','changes':{'records':[{'id':'lensing-survey-r1','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R1.json'),'sha256':pin(ROOT/'DELIVERY_R1.json')['sha256']}],'text':text}],'flow':{'phase':'lensing_survey_and_conditional_precision','next_action':'Recover/derive the physical lens trajectory response; test identifiability against mass/distance nuisance before observed verdict. Reuse R-G, keep formal H3 mission separate.','handles':[]}}},'TRANSITION_R1')
    print(json.dumps({'unit':UNIT,'delivery':pin(ROOT/'DELIVERY_R1.json'),'memory_surfaces':len(surfaces)},ensure_ascii=False))
