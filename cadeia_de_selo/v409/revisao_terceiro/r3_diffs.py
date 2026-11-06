import difflib, glob, os, sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
r2 = json.load(open(R + "revisao_terceiro/REVISAO_TERCEIRO_v409.R2.json", encoding="utf-8"))["arquivos_revisados"]
for a in ("registros_v409.py", "runtime_v409.py", "guarda_frases_v409.py", "delta_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "pos_rito/textos_v409_novo.pysnip", "pos_rito/CUSTODIA_v409_RASCUNHO.txt"):
    baks = sorted(glob.glob(R + a + ".bak_*"), key=os.path.getmtime)
    achado = [b for b in baks if hashlib.sha256(open(b, "rb").read()).hexdigest()[:16] == r2[a]]
    if not achado: print("==", a, "bak da R2 nao encontrado"); continue
    old = open(achado[-1], encoding="utf-8").read().split("\n"); new = open(R + a, encoding="utf-8").read().split("\n")
    d = [l for l in difflib.unified_diff(old, new, "R2", "R3", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    print("==", a, "| -/+:", sum(1 for l in d if l[0] == "-"), sum(1 for l in d if l[0] == "+"))
    for l in d[:30]: print("   ", l[:420])
