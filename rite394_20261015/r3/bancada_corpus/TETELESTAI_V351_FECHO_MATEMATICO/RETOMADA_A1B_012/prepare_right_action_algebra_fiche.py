from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='ScalarPolarRight|scalarPolarRightAlgebra|scalarRightAction_cfc|right_action_cfc'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_right_action_algebra'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ScalarGNSClosedness.lean','scalarWeightGNSEmbedding_of_cut_actions'),('TGLExt/V351ScalarGNSClosedness.lean','scalarGNSCutMap_weight_embedding'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_regular'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_closed_of_bounded_strongStar'),('TGLExt/V350ScalarGNSAction.lean','scalarGNSAmbientAction_norm_le'),('TGLExt/V350DualOrbitRepresentation.lean','dualOrbitRepresentation'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','antiunitaryConjugate_mul'),('.lake/packages/mathlib/Mathlib/Topology/Algebra/Group/Basic.lean','Set.isClosed_centralizer'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Range.lean','cfc_mem')]


providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:noncomputable )?(?:def|theorem|lemma) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end],decision='REUSAR'))
target='Construct a norm-closed star subalgebra of the EXISTING core, consisting of b and b* for which the actual original polar right identity holds on ALL n_nu. Characterize the property by the existing natural cut equations (of_cut_actions), so closedness follows from equality of continuous maps, without a new GNS or trace. Map this algebra by the same core inclusion into ambient bounded operators; the ambient image is closed since the core is a norm-closed bicommutant. Consume mathlib cfc_mem in the ambient CFC to pass the right identity to continuous functions. Consumer: (a) R_n=sigmoid(n sin(k/n)), with k determined by Lambda, to obtain the right action of actual R by bounded strong limits; (b) sqrt(B_epsilon) as an identified continuous function of R. Do not assume a CFC or CompleteSpace instance on N and do not claim that R_n convergence, identification of sqrt(B_epsilon), the trace or traciality are proved by this step.' 


stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_RIGHT_ACTION_CFC',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à passagem da ação direita por CFC]\n\n# A1(b): a álgebra fechada que permite consumir cfc_mem\n\n'+stamp+'\n\n'+target+'\n\nO novo empacotamento algébrico tem consumidor preciso: cfc_mem exige uma subálgebra estrela fechada, e transportará a identidade direita já produzida. Não é nova realização do core ou novo operador. O fechamento GNS foi aceito; os limites da ação direita têm auditoria autoral rc0 e aguardam revisão neste instante.\n\n'

for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA.md',s.encode('utf8'));print('FICHE',len(providers))
