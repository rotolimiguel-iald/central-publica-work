"""Static source census and exact synthetic controls; never imports um.py."""
import ast, hashlib, itertools, json, math, re
from fractions import Fraction as F
from pathlib import Path

root = Path(__file__).resolve().parent
source = root/'um_ordens003_004_snapshot.py'
data = source.read_bytes()
text = data.decode('utf-8-sig')
lines = text.splitlines()
tree = ast.parse(text)
functions = {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
def owner(line):
    return next((n.name for n in functions.values() if n.lineno<=line<=n.end_lineno),'module')
def write(name,content):
    p=root/name
    assert not p.exists(),p
    payload=content.encode('utf-8')
    tmp=p.with_suffix(p.suffix+'.tmp')
    with tmp.open('xb') as f:f.write(payload)
    assert tmp.stat().st_size==len(payload)
    tmp.rename(p)

# Complete lexical census for explicit names and output keys, plus a conservative
# downstream census for their verdict containers. No claim of general dynamic taint solving.
pattern=re.compile(r'in_window|GA_ACCEPTED_WINDOW|in_accepted_window|mass_in_window|accepted_mass_window|accepted_window_Msun|mass_rule|_ga_range|gr_in_window|alive_beta_eq_alpha_sqrt_e_and_in_window|sub_a_conservation|link_closed|identity_true|\["IDENTITY"\]|\["chain_certificates"\]|\["haja_luz_subverdicts"\]|\["fiat_lux"\]|\["fiat_lux_counterfactual"\]')
rows=[]
for i,line in enumerate(lines,1):
    if pattern.search(line):
        role=('declaracao/comentario' if line.lstrip().startswith('#') else
              'emissor/serializacao' if any(w in line for w in ['print(','md.append','r"','seal =','"mass_rule"']) else
              'consumidor/propagacao: conferir contexto')
        rows.append({'line':i,'function':owner(i),'role':role,'source':line})
gate=functions['prove_qg_closure_gate']
evaluator=functions['evaluate_quantum_gravity_closure']
gate_names={n.id for fn in [gate,evaluator] for n in ast.walk(fn) if isinstance(n,ast.Name)}
forbidden={'GA_ACCEPTED_WINDOW_Msun','in_window','identity_verdict','prove_fiat_lux_counterfactual','identity_true'}
assert not gate_names & forbidden
gate_calls=[{'line':n.lineno,'call':ast.unparse(n)} for n in ast.walk(tree)
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='prove_qg_closure_gate']

# Evaluate the exact three decision expressions, not a replacement implementation.
targets={}
for fn,key in [('identity_verdict','sub_a_conservation'),('identity_verdict','link_closed'),
               ('prove_fiat_lux_counterfactual','alive_ok')]:
    found=[n for n in ast.walk(functions[fn]) if isinstance(n,ast.Assign) and
           any(isinstance(t,ast.Name) and t.id==key for t in n.targets)]
    assert len(found)==1
    targets[key]=found[0]
class WithoutWindow(ast.NodeTransformer):
    def visit_BoolOp(self,node):
        node=self.generic_visit(node)
        if isinstance(node.op,ast.And):
            node.values=[v for v in node.values if not
                ('in_window' in ast.unparse(v) or
                 (isinstance(v,ast.Compare) and 'M_GA_Msun' in ast.unparse(v)))]
            if len(node.values)==1:return node.values[0]
        return node
expressions={}
for name,node in targets.items():
    old=ast.unparse(node.value)
    new=ast.unparse(WithoutWindow().visit(ast.parse(old,mode='eval')).body)
    expressions[name]={'line':node.lineno,'old':old,'proposed':new}

controls=[]
for internal,window,em,alive_identity in itertools.product([False,True],repeat=4):
    env={'internal':{'synthetic_internal':internal},'_v3_keys':set(),
         'in_window':{'synthetic_mass':window},'em_face':{'em_identity_closes':em},
         'alive':{'beta':F(1,2) if alive_identity else F(1,3),'M_GA_Msun':F(2) if window else F(4)},
         'beta_live':F(1,2),'lo':F(1),'hi':F(3)}
    measured={key:{kind:bool(eval(expr,{'__builtins__':{},'bool':bool,'all':all,'abs':abs,**env}))
                  for kind,expr in vals.items() if kind!='line'} for key,vals in expressions.items()}
    assert measured['link_closed']['old']==(internal and window)
    assert measured['link_closed']['proposed']==internal
    assert measured['sub_a_conservation']['proposed']==(internal and em)
    assert measured['alive_ok']['proposed']==alive_identity
    controls.append({'inputs':[internal,window,em,alive_identity],'outputs':measured})

# Pure dephasing with retention c is a convex mixture of I and Z channels.
# Exact synthetic states/observables; no astronomical dataset.
c=F(1,2)
rho=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
out=[[rho[i][j]*(1 if i==j else c) for j in range(2)] for i in range(2)]
assert [out[i][i] for i in range(2)]==[F(1,2),F(1,2)]
assert sum(out[i][i] for i in range(2))==1
pplus=sum(sum(row) for row in out)/2
assert pplus==F(3,4)
assert c**4==F(1,16)
ALPHA_FINE_CODATA_2018=1/137.035999084
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
tau=5.391247e-44 # INPUT, Planck-time illustration, not fitted and not measured here.
rate=0.5*beta*tau*(1e15)**2
result={'source_sha256':hashlib.sha256(data).hexdigest().upper(),'source_lines':len(lines),
        'census':rows,'decision_expressions':expressions,'synthetic_truth_table':controls,
        'qg_gate_functions':{'prove_qg_closure_gate':[gate.lineno,gate.end_lineno],
                             'evaluate_quantum_gravity_closure':[evaluator.lineno,evaluator.end_lineno]},
        'gate_forbidden_identifiers_found':sorted(gate_names&forbidden),'gate_calls':gate_calls,
        'dephasing_exact':{'retention':str(c),'population_unchanged':True,'P_plus_after':str(pplus),
                           'retention_double_frequency_gap':str(c**4)},
        'illustrative_rate':{'alpha_input':ALPHA_FINE_CODATA_2018,'beta_runtime':beta,
                            'tau_input_s':tau,'frequency_gap_rad_s':1e15,'rate_s_inverse':rate},
        'scope':'Static census and synthetic expression controls only. No execution of um.py, no observational test.'}
write('D1_D7_CONTROLES.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
table=['# Censo D1 — snapshot estático','',f"[REAL — script] SHA256 `{result['source_sha256']}`; {len(lines)} linhas.",
       '', 'Censo lexical completo para os nomes/chaves explicitados no script; propagação por contêineres é conservadora. Não é uma prova de análise de fluxo dinâmica para Python arbitrário.',
       '', '| Linha | Função | Papel | Fonte |','|---:|---|---|---|']
for row in rows:
    table.append('| '+str(row['line'])+' | '+row['function']+' | '+row['role']+' | `'+row['source'].strip().replace('|','\\|').replace('`',"'")+'` |')
write('D1_CENSO_CONSUMIDORES.md','\n'.join(table)+'\n')
patch=['# PROPOSTA — NÃO APLICADA','',f"Snapshot: {result['source_sha256']}",'',
       'As três substituições decisórias são extraídas por AST; os ajustes editoriais complementares estão no parecer.','']
for name,entry in expressions.items():
    patch+=['```diff',f"@@ {name}, linha {entry['line']} @@",'- '+name+' = '+entry['old'],
            '+ '+name+' = '+entry['proposed'],'```','']
write('D1_PROPOSTA_DIFF.md','\n'.join(patch))
print(json.dumps({'source_sha256':result['source_sha256'],'census_rows':len(rows),
    'truth_table_rows':len(controls),'gate_calls':gate_calls,'rate':rate},ensure_ascii=False))
