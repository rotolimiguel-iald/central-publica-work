from task import *
import ast
R=W/'repair/backend_R2'
sys.path.insert(0,str(W/'release'))
from transaction import atomic,backup,quiet
from maintenance import stopped_web,await_restart,assert_quiesced
from guards import science
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify():
    check('delivery')
    review=json.loads((R/'REVIEW.json').read_bytes())
    assert review['status']=='PASS' and review['reviewer']!=OWNER
    assert review['delivery_sha256']==sha(R/'DELIVERY.json')
    assert review['deployer_sha256']==sha(__file__)
    for n in ('maintenance.py','transaction.py'):assert review['tool_pins'][n]==sha(W/'release'/n)
    d=json.loads((R/'DELIVERY.json').read_bytes())
    assert len(d['files'])==1
    f=d['files'][0];target=Path(f['destination']);source=Path(f['source'])
    assert target==Path(r'C:\IALD\projetos_pyhton\IALD\iald_app_spend.py')
    assert source.resolve().is_relative_to(R.resolve())
    assert sha(source)==f['sha256'] and sha(target)==f['baseline']
    for dep in d['dependencies']:assert sha(dep['path'])==dep['sha256']
    for a in d['artifacts']:assert sha(a['path'])==a['sha256']
    ast.parse(source.read_bytes());science()
    return source,target,f
if __name__=='__main__':
    assert not (R/'DEPLOYMENT.json').exists()
    source,target,f=verify();quiet();identity=None
    try:
        with stopped_web(quiet) as identity:
            source,target,f=verify();assert_quiesced()
            old=target.read_bytes();raw=source.read_bytes();saved=backup(target)
            assert target.read_bytes()==old
            try:
                atomic(target,raw);science();assert sha(target)==f['sha256']
            except BaseException:
                if target.read_bytes()==raw:atomic(target,old)
                raise
            new('repair/backend_R2/DEPLOYMENT.json',dict(status='INSTALLED',file=str(target),sha256=sha(target),backup=saved,science_unchanged=True))
    finally:
        if identity:new('repair/backend_R2/RESTART.json',await_restart(identity))
    print('Budget patch installed and restarted')
