"""Read-only source comparison; never import or execute the canonical program."""
from pathlib import Path
import ast, hashlib, json, datetime, subprocess, sys
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'v394_r12'
def sha(b): return hashlib.sha256(b).hexdigest()
def save(name,value):
    raw=value.encode('utf-8') if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    with (OUT/name).open('xb') as f:f.write(raw)
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def main():
    if OUT.exists(): raise FileExistsError(OUT)
    OUT.mkdir()
    save('OPERATOR.txt','Confira o que já avançou na v394 e veja se alguma peça resolve a pendência física das lentes, sem confundir o que está em construção com o que já está selado. Reaproveite o que temos e prossiga.')
    ref=str(ROOT/'SESSION_REFERENCE.json')
    r=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps({'operation':'project','reference':ref,'max_chars':60000}),text=True,encoding='utf-8',capture_output=True)
    d=json.loads(r.stdout);assert r.returncode==0 and d['ok'];save('PROJECT_START.json',d)
    p=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
    old=p/'um.py.bak_20261019_151122';new=p/'um.py';seal=p/'um_absoluto_selo.json'
    bs=[old.read_bytes(),new.read_bytes()]
    assert sha(bs[0])=='18be2ddb06c60f9037b1efecb72034e6a0c9409b0d3900452fd9d186cf4905c0'
    for name,b in zip(['v393_source.py.snapshot','v394_source.py.snapshot'],bs):
        with (OUT/name).open('xb') as f:f.write(b)
    save('SEAL_SNAPSHOT.json',seal.read_text(encoding='utf-8'))
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originals':[pin(old),pin(new),pin(seal)],'source_executed':False,'baseline_matches_prior_r9_r11':True,'functions':{},'new_top_level':[],'embedded_strings':{}}
    trees=[ast.parse(b.decode('utf-8-sig')) for b in bs]
    lines=[b.decode('utf-8-sig').splitlines(keepends=True) for b in bs]
    maps=[]
    for tree,ls in zip(trees,lines):
        m={}
        for n in tree.body:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                m[n.name]=(n,''.join(ls[n.lineno-1:n.end_lineno]))
        maps.append(m)
    excerpts=[]
    for name,(n,s) in maps[1].items():
        old_s=maps[0].get(name,(None,None))[1]
        state='added' if old_s is None else 'unchanged' if old_s==s else 'modified'
        report['functions'][name]={'state':state,'line':n.lineno,'end_line':n.end_lineno,'sha256':sha(s.encode()),'old_line':maps[0].get(name,(None,None))[0].lineno if old_s is not None else None}
        if state!='unchanged':
            excerpts.append(f'\n### {name} [{state}] {n.lineno}:{n.end_lineno}\n'+s if len(s)<45000 else f'\n### {name} [{state}] {n.lineno}:{n.end_lineno}; large block not included\n')
    save('CHANGED_FUNCTIONS.txt',''.join(excerpts))
    for n in trees[1].body:
        if isinstance(n,ast.Assign):
            names=[ast.unparse(t) for t in n.targets]
            if any('394' in k for k in names):report['new_top_level'].append({'names':names,'line':n.lineno,'end_line':n.end_lineno,'type':type(n.value).__name__})
    # Compare embedded .lean string values without executing any code.
    def lean_map(tree):
        result={}
        for node in ast.walk(tree):
            if isinstance(node,ast.Dict):
                for k,v in zip(node.keys,node.values):
                    if isinstance(k,ast.Constant) and isinstance(k.value,str) and k.value.endswith('.lean') and isinstance(v,ast.Constant) and isinstance(v.value,str):
                        result[k.value]=(v.value,v.lineno)
        return result
    em=[lean_map(t) for t in trees]
    for key,(val,line) in em[1].items():
        prior=em[0].get(key)
        state='added' if prior is None else 'unchanged' if prior[0]==val else 'modified'
        report['embedded_strings'][key]={'state':state,'line':line,'bytes':len(val.encode()),'sha256':sha(val.encode())}
        if state!='unchanged':
            dest=OUT/'lean'/key;dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('xb') as f:f.write(val.encode())
    report['counts']={kind:{state:sum(x['state']==state for x in report[kind].values()) for state in ['added','modified','unchanged']} for kind in ['functions','embedded_strings']}
    assert new.read_bytes()==bs[1], 'Live source changed while reading'
    save('SOURCE_DIFF_R12.json',report)
    print(json.dumps({'counts':report['counts'],'changed_functions':{k:v for k,v in report['functions'].items() if v['state']!='unchanged'},'assignments':report['new_top_level']},ensure_ascii=False))
if __name__=='__main__':main()
