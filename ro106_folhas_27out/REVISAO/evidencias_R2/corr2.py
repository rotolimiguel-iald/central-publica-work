import sys; sys.argv=["x","222"]
exec(open("corr.py").read().split("res={}")[0])
out={}
for sheet in (5,6,7):
    F=np.load(f"filed_fig{sheet}.npy"); pg=doc[sheet-1]; rects=axes_rects(pg)
    for idx,((x0,x1,y0,y1),R) in enumerate(zip(FR[sheet],rects)):
        sel=selected(pg,R); w,h=x1-x0,y1-y0
        variants={"all":sel,"curves_only":[d for d in sel if max(d["rect"].width,d["rect"].height)>=14]}
        Mf=F[y0:y1,x0:x1]<THR; ins=6
        Mf[:ins,:]=0;Mf[-ins:,:]=0;Mf[:,:ins]=0;Mf[:,-ins:]=0
        row={}
        for vn,s in variants.items():
            if vn=="curves_only" and sheet==7: continue
            if not s: continue
            Mn=render_selected(pg,R,s,(w,h)); Mn[:ins,:]=0;Mn[-ins:,:]=0;Mn[:,:ins]=0;Mn[:,-ins:]=0
            band=ndimage.binary_dilation(Mn,iterations=40)
            for sig in (4,12,20):
                gn=ndimage.gaussian_filter(Mn.astype(float),sig); best=(-2,None)
                for dy in range(-16,17,4):
                    for dx in range(-16,17,4):
                        gf=ndimage.gaussian_filter(np.roll(np.roll(Mf,dy,0),dx,1).astype(float),sig)
                        c=ncc(gf,gn,band)
                        if c>best[0]: best=(c,(dx,dy))
                row[f"{vn}_sigma{sig}"]=(round(best[0],3),best[1])
        out[f"{sheet}{'abc'[idx]}"]=row
        print(f"fig {sheet}{'abc'[idx]}:",row)
json.dump(out,open("corr2.json","w"),indent=1)
