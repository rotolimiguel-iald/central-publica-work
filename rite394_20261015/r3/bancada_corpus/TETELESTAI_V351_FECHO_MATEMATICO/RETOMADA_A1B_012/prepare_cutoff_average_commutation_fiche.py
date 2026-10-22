from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
pat='regularSpectralResolvent.{0,45}commut|regularInverseCutoffSqrt.{0,45}commut|regularAverage.{0,45}commut|commut.{0,45}(average|cutoff)'
queries=[('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|regular_unitary_positive_generator',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('others',['rg','-l',pat,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!*.bak*','-g','!**/packages/**'])]
A=R/'search_cutoff_average_commutation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True);out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)));print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
specs=[('TGLExt/V351RegularGeneratorAffiliation.lean','character_commutation_realScalarMultiplier'),('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),('TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_mul'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_cfc'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','hilbertPositiveSqrt'),('TGLExt/V350RegularApproximation.lean','regularAverage_apply'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg')]

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
target='For P,t prove Commute(regularSpectralResolvent P)(regularUnitary P t), using SAME spectral coordinates and commuting characters. For epsilon>0 use existing cutoff CFC identity and existing hilbertPositiveSqrt=CFC.sqrt to deduce Commute(sqrt(B_epsilon))(regularUnitary P t). Integrate the actual regularUnitary using regularAverage_apply to prove Commute(sqrt(B_epsilon))(regularAverage P delta) for EVERY real delta. No new spectral transform, resolvent, average, square root or weight. Consumer: use the already established average recovery on a sqrt(B_epsilon) to extend perturbed-weight order to all positive inputs. This does not infer commutation of arbitrary b in the right algebra with the averages. Mathematical helper is generic CFC commutation instantiated on Hilbert operators.'

stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_CUTOFF_AVERAGE_COMMUTATION',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=36,name='pedersen_takesaki_inverse_generator_trace'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_COMUTACAO_CORTES_MEDIAS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à comutação dos cortes com as médias]\n\n# A1(b): as médias comutam com as raízes dos cortes originais\n\n'+stamp+'\n\n'+target+'\n\nADAPTAR: coordenação espectral, comutação de caracteres, CFC e integral das translações existentes. Não reconstruir as coordenadas nem o resolvente. A consulta TODOS_POSITIVOS nomeia esta ponte como necessária. Mathlib Commute.cfc/IsSelfAdjoint.commute_cfc e Commute.cfcₙ_nnreal foram lidos no fornecedor ContinuousFunctionalCalculus/Commute.lean.\n\n'
for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_COMUTACAO_CORTES_MEDIAS.md',s.encode('utf8'));print('FICHE',len(providers))
