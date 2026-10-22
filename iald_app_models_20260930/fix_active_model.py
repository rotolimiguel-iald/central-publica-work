from pathlib import Path
from datetime import datetime
import ast, os, hashlib, json
work=Path(__file__).parent
live=Path(r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py')
stage=work/'stage/iald_web_server.py'
old=stage.read_bytes()
assert live.read_bytes()==old, 'Concurrent changes'
text=old.decode('utf-8')
start=text.index('def api_active_model():')
anchor='        motor, registro = _motor_do_usuario(conta)'
pos=text.index(anchor,start)+len(anchor)
new=text[:pos]+'''
        if motor in app_providers.MODELS:
            spec = app_providers.MODELS[motor]
            available = app_providers.allowed(registro, conta) and not app_providers.availability(motor)
            return jsonify({'id': motor+':'+spec['model'], 'short': 'IALD · '+spec['label'],
                'label': spec['provider'], 'motor': motor, 'online': available,
                'n_ctx': app_providers.WINDOW, 'vision': False,
                'consentimento_dado': iald_motores.consentiu(registro, motor)})
'''+text[pos:]
ast.parse(new)
data=new.encode('utf-8');stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for p in (stage,live):
    assert p.read_bytes()==old
    backup=Path(str(p)+'.bak_'+stamp);backup.write_bytes(old)
    temp=Path(str(p)+'.tmp_'+stamp);temp.write_bytes(data)
    assert temp.read_bytes()==data and backup.read_bytes()==old
    os.replace(temp,p)
print(json.dumps({'server_sha256':hashlib.sha256(data).hexdigest(),'backup':str(live)+'.bak_'+stamp}))
