from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarRightAction_closed|scalarRightAction_regular|right_action_bounded_strong|rightAction.*strongStar'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_right_action_limits'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ScalarGNSClosedness.lean','scalarWeightGNSEmbedding_closed_of_bounded_strong'),('TGLExt/V350ScalarGNSStrongContinuity.lean','scalarGNSRepresentation_tendsto_of_uniformly_bounded'),('TGLExt/V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines'),('TGLExt/V350ScalarRegularRightGNS.lean','scalarRegularRightProduct'),('TGLExt/V350ScalarRegularRightPolar.lean','scalarTomitaPolarFactor_regular_left'),('TGLExt/V350ScalarTomitaPolarInvolution.lean','scalarTomitaPolarFactor_involutive'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','antiunitaryConjugate_apply')]


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
target='Extend the existing right action through actual bounded strong-star limits. For A in n_nu, b_i and b in the same core, ||b_i||<=C, b_i and b_i* tending strongly to b and b*, and already proved Lambda_nu(A b_i)=J pi(b_i*) J Lambda_nu(A), construct A b in n_nu and the same identity at b. J is scalarTomitaPolarFactor, not the tower J by name. Derive norm convergence of the right vectors from existing normality of pi and continuity of J; then consume full GNS closedness. Also exhibit the initial identity for each regular unitary by consuming existing regularRightGNS_intertwines and scalarTomitaPolarFactor_regular_left. Consumer: actual action of sqrt(B_epsilon) for the inverse-generator weight perturbation, LACUNAS_A1 item4. Do not claim any approximating net has been constructed, or that all of W*(Lambda) is reached.' 


stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_RIGHT_ACTION_LIMITS',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à passagem da ação direita por limites]\n\n# A1(b): ação direita e limites fortes-* limitados\n\n'+stamp+'\n\n'+target+'\n\nO fechamento do mapa GNS é fornecedor recém compilado, ainda em revisão. A continuidade forte limitada de π aplicada aos adjuntos produz a convergência dos vetores direitos. Não será inventada uma rede de aproximação de R: fornecê-la ou uma rota alternativa segue sendo a próxima obrigação. Sem novo tipo de representação.\n\n'

for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA.md',s.encode('utf8'));print('FICHE',len(providers))
