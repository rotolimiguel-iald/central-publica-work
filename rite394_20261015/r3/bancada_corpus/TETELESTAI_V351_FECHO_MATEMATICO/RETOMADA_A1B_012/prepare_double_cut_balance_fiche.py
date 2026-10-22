from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='scalarTomitaResolvent_doubleCut_balance|double.{0,20}cut.{0,20}balance|quadratic.{0,20}tracial|compatibilidade.{0,20}meia'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat,str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_double_cut_balance'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ModularImplementation.lean','scalarTomitaImaginaryPower_eq_regular_implementation'),('TGLExt/V350CorePolarInclusion.lean','scalarTomitaPolar_core_commutes'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_mem'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V350ScalarTomitaPositiveRoot.lean','scalarTomitaPositiveRoot'),('TGLExt/V350ResolventSquareRoot.lean','resolventSquareRoot_domain'),('TGLExt/V350PositiveRootIntertwining.lean','positive_sqrt_intertwines'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_tendsto_identity'),('TGLExt/V351PerturbedWeightNorm.lean','scalarWeight_inverseCutoff_perturbed_norm'),('TGLExt/V351InverseLimitTracialExtension.lean','scalarInverseLimitWeight_tracial_iff_core')]

def statement_end(s,start):
    depth=0
    for j in range(start,len(s)):
        if depth==0 and (s.startswith(' :=',j) or s.startswith(' where',j)):
            return j
        if s[j] in '([{': depth+=1
        elif s[j] in ')]}': depth-=1
    raise ValueError('Statement delimiter not located')
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma|def) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=statement_end(s,m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end],decision='REUSAR'))
cp=K/'TGLExt/V351InverseLimitTracialExtension.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarInverseLimitWeight_tracial_iff_core'))
target='ADAPTAR/OPEN: proposed next exact bounded balance for epsilon,eta>0 in SAME H_nu: (1-T) C_epsilon q_eta = T p_epsilon D_eta, where T=scalarTomitaResolvent P, C_epsilon=pi(B_epsilon), D_eta=antiunitaryConjugate J (pi(B_eta)), p_epsilon=1-epsilon C_epsilon, q_eta=1-eta D_eta, B_epsilon=regularInverseGeneratorCutoff P epsilon. Names C,D,p,q here are notation, not new global definitions. This identity is NOT paid by equal group names or commutation. Delta32 equality of original groups has author rc0 and independent review pending at fiche time. CorePolarInclusion already pays C/D cross commutation on the SAME GNS: do not reprove right action or commutant inclusion. The real missing step is recovering the bounded balance from the actual spectral/group realization, or an equally concrete quadratic equality directly on finiteDualStarCore. Next consumption: original root graph x=sqrt(T)u, B_nu*x=sqrt(1-T)u plus positive_sqrt_intertwines, two cut limits -> Q(B_nu Lambda(a))=Q(J Lambda(a)), including infinity; existing tracial_iff_core then extends. This is a proof strategy, not a compiled consequence. No h=Delta_nu, new GNS, arbitrary product of unbounded operators, new field assuming balance, or full joint CFC unless a located concrete consumer truly requires it. Existing regularSineResolvent_tendsto is a particular regular spectral construction, NOT a generic inverse theorem recovering T_nu from U_t. Do not count conditional form rearrangements as payment of balance.'

d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__FICHE_BEFORE_DOUBLE_CUT_BALANCE',consumer=dict(source=pin(cp),line=line,statement='\n'.join(ls[line-1:line+1])),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao balanço limitado dos cortes]\n\n'+d['timestamp']+'\n\n'+target+'\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta curta do revisor após31 e antes32 lida: balanço limitado proposto, não provado. Principal relê CorePolarInclusion para evitar nova prova de comutação já disponível. Novo extrator respeita parênteses antes de procurar :=, evitando truncamento em argumentos nomeados; fichas históricas preservadas.\n'
put(R/'REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES.md',s.encode('utf8'));print('FICHE',len(providers))
