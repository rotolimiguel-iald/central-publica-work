import os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
def guard(event,args):
    if event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_REVIEW_ONLY')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if not Path(path).resolve().is_relative_to(ROOT):raise RuntimeError('REVIEW_WRITES_ONLY')
sys.addaudithook(guard)
