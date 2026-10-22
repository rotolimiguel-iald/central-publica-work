"""Create a new builder using the completed 93-module overlay; preserve the prior builder."""
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
SRC = ROOT / "ERRO_RECONSTRUCAO_FINITA_20260909" / "build_source.py"
LIB = ROOT / "INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415" / "BUILD_SUCCESSOR_20260909_203414_443930"
def put(p, raw):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    tmp.rename(p)
    assert p.read_bytes()==raw
raw=SRC.read_bytes()
text=raw.decode("utf-8")
changes=[('len(receipt["runs"])==9','len(receipt["runs"])==13'),
         ('len(receipt["cached_modules"])==77','len(receipt["cached_modules"])==83'),
         ('len(approved_plan["sources"])==83','len(approved_plan["sources"])==93'),
         ('approved transposed83 library','approved transposed93 library'),
         ('Approved83 module','Approved93 module')]
for old,new in changes:
    assert text.count(old)==1,old
    text=text.replace(old,new)
result=json.loads((LIB/"TRANSPOSED_RESULT.json").read_bytes())
assert result["status"]=="PASS_TRANSPOSED_SCOPE" and len(result["runs"])==13
assert all(r["valid"] and r["exit_code"]==0 and r["warning_lines"]==0 for r in result["runs"])
put(OUT/"build_source.py",text.encode())
put(OUT/"CONFIG_BUILD.json",(json.dumps({"approved_library":str(LIB),"cached":{}},indent=2)+"\n").encode())
put(OUT/"BUILDER_PROVENANCE.json",(json.dumps({"created_utc":datetime.now(timezone.utc).isoformat(),
 "source":{"path":str(SRC),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()},
 "output":{"path":str(OUT/"build_source.py"),"sha256":hashlib.sha256((OUT/"build_source.py").read_bytes()).hexdigest()},
 "exact_replacements":changes,"library":str(LIB)},indent=2)+"\n").encode())
assert SRC.read_bytes()==raw
print(str(OUT/"build_source.py"))
