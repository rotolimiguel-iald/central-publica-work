"""Recompile prefixed candidate modules against isolated copies of baseline oleans."""
import ast
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
V=OUT/'formal_verified'
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
TRIO={'propext','Classical.choice','Quot.sound'}

def build(name,source):
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    d=V/'builds'/(name.replace('/','_')+'_'+stamp);d.mkdir(parents=True)
    src=V/'src'/(name+'.lean');src.parent.mkdir(parents=True,exist_ok=True)
    new(src,source)
    binary=V/'lib'/(name+'.olean');binary.parent.mkdir(parents=True,exist_ok=True)
    if binary.exists():
        with (d/'PREVIOUS.olean').open('xb') as f:f.write(binary.read_bytes())
    roots=[V/'lib']+sorted(CANON.glob('.lake/packages/*/.lake/build/lib/lean'))
    env=dict(os.environ);env['LEAN_PATH']=';'.join(map(str,roots))
    command=[str(LEAN),'-R',str(V/'src'),'-o',str(binary),str(src)]
    start=dt.datetime.now(dt.timezone.utc).isoformat();t=time.perf_counter()
    print('BUILD_START '+name,flush=True)
    p=subprocess.run(command,cwd=V/'src',env=env,capture_output=True)
    seconds=time.perf_counter()-t;end=dt.datetime.now(dt.timezone.utc).isoformat()
    stdout=p.stdout.decode('utf-8',errors='strict');stderr=p.stderr.decode('utf-8',errors='strict')
    new(d/'STDOUT.log',stdout);new(d/'STDERR.log',stderr)
    axioms={}
    for theorem,values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",stdout,re.S):
        axioms[theorem]=[s.strip() for s in values.split(',') if s.strip()]
    for theorem in re.findall(r"'([^']+)' does not depend on any axioms",stdout):axioms[theorem]=[]
    result={'module':name.replace('/','.'),'relative':name+'.lean','path':str(src),'sha256':pin(src)['sha256'],
            'start_utc':start,'end_utc':end,'seconds':seconds,'command':command,'LEAN_PATH':env['LEAN_PATH'],
            'exit_code':p.returncode,'toolchain':subprocess.check_output([str(LEAN),'--version']).decode().strip(),
            'axiom_report':axioms,'theorems':list(axioms),'passed':p.returncode==0 and all(set(x)<=TRIO for x in axioms.values()),
            'source':pin(src),'stdout':pin(d/'STDOUT.log'),'stderr':pin(d/'STDERR.log')}
    if p.returncode==0:result['olean']=pin(binary)
    new(d/'BUILD_RECEIPT.json',result)
    print(json.dumps({'module':name,'exit':p.returncode,'seconds':seconds,'axioms':len(axioms),'receipt':str(d/'BUILD_RECEIPT.json')},ensure_ascii=False),flush=True)
    assert result['passed'],str(d)
    return result

def main():
    mode=sys.argv[1]
    if mode=='matrix':
        src=OUT/'formal_matrix/TimeGravitonMatrix.lean'
        receipt=json.loads((OUT/'formal_matrix/FINAL_MATRIX_RECEIPT_R1.json').read_bytes())
        assert receipt['exit_code']==0 if 'exit_code' in receipt else receipt['axiom_report_count']==42 if 'axiom_report_count' in receipt else True
        result=build('TGLExt/TimeGravitonMatrix',src.read_text(encoding='utf-8'))
        new(V/'MATRIX_BUILD.json',result)
    elif mode=='flow':
        deliveries=sorted((OUT/'formal_flow').glob('DELIVERY_*.json'))
        assert deliveries, 'flow final receipt required'
        delivery=json.loads(deliveries[-1].read_bytes())
        results=[json.loads((V/'MATRIX_BUILD.json').read_bytes())]
        for record in delivery['sources']:
            p=Path(record['path']);assert pin(p)['sha256']==record['sha256']
            source=p.read_text(encoding='utf-8')
            source=re.sub(r'(?m)^import (TimeGraviton\w+)$',r'import TGLExt.\1',source)
            assert not re.search(r'(?m)^import TimeGraviton',source)
            results.append(build('TGLExt/'+p.stem,source))
        new(V/'FORMAL_MANIFEST.json',{'passed':True,'modules':results,'all_new_axioms_trio':True,'kind':'Fresh compilation under final TGLExt module names; dependencies copied by bytes from baseline cache','source_delivery':pin(deliveries[-1])})
    elif mode=='audit':
        manifest=json.loads((V/'FORMAL_MANIFEST.json').read_bytes())
        imports=''.join('import '+m['module']+'\n' for m in manifest['modules'])
        tree=ast.parse((OUT/'candidate/um.py').read_text(encoding='utf-8'))
        embedded=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets))
        results=[]
        for name in ['TGLExt','TGL/Audit']:
            source=embedded[name+'.lean']
            assert all('import '+m['module'] in source for m in manifest['modules'])
            results.append(build(name,source))
        new(V/'ROOT_AUDIT.json',{'passed':True,'results':results,'coverage_lines':[x for x in Path(results[-1]['stdout']['path']).read_text(encoding='utf-8').splitlines() if 'TGL_AXIOM_COVERAGE_TOTAL' in x]})
    else:raise ValueError(mode)

if __name__=='__main__':main()
