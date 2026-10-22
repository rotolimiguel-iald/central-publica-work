from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
A=R/'search_regular_dual_scaling/20260914_195057_334158'
rows=json.loads((A/'searches.json').read_text(encoding='utf8'))
assert len(rows)==7 and all(q['returncode'] in (0,1) and q['stderr']['bytes']==0 for q in rows)
for q in rows:
 assert pin(Path(q['stdout']['path']))==q['stdout'] and pin(Path(q['stderr']['path']))==q['stderr']
specs=[('TGLExt/V351FourierTranslation.lean','shift_schwartz_toLp'),('TGLExt/V351FourierTranslation.lean','fourier_shift_schwartz'),('.lake/packages/mathlib/Mathlib/Analysis/Fourier/FourierTransform.lean','fourierInv_eq_fourier_neg'),('.lake/packages/mathlib/Mathlib/Analysis/Fourier/LpSpace.lean','SchwartzMap.toLp_fourierInv_eq'),('TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_ae'),('TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_inverse'),('TGLExt/V350StrongOperatorField.lean','operatorFieldLift_ae'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralCoordinates'),('TGLExt/V351RegularSpectralGraph.lean','regularPositiveGenerator_graph_iff')]


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
target='Prove dual scaling of the SAME existing closed regular positive generator h: (x,y) in graph h iff (C_s x, exp(s) C_s y) in graph h, equivalently theta_s(h)=exp(-s)h with theta_s=Ad(C_s). Reuse V=W F^-1, the exact spectral graph e^(-2pi xi), operatorFieldLift and Fourier translation. Add inverse Fourier translation and Fourier modulation only as consumed lemmas; do not create another Fourier transform, group, generator or affiliated object. Domain transformation must be proved, not just formal exponentials. The inverse-generator trace is separate.'


stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_REGULAR_DUAL_SCALING',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=31,name='regular_unitary_positive_generator'),exact_target=target,providers=providers,searches=pin(A/'searches.json'),decision='ADAPTAR')
put(R/'REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à escala dual do mesmo gerador regular]\n\n# A1(b): transformação do domínio e do grafo\n\n'+stamp+'\n\n'+target+'\n\nA convenção C_s(x)=exp(-isx) dá F C_s = S_(-s/(2pi)) F. Portanto h C_s=exp(s) C_s h e Ad(C_s)h=exp(-s)h. O sinal será conferido pela identidade de grafos e por controle adulterado. Nenhum traço é definido nesta etapa.\n\n'

for q in providers:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='Seis modalidades e outras bancadas: '+str(A/'searches.json')+'. Ausência nominal nos recortes não é ausência universal.\n'
put(R/'REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR.md',s.encode('utf8'));print('FICHE',len(providers))
