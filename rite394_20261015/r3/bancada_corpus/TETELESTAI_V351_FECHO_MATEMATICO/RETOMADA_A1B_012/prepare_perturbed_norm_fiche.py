from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_perturbed_weight_norm'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','ScalarPolarRight'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSEmbedding_norm_sq'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','antiunitaryConjugate_apply'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight_normal'),('TGLExt/V350DualFixedWeightLaws.lean','PositiveCoreInput.conjugate')]



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
target='For P, b in the same scalarPolarRightAlgebra and A in n_nu, prove dualQuadraticIntegral(star b.val*(star A.val.val*A.val.val)*b.val)(regularVacuum P) = ENNReal.ofReal(norm(scalarGNSRepresentation P (star b) ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)))^2). Obtain A*b membership from the already proved right identity, rewrite the GNS norm-square and use the isometry of the SAME J. Consumer: bounded cut perturbations with b=hilbertPositiveSqrt(B_epsilon), already constructed. This only gives values on squares of n_nu; do not claim it extends to all positive inputs, proves monotonicity in epsilon, or gives a trace. PositiveCoreInput.conjugate is only a pattern because it requires b in dualFixedCore, whereas our cut lies in regularCoreAlgebra; do not pass it by homonym or claim theta-fixity.'



stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à identidade de norma do peso perturbado]\n\n# A1(b): consumir a ação dos cortes nos valores do peso\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: a identidade da ação direita já fornece Ab no domínio e seu vetor GNS. Basta a ponte algébrica para a norma do peso; não criar outra realização, peso escalar ou inscrição. A normalidade/aditividade de ν são fornecedores, não novos alvos. Não usar a caracterização falsa por minorantes positivos finitos para ν. A passagem a todos positivos e a tracialidade são obrigações posteriores nomeadas, não consequências deste lema isolado.\n\n'


for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA.md',s.encode('utf8'));print('FICHE',len(providers))
