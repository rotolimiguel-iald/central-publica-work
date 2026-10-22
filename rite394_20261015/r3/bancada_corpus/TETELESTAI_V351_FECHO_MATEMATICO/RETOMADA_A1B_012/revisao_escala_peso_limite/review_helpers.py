from build_delta import *

OUT=R/'revisao_escala_peso_limite'
STATUS='A1_INVERSE_LIMIT_SCALING_REVIEW_ACCEPTED__SEMIFINITE_TRACIAL_OPEN'
NAME='REVIEW_A1_INVERSE_LIMIT_SCALING_FINAL'
ALLOWED={'propext','Classical.choice','Quot.sound'}

def norm(s):return re.sub(r'\.\{[^}]*\}','',s).strip()

def parse_axioms(text):
    result={}
    pattern=r"^'([^\r\n]+)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))"
    for m in re.finditer(pattern,text,re.M|re.S):
        name=norm(m[1]); ax=[] if m[3] else [norm(v) for v in m[2].split(',') if v.strip()]
        if name in result:assert result[name]==ax
        result[name]=ax
    return result

def trace(mod):
    p=V/'.lake/build/lib/lean'/Path(mod.replace('.','/')+'.trace');j=load(p)
    assert not any(v['level']=='error' for v in j['log']),mod
    commands=[v['message'] for v in j['log'] if v['level']=='trace' and 'LEAN_PATH=' in v['message']]
    assert commands,mod
    for cmd in commands:
        lp=re.split(r'\s+[cC]:\\',cmd.split('LEAN_PATH=',1)[1],maxsplit=1)[0]
        assert all(Path(x).resolve().is_relative_to(V.resolve()) for x in lp.split(';')),lp
    infos=[re.sub(r'^.*?\.lean:\d+:\d+:\s*','',v['message']) for v in j['log'] if v['level']=='info']
    return p,j,infos

def validate_pin_tree(x,records):
    if isinstance(x,dict):
        if {'path','bytes','sha256'}<=x.keys():
            actual=pin(Path(x['path']))
            assert all(actual[k]==x[k] for k in ['path','bytes','sha256']),x
            records.append(actual)
        else:
            for value in x.values():validate_pin_tree(value,records)
    elif isinstance(x,list):
        for value in x:validate_pin_tree(value,records)

