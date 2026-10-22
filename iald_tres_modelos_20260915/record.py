from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('memory_paths',WORK.parent/'iald_context_math_20260915/record_prepared.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def record(tag,title,note,evidence):
    receipt=WORK/(tag+'.json')
    assert not receipt.exists()
    now=datetime.now().astimezone()
    stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    marker='IALD_TWO_MODELS_'+tag.upper()
    rows=[]
    for path in module.TARGETS:
        before=path.read_bytes()
        assert marker.encode() not in before
        backup=path.with_name(path.name+'.bak_'+stamp)
        module.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n### '+now.strftime('%d/%m/%Y %H:%M %z')+' — '+title+'\n\n'
        addition+='<!-- '+marker+' -->\n\n'+note+'\n\nEvidências: '+str(WORK)+'\\'+tag+'.json\n'
        after=before+addition.replace('\n',newline).encode()
        temp=path.with_name(path.name+'.tmp_'+stamp)
        module.create(temp,after)
        assert path.read_bytes()==before,'Concurrent memory change: '+str(path)
        temp.replace(path)
        assert path.read_bytes()==after and len(after)>len(before)
        rows.append({'path':str(path),'backup':str(backup),'before_bytes':len(before),'after_bytes':len(after)})
    payload={'at':now.isoformat(),'title':title,'note':note,'memories':rows,**evidence}
    module.create(receipt,json.dumps(payload,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'receipt':str(receipt),'memories_updated':len(rows)}))

if __name__=='__main__':
    assert sys.argv[1]=='prepared'
    record('prepared','Dois modelos: ordem corrigida, quotas ×3 e build 16 preparada',
        '[INPUT] Retomada explícita pelo objetivo ORDEM_CODEX_20260915_TRES_MODELOS_SOL_LIMITES.md. Vale a errata SEM O SOL: T2 cancelada; T1 somente Nativa/Luna; T3.1/T3.2 preservam somente_limite_global na conta luiz; T3.3 triplica os valores listados e eleva o global compartilhado a US$3/dia. Kimi só em ordem posterior. A ordem autoriza código, .env somente cotas não secretas, build16, APK autenticado e push privado; nenhuma compra/chave nova.\n\n'
        '[REAL] Hashes iniciais conferiram com a errata. Implantados no disco rótulos por resposta provenientes do servidor, persistidos no histórico, rótulos das duas opções, gastos diários por modelo do SQLite e cotas exatas do documento. Não alterados outros campos de .env, contas ou regras de acesso. Ainda sem reinício para ativar. Seis testes novos Python e oito JS passaram. A guarda de escrita/rede foi reaproveitada de sync2, byte a byte. Baseline da suíte tinha os nove vermelhos descritos + teste CSP desatualizado; corrigido o teste para a exceção preexistente e autorizada http://localhost:8900, sem alterar a política. A primeira suíte após implantação detectou regressão no cancelamento por um yield novo de metadados; corrigido em stream_fix.json e suíte final ainda em execução neste registro.\n\n'
        '[REAL] APK/AAB16 recompilados, certificado comparado diretamente às builds14/15 e igual; APK apksigner e AAB jarsigner válidos, assets completos conferidos com www. Nove backups JS preservados fora das pastas empacotadas, em _backups_packaging; nenhum backup nos novos pacotes. Auditoria dos 173 arquivos do app passou, repositório rotolimiguel-iald/iald-app confirmado privado. Nenhum push ou entrega APK ainda, aguardando término da verificação. Apple autenticada, Xcode Cloud aberto.\n\n'
        '[OPEN] Concluir suíte final (sem vermelho novo), reiniciar somente filho web e testar UI/SSE/painel, publicar APK autenticado, push auditado em codex/mobile-release, acompanhar build16 e adicioná-la ao TestFlight IALD Equipe. Google Play ainda sem cadastro completo por D-U-N-S, fora das tarefas desta ordem; distribuição Android via APK conforme T4. Memória do gratuito permanece conforme proteções existentes, sem exceção para acomodar núcleo integral. Nenhum novo resultado físico/formal e nenhum gate alterado.',
        {'status':'PREPARED_PARTLY_INSTALLED_NOT_ACTIVE','server_restarted':False,'mobile_published':False,
         'live_suite_exec_session':86533,'goal_complete':False})
