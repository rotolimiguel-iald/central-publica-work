import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
fontes = [R + f for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "delta_v409.py", "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_custodia_handoff_v409.py")] + sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt"))
res = {}
for a in fontes:
    t = open(a, encoding="utf-8", errors="replace").read()
    for fr in re.split(r"(?<=[.;])\s+|\n", t):
        if re.search(r"uniforme|uniform", fr) and re.search(r"\[OPEN\]", fr):
            res.setdefault(fr.strip()[:300], set()).add(os.path.basename(a))
for fr, fs in res.items(): print("-", sorted(fs)[:5], "|", fr)
