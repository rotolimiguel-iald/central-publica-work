from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert not p.exists() and p.is_relative_to(R)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
attempt=R/'existing_contract_dependency_attempts/20260914_225600_779024/run.json'
run=json.loads(attempt.read_text(encoding='utf8'));assert run['returncode']==0 and run['sources_unchanged_during_build']
sources=[pin(R/'k/TGLExt'/n) for n in ['V351RegularCoreTraceContract.lean','V350CoreContractCounterexample.lean']]
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='REAL__EXISTING_DEPENDENCY_COMPILED__NO_NEW_THEOREMS',sources=sources,run=pin(attempt),
    initial_failure=pin(R/'dev_inverse_limit_scaling/20260914_225510_147391/run.json'),
    reason='The existing positiveDual definition lives in V351RegularCoreTraceContract. Its source is inherited and unchanged. The first DEV failed before reading the target because this object was absent. Lake compiled the original contract and its original counterexample import; neither is a new result or replacement contract. Prior source manifest checked. Subsequent author acceptance requires full Lake build and independent reviewer-owned objects.')
put(R/'ADENDO_FICHA_ESCALA_DEPENDENCIA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
text='[REAL — dependência original compilada]\n\n# A1(b): reaproveitamento do cone e da ação existentes\n\n'+d['timestamp']+'\n\n'+d['reason']+'\n\nA primeira tentativa falhou ANTES de ler a prova. Nenhuma fonte antiga foi modificada. Não se soma a compilação de fornecedor ao número de teoremas novos.\n\n'
for q in sources:text+=q['path']+' — '+q['sha256']+'\n\n'
text+='Run: '+str(attempt)+'\n'
put(R/'ADENDO_FICHA_ESCALA_DEPENDENCIA.md',text.encode('utf8'))
