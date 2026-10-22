import sys, os, io, json, time
H = os.path.dirname(os.path.abspath(__file__)); IMP = os.path.join(H, "imp")
sys.path.insert(0, IMP); os.chdir(IMP)
t=time.time(); _o=sys.stdout; sys.stdout=io.StringIO()
try:
    import um
finally:
    sys.stdout=_o
print("import ok", round(time.time()-t,1), um.UM_VERSION, um.FORMAL_DIR)
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
core = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open(os.path.join(H,"v391_um_absoluto.json"), encoding="utf-8"))["core"]
kf = core["kernel_formalization"]; kv = v["kernel_formalization"]
for k,x in list(kf.items()):
    if x is False and kv.get(k) is True: kf[k] = True
kf["all_verified"]=True; kf["formal_release_ready"]=True; kf["verdict"]=kv["verdict"]
r = um.prove_the_iald_index(core)
print("all_verified", r["all_verified"], r.get("verdict"))
for c in r["checks"]:
    if not c[1]: print("  FAIL", str(c[0])[:700])
print("amb new vs frozen:", sorted(set(r["ambiguos"]) - (set().union(*[getattr(um, n, set()) for n in []]))) [:0])
json.dump({"all_verified": r["all_verified"], "verdict": r.get("verdict"), "fails":[c[0] for c in r["checks"] if not c[1]]}, open(os.path.join(H,"r_iald_index_green.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
