from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists() and b
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean','cfc_commute_cfc'),
('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean','Commute.mul_nonneg'),
('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','sqrt_mul_sqrt_self')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:protected )?(?:lemma|theorem) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end]))
fiche=json.loads((R/'REAPROVEITAMENTO_A1B_ORDEM_REGULADORES.json').read_text(encoding='utf8'))
search=Path(fiche['searches']['path']);assert pin(search)==fiche['searches']
for row in json.loads(search.read_text(encoding='utf8')):
    assert row['returncode'] in (0,1) and row['stderr']['bytes']==0
    out=Path(row['stdout']['path']);assert pin(out)==row['stdout'];print(row['label'],out.read_text(encoding='utf8'))
reason='Usar CFC somente para comutação de funções do mesmo R. A ordem vem da identidade resolvente e da positividade do PRODUTO de cortes que comutam; não da ordem de sanduíches. A comparação de sanduíches sob o peso usa o teorema all_positive já compilado com suas hipóteses explícitas. Aplicar o fornecedor genérico Commute.mul_nonneg em Hilbert antes da especialização fixa as instâncias. A raiz original satisfaz sqrt(B)*sqrt(B)=B e é autoadjunta por positividade.'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHE_APPEND_BEFORE_REGULATOR_ORDER_CODE',providers=providers,searches=pin(search),reason=reason)
stem='ADENDO_FICHA_REGULADORES_PRODUTO_POSITIVO';put(R/(stem+'.json'),json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — fornecedores antes do código]\n\n'+d['timestamp']+'\n\n'+reason+'\n\n'
for q in providers:md+=str(q['source']['path'])+':'+str(q['line'])+'\n\n```lean\n'+q['statement']+'\n```\n\n'
put(R/(stem+'.md'),md.encode('utf8'));print('PROVIDERS',len(providers))
