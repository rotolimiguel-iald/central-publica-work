from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists() and b
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('TGLExt/V350LevelExpectationUniformBound.lean','vonNeumann_norm_closed'),
       ('TGLExt/V350LevelExpectationUniformBound.lean','vonNeumann_starOrdered'),
       ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Range.lean','cfcₙ_mem'),
       ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','sqrt_eq_real_sqrt'),
       ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','sqrt_mul_sqrt_self')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8')
    m=re.search(r'^(?:protected )?(?:lemma|theorem) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end]))
search=R/'search_all_positive_weight_order/20260914_221338_858806'
rows=json.loads((search/'searches.json').read_text(encoding='utf8'))
for row in rows:
    assert row['returncode'] in (0,1) and row['stderr']['bytes']==0
    out=Path(row['stdout']['path']);assert pin(out)==row['stdout']
    print(row['label'],out.read_text(encoding='utf8'))
reason='Reusar vonNeumann_norm_closed no MESMO core. O corpo de vonNeumann_starOrdered já mostra a pertença da raiz por cfcₙ_mem e sua identidade quadrática; adaptar somente o empacotamento do hilbertPositiveSqrt, sem nova raiz e sem nova demonstração de fechamento. Não inferir que StarOrderedRing abstrato sozinho fornece uma única raiz. Os fornecedores mathlib abaixo foram lidos antes do alvo.'
stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='FICHE_APPEND_BEFORE_ALL_POSITIVE_ORDER_CODE',providers=providers,searches=pin(search/'searches.json'),reason=reason)
stem='ADENDO_FICHA_ORDEM_POSITIVA_RAIZ'
put(R/(stem+'.json'),json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — fornecedores recuperados antes do código]\n\n'+stamp+'\n\n'+reason+'\n\n'
for q in providers:md+=str(q['source']['path'])+':'+str(q['line'])+'\n\n```lean\n'+q['statement']+'\n```\n\n'
put(R/(stem+'.md'),md.encode('utf8'));print('PROVIDERS',len(providers))
