from pathlib import Path
import json,psutil,time,requests
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
W=Path(__file__).parent
matches=[]
for process in psutil.process_iter(['pid','cmdline']):
    cmd=process.info['cmdline'] or []
    if len(cmd)==3 and cmd[1]==str(ROOT/'iald_web_server.py') and cmd[2]=='8082':
        matches.append(process)
assert len(matches)==1,'Expected one verified web server'
p=matches[0];parent=p.parent();args=parent.cmdline()
assert args[-1]==str(ROOT/'start_iald_web.ps1') and '-WindowStyle' in args and 'Hidden' in args
old=p.pid
p.terminate()
for attempt in range(40):
    time.sleep(1)
    try:
        if requests.get('http://127.0.0.1:8082/login',timeout=2).status_code==200:
            print(json.dumps({'status':'WEB_READY','previous_pid':old,'supervisor_pid':parent.pid}))
            break
    except requests.RequestException:pass
else:raise RuntimeError('Server did not restart in time')
