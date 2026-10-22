from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,ast
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
PREV=ROOT/'REEXAME_SUFICIENCIA_078_20260910'
OUT=ROOT/'REEXAME_SUFICIENCIA_079_20260910'
OUT.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def new(p,raw):
    assert not p.exists()
    temp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert temp.read_bytes()==raw;temp.rename(p);assert p.read_bytes()==raw
    return pin(p)
records=[]
for oldname,newname,extra in [
('capture_current078.py','capture_current079.py',[]),
('finalize_delivery078.py','finalize_delivery079.py',[
(b"config['new_cas_controls'] == 122",b"config['new_cas_controls'] == 12"),
(b'ENTREGA_079_ESPONTANEA_residuo_A6_e_comparacao_de_completacoes.md',b'ENTREGA_079_ESPONTANEA_liberdade_de_correcao_e_funcional_impar.md')])]:
    src=PREV/oldname;before=pin(src);raw=src.read_bytes()
    substitutions=[]
    for old,newval in [(b'078',b'079'),(b'077',b'078')]+extra:
        count=raw.count(old);assert count>0
        substitutions.append({'old':old.decode(),'new':newval.decode(),'count':count})
        raw=raw.replace(old,newval)
    ast.parse(raw.decode('utf-8'))
    target=new(OUT/newname,raw)
    assert pin(src)==before
    records.append({'source':before,'target':target,'ordered_substitutions':substitutions,'source_unchanged':True})
obj={'status':'NEW_HELPERS_PREPARED_NOT_EXECUTED','created_utc':datetime.now(timezone.utc).isoformat(),
'copies':records,'writer':pin(Path(__file__).resolve()),
'capture_executed':False,'finalizer_executed':False,'um_executed_or_imported':False,'originals_written':False}
prov=new(OUT/'PROVENIENCIA_AUXILIARES_079.json',(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'helpers':records,'provenance':prov},ensure_ascii=True))

