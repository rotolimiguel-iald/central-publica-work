import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
def tt(p):
    j = json.load(open(p, encoding="utf-8"))
    c = j["core"] if "core" in j else j
    return (c.get("selo_pela_propria_tecnologia_v399") or {}).get("values", {}).get("tempo_total_s")
for p in (NOS + r"\um_absoluto.json", r"C:\t\k411c\falso_nos_v411\um_absoluto.json", V + r"\base_v410\um_absoluto.json"):
    try: print(p[-60:], tt(p))
    except Exception as e: print(p, "ERR", e)
import glob
for p in sorted(glob.glob(NOS + r"\um_absoluto.json.bak_2026110*"))[-3:] + sorted(glob.glob(NOS + r"\um_absoluto.json.bak_20261105*")) + sorted(glob.glob(NOS + r"\um_absoluto.json.bak_2026102*")):
    try: print(os.path.basename(p), tt(p))
    except Exception as e: print(os.path.basename(p), "ERR", str(e)[:60])
