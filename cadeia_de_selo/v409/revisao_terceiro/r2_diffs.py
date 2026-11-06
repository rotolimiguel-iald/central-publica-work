import difflib, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
alvos = ["registros_v409.py", "runtime_v409.py", "guarda_frases_v409.py", "delta_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "pos_rito/textos_v409_novo.pysnip", "pos_rito/CUSTODIA_v409_RASCUNHO.txt"]
for a in alvos:
    baks = sorted(glob.glob(R + a + ".bak_*"), key=os.path.getmtime)
    # o bak mais recente cujo conteudo e' o da R1 (sha16 conhecido)? usamos o mais recente anterior ao arquivo atual
    import hashlib
    r1 = {"registros_v409.py": "7cf94c9bfacccb81", "runtime_v409.py": "38cfee4e7bb83d45", "guarda_frases_v409.py": "ca4da17f9394d844", "delta_v409.py": "cdce507a5ce82c97", "artigo_pt_v409.pysnip": "d80e772b134be24f", "artigo_en_v409.pysnip": "32e20a39e5b0e4ae", "pos_rito/textos_v409_novo.pysnip": "1b073b0370a11732", "pos_rito/CUSTODIA_v409_RASCUNHO.txt": "c74ae1d1b3b3abf0"}[a]
    achado = [b for b in baks if hashlib.sha256(open(b, "rb").read()).hexdigest()[:16] == r1]
    if not achado: print("==", a, "bak da R1 nao encontrado; baks:", [os.path.basename(b) for b in baks][-3:]); continue
    old = open(achado[-1], encoding="utf-8").read().split("\n"); new = open(R + a, encoding="utf-8").read().split("\n")
    d = [l for l in difflib.unified_diff(old, new, "R1", "R2", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    print("==", a, "| linhas -/+:", sum(1 for l in d if l[0] == "-"), sum(1 for l in d if l[0] == "+"))
    for l in d[:40]: print("   ", l[:330])
