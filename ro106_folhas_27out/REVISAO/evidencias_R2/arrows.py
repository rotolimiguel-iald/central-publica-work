import fitz, numpy as np
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
def heads(path):
    d=fitz.open(path); pg=d[0]; H=pg.rect.height; out=[]
    for dr in pg.get_drawings():
        if dr.get("fill")==(0.0,0.0,0.0) and dr["rect"].width<14 and dr["rect"].height<14 and dr["rect"].width>2 and len(dr["items"])>=3:
            pts=[]
            for it in dr["items"]:
                if it[0]=="l": pts+=[it[1],it[2]]
                elif it[0]=="c": pts+=[it[1],it[4]]
            P=np.array([(p.x,p.y) for p in pts]); 
            P=np.unique(np.round(P,2),axis=0)
            c=P.mean(0); dist=np.linalg.norm(P-c,axis=1); tip=P[dist.argmax()]; v=tip-c; v/= np.linalg.norm(v)
            # sheet -> upright: (dx,dy)->(-dy,dx); position (x,y)->(H-y,x)
            up_v=(-v[1],v[0]); up_pos=(H-tip[1],tip[0])
            dirn="right" if abs(up_v[0])>abs(up_v[1]) and up_v[0]>0 else "left" if abs(up_v[0])>abs(up_v[1]) else ("down" if up_v[1]>0 else "up")
            out.append((round(up_pos[0]),round(up_pos[1]),dirn))
    return sorted(out)
for n,p in (("apr R2",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf"),("alt R2",W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf"),("apr R1",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_094406")):
    print(n,heads(p))
