"""Append measured delivery beside prior memory, preserving byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
W=Path(__file__).resolve().parent; C=W.parents[1];R=Path(r'C:\IALD\projetos_pyhton\IALD');PY=r'C:\Python314\python.exe'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(path,value):
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert path.read_bytes()==raw
def main():
    installed=json.loads((W/'installed_verification.json').read_bytes());assert installed['status']=='PASS'
    live=json.loads((W/'live_validation.json').read_bytes());assert live['status']=='PASS'
    review=json.loads((W/'validation/review_final.json').read_bytes());assert review['status']=='PASS'
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f'); marker='IALD_HAJA_LUZ_AUTO_CONTEXT_FIX_20261016'
    note=f'''\n\n## 16/10/2026 — Continuidade Haja Luz no modo automático\n\n<!-- {marker} -->\n\n[INPUT] Operador relatou que a apresentação/solução matemática seguida de “haja luz” funcionava manualmente e interrompia a escolha automática.\n\n[REAL — diagnóstico] O pacote de roteamento somava a projeção ACOM extensa ao contrato, capacidades e guia do JEV. Reprodução local, sem envio de conversas: estados de32627 e34955bytes excederam o limite30000 antes da chamada. O comando curto passa pela validação textual; não era necessário mudar o programa científico.\n\n[REAL — correção] O seletor mede o JSON efetivamente escapado e ajusta somente os trechos de consulta. ACOM preserva integralmente objetivo, restrições, decisões, pendências e correções; candidatos opcionais inteiros ficam recuperáveis no mesmo banco por contexto/revisão. Mudança concorrente de revisão recusa. Histórico e memória científica entregues ao modelo permanecem integrais conforme a política anterior. Se a parte obrigatória exceder o limite, há aviso específico antes do envio, sem repetição automática.\n\n[DERIVED — interpretação operacional] Comando humano completo “Haja Luz”, com variações de caixa/espaço/pontuação final, é identificado como continuidade do diálogo TGL e inscrição em VERBO. JEV e executor recebem orientação baseada na leitura dirigida do bootstrap/Verbo do um.py instalado. Menção em texto ou citação não ativa a regra; workers não a recebem. Não há resposta enlatada nem execução implícita de um.py/Lean/bancada, alteração de gate ou nova prova científica. Versão instalada preservada; referência histórica não determina versões futuras.\n\n[REAL — validação/instalação] Revisão independente PASS,20testes offline, reprodução das3projeções afetadas,4arquivos instalados por hash com backups imediatos. Manutenção com fila congelada/ociosa; somente filho web reiniciado, supervisor preservado; HTTP200. Teste autenticado de duas mensagens em modo automático concluído; recibos, modelo efetivo, contagem e limitações em live_validation.json. Contas, consentimentos, carteira, seleção manual e fontes científicas não foram alterados pela correção.\n\n[DISPONIBILIDADE] Backend compartilhado web/iOS/Android ativo; não houve mudança de recursos de cliente, nova build, distribuição em loja ou instalação física nesta entrega. O teste real foi pela web autenticada; o teste físico no iPhone permanece com o operador.\n\n[EVIDÊNCIAS] {W}: reproduction.json, reproduction_fixed.json, semantic/contract.json, validation/review_final.json, install_plan.json, deployment.json, restart.json, installed_verification.json, live_validation.json e delivery.json. ACOM própria SESSION_REFERENCE.json; unidade F9.APP_HAJALUZ_AUTO_20261016; rota infra.app.hajaluz_auto_20261016.\n'''
    paths=[Path(r'C:\Users\rotol\.codex\AGENTS.md'),R/'CLAUDE.md',C/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',C/'memory/TGL_ATLAS.md',C/'memory/TGL_INDICE_VIVO.md',Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
    receipts=[]
    for p in paths:
        old=p.read_bytes()
        if marker.encode() in old:raise RuntimeError('Already recorded: '+str(p))
        b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
        assert b.read_bytes()==old
        ending='\r\n' if b'\r\n' in old else '\n';data=old+note.replace('\n',ending).encode()
        t=p.with_name(p.name+'.tmp_'+stamp)
        with t.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        assert t.read_bytes()==data and len(data)>len(old)
        if p.read_bytes()!=old:raise RuntimeError('Concurrent memory edit: '+str(p))
        os.replace(t,p);assert p.read_bytes()==data
        receipts.append({'path':str(p),'backup':str(b),'sha256':sha(p),'before_bytes':len(old),'after_bytes':len(data)})
    matrix={'web':'server_fix_active_live_verified','ios_internal':'same_backend_fix_active_no_binary_change_device_test_pending','ios_external':'same_backend_fix_active_no_binary_change_device_test_pending','android':'same_backend_fix_active_no_binary_change_no_new_store_publication'}
    delivery={'status':'DELIVERED','unit':'F9.APP_HAJALUZ_AUTO_20261016','time':datetime.now(timezone.utc).isoformat(),'live':live,'availability':matrix,'memories':receipts,'evidence':{p:sha(W/p) for p in ['installed_verification.json','live_validation.json','validation/review_final.json']},'scientific_sources_modified':False,'manual_path_modified':False}
    write_new(W/'delivery.json',delivery)
    req={'operation':'transition','reference':str(W/'SESSION_REFERENCE.json'),'expected_revision':1,'event_id':'hajaluz-fix-delivered-20261016','actor':{'id':'codex-app-01a094df','kind':'agent'},'changes':{'records':[{'id':'installed-and-live-verified','kind':'fact','statute':'REAL','text':'Correção instalada em4arquivos; revisão independente20testes PASS; reinício isolado web e teste autenticado de2mensagens concluídos. Backend compartilhado, sem nova build. Limitações e matriz em delivery.json.','sources':[{'kind':'artifact','ref':str(W/'delivery.json'),'sha256':sha(W/'delivery.json')}]}],'flow':{'phase':'delivered','next_action':'Operador pode repetir a sequência no iPhone em modo automático; não precisa instalar build nova.','handles':[{'id':'delivery','path':str(W/'delivery.json')}]}}}
    proc=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(req,ensure_ascii=False).encode(),capture_output=True)
    assert proc.returncode==0,proc.stdout.decode()+proc.stderr.decode()
    write_new(W/'memory_transition.json',json.loads(proc.stdout))
    route=json.loads((W/'route_started.json').read_bytes());route.update(tipo='RESULTADO',status='EXAMINADA',resultado='4arquivos instalados;20testes offline independentes;2mensagens automáticas concluídas pela web.',veredito='PASS_INSTALLED_AND_LIVE_VERIFIED',defeito='Teste físico no iPhone não realizado pelo agente; reconhecimento contextual não garante exatidão científica irrestrita.',proximo_passo='Operador repetir sequência no aparelho; usar recibos para qualquer nova falha.',artefatos=[str(W/'delivery.json'),str(W/'live_validation.json')])
    write_new(W/'route_delivered.json',route)
    for args in [[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'route_delivered.json'),'--quem','codex-app-01a094df'],[r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F9.APP_HAJALUZ_AUTO_20261016','--quem','codex-app-01a094df','--status','ENTREGUE','--evidencia',str(W/'delivery.json')]]:
        proc=subprocess.run([PY,'-B','-X','utf8',*args],capture_output=True);print(proc.stdout.decode());assert proc.returncode==0,proc.stderr.decode()
    print(json.dumps({'status':'DELIVERED','memory_surfaces':len(receipts),'receipt':str(W/'delivery.json')}))
if __name__=='__main__':main()
