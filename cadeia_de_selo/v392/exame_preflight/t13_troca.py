import sys, os, io, json, pickle
H = os.path.dirname(os.path.abspath(__file__)); IMP = os.path.join(H, "imp")
sys.path.insert(0, IMP); os.chdir(IMP)
_o=sys.stdout; sys.stdout=io.StringIO()
import um
sys.stdout=_o
core = pickle.load(open(os.path.join(H,"core_green.pkl"),"rb"))
ESP = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\ESPERADOS_v392.json", encoding="utf-8"))
# inject the REAL failing iald index
r = um.prove_the_iald_index(core); core["the_iald_index"] = r
print("iald index", r["all_verified"])
for fn in ["estatuto_da_prova_v391", "three_stress_tests_v387"]:
    f = getattr(um, fn); x = f(core)
    print(fn, x.get("all_verified"), x.get("verdict")[:400])
    print("   v391 esperado:", ESP["vereditos_v391"].get(fn, "")[:400])
