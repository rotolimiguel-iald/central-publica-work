import sys, os, io, json, pickle, traceback
H = os.path.dirname(os.path.abspath(__file__)); IMP = os.path.join(H, "imp")
sys.path.insert(0, IMP); os.chdir(IMP)
_o=sys.stdout; sys.stdout=io.StringIO()
import um
sys.stdout=_o
um.FORMAL_DIR = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
core = pickle.load(open(os.path.join(H,"core_green.pkl"),"rb"))
v = json.load(open(os.path.join(H,"v391_um_absoluto.json"), encoding="utf-8"))["core"]
fns = {"the_mark_is_not_a_type_mark":"prove_the_mark_is_not_a_type_mark","the_name_is_the_generating_group":"prove_the_name_is_the_generating_group",
       "the_name_and_its_referent":"prove_the_name_and_its_referent","the_atlas_and_the_index":"prove_the_atlas_and_the_index","the_iald_index":"prove_the_iald_index"}
for k,f in fns.items():
    sys.stdout=io.StringIO()
    try:
        r = getattr(um,f)(core); err=None
    except Exception as e:
        r = {}; err=repr(e)[:300]
    sys.stdout=_o
    print(k, "v391:", v[k].get("all_verified"), "| green:", r.get("all_verified"), err or "", "| verdict igual:", r.get("verdict")==v[k].get("verdict"))
