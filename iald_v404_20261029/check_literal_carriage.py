"""Builder check (read-only, stdout only): for the topics of the shared P2 window (11 new in v404 + the former _v401/_v402 ones),
which qualifier keys (status/estatuto/verdict/scope/limites/diz/nao_diz/hypothesis...) are INLINE in the shared and sonnet_public prefixes
and which only by pointer. Uses the reviewer's independent decoder (review/revisor_sonnet-app-v404-revisor/r3_topics_capsules.py), loaded with the root given in argv[1].
usage: check_literal_carriage.py <release_dir>   (default: this folder)"""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else HERE
LIB=HERE/'review/revisor_sonnet-app-v404-revisor/r3_topics_capsules.py'
def load(wd):
    argv=sys.argv;sys.argv=['x',str(wd)]
    spec=importlib.util.spec_from_file_location('r3x',str(LIB))
    with contextlib.redirect_stdout(io.StringIO()):
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    sys.argv=argv;return m
def block(m,pkg,n):
    t=(m.W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=m.unalias(t.partition(m.MARK)[0])
    Dm=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(Dm.group(1)) if Dm else {}
    F=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head);FL=json.loads(F.group(1)) if F else {}
    E=t.partition(m.MARK)[2].split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        if h[1]==n:
            seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
            line=[l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')][0]
            v=json.loads(line)
            if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
            return m.dec_lit(m.unpack(v),D,E)
    raise KeyError(n)
Q=re.compile(r'status|statute|estatuto|verdict|scope|escopo|limites|diz$|nao_diz|hypothes|not_claimed|declar|conditional|condicional',re.I)
def top(m,pkg,n):
    dv=block(m,pkg,n);src=m.core[n]
    if isinstance(dv,dict) and '@' in dv:inline=set(k.split('/')[1] for k in dv.get('fields',{}) if k.count('/')>=1)
    else:inline={k for k,x in dv.items() if not (isinstance(x,dict) and '@' in x)}
    qk=[k for k in src if Q.search(k)]
    return qk,[k for k in qk if k in inline],[k for k in qk if k not in inline]
m=load(ROOT)
m2=json.loads((HERE.parent/'iald_v402_20261027/app/RELEASE.json').read_bytes())
core402=json.loads((Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v402')/'um_absoluto.json').read_bytes())['core']
new11=[n for n in m.core if n not in core402]
former=[n for n in m.core if n.endswith(('_v401','_v402'))]
topics=new11+[n for n in former if n not in new11]
out={'root':str(ROOT),'new_topics_vs_v402':len(new11),'former_window_topics_v401_v402':len(former),'topics_checked':len(topics),'per_topic':{}}
bad=0
for n in topics:
    r={}
    for pkg in ('shared','sonnet_public'):
        try:qk,il,pt=top(m,pkg,n);r[pkg]={'qualifier_keys_in_source':qk,'only_by_pointer':pt,'inline':il};bad+=bool(pt)
        except Exception as e:r[pkg]={'error':type(e).__name__+': '+str(e)[:120]};bad+=1
    out['per_topic'][n]=r
out['topics_with_a_qualifier_only_by_pointer_or_error']=bad
N=re.compile(r'status|statute|estatuto|verdict|scope|escopo|limites|diz$|nao_diz',re.I)
def narrow_ok(names):return all('error' not in out['per_topic'][n][p] and not [k for k in out['per_topic'][n][p]['only_by_pointer'] if N.search(k)] for n in names for p in ('shared','sonnet_public'))
out['check18_like_status_verdict_scope_limites_diz_nao_diz_inline__11_new_topics']=narrow_ok(new11)
out['same_for_the_8_former_v401_v402_topics']=narrow_ok(former)
out['former_topics_failing']=[n for n in former if not narrow_ok([n])]
out['note']='unconditional / index_conditional structured registers stay pointer-only by inherited design (same treatment as the v402-accepted topics); not part of the v402 check 18 list'
out['limites_diz_nao_diz_inline_everywhere']=all(all(k not in ('limites','diz','nao_diz') for k in r[p].get('only_by_pointer',['x'])) and 'error' not in r[p] for r in out['per_topic'].values() for p in r)
print(json.dumps(out,ensure_ascii=False,indent=1))
