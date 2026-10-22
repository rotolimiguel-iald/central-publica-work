from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularSineApprox|sine.*resolvent|resolvent.*sine|sigmoid.*sin|realScalarMultiplier.*tendsto'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_sine_resolvent'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','scalarRightAction_cfc'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra_regular_mem'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_closed_of_bounded_strongStar'),('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),('TGLExt/V351ScalarMultiplierCalculus.lean','realScalarMultiplier_cfc_ae'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_norm_le'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent'),('TGLExt/V351RegularGeneratorAffiliation.lean','regularSpectralResolvent_mem'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Trigonometric/Sinc.lean','continuous_sinc'),('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean','tendsto_one_div_add_atTop_nhds_zero_nat')]



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
target='Construct actual b_n in the SAME regularCoreAlgebra P with b_n and b_n* satisfying the original polar right identity, uniform norm at most 1, and strong-star limit regularSpectralResolvent P. Use m=n+1, X_m=1/2 I + (1/(4i))(Lambda_{-1/m}-Lambda_{1/m}), g_m(x)=(1+sin(2*pi*x/m))/2, f_m(z)=sigmoid(m*(2*Re(z)-1)), b_n=cfc(f_m,X_m). Prove spectral identity with the same regularSpectralCoordinates, then symbol sigmoid(m*sin(2*pi*x/m)) convergence to sigmoid(2*pi*x). Reuse cfc_mem through scalarRightAction_cfc, bounded strong-star closure and L2 dominated convergence. The final consumer is P(R) and hence sqrt(B_epsilon) after a separate exact CFC identification. No norm convergence, no monotonicity b_n, no bounded h or log(h), no trace claimed.'



stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_SINE_RESOLVENT_APPROXIMATION',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_APROXIMANTES_SENO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior aos aproximantes explícitos do mesmo resolvente]\n\n# A1(b): translações, seno, CFC e limite forte-*\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: os fornecedores identificam translações e CFC, mas não produzem a família de aproximantes nem o seu limite no tipo exigido. O alvo consome exatamente esses fornecedores, sem novo GNS/J/core. O ramo por grafos/Schwartz/Kaplansky não será construído. A álgebra da ação direita tem DEV limpo e está em validação autoral/revisão neste instante; não é presumida aceita.\n\n'


for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_APROXIMANTES_SENO.md',s.encode('utf8'));print('FICHE',len(providers))
