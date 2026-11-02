"""Reviewer shim (sonnet-app-v404-revisor): same role as the v402 reviewer's shim -- no mission calls, writes only inside this scratch folder."""
from pathlib import Path
import json
W=Path(__file__).resolve().parent
def check(task,actor=None):return {'ready':True}
def new(name,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    with (W/name).open('xb') as f:f.write(raw)
