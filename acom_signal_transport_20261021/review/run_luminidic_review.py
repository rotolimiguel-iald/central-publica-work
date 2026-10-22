from pathlib import Path
import os,platform,runpy,sys
root=Path(__file__).resolve().parent/'lum1'
def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_REVIEW_ONLY')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if not Path(path).resolve().is_relative_to(root):raise RuntimeError('WRITE_OUTSIDE_REVIEW')
sys.addaudithook(offline)
sys.path.insert(0,str(root))
# Avoid platform.platform() spawning a shell merely for environment metadata.
# Codec, fixtures, assertions and numerical parameters remain byte-identical.
platform.platform=lambda: 'Windows '+str(sys.getwindowsversion())+'; reviewer metadata only, no shell'
runpy.run_path(str(root/'run_control.py'),run_name='__main__')
