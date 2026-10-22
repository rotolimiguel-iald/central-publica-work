from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,s):
    assert not p.exists() and p.is_relative_to(R)
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
base=json.loads((R/'REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE.json').read_text(encoding='utf8'))
specs=[('TGLExt/V351RegularDomainCut.lean','regularDomainCut_right'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_product_bound'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_tendsto_identity'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V351PerturbedWeightOrder.lean','scalarWeight_right_perturbed_mono'),('TGLExt/V351ScalarWeightSemifiniteness.lean','scalarWeight_square_finite_wot_closure')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:def|theorem) '+name+r'\b',s,re.M);assert m
    a=m.start();depth=0
    for i in range(a,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and s.startswith(' :=',i):break
    providers.append(dict(source=pin(p),name=name,line=s[:a].count('\n')+1,statement=s[a:i]))
target='Consumer of the previously searched domain-cut route: for a in the ORIGINAL n_nu, show tau((a q_delta)* (a q_delta)) <= ofReal(delta^-1) nu(a*a) < infinity, then use q_n -> I strongly and the OLD WOT closure of n_nu to prove WOT closure of the square-finite set of the SAME tau is the same N. No new weight, square-root or cone. No traciality or finite-positive-minorant contract asserted. The old WOT theorem is imported from source, not re-proved.'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_LIMIT_SEMIFINITE_CONSUMER',exact_target=target,decision='ADAPTAR',searches=base['searches'],reused_full_six_mode_fiche=pin(R/'REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE.json'),providers=providers)
put(R/'REAPROVEITAMENTO_A1B_SEMIFINITUDE_LIMITE.json',json.dumps(d,ensure_ascii=False,indent=2))
s='[OPEN — ficha anterior ao consumidor de semifinitude usual]\n\n'+d['timestamp']+'\n\n'+target+'\n\nReaproveita as seis modalidades e outras bancadas da ficha do corte de domínio, cujo alvo já incluía este consumidor. Não repete a varredura integral nem cria outra raiz. Consulta independente foi lida inteira.\n\n'
for q in providers:s+=q['source']['path']+':'+str(q['line'])+' — '+q['source']['sha256']+'\n\n```lean\n'+q['statement']+'\n```\n\n'
put(R/'REAPROVEITAMENTO_A1B_SEMIFINITUDE_LIMITE.md',s)
s=(R/'dev_compile_domain_cut.py').read_text(encoding='utf8')
for a,b in [('domain_cut','inverse_limit_semifinite'),('V351RegularDomainCut','V351InverseLimitSemifiniteness'),('REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE','REAPROVEITAMENTO_A1B_SEMIFINITUDE_LIMITE')]:s=s.replace(a,b)
put(R/'dev_compile_inverse_limit_semifinite.py',s)
s=(R/'run_existing_contract_dependency.py').read_text(encoding='utf8')
s=s.replace('V351RegularCoreTraceContract','V351ScalarWeightSemifiniteness').replace('existing_contract_dependency_attempts','existing_semifinite_dependency_attempts').replace('AUDITORIA_LEIS_PESO_LIMITE_A1B','AUDITORIA_CORTE_DOMINIO_A1B')
put(R/'run_existing_semifinite_dependency.py',s)
