from b_lib import *
import re, math
T = json.loads(rd(V + r"\TOPO_RATIFICADO_v411.json"))
C = core()["core"]
h = C["h0dn_bg1_v411"]["values"]
ev = C["estatuto_da_prova_v391"]["prova_2_ritos"]
fz = C["teste_de_veracidade_fase9_v397"]["lido"]
def fmt(x, casas=2, sinal=False, lang="pt"):
    s = "%.*f" % (casas, x)
    if sinal and x > 0: s = "+" + s
    if lang == "pt": s = s.replace(".", ",")
    return s.replace("-", "−")
def vals(lang):
    return {
     "⟨Z contra K⟩": fmt(h["primario"]["z_tgl"], 2, True, "pt"),
     "⟨Z contra o nulo⟩": fmt(h["primario"]["z_null"], 2, False, "pt"),
     "⟨n⟩": str(int(math.floor(h["primario"]["z_null"]))),
     "⟨Z das Cefeidas livres⟩": fmt(h["cefeidas_livres"]["z_null"], 2, False, "pt"),
     "⟨N cobranças⟩": str(ev["n_cobrancas"]),
     "⟨não falsificadas⟩": str(ev["ledger"]["NOT_FALSIFIED"]), "⟨inconclusivas⟩": str(ev["ledger"]["INCONCLUSIVE"]),
     "⟨à espera de dado⟩": str(ev["ledger"]["AWAITING"]), "⟨excluídas na leitura⟩": str(ev["ledger"]["EXCLUDED_IN_READING"]),
     "⟨z_disc⟩": fmt(fz["z_disc_calibrado"], 2, False, "pt"), "⟨z_delta⟩": fmt(fz["z_delta_calibrado"], 2, True, "pt"), "⟨lnB⟩": fmt(fz["lnB_lcdm"], 2, False, "pt")}, \
    {"⟨Z against K⟩": fmt(h["primario"]["z_tgl"], 2, True, "en"), "⟨Z against the null⟩": fmt(h["primario"]["z_null"], 2, False, "en"), "⟨n⟩": str(int(math.floor(h["primario"]["z_null"]))),
     "⟨Z of the free Cepheids⟩": fmt(h["cefeidas_livres"]["z_null"], 2, False, "en"), "⟨N charges⟩": str(ev["n_cobrancas"]),
     "⟨not falsified⟩": str(ev["ledger"]["NOT_FALSIFIED"]), "⟨inconclusive⟩": str(ev["ledger"]["INCONCLUSIVE"]),
     "⟨awaiting data⟩": str(ev["ledger"]["AWAITING"]), "⟨excluded in reading⟩": str(ev["ledger"]["EXCLUDED_IN_READING"]),
     "⟨z_disc⟩": fmt(fz["z_disc_calibrado"], 2, False, "en"), "⟨z_delta⟩": fmt(fz["z_delta_calibrado"], 2, True, "en"), "⟨lnB⟩": fmt(fz["lnB_lcdm"], 2, False, "en")}
vpt, ven = vals(None)
exp_pt = T["pt"]; exp_en = T["en"]
for k, v in vpt.items(): exp_pt = exp_pt.replace(k, v)
for k, v in ven.items(): exp_en = exp_en.replace(k, v)
assert "⟨" not in exp_pt and "⟨" not in exp_en
def norm(s):
    s = s.replace("$-$", "-").replace("−", "-")
    s = s.replace("\ln", "ln").replace("\\", "")
    s = re.sub(r"[^\w\-]", "", s, flags=re.U)   # alnum + underscore + hyphen
    s = s.replace("_", "")
    return s
def resumo(txt, ini, fim):
    i = txt.index(ini); j = txt.index(fim, i)
    return txt[i:j]
t = pt(); e = en()
rp = resumo(t, "Dois resultados abrem", "Apresentação do programa terminal")
re_ = resumo(e, "Two results open", "Presentation of the terminal program")  if "Presentation of the terminal program" in e else None
print("EN markers after 'Two results':", e[e.index("Two results open")+len(exp_en)-50: e.index("Two results open")+len(exp_en)+200])
rp_n = norm(rp); ep_n = norm(exp_pt)
print("PT render len", len(rp), "expected len", len(exp_pt))
print("PT igual (norm):", rp_n == ep_n)
if rp_n != ep_n:
    # first diff
    for i,(a,b) in enumerate(zip(rp_n, ep_n)):
        if a != b: print("diff at", i, rp_n[max(0,i-60):i+60], "|||", ep_n[max(0,i-60):i+60]); break
    print(len(rp_n), len(ep_n))
# EN: the resumo end: find where expected ends in render
i = e.index("Two results open")
seg = e[i: i + len(exp_en) + 400]
en_n = norm(exp_en)
sn = norm(e[i: i+ len(exp_en)+300])
print("EN startswith expected (norm):", sn.startswith(en_n))
if not sn.startswith(en_n):
    for k,(a,b) in enumerate(zip(sn, en_n)):
        if a != b: print("diff at", k, sn[max(0,k-60):k+60], "|||", en_n[max(0,k-60):k+60]); break
print("EN after expected:", e[i+len(exp_en)-80:i+len(exp_en)+260])
