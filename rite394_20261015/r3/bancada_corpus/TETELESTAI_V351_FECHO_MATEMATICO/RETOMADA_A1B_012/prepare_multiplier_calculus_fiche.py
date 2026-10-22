from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='compactScalarRepresentation|compactScalarField|cfc.*[mM]ultiplier|[mM]ultiplier.*cfc'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_multiplier_calculus'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V350StrongOperatorField.lean','operatorFieldLift'),('TGLExt/V350StrongOperatorField.lean','operatorFieldLift_ae'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_constant'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_add'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_mul'),('TGLExt/V350OperatorFieldAlgebra.lean','operatorFieldLift_star'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier'),('TGLExt/V351ResolventPhaseCalculus.lean','resolventPhaseOperator'),('TGLExt/V351ResolventImaginaryPowers.lean','resolventImaginaryPower_damping'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean','StarAlgHom.map_cfc')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:@\[[^\n]*\] )?(?:noncomputable )?(?:def|theorem|lemma) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end],decision='REUSAR'))
target='For a continuous scalar g:R->[0,1], use the existing operatorFieldLift to represent C([0,1],C) as bounded operators on RegularHilbert H. Prove this is a unital complex star-algebra homomorphism, equals the existing realScalarMultiplier at the coordinate function, and transports continuous functional calculus. This pays the scalar-multiplier identification needed for resolventPhaseOperator and then regular_unitary_positive_generator. No new L2 space, operator-field machinery or imaginary-power definition.'
stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_MULTIPLIER_CALCULUS',consumer=dict(path=str(K/'TGLExt/V351ResolventPhaseCalculus.lean'),line=17,name='resolventPhaseOperator'),ultimate_consumer='regular_unitary_positive_generator',exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao cálculo funcional do multiplicador existente]\n\n# A1(b): cálculo funcional no mesmo L²\n\n'+stamp+'\n\n'+target+'\n\nO homomorfismo tem consumidor concreto: map_cfc e a fase do resolvente. A maquinaria de lift e sua álgebra são reutilizadas, não reprovadas. A busca negativa nos recortes não afirma ausência universal.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'.\n'
put(R/'REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR.md',s.encode('utf8'));print('FICHE',len(providers))
