"""Custody and additive continuity for the bounded lensing R2 analysis."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from pathlib import Path
import datetime, hashlib, json, os, sys

R2=ROOT/'trajectory_r2'
def pin(p):
    p=Path(p); raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def checkpins(obj):
    if isinstance(obj,dict):
        if 'path' in obj and 'sha256' in obj:
            assert pin(obj['path'])['sha256']==obj['sha256'],obj['path']
        for v in obj.values(): checkpins(v)
    elif isinstance(obj,list):
        for v in obj: checkpins(v)

if __name__=='__main__':
    for n in ['DELIVERY_R2.json','MEMORY_APPEND_R2.txt','MEMORY_APPLIED_R2.json','REGISTRATION_R2.json']:
        if (ROOT/n).exists(): raise FileExistsError(n)
    for n in ['REVIEW_R2.json','REVIEW_BACKGROUND_R2.json']:
        d=json.loads((R2/n).read_text(encoding='utf-8'))
        assert d['status'].startswith('PASS')
        checkpins(d)
    for n in ['SOURCE_ACTION_PINS_R2.json','ALT_LENS_PINS_R2.json','DISTANCE_DELIVERY_R2.json','DELIVERY_IDENTIFIABILITY_R2.json']:
        checkpins(json.loads((R2/n).read_text(encoding='utf-8')))
    board=json.loads(command('BOARD_PREFLIGHT_R2',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json')
    projection=memory({'operation':'project','reference':ref,'max_chars':24000},'PROJECT_BEFORE_R2')
    assert projection['receipt']['revision']==2
    save('DELIVERY_R2.json',{
        'status':'DERIVED_REVIEWED_WITH_SCOPE_NO_OBSERVED_5SIGMA','unit':UNIT,'claim':1009,
        'scope':'Literal photon operators, joint lens nuisance identifiability and synthetic background distance profile; full TGL lens law unresolved.',
        'physical_goal_complete':False,'observed_data_composed':False,'gate_changed':False,
        'evidence':[pin(p) for p in sorted(R2.rglob('*')) if p.is_file()],
        'recording_script':pin(Path(__file__))})
    txt='''

## 19/10/2026 — Lentes R2: ação recuperada, trajetória e perfilamento
<!-- IALD_LENSING_TRAJECTORY_R2_20261019 -->
[DERIVED — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Recuperada a ação histórica q R_ab F^{ac}F^b_c, q=alpha2/M_P², e a identificação posterior alpha2=beta; q geométrico=beta*l_P². Não confundir com alpha_fine² nem com a contração escalar RF² do texto atualum.py. Em campo de teste/óptica geométrica de primeira ordem sobre fundo GR de poeira: deltaDelta_t=(1+zl)8pi beta l_P² G/c³ DeltaSigma. Exterior Schwarzschild Ricci-flat dá zeroextra, conservando Shapiro ordinário. Controle sintético DeltaSigma10kg/m²,zl.5 dá2.93473e-105s; esse ramo normalizado não deriva50ms nem oferece sinal praticável. Não exclui toda a TGL ou respostas adicionais da métrica. Ramo escalar regular tem coneprincipal Maxwell.
[DERIVED] Ação/Fermat consistente inclui deslocamento das imagens. Há família exata de massa/fonte/distância preservando duas posições axiais e um atraso para perturbação radial;23 controles racionais. Razõesdeatraso não quebram MST. A função angular do Custo foi recuperada: fundo H²=H_LCDM²(1+beta|1+w|) reparametriza exatamente GR com densidades livres; a radiação física default fixa impede esse mapa exato. Controle de cinco distâncias sintéticas, H0nu70 Om.3, perfilando H0/Om com radiação fixa: residualmáximo2.011125e-8, norma3.03426e-6 para errosindependentes1%. Precisãoideal6.07e-9 por distância para norma5 nessecontrole; não é poder observado nem precisão realizável. Revisão independente validou álgebra e reprodução numérica; solução local interior, sem prova de mínimo global.
[OPEN] Falta assinatura de lente identificável da leitura acumulada D1b ou outro efeito derivado sobrevivente a nuisances. Reusar ORDEM018 R-G, sem converter K(z) emdistância angular por analogia e sem reinserir lei de massa retirada. O cálculo delimita ramos, não encerra a meta5sigma. Nenhum original científico, kernel, Bancada, dado observado ou gate alterado; nenhum provedor. Primeiro erro mecânico SymPy preservado; scripts/resultados novos. Fontes/pinos/revisões em work/lentes_discriminante_20261019/trajectory_r2; recibo DELIVERY_R2.json. Meta formal H3 permanece separada.
<!-- END_IALD_LENSING_TRAJECTORY_R2_20261019 -->
'''
    save('MEMORY_APPEND_R2.txt',txt)
    extra=txt.encode('utf-8'); stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=p.read_bytes(); assert b'IALD_LENSING_TRAJECTORY_R2_20261019' not in raw
        before=pin(p); bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        temp=p.with_name(p.name+'.tmp_lensR2_'+stamp)
        with temp.open('xb') as f: f.write(raw+extra); f.flush(); os.fsync(f.fileno())
        assert temp.stat().st_size==len(raw)+len(extra) and p.read_bytes()==raw
        os.replace(temp,p); assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R2.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R1_ROTA.json').read_text(encoding='utf-8'))
    entry.update({'tipo':'RESULTADO','titulo':'Lentes R2: atraso Ricci por trajetoria e residual apos massa/distancia',
       'status':'EM_CURSO','estatuto':'DERIVED condicional; calculos sinteticos revisados',
       'resultado':'Acao RicciFF/Planck recuperada: efeito local impraticavel; degenerescencias de massa/distancia demonstradas. Fundo com coeficientes livres exatamente reparametrizavel; cinco distancias com radiacaofixa/H0Om perfilados deixam max2.011125e-8.',
       'veredito':'NO_OBSERVED_5SIGMA__BOUNDED_BRANCHES_UNPROMISING',
       'defeito':'Lei de lente completa e ligacao D1b-angular ainda nao estabelecidas; textos RFF usam contracoes distintas. Nenhuma exclusao global da TGL.',
       'proximo_passo':'Confrontar leitura acumulada D1b com D_A e D_ls no acervo, antes de novo composto; procurar assinatura sobrevivente com informacao externa real.',
       'artefatos':[str(ROOT/'DELIVERY_R2.json'),str(R2/'RESULTADO_LENTES_R2.md'),str(R2/'TRAJECTORY_DERIVATION_R2.md'),str(R2/'BACKGROUND_RESULT_R2.json')],
       'nota':'R2 sintetica; nao reutiliza forecasts50ms/21sigma nem transfere beta para atraso ad hoc; exposicao documental R1 preservada.'})
    save('MAP_ENTRY_R2.json',entry)
    command('MAP_REGISTER_R2',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R2.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R2',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R2.json'),'--nota','R2 revisada: lei por trajetoria de operador recuperado, degenerescencias e residual sintetico apos perfilamento. Sem5sigmaobservado; metaempirica/leiD1b-angular seguemabertas.'])
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_TRANSITION_R2')
    assert state['revision']==2
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':2,'event_id':'lensing-trajectory-r2-delivered','changes':{
        'records':[{'id':'lensing-trajectory-r2','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R2.json'),'sha256':pin(ROOT/'DELIVERY_R2.json')['sha256']}],'text':txt}],
        'flow':{'phase':'trajectory_and_background_profile_r2_reviewed','next_action':'Reuse completed R2; inspect the accumulated D1b reading versus actual angular and lens-source distance laws for an identifiable residual with independent calibration. Do not redo conditional50ms or generic beta forecasts. No observed5sigma; H3 mission stays separate.','handles':[]}}},'TRANSITION_R2')
    save('REGISTRATION_R2.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R2.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R2.json'),'map':pin(ROOT/'MAP_REGISTER_R2.json'),'board':pin(ROOT/'BOARD_UPDATE_R2.json'),'acom':out})
    print(json.dumps({'status':'PASS','delivery':pin(ROOT/'DELIVERY_R2.json'),'acom':out},ensure_ascii=False))
