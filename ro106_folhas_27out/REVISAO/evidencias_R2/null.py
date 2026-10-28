import sys; sys.argv=["x","222"]
exec(open("corr.py").read().split("res={}")[0])
# null: filed panel i vs new panel j (same figure, i != j); same sizes
for sheet in (5,6):
    F=np.load(f"filed_fig{sheet}.npy"); pg=doc[sheet-1]; rects=axes_rects(pg)
    mats={}
    for idx,((x0,x1,y0,y1),R) in enumerate(zip(FR[sheet],rects)):
        sel=[d for d in selected(pg,R) if max(d["rect"].width,d["rect"].height)>=14]
        w,h=x1-x0,y1-y0
        Mn=render_selected(pg,R,sel,(w,h)); Mf=F[y0:y1,x0:x1]<THR
        for M in (Mn,Mf): M[:6,:]=0;M[-6:,:]=0;M[:,:6]=0;M[:,-6:]=0
        mats[idx]=(ndimage.gaussian_filter(Mf.astype(float),4),ndimage.gaussian_filter(Mn.astype(float),4),Mn)
    for i in range(3):
        row=[]
        for j in range(3):
            band=ndimage.binary_dilation(mats[j][2],iterations=40)
            row.append(round(ncc(mats[i][0],mats[j][1],band),3))
        print("fig",sheet,"filed panel","abc"[i],"vs new panels a,b,c:",row)
