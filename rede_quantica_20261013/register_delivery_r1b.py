"""Register the reviewed delivery, append claimed memory with byte backups, release."""
from pathlib import Path
import datetime as dt
import hashlib,json,os,subprocess,sys,time
ROOT=Path(r'C:\IALD\Central de Patentes')
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
WORK=ROOT/'work/rede_quantica_20261013'
PY=r'C:\Python314\python.exe'
CLI=r'C:\IALD\PROGRAMA_IALD\iald.py'
MEM=r'C:\IALD\MEMORIA_IALD\session_memory.py'
WHO='codex-gerente-tgl'

def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def source(p):
    d=pin(p);return {'kind':'artifact','ref':d['path'],'sha256':d['sha256']}
def new(name,value):
    p=OUT/name;t=p.with_name(p.name+'.tmp')
    if p.exists():raise FileExistsError(p)
    b=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.rename(t,p)
    return pin(p)

def run(name,args,payload=None,mutation=False):
    if (OUT/name).exists():raise FileExistsError(OUT/name)
    command=[PY,'-B','-X','utf8',*args]
    if mutation:new(name+'.intent.json',{'command':command,'payload':payload,'at':dt.datetime.now(dt.timezone.utc).isoformat(),'rule':'Do not repeat automatically if receipt is absent; recover outcome.'})
    start=dt.datetime.now(dt.timezone.utc);clock=time.perf_counter()
    cp=subprocess.run(command,input=None if payload is None else json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
    value={'command':command,'start_utc':start.isoformat(),'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
    receipt=new(name,value)
    if cp.returncode:raise RuntimeError(value)
    parsed=json.loads(cp.stdout)
    if parsed.get('ok') is False:raise RuntimeError(parsed)
    print(json.dumps({'receipt':receipt,'result':parsed},ensure_ascii=False))
    return parsed

def claim():
    cp=subprocess.run([PY,'-B','-X','utf8',CLI,'ver','F1.REDE'],capture_output=True,text=True,encoding='utf-8',check=True)
    u=json.loads(cp.stdout);r=u.get('reivindicacao')
    assert r and r['quem']==WHO and dt.datetime.fromisoformat(r['vence_em'])>dt.datetime.now(dt.timezone.utc)
    assert all(s in r['nota'] for s in ['Atlas','índice','AVISO'])
    return u

mode=sys.argv[1]
if mode=='map':
    run('MAP_REGISTER_ENTREGA_R1A.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(OUT/'MAP_ENTRY_ENTREGA_R1A.json'),'--quem',WHO+' / F1.REDE'],mutation=True)
elif mode=='memory':
    if (OUT/'MEMORY_DELIVERY_R1.json').exists():raise FileExistsError('memory receipt')
    u=claim();new('MEMORY_INTENT_R1.json',{'claim':u['reivindicacao'],'unit':'F1.REDE','at':dt.datetime.now(dt.timezone.utc).isoformat()})
    result=pin(OUT/'RESULTADO_ENTREGA_R1.json');mod=pin(OUT/'modular_wedge/RESULTADO_MODULAR_R1.json')
    review=pin(OUT/'review_modular/REVIEW_MODULAR_R1.json')
    text=f'''\n\n## 13/10/2026 — F1.REDE: contrato e habitante espectral concreto\n<!-- f1_rede_delivery_20261013 -->\n\nEm nome de codex-gerente-tgl, sob reivindicação738 da F1.REDE. Base v392 autorizada pelo operador; não se presume ratificação ou implantação.\n\n[REAL — sandbox e recompilação independente] O tipo D1a3OutputBGL ganhou o habitante F1Rede.CanonicalWedge.spectralOutput no H1 original: Fubini L² vetorial, Fourier parcial, J involutivo, T positivo auto-adjunto, S fechado/denso, K padrão não nulo e grafo completo Δ=S†S. Cinco módulos/75declarações modulares só no trio, zero sorry; a revisão recompilou9módulos e conferiu169pinos. A fase multiplicativa modular é B0(−2πt); não foi usada API geral de potência imaginária ilimitada. Apenas2/5olean modulares foram byte-idênticos na revisão, diferença registrada.\n\n[REAL — sintético] Rede da reta construída. Modelo reduzido2×2×2 do Supercondutor:142/142verificações reproduzidas. Representação Wigner:128amostras,12famílias de identidades, resíduo máximo1,564e−13; controle sem reflexão transversal falha0,99109. Não há dado observado, hardware ou5σ medido.\n\n[DERIVED/KNOWN] CONTRATO_REDE_R2 e CONSTRUCAO_CONTINUA_R1 conectam MQC/Supercondutor, Ψ-NET, TGL-Tensor, Wigner e BGL/Fock, com fontes/hash. Rede livre4D explicitada analiticamente e revista. [OPEN] Formalização4D completa, igualdade geométrica do J, refinamento físico unitário/covariante do dispositivo, certificados Fock/Maxwell simultâneos e antecedente H3. A F2.3 fornece a implicação; não se deriva H3 do estado. Takesaki continua na unidade própria.\n\n[DECLARADO — provedor] Uma única chamada DeepSeek, especificamente autorizada, concluída e conferida; erros separados no parecer. Não repetir request701e5bcb-cb47-4706-a9be-9b5ed10f4a35/job4d57aa1f-2d40-43df-8f82-f16593d899a2.\n\nEntrega candidata à gerência, sem alteração de produção/gate. Resultado: {result['path']} (sha256 {result['sha256']}). Módulos: {mod['sha256']}. Revisão: {review['sha256']}. Mapa: recibo MAP_REGISTER_ENTREGA_R1A.json na mesma pasta.\n'''
    entries=[];stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for p in [ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
        old=p.read_bytes();assert b'f1_rede_delivery_20261013' not in old
        bak=p.with_name(p.name+'.bak_'+stamp+'_F1_REDE')
        with bak.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==old
        raw=old+text.encode('utf-8');tmp=p.with_name(p.name+'.tmp_'+stamp+'_F1_REDE')
        with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw and p.read_bytes()==old
        os.replace(tmp,p)
        actual=p.read_bytes();assert actual==raw and actual.startswith(old) and len(actual)>len(old)
        entries.append({'surface':pin(p),'backup':pin(bak),'append_bytes':len(actual)-len(old),'append_only':True})
    print(json.dumps(new('MEMORY_DELIVERY_R1.json',{'unit':'F1.REDE','author':WHO,'claim':u['reivindicacao'],'at':dt.datetime.now(dt.timezone.utc).isoformat(),'surfaces':entries}),ensure_ascii=False))
elif mode=='board':
    claim()
    run('BOARD_REGISTER_ENTREGA_R1.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','ENTREGUE','--evidencia',str(OUT/'RESULTADO_ENTREGA_R1.json'),str(OUT/'MANIFESTO_ARQUIVOS_R1.json'),str(OUT/'MEMORY_DELIVERY_R1.json'),str(OUT/'MEMORY_CORRECTION_R1.json'),str(OUT/'NOTA_REGISTRO_R1.json'),'--nota','Contrato R2 e construção analítica contínua; habitante espectral D1a3OutputBGL concreto/Tpositivo,75declarações trio,9módulos recompilados. Refinamento do dispositivo e rede4D Lean abertos. Candidata à auditoria, nada integrado.'],mutation=True)
elif mode=='acom':
    claim()
    request={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':1,'event_id':'f1-rede-delivery-r1-20261013','actor':{'id':WHO,'kind':'agent'},'changes':{'records':[
        {'id':'modular-spectral-built-r1','supersedes':'modular-wedge-open-r1','kind':'fact','statute':'REAL','text':'D1a3OutputBGL agora tem habitante concreto no mesmoH1, Tpositivo, Jantiunitario, Sfechado/denso, Kstandard não nulo, grafoDelta=S†S.75declarações trio/zero sorry;9módulos recompilados independentemente. Poincare4D/localização formal e refinamento físico continuamOPEN.','sources':[source(OUT/'modular_wedge/RESULTADO_MODULAR_R1.json'),source(OUT/'review_modular/REVIEW_MODULAR_R1.json')]},
        {'id':'contract-r2-reviewed','supersedes':'sources-contract-r1','kind':'candidate','statute':'DECLARADO','text':'Contrato R2 incorporou RC1 (equivalência unitária física e entrelaçamento integral) e RC2 (Tpositivo/grafo máximo). Revisão independente sem achado material; gerência ainda audita.','sources':[source(OUT/'CONTRATO_REDE_R2.json'),source(OUT/'review_contract/REVIEW_CONTRACT_R2.json')]},
        {'id':'continuum-analytic-r1','kind':'candidate','statute':'DECLARADO','text':'Construção analítica da representação Wigner±1 no H1 da casa: seção explícita, cociclo, continuidade, reflexão e aplicação BGL/Fock. Revisão analítica favorável; formalização4D e ponte do dispositivo abertas.128amostras sintéticas verificam convenções, não prova global.','sources':[source(OUT/'CONSTRUCAO_CONTINUA_R1.json'),source(OUT/'review_continuum/REVIEW_R1.json')]},
        {'id':'deepseek-reviewed-r1','supersedes':'deepseek-return-r1','kind':'candidate','statute':'DECLARADO','text':'Resposta única DeepSeek custodiada e revista; sugestões úteis incorporadas, erros matemáticos/numéricos/unidades recusados. Execução concluída; não repetir.','sources':[source(OUT/'review_deepseek/REVIEW_DEEPSEEK_R1.json'),source(OUT/'provider/SOURCE_CUSTODY_R1.json')]},
        {'id':'delivery-registration-r1','kind':'fact','statute':'REAL','text':'Entrega registrada no mapa e quadro, memórias Atlas/índice/AVISO acrescentadas sob reivindicação com backups byte a byte. Nenhuma aceitação c1 ou integração inferida.','sources':[source(OUT/'BOARD_REGISTER_ENTREGA_R1.json'),source(OUT/'MAP_REGISTER_ENTREGA_R1A.json'),source(OUT/'MEMORY_DELIVERY_R1.json'),source(OUT/'MEMORY_CORRECTION_R1.json'),source(OUT/'RESULTADO_ENTREGA_R1.json')]}
    ],'flow':{'phase':'delivered_awaiting_management_audit','next_action':'Gerência audita esta entrega. Próxima construção científica: Poincare/localização formal e contrato de refinamento físico, sem repetir o que já compila nem o provedor.','handles':[{'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}]}}}
    new('ACOM_DELIVERY_REQUEST_R1.json',request)
    run('ACOM_DELIVERY_RECEIPT_R1.json',[MEM],request,mutation=True)
    run('ACOM_DELIVERY_VERIFY_R1.json',[MEM],{'operation':'verify','reference':str(WORK/'ACOM_REFERENCE.json')})
elif mode=='release':
    assert (OUT/'ACOM_DELIVERY_VERIFY_R1.json').exists()
    run('BOARD_RELEASE_R1.json',[CLI,'liberar','F1.REDE','--quem',WHO,'--nota','Entrega registrada com evidencias novas; memórias e ACOM concluídas sob reivindicação. Liberada para auditoria da gerência.'],mutation=True)
elif mode=='verify':
    manifest=json.loads((OUT/'MANIFESTO_ARQUIVOS_R1.json').read_text(encoding='utf-8'))
    changed=[]
    for x in manifest['files']+manifest['work_sources']:
        if pin(x['path'])!=x:changed.append(x['path'])
    value={'all_match':not changed,'checked':len(manifest['files'])+len(manifest['work_sources']),'changed':changed,'at':dt.datetime.now(dt.timezone.utc).isoformat()}
    print(json.dumps(new('VERIFICACAO_FINAL_R1.json',value),ensure_ascii=False))
    if changed:raise RuntimeError(changed)
else:raise ValueError(mode)
