import sys; sys.argv=["x","222"]
exec(open("corr.py").read().split("res={}")[0])
from PIL import Image
def ov(sheet,idx,name):
    F=np.load(f"filed_fig{sheet}.npy"); pg=doc[sheet-1]; rects=axes_rects(pg)
    x0,x1,y0,y1=FR[sheet][idx]; R=rects[idx]; sel=selected(pg,R)
    Mn=render_selected(pg,R,sel,(x1-x0,y1-y0)); Mf=F[y0:y1,x0:x1]<THR
    img=np.full(Mn.shape+(3,),255,np.uint8)
    img[Mf]=(255,0,0); img[Mn]=(0,160,0); img[Mf&Mn]=(0,0,0)
    Image.fromarray(img).resize((img.shape[1]//2,img.shape[0]//2)).save(name)
ov(5,0,"ov_5a.png"); ov(7,1,"ov_7b.png"); ov(7,0,"ov_7a.png")
