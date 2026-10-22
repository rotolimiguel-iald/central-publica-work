"""Append only a measured completed backend delivery, preserving all previous memory."""
from pathlib import Path
from datetime import datetime
import ast,hashlib,json,os
import task

def main():
    task.project()
    assert task.check('verify')['ready']
    d=json.loads((task.W/'delivery.json').read_bytes())
    assert d['status']=='PASS'
    installed_path=task.W/'publication_fix/installed_verification.json'
    installed=json.loads(installed_path.read_bytes())
    live=json.loads((task.W/'live_validation.json').read_bytes())
    assert installed['status']==live['status']=='PASS'
    marker='IALD_V394_BACKEND_DELIVERED_20261019'
    text=f'''\n\n## 19/10/2026 — App/JEV e fila científica atualizados para v394
<!-- {marker} -->
[INPUT/REAL — autorização e escopo] Continuação da própria missão {task.REF}; aprovação humana específica da fila em QUEUE_EXPLICIT_APPROVAL.txt, transição normal aceita no quadro. Corrige ao lado a pendência dos adendos de preparação, preservados como história. A atualização não executou/importou um.py, não compilou Lean nem alterou o gate científico.

[REAL — implantação verificada] Commit público imutável e fontes conferidos contra a custódia;422tópicos e1423fontes formais. Kernelv5 preservado, fontes integrais recuperáveis. Verificados{installed['files_verified']}arquivos efetivos após instalação inicial e correção de dois rótulos operacionais de publicação. Planos revisados, backups de bytes, manutenção controlada somente do filho web e supervisor preservado. App e contratoJEV v394 carregados em processo novo. Haiku: {installed['haiku_permanent_tokens']}tokens permanentes medidos; contexto compartilhado e contagemSonnet próprios no recibo final, sem transferir contagem entre modelos. Conversa/histórico/atividade continuam sujeitos à admissão real de cada chamada. Somente dois limites de leitores Python foram ampliados; ACOM, HajaLuz, direitos, carteira e ordemKimi/MiMo preservados.

[REAL — fila] Snapshot imutável de13documentos/27654trechos revisado e ativado pela API existente com CAS. Fontes/chunks/linhas e recuperação em3modos conferidos; versões anteriores e pedidos fixados preservados. A geração vem do recibo queue_activation.json, não do nome de uma versão lembrada.

[REAL — teste e disponibilidade] Teste sintético autenticado no modo automático e continuidadeHajaLuz: resultado e limites em live_validation.json. Backend comum web/iOS/Android atualizado. Nenhum recurso de cliente foi alterado; não houve nova compilação ou distribuição em loja nesta entrega. Instalação física não verificada. Grupos TestFlight e publicação GooglePlay não foram reinspecionados para uma mudança exclusiva de servidor.

[EVIDÊNCIAS] {task.W}: delivery.json, install_plan.json, validation/review_final.json, queue_activation.json, deployment.json, restart.json, publication_fix/deployment.json, publication_fix/installed_verification.json, live_validation.json. O primeiro teste expôs PUBLICATION_PENDING obsoleto; sua evidência foi preservada, a correção mínima foi revisada e o teste final deve ser lido em live_validation.json. Leitura de memória não muda pesos, prova científica ou confirmação empírica. Reutilizar a mesma referência, não repetir testes/envios já encerrados.
<!-- END_{marker} -->
'''
    original=task.W.parent/'iald_monthly_wallet_20261007/record_memory.py'
    node=next(n for n in ast.parse(original.read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    ns={'Path':Path};exec(compile(ast.Module(body=[node],type_ignores=[]),'established_memory_paths','exec'),ns)
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for p in ns['paths']:
        old=p.read_bytes()
        if marker.encode() in old:rows.append({'path':str(p),'status':'already_present'});continue
        old.decode('utf-8-sig');raw=old+text.replace('\n','\r\n' if b'\r\n' in old else '\n').encode()
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==old
        tmp=p.with_name(p.name+'.tmp_v394_delivered_'+str(os.getpid()))
        with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw and p.read_bytes()==old
        os.replace(tmp,p);assert p.read_bytes()==raw and raw.startswith(old)
        rows.append({'path':str(p),'backup':str(bak),'sha256':hashlib.sha256(raw).hexdigest(),'status':'appended'})
    task.new('MEMORY_DELIVERY.json',{'status':'PASS','marker':marker,'surfaces':rows})
    print(json.dumps({'status':'PASS','surfaces':len(rows)}))

if __name__=='__main__':main()
