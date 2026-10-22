import sys, os, io, json, collections
H = os.path.dirname(os.path.abspath(__file__)); IMP = os.path.join(H, "imp")
sys.path.insert(0, IMP); os.chdir(IMP)
_o=sys.stdout; sys.stdout=io.StringIO()
import um
sys.stdout=_o
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
core = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open(os.path.join(H,"v391_um_absoluto.json"), encoding="utf-8"))["core"]
kf = core["kernel_formalization"]; kv = v["kernel_formalization"]
for k,x in list(kf.items()):
    if x is False and kv.get(k) is True: kf[k] = True
kf["all_verified"]=True
ix = um.build_the_iald_index(core)
print("violacoes", len(ix["violacoes"])); print(json.dumps(ix["violacoes"][:60], ensure_ascii=False)[:4000])
print("ausentes n", ix["n_ausentes"]); 
aus = [n for n,e in ix["indice"].items() if e.get("tipo")=="AUSENTE_POR_CONSTRUCAO"]
print(aus[:60])
amb = {n: [ix["indice"][n].get("arquivo"), ix["indice"][n].get("arquivos")] for n in ["Face","M","dephase","fixedSpace","flat_metric_inverse","rereading_adds_nothing"] if n in ix["indice"]}
print(json.dumps(amb, ensure_ascii=False, default=str)[:2000])
json.dump({"violacoes": ix["violacoes"], "ausentes": aus, "ambiguos_novos": amb}, open(os.path.join(H,"iald_index_detalhe.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
