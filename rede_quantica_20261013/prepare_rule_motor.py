"""Pin existing v392 inputs and a prospective synthetic integration protocol."""
import ast, hashlib, json, os, re
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA.MOTOR'
CANON=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
names=['prove_decision_commutation','_recognition_reading_modes','_v361_pinch','_v361_herm_fn','_v361_flow']

def main():
    raw=(CANON/'um.py').read_bytes(); text=raw.decode('utf-8-sig'); tree=ast.parse(text)
    seal=json.loads((CANON/'um_absoluto_selo.json').read_bytes())
    manifest=json.loads((CANON/'tgl_kernel_proof_manifest.json').read_bytes())
    snap=OUT/'sources'; snap.mkdir(exist_ok=True)
    for name in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json']:
        data=(CANON/name).read_bytes(); dest=snap/name
        if not dest.exists():
            with dest.open('xb') as f: f.write(data)
        assert dest.read_bytes()==data
    funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
    assert set(funcs)==set(names)
    assignments={}
    for n in tree.body:
        if isinstance(n,ast.Assign):
            for target in n.targets:
                if isinstance(target,ast.Name) and target.id in ['SEALED_CODATA_ALPHA','ALPHA_FINE_CODATA_2018']:
                    assignments[target.id]=n
    assert set(assignments)=={'SEALED_CODATA_ALPHA'}
    alpha_lines=[(i,line) for i,line in enumerate(text.splitlines(),1) if re.fullmatch(r'ALPHA_FINE_CODATA_2018\s*=\s*[0-9.eE+\-]+',line)]
    assert len(alpha_lines)==1
    alpha=float(alpha_lines[0][1].split('=',1)[1])
    assert ast.literal_eval(assignments['SEALED_CODATA_ALPHA'].value)==alpha
    # Produce exact source text with original lines; no top-level program execution.
    exact='\n\n'.join(ast.get_source_segment(text,n) for n in [assignments['SEALED_CODATA_ALPHA'],*funcs.values()])+'\n'
    new(snap/'actual_consumer_functions.py',exact)
    flags={}; embedded={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Dict):
            for k,v in zip(node.keys,node.values):
                if isinstance(k,ast.Constant) and isinstance(k.value,str) and isinstance(v,ast.Constant):
                    if k.value.startswith('ext_kd_'): flags[k.value]=v.value
                    if k.value=='TGLExt/DecisionCommutation.lean': embedded[k.value]=v.value
    assert len(flags)==10 and len(embedded)==1
    for path,source in embedded.items():
        assert hashlib.sha256(source.encode()).hexdigest()==manifest['formal_files_sha256'][path]
    allowed={'propext','Classical.choice','Quot.sound'}
    evidence={}
    for flag,theorem in flags.items():
        axioms=manifest['axiom_report'][theorem]
        assert isinstance(axioms,list) and set(axioms)<=allowed
        evidence[flag]={'declaration':theorem,'axioms':axioms,'verified':True}
    new(OUT/'SOURCE_MANIFEST.json',{'unit':'F1.REGRA.MOTOR','canonical':[pin(CANON/n) for n in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json']],
        'copies':[pin(snap/n) for n in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','actual_consumer_functions.py']],
        'functions':{name:{'start':n.lineno,'end':n.end_lineno,'sha256':hashlib.sha256(ast.get_source_segment(text,n).encode()).hexdigest()} for name,n in funcs.items()},
        'alpha_source_line':alpha_lines[0][0],'recorded_kernel_evidence':evidence,
        'proof_basis':pin(OUT.parent/'F1.REGRA.P1/RESULTADO_PROVA_R1.json'),
        'reused_numeric_source':pin(ROOT/'Chatgpt/MOTOR_RECONHECIMENTO_20260915/test_recognition.py')})
    target_re=[[.25,0,0,0],[0,.25,0,0],[0,0,.25,0],[0,0,0,.25]]
    target_im=[[0,-.25,0,0],[.25,0,0,0],[0,0,0,.25],[0,0,-.25,0]]
    new(OUT/'PREREGISTRO_R1.json',{'unit':'F1.REGRA.MOTOR','statute':'INPUT — synthetic finite realization; not observed data',
       'operator':pin(OUT/'OPERADOR_VERBATIM.txt'),'sources':pin(OUT/'SOURCE_MANIFEST.json'),
       'law':'E(X)=C_plus X C_plus+C_minus X C_minus; T_t=E+exp(-Gamma*t)(I-E)',
       'rate':'beta=ALPHA_FINE_CODATA_2018*sqrt(e), Gamma=beta*tau_ref*omega_ref**2/2; tau_ref=omega_ref=1',
       'reference_units_only':True,'mu_do_rito':'q→0 (Thomson; Teorema da Escala)',
       'target_real':target_re,'target_imag':target_im,'target_fixed_before_execution':True,
       'initial_state':'Existing consumer psi=(1,i,1,-i)/2, rho=psi psi*; no alteration',
       'exposure_grid':{'start':0,'stop':12,'count':241},'exposure_checkpoints':[0,.25,.5,1,2,4,8,12],
       'tol_algebra':1e-12,'tol_rule':1e-10,'tol_ode_scaled':1e-7,'spectral_cutoff':1e-10,
       'rules':{'read_rule':'||E(state)-target||_HS<=tol_rule','raw_rule':'||state-target||_HS<=tol_rule',
           'scope':'Numerical tolerance is not exact Lean equality; fixed space has complex dimension 8, no universal unique fixed state.',
           'preflight':'Reject stale hashes, nonfinite/bool scalars, invalid state, invalid target, incomplete theorem evidence.'},
       'checks':['consumer all_verified from actual ten evidence records','reading_modes both pass','semigroup and E^2=E',
           'target is fixed; read_rule invariant along flow','strictly decreasing complement norm follows exponential',
           'raw_rule stays false on this finite grid','trace1, positivity, Hermiticity',
           'independent GKLS matrix exponential agrees','fixed-space dimension8',
           'new rule removes no original consumer output and does not move gate'],
       'negative_controls':['incompatible fixed target rejected','invalid numerical input refused',
           'zero rate leaves complement unchanged','negative rate refused','missing kernel evidence consumer refuses',
           'one-bit source corruption refused','idempotence of E alone does not force the prescribed target'],
       'run_kind':'bounded continuous-time simulation; not a resident daemon; JSONL ledger under sandbox only',
       'interpretation':'Rule contract INPUT/ONTO mapping; finite runtime verification REAL/COMPUTED; no physical confirmation.'})
    print(json.dumps({'source_manifest':pin(OUT/'SOURCE_MANIFEST.json'),'preregister':pin(OUT/'PREREGISTRO_R1.json'),'functions':names},ensure_ascii=False))

if __name__=='__main__': main()
