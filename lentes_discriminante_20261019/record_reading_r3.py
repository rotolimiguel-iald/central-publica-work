"""Register reviewed R3 without modifying its scientific evidence."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, os, sys, json

if __name__ == '__main__':
    folder = ROOT / 'reading_r3'
    for name in ['DELIVERY_R3.json', 'MEMORY_APPEND_R3.txt', 'MEMORY_APPLIED_R3.json', 'REGISTRATION_R3.json']:
        if (ROOT/name).exists(): raise FileExistsError(name)
    review = json.loads((folder/'REVIEW_R3.json').read_text(encoding='utf-8'))
    assert review['status'] == 'PASS_WITH_SCOPE'
    checkpins(review)
    board = json.loads(command('BOARD_PREFLIGHT_R3', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py', 'ver', UNIT]))
    claim = board['reivindicacao']
    assert claim['quem'] == ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em']) > datetime.datetime.now(datetime.timezone.utc)
    ref = str(ROOT/'SESSION_REFERENCE.json')
    state = memory({'operation':'get', 'reference':ref}, 'GET_BEFORE_R3')
    assert state['revision'] == 3
    save('DELIVERY_R3.json', {
        'status':'DERIVED_REVIEWED_WITH_SCOPE_NO_OBSERVED_5SIGMA', 'unit':UNIT,
        'physical_goal_complete':False, 'observed_data_composed':False, 'gate_changed':False,
        'scope':'Existing scalar prediction recovered; conditional optical extension and external-background forecast. Full physical lens likelihood map remains OPEN.',
        'review':pin(folder/'REVIEW_R3.json'),
        'evidence':[pin(p) for p in sorted(folder.rglob('*')) if p.is_file()],
        'recording_script':pin(__file__)})
    txt = '''

## 19/10/2026 — Lentes R3: contrato existente e calibração externa
<!-- IALD_LENSING_READING_R3_20261019 -->
[DERIVED condicional — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação 1009] A v393 e a Fase 9 já escrevem H_lens=K H_bg. A fonte posterior de 08/10 também marca o mapa da likelihood L5 como OPEN. Preservadas ambas: a previsão escalar existe; a dedução conjunta de relógio, feixe, potencial e cinemática ainda não está estabelecida. R-G exige f_t F_D/f_phi=1/K; fixar esse produto não determina os fatores por trajetória.
[DERIVED, extensão nomeada] Se a integral acumulada SN for promovida à geometria óptica plana, chi=c J/(H0 K), J=int E^(2 beta/3-1), então Ddt=c/(H0 K) J_l J_s/(J_s-J_l). Transformações chi/(a+b chi) deixam Ddt/a: b é invisível aos atrasos, sem afirmar invariância da cinemática. Cinco pares sintéticos, matéria+Lambda com radiação zero, após perfilar escala e Omega_m deixam residual máximo 3,77968e-5, norma 0,00615 para erros independentes de 1%. Essa extensão não é promovida a lei canônica.
[DERIVED, cenário escalar] Com BG1=68,531 +/-0,301 e K recalculado das constantes/parametrização pinados, K=1,0838071748529643 e DeltaH=5,7433895 km/s/Mpc. Barras de lente 2,3 e 2,4 usadas como cenários gaussianos independentes dão separação Asimov 2,476 e 2,374; mediana 5 exigiria sigma_lens<=1,10854 km/s/Mpc. K fixo, independência, compressão gaussiana e validade da leitura de H_lens são hipóteses. Nenhum centro de lente foi usado no cálculo; não é detecção observada nem poder de descoberta de 90%. Não somar amostras TDCOSMO sobrepostas.
[REAL documental] Revisão independente PASS_WITH_SCOPE, 29 pinos conferidos, sem achado material. Recibo reading_r3/REVIEW_R3.json; entrega DELIVERY_R3.json. A meta 5 sigma segue aberta. Próximo cálculo: explicitar a perda de identificabilidade por escala de massa comum e as precisões independentes necessárias, sem substituir a ponte física aberta por ajuste ao número. Nenhum original, kernel, Bancada, dado observado ou gate alterado.
<!-- END_IALD_LENSING_READING_R3_20261019 -->
'''
    save('MEMORY_APPEND_R3.txt', txt)
    extra=txt.encode('utf-8'); stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=p.read_bytes(); assert b'IALD_LENSING_READING_R3_20261019' not in raw
        before=pin(p); bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        temp=p.with_name(p.name+'.tmp_lensR3_'+stamp)
        with temp.open('xb') as f: f.write(raw+extra); f.flush(); os.fsync(f.fileno())
        assert temp.stat().st_size==len(raw)+len(extra) and p.read_bytes()==raw
        os.replace(temp,p); assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R3.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R2.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R3: contrato escalar e identificabilidade com fundo externo',
        'resultado':'H_lens=K H_bg existe; mapa fisico da likelihood OPEN. Extensao optica condicional quase absorvida por escala/Omega_m. Ancora externa conserva alvo DeltaH=5,7434; mediana5 requer sigma_lens<=1,10854 no cenario independente.',
        'veredito':'NO_OBSERVED_5SIGMA__SCALAR_FORECAST_CONDITIONAL',
        'defeito':'Ponte de trajetoria/likelihood e calibracao conjunta de massa ainda abertas.',
        'proximo_passo':'Quantificar degenerescencia de escala de massa e exigencias de calibracao externa.',
        'artefatos':[str(ROOT/'DELIVERY_R3.json'),str(folder/'RESULTADO_LEITURA_R3.md'),str(folder/'REVIEW_R3.json')],
        'nota':'R3 condicional, nao combina dados observados nem transforma norma sintetica em descoberta.'})
    save('MAP_ENTRY_R3.json',entry)
    command('MAP_REGISTER_R3',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R3.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R3',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R3.json'),'--nota','R3 revisada: previsao escalar existente e limite condicional de precisao. Lei de lente e calibracao conjunta OPEN; sem5sigmaobservado.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':3,'event_id':'lensing-reading-r3-delivered','changes':{
        'records':[{'id':'lensing-reading-r3','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R3.json'),'sha256':pin(ROOT/'DELIVERY_R3.json')['sha256']}],'text':txt}],
        'flow':{'phase':'reading_r3_reviewed','next_action':'Quantify conditional scalar contrast after common mass-sheet and background calibration; physical trajectory likelihood bridge remains OPEN. No observed verdict; do not redo R1-R3.','handles':[]}}},'TRANSITION_R3')
    save('REGISTRATION_R3.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R3.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R3.json'),'map':pin(ROOT/'MAP_REGISTER_R3.json'),'board':pin(ROOT/'BOARD_UPDATE_R3.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
