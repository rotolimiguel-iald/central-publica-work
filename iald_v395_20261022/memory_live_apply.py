"""Prepare/apply a reviewed additive operational memory note with byte backups."""
from pathlib import Path
from datetime import datetime
import ast,hashlib,json,os,sys
import task
W=Path(__file__).resolve().parent
MARK='IALD_APP_V395_LIVE_20261022'
def sha(b):return hashlib.sha256(b).hexdigest()
def prepare():
    d=json.loads((W/'FINAL_DELIVERY_R1.json').read_bytes())
    assert d['installed_verified']
    original=W.parent/'iald_monthly_wallet_20261007/record_memory.py'
    n=next(n for n in ast.parse(original.read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    paths=[Path(x) for x in ast.literal_eval(n.value.generators[0].iter)]
    paths += [Path(r'C:\IALD\Central de Patentes\memory\TGL_CORE_MEMORY.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\central-de-patentes-estado.md')]
    text=f'''\n\n## 22/10/2026 — Ciência v395 no app e JEV
<!-- {MARK} -->
[INPUT/REAL — codex-gerente-tgl] Ordem: atualizar tudo com a versão nova do um.py. Unidade F9.APP_V395_20261022; referência própria {task.REF}. Fontes v395 custodiadas/publicadas conferidas; fila v395 CURRENT e Bancada B5-v395 já atualizadas foram reaproveitadas. Custódia/site/repositório/dispositivos mantêm recibos próprios, sem repetir publicação.
[REAL — implantação local] Pacote científico com 425 tópicos e 1424 fontes formais, kernel v5 preservado, JEV atual reancorado. Plano somente dados/contratos/pacotes; Python operacional, carteira, consentimentos, memória de atividade e interface preservados. Backups de bytes, revisão independente, troca em janela ociosa e reinício somente filho web sob o mesmo supervisor. Hashes e loaders conferidos em processo novo. Seis chamadas COUNT de fontes públicas, zero geração nessa contagem; medidas vinculadas aos bytes por modelo, sem transferir tokens entre provedores. Admissão de conversas reais continua própria.
[ESCOPO] Nenhuma execução/importação de um.py ou Lean, alteração de kernel científico/gate ou nova prova. Psion segue condicional ao certificado sem habitante; a bijeção da v395 é de conjuntos. A implantação de memória não instala ciência nos pesos.
[DISPONIBILIDADE] Backend compartilhado web/iOS/Android atualizado sem mudança de cliente; nenhuma nova build ou distribuição de loja nesta entrega. Instalação física não verificada. Teste autenticado: {d['authenticated_live_status']}. Não presumir recarga de sessões/MCPs antigos ou atualização de conversas avulsas do Kimi Work.
[EVIDÊNCIAS] {W}: FINAL_DELIVERY_R1.json, INSTALLED_VERIFICATION.json, deployment.json, restart.json, validation/review_final.json, app/NATIVE_COUNTS_COMPLETE.json, QUEUE_CURRENT.json e BANCADA_CURRENT.json. Recuperar referência e recibos atuais antes de retomar.
<!-- END_{MARK} -->
'''
    rows=[]
    for p in paths:
        b=p.read_bytes();assert MARK.encode() not in b
        rows.append({'path':str(p),'baseline_sha256':sha(b),'baseline_bytes':len(b),'append_utf8':text.replace('\n','\r\n' if b'\r\n' in b else '\n')})
    task.new('MEMORY_LIVE_PLAN.json',{'marker':MARK,'surfaces':rows,'delivery_sha256':sha((W/'FINAL_DELIVERY_R1.json').read_bytes())})
def apply():
    assert task.check('verify')['ready']
    raw=(W/'MEMORY_LIVE_PLAN.json').read_bytes();plan=json.loads(raw)
    review=json.loads((W/'review/MEMORY_LIVE_REVIEW.json').read_bytes())
    assert review['status']=='PASS' and review['plan_sha256']==sha(raw)
    assert sha((W/'FINAL_DELIVERY_R1.json').read_bytes())==plan['delivery_sha256']
    pending=[]
    for row in plan['surfaces']:
        p=Path(row['path']);old=p.read_bytes();assert sha(old)==row['baseline_sha256']
        pending.append((p,old,old+row['append_utf8'].encode()))
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');receipts=[]
    for p,old,new in pending:
        assert p.read_bytes()==old
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==old
        tmp=p.with_name(p.name+'.tmp_'+MARK)
        with tmp.open('xb') as f:f.write(new);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==new and p.read_bytes()==old
        os.replace(tmp,p);assert p.read_bytes()==new and new.startswith(old)
        receipts.append({'path':str(p),'backup':str(bak),'before':sha(old),'after':sha(new),'append_only':True})
    task.new('MEMORY_LIVE_APPLIED.json',{'status':'PASS','surfaces':receipts})
if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()
