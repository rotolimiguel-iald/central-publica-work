import json, re, unicodedata, collections, fitz
TOK=re.compile(r"[^\W_\d]+",re.U)   # letters only
def toks(s):
    s=unicodedata.normalize("NFKC",s)
    return [t.lower() for t in TOK.findall(s)]
F={}
for fn in ("ocr_filed.json","ocr_filed_rot.json"):
    for e in json.load(open(fn,encoding="utf-8-sig")):
        k=re.sub(r"_(x\d|r90|r270)\.png$","",e["file"])
        lines=e["lines"] if isinstance(e["lines"],list) else [e["lines"]]
        F.setdefault(k,set()).update(toks(" ".join(lines)))
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
L={}
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for i,pg in enumerate(d): L[f"{n}_{i+1}"]=set(toks(pg.get_text()))
plan={"050576":{1:[1],2:[2,3],3:[4,5],4:[6,7],5:[8],6:[9]},"050579":{i:[i] for i in range(1,9)}}
key={"050576":"apr","050579":"mqc"}
for n,pl in plan.items():
    for sh,figs in pl.items():
        a=set()
        for f in figs: a|=F[f"filed_{key[n]}_fig{f}"]
        live=L[f"{n}_{sh}"]
        print(f"== {n} sheet {sh}\n   newlive-not-in-filedOCR: {sorted(w for w in live if w not in a and len(w)>1)}\n   filedOCR-not-in-newlive(len>2): {sorted(w for w in a if w not in live and len(w)>2)}")
