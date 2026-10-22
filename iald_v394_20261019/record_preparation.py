"""Append preparation status on the established memory surfaces; never claim activation."""
from pathlib import Path
from datetime import datetime
import ast,hashlib,json,os
import task

def main():
    task.project()
    old_script=task.W.parent/'iald_monthly_wallet_20261007/record_memory.py'
    assignment=next(n for n in ast.parse(old_script.read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    ns={'Path':Path}
    exec(compile(ast.Module(body=[assignment],type_ignores=[]),'established_memory_surface_paths','exec'),ns)
    marker='IALD_V394_PREPARED_NOT_ACTIVATED_20261019'
    source=task.W/'PREPARATION_STATUS_R2.json'
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    text=f'''\n\n## 19/10/2026 — Preparação da v394; ativação pendente
<!-- {marker} -->
[REAL — preparação, sem instalação] Pedido próprio de atualizar tudo para v394, referência {task.REF}. Quarenta artefatos custodiados conferidos por hash; programa e selo v394 lidos, sem execução/importação de um.py ou Lean. Preparados422tópicos, kernel preservado e recuperação integral no JSON científico. Dois limites de leitura de10MB para32MB preparados e revisados independentemente; não instalados. A representação de contexto para OpenAI/Sonnet foi ajustada em staging; revisãoR2 e admissão nativa final ainda pendentes.

[REAL/OPEN — versões distintas] App permanecev392 e fila científicav393 nas últimas leituras; Bancada já informa implantaçãoB4-v394-20261019-R1 em consulta somente leitura. O espelho recebeu arquivosv394 em edição, mas HEAD local e origin/main ainda mostram a publicação anteriorv392. Não inferir commit, URL, ativação ou disponibilidade no app. PacotesHaiku877536/shared395669tokens são medições de staging, não prova de carregamento ou de admissão dos bytes finais.

[OPEN — bloqueio concreto] A revisão automática recusou mudar F0.3.MEMORIA_CIENTIFICA_SYNC deAGUARDA_OPERADOR paraEM_CURSO. Pergunta específica ao operador permanece pendente; não contornar por nova unidade nem preparar/ativar snapshot sem a resposta. Depois: conferir publicação imutávelv394, revincular pacotes, contar os payloads finais por modelo, revisar e implantar de forma controlada. Preservar fontes, carteira, contas, consentimentos, atividade e correçãoHajaLuz.

[DISPONIBILIDADE] Nenhuma troca de runtime, reinício, compilação mobile ou distribuição em loja nesta preparação. A mudança de ciência é do backend compartilhado; nova build só se o cliente mudar. Nenhuma instalação física conferida. Recibo: {source}; SHA256{sha}. Retomar pela referência própria, sem adotar missão de outra sessão.
<!-- END_{marker} -->
'''
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    rows=[]
    for p in ns['paths']:
        before=p.read_bytes()
        if marker.encode() in before:
            rows.append({'path':str(p),'status':'already_present'});continue
        before.decode('utf-8-sig')
        addition=text.replace('\n','\r\n' if b'\r\n' in before else '\n').encode()
        after=before+addition
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(before);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==before
        tmp=p.with_name(p.name+'.tmp_v394_prepared_'+str(os.getpid()))
        with tmp.open('xb') as f:f.write(after);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==after and len(after)>len(before)
        assert p.read_bytes()==before,'Concurrent memory edit: '+str(p)
        os.replace(tmp,p)
        assert p.read_bytes()==after and after.startswith(before)
        rows.append({'path':str(p),'status':'appended','backup':str(bak),'sha256':hashlib.sha256(after).hexdigest()})
    task.new('MEMORY_PREPARATION_R2.json',{'status':'PREPARATION_ONLY','marker':marker,'surfaces':rows})
    print(json.dumps({'status':'PREPARATION_ONLY','surfaces':len(rows),'activation':False}))

if __name__=='__main__':main()
