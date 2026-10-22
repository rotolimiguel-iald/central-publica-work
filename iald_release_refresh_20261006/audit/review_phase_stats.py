"""Read exact P4/P5/F9 values from Git objects and bind to the sealed core."""
import json
from pathlib import PurePosixPath
from review_sources import git, COMMIT, CUSTODY, sha, load, save, walk

core=load(CUSTODY/'um_absoluto.json')['core']
tree={}
for row in git('ls-tree','-r','-z',COMMIT).split(b'\0'):
    if row:
        metadata, path=row.split(b'\t',1)
        tree[path.decode('utf8')]=metadata.split()[2].decode()
specs=[
    ('P4','RESULTADO_FASE4_DESVIO_20260930.json','/familias/P_dr2_escada/nucleos/d1b/evidencia/lnB'),
    ('P5','RESULTADO_FASE5_SH0ES_20261001.json','/familias/P_dr2_sh0es/leituras/sombra/evidencia/lnB'),
    ('F9','RESULTADO_FASE9_V1_20261006_110507.json',None),
]
out=[]
for phase,name,pointer in specs:
    paths=[p for p in tree if PurePosixPath(p).name==name]
    assert len(paths)==1,paths
    raw=git('cat-file','blob',tree[paths[0]])
    pin=sha(raw)
    value=json.loads(raw)
    if pointer:
        for part in pointer.strip('/').split('/'):
            value=value[part]
    else:
        value=core['hubble_ratio_opening_v388']['numbers']
    bindings=[p for p,v in walk(core,'/core') if v==pin]
    assert bindings, (phase,pin)
    out.append({'phase':phase,'git_path':paths[0],'commit':COMMIT,'sha256':pin,
                'sealed_core_hash_pointers':bindings,'pointer':pointer,'values':value})
save('phase_statistics_review.json',{'status':'PASS','method':'Read committed JSON; no fits, calculations, tests or scientific code executed.',
                                   'phases':out,'rule':'Different universes; do not combine or relabel P4/P5/F9 evidence.'})
print(json.dumps({'status':'PASS','phase_pins':{r['phase']:r['sha256'] for r in out}},ensure_ascii=False))
