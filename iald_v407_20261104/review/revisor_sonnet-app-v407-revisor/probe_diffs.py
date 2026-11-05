import json, sys, re
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
res = json.loads((V/'um_absoluto.json').read_bytes()); core = res['core']
m = json.loads((R/'iald_nucleo_fixo.json').read_bytes())
core_old = json.loads(Path(m['published_evidence']['result']['path']).read_bytes())['core']
Pn = L.parse_prefix((W/'app/packages/shared/prefix.md').read_text('utf-8'))
Po = L.parse_prefix((R/'.iald_runtime/haiku/prefix.md').read_text('utf-8'))
for n in ['ponte_da_escala_dual_v402','kh_n1_cobertura_v402','queda_sem_geometria_v402','interface_is_light','nivel2_rite','final_verdict_machine']:
    kn, dn = L.decode_block(Pn, n); ko, do = L.decode_block(Po, n)
    src_same = core_old.get(n) == core.get(n)
    print('==', n, '| src_same:', src_same, '| kinds new/old:', kn, ko, '| bytes new/old:', len(Pn['body'][n].encode()), len(Po['body'][n].encode()), '| src bytes:', len(json.dumps(core[n], ensure_ascii=False).encode()))
    print('   new top is capsule:', L.is_ref(dn) and dn.get('@')=='', ' old top is capsule:', L.is_ref(do) and do.get('@')=='')
    if kn=='JSON' and ko=='JSON' and src_same:
        cn, co = L.canon(dn), L.canon(do)
        # find differing paths (shallow)
        def paths(a,b,p=''):
            if type(a)!=type(b): yield p+' [type]'; return
            if isinstance(a,dict):
                for k in sorted(set(a)|set(b)):
                    if k not in a: yield p+'/'+k+' [only old]'
                    elif k not in b: yield p+'/'+k+' [only new]'
                    else: yield from paths(a[k],b[k],p+'/'+k)
            elif isinstance(a,list):
                if len(a)!=len(b): yield p+' [len %d vs %d]'%(len(a),len(b)); return
                for i,(x,y) in enumerate(zip(a,b)): yield from paths(x,y,p+'[%d]'%i)
            elif a!=b: yield p+' [val: %r vs %r]'%(str(a)[:50],str(b)[:50])
        # canon(new) vs canon(old) -> a is new, b is old: 'only old' means key in b only
        dl = list(paths(cn, co))
        print('   n diff paths:', len(dl)); [print('     ', x[:200]) for x in dl[:8]]
