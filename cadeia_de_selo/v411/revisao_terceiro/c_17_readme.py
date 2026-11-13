import sys, os, json, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
EN = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos"
rm = rd(EN + r"\README_PROJETADO_v411.md")
print("README projetado:", len(rm.encode("utf-8")), "B (teto 40960);", rm.count("\n"), "quebras")
T = json.load(open(V + r"\TOPO_RATIFICADO_v411.json", encoding="utf-8"))
core = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
def resolve(c, caminho):
    x = c
    for k in caminho:
        x = x.get(k) if isinstance(x, dict) else None
    return x
def fmt(x, d, lang):
    fo, fn = d["formato"], d["fonte"]
    if fn.startswith("parte inteira"): return str(int(math.floor(float(x))))
    if fo.startswith("inteiro"): return str(int(x))
    m = re.match(r"(\d+) casas", fo); rep = "%.*f" % (int(m.group(1)), float(x))
    if "com sinal" in fo and float(x) > 0: rep = "+" + rep
    return (rep.replace(".", ",") if lang == "pt" else rep).replace("-", "−")
mk = T["marcadores"]
vals = {}
for pt_, d in mk.items():
    fn = d["fonte"]
    if fn.startswith("teste_de_veracidade_fase9_v397"):
        nome = {"⟨z_disc⟩": "z_disc_calibrado", "⟨z_delta⟩": "z_delta_calibrado", "⟨lnB⟩": "lnB_lcdm"}[pt_]
        cam = ["teste_de_veracidade_fase9_v397", "lido", nome]
    else:
        cam = re.match(r"(?:parte inteira de )?([A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*)", fn).group(1).split(".")
    vals[pt_] = (resolve(core, cam), d)
def preencher(t, lang):
    for pt_, (x, d) in vals.items():
        m = pt_ if lang == "pt" else d["en"]
        t = t.replace(m, fmt(x, d, lang))
    return t
for lang in ("pt", "en"):
    pn = preencher(T["painel_readme_" + lang], lang)
    print(lang, "painel (preenchido) no README inteiro:", pn in rm, "| len", len(pn))
    if pn not in rm:
        # procurar a primeira linha
        pl = pn.split("\n")[0][:80]
        print("   primeira linha do painel no README:", pl in rm)
# a frase do acervo: ler do TOPO (pt) a parte 'Ele nao se le sozinho' e ver se esta no painel / README
i = T["pt"].find("Ele não se lê sozinho")
print("frase do acervo (pt) no TOPO:", T["pt"][i:i+500] if i >= 0 else "NAO ENCONTRADA no topo.pt")
print("painel_readme_pt contem 'acervo':", "acervo" in T["painel_readme_pt"], "| painel_readme_en contem 'archive':", "archive" in T["painel_readme_en"])
