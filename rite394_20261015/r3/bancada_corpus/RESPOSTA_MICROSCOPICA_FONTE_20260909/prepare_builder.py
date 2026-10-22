"""Copy and adapt the frozen leaf builder to the verified 77-module library."""
from pathlib import Path
import os, json, hashlib
base = Path(r"C:\IALD\Central de Patentes\Chatgpt")
out = Path(__file__).resolve().parent
source = base / "SELETOR_BORN_REGISTRO_20260909/build_selector_bridge.py"
raw = source.read_bytes()
text = raw.decode("utf-8")
changes = {
    'len(receipt["runs"])==12': 'len(receipt["runs"])==8',
    'len(receipt["cached_modules"])==63': 'len(receipt["cached_modules"])==72',
    'len(approved_plan["sources"])==72': 'len(approved_plan["sources"])==77',
    'transposed72 library': 'transposed77 library',
    'Approved72 module': 'Approved77 module',
}
for old, new in changes.items():
    assert text.count(old) == 1, old
    text = text.replace(old, new)

def new_file(path, data):
    assert not path.exists() and path.resolve().is_relative_to(base.resolve())
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, path)
    assert path.read_bytes() == data

new_file(out / "build_source.py", text.encode())
config = {"approved_library": (base / "INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582/BUILD_SUCCESSOR_20260909_174751_385895").as_posix()}
new_file(out / "CONFIG_BUILD.json", (json.dumps(config, indent=2)+"\n").encode())
assert source.read_bytes() == raw
new_file(out / "BUILDER_PROVENANCE.json", (json.dumps({"source":source.as_posix(),"sha256":hashlib.sha256(raw).hexdigest(),"changes":changes},indent=2)+"\n").encode())
print("Fresh builder77 prepared; frozen source unchanged.")
