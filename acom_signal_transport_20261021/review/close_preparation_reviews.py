"""Documentary pin/mask check only; never imports application wrappers."""
import copy, hashlib, json
from pathlib import Path
from datetime import datetime, timezone
W=Path(__file__).resolve().parent.parent
def sha(raw): return hashlib.sha256(raw).hexdigest()
def pin(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p),sha256=sha(b),bytes=len(b))
def read(p): return json.loads(Path(p).read_bytes())
def verify(e):
    b=Path(e['path']).read_bytes()
    assert sha(b)==e['sha256'],e['path']
    if 'bytes' in e: assert len(b)==e['bytes'],e['path']
    return b
def emit(name, data):
    data.update(reviewer='codex-readability-reviewer',created_utc=datetime.now(timezone.utc).isoformat(),new_tests=0,application_executed=False)
    p=W/'review'/name
    with p.open('xb') as f: f.write((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(pin(p)))

# Independent JSON spans, preserving every byte outside the two item values.
def members(text,start=0):
    decoder=json.JSONDecoder(); out={}; i=start
    while text[i].isspace(): i+=1
    assert text[i]=='{'; i+=1
    while True:
        while text[i].isspace() or text[i]==',': i+=1
        if text[i]=='}': return out
        key,end=decoder.raw_decode(text,i); i=end
        while text[i].isspace(): i+=1
        assert text[i]==':'; i+=1
        while text[i].isspace(): i+=1
        _,end=decoder.raw_decode(text,i); assert key not in out
        out[key]=(i,end); i=end
def outside(raw):
    text=raw.decode(); items=members(text,members(text)['items'][0])
    spans=sorted((len(text[:items[k][0]].encode()),len(text[:items[k][1]].encode())) for k in ('testflight_internal','testflight_external'))
    out=[]; pos=0
    for start,end in spans: out.append(raw[pos:start]); pos=end
    out.append(raw[pos:]); return out

A=W/'admin_deadlines37stage'; ap=A/'UPDATE_PLAN_R2.json'; plan=read(ap)
for e in read(A/'MANIFEST_R2.json')['files']: verify(e)
for e in [plan['source'],plan['final_gui_receipt'],*plan['gui_evidence'],*plan['reuse_sources']]: verify(e)
old=verify(plan['baseline']); new=verify(plan['candidate']); mask=json.loads(verify(plan['strictmask']))
assert Path(plan['destination']).read_bytes()==old
assert outside(old)==outside(new)
assert [dict(bytes=len(b),sha256=sha(b)) for b in outside(old)]==mask['outside_segments']
b=json.loads(old); a=json.loads(new); other=copy.deepcopy(a)
for k,count in [('testflight_internal',1),('testflight_external',6)]:
    item=a['items'][k]
    assert item['build']=='4.1 (37)' and item['status']=='Em testes' and item['testers']==count
    assert item['expires_at'] is None and item['observed_utc'] is None
    assert item['source_reference']==plan['source']
    other['items'][k]=b['items'][k]
assert other==b
emit('ADMIN_DEADLINES37_REVIEW_R2.json',dict(status='PASS',scope='Aplicação administrativa R2 autorizável pelo pai: somente os dois subobjetos TestFlight, sem restart/chat.',plan=pin(ap),plan_sha256=pin(ap)['sha256'],wrapper=pin(A/'apply_admin37_R2.py'),candidate=plan['candidate'],strictmask=plan['strictmask'],manifest=pin(A/'MANIFEST_R2.json'),findings=[],checks=['Pins atuais e baseline conferidos','Máscara independente: todos os bytes externos idênticos','GUI e evidências pinadas; build37 Equipe1/Piloto6; expiração/timestamp exatos desconhecidos','Leitura estática do wrapper: review+SHA, plano fixo, allowlist, fontes, CAS, intenção exclusiva, backup imediato, fsync, replace e snapshot posterior'],application_conditions=['Pai fornece este parecer e seu SHA, confere hash do wrapper e mantém escritores concorrentes quiescentes.','Intenção existente exige reconciliar estado; não repetir aplicação.'],limitations=['Sem execução do wrapper nesta revisão.','Campo histórico no_apply_helper do plano precede o wrapper; este parecer cobre explicitamente o wrapper agora pinado.']))

M=W/'memory_prepare'; mp=M/'FINAL_R1/PLAN.json'; p=read(mp)
for e in p['receipts']+[p['append']]: verify(e)
chunk=Path(p['append']['path']).read_bytes()
assert len(p['surfaces'])==8
for item in p['surfaces']:
    raw=Path(item['path']).read_bytes()
    assert sha(raw)==item['before_sha256'],item['path']
    assert sha(raw+chunk)==item['expected_after_sha256'],item['path']
emit('MEMORY_PREPARE_REVIEW_R1.json',dict(status='PASS',task_id='memory_prepare',scope='Preparação e aplicação pelo pai do plano FINAL_R1 nas oito superfícies; não equivale a aplicação concluída nem aceite de deployment.',plan=pin(mp),plan_sha256=pin(mp)['sha256'],wrapper=pin(W/'apply_final_memory.py'),helper=pin(M/'atomic_append.py'),append=p['append'],evidence=[pin(W/'review/memory_final_r1/TEST_RESULTS.json'),pin(W/'review/MATERIAL_FINAL_CHECKS_R1.json')],findings=[],checks=['Oito before/after pins atuais e recibos fonte conferidos','APPEND preserva estatutos e limitações, sem promoção científica','Helper: backup byte a byte na mesma pasta, escrita temporária fsync, CAS e restauração em divergência pós-escrita','Wrapper: check deployment, preflight de todas as superfícies e fontes antes da primeira escrita; sem --apply não aplica','Oito testes anteriores reutilizados; nenhum novo teste'],application_conditions=['Pai compara imediatamente os SHA do plano, wrapper e helper com este parecer antes de executar Python sem -O; o wrapper depende desse precheck externo.','Conservar exclusividade de escrita durante aplicação.','Se houver interrupção parcial, reconciliar hashes e backups por superfície antes de qualquer continuação.'],limitations=['Atomicidade por arquivo, não transação entre oito arquivos.','Nenhuma memória aplicada nesta revisão.']))
