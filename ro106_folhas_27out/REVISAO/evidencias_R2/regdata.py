import fitz, numpy as np, re, unicodedata, collections
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
TOK=re.compile(r"[^\W_]+",re.U)
def toks(s): return collections.Counter(t.lower() for t in TOK.findall(unicodedata.normalize("NFKC",s.replace("\x1c","fi").replace("\x1d","fl"))))
def curves(pg,minpts=8):
    out=[]
    for dr in pg.get_drawings():
        if dr["type"]!="s": continue
        pts=[]
        for it in dr["items"]:
            if it[0]=="l":
                if not pts: pts.append((it[1].x,it[1].y))
                pts.append((it[2].x,it[2].y))
        if len(pts)>=minpts:
            P=np.array(pts); out.append(P)
    return out
def norm(P):
    mn=P.min(0); mx=P.max(0); sp=np.where(mx-mn>0,mx-mn,1); return (P-mn)/sp
for tag,new,old,rot in (("apr",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_094406",None),("mqc",W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf",W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf.bak_20261027_094406",None)):
    a=fitz.open(new); b=fitz.open(old)
    for i in range(len(a)):
        wa=toks(a[i].get_text()); wb=toks(b[i].get_text())
        dif={k:(wb[k],wa[k]) for k in set(wa)|set(wb) if wa[k]!=wb[k]}
        # curves
        ca=curves(a[i]); cb=curves(b[i]); matched=0; maxdev=0.0
        used=set()
        for P in ca:
            best=None
            for j,Q in enumerate(cb):
                if j in used or len(Q)!=len(P): continue
                for NA,NB in ((norm(P),norm(Q)),(norm(P),norm(Q)[::-1])):
                    dev=np.abs(NA-NB).max()
                    if best is None or dev<best[0]: best=(dev,j)
            if best is not None and best[0]<0.02:
                matched+=1; used.add(best[1]); maxdev=max(maxdev,best[0])
        print(tag,"sheet",i+1,"| word-count diffs R1->R2:",dif if dif else "none","| curves(>=8 pts) R2:",len(ca),"R1:",len(cb),"matched by shape:",matched,"max normalized deviation %.4f"%maxdev)
