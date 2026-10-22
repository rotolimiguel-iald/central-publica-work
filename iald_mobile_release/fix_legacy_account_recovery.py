import ast
from pathlib import Path
from datetime import datetime
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
def save(path,text):
    data=text.encode('utf-8')
    backup=path.with_name(path.name+'.bak_'+stamp)
    backup.write_bytes(path.read_bytes())
    assert backup.read_bytes()==path.read_bytes()
    tmp=path.with_name(path.name+'.tmp_release')
    tmp.write_bytes(data)
    assert tmp.stat().st_size==len(data)>0
    tmp.replace(path)

p=ROOT/'iald_web_server.py'
s=p.read_text(encoding='utf-8-sig')
for variable in ('apple_id','marca'):
    old=f'    pedido = access_engine.find_by_apple_id({variable})\n    if not pedido:'
    new=f'''    pedido = access_engine.find_by_apple_id({variable})
    if pedido and pedido.get("assigned_username") and pedido["assigned_username"] not in USERS_CURRENT:
        # The earlier account reset did not remove Apple/device access records.
        access_engine.reset_request({variable})
        pedido = None
    if not pedido:'''
    assert old in s
    s=s.replace(old,new,1)
ast.parse(s)
save(p,s)
p=ROOT/'iald_access_engine.py'
s=p.read_text(encoding='utf-8-sig')
node=next(n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.FunctionDef) and n.name=='reset_request')
lines=s.splitlines(keepends=True)
replacement='''    def reset_request(self, apple_id: str) -> bool:
        requests_list = self._load()
        changed = False
        for entry in requests_list:
            if entry.get("apple_id") == apple_id and entry.get("status") != "reset":
                entry["status"] = "reset"
                entry["assigned_username"] = None
                entry["reviewed"] = datetime.now().isoformat()
                entry["reviewer_notes"] = "Auto-reset: usuário deletado do sistema"
                changed = True
        if changed:
            self._save(requests_list)
        return changed
'''
s=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:])
ast.parse(s)
save(p,s)
print('Legacy Apple/device account recovery fixed; no real account records changed.')
