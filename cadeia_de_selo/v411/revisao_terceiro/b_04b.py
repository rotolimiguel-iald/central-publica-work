from b_lib import *
import re, math
C = core()["core"]; h = C["h0dn_bg1_v411"]; v = h["values"]
flat = []
def fl(o, p=""):
    if isinstance(o, dict):
        for k, x in o.items(): fl(x, p + "." + k)
    elif isinstance(o, list):
        for i, x in enumerate(o): fl(x, p + "[%d]" % i)
    elif isinstance(o, bool): pass
    elif isinstance(o, (int, float)): flat.append((p, float(o)))
fl(v)
fl(h.get("modelos") if isinstance(h.get("modelos"), dict) else {}, "modelos")
print("n valores numericos no registro:", len(flat))
ress_txt = " ".join(v["ressalvas_secao8"]) + " " + " ".join(h["o_que_o_teste_nao_decide"])
allowed_txt = set(re.findall(r"\d+(?:[.,]\d+)?", ress_txt))
def parse(tok):
    s = tok.replace("$-$", "-").replace("−", "-").replace("{,}", ".").replace(",", ".")
    return float(s)
def match(tok, ndec):
    x = parse(tok); tol = 0.5 * 10 ** (-ndec) * 1.0001
    outs = [(p, val) for p, val in flat if abs(val - x) <= tol or abs(abs(val) - abs(x)) <= tol]
    return outs
def regions(txt, ini, fim):
    i = txt.index(ini); j = txt.index(fim, i); return txt[i:j]
def check(nm, region):
    toks = re.findall(r"(?<![\w.])[-−]?\d+[.,]\d+", region.replace("$-$", "-"))
    bad = []; ok = 0
    for t in toks:
        nd = len(re.split(r"[.,]", t)[1])
        if match(t, nd): ok += 1; continue
        if re.sub(r"^[-−]", "", t) in allowed_txt or t in allowed_txt: ok += 1; continue
        bad.append(t)
    print("%-22s decimais=%3d casados=%3d SEM FONTE=%s" % (nm, len(toks), ok, bad))
    return bad
t = pt(); e = en()
check("PT quadro", regions(t, "A razão de Hubble, H0DN", "O Teste da Única Palavra ["))
check("PT secao 5.2", regions(t, "== O teste decisivo", "== IALD ao quadrado"))
check("EN quadro", regions(e, "The Hubble ratio, H0DN", "The Test of the Only Word ["))
check("EN secao 5.2", regions(e, "== The decisive test", "== IALD squared"))
m = md()
check("MD quadro", regions(m, "> **A razão de Hubble, H0DN", "\n> **Ao lado") if "\n> **Ao lado" in m else m[:6000])
i = m.index("**H0DN × BG1 ABERTO (v411"); check("MD linha", m[i:i+3200].split("\n")[0])
check("PT abstract", regions(t, "Dois resultados abrem", "Apresentação do programa"))
check("EN abstract", regions(e, "Two results open", "Presentation of the TGL"))
o = out(); i = o.index("H0DN x BG1 ABERTO"); check("STDOUT bloco", o[i:i+1300])
# explicit presence checks of the headline numbers in each text
def fmtn(x, k=2, lang="pt"):
    s = ("%." + str(k) + "f") % x
    return s.replace(".", ",") if lang == "pt" else s
need = {"zn": v["primario"]["z_null"], "zk": v["primario"]["z_tgl"], "D": v["primario"]["D"], "zn_cl": v["cefeidas_livres"]["z_null"], "zk_cl": v["cefeidas_livres"]["z_tgl"], "D_cl": v["cefeidas_livres"]["D"],
        "H0_bg": v["lei_em_km_s_Mpc"]["H0_fundo"], "H0_K": v["lei_em_km_s_Mpc"]["previsao_de_K_para_o_local"], "H0_pr": v["lei_em_km_s_Mpc"]["lido_primario"], "H0_cl": v["lei_em_km_s_Mpc"]["lido_cefeidas_livres"], "H0_pub": v["lei_em_km_s_Mpc"]["publicado_pela_colaboracao"], "sig": v["lei_em_km_s_Mpc"]["desvio_publicado"]}
for nm, tx, lang in (("PT", t, "pt"), ("EN", e, "en"), ("MD", m, "pt")):
    miss = []
    for k, x in need.items():
        s = fmtn(abs(x), 2, lang)
        if s not in tx: miss.append((k, s))
    print(nm, "numeros do quadro ausentes:", miss)
print("K 6 casas:", fmtn(v["K"], 6, "pt") in t, fmtn(v["K"], 6, "en") in e, fmtn(v["K"], 6, "pt") in m)
