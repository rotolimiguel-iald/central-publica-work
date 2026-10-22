from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists() and b
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('Algebra/Order/Star/Basic.lean','star_left_conjugate_nonneg'),('Algebra/Order/Star/Basic.lean','star_left_conjugate_le_conjugate'),('Algebra/Order/Field/Basic.lean','one_div_le_one_div_of_le'),('Data/ENNReal/Operations.lean','iSup_add_iSup_of_monotone'),('Data/ENNReal/Inv.lean','mul_iSup')]
providers=[]
for path,name in specs:
    p=K/'.lake/packages/mathlib/Mathlib'/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:protected )?(?:lemma|theorem) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    start=m.start();depth=0;end=None
    for i in range(start,len(s)):
        if s[i] in '([{':depth+=1
        elif s[i] in ')]}':depth-=1
        if not depth and (s.startswith(' :=',i) or s.startswith(' where',i)):end=i;break
    assert end is not None
    providers.append(dict(name=name,source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end]))
fiche=json.loads((R/'REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE.json').read_text(encoding='utf8'));search=Path(fiche['searches']['path']);assert pin(search)==fiche['searches']
for row in json.loads(search.read_text(encoding='utf8')):
    assert row['returncode'] in (0,1) and row['stderr']['bytes']==0
    out=Path(row['stdout']['path']);assert pin(out)==row['stdout'];print(row['label'],out.read_text(encoding='utf8'))
reason='A ordem de conjugação refere-se ao input X com conjugador fixo; não compara conjugadores ordenados. A soma de supremos usa MONOTONIA no mesmo índice natural (fornecedor ENNReal), evitando a igualdade falsa para duas famílias arbitrárias não dirigidas conjuntamente. Homogeneidade usa mul_iSup, inclusive nos valores infinitos. Normalidade do limite é troca de supremos do peso construído. Nenhuma lei deste delta implica tracialidade ou semifinitude.'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHE_APPEND_BEFORE_LIMIT_WEIGHT_CODE',providers=providers,searches=pin(search),reason=reason)
stem='ADENDO_FICHA_PESO_LIMITE_SUPREMOS';put(R/(stem+'.json'),json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — fornecedores antes do código]\n\n'+d['timestamp']+'\n\n'+reason+'\n\n'
for q in providers:md+=str(q['source']['path'])+':'+str(q['line'])+'\n\n```lean\n'+q['statement']+'\n```\n\n'
put(R/(stem+'.md'),md.encode('utf8'));print('PROVIDERS',len(providers))
