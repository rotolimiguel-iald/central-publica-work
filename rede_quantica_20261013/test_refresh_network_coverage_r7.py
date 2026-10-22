"""Focused synthetic tests of the new exact-coverage data transformation."""
import ast
import copy
import hashlib
import json
from diary_r1 import new, pin
from refresh_network_coverage_r7 import OUT, compose


def fixture():
    bodies = {'TGLExt/Fixture.lean':'example : True := True.intro\n'}
    checks = [dict(id=k,valor=1) for k in ('h_decl','h_thm','h_fora_do_trio',
        'h_nao_lidas_pelo_regex','h_report_exact','h_sources_exact')]
    spec = dict(nome='kh_n1_cobertura_v394',checks=checks,extras={},erratas=[])
    raw = ('_EMBEDDED_KERNEL_FILES = '+repr(bodies)+'\n_V393_SPECS = '+repr([spec])+
        '\n_V393_FONTES = '+repr({'kh_n1_v394':{'historical':True}})+
        '\ndef actual_function(x):\n    return x + 1\n').encode('utf8')
    contract = dict(decl=7,thm=5,axiom_report_entries=7,nao_lidas_pelo_regex=0,fora_do_trio=0,
        formal_files_sha256={k:hashlib.sha256(v.encode()).hexdigest() for k,v in bodies.items()})
    return raw,contract,{'path':'SYNTHETIC_NOT_REAL_PROOF.json','sha256':'fixture-not-a-pin','bytes':10}


def rejected(change):
    raw,c,m = fixture(); raw,c,m = change(raw,c,m)
    try:
        compose(raw,c,m)
    except (AssertionError,ValueError):
        return True
    return False


def main():
    destination = OUT/'coverage_refresh_tests_r1/RESULT.json'
    assert not destination.exists()
    raw,c,m = fixture(); updated = compose(raw,c,m)
    vals = {n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(updated).body
        if isinstance(n,ast.Assign)}
    spec = vals['_V393_SPECS'][0]
    tests = dict(valid_synthetic_transform=True,
        preserves_previous_spec=spec['extras']['previous_spec_preserved']['checks'][0]['valor']==1,
        preserves_previous_source=spec['extras']['previous_source_preserved']=={'historical':True},
        no_duplicate_current_spec=len(vals['_V393_SPECS'])==1,
        new_counts_are_exact=next(v['valor'] for v in spec['checks'] if v['id']=='h_decl')==7)
    for name,key,value in [('boolean_count','decl',True),('negative_count','thm',-1),
        ('count_disagreement','axiom_report_entries',6),('outside_trio','fora_do_trio',1),
        ('unread_names','nao_lidas_pelo_regex',1),('source_hash_changed','formal_files_sha256',{})]:
        def change(raw,c,m,key=key,value=value):
            c[key]=value
            return raw,c,m
        tests[name+'_refused']=rejected(change)
    assert all(tests.values()),tests
    new(destination,dict(status='PASS',checks=tests,harness=pin(__file__),
        composer=pin(__import__('refresh_network_coverage_r7').__file__),
        scope='Synthetic composition checks, not a pre-audit, Lean build, main invocation or scientific proof.'))
    print(json.dumps(dict(checks=len(tests),receipt=pin(destination)),ensure_ascii=False))


if __name__=='__main__':
    main()
