from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('ContinuousModularMultipliers','SpectralHilbert'),('ContinuousModularResolvent','bounded_spectral_multiplier_nonneg'),('ContinuousModularDomain','continuousModularOperator'),('ContinuousModularDomain','continuous_modular_graph_iff')]
rows=[]
for mod,name in specs:
    p=K/'TGLExt'/f'{mod}.lean';s=p.read_text(encoding='utf8');m=re.search(r'^(?:abbrev|def|theorem) '+name+r'\b',s,re.M);assert m
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    statement=s[start:end]
    if name=='SpectralHilbert':statement=s[start:s.index('\n',start)]
    rows.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=statement))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='REUSE_REFINEMENT__SCALAR_PREDECESSOR_TYPED',original_fiche=pin(R/'REAPROVEITAMENTO_A1B_GERADOR_POSITIVO.json'),providers=rows,decision='ADAPTAR only vector-valued multiplier positivity; REUSAR bounded/resolvent graph infrastructure',reason='SpectralHilbert is fixed to Lp Complex 2 volume. The present consumer is Lp (TowerHilbert P) 2 volume. No existing isometry/intertwiner identifies those multiplication representations. Do not substitute by homonym or assume equal Hilbert-space dimensions preserve the core.',not_reproved='Graph/domain/selfadjointness theorems are consumed from generic resolventGraphOperator. Existing scalar construction remains unchanged.')
put(R/'ADENDO_GERADOR_ANTECEDENTE_ESCALAR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[REAL — antecedente localizado, com diferença de tipo explícita]\n\n# A1(b): reaproveitamento da construção escalar 049–050\n\n'+d['timestamp']+'\n\nA leitura do cabeçalho de BoundedGraphOperator levou às fontes ContinuousModular*. Elas já contêm o multiplicador exponencial positivo, domínio denso e autoadjunção. Contudo SpectralHilbert é fixado a Lp ℂ 2 volume. O alvo desta retomada tem fibra TowerHilbert P. A identificação entre espaços e suas representações não vem do nome nem de uma isometria abstrata.\n\nDecisão: adaptar a positividade ao multiplicador vetorial que a casa já tem. Consumir o resolventGraphOperator genérico para construir e provar as propriedades do grafo, sem repetir essas provas. A construção escalar não é reescrita. A identificação espectral, afiliação e escala do novo grafo continuam obrigações posteriores.\n\n'
for q in rows:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
put(R/'ADENDO_GERADOR_ANTECEDENTE_ESCALAR.md',s.encode('utf8'));print('Scalar predecessor recorded',len(rows))
