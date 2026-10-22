"""Stage an explicitly incomplete operational addendum. Never apply memories."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
W=HERE.parent
PRIOR=W.parent/'acom_signal_transport_20261021/memory_prepare'
sys.path.insert(0,str(W))
import task

def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);raw=p.read_bytes()
    return dict(path=str(p),sha256=sha(raw),bytes=len(raw))
def new(p,raw):
    if not isinstance(raw,bytes):raw=json.dumps(raw,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(raw)
    if p.read_bytes()!=raw:raise ValueError('Stage write mismatch')

def main():
    project=task.project()
    preflight=task.check('delivery')
    out=HERE/'R1';out.mkdir(exist_ok=False)
    new(out/'PROJECT.json',project);new(out/'PREFLIGHT.json',preflight)
    paths=['release/deployment.json','release/CHECK_INSTALLED_R1.json',
           'release/mobile_stage/AUDIT.json','release/APK_PUBLICATION.json',
           'release/ANDROID_AUTH_DOWNLOAD.json','release/CHECK_APK_PUBLIC_R1.json',
           'release/IOS38_STARTED.json','LIVE_BUDGET_REFUSAL.txt']
    pins=[pin(W/p) for p in paths]
    installed=load(W/paths[1]);audit=load(W/paths[2]);download=load(W/paths[4]);ios=load(W/paths[6])
    if installed['files']!=11 or installed['status']!='PASS_WITH_SCOPE':raise ValueError('Deployment snapshot changed')
    if audit['status']!='PASS' or audit['versionCode']!=33 or download['status']!='PASS':raise ValueError('Android receipts changed')
    if audit['apk_sha256']!=download['sha256'] or sha(Path(download['path']).read_bytes())!=download['sha256']:raise ValueError('Downloaded APK mismatch')
    if ios['status']!='RUNNING' or ios['build']!='4.1(38)':raise ValueError('iOS snapshot changed; revise staging explicitly')
    refusal=(W/'LIVE_BUDGET_REFUSAL.txt').read_text(encoding='utf-8')
    if 'Entrada/preços não verificáveis; envio bloqueado.' not in refusal:raise ValueError('Expected live failure absent')
    marker='IALD_APP_ATTACHMENTS_BETA_PROGRESS_20261021'
    text='''

## 21/10/2026 — Anexos e indicador beta: progresso operacional, live pendente
<!-- IALD_APP_ATTACHMENTS_BETA_PROGRESS_20261021 -->
[INPUT — tarefa operacional] F9.APP_ANEXOS_BETA_20261021. Correção de anexos de imagem/documento e indicador beta animado enquanto a entrega está pendente. Este registro não altera teoria, ciência, kernel, selo ou gate.
[REAL — recibos locais conferidos nesta preparação] Integração de JS/CSS com backend repair; recibo de instalação e verificação cobre 11 arquivos. CHECK_INSTALLED_R1 registra PASS_WITH_SCOPE para bytes e fronteira HTTP anônima; não certifica sucesso da conversa autenticada. Os cinco pinos científicos foram preservados no recibo da instalação. Testes sintéticos e verificação de bytes não equivalem a acerto de modelo ou teste físico.
[REAL — Android] Android 4.1(33): auditoria de APK/AAB assinados PASS, certificado igual ao anterior; publicação aditiva e download autenticado com SHA256 igual ao APK auditado. Bytes do arquivo baixado novamente conferidos nesta preparação. Instalação física não verificada; Google Play não publicado por estes recibos.
[REAL/OPEN — iOS] IOS38_STARTED.json registra build 4.1(38) RUNNING, iniciada manualmente uma vez após não aparecer build nova. Commit vinculado: COMMIT_VALUE. Início não é conclusão nem distribuição. IALD Equipe e IALD Piloto ainda precisam dos recibos da build38 em testes; instalação física não verificada.
[REAL — negativo live preservado] LIVE_BUDGET_REFUSAL.txt registra “Entrada/preços não verificáveis; envio bloqueado.” no ensaio de imagem/PDF. Não declarar PASS live/final. O requisito backend_budget_r2 está em correção de backend; o parent informou que não haverá clientes novos nesta correção. O resultado do patch, instalação e novo ensaio ainda não foi verificado nesta preparação; não inferir causa resolvida nem sucesso posterior.
[OPEN — continuidade] Aguardar recibo do patch backend, revisão independente, pinos instalados e resultado live final; conferir também conclusão/distribuição iOS nos dois grupos. Preservar falha anterior e identificadores de execução; não repetir envio incerto. Este adendo é STAGING, não memória aplicada nem aceite da missão.
[REFERÊNCIA] REF_VALUE. Projeção própria recuperada para este staging; revisão é retrato, não permanente. Diário Claude em MEMORY_2.md, nunca no índice MEMORY.md. Nenhuma memória científica atualizada por esta etapa.
'''.replace('COMMIT_VALUE',ios['commit']).replace('REF_VALUE',str(task.REF))
    text+='[EVIDÊNCIAS] '+'; '.join(p['path']+' SHA256 '+p['sha256'] for p in pins)+'.\n'
    text+='<!-- END_'+marker+' -->\n'
    chunk=text.encode('utf-8')
    surfaces=load(PRIOR/'SURFACES.json')['surfaces']
    if len(surfaces)!=8:raise ValueError('Expected existing eight surfaces')
    items=[]
    for row in surfaces:
        target=Path(row['path']);before=target.read_bytes()
        if target.name.upper()=='MEMORY.MD' or marker.encode() in before:raise ValueError('Forbidden diary target or duplicate marker')
        items.append(dict(**row,before_sha256=sha(before),before_bytes=len(before),
            expected_after_sha256=sha(before+chunk),expected_after_bytes=len(before+chunk),
            operation='APPEND_ONLY_NOT_APPLIED',backup='Immediate raw bytes in SAME folder before atomic temp verification/replace; recheck CAS; never delete backup'))
    new(out/'APPEND.txt',chunk)
    new(out/'PLAN.json',dict(status='STAGING_PROGRESS_ONLY_BLOCKED_UNTIL_FINAL_LIVE',
        apply_allowed=False,final_snapshot=False,reference=str(task.REF),unit=task.UNIT,
        parent_owner=task.OWNER,projection_revision=project['receipt']['revision'],
        sources=pins,append=pin(out/'APPEND.txt'),surfaces=items,
        reuse=dict(surfaces=pin(PRIOR/'SURFACES.json'),helper_original=pin(PRIOR/'atomic_append.py'),helper_stage=pin(HERE/'atomic_append.py')),
        required_before_apply=['Final live receipt from parent, preserving initial negative','Refresh prose and exact source pins from final receipts','Refresh all eight target baselines; stale CAS refuses','Independent review and fresh parent preflight','Explicit parent release of memory application'],
        memory_applied=False,science_changed=False,board_updated=False))
    # Read-only check: originals must remain at their exact initial bytes.
    for row in items:
        if sha(Path(row['path']).read_bytes())!=row['before_sha256']:raise ValueError('Surface changed concurrently; staging stale')
    new(out/'CHECKS.json',dict(status='STAGING_ONLY_CHECKED',surfaces=8,
        unchanged_originals=8,source_receipts=len(pins),backup_helper_identical=sha((HERE/'atomic_append.py').read_bytes())==sha((PRIOR/'atomic_append.py').read_bytes()),
        applies_executed=0,final_live_pass_claimed=False,ios_available_claimed=False))
    print(json.dumps(dict(status='STAGING_PROGRESS_ONLY',surfaces=8,applied=0,path=str(out))))

if __name__=='__main__':main()
