"""V-only guards inherited by child Python processes; never installed globally."""
from pathlib import Path
import atexit, hashlib, json, os, sys
ROOT=Path(__file__).resolve().parent
DENIED=[]
def local(p):
    if isinstance(p,int) or p is None:return True
    p=os.fsdecode(p)
    if p.startswith('\\\\?\\'):p=p[4:]
    return Path(p).resolve().is_relative_to(ROOT)
def audit(event,args):
    if event in ('socket.connect','socket.bind','socket.getaddrinfo'):
        DENIED.append(event);raise AssertionError('V forbids network: '+event)
    if event=='open':
        p,mode,flags=args
        if isinstance(p,(str,bytes)):
            name=Path(os.fsdecode(p)).name.lower()
            if name in ('.env','iald_stack_v7.py') or name.startswith('iald_psion_state'):
                DENIED.append('confidential read');raise AssertionError('V forbids confidential reads')
        if ((mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)) and not local(p):
            DENIED.append('write outside V');raise AssertionError('V forbids write outside private tree: '+str(p))
    if event in ('os.remove','os.rmdir','os.mkdir') and not local(args[0]):
        DENIED.append(event);raise AssertionError('V forbids mutation outside private tree: '+str(args[0]))
    if event in ('os.rename','os.link','os.symlink') and not all(local(p) for p in args[:2]):
        DENIED.append(event);raise AssertionError('V forbids move outside private tree')
sys.addaudithook(audit)
@atexit.register
def receipt():
    modules=[]
    for name,module in tuple(sys.modules.items()):
        if name=='iald_memory' or name.startswith('iald_memory.'):
            path=Path(module.__file__).resolve()
            modules.append({'module':name,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'final_tree':path.is_relative_to(ROOT/'staging')})
    folder=ROOT/'process_receipts';folder.mkdir(exist_ok=True)
    value={'pid':os.getpid(),'argv':sys.argv,'modules':modules,'denied':DENIED,'guard':'no network, no writes outside V, no confidential source reads'}
    with (folder/(str(os.getpid())+'.json')).open('x',encoding='utf8') as f:json.dump(value,f,ensure_ascii=False,indent=2)
