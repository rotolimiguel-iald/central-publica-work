"""Custody the R5 action audit and preserve the unfinished physical goal."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, os, sys, json

if __name__=='__main__':
    folder=ROOT/'historical_r5'; ref=str(ROOT/'SESSION_REFERENCE.json')
    for name in ['DELIVERY_R5.json','MEMORY_APPEND_R5.txt','MEMORY_APPLIED_R5.json','REGISTRATION_R5.json']:
        if (ROOT/name).exists():raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R5.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS'); checkpins(review)
    checkpins(json.loads((folder/'SOURCE_TRACE_R5.json').read_text(encoding='utf-8')))
    checkpins(json.loads((folder/'PUBLIC_CUSTODY_R5.json').read_text(encoding='utf-8')))
    board=json.loads(command('BOARD_PREFLIGHT_R5',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao']; assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_R5'); assert state['revision']==5
    save('DELIVERY_R5.json',{'status':'REVIEWED_BOUNDED_ACTION_AUDIT__PHYSICAL_LENS_MAP_OPEN','unit':UNIT,
      'goal_complete':False,'observed_data_composed':False,'gate_changed':False,
      'evidence':[pin(p) for p in sorted(folder.rglob('*')) if p.is_file()],'recording_script':pin(__file__)})
    txt='''

## 19/10/2026 — Lentes R5: origem do atraso histórico e distinção dos acoplamentos
<!-- IALD_LENSING_HISTORICAL_R5_20261019 -->
[REAL documental — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Recuperada a nota de lentes de11/10/2025: xi integral|Psi|²/c³ era acompanhada de ajuste de xi/lambda/m, priors e posteriores. Tratado histórico identifica xi=beta com ressalva semiquantitativa; Custo vigente e um.py171003 distinguem explicitamente xi=1/6 conforme de beta modular. Não transferir beta para xi, lambda ou alpha2/RicciFF por homonímia. Normalização alpha_Psi aparece com c⁴ e c²; R_E também em arcsegundos. Fonte positiva preservada; não constitui previsão fixa normalizada por lente.
[DERIVED com escopo] Para L_EM=-Z(Psi)F²/4, a variação dá nabla(ZF)=0; em fundo suave fixo, Z não nulo, o símbolo principal mantém k²=0. Isso não produz diretamente a demora universal xi integral|Psi|² da nota. Pode alterar transporte de amplitude; resposta da métrica, matéria, frequência finita e operadores tensoriais são questões distintas. Controle simbólico A=u/sqrtZ em1D verifica u_tt-u_xx+[(sqrtZ)''/sqrtZ]u=0. Não se afirmou que todo pacote ou a TGL inteira tenham atrasoextra zero. Fonte primária Hees etal1406.6187v2, equações6–9, custodiada porhash; serve de conferência de escopo.
[DERIVED controles internos] Alpha_Psi histórico3,1e8 com velocidade sintética250km/s dá0,01499% pela fórmula impressa, sem composto observado. NaSIS, atraso escala sigma² para fonteangular fixa e sigma⁴ para fonte normalizada fixa: potência quartica sozinha não discrimina. Script exit0; revisão independente delimita alcance. Os alegados números históricos permanecem DECLARADO, não reproduzidos nesta etapa.
[OPEN] Falta resolver/recuperar o problema de contorno vigente do escalar e da métrica: V, K_boundary, fonte, perfil e condições de contorno, produzindo os potenciais fotônico/estelar e a diferença entre trajetórias na mesma convenção de relógio. R4 já dispõe do perfilamento; não repetir forecasts sem esse insumo. Não escolher coeficiente pelo efeito desejado. Meta5sigma ativa; nenhuma detecção observada nem alteração de original/kernel/Bancada/gate.
Evidências: DELIVERY_R5.json; historical_r5/RESULTADO_ORIGEM_ATRASO_R5.md, SOURCE_TRACE_R5.json, ACTION_RESULT_R5.json, RUN_R5.json e REVIEW_R5.json.
<!-- END_IALD_LENSING_HISTORICAL_R5_20261019 -->
'''
    save('MEMORY_APPEND_R5.txt',txt); extra=txt.encode('utf-8')
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name; raw=p.read_bytes()
        assert b'IALD_LENSING_HISTORICAL_R5_20261019' not in raw
        before=pin(p); bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_lensR5_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R5.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R4.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R5: formula historica, acoplamento conforme e cone fotonico',
      'resultado':'Atraso historico usa parametros ajustados e normalizacoes conflitantes; xi vigente=1/6 distinto beta. Z(Psi)F² mantem cone principal nulo no fundo fixo; atraso integral nao derivado desse fator.',
      'veredito':'NO_OBSERVED_5SIGMA__HISTORICAL_SHORTCUT_NOT_ESTABLISHED',
      'defeito':'Solucao conjunta escalar/metrica e consumidor de lentes ainda OPEN; resultado local nao exclui todaTGL.',
      'proximo_passo':'Recuperar V, K_boundary e condicoes de contorno vigentes para os potenciais fotonico/estelar; nao promover xi ajustado a beta.',
      'artefatos':[str(ROOT/'DELIVERY_R5.json'),str(folder/'RESULTADO_ORIGEM_ATRASO_R5.md'),str(folder/'SOURCE_TRACE_R5.json')],
      'nota':'Conferencia de acao e simbolos, nao recomposicao dos alegados dados historicos; originais preservados.'})
    save('MAP_ENTRY_R5.json',entry)
    command('MAP_REGISTER_R5',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R5.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R5',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R5.json'),'--nota','R5 revisada: atraso historico nao fornece previsao fixa; acoplamentos e cone principal conferidos. Solucao metrica/estelar OPEN.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':5,'event_id':'lensing-historical-r5-delivered','changes':{
      'records':[{'id':'lensing-historical-r5','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R5.json'),'sha256':pin(ROOT/'DELIVERY_R5.json')['sha256']}],'text':txt}],
      'flow':{'phase':'historical_action_r5_reviewed','next_action':'Recover current scalar/metric boundary-value law (V, K_boundary, source and asymptotics); compute photon and stellar potentials consistently. R5 excludes only direct scalar-prefactor shortcut at fixed metric. Do not reuse fitted historical xi as beta or redo R1-R4 forecasts. No observed5sigma.','handles':[]}}},'TRANSITION_R5')
    save('REGISTRATION_R5.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R5.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R5.json'),'map':pin(ROOT/'MAP_REGISTER_R5.json'),'board':pin(ROOT/'BOARD_UPDATE_R5.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
