import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
cd = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca"
r = json.load(open(cd + r"\result.json", encoding="utf-8"))
print("cached env:", r.get("env"))
code = ("import json,platform,torch,numpy,scipy;ok=torch.cuda.is_available();"
        "print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':numpy.__version__,'scipy':scipy.__version__,"
        "'python':platform.python_version(),'gpu':(torch.cuda.get_device_name(0) if ok else None)}))")
for exe in (sys.executable, "python"):
    try:
        o = subprocess.run([exe, "-c", code], capture_output=True, text=True, timeout=300)
        print(exe, "->", o.stdout.strip()[-300:], o.stderr.strip()[-200:])
    except Exception as e:
        print(exe, "ERR", e)
