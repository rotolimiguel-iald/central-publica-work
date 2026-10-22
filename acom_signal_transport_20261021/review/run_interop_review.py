from pathlib import Path
import os,runpy,subprocess,sys
root=Path(__file__).resolve().parent/'interop1';node=r'C:\Program Files\nodejs\node.exe'
def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo','socket.bind'):raise RuntimeError('OFFLINE_ONLY')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if str(path).lower() not in ('nul',os.devnull.lower()) and not Path(path).resolve().is_relative_to(root):raise RuntimeError('REVIEW_WRITES_ONLY')
    if event=='subprocess.Popen':
        executable=args[0];assert str(executable).lower()==node.lower(),'ONLY_REVIEW_NODE'
sys.addaudithook(offline)
original=subprocess.run
def guarded(args,*pos,**kw):
    assert args==[node,str(root/'node_tests.mjs'),str(root/'fixtures')]
    return original([node,'--import',(root/'offline_guard.mjs').as_uri(),*args[1:]],*pos,executable=node,**kw)
subprocess.run=guarded
sys.path.insert(0,str(root))
runpy.run_path(str(root/'run_tests.py'),run_name='__main__')
